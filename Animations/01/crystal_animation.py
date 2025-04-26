import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QRadialGradient
from PySide6.QtCore import Qt, QTimer, QPointF, QRectF
from math import cos, sin, pi

class CrystalWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cristais Mágicos")
        self.resize(600, 600)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        self.angle = 0
        self.crystal_pulse = 0
        self.magic_wave = 0
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(30)
    
    def update_animation(self):
        self.angle = (self.angle + 1) % 360
        self.crystal_pulse = (self.crystal_pulse + 0.08) % (2 * pi)
        self.magic_wave = (self.magic_wave + 0.05) % (2 * pi)
        self.update()
    
    def draw_crystal(self, painter, x, y, size, rotation):
        points = []
        sides = 6
        for i in range(sides):
            angle = (rotation + i * 360 / sides) * pi / 180
            px = x + size * cos(angle)
            py = y + size * sin(angle)
            points.append(QPointF(px, py))
        
        # Desenhar cristal com gradiente
        gradient = QRadialGradient(x, y, size)
        pulse = abs(sin(self.crystal_pulse))
        gradient.setColorAt(0, QColor(200, 100, 255, int(200 * pulse)))
        gradient.setColorAt(1, QColor(100, 0, 150, int(100 * pulse)))
        
        painter.setBrush(gradient)
        painter.setPen(QPen(QColor(220, 180, 255, 150), 2))
        
        # Desenhar o hexágono
        for i in range(sides):
            j = (i + 1) % sides
            painter.drawLine(points[i], points[j])
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        
        # Fundo mágico
        gradient = QRadialGradient(0, 0, 300)
        gradient.setColorAt(0, QColor(60, 0, 100, 30))
        gradient.setColorAt(1, QColor(0, 0, 0, 0))
        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(-300, -300, 600, 600)
        
        # Cristais orbitando
        num_crystals = 6
        for i in range(num_crystals):
            angle = self.angle + i * (360 / num_crystals)
            radius = 150 + sin(self.crystal_pulse + i) * 20
            x = radius * cos(angle * pi / 180)
            y = radius * sin(angle * pi / 180)
            size = 30 + sin(self.crystal_pulse + i) * 5
            self.draw_crystal(painter, x, y, size, angle)
            
            # Linhas de energia entre cristais
            if i > 0:
                prev_x = radius * cos((angle - 360/num_crystals) * pi / 180)
                prev_y = radius * sin((angle - 360/num_crystals) * pi / 180)
                
                pen = QPen(QColor(180, 100, 255, 100))
                pen.setWidth(2)
                painter.setPen(pen)
                painter.drawLine(QPointF(prev_x, prev_y), QPointF(x, y))
        
        # Cristal central maior
        self.draw_crystal(painter, 0, 0, 50 + sin(self.crystal_pulse) * 10, self.angle * 2)
        
        # Partículas mágicas
        for i in range(20):
            angle = (self.angle * 3 + i * 18) * pi / 180
            radius = 100 + 50 * sin(self.magic_wave + i)
            x = radius * cos(angle)
            y = radius * sin(angle)
            
            size = 3 + sin(self.crystal_pulse + i) * 2
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(220, 180, 255, 150))
            painter.drawEllipse(QPointF(x, y), size, size)
        
        # Texto central
        font = QFont("Arial", 35, QFont.Bold)
        painter.setFont(font)
        
        # Sombra mágica do texto
        for i in range(10):
            opacity = (10 - i) * 15
            pen = QPen(QColor(180, 0, 255, opacity))
            painter.setPen(pen)
            offset = i * 0.5
            painter.drawText(QRectF(-150, -20 - offset, 300, 40),
                           Qt.AlignCenter, "Gysin-IA")
        
        # Texto principal em branco
        pen = QPen(QColor(255, 255, 255))
        painter.setPen(pen)
        painter.drawText(QRectF(-150, -20, 300, 40),
                        Qt.AlignCenter, "Gysin-IA")

    def mousePressEvent(self, event):
        self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        delta = event.globalPosition().toPoint() - self.old_pos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.old_pos = event.globalPosition().toPoint()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CrystalWidget()
    window.show()
    sys.exit(app.exec_()) 