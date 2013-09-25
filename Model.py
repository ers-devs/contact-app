'''
@author: cgueret
'''
import os
import sys
TESTS_PATH = os.path.dirname(os.path.realpath(__file__))
ERS_PATH = os.path.join(os.path.dirname(TESTS_PATH), 'ers/ers-local')
sys.path.insert(0, ERS_PATH)
from ers import ERSLocal
import getpass

class Model(object):
	def __init__(self):
		'''
		Constructor
		'''
		
		# Create an instance of ERS
		self._ers = ERSLocal(reset_database=False)
		
		# Generate a resource name for the owner profile
		entity_name = 'urn:ers:app:Contact:' + self._ers.get_machine_uuid()
		
		# Create the local profile ?
		if not self._ers.contains_entity(entity_name):
			entity = self._ers.create_entity(entity_name)
			entity.add_property("rdf:type", "foaf:Person")
			entity.add_property("foaf:name", getpass.getuser())
			self._ers.persist_entity(entity)
			
	def get_contacts(self):
		'''
		Get the list of visible contacts
		'''
		# Issue a search with ERS
		list = self._ers.search("rdf:type", "foaf:Person")
		
		# Return the list
		return list
			
	def get_entity_description(self, entity_name):
		'''
		Get all the available data about the selected entity
		'''
		# Get all the (accessible) documents describing that identifier
		entity = self._ers.get_entity(entity_name)
		
		# Get the aggregated description
		description = entity.get_properties()
		
		# Return it
		return description
	
	def add_property(self, entity_name, property, value):
		'''
		Complete the description of an entity with a new property/value
		'''
		entity = self._ers.get_entity(entity_name)
		entity.add_property(property, value)
		self._ers.persist_entity(entity)
		
	def delete_property(self, entity_name, property, value):
		'''
		Remove a given triple entity_name/property/value
		'''
		entity = self._ers.get_entity(entity_name)
		entity.delete_property(property, value)
		self._ers.persist_entity(entity)
		