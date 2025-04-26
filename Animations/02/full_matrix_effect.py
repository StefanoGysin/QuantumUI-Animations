import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QRadialGradient
from PySide6.QtCore import Qt, QTimer, QPointF, QRectF
from math import cos, sin, pi, exp
import random
import string

class FullMatrixEffect(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Matrix Effect")
        # Fazer janela em tela cheia
        self.showFullScreen()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        # Caracteres Matrix
        self.matrix_streams = []
        self.japanese_chars = ''.join(chr(i) for i in range(0x30A0, 0x30FF + 1))  # Katakana
        self.all_chars = self.japanese_chars + string.ascii_letters + string.digits
        
        # Estados e animação
        self.time = 0
        self.pulse = 0
        self.is_listening = False
        
        # Inicializar streams
        self.initialize_streams()
        
        # Timer para animação
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(50)  # Velocidade da animação
    
    def initialize_streams(self):
        spacing = 25  # Espaçamento entre colunas
        num_columns = self.width() // spacing
        
        for i in range(num_columns):
            stream = {
                'x': i * spacing,
                'y': random.randint(-1000, 0),
                'speed': random.uniform(3, 10),
                'length': random.randint(15, 30),
                'chars': self.generate_chars(random.randint(15, 30)),
                'brightness': random.uniform(0.5, 1.0)
            }
            self.matrix_streams.append(stream)
    
    def generate_chars(self, length):
        return [random.choice(self.all_chars) for _ in range(length)]
    
    def update_animation(self):
        self.time += 0.1
        self.pulse = (self.pulse + 0.05) % (2 * pi)
        
        # Atualizar streams
        for stream in self.matrix_streams:
            stream['y'] += stream['speed']
            
            # Resetar stream quando sair da tela
            if stream['y'] - len(stream['chars']) * 20 > self.height():
                stream['y'] = random.randint(-500, 0)
                stream['chars'] = self.generate_chars(len(stream['chars']))
                stream['speed'] = random.uniform(3, 10)
                stream['brightness'] = random.uniform(0.5, 1.0)
            
            # Chance de mudar caracteres aleatoriamente
            if random.random() < 0.05:
                idx = random.randint(0, len(stream['chars']) - 1)
                stream['chars'][idx] = random.choice(self.all_chars)
        
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Fundo preto semi-transparente
        painter.fillRect(0, 0, self.width(), self.height(), QColor(0, 0, 0, 200))
        
        # Desenhar streams matrix
        font = QFont("Courier New", 14)
        painter.setFont(font)
        
        for stream in self.matrix_streams:
            x = stream['x']
            y = stream['y']
            chars = stream['chars']
            brightness = stream['brightness']
            
            for i, char in enumerate(chars):
                # Calcular opacidade baseada na posição
                fade = 1 - (i / len(chars))
                glow = abs(sin(self.pulse + i * 0.1))
                
                # Primeiro caractere mais brilhante
                if i == 0:
                    color = QColor(200, 255, 200, int(255 * brightness))
                else:
                    green = int(180 * fade * brightness)
                    opacity = int(255 * fade * brightness)
                    color = QColor(0, green, 0, opacity)
                
                # Adicionar efeito de brilho
                if random.random() < 0.01:
                    color = QColor(200, 255, 200, int(255 * brightness))
                
                painter.setPen(color)
                painter.drawText(QPointF(x, y - i * 20), char)
        
        # Desenhar interface central
        center_x = self.width() / 2
        center_y = self.height() / 2
        
        # Círculo central com efeito de pulso
        radius = 150 + sin(self.pulse) * 10
        for i in range(3):
            opacity = 100 - i * 30
            pen = QPen(QColor(0, 255, 0, opacity))
            pen.setWidth(2)
            painter.setPen(pen)
            painter.drawEllipse(QPointF(center_x, center_y), radius + i * 20, radius + i * 20)
        
        # Texto Gysin-IA com efeito glitch
        font = QFont("Courier New", 40, QFont.Bold)
        painter.setFont(font)
        
        # Efeito de glitch no texto
        for i in range(5):
            if random.random() < 0.1:  # Chance de glitch
                offset_x = random.uniform(-2, 2)
                offset_y = random.uniform(-2, 2)
            else:
                offset_x = offset_y = 0
            
            opacity = int(200 + 55 * sin(self.pulse + i))
            painter.setPen(QColor(0, 255, 0, opacity))
            painter.drawText(QRectF(center_x-150+offset_x, center_y-25+offset_y, 300, 50),
                           Qt.AlignCenter, "Gysin-IA")
        
        # Status com efeito matrix
        status = "SCANNING..." if self.is_listening else "ANALYZING..."
        font.setPointSize(12)
        painter.setFont(font)
        
        for i, char in enumerate(status):
            if random.random() < 0.05:  # Chance de glitch
                char = random.choice(self.all_chars)
            
            x = center_x - len(status)*5 + i*10
            y = center_y + 50
            
            opacity = int(200 + 55 * sin(self.pulse + i * 0.5))
            painter.setPen(QColor(0, 255, 0, opacity))
            painter.drawText(QPointF(x, y), char)

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
    
    def set_listening(self, is_listening):
        self.is_listening = is_listening

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FullMatrixEffect()
    window.show()
    sys.exit(app.exec_()) 