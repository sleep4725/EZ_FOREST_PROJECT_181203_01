# tb_frip_categorycode => categorycode | 서비스 분류 코드 | 한국관광공사
from Elasticsearch.Server import Elastic

class Tourcategorycode():
    elasticnode = Elastic()
    es = elasticnode.es
    @classmethod
    def indexCreate(cls):
        cls.es.indices.create(
            index=str("tb_frip_categorycode").lower(),
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