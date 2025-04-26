import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QRadialGradient, QLinearGradient
from PySide6.QtCore import Qt, QTimer, QPointF, QRectF
from math import cos, sin, pi, sqrt

class JarvisWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gysin-IA")
        self.resize(600, 600)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        # Ângulos para diferentes animações
        self.angle = 0
        self.pulse_angle = 0
        self.text_opacity = 255
        self.pulse_size = 0
        
        # Configurar timer para animação
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(30)  # Mais rápido para animação mais suave
        
    def update_animation(self):
        self.angle = (self.angle + 3) % 360
        self.pulse_angle = (self.pulse_angle + 5) % 360
        self.pulse_size = 10 + sin(self.pulse_angle * pi / 180) * 5
        self.text_opacity = 155 + int(abs(sin(self.pulse_angle * pi / 180)) * 100)
        self.update()
        
    def draw_tech_circle(self, painter, radius, segments):
        for i in range(segments):
            angle = (i * 360 / segments + self.angle) * pi / 180
            next_angle = ((i + 1) * 360 / segments + self.angle) * pi / 180
            
            if i % 2 == 0:
                inner_radius = radius - 10
                outer_radius = radius
            else:
                inner_radius = radius - 5
                outer_radius = radius
                
            x1, y1 = cos(angle) * inner_radius, sin(angle) * inner_radius
            x2, y2 = cos(angle) * outer_radius, sin(angle) * outer_radius
            x3, y3 = cos(next_angle) * outer_radius, sin(next_angle) * outer_radius
            x4, y4 = cos(next_angle) * inner_radius, sin(next_angle) * inner_radius
            
            opacity = 100 + abs(sin(angle + self.pulse_angle * pi / 180)) * 155
            painter.setPen(QPen(QColor(0, 255, 255, int(opacity)), 1))
            painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))
            painter.drawLine(QPointF(x2, y2), QPointF(x3, y3))
            painter.drawLine(QPointF(x3, y3), QPointF(x4, y4))
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Centralizar na janela
        painter.translate(self.width() / 2, self.height() / 2)
        
        # Gradiente de fundo circular
        gradient = QRadialGradient(0, 0, 250)
        gradient.setColorAt(0, QColor(0, 0, 0, 0))
        gradient.setColorAt(1, QColor(0, 255, 255, 80))
        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QPointF(0, 0), 250, 250)
        
        # Círculos técnicos
        self.draw_tech_circle(painter, 200, 32)
        self.draw_tech_circle(painter, 180, 24)
        self.draw_tech_circle(painter, 160, 16)
        
        # Círculo externo pulsante
        pen = QPen(QColor(0, 200, 255, 100))
        pen.setWidth(self.pulse_size)
        painter.setPen(pen)
        painter.drawEllipse(QPointF(0, 0), 220, 220)
        
        # Arcos rotativos
        for i in range(4):
            opacity = 255 - i * 40
            width = 8 - i
            pen.setWidth(width)
            pen.setColor(QColor(0, 255, 255, opacity))
            painter.setPen(pen)
            start_angle = (self.angle + i * 30) * 16
            painter.drawArc(QRectF(-220, -220, 440, 440), start_angle, 45 * 16)
        
        # Linhas de dados
        for i in range(0, 360, 45):
            angle_rad = (i + self.angle / 2) * pi / 180
            length = 150 + sin(self.pulse_angle * pi / 180) * 20
            end_x = cos(angle_rad) * length
            end_y = sin(angle_rad) * length
            
            pen.setColor(QColor(0, 255, 255, 100))
            pen.setWidth(1)
            painter.setPen(pen)
            painter.drawLine(QPointF(0, 0), QPointF(end_x, end_y))
            
            # Pequenos círculos nas pontas
            painter.drawEllipse(QPointF(end_x, end_y), 3, 3)
        
        # Texto Gysin-IA com efeito futurista
        font = QFont("Arial", 30, QFont.Bold)
        painter.setFont(font)
        
        # Efeito de brilho dinâmico
        glow_radius = 15
        for i in range(glow_radius):
            opacity = (glow_radius - i) * 8
            y_offset = -sin(self.pulse_angle * pi / 180) * 3
            pen.setColor(QColor(0, 255, 255, opacity))
            painter.setPen(pen)
            painter.drawText(QRectF(-150, -20 + y_offset - i/2, 300, 40), 
                           Qt.AlignCenter, "Gysin-IA")
        
        # Texto principal com opacidade pulsante
        pen.setColor(QColor(255, 255, 255, self.text_opacity))
        painter.setPen(pen)
        painter.drawText(QRectF(-150, -20, 300, 40), Qt.AlignCenter, "Gysin-IA")
        
        # Pequenos detalhes técnicos
        detail_font = QFont("Arial", 8)
        painter.setFont(detail_font)
        for i in range(8):
            angle = (i * 45 + self.angle) * pi / 180
            x = cos(angle) * 240
            y = sin(angle) * 240
            text = f"SEC.{i:02d}"
            pen.setColor(QColor(0, 255, 255, 100))
            painter.setPen(pen)
            painter.drawText(QPointF(x-20, y), text)

    def mousePressEvent(self, event):
        self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        delta = event.globalPosition().toPoint() - self.old_pos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.old_pos = event.globalPosition().toPoint()

    def set_listening(self, is_listening):
        self.is_listening = is_listening

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = JarvisWidget()
    window.show()
    sys.exit(app.exec_())
