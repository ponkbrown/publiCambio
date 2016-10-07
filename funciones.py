import exifread

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
