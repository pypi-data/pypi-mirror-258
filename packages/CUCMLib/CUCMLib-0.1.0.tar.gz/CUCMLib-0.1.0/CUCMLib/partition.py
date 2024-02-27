from requests import Session
from zeep import Client
from zeep.transports import Transport
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from zeep.cache import SqliteCache
from zeep.plugins import HistoryPlugin
from zeep.exceptions import Fault
from zeep.helpers import serialize_object
from lxml import etree
from requests.auth import HTTPBasicAuth
import pandas as pd
import json

with open('information.json', 'r') as config_file:
    config = json.load(config_file)

disable_warnings (InsecureRequestWarning)

username = config["username"]
password = config["password"]
fqdn = config["fqdn"]
address = 'https://{}:8443/axl/'.format(fqdn)
wsdl = 'AXLAPI.wsdl'
binding = "{http://www.cisco.com/AXLAPIService/}AXLAPIBinding"

session = Session()
session.verify = False
session.auth = HTTPBasicAuth (username , password)
transport = Transport(cache=SqliteCache(), session=session , timeout=20)
history = HistoryPlugin()
client = Client(wsdl = wsdl , transport = transport , plugins =[ history ])
axl = client.create_service( binding , address )

def show_history() :
    for item in [history.last_sent , history.last_received ]:
        print (etree.tostring ( item ["envelope"] , encoding ="unicode", pretty_print = True ))

###################################################################################################################################

   
    
def updatePhoneExcel():
    df_devices = pd.read_excel("updatePhone.xlsx")

    veri = df_devices.to_dict()

    for item in veri.keys():
        arr = []
        for key in veri[item].keys():
            value = veri[item][key]
            if pd.isna(value):
                value = None
            arr.append(value)
        
        veri[item] = arr

    i=0
    while (len(veri["Name"])) > i:
        update_phone = axl.updatePhone(name = veri["Name"][i],
            callingSearchSpaceName = veri["CSS"][i],                           
                               lines = {
            "line" : [{
            "label" : "line1",
            "index" : "1",
            "dirn" : {
                "pattern" : veri["Directory Number"][i],
                "routePartitionName" : veri["Partition"][i]
            }} ,
        ]})
        i=i+1

def updatePhoneExcelHelp():
    print("""
        Bu  fonksiyon ile CUCM'da bulunan cihazlar update edilmektedir. Fakat bu cihazların bilgilerini updatePhone.xlsx olarak kayıt edilmesi gerekmektedir.
        
        Bu değişikliklerde cihaz adı alınarak değişiklik yapılmaktadır. Bu yüzden cihaz adı doğru girilmelidir.
        
        Ayrıca sadece CSS - Directory Number - Partition verilerinde değişiklik yapılmaktadır.
          
        Bu excel dosyası içerisinde Name - Description - CSS - Directory Number - Partition yazılması gerekmektedir.
          
        Name    CSS	    Directory Number    Partition
        D1      	    101	
        D2      CSS_B   102	
        D3      CSS_C   103                 PT_300
            
        Yukarıda örnek bir excel dosyası görülmektedir. Burada girilmek istenilmeyen bilgiler boş bırakılabilmektedir. (NOT: Name kısmı boşbırakılamaz)
            
        ÖNMELİ NOT : CUCM ÜZERİNE DAHA ÖNCE OLUŞTURULMAMIŞ PARTİTİON VEYA CSS'İ EXCEL DOSYASI ÜZERİNE YAZDIRARAK CUCM'A YÜKLENMEK İSTENİRSE HATA VERECEKTİR.
        
        """)