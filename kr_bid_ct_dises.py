'''
@ junhyeon.kim
@ emil - sleep4725@naver.com
@ 예측진료정보조회
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
            "serviceKey":None, "pageNo":None, "numOfRows":None,  "itemCode":None,
            "dataGubun":None,  "searchCondition":None, "_returnType":None,
        }
        self.yaml_doc = None
        self.resp_data = None
        self.json_data = []
        self.f = None
        self.jsonFileCreate()  # function call
        self.localinfo = {
            "busan":"부산",     "chungbuk":"충북",  "chungnam":"충남",  "daegu":"대구",
            "daejeon" :"대전",  "gangwon":"강원" ,  "gwangju":"광주",   "gyeongbuk":"경북",
            "gyeonggi":"경기",  "gyeongnam":"경남", "incheon":"인천",   "jeju":"제주",
            "jeonbuk":"전북",   "jeonnam":"전남",   "sejong":"세종",    "seoul":"서울",
            "ulsan":"울산",
        }

    # instance method - 0
    # json 파일 생성
    def jsonFileCreate(self):
        try:
            self.f = open("./OUTPUT/DU_JSON/du.json", "x")
        except FileExistsError as e:
            print (e)
        else:
            self.f.close()

    # instance method - 1
    # yaml 파일 읽어 오기
    def paramsSett(self):
        try:
            with open("./CONF/DU/data_go_kr_dust", "r", encoding="utf-8") as f:
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
            self.params['itemCode'] = self.yaml_doc["params"]["itemCode"]              # type (json/xml)
            self.params['dataGubun'] = self.yaml_doc["params"]["dataGubun"]  # numOfRows
            self.params['searchCondition'] = self.yaml_doc["params"]["searchCondition"]
            self.params['_returnType'] = self.yaml_doc["params"]["_returnType"]
            # =========================================================

    # instance method - 2
    def urlRequests(self):
        e_params = urlencode(self.params)
        url = self.url_target + self.url_path + "?" + e_params
        # print (url)
        html = requests.get(url)
        if html.status_code == 200:
            self.resp_data = html.json()
            # pprint.pprint (self.resp_data)

    # instance method - 3
    def reponseDataParcing(self):
        data = self.resp_data["list"]
        '''
        dataTime
        부산 : busan,   충북 : chungbuk,  충남 : chungnam, 대구 : daegu,     대전 : daejeon, 강원 : gangwon,
        광주 : gwangju, 경북 : gyeongbuk, 경기 : gyeonggi, 경남 : gyeongnam, 인천 : incheon, 제주 : jeju,
        전북 : jeonbuk, 전남 : jeonnam,   세종 : sejong,   서울 : seoul,     울산 : ulsan
        '''
        for i in data:

            tmp_dict = dict(i)

            for remv in ['_returnType', 'dataGubun', 'dataTerm', 'numOfRows', 'totalCount', 'pageNo',
                         'resultCode', 'resultMsg', 'searchCondition','serviceKey', 'itemCode']:
                try:
                    tmp_dict.pop(remv)
                except KeyError as e:
                    print (e)

            tmp_k = [k for k in tmp_dict.keys()]
            for k in tmp_k:
                t = {"si-name": None, "pm": None, "date-time": None}
                if k != "dataTime":
                    t["si-name"] = self.localinfo[k]
                    t['pm'] = tmp_dict[k]
                    t['date-time'] = tmp_dict['dataTime']
                    self.json_data.append(t)
        # json 파일에 데이터 적재
        with open("./OUTPUT/DU_JSON/du.json", "a", encoding="utf-8") as make_json:
            json.dump(self.json_data, make_json, ensure_ascii=False, indent="\t")
            make_json.close()

def main():
    proj_node = PROJ() # 객체 생성
    proj_node.paramsSett()
    proj_node.urlRequests()
    proj_node.reponseDataParcing()
if __name__ == "__main__":
    main()