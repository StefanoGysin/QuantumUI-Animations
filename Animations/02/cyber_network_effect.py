import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QRadialGradient
from PySide6.QtCore import Qt, QTimer, QPointF, QRectF
from math import cos, sin, pi, exp, sqrt
import random
import string

class CyberNetworkEffect(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cyber Network")
        self.showFullScreen()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        # Nós da rede
        self.nodes = []
        self.connections = []
        self.data_packets = []
        
        # Estados e animação
        self.time = 0
        self.pulse = 0
        self.is_listening = False
        
        # Inicializar rede
        self.initialize_network()
        
        # Timer para animação
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(30)  # 30ms para animação mais suave
    
    def initialize_network(self):
        # Criar nós da rede
        num_nodes = 30
        for _ in range(num_nodes):
            node = {
                'x': random.randint(100, self.width() - 100),
                'y': random.randint(100, self.height() - 100),
                'size': random.uniform(5, 15),
                'pulse': random.uniform(0, 2 * pi),
                'velocity_x': random.uniform(-0.5, 0.5),
                'velocity_y': random.uniform(-0.5, 0.5)
            }
            self.nodes.append(node)
        
        # Criar conexões entre nós próximos
        for i in range(len(self.nodes)):
            for j in range(i + 1, len(self.nodes)):
                if self.calculate_distance(self.nodes[i], self.nodes[j]) < 200:
                    self.connections.append((i, j))
    
    def calculate_distance(self, node1, node2):
        return sqrt((node1['x'] - node2['x'])**2 + (node1['y'] - node2['y'])**2)
    
    def create_data_packet(self):
        if len(self.connections) > 0 and random.random() < 0.1:
            connection = random.choice(self.connections)
            start_node = self.nodes[connection[0]]
            end_node = self.nodes[connection[1]]
            
            packet = {
                'x': start_node['x'],
                'y': start_node['y'],
                'target_x': end_node['x'],
                'target_y': end_node['y'],
                'progress': 0,
                'color': QColor(0, random.randint(150, 255), random.randint(150, 255), 200)
            }
            self.data_packets.append(packet)
    
    def update_animation(self):
        self.time += 0.1
        self.pulse = (self.pulse + 0.05) % (2 * pi)
        
        # Atualizar posição dos nós
        for node in self.nodes:
            node['x'] += node['velocity_x']
            node['y'] += node['velocity_y']
            node['pulse'] = (node['pulse'] + 0.1) % (2 * pi)
            
            # Inverter direção ao atingir bordas
            if node['x'] < 100 or node['x'] > self.width() - 100:
                node['velocity_x'] *= -1
            if node['y'] < 100 or node['y'] > self.height() - 100:
                node['velocity_y'] *= -1
        
        # Criar novos pacotes de dados
        self.create_data_packet()
        
        # Atualizar pacotes de dados
        for packet in self.data_packets[:]:
            packet['progress'] += 0.02
            if packet['progress'] >= 1:
                self.data_packets.remove(packet)
        
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Fundo escuro semi-transparente
        painter.fillRect(0, 0, self.width(), self.height(), QColor(0, 0, 20, 230))
        
        # Desenhar conexões
        for conn in self.connections:
            node1 = self.nodes[conn[0]]
            node2 = self.nodes[conn[1]]
            
            # Calcular opacidade baseada na distância
            distance = self.calculate_distance(node1, node2)
            opacity = int(255 * (1 - distance/300))
            if opacity > 0:
                pen = QPen(QColor(0, 150, 255, opacity))
                pen.setWidth(1)
                painter.setPen(pen)
                painter.drawLine(node1['x'], node1['y'], node2['x'], node2['y'])
        
        # Desenhar pacotes de dados
        for packet in self.data_packets:
            x = packet['x'] + (packet['target_x'] - packet['x']) * packet['progress']
            y = packet['y'] + (packet['target_y'] - packet['y']) * packet['progress']
            
            painter.setPen(Qt.NoPen)
            painter.setBrush(packet['color'])
            painter.drawEllipse(QPointF(x, y), 4, 4)
        
        # Desenhar nós
        for node in self.nodes:
            # Efeito de pulso
            glow = abs(sin(node['pulse']))
            size = node['size'] * (1 + 0.2 * glow)
            
            # Gradiente para cada nó
            gradient = QRadialGradient(node['x'], node['y'], size * 2)
            gradient.setColorAt(0, QColor(0, 200, 255, 150))
            gradient.setColorAt(1, QColor(0, 100, 255, 0))
            
            painter.setPen(Qt.NoPen)
            painter.setBrush(gradient)
            painter.drawEllipse(QPointF(node['x'], node['y']), size * 2, size * 2)
            
            painter.setBrush(QColor(0, 220, 255))
            painter.drawEllipse(QPointF(node['x'], node['y']), size, size)
        
        # Interface central
        center_x = self.width() / 2
        center_y = self.height() / 2
        
        # Círculos concêntricos pulsantes
        for i in range(3):
            radius = 150 + sin(self.pulse + i * 0.5) * 10
            gradient = QRadialGradient(center_x, center_y, radius)
            gradient.setColorAt(0, QColor(0, 150, 255, 30))
            gradient.setColorAt(1, QColor(0, 100, 255, 0))
            
            painter.setPen(Qt.NoPen)
            painter.setBrush(gradient)
            painter.drawEllipse(QPointF(center_x, center_y), radius, radius)
        
        # Texto Gysin-IA com efeito cyber
        font = QFont("Courier New", 40, QFont.Bold)
        painter.setFont(font)
        
        # Efeito de glitch digital
        for i in range(5):
            offset_x = random.uniform(-2, 2) if random.random() < 0.1 else 0
            offset_y = random.uniform(-2, 2) if random.random() < 0.1 else 0
            
            opacity = int(200 + 55 * sin(self.pulse + i))
            color = QColor(0, 200, 255, opacity)
            
            painter.setPen(color)
            painter.drawText(QRectF(center_x-150+offset_x, center_y-25+offset_y, 300, 50),
                           Qt.AlignCenter, "Gysin-IA")
        
        # Status com efeito cyber
        status = "NETWORK SCAN..." if self.is_listening else "ANALYZING DATA..."
        font.setPointSize(12)
        painter.setFont(font)
        
        for i, char in enumerate(status):
            x = center_x - len(status)*5 + i*10
            y = center_y + 50
            
            opacity = int(200 + 55 * sin(self.pulse + i * 0.3))
            color = QColor(0, 200, 255, opacity)
            
            painter.setPen(color)
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
    window = CyberNetworkEffect()
    window.show()
    sys.exit(app.exec_()) 