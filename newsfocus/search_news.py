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
    return res['hits']['hits']
