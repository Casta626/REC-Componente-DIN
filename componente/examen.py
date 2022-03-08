import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider
from animated_toggle import AnimatedToggle

from powerbar import PowerBar


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout2 = QVBoxLayout()
        layout3 = QVBoxLayout()
        # Creamos una instancia del nuevo componente PowerBar con 10 steps (grados)
        # powerbar = PowerBar(10)
        # Creamos una instancia del nuevo componente PowerBar con colores personalizados (lista)
        self.bol = False
        powerbar = PowerBar(["#5e4fa2" , "#3288bd", "#66c2a5", "#fee08b", "#fdae61"], self.bol)
        layout.addWidget(powerbar)
        

        mainToggle = AnimatedToggle()

        self.secondaryToggle = AnimatedToggle(
        checked_color="#FFB000",
        pulse_checked_color="#44FFB000"
        )
        mainToggle.setFixedSize(mainToggle.sizeHint())
        self.secondaryToggle.setFixedSize(mainToggle.sizeHint())

        slider = QSlider()

        # layout2.addWidget(slider)

        layout.addWidget(self.secondaryToggle)

        layout2.addWidget(self.secondaryToggle)
        layout3.addLayout(layout)
        layout3.addLayout(layout2)

        # layout.addLayout(layout2)
        container = QWidget()
        container.setLayout(layout3)
        self.setCentralWidget(container)

        self.secondaryToggle.clicked.connect(self.syncChange)

    def syncChange(self):
        if (self.secondaryToggle.isChecked()):
            print(self.secondaryToggle.isChecked())
            self.bol = True
            # self.BarSliderSync.setValue(0)
        else:
           print(self.secondaryToggle.isChecked())
           self.bol = False

        



        


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()