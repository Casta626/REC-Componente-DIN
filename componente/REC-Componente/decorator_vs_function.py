# PySide6 @decorator

from PySide6.QtCore import Property

class CustomObject(QObject):
    def __init__(self):
        super().__init__()
        self._value = 0        # valor por defecto

    @Property(int)
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

# PySide6 function

from PySide6.QtCore import Property

class CustomObject(QObject):
    def __init__(self):
        super().__init__()
        self._value = 0        # valor por defecto

    def getValue(self):
        return self._value

    def setValue(self, value):
        self._value = value

    value = Property(int, getValue, setValue)