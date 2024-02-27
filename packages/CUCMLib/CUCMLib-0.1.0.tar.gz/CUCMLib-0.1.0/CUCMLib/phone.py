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

def phoneHelp():
    print("""
          
          Bu kütüphane ile telefon ile ilgili geliştirmeler yapılabilmektedir.
          
          listPhone() -> Bu fonksiyon ile Call Manager'a kayıtlı telefonları listelemektedir. Deaylı bilgi için listPhoneHelp() komutunu çağırınız.
          
          addPhone -> Bu fonksiyon ile Call Manager'a yeni telefon eklemek için kullanılmaktadır. Deaylı bilgi için addPhoneHelp() komutunu çağırınız.
          
          deletePhone -> Bu fonksiyon ile Call Manager'da bulunan telefonu silmek için kullanılmaktadır. Deaylı bilgi için deletePhoneHelp() komutunu çağırınız.
          
          
          """  
    )

def listPhone():
    
    list_phone= axl.listPhone(searchCriteria={"name":"%"}, returnedTags={"name":"","description":"","callingSearchSpaceName":""})

    veri = {
    "Name": [],
    "Description": [],
    "CSS":[],
    "Directory Number":[],
    "Partition":[]
    }
    
    for phone in list_phone["return"]["phone"]:
        get_phone = axl.getPhone(name = phone["name"])
    
        names = get_phone["return"]["phone"]["name"]
        description = get_phone["return"]["phone"]["description"]
        css = get_phone["return"]["phone"]["callingSearchSpaceName"]["_value_1"]
        pattern = get_phone["return"]["phone"]["lines"]["line"][0]["dirn"]["pattern"]
        partition = get_phone["return"]["phone"]["lines"]["line"][0]["dirn"]["routePartitionName"]["_value_1"]
    
        veri["Name"].append(names)
        veri["Description"].append(description)
        veri["CSS"].append(css)
        veri["Directory Number"].append(pattern)
        veri["Partition"].append(partition)
    

    print(veri)

def listPhoneHelp():
    print("""
          Bu fonksiyon çağırıldığında Call Manager üzeride bulunan telefonları listemektedir. Fakat telefon üzerinde bulunan bütün özellikleri listelememektedir.
        
          Liste sırasında verilecek olan bilgiler:
          
          Name  -  Description  -  CSS  -  Directory Number  -  Partition
          
          Bu bilgiler haricinde bulunan bilgiler listelenmemektedir.
          
       
          """
    )

def listPhoneCsv():
    list_phone= axl.listPhone(searchCriteria={"name":"%"}, returnedTags={"name":"","description":"","callingSearchSpaceName":""})

    veri = {
        "Name": [],
        "Description": [],
        "CSS":[],
        "Directory Number":[],
        "Partition":[]
    }

    for phone in list_phone["return"]["phone"]:
        get_phone = axl.getPhone(name = phone["name"])
    
        names = get_phone["return"]["phone"]["name"]
        description = get_phone["return"]["phone"]["description"]
        css = get_phone["return"]["phone"]["callingSearchSpaceName"]["_value_1"]
        pattern = get_phone["return"]["phone"]["lines"]["line"][0]["dirn"]["pattern"]
        partition = get_phone["return"]["phone"]["lines"]["line"][0]["dirn"]["routePartitionName"]["_value_1"]
    
        veri["Name"].append(names)
        veri["Description"].append(description)
        veri["CSS"].append(css)
        veri["Directory Number"].append(pattern)
        veri["Partition"].append(partition)
    

    veri_listesi = pd.DataFrame(veri)

    veri_listesi.to_csv('veri_listesi.csv', index=False)

def listPhoneCsvHelp():
    print("""
    Bu kütüphane ile CUCM'da bulunan cihazların bilgilerini, bulunduğu klasöre CSV formatında kaydetmektedir.
    
    Kaydedilen bilgiler : Name  -  Description  -  CSS  -  Directory Number  -  Partition
          
    Bu bilgiler haricinde bulunan bilgiler yazılmamaktadır.
    
    """)
    
def addPhoneExcel():
    df_devices = pd.read_excel("phoneList.xlsx")

    veri = df_devices.to_dict()

    for item in veri.keys():
        arr = []
        for key in veri[item].keys():
            value = veri[item][key]
            if pd.isna(value):
                value = None
            arr.append(value)
        
        veri[item] = arr


    i = 0
    while (len(veri["Name"])) > i:
        add_phone = axl.addPhone(
            phone={
                "name": veri["Name"][i],
                "description": veri["Description"][i],
                "product": "Cisco Unified Client Services Framework",
                "class": "Phone",
                "protocol": "SIP",
                "protocolSide": "User",
                "callingSearchSpaceName": veri["CSS"][i],
                "devicePoolName": "Default",
                "commonPhoneConfigName": "Standard Common Phone Profile",
                "locationName": "Hub_None",
                "useTrustedRelayPoint": "Default",
                "phoneTemplateName": "Standard Client Services Framework",
                "userLocale": "English United States",
                "lines": {
                    "line": [
                        {
                            "label": "line1",
                            "index": 1,
                            "dirn": {
                                "pattern": veri["Directory Number"][i],
                                "routePartitionName": veri["Partition"][i],
                            },
                        },
                    ],
                },
            },
        )
        i = i + 1

def addPhoneExcelHelp():
    print("""
          
        Bu  fonksiyon ile CUCM'a yeni cihaz eklenmektedir. Fakat bu cihazların bilgilerini phoneList.xlsx olarak kayıt edilmesi gerekmektedir.
          
        Bu excel dosyası içerisinde Name - Description - CSS - Directory Number - Partition yazılması gerekmektedir.
          
        Name    Description     CSS	    Directory Number    Partition
        D1      Deneme1		            101	
        D2      Deneme2         CSS_B   102	
        D3      Deneme3         CSS_C   103                 PT_300
            
        Yukarıda örnek bir excel dosyası görülmektedir. Burada girilmek istenilmeyen bilgiler boş bırakılabilmektedir.
            
        ÖNMELİ NOT : CUCM ÜZERİNE DAHA ÖNCE OLUŞTURULMAMIŞ PARTİTİON VEYA CSS'İ EXCEL DOSYASI ÜZERİNE YAZDIRARAK CUCM'A YÜKLENMEK İSTENİRSE HATA VERECEKTİR.
            
        Bu değerler haricinde diğer değerler varsayılan olan gelmektedir. Varsayılan olarak gelen değeler:
            
                product : Cisco Unified Client Services Framework,
                class : Phone,
                protocol : SIP,
                protocolSide : User,
                devicePoolName": Default,
                commonPhoneConfigName : Standard Common Phone Profile,
                locationName : Hub_None,
                useTrustedRelayPoint : Default,
                phoneTemplateName : Standard Client Services Framework,
                userLocale : English United States,
        """)
    
    
 