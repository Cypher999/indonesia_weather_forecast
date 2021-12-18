import requests as req
from bs4 import BeautifulSoup as bs
import json
from termcolor import colored
import os
import datetime

class data_retrieval:
    head={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0"}
    def __init__(self):
        h = self.data_cuaca_nasional("https://www.bmkg.go.id/cuaca/prakiraan-cuaca-indonesia.bmkg")
        h = json.dumps(h)
        f = open("a.json", "w")
        f.write(h)
        f.close()
        tgl_now = datetime.datetime.now()
        l = open("last_update.txt", "w")
        l.write(tgl_now.strftime("%Y") + "," + tgl_now.strftime("%m") + "," + tgl_now.strftime("%d"))
        l.close()
    def data_cuaca_kota(self,link):
        hasil_akses=req.get(link,headers=self.head,timeout=5).text
        data=[]
        parsing_hasil=bs(hasil_akses,"html.parser")
        lihat_tanggal=parsing_hasil.find_all("div",{"class":"prakicu-kabkota tab-v1 margin-bottom-30"})[0].find_all("ul",{"class":"nav"})[0].find_all("li")
        for lt in lihat_tanggal:
            data.append({"tanggal":lt.find_all("a")[0].get_text()})
        cuaca_per_hari =parsing_hasil.find_all("div",{"class":"tab-content no-padding"})[0].select('div[id*="TabPaneCuaca"]')
        if(len(cuaca_per_hari)!=len(data)):
            cuaca_per_hari.pop()
        for cph in cuaca_per_hari:
            hasil_hari=[]
            cuaca_per_jam=cph.find_all("div",{"class":"cuaca-flex-child"})
            for cpj in cuaca_per_jam:
                hasil_jam={}
                hasil_jam["jam"]=cpj.find_all("h2",{"class":"kota"})[0].get_text()
                hasil_jam["kondisi"] = cpj.find_all("div", {"class": "kiri"})[0].find_all("p")[0].get_text()
                hasil_jam["suhu"] = cpj.find_all("div", {"class": "kanan"})[0].find_all("h2",{"class":"heading-md"})[0].get_text()
                hasil_jam["kelembaban"] = cpj.find_all("div", {"class": "kanan"})[0].find_all("p")[0].get_text()
                hasil_jam["arah_mata_angin"] = cpj.find_all("div", {"class": "kanan"})[0].find_all("p")[1].get_text()
                hasil_hari.append(hasil_jam)
            data[cuaca_per_hari.index(cph)]["prakiraan_cuaca"]=hasil_hari
            notif = "{:,.2f} %".format(((cuaca_per_hari.index(cph) + 1) / len(cuaca_per_hari)) * 100)
            print(colored(notif, "green"))
        return data

    def data_cuaca_provinsi(self,link):
        hasil_akses=req.get(link,headers=self.head,timeout=5).text
        data=[]
        parsing_hasil=bs(hasil_akses,"html.parser")
        lihat_kota=parsing_hasil.find_all("table",{"class":"table table-hover table-striped table-prakicu-provinsi"})[0].find_all("a")
        i=0
        while(i<len(lihat_kota)):
            try:
                os.system('cls')
                notif="Retrieving data at {} [in progress]".format(lihat_kota[i].get_text())
                print(colored(notif,"blue"))
                link_kota = "https://www.bmkg.go.id/cuaca/" + lihat_kota[i]["href"]
                dc = self.data_cuaca_kota(link_kota)
                data.append({"kota":lihat_kota[i].get_text(),"prakiraan_cuaca_kota":dc})
                notif = "retrieving complete [progress == {:,.2f} % complete]".format(((i+1)/len(lihat_kota))*100)
                print(colored(notif, "green"))
                i=i+1
            except:
                notif="Error... reconnecting"
                print(colored(notif,"red"))
        return data

    def data_cuaca_nasional(self,link):
        hasil_akses=req.get(link,headers=self.head,timeout=5).text
        data=[]
        parsing_hasil=bs(hasil_akses,"html.parser")
        lihat_provinsi=parsing_hasil.find_all("div",{"class":"row list-cuaca-provinsi md-margin-bottom-10"})[0].find_all("div",{"class":"col-sm-4 col-xs-6"})
        lihat_provinsi.pop()
        i=0
        while(i<len(lihat_provinsi)):
            try:
                notif = "Retrieving data on province {} [in progress]".format(lihat_provinsi[i].get_text())
                print(colored(notif, "yellow"))
                hasil_provinsi=lihat_provinsi[i].find_all("a")[0].get_text()
                link_prov="https://www.bmkg.go.id/cuaca/prakiraan-cuaca-indonesia.bmkg"+lihat_provinsi[i].find_all("a")[0]["href"]
                dp=self.data_cuaca_provinsi(link_prov)
                data.append({"provinsi":hasil_provinsi,"data_kota":dp})
                notif = "retrieving province data is complete [progress == {:,.2f} % complete]".format(((i + 1) / len(lihat_provinsi)) * 100)
                print(colored(notif, "yellow"))
                i = i + 1
            except:
                notif="Error... reconnecting"
                print(colored(notif,"red"))
        return data



