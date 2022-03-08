from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider
from PySide6.QtCore import (
    Qt, QSize, QPoint, QPointF, QRectF,
    QEasingCurve, QPropertyAnimation, QSequentialAnimationGroup,
    Slot, Property)

from PySide6.QtWidgets import QCheckBox
from PySide6.QtGui import QColor, QBrush, QPaintEvent, QPen, QPainter

# Barra que hereda de QWidget
class _Bar(QtWidgets.QWidget):
    #clickedValue es una señal que emite un número entero
    clickedValue = QtCore.Signal(int)
    # El constructor debe recibir los "steps"
    def __init__(self, steps):
        super().__init__()
        # La política MininumExpanding permite usar todo el espacio disponible a partir del tamaño mínimo establecido en sizeHint()
        self.setSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding,
        )
        # La función isinstance recibe como argumentos un objeto y una clase y devuelve True si el objeto es una instancia de dicha clase o de una subclase de ella.
        
        # Si steps es una lista de colores
        if isinstance(steps, list):
            # El número de steps es la longitud de la lista
            self.n_steps = len(steps)
            # self.steps es la lista de colores
            self.steps = steps

        # Si steps es un entero
        elif isinstance(steps, int):
            # El número de steps es ese entero
            self.n_steps = steps
            # self.steps es una lista de colores rojos del tamaño de steps
            self.steps = ["red"] * steps
        # Si no es una lista o un entero, lanzamos un error
        else:
            # raise fuerza una excepción
            raise TypeError("steps must be a list or int")

        # Porcentaje de altura de las barras dentro del rectángulo individual de cada una
        self._bar_solid_percent = 0.8
        # El color de fondo de la Bar es negro
        self._background_color = QtGui.QColor("black")
        # Los píxeles de padding alrededor del borde son 4
        self._padding = 4

    # Ante un evento de dibujo
    def paintEvent(self, e):
        # Creamos el objeto painter
        painter = QtGui.QPainter(self)

        # Creamos la brocha
        brush = QtGui.QBrush()
        # Establecemos el color de la brocha (el color de fondo, negro)
        brush.setColor(self._background_color)
        # Establecemos el estilo de patrón de relleno: sólido
        brush.setStyle(Qt.SolidPattern)
        # Dibujamos un rectángulo (fondo de la Bar)
        rect = QtCore.QRect(0, 0, painter.device().width(), painter.device().height())
        # Rellenamos el rectángulo
        painter.fillRect(rect, brush)

        # Obtenemos estado actual del padre (PowerBar)
        parent = self.parent()
        # Obtenemos el mínimo, el máximo y el valor del padre
        # Al no existir esas propiedades en Bar, las obtiene del QDial (método (__getattr__)), que las hereda de QAbstractSlider
        vmin, vmax = parent.minimum(), parent.maximum()
        value = parent.value()

        # Definimos la altura y la anchura del canvas en el que vamos a dibujar las barras
        d_height = painter.device().height() - (self._padding * 2)
        d_width = painter.device().width() - (self._padding * 2)

        # Dibujamos las barras

        # Para la altura del rectángulo para cada barra, dividimos la altura del canvas entre el número de barras
        step_size = d_height / self.n_steps
        # Para determinar la altura del relleno de la barra, multiplicamos la altura del rectángulo para cada una por el porcentaje previamente definido
        bar_height = step_size * self._bar_solid_percent

        # Calculamos el número de barras a dibujar en función del valor actual
        pc = (value - vmin) / (vmax - vmin)
        n_steps_to_draw = int(pc * self.n_steps)

        # Por cada barra a dibujar
        for n in range(n_steps_to_draw):
            # Establecemos el color según la posición de la lista self.steps
            brush.setColor(QtGui.QColor(self.steps[n]))
            # Calculamos su posición en el canvas
            ypos = (1 + n) * step_size
            # Dibujamos el rectángulo de la barra
            rect = QtCore.QRect(
                self._padding,
                self._padding + d_height - int(ypos),
                d_width,
                int(bar_height),
            )
            # Y lo rellenamos
            painter.fillRect(rect, brush)

        painter.end()
    
    # El método sizeHint siempre devuelve el tamaño recomendado del widget (por defecto)
    def sizeHint(self):
        return QtCore.QSize(40, 120)

    # Cada vez que se cambia el valor del QDial, se llama a este método que ejecuta un update()
    # https://doc.qt.io/qt-5/qwidget.html#update
    # update() programa un paintEvent, que provocará el redibujado de la Bar
    def _trigger_refresh(self):
        self.update()

    # Cálculo del valor de la barra en función de donde se haga clic
    def _calculate_clicked_value(self, e):
        parent = self.parent()
        vmin, vmax = parent.minimum(), parent.maximum()
        d_height = self.size().height() + (self._padding * 2)
        step_size = d_height / self.n_steps
        click_y = e.y() - self._padding - step_size / 2

        pc = (d_height - click_y) / d_height
        value = int(vmin + pc * (vmax - vmin))
        # Emitimos una señal con el vambio de valor. Esta es una señal propia de este componente
        self.clickedValue.emit(value)

    # Un evento de movimiento de arrastre del ratón provoca el cálculo del clic
    def mouseMoveEvent(self, e):
        self._calculate_clicked_value(e)

    # Un evento de presionado en el ratón provoca el cálculo del clic
    def mousePressEvent(self, e):
        self._calculate_clicked_value(e)

# Custom widget que combina una Bar y un QDial
class PowerBar(QtWidgets.QWidget):

    def __init__(self, steps=5, bol=True, color="#4400B0EE",color2="#4400B0EE", parent=None):
        super().__init__(parent)
        self.bol = False
        self.color = "#4400B0EE"
        self.color2 = "#7400B0EE"
            
        self.secondaryToggle = AnimatedToggle(
        checked_color=color,
        pulse_checked_color=color2
        )
        # Creamos un Layout vertical con un objeto Bar y un objeto QDial
        layout = QtWidgets.QHBoxLayout()
        layout2 = QtWidgets.QHBoxLayout()
        layout3 =  QtWidgets.QVBoxLayout()
        self._bar = _Bar(steps)
        layout.addWidget(self._bar)
        self.BarSliderSync = QSlider()
        self.nulo = 0
        # Establecemos algunas propiedades del QDial
        self.BarSliderSync.setMinimum(0)
        self.BarSliderSync.setMaximum(100)
        self.label = QLabel()
        self.label.setText("*Soy la Imagen 1*")
        self.label.setVisible(False)

        self.label2 = QLabel()
        self.label2.setText("*Soy la Imagen 2*")

            # self._dial.setNotchesVisible(True)
            # self._dial.setWrapping(False)
            # Conectamos la señal del cambio de valor en el QDial con _trigger_refresh de la Bar para actualizarla
        

            # De la misma forma, conectamos la señal del cambio de valor en la barra con el setValue del QDial para actualizarlo
        self._bar.clickedValue.connect(self.BarSliderSync.setValue)

        layout2.addWidget(self.secondaryToggle)

        layout.addWidget(self.BarSliderSync)
        layout3.addWidget(self.label)
        layout3.addWidget(self.label2)
        # layout.addLayout(layout2)
        layout3.addLayout(layout)
        layout3.addLayout(layout2)
        self.setLayout(layout3)

        self.secondaryToggle.clicked.connect(self.syncChange)

        
        # print("Activa el toggle")
    # Este método se ejecuta cuando se intenta obtener alguna propiedad de PowerBar
    @Property(str)
    def getColor1(self):
        return self.color

    @Property(str)
    def setColor1(self, color):
        self.color = color

    @Property(str)
    def getColor2(self):
        return self.color2

    @Property(str)
    def setColor2(self, color2):
        self.color2 = color2

    def syncChange(self):
        if (self.secondaryToggle.isChecked()==False):
            print(self.secondaryToggle.isChecked())

            self.bol = True
            self.BarSliderSync.setMinimum(0)
            self.BarSliderSync.setMaximum(1)
            self.BarSliderSync.setValue(0)
            self.label.setVisible(False)
            self.label2.setVisible(True)
            # self.BarSliderSync.setVisible(False)
            

        else:
            print(self.secondaryToggle.isChecked())
        #    while self.bol == True:
            self.BarSliderSync.setMinimum(0)
            self.BarSliderSync.setMaximum(100)
            self.BarSliderSync.setValue(0)
            self.label.setVisible(True)
            self.label2.setVisible(False)
            self.BarSliderSync.valueChanged.connect(self._bar._trigger_refresh)
            # self.BarSliderSync.setValue(0)


            self.bol = False
    def returnNull(self):
        return self.nulo

    def __getattr__(self, name):
        # Si se trata de una propiedad de PowerBar, la devuelve
        if name in self.__dict__:
            return self[name]
        # Si no, intenta obtener la propiedad del objeto QDial
        try:
            return getattr(self.BarSliderSync, name)
        except AttributeError:
            raise AttributeError(
                "'{}' object has no attribute '{}'".format(
                    self.__class__.__name__, name
                )
            )
    # Método que establece un color para toda la PowerBar
    def setColor(self, color):
        self._bar.steps = [color] * self._bar.n_steps
        self._bar.update()
    # Método que establece los colores de cada barra
    def setColors(self, colors):
        self._bar.n_steps = len(colors)
        self._bar.steps = colors
        self._bar.update()
    # Método que establece un padding diferente para las barras
    def setBarPadding(self, i):
        self._bar._padding = int(i)
        self._bar.update()
    # Método que cambia el porcentaje del relleno de la barra
    def setBarSolidPercent(self, f):
        self._bar._bar_solid_percent = float(f)
        self._bar.update()
    # Método que cambia el color de fondo de la barra
    def setBackgroundColor(self, color):
        self._bar._background_color = QtGui.QColor(color)
        self._bar.update()

class AnimatedToggle(QCheckBox):

    _transparent_pen = QPen(Qt.transparent)
    _light_grey_pen = QPen(Qt.lightGray)

    def __init__(self,
        parent=None,
        bar_color=Qt.gray,
        checked_color="#00B0FF",
        handle_color=Qt.white,
        pulse_unchecked_color="#44999999",
        pulse_checked_color="#4400B0EE"
        ):
        super().__init__(parent)

        self._bar_brush = QBrush(bar_color)
        self._bar_checked_brush = QBrush(QColor(checked_color).lighter())

        self._handle_brush = QBrush(handle_color)
        self._handle_checked_brush = QBrush(QColor(checked_color))

        self._pulse_unchecked_animation = QBrush(QColor(pulse_unchecked_color))
        self._pulse_checked_animation = QBrush(QColor(pulse_checked_color))

        self.setContentsMargins(8, 0, 8, 0)
        self._handle_position = 0

        self._pulse_radius = 0

        self.animation = QPropertyAnimation(self, b"handle_position", self)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)
        self.animation.setDuration(200)

        self.pulse_anim = QPropertyAnimation(self, b"pulse_radius", self)
        self.pulse_anim.setDuration(350)
        self.pulse_anim.setStartValue(10)
        self.pulse_anim.setEndValue(20)

        self.animations_group = QSequentialAnimationGroup()
        self.animations_group.addAnimation(self.animation)
        self.animations_group.addAnimation(self.pulse_anim)

        self.stateChanged.connect(self.setup_animation)

    def sizeHint(self):
        return QSize(58, 45)

    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    @Slot(int)
    def setup_animation(self, value):
        self.animations_group.stop()
        if value:
            self.animation.setEndValue(1)
        else:
            self.animation.setEndValue(0)
        self.animations_group.start()

    def paintEvent(self, e: QPaintEvent):

        contRect = self.contentsRect()
        handleRadius = round(0.24 * contRect.height())

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        p.setPen(self._transparent_pen)
        barRect = QRectF(
            0, 0,
            contRect.width() - handleRadius, 0.40 * contRect.height()
        )
        barRect.moveCenter(contRect.center())
        rounding = barRect.height() / 2

        trailLength = contRect.width() - 2 * handleRadius

        xPos = contRect.x() + handleRadius + trailLength * self._handle_position

        if self.pulse_anim.state() == QPropertyAnimation.Running:
            p.setBrush(
                self._pulse_checked_animation if
                self.isChecked() else self._pulse_unchecked_animation)
            p.drawEllipse(QPointF(xPos, barRect.center().y()),
                          self._pulse_radius, self._pulse_radius)

        if self.isChecked():
            p.setBrush(self._bar_checked_brush)
            p.drawRoundedRect(barRect, rounding, rounding)
            p.setBrush(self._handle_checked_brush)

        else:
            p.setBrush(self._bar_brush)
            p.drawRoundedRect(barRect, rounding, rounding)
            p.setPen(self._light_grey_pen)
            p.setBrush(self._handle_brush)

        p.drawEllipse(
            QPointF(xPos, barRect.center().y()),
            handleRadius, handleRadius)

        p.end()

    @Property(float)
    def handle_position(self):
        return self._handle_position

    @handle_position.setter
    def handle_position(self, pos):
        self._handle_position = pos
        self.update()

    @Property(float)
    def pulse_radius(self):
        return self._pulse_radius

    @pulse_radius.setter
    def pulse_radius(self, pos):
        self._pulse_radius = pos
        self.update()