import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QRadialGradient
from PySide6.QtCore import Qt, QTimer, QPointF, QRectF
from math import cos, sin, pi, sqrt

class ScannerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scanner Holográfico")
        self.resize(600, 600)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        self.scan_angle = 0
        self.wave_offset = 0
        self.scan_line = 0
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(30)
    
    def update_animation(self):
        self.scan_angle = (self.scan_angle + 4) % 360
        self.wave_offset = (self.wave_offset + 0.2) % (2 * pi)
        self.scan_line = (self.scan_line + 2) % 200
        self.update()
    
    def draw_scan_line(self, painter, start_x, start_y, end_x, end_y):
        gradient = QRadialGradient(start_x, start_y, 200)
        gradient.setColorAt(0, QColor(0, 255, 255, 100))
        gradient.setColorAt(1, QColor(0, 255, 255, 0))
        pen = QPen()
        pen.setBrush(gradient)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawLine(QPointF(start_x, start_y), QPointF(end_x, end_y))
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        
        # Grade de fundo
        pen = QPen(QColor(0, 255, 255, 30))
        pen.setWidth(1)
        painter.setPen(pen)
        
        for i in range(-300, 301, 30):
            # Linhas horizontais com onda
            for x in range(-300, 301, 5):
                y1 = i + sin(x/30 + self.wave_offset) * 5
                y2 = i + sin((x+5)/30 + self.wave_offset) * 5
                painter.drawLine(QPointF(x, y1), QPointF(x+5, y2))
            
            # Linhas verticais
            painter.drawLine(QPointF(i, -300), QPointF(i, 300))
        
        # Círculo de escaneamento
        scan_radius = 200
        painter.setPen(Qt.NoPen)
        
        # Linha de escaneamento girando
        angle_rad = self.scan_angle * pi / 180
        end_x = scan_radius * cos(angle_rad)
        end_y = scan_radius * sin(angle_rad)
        
        # Efeito de escaneamento
        for i in range(5):
            opacity = 150 - i * 30
            width = 3 - i * 0.5
            pen = QPen(QColor(0, 255, 255, opacity))
            pen.setWidth(width)
            painter.setPen(pen)
            
            scan_angle = (self.scan_angle - i * 5) * pi / 180
            x = scan_radius * cos(scan_angle)
            y = scan_radius * sin(scan_angle)
            self.draw_scan_line(painter, 0, 0, x, y)
        
        # Círculos concêntricos
        for i in range(4):
            radius = 50 + i * 50
            pen = QPen(QColor(0, 255, 255, 100 - i * 20))
            pen.setWidth(2)
            painter.setPen(pen)
            painter.drawEllipse(QPointF(0, 0), radius, radius)
        
        # Pontos de dados
        for i in range(12):
            angle = i * 30 * pi / 180
            radius = 150 + sin(self.wave_offset + i) * 20
            x = radius * cos(angle)
            y = radius * sin(angle)
            
            # Conectar pontos
            if i > 0:
                pen = QPen(QColor(0, 255, 255, 100))
                pen.setWidth(1)
                painter.setPen(pen)
                painter.drawLine(prev_point, QPointF(x, y))
            
            # Desenhar ponto
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(0, 255, 255, 150))
            painter.drawEllipse(QPointF(x, y), 4, 4)
            
            prev_point = QPointF(x, y)
        
        # Linha de escaneamento horizontal
        scan_gradient = QRadialGradient(0, self.scan_line - 100, 300)
        scan_gradient.setColorAt(0, QColor(0, 255, 255, 50))
        scan_gradient.setColorAt(1, QColor(0, 255, 255, 0))
        painter.setBrush(scan_gradient)
        painter.setPen(Qt.NoPen)
        painter.drawRect(-300, self.scan_line - 100, 600, 5)
        
        # Texto central com efeito de escaneamento
        font = QFont("Arial", 30, QFont.Bold)
        painter.setFont(font)
        
        scan_height = 40
        clip_rect = QRectF(-100, -20, 200, scan_height)
        painter.setClipRect(clip_rect)
        
        # Efeito de escaneamento no texto
        scan_y = -20 + (self.scan_line % scan_height)
        scan_gradient = QRadialGradient(0, scan_y, 100)
        scan_gradient.setColorAt(0, QColor(0, 255, 255, 255))
        scan_gradient.setColorAt(1, QColor(0, 255, 255, 100))
        
        pen = QPen()
        pen.setBrush(scan_gradient)
        painter.setPen(pen)
        painter.drawText(clip_rect, Qt.AlignCenter, "Gysin-IA")
        
        painter.setClipping(False)

    def mousePressEvent(self, event):
        self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        delta = event.globalPosition().toPoint() - self.old_pos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.old_pos = event.globalPosition().toPoint()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ScannerWidget()
    window.show()
    sys.exit(app.exec_()) 