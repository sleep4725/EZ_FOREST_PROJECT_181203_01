'''
@ junhyeon.kim
@ emil - sleep4725@naver.com
@ 공원 정보
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
            "serviceKey":None, "pageNo":None, "numOfRows":None, "_type":None
        }
        self.yaml_doc = None
        self.resp_data = None
        self.json_data = []
        self.filter_string = ["<BR>", "<BR>&gt;", "&gt;", "<p>", "</p>"]
        self.f = None
        self.jsonFileCreate()  # function call

    # instance method - 0
    def jsonFileCreate(self):
        try:
            self.f = open("./OUTPUT/FO_JSON/forest.json", "x")
        except FileExistsError as e:
            print (e)
        else:
            self.f.close()

    # instance method - 1
    def paramsSett(self):
        try:
            with open("./CONF/FO/data_go_kr_forest.yaml", "r") as f:
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
            self.params['_type'] = self.yaml_doc["params"]["_type"]              # type (json/xml)
            # =========================================================

    # instance method - 2
    def urlRequests(self):
        e_params = urlencode(self.params)
        url = self.url_target + self.url_path + "?" + e_params
        html = requests.get(url)
        if html.status_code == 200:
            self.resp_data = html.json()

    # instance method - 3
    def reponseDataParcing(self):
        data = self.resp_data["response"]['body']['items']['item']

        for d in data:
            tmp_data = {'areanm':str(d['areanm']),
                        'mntnm': str(d['mntnm']),
                        'transport':str(d['transport']),}

            for k, v in tmp_data.items():
                for f in self.filter_string:
                    if f in v:
                        v = v.replace(f, "")

            tmp_data[k] = v
            self.json_data.append(tmp_data)

        # json 파일에 데이터 적재
        with open("./OUTPUT/FO_JSON/forest.json", "a", encoding="utf-8") as make_json:
            json.dump(self.json_data, make_json, ensure_ascii=False, indent="\t")
            make_json.close()

def main():
    proj_node = PROJ() # 객체 생성
    proj_node.paramsSett()
    proj_node.urlRequests()
    proj_node.reponseDataParcing()
if __name__ == "__main__":
    main()