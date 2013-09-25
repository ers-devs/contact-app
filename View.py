'''
@author: cgueret
'''
from gi.repository import Gtk
	
class View(object):
	def __init__(self, model):
		'''
		Constructor
		'''
		# Keep a pointer to the model
		self._model = model
		
		# Load the graphical user interface
		self._gui = Gtk.Builder()
		self._gui.add_from_file("ui.glade")
		
	def get_widget(self):
		'''
		Return the main widget of the application
		'''
		return self._gui.get_object("main")

	def get_object(self, object_name):
		'''
		Return an object from the GUI
		'''
		return self._gui.get_object(object_name)