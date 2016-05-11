import json
from pprint import pprint
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch import helpers

class MyElasticsearch():
    def __init__(self, data, schema):
        self.es = Elasticsearch()
        self.data = data
        self.schema = schema

    def create_news_index(self):
        if self.es.indices.exists("es_news"):
            self.es.indices.delete(index='es_news')
        self.es.indices.create(index = "es_news", body = self.schema)


    def format_action(self, id, value):
        return {
            "_index": "es_news",
            "_type": "news",
            "_id": id,
            "_source": value
        }

    def bulk_insert(self):
        actions = []
        for key, value in self.data.iteritems():
            #value contains "related_urls" field that we don't map.
            value2 = {}
            value2['section'] = value['section']
            value2['title'] = value['title']
            value2['abstract'] = value['abstract']
            value2['url'] = value['url']
            value2['content'] = value['content']
            value2['byline'] = value['byline']
            value2['thumbnail_standard'] = value['thumbnail_standard']
            value2['source'] = value['source']
            value2['published_date'] = value['published_date']
            value2['des_facet'] = value['des_facet']
            value2['geo_facet'] = value['geo_facet']
            actions.append(self.format_action(key, value2))
        helpers.bulk(self.es, actions, stats_only=True)

    def q_category(self, field_name, value):
        query_body={
            "query":{
                "match":{
                    field_name: value
                }
            }
        }
        res = self.es.search(index="es_news", doc_type="news", body=query_body)
        return res['hits']['hits']

    def q_keywords(self, value):
        query_body={
            "query":{
                "multi_match":{
                    "query": value,
                    "fields": ["section^1", "title^3", "abstract^2", "content^2", "byline^1", "source^1", "des_facet^1", "geo_facet^1"]
                }
            }
        }
        res = self.es.search(index="es_news", doc_type="news", body=query_body)
        return res['hits']['hits']

    def q_nicesearch(self, keywords, ctg=["food", "art", "business", "health", "science", "sport", "travel", "world"], daterange="01/01/2010 - 05/10/2016"):
        dateList = daterange.split("-")
        query_body={
            "query":{
                "bool":{
                    "must":{
                        "multi_match":{
                            "section" : ctg,
                        }},
                    "must":{
                        "range":{
                            "published_date": {"gte": dateList[0].strip(), "lte": dateList[1].strip(), "format": "MM/dd/yyyy"}
                        }},
                    "must":{
                        "multi_match":{
                            "query": keywords,
                            "fields": ["section^1", "title^3", "abstract^2", "content^2", "byline^1", "source^1", "des_facet^1", "geo_facet^1"]
                        }
                    }
                }
            }
        }
        res = self.es.search(index="es_news", doc_type="news", body=query_body)
        return res['hits']['hits']

with open("all_news.json") as data_file:
    data = json.load(data_file)
with open("es_mapping_file.json") as data_file2:
    schema = json.load(data_file2)
myElasticsearch = MyElasticsearch(data, schema)
# myElasticsearch.create_news_index()
# myElasticsearch.bulk_insert()
#rs = myElasticsearch.es.search(index="es_news", body={"query":{"match_all":{}}})
a="statins may help"
s="01/01/2014 - 02/28/2016"
rs2 = myElasticsearch.q_nicesearch(keywords=a,daterange=s)
#print rs['hits']['total']
print rs2[0]['_source']['title']
#print rs3[0]['_source']['section']
