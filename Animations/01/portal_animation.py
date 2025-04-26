import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QRadialGradient, QLinearGradient
from PySide6.QtCore import Qt, QTimer, QPointF, QRectF
from math import cos, sin, pi

class PortalWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Portal Energético")
        self.resize(600, 600)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        self.angle = 0
        self.portal_pulse = 0
        self.energy_wave = 0
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(30)
    
    def update_animation(self):
        self.angle = (self.angle + 2) % 360
        self.portal_pulse = (self.portal_pulse + 0.1) % (2 * pi)
        self.energy_wave = (self.energy_wave + 0.05) % (2 * pi)
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        
        # Portal com gradiente roxo pulsante
        portal_size = 200 + sin(self.portal_pulse) * 10
        gradient = QRadialGradient(0, 0, portal_size)
        pulse = abs(sin(self.portal_pulse))
        gradient.setColorAt(0, QColor(180, 0, 255, int(150 * pulse)))
        gradient.setColorAt(0.5, QColor(120, 0, 180, int(100 * pulse)))
        gradient.setColorAt(1, QColor(60, 0, 100, 0))
        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(-portal_size, -portal_size, portal_size * 2, portal_size * 2)
        
        # Anéis energéticos
        for i in range(5):
            radius = 100 + i * 30
            pen = QPen(QColor(180, 0, 255, 150 - i * 20))
            pen.setWidth(3)
            painter.setPen(pen)
            
            # Desenhar segmentos do anel
            for j in range(36):
                start_angle = (j * 10 + self.angle) * pi / 180
                end_angle = ((j + 1) * 10 + self.angle) * pi / 180
                
                x1 = radius * cos(start_angle)
                y1 = radius * sin(start_angle)
                x2 = radius * cos(end_angle)
                y2 = radius * sin(end_angle)
                
                if j % 2 == 0:
                    painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))
        
        # Ondas de energia
        for i in range(8):
            angle = (i * 45 + self.angle) * pi / 180
            start_radius = 50
            end_radius = 250 + sin(self.energy_wave + i) * 20
            
            pen = QPen(QColor(200, 100, 255, 100))
            pen.setWidth(2)
            painter.setPen(pen)
            
            x1 = start_radius * cos(angle)
            y1 = start_radius * sin(angle)
            x2 = end_radius * cos(angle)
            y2 = end_radius * sin(angle)
            
            painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))
            
            # Partículas nas pontas
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(200, 100, 255, 150))
            particle_size = 4 + sin(self.portal_pulse + i) * 2
            painter.drawEllipse(QPointF(x2, y2), particle_size, particle_size)
        
        # Texto central com efeito de brilho
        font = QFont("Arial", 35, QFont.Bold)
        painter.setFont(font)
        
        # Sombra do texto
        for i in range(10):
            opacity = (10 - i) * 10
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
    window = PortalWidget()
    window.show()
    sys.exit(app.exec_()) 