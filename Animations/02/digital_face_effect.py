import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QRadialGradient
from PySide6.QtCore import Qt, QTimer, QPointF, QRectF
from math import cos, sin, pi, sqrt, atan2
import random

class DigitalFaceWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Digital Face")
        self.resize(600, 600)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        # Estados da animação
        self.angle = 0
        self.pulse_angle = 0
        self.text_opacity = 255
        self.pulse_size = 0
        self.mouse_x = self.width() / 2
        self.mouse_y = self.height() / 2
        self.eye_target_x = 0
        self.eye_target_y = 0
        self.left_eye_x = -50
        self.right_eye_x = 50
        self.eye_y = 0
        self.blink_timer = 0
        self.is_blinking = False
        
        # Configurar timer para animação
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(30)
        
    def update_animation(self):
        self.angle = (self.angle + 2) % 360
        self.pulse_angle = (self.pulse_angle + 3) % 360
        self.pulse_size = 10 + sin(self.pulse_angle * pi / 180) * 5
        self.text_opacity = 155 + int(abs(sin(self.pulse_angle * pi / 180)) * 100)
        
        # Atualizar posição dos olhos suavemente
        center_x = self.width() / 2
        center_y = self.height() / 2
        
        # Calcular ângulo para os olhos
        dx = self.mouse_x - center_x
        dy = self.mouse_y - center_y
        angle = atan2(dy, dx)
        
        # Limitar movimento dos olhos
        max_eye_move = 15
        self.eye_target_x = cos(angle) * max_eye_move
        self.eye_target_y = sin(angle) * max_eye_move
        
        # Suavizar movimento
        self.left_eye_x = -50 + self.eye_target_x
        self.right_eye_x = 50 + self.eye_target_x
        self.eye_y = self.eye_target_y
        
        # Gerenciar piscada
        if not self.is_blinking:
            if random.random() < 0.01:  # 1% de chance de piscar
                self.is_blinking = True
                self.blink_timer = 0
        else:
            self.blink_timer += 1
            if self.blink_timer > 10:  # Duração da piscada
                self.is_blinking = False
        
        self.update()
        
    def draw_tech_circle(self, painter, radius, segments):
        for i in range(segments):
            angle = (i * 360 / segments + self.angle) * pi / 180
            next_angle = ((i + 1) * 360 / segments + self.angle) * pi / 180
            
            inner_radius = radius - 5 if i % 2 == 0 else radius - 2
            
            x1, y1 = cos(angle) * inner_radius, sin(angle) * inner_radius
            x2, y2 = cos(angle) * radius, sin(angle) * radius
            x3, y3 = cos(next_angle) * radius, sin(next_angle) * radius
            x4, y4 = cos(next_angle) * inner_radius, sin(next_angle) * inner_radius
            
            opacity = 100 + abs(sin(angle + self.pulse_angle * pi / 180)) * 155
            painter.setPen(QPen(QColor(0, 255, 255, int(opacity)), 1))
            painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))
            painter.drawLine(QPointF(x2, y2), QPointF(x3, y3))
            painter.drawLine(QPointF(x3, y3), QPointF(x4, y4))
    
    def draw_eye(self, painter, x, y):
        # Contorno do olho
        painter.setPen(QPen(QColor(0, 255, 255, 200), 2))
        painter.drawEllipse(QPointF(x, y), 30, 25)
        
        # Íris com efeito de brilho
        if not self.is_blinking:
            gradient = QRadialGradient(x + self.eye_target_x/2, y + self.eye_target_y/2, 15)
            gradient.setColorAt(0, QColor(0, 255, 255, 255))
            gradient.setColorAt(0.5, QColor(0, 150, 255, 200))
            gradient.setColorAt(1, QColor(0, 50, 255, 150))
            painter.setBrush(gradient)
            painter.drawEllipse(QPointF(x + self.eye_target_x/2, y + self.eye_target_y/2), 15, 15)
            
            # Pupila
            painter.setBrush(QColor(0, 0, 0, 255))
            painter.drawEllipse(QPointF(x + self.eye_target_x/2, y + self.eye_target_y/2), 5, 5)
            
            # Reflexo
            painter.setBrush(QColor(255, 255, 255, 200))
            painter.drawEllipse(QPointF(x + self.eye_target_x/2 - 3, y + self.eye_target_y/2 - 3), 2, 2)
        else:
            # Olho piscando
            painter.drawLine(QPointF(x - 30, y), QPointF(x + 30, y))
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Centralizar na janela
        painter.translate(self.width() / 2, self.height() / 2)
        
        # Círculos técnicos externos
        self.draw_tech_circle(painter, 200, 32)
        self.draw_tech_circle(painter, 180, 24)
        
        # Rosto base
        gradient = QRadialGradient(0, 0, 150)
        gradient.setColorAt(0, QColor(0, 50, 100, 30))
        gradient.setColorAt(1, QColor(0, 0, 0, 0))
        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QPointF(0, 0), 150, 150)
        
        # Desenhar olhos
        self.draw_eye(painter, self.left_eye_x, self.eye_y)
        self.draw_eye(painter, self.right_eye_x, self.eye_y)
        
        # Linhas de circuito no rosto
        for i in range(0, 360, 45):
            angle_rad = (i + self.angle / 2) * pi / 180
            length = 120 + sin(self.pulse_angle * pi / 180) * 10
            end_x = cos(angle_rad) * length
            end_y = sin(angle_rad) * length
            
            painter.setPen(QPen(QColor(0, 255, 255, 100), 1))
            painter.drawLine(QPointF(0, 0), QPointF(end_x, end_y))
            painter.drawEllipse(QPointF(end_x, end_y), 3, 3)
        
        # Boca digital
        mouth_y = 50
        mouth_width = 80 + sin(self.pulse_angle * pi / 180) * 10
        painter.setPen(QPen(QColor(0, 255, 255, 200), 2))
        points = []
        for i in range(10):
            x = -mouth_width/2 + (mouth_width * i / 9)
            y = mouth_y + sin(i * pi / 2 + self.pulse_angle * pi / 180) * 5
            points.append(QPointF(x, y))
        
        for i in range(len(points)-1):
            painter.drawLine(points[i], points[i+1])
        
        # Detalhes técnicos
        detail_font = QFont("Arial", 8)
        painter.setFont(detail_font)
        for i in range(8):
            angle = (i * 45 + self.angle) * pi / 180
            x = cos(angle) * 220
            y = sin(angle) * 220
            text = f"SYS.{i:02d}"
            painter.setPen(QColor(0, 255, 255, 100))
            painter.drawText(QPointF(x-20, y), text)
    
    def mouseMoveEvent(self, event):
        self.mouse_x = event.position().x()
        self.mouse_y = event.position().y()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.close()
        self.old_pos = event.globalPosition().toPoint()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DigitalFaceWidget()
    window.show()
    sys.exit(app.exec_()) 