import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QRadialGradient
from PySide6.QtCore import Qt, QTimer, QPointF, QRectF
from math import cos, sin, pi

class ReactorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reator de Energia")
        self.resize(600, 600)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        self.angle = 0
        self.energy_level = 0
        self.pulse = 0
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(30)
    
    def update_animation(self):
        self.angle = (self.angle + 3) % 360
        self.energy_level = (self.energy_level + 0.05) % (2 * pi)
        self.pulse = (self.pulse + 0.1) % (2 * pi)
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        
        # Núcleo do reator com gradiente pulsante
        core_gradient = QRadialGradient(0, 0, 100)
        energy = abs(sin(self.energy_level))
        core_gradient.setColorAt(0, QColor(0, 255, 255, int(200 * energy)))
        core_gradient.setColorAt(0.5, QColor(0, 150, 255, int(100 * energy)))
        core_gradient.setColorAt(1, QColor(0, 50, 255, 0))
        painter.setBrush(core_gradient)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(-100, -100, 200, 200)
        
        # Anéis de energia
        for i in range(3):
            radius = 120 + i * 30
            pen = QPen(QColor(0, 255, 255, 100 - i * 20))
            pen.setWidth(2)
            painter.setPen(pen)
            
            # Anel principal
            painter.drawEllipse(-radius, -radius, radius * 2, radius * 2)
            
            # Segmentos de energia
            for j in range(12):
                angle = (j * 30 + self.angle) * pi / 180
                next_angle = ((j + 1) * 30 + self.angle) * pi / 180
                
                x1 = radius * cos(angle)
                y1 = radius * sin(angle)
                x2 = radius * cos(next_angle)
                y2 = radius * sin(next_angle)
                
                # Pulso de energia
                pulse_pos = (angle + self.pulse) % (2 * pi)
                if pulse_pos < pi/6:
                    opacity = int(255 * (1 - pulse_pos/(pi/6)))
                    pen.setColor(QColor(0, 255, 255, opacity))
                    painter.setPen(pen)
                    painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))
        
        # Partículas de energia
        for i in range(20):
            angle = (self.angle * 2 + i * 18) * pi / 180
            radius = 80 + 20 * sin(self.pulse + i)
            x = radius * cos(angle)
            y = radius * sin(angle)
            
            particle_size = 3 + 2 * sin(self.pulse + i)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(0, 255, 255, 150))
            painter.drawEllipse(QPointF(x, y), particle_size, particle_size)
        
        # Medidores de energia
        font = QFont("Arial", 8)
        painter.setFont(font)
        for i in range(8):
            angle = i * 45 * pi / 180
            x = 200 * cos(angle)
            y = 200 * sin(angle)
            
            level = abs(sin(self.energy_level + i))
            text = f"E{i:02d}:{int(level*100):02d}%"
            
            pen = QPen(QColor(0, 255, 255, 150))
            painter.setPen(pen)
            painter.drawText(QPointF(x-30, y), text)
        
        # Texto central
        font = QFont("Arial", 30, QFont.Bold)
        painter.setFont(font)
        
        # Efeito de energia pulsante
        glow = abs(sin(self.pulse)) * 255
        for i in range(10):
            opacity = (10 - i) * glow / 10
            pen = QPen(QColor(0, 255, 255, int(opacity)))
            painter.setPen(pen)
            offset = sin(self.pulse) * 3
            painter.drawText(QRectF(-100, -20 + offset, 200, 40),
                           Qt.AlignCenter, "Gysin-IA")

    def mousePressEvent(self, event):
        self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        delta = event.globalPosition().toPoint() - self.old_pos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.old_pos = event.globalPosition().toPoint()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ReactorWidget()
    window.show()
    sys.exit(app.exec_()) 