from elasticsearch import Elasticsearch

def searchByCategory(value):
    es = Elasticsearch()
    indexName = "es_news"
    doc_type = "news"
    query_body={
        "query":{
            "match":{
                "section": value
            }
        }
    }
    res = es.search(index=indexName, doc_type=doc_type, body=query_body)
    res = res['hits']['hits']
    resList = []
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
        resList.append(normalized_res)
    return resList

def niceSearch(keywords, ctg=["food", "art", "business", "health", "science", "sport", "travel", "world"], daterange="2010-01-01 | 2016-05-10"):
    es = Elasticsearch()
    indexName = "es_news"
    doc_type = "news"
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
    res = es.search(index=indexName, doc_type=doc_type, body=query_body)
    res = res['hits']['hits']
    resList = []
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
        resList.append(normalized_res)
    return resList
