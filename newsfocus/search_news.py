from elasticsearch import Elasticsearch
import shelve
import json

with open("newsfocus/some_news.json") as df:
    data = json.load(df)
myShelve = shelve.open("all_news_shelve")
try:
    for key, value in data.iteritems():
        myShelve[str(key)] = value
finally:
    myShelve.close()

def search_by_category(ctg):
    es = Elasticsearch()
    indexName = "es_news"
    doc_type = "news"
    query_body={
        "from": 0, "size":30,
        "query":{
            "match":{
                "section": ctg
            }
        }
    }
    res = es.search(index=indexName, doc_type=doc_type, body=query_body)
    return format_output(res['hits']['hits'])


def search_by_all(keywords, ctg=None, daterange=None):
    if ctg == None:
        ctg = ["food", "art", "business", "health", "science", "sport", "travel", "world"]
    if daterange == None:
        daterange = "01/01/2010 - 05/10/2016"
    dateList = daterange.split("-")
    query_body={
        "from": 0, "size":30,
        "query":{
            "bool":{
                "must":[
                    {"bool":{
                        "must":[
                            {"range":{
                                "published_date": {"gte": dateList[0].strip(), "lte": dateList[1].strip(), "format": "MM/dd/yyyy"}
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
    es = Elasticsearch()
    res = es.search(index="es_news", doc_type="news", body=query_body)
    return format_output(res['hits']['hits'])

def format_output(output):
    all_news = shelve.open("all_news_shelve")
    resList = []
    for n in output:
        normalized_res = {}
        normalized_res['id'] = n['_id']
        normalized_res['byline'] = n['_source']['byline']
        normalized_res['title'] = n['_source']['title']
        normalized_res['abstract'] = n['_source']['abstract']
        normalized_res['content'] = n['_source']['content']
        normalized_res['url'] = n['_source']['url']
        normalized_res['section'] = n['_source']['section']
        normalized_res['published_date'] = n['_source']['published_date']
        normalized_res['thumbnail_standard'] = n['_source']['thumbnail_standard']
        if all_news[str(n['_id'])]['related_urls'] is None:
            normalized_res['related_urls'] = []
        else:
            normalized_res['related_urls'] = all_news[str(n['_id'])]['related_urls']
        resList.append(normalized_res)
    return resList
