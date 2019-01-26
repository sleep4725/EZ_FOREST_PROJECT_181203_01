# tb_frip_tourareacode => tourareacode | 지역코드 | 한국관광공사

from Elasticsearch.Server import Elastic

class Tourareacode():
    elasticnode = Elastic()
    es = elasticnode.es
    @classmethod
    def indexCreate(cls):
        cls.es.indices.create(
            index=str("tb_frip_tourareacode").lower(),
            body={
                "mappings": {
                    "doc": {
                        "properties": {
                            "code": {
                                "type": "text"
                            },
                            "name": {
                                "type": "integer"
                            }
                        }
                    }
                }
            }
        )