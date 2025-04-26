import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QRadialGradient, QPainterPath
from PySide6.QtCore import Qt, QTimer, QPointF, QRectF
from math import cos, sin, pi, exp

class HologramAssistant(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hologram Interface")
        self.resize(800, 600)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        # Estados e animação
        self.is_listening = False
        self.rotation = 0
        self.wave_time = 0
        self.scan_line = 0
        
        # Timer para animação
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(16)  # 60 FPS
    
    def update_animation(self):
        self.rotation = (self.rotation + 1) % 360
        self.wave_time = (self.wave_time + 0.1) % (2 * pi)
        self.scan_line = (self.scan_line + 2) % self.height()
        self.update()
    
    def draw_3d_circle(self, painter, cx, cy, radius, num_circles=20):
        for i in range(num_circles):
            angle = self.rotation * pi / 180
            # Simular perspectiva 3D
            scale_x = abs(cos(angle + i * pi / num_circles))
            y_offset = 15 * sin(angle + i * pi / num_circles)
            
            # Desenhar elipse para efeito 3D
            pen = QPen(QColor(0, 200, 255, int(100 * scale_x)))
            pen.setWidth(2)
            painter.setPen(pen)
            painter.drawEllipse(QPointF(cx, cy + y_offset),
                              radius * scale_x, radius)
    
    def draw_hologram_scan(self, painter, rect):
        # Linha de escaneamento holográfico
        gradient = QRadialGradient(rect.center(), rect.width()/2)
        gradient.setColorAt(0, QColor(0, 200, 255, 50))
        gradient.setColorAt(1, QColor(0, 200, 255, 0))
        
        scan_rect = QRectF(rect.x(), self.scan_line - 2,
                          rect.width(), 4)
        painter.fillRect(scan_rect, gradient)
    
    def draw_data_points(self, painter, cx, cy, radius):
        num_points = 36
        for i in range(num_points):
            angle = (i * 360 / num_points + self.rotation) * pi / 180
            x = cx + radius * cos(angle)
            y = cy + radius * sin(angle)
            
            # Pontos de dados holográficos
            size = 3 + 2 * sin(self.wave_time + i)
            opacity = int(100 + 100 * abs(sin(self.wave_time + i)))
            
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(0, 200, 255, opacity))
            painter.drawEllipse(QPointF(x, y), size, size)
            
            # Linhas de conexão
            if i > 0:
                pen = QPen(QColor(0, 200, 255, opacity//2))
                pen.setWidth(1)
                painter.setPen(pen)
                painter.drawLine(QPointF(prev_x, prev_y), QPointF(x, y))
            
            prev_x, prev_y = x, y
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Centro da tela
        center_x = self.width() / 2
        center_y = self.height() / 2
        
        # Fundo com gradiente
        gradient = QRadialGradient(center_x, center_y, 400)
        gradient.setColorAt(0, QColor(0, 40, 60, 30))
        gradient.setColorAt(1, QColor(0, 0, 0, 0))
        painter.fillRect(0, 0, self.width(), self.height(), gradient)
        
        # Círculos 3D girando
        self.draw_3d_circle(painter, center_x, center_y, 150)
        
        # Pontos de dados e conexões
        self.draw_data_points(painter, center_x, center_y, 120)
        
        # Área do holograma
        holo_rect = QRectF(center_x - 200, center_y - 200, 400, 400)
        self.draw_hologram_scan(painter, holo_rect)
        
        # Grade holográfica
        num_lines = 20
        spacing = 400 / num_lines
        pen = QPen(QColor(0, 200, 255, 30))
        pen.setWidth(1)
        painter.setPen(pen)
        
        for i in range(num_lines + 1):
            # Linhas horizontais
            y = center_y - 200 + i * spacing
            y_offset = 5 * sin(self.wave_time + i * 0.2)
            painter.drawLine(QPointF(center_x - 200, y + y_offset),
                           QPointF(center_x + 200, y + y_offset))
            
            # Linhas verticais
            x = center_x - 200 + i * spacing
            x_offset = 5 * sin(self.wave_time + i * 0.2)
            painter.drawLine(QPointF(x + x_offset, center_y - 200),
                           QPointF(x + x_offset, center_y + 200))
        
        # Texto holográfico
        font = QFont("Arial", 40, QFont.Bold)
        painter.setFont(font)
        
        # Efeito de distorção holográfica
        for i in range(5):
            offset = 2 * sin(self.wave_time + i)
            opacity = int(150 + 100 * sin(self.wave_time + i))
            color = QColor(0, 200, 255, opacity)
            
            painter.setPen(color)
            painter.drawText(QRectF(center_x-150, center_y-25+offset, 300, 50),
                           Qt.AlignCenter, "Gysin-IA")
        
        # Status holográfico
        status = "SCANNING..." if self.is_listening else "ANALYZING..."
        font.setPointSize(12)
        painter.setFont(font)
        
        # Efeito de flutuação no status
        y_offset = 5 * sin(self.wave_time * 2)
        painter.setPen(QColor(0, 200, 255, 200))
        painter.drawText(QRectF(center_x-100, center_y+40+y_offset, 200, 30),
                        Qt.AlignCenter, status)

    def mousePressEvent(self, event):
        self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        delta = event.globalPosition().toPoint() - self.old_pos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.old_pos = event.globalPosition().toPoint()
    
    def set_listening(self, is_listening):
        self.is_listening = is_listening

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HologramAssistant()
    window.show()
    sys.exit(app.exec_()) 