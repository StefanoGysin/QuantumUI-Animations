import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QRadialGradient, QLinearGradient
from PySide6.QtCore import Qt, QTimer, QPointF, QRectF
from math import cos, sin, pi, sqrt

class IntenseAIAssistant(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Assistente Virtual IA - Intensa")
        self.resize(800, 600)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        # Estados da animação
        self.angle = 0
        self.pulse = 0
        self.data_flow = 0
        self.oscillation = [0.5 * sin(i) for i in range(20)]  # Para movimentar os nós
        
        # Timer para animação
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(30)
    
    def update_animation(self):
        self.angle = (self.angle + 1) % 360
        self.pulse = (self.pulse + 0.1) % (2 * pi)
        self.data_flow = (self.data_flow + 2) % 100
        
        # Atualizar oscilação
        for i in range(len(self.oscillation)):
            self.oscillation[i] = 0.5 * sin(self.pulse + i / 2)
        
        self.update()
    
    def draw_neural_network(self, painter, center_x, center_y, scale):
        layers = [4, 6, 6, 4]
        layer_distance = 150 * scale
        node_radius = 10 * scale
        
        for layer_idx, nodes in enumerate(layers):
            for node in range(nodes):
                x = center_x + (layer_idx - 1.5) * layer_distance
                y = center_y + (node - (nodes - 1) / 2) * 60 * scale + self.oscillation[node % len(self.oscillation)] * 10
                
                # Desenhar nó com pulso
                gradient = QRadialGradient(x, y, node_radius + sin(self.pulse * 2) * 3)
                gradient.setColorAt(0, QColor(255, 0, 100))
                gradient.setColorAt(1, QColor(100, 0, 255))
                painter.setBrush(gradient)
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(QPointF(x, y), node_radius, node_radius)
                
                # Desenhar conexões com brilho dinâmico
                if layer_idx < len(layers) - 1:
                    for next_node in range(layers[layer_idx + 1]):
                        next_x = center_x + (layer_idx - 0.5) * layer_distance
                        next_y = center_y + (next_node - (layers[layer_idx + 1] - 1) / 2) * 60 * scale + self.oscillation[next_node % len(self.oscillation)] * 10
                        
                        # Animação de fluxo de dados
                        flow_offset = (self.data_flow + layer_idx * 25 + node * 10 + next_node * 5) % 100
                        gradient = QLinearGradient(x, y, next_x, next_y)
                        gradient.setColorAt(0, QColor(150, 0, 255, 50))
                        gradient.setColorAt(flow_offset / 100, QColor(255, 0, 100, 200))
                        gradient.setColorAt(min(1, (flow_offset + 20) / 100), QColor(150, 0, 255, 50))
                        
                        pen = QPen(gradient, 2 * scale)
                        painter.setPen(pen)
                        painter.drawLine(QPointF(x, y), QPointF(next_x, next_y))
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Calcular escala baseada no tamanho da janela
        scale = min(self.width(), self.height()) / 800
        
        # Centro da tela
        center_x = self.width() / 2
        center_y = self.height() / 2
        
        # Desenhar rede neural
        self.draw_neural_network(painter, center_x, center_y, scale)
        
        # Círculo externo com segmentos
        radius = 250 * scale
        segments = 36
        for i in range(segments):
            angle = (i * 360 / segments + self.angle) * pi / 180
            next_angle = ((i + 1) * 360 / segments + self.angle) * pi / 180
            
            pen = QPen(QColor(255, 0, 100, 100))
            pen.setWidth(2 * scale)
            painter.setPen(pen)
            
            x1 = center_x + radius * cos(angle)
            y1 = center_y + radius * sin(angle)
            x2 = center_x + radius * cos(next_angle)
            y2 = center_y + radius * sin(next_angle)
            
            if i % 2 == 0:
                painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))
        
        # Texto central com brilho intenso
        font = QFont("Arial", int(30 * scale), QFont.Bold)
        painter.setFont(font)
        for i in range(5):
            brightness = (5 - i) * 50
            painter.setPen(QColor(255, 0, 100, brightness))
            painter.drawText(QRectF(center_x-150*scale, center_y-40*scale, 300*scale, 40*scale),
                             Qt.AlignCenter, "AI Assistant")
        
        # Status da IA
        font.setPointSize(int(12 * scale))
        painter.setFont(font)
        painter.setPen(QColor(255, 0, 100, 200))
        painter.drawText(QRectF(center_x-150*scale, center_y+50*scale, 300*scale, 30*scale),
                         Qt.AlignCenter, "PROCESSING DATA...")

    def mousePressEvent(self, event):
        self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        delta = event.globalPosition().toPoint() - self.old_pos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.old_pos = event.globalPosition().toPoint()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = IntenseAIAssistant()
    window.show()
    sys.exit(app.exec_())