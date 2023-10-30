import requests
import pandas as pd
import matplotlib
from requests.auth import HTTPBasicAuth
from urllib3.exceptions import InsecureRequestWarning
import tkinter as tk
import json
from json import loads

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


err01 = "Credenciais inválidas, por favor verifique novamente."
err02 = "Não foi possível obter o Token de Sessão Archer"

def userInput(x,y,z):
    if not (x and y and z):
        raise ValueError("[ERRO] As credenciais não podem estar em branco.")
    data = {
        'InstanceName': z, 
        'UserName': x, 
        'UserDomain': '', 
        'Password': y
    }
    return data
    
# Read the JSON file
with open(r"C:\Users\user\AppData\Local\Programs\Python\Python312\credentials.json") as json_file:
    data = json.load(json_file)

username = str(data["UserName"])
password = str(data["Password"])
instance = str(data["InstanceName"])

# ------------------------ ### ---------------------------

data = userInput(username,password,instance)

url = "https://192.168.0.54/rsaarcher/api/core/security/login"

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

try:
    r = requests.post(url, data=json.dumps(data), headers=headers, verify = False)
    r.raise_for_status()
except requests.exceptions.RequestException as errex:
    print("An error ocurred")

r_dict = r.json()

# print(json.dumps(r_dict, indent=4, sort_keys=True))
# session_token = r_dict.get('IsSuccessful')

def printToken():
    requested_object = r_dict.get("RequestedObject")
    if requested_object:
        session_token = requested_object.get("SessionToken")
        # if(session_token != ''):
        #     print("------------------- TOKEN OBTIDO -------------------"+"\n" + session_token +"\n"+"----------------------------------------------------")
    return session_token

# printToken()

token = printToken()

contentURL = "http://192.168.0.54/rsaarcher/contentapi/RestAPI_1/RestAPI"

basic = HTTPBasicAuth('session-id', token)
response3 = requests.get(contentURL, auth=basic)

jsonData = response3.json()

df = pd.json_normalize(jsonData, record_path =['value'])

print(df)

# df = pd.DataFrame(jsonData,columns=['RestAPI_Id','ID_de_rastreamento', 'Nome', 'Primeira_publica\u00e7\u00e3o', '\u00daltima_atualiza\u00e7\u00e3o'])
