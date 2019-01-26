'''
@ junhyeon.kim
@ emil - sleep4725@naver.com
@ 한국 관광공사 - 지역코드
@ 2019-01-26
'''
# ==================================
import requests
from yaml import load, load_all, YAMLError
import sys
from urllib.parse import urlencode
import pprint
import re
import json
import time
# ==================================
class PROJ:
    # 생성자
    def __init__(self):
        self.url_target = None
        self.url_path   = None

        self.params = {
            "serviceKey":None, "pageNo":None, "numOfRows":None,  "MobileOS":None,
            "MobileApp":None,  "areaCode":None, "_type":None,
        }
        self.yaml_doc = None
        self.resp_data = None
        self.json_data = []
        self.f = None
        self.jsonFileCreate()  # function call
        self.localinfo = {

        }

    # instance method - 0
    # json 파일 생성
    def jsonFileCreate(self):
        try:
            self.f = open("./OUTPUT/TU_JSON/areacode.json", "x")
        except FileExistsError as e:
            print (e)
        else:
            self.f.close()

    # instance method - 1
    # yaml 파일 읽어 오기
    def paramsSett(self):
        try:
            with open("./CONF/TU/data_go_kr_tu_tourareacode.yml", "r", encoding="utf-8") as f:
                self.yaml_doc = load(f)
                f.close()
        except FileNotFoundError as e: # 해당 파일이 조재하지 않는 경우
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
            self.params['MobileOS'] = self.yaml_doc["params"]["MobileOS"]        # type (json/xml)
            self.params['MobileApp'] = self.yaml_doc["params"]["MobileApp"]      # numOfRows
            self.params['areaCode'] = self.yaml_doc["params"]["areaCode"]        # areaCode
            self.params['_type'] = self.yaml_doc["params"]["_type"]              # _type
            # =========================================================

    # instance method - 2
    def urlRequests(self):
        num = 1
        # pageNo
        while True:
            e_params = urlencode(self.params)
            url = self.url_target + self.url_path + "?" + e_params
            # print (url)
            html = requests.get(url)
            if html.status_code == 200:
                self.resp_data = html.json()
                response = self.resp_data['response']["body"]['items']
                if "item" in dict(response).keys():
                    pprint.pprint(response)
                    self.params['pageNo'] += 1
            else:
                if num:
                    self.params['areaCode'] += 1
                    num = 0
                    self.params['pageNo'] = 1
                else:
                    break

    # instance method - 3
    def reponseDataParcing(self):
        data = self.resp_data["list"]
        # json 파일에 데이터 적재
        with open("./OUTPUT/TU_JSON/areacode.json", "a", encoding="utf-8") as make_json:
            json.dump(self.json_data, make_json, ensure_ascii=False)
            make_json.close()

def main():
    proj_node = PROJ() # 객체 생성
    proj_node.paramsSett()
    proj_node.urlRequests()
    # proj_node.reponseDataParcing()
if __name__ == "__main__":
    main()