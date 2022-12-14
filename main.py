from distutils.log import error
import sys
import os
from tkinter import dialog
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from gui import Ui_ventana

# cambiar volumen con FFMPEG = ffmpeg -i 01.mp3 -filter:a "volume=4dB" 001.mp3


class window(Ui_ventana):
    def __init__(self, dialog):
        super().__init__()
        self.setupUi(dialog)

        # CONECTAMOS LOS CONTROLES
        self.pushButton.clicked.connect(self.buscarArchivos)

        self.pushButton_2.clicked.connect(self.cancelar)

        self.lbl_contador.setText('Sin archivos a normalizar.')

        self.label_2.setText('Aumento de volumen')
        # Establece el aumento por defecto
        self.spinBox.setValue(2)

        # Accion de ACEPTAR
        self.pushButton_3.clicked.connect(self.convertir)

    def convertir(self):
        cont = self.listWidget.count()
        if cont == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText(
                "Debe seleccionar la carpeta que contanta los archivos mp3.")
            msg.setWindowTitle("Aviso")
            retval = msg.exec()

        else:
            try:
                for i in range(0, cont):
                    # Indica el indice y obtiene el item de la lista
                    item = self.listWidget.item(i).text()
                    vol = self.spinBox.text()
                    listado = item.split('/')
                    itemMp3 = listado[len(listado)-1]
                    os.system(
                        f'ffmpeg -i "{item}" -filter:a "volume={vol}dB" "{item.replace(itemMp3,"nomr_"+str(itemMp3))}"')

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Todos los archivos normalizados con exito.")
                msg.setWindowTitle("Información")
                retval = msg.exec()
            except error:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Error)
                msg.setText("Ha ocurrido un error al intentar normalizar el audio.")
                msg.setWindowTitle("ERROR")
                retval = msg.exec()

    def cancelar(self):
        self.listWidget.clear()
        self.lbl_contador.setText('Sin archivos a normalizar.')
        self.lineEdit.setText('')

    def buscarArchivos(self):
        # Obtiene la carpeta donde buscar los mp3
        file = QFileDialog.getExistingDirectory()
        # Lista los archivos en el directorio
        for i in os.listdir(file):
            if i.endswith('.mp3'):
                self.listWidget.addItem(file + "/" + i)
                # Agrega el directorio que contiene los mp3
                self.lineEdit.setText(file)
                # Indica cuantos archivos se encontraron
                contador = self.listWidget.count()
                self.lbl_contador.setText(
                    'Cantidad de archivos agregados: ' + str(contador))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    prog = window(dialog)
    dialog.show()
    sys.exit(app.exec_())
