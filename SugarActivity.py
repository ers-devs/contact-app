'''
@author: cgueret
'''
from gi.repository import Gtk

from sugar3.activity import activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import ActivityButton
from sugar3.activity.widgets import TitleEntry
from sugar3.activity.widgets import StopButton
from sugar3.activity.widgets import DescriptionItem

from View import View
from Controller import Controller
from Model import Model

class QuizActivity(activity.Activity):
	def __init__(self, handle):
		'''
		Initialise the activity
		'''
		activity.Activity.__init__(self, handle)
		
		# Create the model
		model = Model()
		
		# Create the view
		view = View(model)
		
		# Create the controller
		controller = Controller(view, model)
		
		# Sugar toolbar with the new toolbar redesign
		toolbar_box = ToolbarBox()
		
		activity_button = ActivityButton(self)
		toolbar_box.toolbar.insert(activity_button, 0)
		activity_button.show()
		
		title_entry = TitleEntry(self)
		toolbar_box.toolbar.insert(title_entry, -1)
		title_entry.show()
		
		description_item = DescriptionItem(self)
		toolbar_box.toolbar.insert(description_item, -1)
		description_item.show()
		
		separator = Gtk.SeparatorToolItem()
		separator.props.draw = False
		separator.set_expand(True)
		toolbar_box.toolbar.insert(separator, -1)
		separator.show()
		
		stop_button = StopButton(self)
		toolbar_box.toolbar.insert(stop_button, -1)
		stop_button.show()
		
		self.set_toolbar_box(toolbar_box)
		toolbar_box.show()
		
		# Set the canvas		
		self.set_canvas(view.get_widget())
		self.canvas.show()
