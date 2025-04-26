import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QRadialGradient, QPainterPath, QLinearGradient
from PySide6.QtCore import Qt, QTimer, QPointF, QRectF
from math import cos, sin, pi, exp, sqrt, atan2

class CrystalWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cristal Sombrio")
        self.resize(800, 600)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        # Estados da animação
        self.energy_level = 0.5
        self.crystal_rotation = 0
        self.inner_pulse = 0
        self.darkness_level = 0
        
        # Variáveis de animação
        self.time = 0
        self.particle_time = 0
        self.shadow_intensity = 0
        self.crystal_vertices = self.generate_crystal_vertices()
        self.energy_particles = []
        
        # Configurar timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(16)

    def generate_crystal_vertices(self):
        # Gera vértices para um cristal mais complexo e assimétrico
        vertices = []
        num_points = 8
        for i in range(num_points):
            angle = (i * 2 * pi / num_points)
            radius = 100 + 20 * sin(i * 1.5)
            x = radius * cos(angle)
            y = radius * sin(angle)
            vertices.append(QPointF(x, y))
        return vertices

    def update_animation(self):
        self.time += 0.05
        self.crystal_rotation += 0.01
        self.inner_pulse = (self.inner_pulse + 0.03) % (2 * pi)
        self.particle_time += 0.02
        self.darkness_level = 0.5 + 0.3 * sin(self.time)
        self.shadow_intensity = 0.7 + 0.3 * sin(self.time * 0.5)
        self.update()

    def draw_crystal(self, painter, center_x, center_y):
        # Desenha o cristal principal com gradiente vermelho sangue
        crystal_path = QPainterPath()
        
        # Transformação dos vértices
        transformed_vertices = []
        for vertex in self.crystal_vertices:
            x = vertex.x() * cos(self.crystal_rotation) - vertex.y() * sin(self.crystal_rotation)
            y = vertex.x() * sin(self.crystal_rotation) + vertex.y() * cos(self.crystal_rotation)
            transformed_vertices.append(QPointF(center_x + x, center_y + y))

        # Criar caminho do cristal
        crystal_path.moveTo(transformed_vertices[0])
        for vertex in transformed_vertices[1:]:
            crystal_path.lineTo(vertex)
        crystal_path.lineTo(transformed_vertices[0])

        # Gradiente principal do cristal
        gradient = QLinearGradient(center_x - 100, center_y - 100, center_x + 100, center_y + 100)
        gradient.setColorAt(0, QColor(180, 0, 0, 255))
        gradient.setColorAt(0.5, QColor(120, 0, 0, 200))
        gradient.setColorAt(1, QColor(80, 0, 0, 255))

        # Desenhar sombra
        shadow_path = QPainterPath(crystal_path)
        shadow_offset = 10
        shadow_path.translate(shadow_offset, shadow_offset)
        painter.fillPath(shadow_path, QColor(0, 0, 0, 100))

        # Desenhar cristal
        painter.fillPath(crystal_path, gradient)

        # Efeito de brilho interno
        inner_gradient = QRadialGradient(center_x, center_y, 150)
        inner_color = QColor(255, 0, 0, int(100 + 50 * sin(self.inner_pulse)))
        inner_gradient.setColorAt(0, inner_color)
        inner_gradient.setColorAt(1, QColor(100, 0, 0, 0))
        painter.fillPath(crystal_path, inner_gradient)

    def draw_energy_particles(self, painter, center_x, center_y):
        # Partículas de energia flutuando ao redor do cristal
        num_particles = 50
        for i in range(num_particles):
            angle = self.time * 2 + i * (2 * pi / num_particles)
            radius = 150 + 30 * sin(self.time * 3 + i)
            x = center_x + radius * cos(angle)
            y = center_y + radius * sin(angle)
            
            size = 3 + 2 * sin(self.time + i)
            opacity = int(200 * (0.5 + 0.5 * sin(self.time * 2 + i)))
            
            particle_gradient = QRadialGradient(x, y, size * 2)
            particle_gradient.setColorAt(0, QColor(255, 0, 0, opacity))
            particle_gradient.setColorAt(1, QColor(100, 0, 0, 0))
            
            painter.setBrush(particle_gradient)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(QPointF(x, y), size, size)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Centro da tela
        center_x = self.width() / 2
        center_y = self.height() / 2
        
        # Fundo escuro com névoa
        background_gradient = QRadialGradient(center_x, center_y, 400)
        background_gradient.setColorAt(0, QColor(20, 0, 0, 200))
        background_gradient.setColorAt(1, QColor(0, 0, 0, 255))
        painter.fillRect(0, 0, self.width(), self.height(), background_gradient)
        
        # Desenhar aura sombria
        for i in range(3):
            radius = 200 + i * 30
            aura_gradient = QRadialGradient(center_x, center_y, radius)
            opacity = int(100 * (1 - i/3) * self.shadow_intensity)
            aura_gradient.setColorAt(0, QColor(100, 0, 0, opacity))
            aura_gradient.setColorAt(1, QColor(0, 0, 0, 0))
            painter.fillRect(0, 0, self.width(), self.height(), aura_gradient)
        
        # Desenhar cristal principal
        self.draw_crystal(painter, center_x, center_y)
        
        # Desenhar partículas de energia
        self.draw_energy_particles(painter, center_x, center_y)

    def mousePressEvent(self, event):
        self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        delta = event.globalPosition().toPoint() - self.old_pos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.old_pos = event.globalPosition().toPoint()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CrystalWidget()
    window.show()
    sys.exit(app.exec_())
