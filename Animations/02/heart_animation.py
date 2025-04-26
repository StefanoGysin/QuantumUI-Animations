import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QPainterPath, QColor
from PySide6.QtCore import Qt
from math import cos, sin, pi

class HeartWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Coração")
        self.resize(400, 400)
        # Remove o fundo da janela
        self.setAttribute(Qt.WA_TranslucentBackground)
        # Remove a borda da janela
        self.setWindowFlags(Qt.FramelessWindowHint)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Centralizar o coração
        painter.translate(self.width() / 2, self.height() / 2)
        
        # Desenhar o coração
        path = QPainterPath()
        size = 100
        
        # Criar o caminho do coração
        for t in range(0, 360):
            t_rad = t * pi / 180
            x = size * 16 * sin(t_rad) ** 3 / 16
            y = -size * (13 * cos(t_rad) - 5 * cos(2 * t_rad) - 2 * cos(3 * t_rad) - cos(4 * t_rad)) / 16
            if t == 0:
                path.moveTo(x, y)
            else:
                path.lineTo(x, y)
        
        # Preencher o coração com vermelho
        painter.fillPath(path, QColor(255, 0, 0))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HeartWidget()
    window.show()
    sys.exit(app.exec_()) 