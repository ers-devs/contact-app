'''
@author: cgueret
'''
from gi.repository import GLib, Gtk

class Controller(object):
	def __init__(self, view, model):
		'''
		Constructor
		'''
		# Keep a pointer to the view and the model
		self._model = model
		self._view = view

		# Local variables
		self._selected_entity_name = None
		
		# Get a pointer to some objects from the interface
		contact_list_obj = self._view.get_object('contacts_list')
		button_newprop = self._view.get_object('button_newprop')
		
		# Connect the signals
		contact_list_obj.connect("cursor-changed", self._contact_selected_cb)
		button_newprop.connect("clicked", self._new_prop_clicked_cb)
		self._view.get_object('button_keep').connect("clicked", self._keep_clicked_cb)
		
		# Add a timeout to update contacts and force first call
		self._previous_contact_list = None
		self._update_contacts_cb(contact_list_obj)
		GLib.timeout_add_seconds(2, self._update_contacts_cb, contact_list_obj)

		# FIXME Sometimes contacts get stuck. We just force update every 30sec for now. 
		GLib.timeout_add_seconds(30, self._force_update_contacts_cb, contact_list_obj)

		# Hack to clean the grid
		self._grid_objs = []
		
	def _contact_selected_cb(self, obj):
		'''
		Called when a contact is selected
		'''
		# Get the identifier of the entity the user selected

		# If this fails, probably contacts have changed,
		# so we update the list of contacts and exit
		try:
			selected_row = obj.get_selection().get_selected_rows()[1][0][0]
			identifier = obj.get_model()[selected_row][0]
		except:
			self._update_contacts_cb(obj)
			return
		
		# Get the entity description from the model
		self._selected_entity_name = identifier
		
		# Refresh the display of the description
		self.refresh_entity_description()
		
		# Refresh the activation of the buttons
		self.refresh_toolbar_buttons()
			
	def _new_prop_clicked_cb(self, obj):
		'''
		Called when the button to add a new property/value is pressed
		'''
		# Get the selected property (return if none)
		property_obj = self._view.get_object('combobox1')
		tree_iter = property_obj.get_active_iter()
		if tree_iter == None:
			return
		model = property_obj.get_model()
		property = model[tree_iter][1]
		
		# Get the value (return if blank
		value = self._view.get_object('entry1').get_text()
		if value == '':
			return
		
		# Add the property/value to the description of the entity
		self._model.add_property(self._selected_entity_name, property, value)
		
		# Clear the input field
		self._view.get_object('entry1').set_text('')
		
		# Refresh the display
		self.refresh_entity_description()
				
	def _delete_prop_clicked_cb(self, obj, params):
		'''
		Called when the button to delete a property/value is pressed
		'''
		# Delete the property/value to the description of the entity
		self._model.delete_property(self._selected_entity_name, params['property'], params['value'])
		
		# Refresh the display
		self.refresh_entity_description()
		
	def _update_contacts_cb(self, obj):
		'''
		Called on a regular basis to update the list of contacts available
		'''
		contacts = sorted(self._model.get_contacts())
		if self._previous_contact_list == None or self._previous_contact_list != contacts:
			self._previous_contact_list = contacts
			contacts_list = obj.get_model()
			contacts_list.clear()
			for contact in contacts:
				# By default, show the URN
				contact_diplay_name = contact
				# If the contact is ourselves, display "Me"
				if contact == self._model.get_own_contact_name():
					contact_diplay_name = 'Me'
				# Add the entry
				contacts_list.append(row=[contact, contact_diplay_name])
		return True

	def _force_update_contacts_cb(self, obj):
		self._previous_contact_list = None
		self._update_contacts_cb(obj)
	
	def _keep_clicked_cb(self, obj):
		'''
		Called then the keep button is pressed
		'''
		self._model.cache_entity(self._selected_entity_name)
		self.refresh_toolbar_buttons()
		
	def refresh_entity_description(self):
		'''
		Display all the properties of an entity in a grid
		'''
		# Get the description
		entity = self._model.get_entity_description(self._selected_entity_name)
		
		# Get and clear the grid
		grid_obj = self._view.get_object('grid1')
		for obj in self._grid_objs:
				grid_obj.remove(obj)
		self._grid_objs = []
		
		# Push the new content starting from the bottom with the new entry widgets
		anchor_obj = self._view.get_object('combobox1')
		for key, values in entity.iteritems():
			for value in values:
				# Create the widgets
				label_key = Gtk.Label(key)
				label_key.set_justify(Gtk.Justification.LEFT)
				label_value = Gtk.Label(value)
				label_value.set_justify(Gtk.Justification.LEFT)
				label_value.set_line_wrap(True)
				button = Gtk.Button(stock=Gtk.STOCK_DELETE)
				
				# Pack them
				grid_obj.attach_next_to(label_key, anchor_obj, Gtk.PositionType.TOP, 1, 1)
				grid_obj.attach_next_to(label_value, label_key, Gtk.PositionType.RIGHT, 1, 1)
				grid_obj.attach_next_to(button, label_value, Gtk.PositionType.RIGHT, 1, 1)
				
				# Move to the next line
				anchor_obj = label_key
				
				# Connect click handler for property deletion
				params = {'property' : key, 'value' : value}
				button.connect("clicked", self._delete_prop_clicked_cb, params)
		
				# Hack to clean the grid
				self._grid_objs.append(label_key)
				self._grid_objs.append(label_value)
				self._grid_objs.append(button)
				
		# Show the content of the new grid
		grid_obj.show_all()
		
	def refresh_toolbar_buttons(self):
		'''
		Update the status of the buttons in the toolbar depending on the contact selected
		'''
		# Keep button is enabled by default...
		keep_button_obj = self._view.get_object('button_keep')
		keep_button_obj.set_sensitive(True)
		
		# disabled for the owner profile
		if self._selected_entity_name == self._model.get_own_contact_name():
			keep_button_obj.set_sensitive(False)
			
		# and disabled for contacts that are already in cache
		if self._model.is_cached(self._selected_entity_name):
			keep_button_obj.set_sensitive(False)
					
