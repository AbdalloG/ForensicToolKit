from re import L
from secrets import choice
from PIL import Image, ImageOps
from PIL.ExifTags import TAGS, GPSTAGS
import os
import googlemaps
from csv import writer
import cv2
import base64

#Base64 Data
def B64E(img):
    path = 'D:/Perfil/Abdall/Escritorio/Tareas/Rashid/4to Semestre/Programacion Para Ciberseguridad/PIA/ImagesB64/'
    with open(img, "rb") as img_file:
        b64_string = base64.b64encode(img_file.read())
        N = img.rsplit('.', 1)[0]
        with open(path+'B64'+N+'.txt', 'a', newline='') as w:
            w.write(b64_string.decode('utf-8'))
            w.close

#Stripp Meta
def HMeta(img):
    path = 'D:/Perfil/Abdall/Escritorio/Tareas/Rashid/4to Semestre/Programacion Para Ciberseguridad/PIA/ImagesSM/'
    try:
        original = Image.open(img) 
    except IOError:
        print('Problemas al leer la imagen.' + str(img))
        return
    original = ImageOps.exif_transpose(original) #Verifica que existe EXIF
    stripped = Image.new(original.mode, original.size) #Creamos una nueva imagen ya sin EXIF
    stripped.putdata(list(original.getdata()))
    stripped.save(f"{path}""SM"+img)


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

def MapsApi(geo):
    key = googlemaps.Client(key='')
    Lat = geo['GPSInfo']['Lat']
    Lng = geo['GPSInfo']['Lng']
    geocode_result = key.reverse_geocode((Lat, Lng))[0]
    geo['Direccion'] = {geocode_result['formatted_address']}

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
    MapsApi(data)
    return data

def printMetaData(ruta):
    path = 'D:/Perfil/Abdall/Escritorio/Tareas/Rashid/4to Semestre/Programacion Para Ciberseguridad/PIA/Reportes/'
    os.chdir(ruta)
    for root, dirs, files in os.walk(".", topdown=False):   
        for name in files:
            try:
                N = name.rsplit('.', 1)[0]+'.csv'
                with open(path+N, 'a', newline='') as w:
                    object = writer(w)
                    object.writerow(["Tags", "Values"])
                    try:
                        exifData = {}
                        exif = Meta(name)
                        for metadata in exif:
                            object.writerow([metadata, exif[metadata]])
                            w.close
                    except:
                        import sys, traceback
                        traceback.print_exc(file=sys.stdout)
            except:
                continue

#
def Hide(file1, file2):
    img1 = cv2.imread(file1) 
    img2 = cv2.imread(file2)
    scale_percent = 50
    width = int(img2.shape[1] * scale_percent / 100)
    height = int(img2.shape[0] * scale_percent / 100)
    dsize = (width, height)
    output = cv2.resize(img2, dsize)
    cv2.imwrite("D:/Perfil/Abdall/Escritorio/Tareas/Rashid/4to Semestre/Programacion Para Ciberseguridad/PIA/Steganography/rezice.jpg", output)
    img3 = cv2.imread("D:/Perfil/Abdall/Escritorio/Tareas/Rashid/4to Semestre/Programacion Para Ciberseguridad/PIA/Steganography/rezice.jpg")
    for i in range(img3.shape[0]): 
        for j in range(img3.shape[1]): 
            for l in range(3): 
                v1 = format(img1[i][j][l], '08b') 
                v2 = format(img3[i][j][l], '08b')
                v3 = v1[:4] + v2[:4]  
                img1[i][j][l]= int(v3, 2) 
    cv2.imwrite('imagehide.jpg', img1) 
