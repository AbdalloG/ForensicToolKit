from re import L
from PIL import Image, ImageOps
from PIL.ExifTags import TAGS, GPSTAGS
from prettytable import PrettyTable
import os
import googlemaps
from datetime import datetime

#Hex Data
def HexView(img):
    f = open(img,'rb')
    fcontents = f.read()
    bytes = 0
    line = []
    for by in fcontents:
        bytes = bytes + 1
        line.append(by)
        print("{0:0{1}x}".format(by,2), end=" ")
        if bytes % 16 == 0:
            print("#", end="")
            for by2 in line:
                if (by2 >= 32) and (by2 <= 126):
                    print(chr(by2), end="")
                else:
                    print("*", end="")
            line=[]
            print("")

#Stripp Meta
def HMeta(img):
    try:
        original = Image.open(img) 
    except IOError:
        print('Problemas al leer la imagen.' + str(img))
        return
    original = ImageOps.exif_transpose(original) #Verifica que existe EXIF
    stripped = Image.new(original.mode, original.size) #Creamos una nueva imagen ya sin EXIF
    stripped.putdata(list(original.getdata()))
    stripped.save("SM"+img)


#Start EXIF
def decode_gps_info(exif):
    gpsinfo = {}
    if 'GPSInfo' in exif:
        Nsec = exif['GPSInfo'][2][2]
        Nmin = exif['GPSInfo'][2][1]
        Ndeg = exif['GPSInfo'][2][0]
        Wsec = exif['GPSInfo'][4][2] 
        Wmin = exif['GPSInfo'][4][1]
        Wdeg = exif['GPSInfo'][4][0] 
        if exif['GPSInfo'][1] == 'N':
            Nmult = 1
        else:
            Nmult = -1
        if exif['GPSInfo'][1] == 'E':
            Wmult = 1
        else:
            Wmult = -1
        Lat = Nmult * (Ndeg + (Nmin + Nsec/60.0)/60.0)
        Lng = Wmult * (Wdeg + (Wmin + Wsec/60.0)/60.0)
        exif['GPSInfo'] = {"Lat" : Lat, "Lng" : Lng}
    else:
            print ("Sin Metadata")

def Meta(img):
    data = {}
    try:
        imagen = Image.open(img) 
    except IOError:
        print('Problemas al leer la imagen.' + str(img))
        return
    if hasattr(imagen, '_getexif'):
        exif = imagen._getexif()
        if exif is not None:
            for tag,value in exif.items():
                tag_n = TAGS.get(tag, tag)
                data[tag_n] = value
    decode_gps_info(data)
    return data

def printMetaData(ruta):
    table = PrettyTable()
    table.field_names = ["Tags", "Values"]
    os.chdir(ruta)
    for root, dirs, files in os.walk(".", topdown=False):   
        for name in files:
            try:
                exifData = {}
                exif = Meta(name)
                for metadata in exif:
                    table.add_row([metadata, exif[metadata]])
            except:
                import sys, traceback
                traceback.print_exc(file=sys.stdout)
    N = name.rsplit('.', 1)[0]
    with open(N + '.txt', 'w') as w:
        w.write(str(table))
        w.close

#Using de information
def MapsApi():
    key = googlemaps.Client(key='AIzaSyBDfz-d-9pEGkVNxZKDKE6VfCC9p0yxtx4')
    geocode_result = key.reverse_geocode((25.7789497375, -100.33634185777778))[0]
    print(geocode_result['formatted_address'])

