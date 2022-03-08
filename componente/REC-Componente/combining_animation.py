import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QParallelAnimationGroup, QPropertyAnimation, QPoint, QSequentialAnimationGroup, QSize

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(600, 600)
        self.child = QWidget(self)
        self.child.setStyleSheet("background-color:red;border-radius:15px;")
        self.child.resize(100, 100)
        self.anim = QPropertyAnimation(self.child, b"pos")
        self.anim.setEndValue(QPoint(200, 200))
        self.anim.setDuration(1500)
        self.anim_2 = QPropertyAnimation(self.child, b"size")
        self.anim_2.setEndValue(QSize(250, 150))
        self.anim_2.setDuration(2000)
        # Grupo de animación secuencial
        self.anim_group = QSequentialAnimationGroup()
        # Grupo de animación paralela
        # self.anim_group = QParallelAnimationGroup()
        self.anim_group.addAnimation(self.anim)
        self.anim_group.addAnimation(self.anim_2)
        self.anim_group.start()

app = QApplication(sys.argv)
w = Window()
w.show()
app.exec()