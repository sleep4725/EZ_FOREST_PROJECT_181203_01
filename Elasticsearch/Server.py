from elasticsearch import Elasticsearch, ElasticsearchException
from yaml import load
import sys
import os
#
#  @ kimjh
#
# ============================================
class Srv:
    @classmethod
    def servReturn(cls):
        es = None
        healthcheck = None
        try:
            f = open("elasticinfo", "r", encoding="utf-8")
        except FileNotFoundError as e:
            print (e)
            sys.exit(1)
        else:
            text = load(f.read())
            es = Elasticsearch(hosts=text["srvip"], port=text["port"])
            healthcheck = es.cluster.health()['status']
            if healthcheck != "green" and healthcheck != "yellow":
                sys.exit(1)
            else: # healthcheck == "green" or == "yellow"
                return es

class Elastic:
    def __init__(self):
        self.es = Srv.servReturn()
