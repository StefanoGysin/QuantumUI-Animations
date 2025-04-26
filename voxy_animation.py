import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QRadialGradient, QPainterPath, QLinearGradient, QBrush
from PySide6.QtCore import Qt, QTimer, QPointF, QRectF, QEasingCurve
from math import cos, sin, pi, exp
import random

class GhostlyAssistantWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ghostly Assistant")
        self.resize(1000, 800)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        # Estados da animação
        self.is_listening = False
        self.is_speaking = True
        self.energy_level = 0.5
        self.ghost_opacity = 0  # Começa invisível
        self.fade_in = True
        
        # Variáveis de movimento fantasmagórico
        self.ghost_y_offset = 0
        self.ghost_scale = 0.8  # Começa menor
        self.appear_time = 0
        self.initial_appear = True  # Controla a animação inicial
        
        # Variáveis de animação
        self.wave_time = 0
        self.ring_rotation = 0
        self.pulse = 0
        self.particle_time = 0
        self.ghost_movement = 0
        self.ghost_particles = []
        self.generate_ghost_particles()
        
        # Easing curve para movimento fantasmagórico
        self.easing = QEasingCurve(QEasingCurve.InOutSine)
        
        # Configurar timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(16)  # 60 FPS
    
    def generate_ghost_particles(self):
        for _ in range(30):
            particle = {
                'x': random.uniform(0, self.width()),
                'y': random.uniform(0, self.height()),
                'size': random.uniform(5, 15),
                'speed': random.uniform(0.2, 1.0),
                'angle': random.uniform(0, 2*pi),
                'opacity': random.uniform(50, 150)
            }
            self.ghost_particles.append(particle)
    
    def update_animation(self):
        # Atualizar variáveis de animação
        self.wave_time = (self.wave_time + 0.1) % (2 * pi)
        self.ring_rotation = (self.ring_rotation + 1) % 360
        self.pulse = (self.pulse + 0.03) % (2 * pi)
        self.particle_time += 0.02
        self.ghost_movement = (self.ghost_movement + 0.02) % (2 * pi)
        self.appear_time += 0.02
        
        # Animação de aparecimento inicial
        if self.initial_appear:
            # Fade in mais suave
            self.ghost_opacity = min(255, self.ghost_opacity + 3)
            # Movimento de flutuação para cima
            self.ghost_y_offset = -30 * (1 - exp(-self.appear_time))
            # Crescimento suave
            self.ghost_scale = 0.8 + 0.2 * (1 - exp(-self.appear_time))
            
            if self.ghost_opacity >= 255:
                self.initial_appear = False
        else:
            # Fade in/out fantasmagórico normal
            if self.fade_in:
                self.ghost_opacity = min(255, self.ghost_opacity + 5)
                if self.ghost_opacity >= 255:
                    self.fade_in = False
            else:
                self.ghost_opacity = max(180, self.ghost_opacity - 3)
                if self.ghost_opacity <= 180:
                    self.fade_in = True
            
            # Movimento flutuante contínuo
            self.ghost_y_offset = -10 + 5 * sin(self.ghost_movement)
        
        self.update()
    
    def draw_ghost_effects(self, painter, center_x, center_y):
        # Aura fantasmagórica
        ghost_radius = 200 + 30 * sin(self.ghost_movement)
        ghost_gradient = QRadialGradient(center_x, center_y, ghost_radius)
        ghost_gradient.setColorAt(0, QColor(0, 255, 255, int(30 * (1 + sin(self.pulse)))))
        ghost_gradient.setColorAt(0.5, QColor(0, 255, 0, int(20 * (1 + sin(self.pulse)))))
        ghost_gradient.setColorAt(1, QColor(0, 0, 150, 0))
        
        painter.setBrush(ghost_gradient)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QPointF(center_x, center_y), ghost_radius, ghost_radius)
    
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
        gradient.setColorAt(0, QColor(0, 255, 255, 100))
        gradient.setColorAt(0.5, QColor(0, 255, 0, 100))
        gradient.setColorAt(1, QColor(0, 0, 150, 0))
        
        painter.setPen(QPen(QColor(0, 255, 255, 100), 2))
        painter.setBrush(gradient)
        painter.drawPath(path)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Centro da tela com offset fantasmagórico
        center_x = self.width() / 2
        center_y = self.height() / 2 + self.ghost_y_offset
        
        # Aplicar escala
        painter.translate(center_x, center_y)
        painter.scale(self.ghost_scale, self.ghost_scale)
        painter.translate(-center_x, -center_y)
        
        # Ajustar opacidade global
        painter.setOpacity(self.ghost_opacity / 255.0)
        
        # Fundo com gradiente fantasmagórico
        gradient = QRadialGradient(center_x, center_y, 500)
        gradient.setColorAt(0, QColor(20, 30, 50, int(20 * (1 + sin(self.ghost_movement)))))
        gradient.setColorAt(1, QColor(0, 0, 20, 0))
        painter.fillRect(0, 0, self.width(), self.height(), gradient)
        
        # Efeitos fantasmagóricos
        self.draw_ghost_effects(painter, center_x, center_y)
        
        # Círculos de energia fantasmagóricos
        for i in range(3):
            radius = 150 + i * 60 + 20 * sin(self.ghost_movement + i)
            self.draw_wave_circle(painter, center_x, center_y, radius)
        
        # Ondas de voz fantasmagóricas
        if self.is_speaking:
            wave_points = int(self.width() * 0.15)
            wave_width = min(self.width() * 0.9, 1200)
            wave_height = min(self.height() * 0.1, 100) * self.energy_level
            wave_thickness = max(self.width() * 0.003, 3)
            
            wave_vertical_offset = self.height() * 0.25
            
            for i in range(wave_points):
                x = center_x - wave_width/2 + i * (wave_width / wave_points)
                
                wave1 = wave_height * sin(self.wave_time * 2 + i * 0.2)
                wave2 = wave_height/1.5 * sin(self.wave_time * 3 + i * 0.3)
                wave3 = wave_height/2 * sin(self.wave_time * 5 + i * 0.5)
                
                y1 = center_y - wave_vertical_offset + wave1 + wave2 + wave3
                y2 = center_y + wave_vertical_offset + wave1 + wave2 + wave3
                
                if i > 0:
                    opacity = int(200 * exp(-abs(x - center_x)/(wave_width/3)))
                    
                    # Gradiente para as ondas com efeito fantasma
                    gradient = QLinearGradient(prev_x, prev_y1, x, y1)
                    gradient.setColorAt(0, QColor(0, 255, 255, opacity))
                    gradient.setColorAt(0.5, QColor(100, 200, 255, opacity))
                    gradient.setColorAt(1, QColor(0, 255, 0, opacity))
                    
                    pen = QPen(QBrush(gradient), wave_thickness)
                    pen.setCapStyle(Qt.RoundCap)
                    pen.setJoinStyle(Qt.RoundJoin)
                    painter.setPen(pen)
                    
                    painter.drawLine(QPointF(prev_x, prev_y1), QPointF(x, y1))
                    painter.drawLine(QPointF(prev_x, prev_y2), QPointF(x, y2))
                    
                    # Pontos de brilho nas intersecções com efeito fantasma
                    glow_size = wave_thickness * 1.5
                    painter.setPen(Qt.NoPen)
                    painter.setBrush(QColor(0, 255, 255, opacity))
                    painter.drawEllipse(QPointF(x, y1), glow_size/2, glow_size/2)
                    painter.drawEllipse(QPointF(x, y2), glow_size/2, glow_size/2)
                
                prev_x, prev_y1, prev_y2 = x, y1, y2
        
        self.update()

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
    window = GhostlyAssistantWidget()
    window.show()
    sys.exit(app.exec())