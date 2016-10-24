# Funciones que uso para el sitio de cambio, sobre todo estas funciones saca informacion de los datos exif de las fotos
# y estos datos los usa la app para agregar los datos a la base de datos
import exifread
import json
import requests
from datetime import datetime

def exifobj2lista(objDatos):
    ''' Recibe un objeto tag GPS de exifdata y devuelve una tupla de
    datos'''

    regresar = []
    for a in objDatos.values:
        regresar.append(a.num/a.den)
    return tuple(regresar)

def grados2decimal(grados):
    ''' Recibe una tupla de datos gps y devuelve valores en decimal '''

    Grad = grados[0]
    Mins = grados[1]
    Secs = grados[2]

    GPSdecimal = Grad + (Mins/60) + (Secs/3600)
    return GPSdecimal

def findDatetime(imagen):
    ''' Encuentra la fecha en los datos Exif de la imagen y debuelve el objeto datetime '''
    tags = exifread.process_file(open(imagen, 'rb'))
    imageDateTime = tags['Image DateTime'].values
    datetimeObj = datetime.strptime(imageDateTime, '%Y:%m:%d %H:%M:%S')
    return datetimeObj

def findGPS(imagen):
    ''' Encuentra los datos GPS si existen de una imagen y devuelve
    las cordenadas en decimal '''
    datos = ['GPS GPSLatitude','GPS GPSLatitudeRef','GPS GPSLongitude', 'GPS GPSLongitudeRef']
    tags = exifread.process_file(open(imagen, 'rb'))
    if all(tag in tags for tag in datos):
        # Agarramos los datos para latitude
        latitudeRef = tags['GPS GPSLatitudeRef'].values
        latitude = tags['GPS GPSLatitude']
        latitude = exifobj2lista(latitude)
        latitude = grados2decimal(latitude)
        if latitudeRef == 'S':
            latitude = latitude * -1
        # Agarramos los datos para longitude
        longitudeRef = tags['GPS GPSLongitudeRef'].values
        longitude = tags['GPS GPSLongitude']
        longitude = exifobj2lista(longitude)
        longitude = grados2decimal(longitude)
        if longitudeRef == 'W':
            longitude = longitude * -1

        return (latitude, longitude)

    print('No se encontraron los datos exif para GPS')
    return (None)

def reverseGeo(latitud, longitud, api='GoogleApi.secret'):
    ''' Encuentra la direccion a partir de los datos GEO latitud y longitud
    se requiere de un api de google '''

    #Cargamos el api
    with open(api, 'r') as f:
        GAPI = json.loads(f.read())

    url = GAPI['url']
    payload = { 'latlng' : str(latitud)+','+str(longitud), api : GAPI['api'] }

    r = requests.get(url, params=payload )
    if r.ok:
        resultado = json.loads(r.text)
        direccion = resultado['results'][0]['formatted_address']
    else:
        return 'No se pudo obtener la direccion'

    return direccion
