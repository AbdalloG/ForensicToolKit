import os
from Script import *
import subprocess as sp
import argparse

try:
    os.mkdir('ImagesSM')
    os.mkdir('Reportes')
    os.mkdir('ImagesB64')
    os.mkdir('Steganography')
except:
    pass

if __name__ == "__main__":
    description = '''Ejemplo de uso:
python Main.py -b64 "D:/Perfil/Abdall/Escritorio/Tareas/Rashid/4to Semestre/Programacion Para Ciberseguridad/PIA/Images/"

python Main.py -smd "D:/Perfil/Abdall/Escritorio/Tareas/Rashid/4to Semestre/Programacion Para Ciberseguridad/PIA/Images/"

python Main.py -md "D:/Perfil/Abdall/Escritorio/Tareas/Rashid/4to Semestre/Programacion Para Ciberseguridad/PIA/Images/"

python Main.py -hide * -file1 "D:/Perfil/Abdall/Escritorio/Tareas/Rashid/4to Semestre/Programacion Para Ciberseguridad/PIA/Images/IMG_20200817_180440.jpg" -file2 "D:/Perfil/Abdall/Escritorio/Tareas/Rashid/4to Semestre/Programacion Para Ciberseguridad/PIA/Images/IMG_20201230_150141.jpg"

python Main.py -list "D:/Perfil/Abdall/Escritorio/Tareas/Rashid/4to Semestre/Programacion Para Ciberseguridad/PIA/Images/"
    '''
    parser = argparse.ArgumentParser(description='Toolkit', epilog=description, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-b64", metavar='PATHIMAGES', dest='b64', help='To encript BASE64 an image in images folder')
    parser.add_argument("-smd", metavar='PATHIMAGES', dest='smd', help='To stripp metadata from images in images folder')
    parser.add_argument("-md", metavar='PATHIMAGES', dest='md', help='To get metadata from images in images folder')
    parser.add_argument("-hide", metavar='PATHIMAGES', dest='hide', help='To hide a image in otherone')
    parser.add_argument("-file1", metavar='PATHIMAGE1', dest='file1', help='Image 1 to hide')
    parser.add_argument("-file2", metavar='PATHIMAGE2', dest='file2', help='Image 2 to hide')
    parser.add_argument("-list", metavar='PATHIMAGES', dest='list', help='List of images in path')
    params = parser.parse_args()

    if params.smd:
        pathImages = params.smd
        os.chdir(pathImages)
        for file in os.listdir():
            HMeta(file)
    
    if params.b64:
        pathImages = params.b64
        os.chdir(pathImages)
        for file in os.listdir():
            B64E(file)
    
    if params.md:
        pathImages = params.md
        printMetaData(pathImages)
    
    if params.list:
        pathImages = params.list
        os.chdir(pathImages)
        for files in os.listdir():
            print(files)

    if params.hide:
        file1 = params.file1
        file2 = params.file2
        Hide(file1, file2)
