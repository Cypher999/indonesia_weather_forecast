import json
import retrieve_data
import datetime

l=open("last_update.txt","r")
isi=l.read()
l.close()
isi=isi.split(",")

#mengecek tanggal update terakhir
last_update=datetime.date(int(isi[0]),int(isi[1]),int(isi[2]))

#mengecek tanggal sekarang
date_now=datetime.datetime.now()
date_n=datetime.date(int(date_now.strftime("%Y")),int(date_now.strftime("%m")),int(date_now.strftime("%d")))

#untuk mengecek selisih tanggal sekarang dengan tanggal terakhir update
update_int=date_n-last_update
update_int=update_int.days
print("="*31)
print("| Indonesian Weather Forecast | ")
print("| Code by r@t dev aka sandi   | ")
print("="*31)
print("Last update ={}".format(last_update))
if(update_int>5):
    print("The data is outdated, considere update the data before run this application")
class prakiraan_cuaca:
    def __init__(self):
        f=open("a.json","r")
        self.isi=json.loads(f.read())
        self.provinsi=0
        self.kota=0
        self.tanggal=0
    def lihat_daftar_provinsi(self):
        for isi in self.isi:
            print("[{}] . {}".format(self.isi.index(isi)+1,isi["provinsi"]))
        self.provinsi=int(input("Set Province (its number) ...."))
        self.provinsi=self.provinsi-1
    def lihat_daftar_kabupaten(self):
        daftar_kab=self.isi[self.provinsi]["data_kota"]
        for dk in daftar_kab:
            print("[{}] . {}".format(daftar_kab.index(dk)+1, dk["kota"]))
        self.kota = int(input("Set City / district (its number) ...."))
        self.kota = self.kota - 1
    def lihat_tanggal(self):
        daftar_tgl=self.isi[self.provinsi]["data_kota"][self.kota]["prakiraan_cuaca_kota"]
        for dt in daftar_tgl:
            print("[{}] . {}".format(daftar_tgl.index(dt)+1, dt["tanggal"]))
        self.tanggal = int(input("Set Date (its number) ...."))
        self.tanggal = self.tanggal - 1
    def lihat_cuaca(self):
        daftar_cuaca = self.isi[self.provinsi]["data_kota"][self.kota]["prakiraan_cuaca_kota"][self.tanggal]["prakiraan_cuaca"]
        for dc in daftar_cuaca:
            print("[{}]\n Hour : {} \nCondition :{} \nTemperature :{} \nHumidity :{} \nWind speed & direction ".format(daftar_cuaca.index(dc)+1, dc["jam"], dc["kondisi"],dc["suhu"], dc["kelembaban"], dc["arah_mata_angin"]))
        input()
    def lihat_opsi(self):
        prov=self.isi[self.provinsi]["provinsi"]
        kab = self.isi[self.provinsi]["data_kota"][self.kota]["kota"]
        tgl = self.isi[self.provinsi]["data_kota"][self.kota]["prakiraan_cuaca_kota"][self.tanggal]["tanggal"]
        print("current options")
        print("Province        = {}".format(prov))
        print("District / city = {}".format(kab))
        print("Date            = {}".format(tgl))
        input()

pc=prakiraan_cuaca()

def tampil_menu():
    print("Menu :")
    print("[1] Update data ")
    print("[2] Set Provinsi")
    print("[3] Set Kota / Kabupaten")
    print("[4] Set Tanggal ")
    print("[5] Open Weather Forecast")
    print("[6] Look Options")
    print("[X] Exit")

pil="0"
while(pil!="X"):
    tampil_menu()
    pil=input("Pilihan ...")
    if(pil=="2"):
        pc.lihat_daftar_provinsi()
    elif (pil=="1"):
        try:
            retrieve_data.data_retrieval()
        except:
            print("Connection error...")
    elif(pil=="3"):
        pc.lihat_daftar_kabupaten()
    elif(pil=="4"):
        pc.lihat_tanggal()
    elif(pil=="5"):
        pc.lihat_cuaca()
    elif(pil=="6"):
        pc.lihat_opsi()
    elif(pil=="x"):
        break
    elif(pil=="X"):
        break
    else:
        print("Wrong command...")
        input()