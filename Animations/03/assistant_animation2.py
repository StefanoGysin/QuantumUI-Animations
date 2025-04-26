import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QRadialGradient, QPainterPath, QLinearGradient, QBrush
from PySide6.QtCore import Qt, QTimer, QPointF, QRectF
from math import cos, sin, pi, exp
import random

class QuantumAssistantWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quantum Assistant")
        self.resize(1000, 800)
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
        self.quantum_particles = []
        self.generate_quantum_particles()
        
        # Configurar timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(16)  # 60 FPS para animação mais suave
    
    def generate_quantum_particles(self):
        for _ in range(50):
            particle = {
                'x': random.uniform(0, self.width()),
                'y': random.uniform(0, self.height()),
                'size': random.uniform(2, 6),
                'speed': random.uniform(0.5, 2),
                'angle': random.uniform(0, 2*pi)
            }
            self.quantum_particles.append(particle)
    
    def update_animation(self):
        # Atualizar variáveis de animação
        self.wave_time = (self.wave_time + 0.1) % (2 * pi)
        self.ring_rotation = (self.ring_rotation + 2) % 360
        self.pulse = (self.pulse + 0.05) % (2 * pi)
        self.particle_time += 0.02
        
        # Atualizar partículas quânticas
        for particle in self.quantum_particles:
            particle['x'] += cos(particle['angle']) * particle['speed']
            particle['y'] += sin(particle['angle']) * particle['speed']
            
            # Manter partículas dentro da tela
            if particle['x'] < 0 or particle['x'] > self.width():
                particle['angle'] = pi - particle['angle']
            if particle['y'] < 0 or particle['y'] > self.height():
                particle['angle'] = -particle['angle']
        
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
            painter.setBrush(QColor(0, 255, 255, opacity))
            painter.drawEllipse(QPointF(x, y), size, size)
            
            # Conectar com próxima partícula
            if i > 0:
                prev_angle = ((i-1) * 360 / num_particles + self.ring_rotation) * pi / 180
                prev_x = center_x + radius * cos(prev_angle)
                prev_y = center_y + radius * sin(prev_angle)
                
                # Linha de energia
                gradient = QLinearGradient(prev_x, prev_y, x, y)
                gradient.setColorAt(0, QColor(0, 255, 255, opacity))
                gradient.setColorAt(1, QColor(255, 0, 255, opacity))
                
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
        gradient.setColorAt(0, QColor(0, 255, 255, 100))
        gradient.setColorAt(0.5, QColor(255, 0, 255, 100))
        gradient.setColorAt(1, QColor(0, 0, 150, 0))
        
        painter.setPen(QPen(QColor(0, 255, 255, 100), 2))
        painter.setBrush(gradient)
        painter.drawPath(path)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Centro da tela
        center_x = self.width() / 2
        center_y = self.height() / 2
        
        # Fundo com gradiente
        gradient = QRadialGradient(center_x, center_y, 500)
        gradient.setColorAt(0, QColor(0, 20, 40, 30))
        gradient.setColorAt(1, QColor(0, 0, 0, 0))
        painter.fillRect(0, 0, self.width(), self.height(), gradient)
        
        # Partículas quânticas
        for particle in self.quantum_particles:
            opacity = int(100 + 100 * abs(sin(self.pulse + particle['x'] * 0.01)))
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(255, 255, 255, opacity))
            painter.drawEllipse(QPointF(particle['x'], particle['y']), particle['size'], particle['size'])
        
        # Círculos de energia pulsantes
        for i in range(3):
            radius = 150 + i * 60
            self.draw_wave_circle(painter, center_x, center_y, radius)
        
        # Anéis de partículas
        for i in range(2):
            radius = 250 + i * 80
            self.draw_energy_ring(painter, center_x, center_y, radius, 48 + i * 16)
        
        # Ondas de voz
        if self.is_speaking:
            # Ajuste automático baseado no tamanho da tela
            wave_points = int(self.width() * 0.15)  # Número de pontos proporcional à largura
            wave_width = min(self.width() * 0.9, 1200)  # Largura máxima de 1200px
            wave_height = min(self.height() * 0.1, 100) * self.energy_level  # Altura proporcional
            wave_thickness = max(self.width() * 0.003, 3)  # Espessura mínima de 3px
            
            # Calcular posição vertical baseada na altura da tela
            wave_vertical_offset = self.height() * 0.25
            
            for i in range(wave_points):
                x = center_x - wave_width/2 + i * (wave_width / wave_points)
                
                # Múltiplas ondas sobrepostas com amplitude ajustável
                wave1 = wave_height * sin(self.wave_time * 2 + i * 0.2)
                wave2 = wave_height/1.5 * sin(self.wave_time * 3 + i * 0.3)
                wave3 = wave_height/2 * sin(self.wave_time * 5 + i * 0.5)
                
                y1 = center_y - wave_vertical_offset + wave1 + wave2 + wave3
                y2 = center_y + wave_vertical_offset + wave1 + wave2 + wave3
                
                if i > 0:
                    opacity = int(200 * exp(-abs(x - center_x)/(wave_width/3)))
                    
                    # Gradiente mais vibrante para as ondas
                    gradient = QLinearGradient(prev_x, prev_y1, x, y1)
                    gradient.setColorAt(0, QColor(0, 255, 255, opacity))
                    gradient.setColorAt(0.5, QColor(100, 200, 255, opacity))
                    gradient.setColorAt(1, QColor(255, 0, 255, opacity))
                    
                    # Linha mais grossa com ponta arredondada
                    pen = QPen(QBrush(gradient), wave_thickness)
                    pen.setCapStyle(Qt.RoundCap)
                    pen.setJoinStyle(Qt.RoundJoin)
                    painter.setPen(pen)
                    
                    # Desenhar linhas com suavização
                    painter.drawLine(QPointF(prev_x, prev_y1), QPointF(x, y1))
                    painter.drawLine(QPointF(prev_x, prev_y2), QPointF(x, y2))
                    
                    # Adicionar pontos de brilho nas intersecções
                    glow_size = wave_thickness * 1.5
                    painter.setPen(Qt.NoPen)
                    painter.setBrush(QColor(255, 255, 255, opacity))
                    painter.drawEllipse(QPointF(x, y1), glow_size/2, glow_size/2)
                    painter.drawEllipse(QPointF(x, y2), glow_size/2, glow_size/2)
                
                prev_x, prev_y1, prev_y2 = x, y1, y2
        
        # Texto Staley IA com efeito futurista
        font = QFont("Arial", 60, QFont.Bold)
        painter.setFont(font)
        
        # Efeito de energia futurista
        for i in range(25):
            # Efeito de pulso dinâmico
            pulse_effect = sin(self.wave_time * 3 + i * 0.2)
            scale = 1 + 0.05 * pulse_effect
            opacity = int((25 - i) * 8 * (0.9 + 0.1 * sin(self.pulse * 3)))
            
            # Cores futuristas com variação dinâmica
            hue_shift = 30 * sin(self.wave_time + i * 0.1)
            
            # Gradiente com efeito de energia tecnológica
            gradient = QLinearGradient(center_x - 300, center_y, center_x + 300, center_y)
            gradient.setColorAt(0, QColor(0, 200 + 55 * sin(self.pulse + hue_shift), 255, opacity))
            gradient.setColorAt(0.3, QColor(0, 150, 255, opacity))
            gradient.setColorAt(0.5, QColor(255, 255, 255, opacity))
            gradient.setColorAt(0.7, QColor(100, 0, 255, opacity))
            gradient.setColorAt(1, QColor(200 + 55 * cos(self.pulse), 0, 255, opacity))
            
            pen = QPen()
            pen.setBrush(QBrush(gradient))
            painter.setPen(pen)
            
            # Efeito de deslocamento dinâmico
            offset_x = 10 * sin(self.wave_time * 2 + i * 0.3)
            offset_y = 5 * cos(self.wave_time * 3 + i * 0.2)
            
            # Desenho do texto com efeito de movimento
            rect = QRectF(
                center_x - 250 * scale + offset_x,
                center_y - 50 * scale - i * 0.8 + offset_y,
                500 * scale,
                100 * scale
            )
            painter.drawText(rect, Qt.AlignCenter, "Staley IA")
        
        # Efeito de brilho central
        glow_radius = 50 + 20 * sin(self.pulse * 2)
        glow_gradient = QRadialGradient(center_x, center_y - 20, glow_radius)
        glow_gradient.setColorAt(0, QColor(255, 255, 255, 180))
        glow_gradient.setColorAt(0.2, QColor(100, 200, 255, 150))
        glow_gradient.setColorAt(0.5, QColor(0, 100, 255, 100))
        glow_gradient.setColorAt(1, QColor(0, 0, 200, 0))
        
        painter.setBrush(glow_gradient)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QPointF(center_x, center_y - 20), glow_radius, glow_radius)
        
        # Texto principal com efeito de energia
        main_gradient = QLinearGradient(center_x - 200, center_y, center_x + 200, center_y)
        energy_pulse = sin(self.wave_time * 2)
        main_gradient.setColorAt(0, QColor(150 + 105 * energy_pulse, 200, 255, 255))
        main_gradient.setColorAt(0.5, QColor(255, 255, 255, 255))
        main_gradient.setColorAt(1, QColor(200, 100 + 155 * energy_pulse, 255, 255))
        
        pen = QPen()
        pen.setBrush(QBrush(main_gradient))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawText(QRectF(center_x - 250, center_y - 50, 500, 100),
                        Qt.AlignCenter, "Staley IA")
                        
        # Linhas de energia horizontais
        for i in range(5):
            y_offset = -20 + i * 10
            line_opacity = int(100 + 100 * sin(self.wave_time * 2 + i))
            line_gradient = QLinearGradient(center_x - 200, center_y, center_x + 200, center_y)
            line_gradient.setColorAt(0, QColor(0, 200, 255, 0))
            line_gradient.setColorAt(0.2, QColor(0, 200, 255, line_opacity))
            line_gradient.setColorAt(0.5, QColor(255, 255, 255, line_opacity))
            line_gradient.setColorAt(0.8, QColor(100, 0, 255, line_opacity))
            line_gradient.setColorAt(1, QColor(100, 0, 255, 0))
            
            pen = QPen(QBrush(line_gradient), 2)
            painter.setPen(pen)
            line_x = 50 * sin(self.wave_time + i)
            painter.drawLine(
                center_x - 150 - line_x, center_y + y_offset,
                center_x + 150 + line_x, center_y + y_offset
            )
        
        # Status do assistente
        status_text = "Analisando Dados Quânticos..." if self.is_listening else "Processando Realidade..."
        font.setPointSize(16)
        painter.setFont(font)
        painter.drawText(QRectF(center_x - 250, center_y + 60, 500, 40),
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
    window = QuantumAssistantWidget()
    window.show()
    sys.exit(app.exec())