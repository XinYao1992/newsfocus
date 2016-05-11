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

    def q_category(self, value):
        query_body={
            "query":{
                "match":{
                    "section": value
                }
            }
        }
        res = self.es.search(index="es_news", doc_type="news", body=query_body)
        res = res['hits']['hits']
        resList = []
        #with open("some_news.json") as data_file:
        #    data = json.load(data_file)
        for n in res:
            normalized_res = {}
            normalized_res['id'] = n['_id']
            normalized_res['byline'] = n['_source']['byline']
            normalized_res['title'] = n['_source']['title']
            normalized_res['abstract'] = n['_source']['abstract']
            normalized_res['content'] = n['_source']['content']
            normalized_res['url'] = n['_source']['url']
            normalized_res['section'] = n['_source']['section']
            normalized_res['published_date'] = n['_source']['published_date']
        #    if data[n['_id']]['related_urls'] is None:
        #        normalized_res['related_urls'] = []
        #    else:
        #        normalized_res['related_urls'] = data[n['_id']]['related_urls']
            resList.append(normalized_res)
        return resList

    # def q_keywords(self, value):
    #     query_body={
    #         "query":{
    #             "multi_match":{
    #                 "query": value,
    #                 "fields": ["section^1", "title^3", "abstract^2", "content^2", "byline^1", "source^1", "des_facet^1", "geo_facet^1"]
    #             }
    #         }
    #     }
    #     res = self.es.search(index="es_news", doc_type="news", body=query_body)
    #     return res['hits']['hits']

    def q_nicesearch(self, keywords, ctg=["food", "art", "business", "health", "science", "sport", "travel", "world"], daterange="2010-01-01 | 2016-05-10"):
        dateList = daterange.split("|")
        query_body={
            "query":{
                "bool":{
                    "must":[
                        {"bool":{
                            "must":[
                                {"range":{
                                    "published_date": {"gte": dateList[0].strip(), "lte": dateList[1].strip(), "format": "yyyy-MM-dd"}
                                }},
                                {"multi_match":{
                                    "query": keywords,
                                    "fields": ["section^1", "title^3", "abstract^2", "content^2", "byline^1", "source^1", "des_facet^1", "geo_facet^1"]
                                }}
                            ]
                        }},
                        {"bool":{
                            "should":[]
                        }}
                    ]
                }
            }
        }
        for c in ctg:
            query_body['query']['bool']['must'][1]['bool']['should'].append({"match": {"section" : c}})
        res = self.es.search(index="es_news", doc_type="news", body=query_body)
        res = res['hits']['hits']
        resList = []
        #with open("some_news.json") as data_file:
        #    data = json.load(data_file)
        for n in res:
            normalized_res = {}
            normalized_res['id'] = n['_id']
            normalized_res['byline'] = n['_source']['byline']
            normalized_res['title'] = n['_source']['title']
            normalized_res['abstract'] = n['_source']['abstract']
            normalized_res['content'] = n['_source']['content']
            normalized_res['url'] = n['_source']['url']
            normalized_res['section'] = n['_source']['section']
            normalized_res['published_date'] = n['_source']['published_date']
            #if data[n['_id']]['related_urls'] is None:
            #    normalized_res['related_urls'] = []
            #else:
            #    normalized_res['related_urls'] = data[n['_id']]['related_urls']
            resList.append(normalized_res)
        return resList

with open("some_news.json") as data_file:
    data = json.load(data_file)
with open("es_mapping_file.json") as data_file2:
    schema = json.load(data_file2)
myElasticsearch = MyElasticsearch(data, schema)
myElasticsearch.create_news_index()
myElasticsearch.bulk_insert()
# with open("all_news.json") as data_file:
#     data = json.load(data_file)
# with open("es_mapping_file.json") as data_file2:
#     schema = json.load(data_file2)
# myElasticsearch = MyElasticsearch(data, schema)
# myElasticsearch.create_news_index()
# myElasticsearch.bulk_insert()
#rs = myElasticsearch.es.search(index="es_news", body={"query":{"match_all":{}}})
# a="statins may help"
# s="01/01/2014 - 02/28/2016"
# rs2 = myElasticsearch.q_nicesearch(keywords=a,daterange=s)
#print rs['hits']['total']
# print rs2[0]['_source']['title']
a="statins may help"
c=['health']
s="2014-01-01 | 2016-01-01"
#rs1 = myElasticsearch.q_category('science')
rs2 = myElasticsearch.q_nicesearch(keywords=a,ctg=c,daterange=s)
#print rs['hits']['total']
print rs2[0]
print rs2
#print rs3[0]['_source']['section']
