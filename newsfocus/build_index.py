from elasticsearch import Elasticsearch, helpers
import json
import sys

class NewsElasticSearch:

	def __init__(self, index_name, doc_type):
		self.es = Elasticsearch()
		self.index_name = index_name
		self.doc_type = doc_type

	def load_data(self, filename):
		with open(filename, 'r') as infile:
			self.data = json.load(infile)

	def load_schema(self, filename):
		with open(filename, "r") as infile:
			self.schema = json.load(infile)

	def populate_schema(self, filename):
		schema = {
			"settings": {
				"index": {
					"analysis": {
						"analyzer": {
							"snowball_analyzer": {
								"type": "snowball",
								"language": "English"
							},
							"analyzer_lower": {
								"type": "standard",
								"lowercase": "true"
							}
						}
					}
				}
			},
			"mappings": {
				"movie": {
					"properties": {
						"title": {"type": "string", "analyzer": "analyzer_lower", "index_options": "offsets"},
						"abstract": {"type": "string", "analyzer": "analyzer_lower", "index_options": "offsets"},
						"byline": {"type": "string", "analyzer": "analyzer_lower", "index_options": "offsets"},
						"content": {"type": "string", "analyzer": "snowball_analyzer", "index_options": "offsets"},
						"section": {"type": "string", "store" : "yes", "include_in_all" : False},
						"url": {"type": "string", "store" : "yes", "include_in_all" : False},
						"item_type": {"type": "string", "store" : "yes", "include_in_all" : False},
						"date": {"type": "date", "store" : "yes", "include_in_all" : False},
					}
				}
			}
		}
		with open(filename, "w") as outfile:
			json.dump(schema, outfile, indent = 4)

	def create_index(self):
		if not self.es.indices.exists(index = self.index_name):
			self.index = self.es.indices.create(index = self.index_name, body = self.schema)
			return self.schema

	def delete_index(self):
		if self.es.indices.exists(index = self.index_name):
			self.es.indices.delete(index = self.index_name)

	def format_action(self, key, value):
		""" This method returns the correct format for the bulk action """

		return {
				"_index" : self.index_name,
				"_type" : self.doc_type,
				"_id": int(key),
				"_source": value
		}

	def bulk_insert(self):
		""" This module bulk inserts the given max_size number of records in the "i_novels" index """
		actions = []
		for key, value in self.data.iteritems():
			actions.append(self.format_action(key, value))
		return helpers.bulk(self.es, actions, stats_only = True)

	def q_field(self, field_name, value):
		""" Return docs and their field values (for specified field) """

		query_body = {
			"query": {
				"match": {
					field_name : value
				}
			}
		}
		result = self.es.search(index = self.index_name, doc_type = self.doc_type, body = query_body)
		return result['hits']['hits']

if __name__ == '__main__':
	esEngine = NewsElasticSearch(index_name = "es_news", doc_type = "news")
	#esEngine.load_data(filename = "datasets/food_news.json")
	#esEngine.populate_schema(filename = "schema")
	#esEngine.load_schema(filename = "schema")
	#esEngine.delete_index()
	#esEngine.create_index()
	#esEngine.bulk_insert()
	print esEngine.q_field('content', 'fish')
