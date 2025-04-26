import sys
from math import cos, sin, pi, exp
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QRadialGradient, QPainterPath, QGuiApplication
from PySide6.QtCore import Qt, QTimer, QPointF, QRectF

class AssistantAIModule(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Assistente Virtual - Módulo AI Avançada")
        screen = QGuiApplication.primaryScreen()
        geom = screen.availableGeometry()
        self.resize(geom.width(), geom.height())
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        # Estados da animação
        self.is_listening = False
        self.is_speaking = True
        self.energy_level = 0.7
        
        # Variáveis de animação
        self.wave_time = 0
        self.ring_rotation = 0
        self.pulse = 0
        self.pulse_expansion = 0
        self.grid_offset = 0

        # Configurar timer para animação
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(16)  # Aproximadamente 60 FPS
    
    def update_animation(self):
        self.wave_time = (self.wave_time + 0.07) % (2 * pi)
        self.ring_rotation = (self.ring_rotation + 1.5) % 360
        self.pulse = (self.pulse + 0.04) % (2 * pi)
        self.pulse_expansion = (self.pulse_expansion + 2) % 300
        self.grid_offset = (self.grid_offset + 0.5) % 20
        
        self.update()
        
    def draw_digital_pulse(self, painter, center_x, center_y):
        # Desenha um pulso digital em expansão, simulando uma tecnologia avançada
        max_radius = 250
        current_radius = (self.pulse_expansion / 300) * max_radius
        opacity = max(0, 150 - (self.pulse_expansion / 300) * 150)
        painter.setPen(Qt.NoPen)
        gradient = QRadialGradient(center_x, center_y, current_radius)
        gradient.setColorAt(0, QColor(75, 0, 130, int(opacity)))
        gradient.setColorAt(1, QColor(75, 0, 130, 0))
        painter.setBrush(gradient)
        painter.drawEllipse(QPointF(center_x, center_y), current_radius, current_radius)
    
    def draw_network_ring(self, painter, center_x, center_y, radius, num_nodes):
        # Desenha um anel com nós interconectados, simulando uma rede neural
        nodes = []
        for i in range(num_nodes):
            angle = (i * 360 / num_nodes + self.ring_rotation) * pi / 180
            node_x = center_x + radius * cos(angle)
            node_y = center_y + radius * sin(angle)
            nodes.append((node_x, node_y))
            # Desenha o nó
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(75, 0, 130, 200))
            painter.drawEllipse(QPointF(node_x, node_y), 4, 4)
        
        # Conecta os nós com linhas estilizadas
        painter.setPen(QPen(QColor(75, 0, 130, 150), 2))
        for i in range(len(nodes)):
            next_index = (i + num_nodes // 2) % num_nodes
            painter.drawLine(QPointF(nodes[i][0], nodes[i][1]), QPointF(nodes[next_index][0], nodes[next_index][1]))
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        width = self.width()
        height = self.height()
        center_x = width / 2
        center_y = height / 2
        
        # Fundo removido
        
        # Desenhar o pulso digital central
        self.draw_digital_pulse(painter, center_x, center_y)
        
        # Desenhar anéis representando redes neurais
        for i in range(1, 4):
            radius = 80 + i * 40
            self.draw_network_ring(painter, center_x, center_y, radius, 24 + i * 4)
        
        # Desenhar ondas de voz futurísticas se o assistente estiver falando
        if self.is_speaking:
            wave_points = 120
            wave_width = width * 0.7
            wave_height = 40 * self.energy_level
            prev_x = center_x - wave_width / 2
            for i in range(wave_points):
                x = center_x - wave_width / 2 + i * (wave_width / wave_points)
                wave_offset = wave_height * sin(self.wave_time * 2 + i * 0.3)
                y_up = center_y - 120 + wave_offset
                y_down = center_y + 120 - wave_offset
                if i > 0:
                    pen = QPen(QColor(75, 0, 130, 180), 3)
                    painter.setPen(pen)
                    painter.drawLine(QPointF(prev_x, prev_y_up), QPointF(x, y_up))
                    painter.drawLine(QPointF(prev_x, prev_y_down), QPointF(x, y_down))
                prev_x = x
                prev_y_up = y_up
                prev_y_down = y_down
        
        # Texto com efeito futurístico
        font = QFont("Consolas", 36, QFont.Bold)
        painter.setFont(font)
        # Sombra do texto
        for i in range(8):
            opacity = max(0, 120 - i * 15)
            pen = QPen(QColor(75, 0, 130, opacity))
            painter.setPen(pen)
            offset = i * 1.5
            painter.drawText(QRectF(center_x - 150, center_y - 40 - offset, 300, 50),
                             Qt.AlignCenter, "Staley IA")
        # Texto principal
        painter.setPen(QColor(255, 255, 255))
        painter.drawText(QRectF(center_x - 150, center_y - 40, 300, 50),
                         Qt.AlignCenter, "Staley IA")
        
        # Exibição do status do assistente
        font.setPointSize(12)
        painter.setFont(font)
        status_text = "Ouvindo..." if self.is_listening else "Respondendo..."
        painter.drawText(QRectF(center_x - 100, center_y + 30, 200, 30),
                         Qt.AlignCenter, status_text)
    
    def mousePressEvent(self, event):
        self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        delta = event.globalPosition().toPoint() - self.old_pos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.old_pos = event.globalPosition().toPoint()
    
    def set_listening(self, listening):
        self.is_listening = listening
        self.is_speaking = not listening
        self.energy_level = 0.3 if listening else 0.8

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AssistantAIModule()
    window.show()
    sys.exit(app.exec_()) 