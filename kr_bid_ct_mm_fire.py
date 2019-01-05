'''
@ junhyeon.kim
@ emil - sleep4725@naver.com
@ 산불위험예보 서비스
'''
# ==================================
import requests
from yaml import load, load_all, YAMLError
import sys
from urllib.parse import urlencode
import pprint
import re
import json
# ==================================
class PROJ:
    # 생성자
    def __init__(self):
        self.url_target = None
        self.url_path   = None
        self.params = {
            "serviceKey":None, "pageNo":None, "numOfRows":None, "ffDt":None, "_type":None,
        }
        self.yaml_doc = None
        self.resp_data = None
        self.json_data = []
        self.f = None
        self.jsonFileCreate()  # function call

    # instance method - 0
    # json 파일 생성
    def jsonFileCreate(self):
        try:
            self.f = open("./OUTPUT/MM_JSON/mm_fire.json", "x")
        except FileExistsError as e:
            # 파일이 존재하지 않는 경우
            print (e)
        else:
            self.f.close()

    # instance method - 1
    # yaml 파일 읽어 오기
    def paramsSett(self):
        try:
            with open("./CONF/FR/data_go_kr_mm_fire", "r", encoding="utf-8") as f:
                self.yaml_doc = load(f)
                f.close()
        except FileNotFoundError as e: # 해당 파일이 존재하지 않는 경우
            print (e)
            sys.exit(1)   # program 종료
        except YAMLError as e:
            print(e)
            sys.exit(1)  # program 종료
        else:
            print (self.yaml_doc)
            # params setting  =========================================
            self.url_target = self.yaml_doc["url"]                               # url
            self.url_path = self.yaml_doc["params"]["path"]                      # url path
            self.params['serviceKey'] = self.yaml_doc["params"]["serviceKey"]    # serviceKey
            self.params['pageNo'] = self.yaml_doc["params"]["pageNo"]            # pageNo
            self.params['numOfRows'] = self.yaml_doc["params"]["numOfRows"]      # numOfRows
            self.params['ffDt'] = self.yaml_doc["params"]["ffDt"]                # ffDt
            self.params['_type'] = self.yaml_doc["params"]["_type"]              # _type
            # =========================================================

    # instance method - 2
    def urlRequests(self):
        e_params = urlencode(self.params)
        url = self.url_target + self.url_path + "?" + e_params
        # print (url)
        html = requests.get(url)
        if html.status_code == 200:
            self.resp_data = html.json()
            self.resp_data = self.resp_data["response"]['body']['items']['item']

    # instance method - 3
    def reponseDataParcing(self):
        for d in self.resp_data:
            tmp_dict = {"ffclsnm":None,  # 산불위험구분코드명
                        "ffdt":None,     # 산불위험예보일자
                        "ffid":None,     # 산불위험행정기관코드
                        "ffquot":None}   # 산불위험지수
            tmp_dict["ffclsnm"] = d["ffclsnm"]
            tmp_dict["ffdt"] = d["ffdt"]
            tmp_dict["ffid"] = d["ffid"]
            tmp_dict["ffquot"] = d["ffquot"]
            self.json_data.append(tmp_dict)

        pprint.pprint(self.json_data)

        # json 파일에 데이터 적재
        with open("./OUTPUT/MM_JSON/mm_fire.json", "a", encoding="utf-8") as make_json:
            json.dump(self.json_data, make_json, ensure_ascii=False, indent="\t")
            make_json.close()

def main():
    proj_node = PROJ() # 객체 생성
    proj_node.paramsSett()
    proj_node.urlRequests()
    proj_node.reponseDataParcing()
if __name__ == "__main__":
    main()