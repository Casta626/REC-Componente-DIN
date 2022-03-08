import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtGui import QColor

from powerbar import PowerBar


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        # Creamos una instancia del nuevo componente PowerBar con 10 steps (grados)
        # powerbar = PowerBar(10)
        # Creamos una instancia del nuevo componente PowerBar con colores personalizados (lista)
        powerbar = PowerBar(["#5e4fa2" , "#3288bd", "#66c2a5", "#fee08b", "#fdae61"])
        layout.addWidget(powerbar)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
