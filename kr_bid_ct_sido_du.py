'''
@ junhyeon.kim
@ emil - sleep4725@naver.com
@ 시도별 실시간 측정정보 조회
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
            "serviceKey":None, "pageNo":None, "numOfRows":None,  "sidoName":None,
            "ver":None, "_returnType":None,
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
            self.f = open("./OUTPUT/DU_JSON/sido_du.json", "x")
        except FileExistsError as e:
            # 파일이 존재하지 않는 경우
            print (e)
        else:
            self.f.close()

    # instance method - 1
    # yaml 파일 읽어 오기
    def paramsSett(self):
        try:
            with open("./CONF/DU/data_go_kr_sido_dust", "r", encoding="utf-8") as f:
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
            self.params['sidoName'] = self.yaml_doc["params"]["sidoName"]        # sidoname
            self.params['ver'] = self.yaml_doc["params"]["ver"]                  # version
            self.params['_returnType'] = self.yaml_doc["params"]["_returnType"]  # type (xml/json)
            # =========================================================

    # instance method - 2
    def urlRequests(self):
        e_params = urlencode(self.params)
        url = self.url_target + self.url_path + "?" + e_params
        # print (url)
        html = requests.get(url)
        if html.status_code == 200:
            self.resp_data = html.json()
            pprint.pprint (self.resp_data)

    # instance method - 3
    def reponseDataParcing(self):
        data = self.resp_data["list"]
        for d in data:
            tmp_info = {"stationName":None, "so2Value":None, "coValue":None, "o3Value":None, "no2Value":None,
                        "pm10Value":None, "pm10Value24":None, "pm25Value":None, "pm25Value24":None, "khai":None,
                        "khaiGrade":None, "so2Grade":None, "coGrade":None, "o3Grade":None, "no2Grade":None,
                        "pm10Grade":None, "pm25Grade":None, "pm10Grade1h":None, "pm25Grade1h":None}

            tmp_info["stationName"] = d["stationName"]   # 측정소 명
            tmp_info["so2Value"] = d["so2Value"]         # 아황산가스 농도
            tmp_info["coValue"] = d["coValue"]           # 일산화탄소 농도
            tmp_info["o3Value"] = d["o3Value"]           # 오존농도
            tmp_info["no2Value"] = d["no2Value"]         # 이산화질소 농도
            tmp_info["pm10Value"] = d["pm10Value"]       # 미세먼지 농도(pm10)
            tmp_info["pm10Value24"] = d["pm10Value24"]   # 미세먼지 농도 24시간 예측이동 농도
            tmp_info["o3Value"] = d["o3Value"]           # 오존농도
            tmp_info["no2Grade"] = d["no2Grade"]         # 이산화질수 지수
            tmp_info["pm10Grade"] = d["pm10Grade"]       # 미세먼지(PM10) 24시간 등급
            tmp_info["pm25Grade"] = d["pm25Grade"]       # 미세먼지(PM2.5) 24시간 등급
            tmp_info["pm10Grade1h"] = d["pm10Grade1h"]   # 미세먼지(PM10) 1시간 등급
            tmp_info["pm25Grade1h"] = d["pm25Grade1h"]   # 미세먼지(PM2.5) 1시간 등급
            self.json_data.append(tmp_info)
        # json 파일에 데이터 적재
        with open("./OUTPUT/DU_JSON/sido_du.json", "a", encoding="utf-8") as make_json:
            json.dump(self.json_data, make_json, ensure_ascii=False, indent="\t")
            make_json.close()

def main():
    proj_node = PROJ() # 객체 생성
    proj_node.paramsSett()
    proj_node.urlRequests()
    proj_node.reponseDataParcing()
if __name__ == "__main__":
    main()