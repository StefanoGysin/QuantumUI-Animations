import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QRadialGradient, QLinearGradient
from PySide6.QtCore import Qt, QTimer, QPointF, QRectF
from math import cos, sin, pi, sqrt
import random

class AdvancedGysinIA(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced Gysin-IA")
        self.resize(800, 800)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        # Ângulos e variáveis para animações
        self.angle = 0
        self.pulse_angle = 0
        self.text_opacity = 255
        self.pulse_size = 0
        self.data_points = []
        self.generate_data_points()
        
        # Configurar timer para animação
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(20)  # Animação mais suave
        
    def generate_data_points(self):
        for _ in range(50):
            angle = random.uniform(0, 2*pi)
            radius = random.uniform(100, 280)
            self.data_points.append((angle, radius))
        
    def update_animation(self):
        self.angle = (self.angle + 2) % 360
        self.pulse_angle = (self.pulse_angle + 3) % 360
        self.pulse_size = 10 + sin(self.pulse_angle * pi / 180) * 5
        self.text_opacity = 155 + int(abs(sin(self.pulse_angle * pi / 180)) * 100)
        self.update()
        
    def draw_tech_circle(self, painter, radius, segments):
        for i in range(segments):
            angle = (i * 360 / segments + self.angle) * pi / 180
            next_angle = ((i + 1) * 360 / segments + self.angle) * pi / 180
            
            inner_radius = radius - 10 if i % 2 == 0 else radius - 5
            outer_radius = radius
                
            x1, y1 = cos(angle) * inner_radius, sin(angle) * inner_radius
            x2, y2 = cos(angle) * outer_radius, sin(angle) * outer_radius
            x3, y3 = cos(next_angle) * outer_radius, sin(next_angle) * outer_radius
            x4, y4 = cos(next_angle) * inner_radius, sin(next_angle) * inner_radius
            
            opacity = 100 + abs(sin(angle + self.pulse_angle * pi / 180)) * 155
            painter.setPen(QPen(QColor(0, 255, 255, int(opacity)), 1))
            painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))
            painter.drawLine(QPointF(x2, y2), QPointF(x3, y3))
            painter.drawLine(QPointF(x3, y3), QPointF(x4, y4))
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Centralizar na janela
        painter.translate(self.width() / 2, self.height() / 2)
        
        # Gradiente de fundo circular
        gradient = QRadialGradient(0, 0, 350)
        gradient.setColorAt(0, QColor(0, 50, 100, 30))
        gradient.setColorAt(1, QColor(0, 0, 0, 0))
        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QPointF(0, 0), 350, 350)
        
        # Círculos técnicos
        self.draw_tech_circle(painter, 300, 48)
        self.draw_tech_circle(painter, 260, 36)
        self.draw_tech_circle(painter, 220, 24)
        
        # Círculo externo pulsante
        pen = QPen(QColor(0, 200, 255, 100))
        pen.setWidth(self.pulse_size)
        painter.setPen(pen)
        painter.drawEllipse(QPointF(0, 0), 320, 320)
        
        # Arcos rotativos
        for i in range(6):
            opacity = 255 - i * 30
            width = 8 - i
            pen.setWidth(width)
            pen.setColor(QColor(0, 255, 255, opacity))
            painter.setPen(pen)
            start_angle = (self.angle + i * 20) * 16
            painter.drawArc(QRectF(-320, -320, 640, 640), start_angle, 30 * 16)
        
        # Pontos de dados
        for angle, radius in self.data_points:
            x = cos(angle + self.angle * pi / 180) * radius
            y = sin(angle + self.angle * pi / 180) * radius
            opacity = 100 + abs(sin(angle + self.pulse_angle * pi / 180)) * 155
            painter.setPen(QPen(QColor(0, 255, 255, int(opacity)), 2))
            painter.drawPoint(QPointF(x, y))
        
        # Linhas de conexão
        for i in range(len(self.data_points)):
            for j in range(i+1, min(i+5, len(self.data_points))):
                x1, y1 = cos(self.data_points[i][0] + self.angle * pi / 180) * self.data_points[i][1], sin(self.data_points[i][0] + self.angle * pi / 180) * self.data_points[i][1]
                x2, y2 = cos(self.data_points[j][0] + self.angle * pi / 180) * self.data_points[j][1], sin(self.data_points[j][0] + self.angle * pi / 180) * self.data_points[j][1]
                distance = sqrt((x2-x1)**2 + (y2-y1)**2)
                if distance < 100:
                    opacity = int((1 - distance/100) * 100)
                    painter.setPen(QPen(QColor(0, 255, 255, opacity), 1))
                    painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))
        
        # Texto Gysin-IA com efeito futurista
        font = QFont("Arial", 40, QFont.Bold)
        painter.setFont(font)
        
        # Efeito de brilho dinâmico
        glow_radius = 20
        for i in range(glow_radius):
            opacity = (glow_radius - i) * 8
            y_offset = -sin(self.pulse_angle * pi / 180) * 4
            pen.setColor(QColor(0, 255, 255, opacity))
            painter.setPen(pen)
            painter.drawText(QRectF(-200, -30 + y_offset - i/2, 400, 60), 
                           Qt.AlignCenter, "Gysin-IA")
        
        # Texto principal com opacidade pulsante
        pen.setColor(QColor(255, 255, 255, self.text_opacity))
        painter.setPen(pen)
        painter.drawText(QRectF(-200, -30, 400, 60), Qt.AlignCenter, "Gysin-IA")
        
        # Detalhes técnicos
        detail_font = QFont("Arial", 10)
        painter.setFont(detail_font)
        for i in range(12):
            angle = (i * 30 + self.angle) * pi / 180
            x = cos(angle) * 340
            y = sin(angle) * 340
            text = f"NODE.{i:02d}"
            pen.setColor(QColor(0, 255, 255, 150))
            painter.setPen(pen)
            painter.drawText(QPointF(x-30, y), text)

        # Status dinâmico
        status_text = "ANALYZING..." if self.angle % 180 < 90 else "PROCESSING..."
        painter.setFont(QFont("Arial", 14))
        pen.setColor(QColor(0, 255, 255, 200))
        painter.setPen(pen)
        painter.drawText(QRectF(-100, 320, 200, 30), Qt.AlignCenter, status_text)

    def mousePressEvent(self, event):
        self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        delta = event.globalPosition().toPoint() - self.old_pos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.old_pos = event.globalPosition().toPoint()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AdvancedGysinIA()
    window.show()
    sys.exit(app.exec_())