import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QRadialGradient, QPainterPath
from PySide6.QtCore import Qt, QTimer, QPointF, QRectF
from math import cos, sin, pi, exp

class AssistantWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Assistente Virtual")
        self.resize(800, 600)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        # Estados da animação
        self.is_listening = False
        self.is_speaking = True
        self.energy_level = 0.5
        
        # Variáveis de animação
        self.wave_time = 0
        self.ring_rotation = 0
        self.pulse = 0
        self.particle_time = 0
        
        # Configurar timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(16)  # 60 FPS para animação mais suave
    
    def update_animation(self):
        # Atualizar variáveis de animação
        self.wave_time = (self.wave_time + 0.1) % (2 * pi)
        self.ring_rotation = (self.ring_rotation + 2) % 360
        self.pulse = (self.pulse + 0.05) % (2 * pi)
        self.particle_time += 0.02
        
        # Simular níveis de energia variáveis
        self.energy_level = 0.5 + 0.3 * sin(self.pulse)
        self.update()
    
    def draw_energy_ring(self, painter, center_x, center_y, radius, num_particles):
        for i in range(num_particles):
            angle = (i * 360 / num_particles + self.ring_rotation) * pi / 180
            
            # Posição da partícula
            x = center_x + radius * cos(angle)
            y = center_y + radius * sin(angle)
            
            # Tamanho e opacidade variáveis
            size = 4 + 2 * sin(self.pulse + i * 0.2)
            opacity = int(100 + 100 * abs(sin(self.pulse + i * 0.1)))
            
            # Desenhar partícula
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(180, 0, 255, opacity))
            painter.drawEllipse(QPointF(x, y), size, size)
            
            # Conectar com próxima partícula
            if i > 0:
                prev_angle = ((i-1) * 360 / num_particles + self.ring_rotation) * pi / 180
                prev_x = center_x + radius * cos(prev_angle)
                prev_y = center_y + radius * sin(prev_angle)
                
                # Linha de energia
                gradient = QRadialGradient(x, y, 20)
                gradient.setColorAt(0, QColor(180, 0, 255, opacity))
                gradient.setColorAt(1, QColor(180, 0, 255, 0))
                
                pen = QPen()
                pen.setBrush(gradient)
                pen.setWidth(2)
                painter.setPen(pen)
                painter.drawLine(QPointF(prev_x, prev_y), QPointF(x, y))
    
    def draw_wave_circle(self, painter, center_x, center_y, base_radius):
        num_points = 180
        path = QPainterPath()
        first_point = None
        
        for i in range(num_points + 1):
            angle = (i * 360 / num_points) * pi / 180
            # Raio variável baseado em várias ondas
            radius = base_radius + 20 * sin(4 * angle + self.wave_time) * self.energy_level
            radius += 10 * cos(8 * angle - self.wave_time * 2) * self.energy_level
            
            x = center_x + radius * cos(angle)
            y = center_y + radius * sin(angle)
            
            if i == 0:
                path.moveTo(x, y)
                first_point = (x, y)
            else:
                path.lineTo(x, y)
        
        if first_point:
            path.lineTo(first_point[0], first_point[1])
        
        # Desenhar com gradiente
        gradient = QRadialGradient(center_x, center_y, base_radius * 2)
        gradient.setColorAt(0, QColor(180, 0, 255, 100))
        gradient.setColorAt(1, QColor(100, 0, 150, 0))
        
        painter.setPen(QPen(QColor(180, 0, 255, 100), 2))
        painter.setBrush(gradient)
        painter.drawPath(path)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Centro da tela
        center_x = self.width() / 2
        center_y = self.height() / 2
        
        # Fundo com gradiente
        gradient = QRadialGradient(center_x, center_y, 400)
        gradient.setColorAt(0, QColor(0, 0, 0, 0))
        gradient.setColorAt(1, QColor(0, 255, 255, 80))
        painter.fillRect(0, 0, self.width(), self.height(), gradient)
        
        # Círculos de energia pulsantes
        for i in range(3):
            radius = 100 + i * 40
            self.draw_wave_circle(painter, center_x, center_y, radius)
        
        # Anéis de partículas
        for i in range(2):
            radius = 180 + i * 60
            self.draw_energy_ring(painter, center_x, center_y, radius, 32 + i * 16)
        
        # Ondas de voz
        if self.is_speaking:
            wave_points = 100
            wave_width = self.width() * 0.8
            wave_height = 50 * self.energy_level
            
            for i in range(wave_points):
                x = center_x - wave_width / 2 + i * (wave_width / wave_points)
                
                # Múltiplas ondas sobrepostas
                wave1 = wave_height * sin(self.wave_time * 2 + i * 0.2)
                wave2 = wave_height / 2 * sin(self.wave_time * 3 + i * 0.3)
                wave3 = wave_height / 3 * sin(self.wave_time * 5 + i * 0.5)
                
                y1 = center_y - 150 + wave1 + wave2 + wave3
                y2 = center_y + 150 + wave1 + wave2 + wave3
                
                if i > 0:
                    opacity = int(200 * exp(-abs(x - center_x) / (wave_width / 3)))
                    pen = QPen(QColor(180, 0, 255, opacity))
                    pen.setWidth(2)
                    painter.setPen(pen)
                    
                    painter.drawLine(QPointF(prev_x, prev_y1), QPointF(x, y1))
                    painter.drawLine(QPointF(prev_x, prev_y2), QPointF(x, y2))
                
                prev_x, prev_y1, prev_y2 = x, y1, y2
        
        # Texto Gysin-IA com efeito de brilho
        font = QFont("Arial", 40, QFont.Bold)
        painter.setFont(font)
        
        # Sombra do texto
        for i in range(10):
            opacity = int((10 - i) * 15 * (0.7 + 0.3 * sin(self.pulse)))
            pen = QPen(QColor(180, 0, 255, opacity))
            painter.setPen(pen)
            offset = i * 0.5
            painter.drawText(QRectF(center_x - 150, center_y - 25 - offset, 300, 50),
                           Qt.AlignCenter, "Gysin-IA")
        
        # Texto principal
        pen = QPen(QColor(255, 255, 255))
        painter.setPen(pen)
        painter.drawText(QRectF(center_x - 150, center_y - 25, 300, 50),
                        Qt.AlignCenter, "Gysin-IA")
        
        # Status do assistente
        status_text = "Ouvindo..." if self.is_listening else "Respondendo..."
        font.setPointSize(12)
        painter.setFont(font)
        painter.drawText(QRectF(center_x - 100, center_y + 30, 200, 30),
                        Qt.AlignCenter, status_text)

    def mousePressEvent(self, event):
        self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        delta = event.globalPosition().toPoint() - self.old_pos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.old_pos = event.globalPosition().toPoint()
    
    def set_listening(self, is_listening):
        self.is_listening = is_listening
        self.is_speaking = not is_listening
        self.energy_level = 0.3 if is_listening else 0.7

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AssistantWidget()
    window.show()
    sys.exit(app.exec_())
