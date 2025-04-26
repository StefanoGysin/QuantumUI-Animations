import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QRadialGradient, QPainterPath
from PySide6.QtCore import Qt, QTimer, QPointF, QRectF
from math import cos, sin, pi, exp, sqrt
import random

class CosmicNebula(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nebulosa Cósmica")
        self.resize(800, 600)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        # Estados da animação
        self.time = 0
        self.nebula_pulse = 0
        self.star_positions = self.generate_stars(100)  # 100 estrelas
        self.cosmic_particles = self.generate_particles(50)  # 50 partículas
        self.is_active = True
        
        # Timer para animação
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(16)  # 60 FPS
    
    def generate_stars(self, num_stars):
        stars = []
        for _ in range(num_stars):
            stars.append({
                'x': random.randint(0, self.width()),
                'y': random.randint(0, self.height()),
                'brightness': random.random(),
                'pulse_offset': random.uniform(0, 2 * pi)
            })
        return stars
    
    def generate_particles(self, num_particles):
        particles = []
        for _ in range(num_particles):
            particles.append({
                'x': self.width() / 2,
                'y': self.height() / 2,
                'angle': random.uniform(0, 2 * pi),
                'speed': random.uniform(0.5, 2),
                'size': random.uniform(2, 6),
                'color': random.choice(['purple', 'blue', 'pink'])
            })
        return particles
    
    def update_animation(self):
        self.time += 0.016  # Incremento baseado no FPS
        self.nebula_pulse = (self.nebula_pulse + 0.02) % (2 * pi)
        
        # Atualizar partículas cósmicas
        for particle in self.cosmic_particles:
            # Movimento em espiral
            radius = self.time * particle['speed'] * 20
            angle = particle['angle'] + self.time * particle['speed']
            
            particle['x'] = self.width()/2 + radius * cos(angle)
            particle['y'] = self.height()/2 + radius * sin(angle)
            
            # Reiniciar partícula quando sair da tela
            if radius > sqrt(self.width()**2 + self.height()**2):
                particle['x'] = self.width() / 2
                particle['y'] = self.height() / 2
                particle['angle'] = random.uniform(0, 2 * pi)
        
        self.update()
    
    def draw_nebula_cloud(self, painter, center_x, center_y):
        # Criar várias nuvens nebulosas sobrepostas
        for i in range(5):
            path = QPainterPath()
            radius = 200 + i * 30
            points = []
            
            # Gerar pontos para forma orgânica
            for angle in range(0, 360, 10):
                rad = angle * pi / 180
                r = radius + 50 * sin(self.nebula_pulse + i + rad * 2)
                x = center_x + r * cos(rad)
                y = center_y + r * sin(rad)
                points.append(QPointF(x, y))
            
            # Criar caminho suave
            path.moveTo(points[0])
            for j in range(len(points)):
                next_j = (j + 1) % len(points)
                path.quadTo(points[j], points[next_j])
            
            # Gradiente nebuloso
            gradient = QRadialGradient(center_x, center_y, radius)
            if i % 3 == 0:
                gradient.setColorAt(0, QColor(180, 100, 255, 30))
                gradient.setColorAt(1, QColor(100, 0, 150, 0))
            elif i % 3 == 1:
                gradient.setColorAt(0, QColor(100, 150, 255, 30))
                gradient.setColorAt(1, QColor(50, 0, 200, 0))
            else:
                gradient.setColorAt(0, QColor(255, 100, 200, 30))
                gradient.setColorAt(1, QColor(150, 0, 100, 0))
            
            painter.fillPath(path, gradient)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Fundo escuro do espaço
        painter.fillRect(0, 0, self.width(), self.height(), QColor(0, 0, 20, 255))
        
        # Desenhar estrelas
        for star in self.star_positions:
            brightness = abs(sin(self.time * 2 + star['pulse_offset'])) * star['brightness']
            color = QColor(255, 255, 255, int(100 + 155 * brightness))
            painter.setPen(color)
            painter.drawPoint(QPointF(star['x'], star['y']))
        
        # Centro da tela
        center_x = self.width() / 2
        center_y = self.height() / 2
        
        # Desenhar nebulosa
        self.draw_nebula_cloud(painter, center_x, center_y)
        
        # Desenhar partículas cósmicas
        for particle in self.cosmic_particles:
            if particle['color'] == 'purple':
                color = QColor(180, 100, 255, 150)
            elif particle['color'] == 'blue':
                color = QColor(100, 150, 255, 150)
            else:
                color = QColor(255, 100, 200, 150)
            
            painter.setPen(Qt.NoPen)
            painter.setBrush(color)
            size = particle['size'] * (1 + 0.3 * sin(self.nebula_pulse))
            painter.drawEllipse(QPointF(particle['x'], particle['y']), size, size)
        
        # Círculos concêntricos pulsantes
        for i in range(3):
            radius = 100 + i * 40 + 20 * sin(self.nebula_pulse + i)
            pen = QPen(QColor(180, 100, 255, 50 - i * 10))
            pen.setWidth(2)
            painter.setPen(pen)
            painter.drawEllipse(QPointF(center_x, center_y), radius, radius)
        
        # Texto Gysin-IA com efeito cósmico
        font = QFont("Arial", 40, QFont.Bold)
        painter.setFont(font)
        
        # Efeito de brilho estelar
        for i in range(10):
            opacity = int((10 - i) * 20 * (0.5 + 0.5 * sin(self.nebula_pulse)))
            offset = 3 * sin(self.nebula_pulse + i * 0.5)
            color = QColor(200, 150, 255, opacity)
            painter.setPen(color)
            painter.drawText(QRectF(center_x-150, center_y-25-offset, 300, 50),
                           Qt.AlignCenter, "Gysin-IA")
        
        # Texto principal
        painter.setPen(QColor(255, 255, 255))
        painter.drawText(QRectF(center_x-150, center_y-25, 300, 50),
                        Qt.AlignCenter, "Gysin-IA")
        
        # Status cósmico
        status = "EXPLORANDO O COSMOS..." if self.is_active else "NEBULOSA ESTÁVEL"
        font.setPointSize(12)
        painter.setFont(font)
        y_offset = 5 * sin(self.nebula_pulse * 2)
        painter.setPen(QColor(180, 100, 255, 200))
        painter.drawText(QRectF(center_x-200, center_y+40+y_offset, 400, 30),
                        Qt.AlignCenter, status)

    def mousePressEvent(self, event):
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
    window = CosmicNebula()
    window.show()
    sys.exit(app.exec_()) 