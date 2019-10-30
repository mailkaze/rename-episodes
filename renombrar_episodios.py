import re
import os

#nombre_archivo = 'Hora de Aventuras - Temporada 10 [HDTV 720p][Cap.1001][AC3 5.1 Castellano][www.descargas2020.org][www.pctnew.org].mpeg'

def renombrar(nombre_archivo):
    patron_nombre = r'(?P<nombre>^\w+[-\s\w]*)(?P<separador>\s-\s)'
    patron_temporada = r'-\sTemporada\s(?P<temporada>\d+)'
    patron_capitulo = r'\[Cap\.(?P<capitulo>\d{2,6})'
    patron_extension = r'(?P<extension>\.(\w)+$)'

    nombre = re.search(patron_nombre, nombre_archivo)
    temporada = re.search(patron_temporada, nombre_archivo)
    capitulo = re.search(patron_capitulo, nombre_archivo)
    extension = re.search(patron_extension, nombre_archivo)

    if not nombre or not temporada or not capitulo or not extension:
        #no generar un nuevo nombre si no es el patron a cambiar.
        return None

    capitulo = capitulo.group('capitulo')
    if len(capitulo) == 3:
        #temporada entre la 1 y la 9
        capitulo = capitulo[1:]
    elif len(capitulo) == 4:
        #temporada 10 en adelante
        capitulo = capitulo[2:]

    nuevo_nombre = '{} {}x{}{}'.format(nombre.group('nombre').strip(), temporada.group('temporada'), capitulo, extension.group())
    return nuevo_nombre

#pedir ruta de la carpeta contenedora
ruta = input('Pega aquí la ruta de la carpeta contenedora: ').strip()
#mover el directorio actual ahí, controlar errores
try:
    os.chdir(ruta)
except:
    print('No se encontró esa carpeta.')
#crear una lista con los archivos contenidos
archivos = os.listdir()
archivos_renombrados = archivos.copy()
#copia la lista de archivos, si solo se iguala, ambas comparten el mismo espacio en memoria.

if len(archivos) > 0:
    #llamar la funcion renombrar desde un for que recorre la lista, actualiza la copia con los nombres arreglados.
    for i in range(len(archivos)):
        renombrado = renombrar(archivos[i])
        if renombrado:
            archivos_renombrados[i] = renombrado

    try:
        renombrados = 0
        for i in range(len(archivos)):
            if archivos[i] != archivos_renombrados[i]:
                os.rename(archivos[i], archivos_renombrados[i])
                renombrados += 1
                print('El archivo {} se renombró a {}'.format(archivos[i], archivos_renombrados[i]))
        print('Trabajo completado, se renombraron un total de {} archivos.'.format(renombrados))
    except:
        print('ocurrió un error al intentar renombrar los archivos')

else:
    #si la lista está vacía, avisar de que la carpeta está vacía y no hacer nada.
    print('La carpeta está vacía')

