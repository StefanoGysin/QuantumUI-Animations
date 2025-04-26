import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QRadialGradient, QLinearGradient
from PySide6.QtCore import Qt, QTimer, QPointF, QRectF
from math import cos, sin, pi

class VirtualAssistantAnimation(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Assistente Virtual - Animação")
        # Ajustar tamanho da janela dinamicamente com base na resolução do monitor
        app = QApplication.instance() or QApplication(sys.argv)
        screen = app.primaryScreen()
        screen_geometry = screen.availableGeometry()
        width = int(screen_geometry.width() * 0.6)
        height = int(screen_geometry.height() * 0.6)
        self.resize(width, height)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        # Variáveis de animação
        self.angle = 0       # Rotação para os nós
        self.pulse = 0       # Pulso para efeitos dinâmicos
        self.phase = 0       # Fase adicional para variações
        
        # Timer para atualizar a animação
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(30)
    
    def update_animation(self):
        self.angle = (self.angle + 2) % 360
        self.pulse = (self.pulse + 0.1) % (2 * pi)
        self.phase += 0.02
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Obter dimensões da janela
        width = self.width()
        height = self.height()
        center_x = width / 2
        center_y = height / 2
        
        # Não desenhar fundo para manter visual clean (fundo removido)
        
        # Desenhar nós da rede neural melhorados
        num_nos = 12
        base_radius = min(width, height) * 0.35
        nos = []
        for i in range(num_nos):
            angle_rad = (2 * pi / num_nos) * i + (self.angle * pi / 180)
            r_mod = base_radius + 12 * sin(self.pulse + i)  # amplitude ligeiramente menor
            x = center_x + r_mod * cos(angle_rad)
            y = center_y + r_mod * sin(angle_rad)
            nos.append((x, y))
            
            # Nó com gradiente suave
            node_gradient = QRadialGradient(x, y, 10)
            node_gradient.setColorAt(0, QColor(0, 210, 255, 240))
            node_gradient.setColorAt(1, QColor(0, 150, 230, 0))
            painter.setBrush(node_gradient)
            painter.setPen(Qt.NoPen)
            node_size = 6 + sin(self.pulse + i)  # variação sutil no tamanho
            painter.drawEllipse(QPointF(x, y), node_size, node_size)
        
        # Desenhar conexões entre os nós com linhas suaves
        connection_pen = QPen(QColor(0, 190, 255, 200))
        connection_pen.setWidth(1)
        painter.setPen(connection_pen)
        for i in range(num_nos):
            x1, y1 = nos[i]
            x2, y2 = nos[(i + 1) % num_nos]
            painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))
        
        # Elemento central pulsante, representando o núcleo da IA
        core_radius = 20 + 5 * sin(self.pulse * 2)
        core_gradient = QRadialGradient(center_x, center_y, core_radius)
        core_gradient.setColorAt(0, QColor(255, 255, 255, 250))
        core_gradient.setColorAt(1, QColor(180, 180, 180, 0))
        painter.setBrush(core_gradient)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QPointF(center_x, center_y), core_radius, core_radius)
        
        # Texto central com sombra sutil
        font = QFont("Helvetica", 24, QFont.Bold)
        painter.setFont(font)
        text = "Assistente Virtual"
        
        # Desenhando sombra
        shadow_offset = 2
        painter.setPen(QColor(0, 0, 0, 120))
        painter.drawText(QRectF(center_x - 200 + shadow_offset, center_y - 40 + shadow_offset, 400, 80), Qt.AlignCenter, text)
        
        # Desenhando o texto principal
        painter.setPen(QColor(0, 190, 255, 230))
        painter.drawText(QRectF(center_x - 200, center_y - 40, 400, 80), Qt.AlignCenter, text)
        
        # NOVOS ELEMENTOS: Efeitos tecnológicos e mais vivos
        
        # Anel de energia pulsante
        ring_radius = base_radius * 0.5 + (base_radius * 0.5) * abs(sin(self.pulse * 3))
        ring_pen = QPen(QColor(0, 255, 255, 150))
        ring_pen.setWidth(2)
        painter.setPen(ring_pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(QPointF(center_x, center_y), ring_radius, ring_radius)
        
        # Raios de energia radiantes
        num_beams = 8
        for i in range(num_beams):
            angle_beam = (2 * pi / num_beams) * i + self.phase
            beam_length = base_radius * 0.5 + (base_radius * 0.5) * abs(sin(self.phase * 2 + i))
            x_end = center_x + beam_length * cos(angle_beam)
            y_end = center_y + beam_length * sin(angle_beam)
            beam_pen = QPen(QColor(0, 255, 255, 180))
            beam_pen.setWidth(2)
            painter.setPen(beam_pen)
            painter.drawLine(QPointF(center_x, center_y), QPointF(x_end, y_end))
    
    def mousePressEvent(self, event):
        self.old_pos = event.globalPosition().toPoint()
    
    def mouseMoveEvent(self, event):
        delta = event.globalPosition().toPoint() - self.old_pos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.old_pos = event.globalPosition().toPoint()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VirtualAssistantAnimation()
    window.show()
    sys.exit(app.exec()) 