from tkinter import *
from tkinter import ttk 
from tkinter import filedialog
import os
import re

class App:
    def __init__(self, ventana):
        #constructor de la ventana
        self.ventana = ventana
        self.ventana.title('Renombrar episodios')

        marco = LabelFrame(self.ventana)
        marco.grid(row=0, column=0, columnspan=3, pady=5)

        Label(marco, text='Ruta de la carpeta contenedora:                                                              ').grid(
            row=0, column=0)
        self.ruta = Entry(marco)
        self.ruta.insert(END, 'C:\\Users\\Kaze\\Downloads')
        self.ruta.focus()
        self.ruta.grid(row=1,column=0, sticky=W + E)
        ttk.Button(marco, text='Buscar', command=self.buscar_carpeta).grid(
            row=1, column=1)
        ttk.Button(marco, text='Renombrar', command=self.ejecutar).grid(
            row=2, column=0, columnspan=2, sticky=W + E)
        self.lista = Listbox(marco)
        self.lista.grid(row=4, column=0, columnspan=2, sticky=W + E)

    def buscar_carpeta(self):
        ruta_carpeta = filedialog.askdirectory()
        self.ruta.delete(0, END)
        self.ruta.insert(END, ruta_carpeta)

    def renombrar(self, nombre_archivo):
        #patrones en regular expressions
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

        nuevo_nombre = '{} {}x{}{}'.format(nombre.group('nombre').strip(), 
                temporada.group('temporada'), capitulo, extension.group())
        return nuevo_nombre

    def ejecutar(self):
        ruta = self.ruta.get()
        if ruta == '':
            self.lista.insert(END, 'Pega en el cuadro la ruta de la carpeta que contiene los episodios.')
            return
        try:
            os.chdir(ruta)
        except:
            self.lista.insert(END, 'No se encontró esa carpeta.')
            return
        #crear una lista con los archivos contenidos
        archivos = os.listdir()
        archivos_renombrados = archivos.copy()
        #copia la lista de archivos, si solo se iguala, ambas comparten el mismo espacio en memoria.

        if len(archivos) > 0:
            #llamar la funcion renombrar desde un for que recorre la lista, actualiza la copia con los nombres arreglados.
            for i in range(len(archivos)):
                renombrado = self.renombrar(archivos[i])
                if renombrado:
                    archivos_renombrados[i] = renombrado

            try:
                renombrados = 0
                for i in range(len(archivos)):
                    if archivos[i] != archivos_renombrados[i]:
                        os.rename(archivos[i], archivos_renombrados[i])
                        renombrados += 1
                        #muestra el cambio en la lista
                        self.lista.insert(END,  'El archivo:')
                        self.lista.insert(END, archivos[i])
                        self.lista.insert(END, 'se renombró a:')
                        self.lista.insert(END, archivos_renombrados[i])     
                self.lista.insert(END, 'Trabajo completado.')

                if renombrados == 0:
                    self.lista.insert(END, 'No se encontraron archivos para renombrar.')
                elif renombrados == 1:
                    self.lista.insert(END, 'Se renombraró {} archivo.'.format(renombrados))
                else:
                    self.lista.insert(END, 'Se renombraron {} archivos.'.format(renombrados))
            except:
                self.lista.insert(END, 'Ocurrió un error al intentar renombrar los archivos.')
        else:
            #si la lista está vacía, avisar de que la carpeta está vacía y no hacer nada.
            self.lista.insert(END, 'La carpeta está vacía.')
    
    
if __name__ == '__main__':
    ventana = Tk()
    #ventana.geometry('500x250')
    app = App(ventana)
    ventana.mainloop()

