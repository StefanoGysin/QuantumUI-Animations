import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QRadialGradient, QLinearGradient
from PySide6.QtCore import Qt, QTimer, QPointF, QRectF, QLineF
from math import cos, sin, pi, exp, sqrt
import random
import string

class EnhancedMatrixAssistant(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enhanced Matrix Interface")
        self.resize(1000, 800)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        # Caracteres Matrix
        self.matrix_chars = []
        self.generate_matrix_chars()
        
        # Estados e animação
        self.is_listening = False
        self.time = 0
        self.pulse = 0
        
        # Raios
        self.lightning_bolts = []
        self.generate_lightning_bolts()
        
        # Timer para animação
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(30)
    
    def generate_matrix_chars(self):
        num_columns = 50
        for i in range(num_columns):
            column = {
                'x': random.randint(0, self.width()),
                'y': random.randint(-500, 0),
                'speed': random.uniform(2, 5),
                'chars': ''.join(random.choices(string.ascii_letters + string.digits, k=30)),
                'opacity': random.randint(100, 255)
            }
            self.matrix_chars.append(column)
    
    def generate_lightning_bolts(self):
        num_bolts = 5
        for _ in range(num_bolts):
            bolt = {
                'start': QPointF(random.randint(0, self.width()), 0),
                'end': QPointF(random.randint(0, self.width()), self.height()),
                'segments': [],
                'lifetime': random.randint(10, 30),
                'alpha': 255
            }
            self.generate_bolt_segments(bolt)
            self.lightning_bolts.append(bolt)
    
    def generate_bolt_segments(self, bolt):
        start = bolt['start']
        end = bolt['end']
        segments = []
        segments.append(start)
        
        while start.y() < end.y():
            next_x = start.x() + random.uniform(-50, 50)
            next_y = start.y() + random.uniform(20, 60)
            next_point = QPointF(next_x, next_y)
            segments.append(next_point)
            start = next_point
        
        segments.append(end)
        bolt['segments'] = segments
    
    def update_animation(self):
        self.time += 0.1
        self.pulse = (self.pulse + 0.05) % (2 * pi)
        
        # Atualizar caracteres Matrix
        for column in self.matrix_chars:
            column['y'] += column['speed']
            if column['y'] > self.height():
                column['y'] = random.randint(-500, 0)
                column['chars'] = ''.join(random.choices(string.ascii_letters + string.digits, k=30))
                column['opacity'] = random.randint(100, 255)
        
        # Atualizar raios
        for bolt in self.lightning_bolts:
            bolt['lifetime'] -= 1
            bolt['alpha'] = max(0, bolt['alpha'] - 10)
            
            if bolt['lifetime'] <= 0 or bolt['alpha'] <= 0:
                self.lightning_bolts.remove(bolt)
                new_bolt = {
                    'start': QPointF(random.randint(0, self.width()), 0),
                    'end': QPointF(random.randint(0, self.width()), self.height()),
                    'segments': [],
                    'lifetime': random.randint(10, 30),
                    'alpha': 255
                }
                self.generate_bolt_segments(new_bolt)
                self.lightning_bolts.append(new_bolt)
        
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Fundo escuro com gradiente
        gradient = QRadialGradient(self.width()/2, self.height()/2, 500)
        gradient.setColorAt(0, QColor(0, 20, 0, 30))
        gradient.setColorAt(1, QColor(0, 0, 0, 0))
        painter.fillRect(0, 0, self.width(), self.height(), gradient)
        
        # Desenhar caracteres Matrix
        self.draw_matrix_rain(painter)
        
        # Desenhar raios
        self.draw_lightning(painter)
        
        # Círculo central
        center_x = self.width() / 2
        center_y = self.height() / 2
        
        # Hexágonos concêntricos
        for i in range(5):
            self.draw_hexagon(painter, center_x, center_y, 100 + i * 30,
                            self.time + i * pi/3)
        
        # Texto central com efeito digital
        self.draw_digital_text(painter, center_x, center_y)
        
        # Status com efeito digital
        status = "SCANNING..." if self.is_listening else "PROCESSING..."
        self.draw_status_text(painter, center_x, center_y + 80, status)
    
    def draw_matrix_rain(self, painter):
        font = QFont("Courier New", 14)
        painter.setFont(font)
        
        for column in self.matrix_chars:
            x, y = column['x'], column['y']
            chars = column['chars']
            for i, char in enumerate(chars):
                opacity = max(0, column['opacity'] - i * 8)
                color = QColor(0, 255, 0, opacity)
                if i == 0:  # Primeiro caractere mais brilhante
                    color = QColor(200, 255, 200, opacity)
                painter.setPen(color)
                painter.drawText(QPointF(x, y + i * 20), char)
    
    def draw_lightning(self, painter):
        for bolt in self.lightning_bolts:
            pen = QPen(QColor(200, 255, 255, bolt['alpha']))
            pen.setWidth(2)
            painter.setPen(pen)
            
            for i in range(len(bolt['segments']) - 1):
                start = bolt['segments'][i]
                end = bolt['segments'][i + 1]
                painter.drawLine(start, end)
            
            # Efeito de brilho
            glow = QRadialGradient(bolt['segments'][-1], 20)
            glow.setColorAt(0, QColor(200, 255, 255, bolt['alpha']))
            glow.setColorAt(1, QColor(200, 255, 255, 0))
            painter.setBrush(glow)
            painter.drawEllipse(bolt['segments'][-1], 20, 20)
    
    def draw_hexagon(self, painter, cx, cy, size, rotation):
        points = []
        for i in range(6):
            angle = rotation + i * pi / 3
            x = cx + size * cos(angle)
            y = cy + size * sin(angle)
            points.append(QPointF(x, y))
        
        # Desenhar linhas do hexágono
        pen = QPen(QColor(0, 255, 0, 100))
        pen.setWidth(2)
        painter.setPen(pen)
        
        for i in range(6):
            j = (i + 1) % 6
            painter.drawLine(points[i], points[j])
        
        # Pontos nos vértices
        for point in points:
            painter.drawEllipse(point, 3, 3)
    
    def draw_digital_text(self, painter, cx, cy):
        text = "Gysin-IA"
        font = QFont("Courier New", 50, QFont.Bold)
        painter.setFont(font)
        
        # Efeito de glitch
        for i in range(5):
            offset = random.uniform(-2, 2) * sin(self.pulse)
            opacity = int(200 + 55 * sin(self.pulse + i))
            painter.setPen(QColor(0, 255, 0, opacity))
            painter.drawText(QRectF(cx-200, cy-35+offset, 400, 70),
                           Qt.AlignCenter, text)
        
        # Texto principal
        painter.setPen(QColor(200, 255, 200))
        painter.drawText(QRectF(cx-200, cy-35, 400, 70),
                        Qt.AlignCenter, text)
    
    def draw_status_text(self, painter, cx, cy, text):
        font = QFont("Courier New", 16)
        painter.setFont(font)
        
        # Efeito de digitalização
        for i in range(len(text)):
            if random.random() < 0.1:  # 10% de chance de glitch
                char = random.choice(string.ascii_uppercase + string.digits)
            else:
                char = text[i]
            
            x = cx - len(text)*7 + i*14
            y = cy
            
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
    window = EnhancedMatrixAssistant()
    window.show()
    sys.exit(app.exec_())