import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QRadialGradient, QPainterPath, QLinearGradient
from PySide6.QtCore import Qt, QTimer, QPointF, QRectF
from math import cos, sin, pi, sqrt, exp, pow
import random

class GridFaceWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grid Face")
        self.showFullScreen()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        # Cores
        self.color = QColor(0, 150, 255)  # Azul brilhante
        
        # Grade
        self.grid_points = []
        self.initialize_grid()
        
        # Timer para animação suave dos pontos
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(50)
        
        self.time = 0
    
    def create_oval_point(self, u, v):
        # Normalizar coordenadas para -1 a 1
        nx = u * 2 - 1
        ny = v * 2 - 1
        
        # Criar forma oval
        oval_factor = sqrt(pow(nx, 2)/1.2 + pow(ny, 2)/1.8)
        if oval_factor > 1:
            return None, None
        
        # Dimensões do rosto
        width = 400
        height = 500
        
        # Calcular coordenadas
        x = nx * width * (1 - 0.1 * abs(ny))  # Leve estreitamento nas extremidades
        y = ny * height
        
        return x, y
    
    def initialize_grid(self):
        # Criar grade uniforme
        resolution = 30  # Número de pontos em cada direção
        
        for i in range(resolution):
            for j in range(resolution):
                u = i / (resolution - 1)
                v = j / (resolution - 1)
                
                x, y = self.create_oval_point(u, v)
                if x is not None:
                    self.grid_points.append({
                        'x': x,
                        'y': y,
                        'orig_x': x,
                        'orig_y': y,
                        'phase': random.uniform(0, 2*pi)
                    })
    
    def update_animation(self):
        self.time += 0.05
        for point in self.grid_points:
            # Movimento muito sutil dos pontos
            point['x'] = point['orig_x'] + cos(self.time + point['phase']) * 1
            point['y'] = point['orig_y'] + sin(self.time + point['phase']) * 1
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Centralizar na janela
        painter.translate(self.width() / 2, self.height() / 2)
        
        # Desenhar linhas entre pontos próximos
        max_dist = 30  # Distância máxima para conectar pontos
        
        # Primeiro, desenhar todas as linhas
        pen = QPen(self.color)
        pen.setWidth(1)
        painter.setPen(pen)
        
        for i, p1 in enumerate(self.grid_points):
            for p2 in self.grid_points[i+1:]:
                dx = p1['x'] - p2['x']
                dy = p1['y'] - p2['y']
                dist = sqrt(dx*dx + dy*dy)
                
                if dist < max_dist:
                    opacity = int(255 * (1 - dist/max_dist))
                    pen.setColor(QColor(0, 150, 255, opacity))
                    painter.setPen(pen)
                    painter.drawLine(QPointF(p1['x'], p1['y']), 
                                   QPointF(p2['x'], p2['y']))
        
        # Depois, desenhar os pontos por cima
        for point in self.grid_points:
            # Brilho do ponto
            glow = QRadialGradient(point['x'], point['y'], 4)
            glow.setColorAt(0, QColor(0, 150, 255, 200))
            glow.setColorAt(1, QColor(0, 150, 255, 0))
            
            painter.setBrush(glow)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(QPointF(point['x'], point['y']), 2, 2)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.close()
        self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        delta = event.globalPosition().toPoint() - self.old_pos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.old_pos = event.globalPosition().toPoint()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GridFaceWidget()
    window.show()
    sys.exit(app.exec_()) 