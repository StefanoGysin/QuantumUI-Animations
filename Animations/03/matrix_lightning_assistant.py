import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QRadialGradient, QPainterPath
from PySide6.QtCore import Qt, QTimer, QPointF, QRectF
from math import cos, sin, pi, exp, sqrt
import random
import string

class LightningMatrixAssistant(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lightning Matrix Interface")
        self.resize(800, 600)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        # Caracteres Matrix
        self.matrix_chars = []
        self.generate_matrix_chars()
        
        # Raios
        self.lightning_bolts = []
        self.lightning_timer = 0
        
        # Estados e animação
        self.is_listening = False
        self.time = 0
        self.pulse = 0
        self.energy_level = 0
        
        # Timer para animação
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(30)
    
    def generate_matrix_chars(self):
        num_columns = 40  # Aumentado para mais densidade
        for i in range(num_columns):
            column = {
                'x': random.randint(0, self.width()),
                'y': random.randint(-500, 0),
                'speed': random.uniform(2, 6),
                'chars': ''.join(random.choices(string.ascii_letters + string.digits, k=25)),
                'opacity': random.randint(100, 255)
            }
            self.matrix_chars.append(column)
    
    def generate_lightning(self):
        if len(self.lightning_bolts) < 3 and random.random() < 0.1:
            start = QPointF(random.randint(0, self.width()), 0)
            end = QPointF(self.width()/2 + random.randint(-100, 100),
                         self.height()/2 + random.randint(-100, 100))
            segments = self.create_lightning_path(start, end)
            self.lightning_bolts.append({
                'segments': segments,
                'life': 5,
                'opacity': 255
            })
    
    def create_lightning_path(self, start, end):
        segments = []
        current = QPointF(start)
        target = QPointF(end)
        
        while current.y() < target.y():
            next_point = QPointF(
                current.x() + random.uniform(-30, 30),
                current.y() + random.uniform(20, 40)
            )
            segments.append((current, next_point))
            current = next_point
        
        segments.append((current, target))
        return segments
    
    def update_animation(self):
        self.time += 0.1
        self.pulse = (self.pulse + 0.05) % (2 * pi)
        self.energy_level = (sin(self.time * 0.5) + 1) * 0.5
        
        # Atualizar caracteres Matrix
        for column in self.matrix_chars:
            column['y'] += column['speed']
            if column['y'] > self.height():
                column['y'] = random.randint(-500, 0)
                column['chars'] = ''.join(random.choices(string.ascii_letters + string.digits, k=25))
                column['opacity'] = random.randint(100, 255)
        
        # Gerar e atualizar raios
        self.generate_lightning()
        
        # Atualizar raios existentes
        for bolt in self.lightning_bolts[:]:
            bolt['life'] -= 0.2
            bolt['opacity'] = int(bolt['life'] * 51)  # 255/5 = 51
            if bolt['life'] <= 0:
                self.lightning_bolts.remove(bolt)
        
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Fundo com gradiente mais elaborado
        gradient = QRadialGradient(self.width()/2, self.height()/2, 400)
        gradient.setColorAt(0, QColor(0, 30, 30, 40))
        gradient.setColorAt(0.5, QColor(0, 20, 20, 30))
        gradient.setColorAt(1, QColor(0, 0, 0, 20))
        painter.fillRect(0, 0, self.width(), self.height(), gradient)
        
        # Desenhar caracteres Matrix
        self.draw_matrix_effect(painter)
        
        # Desenhar efeitos centrais
        center_x = self.width() / 2
        center_y = self.height() / 2
        
        # Círculos de energia
        self.draw_energy_circles(painter, center_x, center_y)
        
        # Hexágonos giratórios
        self.draw_rotating_hexagons(painter, center_x, center_y)
        
        # Raios
        self.draw_lightning_bolts(painter)
        
        # Interface central
        self.draw_central_interface(painter, center_x, center_y)
        
        # Status
        self.draw_enhanced_status(painter, center_x, center_y)
    
    def draw_matrix_effect(self, painter):
        font = QFont("Courier New", 14)
        painter.setFont(font)
        
        for column in self.matrix_chars:
            x, y = column['x'], column['y']
            chars = column['chars']
            for i, char in enumerate(chars):
                opacity = max(0, column['opacity'] - i * 10)
                color = QColor(0, 255, 0, opacity)
                if i == 0:
                    color = QColor(200, 255, 200, opacity)
                painter.setPen(color)
                painter.drawText(QPointF(x, y + i * 20), char)
    
    def draw_energy_circles(self, painter, cx, cy):
        for i in range(3):
            radius = 150 + i * 30 + sin(self.pulse + i) * 10
            gradient = QRadialGradient(cx, cy, radius)
            gradient.setColorAt(0, QColor(0, 255, 0, 0))
            gradient.setColorAt(0.8, QColor(0, 255, 0, 30))
            gradient.setColorAt(1, QColor(0, 255, 0, 0))
            painter.setBrush(gradient)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(QPointF(cx, cy), radius, radius)
    
    def draw_rotating_hexagons(self, painter, cx, cy):
        for i in range(3):
            size = 100 + i * 30
            rotation = self.time + i * pi/3
            points = []
            for j in range(6):
                angle = rotation + j * pi / 3
                x = cx + size * cos(angle)
                y = cy + size * sin(angle)
                points.append(QPointF(x, y))
            
            pen = QPen(QColor(0, 255, 0, 100))
            pen.setWidth(2)
            painter.setPen(pen)
            
            for j in range(6):
                next_j = (j + 1) % 6
                painter.drawLine(points[j], points[next_j])
                painter.drawEllipse(points[j], 3, 3)
    
    def draw_lightning_bolts(self, painter):
        for bolt in self.lightning_bolts:
            pen = QPen(QColor(0, 255, 255, bolt['opacity']))
            pen.setWidth(3)
            painter.setPen(pen)
            
            for segment in bolt['segments']:
                painter.drawLine(segment[0], segment[1])
                
                # Brilho ao redor do raio
                glow = QPen(QColor(0, 255, 255, bolt['opacity'] // 3))
                glow.setWidth(6)
                painter.setPen(glow)
                painter.drawLine(segment[0], segment[1])
    
    def draw_central_interface(self, painter, cx, cy):
        # Texto principal com efeito de glitch
        text = "Gysin-IA"
        font = QFont("Courier New", 40, QFont.Bold)
        painter.setFont(font)
        
        for i in range(5):
            offset = random.uniform(-2, 2) * sin(self.pulse)
            opacity = int(200 + 55 * sin(self.pulse + i))
            color = QColor(0, 255, 0, opacity)
            if random.random() < 0.1:  # Chance de cor diferente
                color = QColor(0, 255, 255, opacity)
            painter.setPen(color)
            painter.drawText(QRectF(cx-150, cy-25+offset, 300, 50),
                           Qt.AlignCenter, text)
    
    def draw_enhanced_status(self, painter, cx, cy):
        status = "SCANNING..." if self.is_listening else "PROCESSING..."
        font = QFont("Courier New", 12)
        painter.setFont(font)
        
        # Barra de energia
        bar_width = 200
        bar_height = 10
        energy_width = bar_width * self.energy_level
        
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(0, 255, 0, 50))
        painter.drawRect(cx - bar_width/2, cy + 70, bar_width, bar_height)
        
        painter.setBrush(QColor(0, 255, 0, 150))
        painter.drawRect(cx - bar_width/2, cy + 70, energy_width, bar_height)
        
        # Status text com efeito digital
        for i in range(len(status)):
            if random.random() < 0.1:
                char = random.choice(string.ascii_uppercase + string.digits)
            else:
                char = status[i]
            
            x = cx - len(status)*5 + i*10
            y = cy + 50
            
            painter.setPen(QColor(0, 255, 0, 200))
            painter.drawText(QPointF(x, y), char)

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
    window = LightningMatrixAssistant()
    window.show()
    sys.exit(app.exec_()) 