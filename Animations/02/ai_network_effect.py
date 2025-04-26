import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QRadialGradient, QLinearGradient
from PySide6.QtCore import Qt, QTimer, QPointF, QRectF
from math import cos, sin, pi, exp, sqrt
import random
import string

class AINetworkEffect(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Network Effect")
        self.showFullScreen()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        # Nós da rede neural
        self.nodes = []
        self.connections = []
        self.thought_bubbles = []
        
        # Estados e animação
        self.time = 0
        self.pulse = 0
        self.is_thinking = False
        self.energy_flow = 0
        
        # Cores
        self.colors = [
            QColor(0, 255, 255),  # Ciano
            QColor(255, 0, 255),  # Magenta
            QColor(0, 255, 150),  # Verde neon
            QColor(150, 0, 255)   # Roxo
        ]
        
        # Inicializar rede
        self.initialize_network()
        
        # Timer para animação
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(30)
    
    def initialize_network(self):
        # Criar nós em uma estrutura de rede neural
        layers = [8, 12, 15, 12, 8]  # Estrutura da rede
        vertical_spacing = self.height() / (len(layers) + 1)
        
        for layer_idx, nodes_count in enumerate(layers):
            horizontal_spacing = self.width() / (nodes_count + 1)
            for node_idx in range(nodes_count):
                node = {
                    'x': horizontal_spacing * (node_idx + 1),
                    'y': vertical_spacing * (layer_idx + 1),
                    'size': random.uniform(5, 15),
                    'pulse': random.uniform(0, 2*pi),
                    'color_idx': random.randint(0, len(self.colors)-1),
                    'energy': random.uniform(0.5, 1.0)
                }
                self.nodes.append(node)
        
        # Criar conexões entre nós
        for i, node1 in enumerate(self.nodes):
            for node2 in self.nodes[i+1:]:
                if random.random() < 0.2:  # 20% de chance de conexão
                    self.connections.append({
                        'start': node1,
                        'end': node2,
                        'strength': random.uniform(0.1, 1.0),
                        'active': False,
                        'energy_particle': 0.0
                    })
    
    def create_thought_bubble(self):
        bubble = {
            'x': random.uniform(0, self.width()),
            'y': self.height(),
            'size': random.uniform(20, 40),
            'speed': random.uniform(2, 5),
            'text': random.choice([
                "Analyzing patterns...",
                "Processing data...",
                "Learning...",
                "Optimizing...",
                "Neural mapping...",
                "Generating response...",
                "Training model..."
            ]),
            'opacity': 255
        }
        self.thought_bubbles.append(bubble)
    
    def update_animation(self):
        self.time += 0.1
        self.pulse = (self.pulse + 0.05) % (2 * pi)
        self.energy_flow = (self.energy_flow + 0.02) % 1.0
        
        # Atualizar nós
        for node in self.nodes:
            node['pulse'] = (node['pulse'] + 0.05) % (2 * pi)
            if random.random() < 0.01:
                node['energy'] = random.uniform(0.5, 1.0)
        
        # Atualizar conexões
        for conn in self.connections:
            if random.random() < 0.05:
                conn['active'] = not conn['active']
            if conn['active']:
                conn['energy_particle'] = (conn['energy_particle'] + 0.05) % 1.0
        
        # Gerenciar bolhas de pensamento
        if random.random() < 0.02:
            self.create_thought_bubble()
        
        # Atualizar bolhas existentes
        self.thought_bubbles = [b for b in self.thought_bubbles if b['opacity'] > 0]
        for bubble in self.thought_bubbles:
            bubble['y'] -= bubble['speed']
            if bubble['y'] < self.height() / 2:
                bubble['opacity'] = max(0, bubble['opacity'] - 5)
        
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Desenhar conexões
        for conn in self.connections:
            start = conn['start']
            end = conn['end']
            
            # Gradiente para a linha
            if conn['active']:
                color = self.colors[start['color_idx']]
                color.setAlpha(100)
                pen = QPen(color)
                pen.setWidth(2)
                painter.setPen(pen)
                
                # Partícula de energia
                if conn['active']:
                    particle_x = start['x'] + (end['x'] - start['x']) * conn['energy_particle']
                    particle_y = start['y'] + (end['y'] - start['y']) * conn['energy_particle']
                    
                    radial = QRadialGradient(particle_x, particle_y, 10)
                    glow_color = self.colors[start['color_idx']]
                    radial.setColorAt(0, QColor(glow_color.red(), glow_color.green(), glow_color.blue(), 150))
                    radial.setColorAt(1, QColor(0, 0, 0, 0))
                    painter.setBrush(radial)
                    painter.setPen(Qt.NoPen)
                    painter.drawEllipse(QPointF(particle_x, particle_y), 10, 10)
            else:
                painter.setPen(QPen(QColor(100, 100, 100, 50)))
            
            painter.drawLine(start['x'], start['y'], end['x'], end['y'])
        
        # Desenhar nós
        for node in self.nodes:
            # Brilho do nó
            glow = abs(sin(node['pulse']))
            color = self.colors[node['color_idx']]
            radial = QRadialGradient(node['x'], node['y'], node['size'] * 2)
            radial.setColorAt(0, QColor(color.red(), color.green(), color.blue(), int(200 * glow)))
            radial.setColorAt(1, QColor(0, 0, 0, 0))
            painter.setBrush(radial)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(QPointF(node['x'], node['y']), node['size'] * 2, node['size'] * 2)
            
            # Núcleo do nó
            painter.setBrush(color)
            painter.drawEllipse(QPointF(node['x'], node['y']), node['size'], node['size'])
        
        # Desenhar bolhas de pensamento
        font = QFont("Arial", 10)
        painter.setFont(font)
        
        for bubble in self.thought_bubbles:
            color = self.colors[random.randint(0, len(self.colors)-1)]
            color.setAlpha(bubble['opacity'])
            painter.setPen(color)
            painter.drawText(QRectF(bubble['x']-50, bubble['y']-10, 100, 20),
                           Qt.AlignCenter, bubble['text'])
        
        # Interface central
        center_x = self.width() / 2
        center_y = self.height() / 2
        
        # Círculos concêntricos pulsantes
        for i in range(3):
            radius = 100 + sin(self.pulse + i * 0.5) * 10
            color = self.colors[i % len(self.colors)]
            pen = QPen(color)
            pen.setWidth(2)
            painter.setPen(pen)
            painter.drawEllipse(QPointF(center_x, center_y), radius + i * 20, radius + i * 20)
        
        # Logo central
        font = QFont("Arial", 40, QFont.Bold)
        painter.setFont(font)
        text = "NEURAL-AI"
        
        # Efeito de glitch no texto
        for i in range(3):
            offset_x = random.uniform(-2, 2) if random.random() < 0.1 else 0
            offset_y = random.uniform(-2, 2) if random.random() < 0.1 else 0
            color = self.colors[i % len(self.colors)]
            color.setAlpha(150)
            painter.setPen(color)
            painter.drawText(QRectF(center_x-200+offset_x, center_y-30+offset_y, 400, 60),
                           Qt.AlignCenter, text)
    
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
    
    def set_thinking(self, is_thinking):
        self.is_thinking = is_thinking

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AINetworkEffect()
    window.show()
    sys.exit(app.exec_()) 