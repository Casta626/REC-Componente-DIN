import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QPropertyAnimation, QPoint, QEasingCurve

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(600, 600)
        self.child = QWidget(self)
        self.child.setStyleSheet("background-color:red;border-radius:15px;")
        self.child.resize(100, 100)
        self.anim = QPropertyAnimation(self.child, b"pos")
        # Podemos establecer diferentes curvas
        self.anim.setEasingCurve(QEasingCurve.InOutCubic)
        self.anim.setEasingCurve(QEasingCurve.InCubic)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        self.anim.setEasingCurve(QEasingCurve.OutInCubic)
        self.anim.setEasingCurve(QEasingCurve.InBounce)
        self.anim.setEasingCurve(QEasingCurve.OutBounce)
        self.anim.setEndValue(QPoint(400, 400))
        self.anim.setDuration(1500)
        self.anim.start()

app = QApplication(sys.argv)
w = Window()
w.show()
app.exec()