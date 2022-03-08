import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QPropertyAnimation, QPoint, QEasingCurve

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(600, 600)
        # Creamos un widget
        self.child = QWidget(self)
        # Le ponemos un estilo con un color para que se vea
        self.child.setStyleSheet("background-color:red;border-radius:15px;")
        # Le ponemos un tamaño de 100x100
        self.child.resize(100, 100)
        # Creamos una QPropertyAnimation(elemento, propiedad)
        self.anim = QPropertyAnimation(self.child, b"pos")
        # Establecemos una coordenada final
        self.anim.setEndValue(QPoint(400, 400))
        # Establecemos la duración de la animación
        self.anim.setDuration(1500)
        # Iniciamos la animación
        self.anim.start()

app = QApplication(sys.argv)
w = Window()
w.show()
app.exec()