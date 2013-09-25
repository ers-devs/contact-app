'''
Created on 11 Jan 2013

@author: cgueret
'''
from gi.repository import Gtk, Gio
from View import View
from Controller import Controller
from Model import Model

class ContactApplication(Gtk.Application):
	def __init__(self):
		Gtk.Application.__init__(self, application_id="ers.Contact", flags=Gio.ApplicationFlags.FLAGS_NONE)
		self.connect("activate", self.on_activate)
		
	def on_activate(self, data=None):
		# Create the model
		model = Model()
		
		# Create the view
		view = View(model)
		
		# Create the controller
		controller = Controller(view, model)
		
		# Create the window		
		window = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
		window.set_default_size(600,450)
		window.set_title("Contact")
		window.set_border_width(2)
		window.set_position(Gtk.WindowPosition.CENTER)
		window.add(view.get_widget())
		
		# Show the window and add it to the application
		window.show_all()
		self.add_window(window)
				
if __name__ == "__main__":
	app = ContactApplication()
	app.run(None)
