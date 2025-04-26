import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QRadialGradient, QLinearGradient, QPainterPath
from PySide6.QtCore import Qt, QTimer, QPointF, QRectF
from math import cos, sin, pi, sqrt, exp

class DarkCrystalAnimation(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cristal Sombrio")
        self.resize(800, 600)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        # Estados da animação
        self.angle = 0
        self.pulse = 0
        self.energy_flow = 0
        self.crystal_glow = 0
        self.darkness_intensity = 0
        self.eye_pulse = 0
        self.crystal_rotation = 0
        
        # Cores base
        self.crystal_color = QColor(150, 0, 0)
        self.glow_color = QColor(255, 0, 0)
        self.shadow_color = QColor(20, 0, 0)
        self.eye_color = QColor(255, 0, 0)
        
        # Timer para animação
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(16)  # ~60 FPS
    
    def update_animation(self):
        self.angle = (self.angle + 0.5) % 360
        self.pulse = (self.pulse + 0.05) % (2 * pi)
        self.energy_flow = (self.energy_flow + 1) % 100
        self.crystal_glow = abs(sin(self.pulse)) * 0.8
        self.darkness_intensity = (sin(self.pulse * 0.5) + 1) * 0.5
        self.eye_pulse = (self.eye_pulse + 0.03) % (2 * pi)
        self.crystal_rotation = (self.crystal_rotation - 0.02) % (2 * pi)
        self.update()
    
    def draw_eye(self, painter, center_x, center_y, scale):
        # Tamanho do olho
        eye_size = 40 * scale
        
        # Desenhar a íris
        iris_gradient = QRadialGradient(center_x, center_y, eye_size)
        iris_color = QColor(255, 0, 0)
        iris_color.setAlpha(int(200 + 55 * sin(self.eye_pulse)))
        iris_gradient.setColorAt(0, iris_color)
        iris_gradient.setColorAt(0.5, QColor(100, 0, 0))
        iris_gradient.setColorAt(1, QColor(50, 0, 0))
        
        painter.setBrush(iris_gradient)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QPointF(center_x, center_y), eye_size, eye_size)
        
        # Desenhar a pupila
        pupil_size = eye_size * 0.4
        pupil_gradient = QRadialGradient(center_x, center_y, pupil_size)
        pupil_gradient.setColorAt(0, QColor(0, 0, 0))
        pupil_gradient.setColorAt(1, QColor(20, 0, 0))
        
        painter.setBrush(pupil_gradient)
        painter.drawEllipse(QPointF(center_x, center_y), pupil_size, pupil_size)
        
        # Brilho do olho
        highlight_size = pupil_size * 0.3
        highlight_color = QColor(255, 255, 255, 150)
        painter.setBrush(highlight_color)
        painter.drawEllipse(
            QPointF(center_x - pupil_size * 0.3, center_y - pupil_size * 0.3),
            highlight_size, highlight_size
        )
    
    def draw_crystal(self, painter, center_x, center_y, scale):
        # Desenhar sombra do cristal
        shadow_path = QPainterPath()
        
        # Pontos do cristal com rotação
        points = []
        base_points = [
            (0, -200),
            (100, 0),
            (0, 200),
            (-100, 0)
        ]
        
        for x, y in base_points:
            rotated_x = x * cos(self.crystal_rotation) - y * sin(self.crystal_rotation)
            rotated_y = x * sin(self.crystal_rotation) + y * cos(self.crystal_rotation)
            points.append(QPointF(
                center_x + rotated_x * scale,
                center_y + rotated_y * scale
            ))
        
        shadow_path.moveTo(points[0])
        for point in points[1:]:
            shadow_path.lineTo(point)
        shadow_path.lineTo(points[0])
        
        # Efeito de brilho pulsante
        glow_gradient = QRadialGradient(center_x, center_y, 250 * scale)
        glow_color = self.glow_color
        glow_color.setAlpha(int(100 * self.crystal_glow))
        glow_gradient.setColorAt(0, glow_color)
        glow_color.setAlpha(0)
        glow_gradient.setColorAt(1, glow_color)
        
        painter.setBrush(glow_gradient)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QPointF(center_x, center_y), 250 * scale, 250 * scale)
        
        # Desenhar cristal principal
        crystal_gradient = QLinearGradient(
            points[3].x(), points[0].y(),
            points[1].x(), points[2].y()
        )
        
        base_color = self.crystal_color
        dark_color = self.shadow_color
        
        crystal_gradient.setColorAt(0, base_color)
        crystal_gradient.setColorAt(0.5, dark_color)
        crystal_gradient.setColorAt(1, base_color)
        
        painter.setBrush(crystal_gradient)
        painter.setPen(QPen(QColor(100, 0, 0), 2 * scale))
        painter.drawPath(shadow_path)
        
        # Desenhar o olho no centro
        self.draw_eye(painter, center_x, center_y, scale)
        
        # Efeitos de energia
        for i in range(12):
            angle = (self.angle + i * 30) * pi / 180
            energy_x = center_x + cos(angle) * 150 * scale
            energy_y = center_y + sin(angle) * 150 * scale
            
            energy_gradient = QRadialGradient(energy_x, energy_y, 20 * scale)
            energy_color = QColor(255, 0, 0, int(200 * abs(sin(self.pulse + i))))
            energy_gradient.setColorAt(0, energy_color)
            energy_color.setAlpha(0)
            energy_gradient.setColorAt(1, energy_color)
            
            painter.setBrush(energy_gradient)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(QPointF(energy_x, energy_y), 20 * scale, 20 * scale)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        scale = min(self.width(), self.height()) / 800
        center_x = self.width() / 2
        center_y = self.height() / 2
        
        # Desenhar o cristal principal
        self.draw_crystal(painter, center_x, center_y, scale)
        
        # Texto ameaçador
        font = QFont("Arial", int(20 * scale), QFont.Bold)
        painter.setFont(font)
        text_color = QColor(150, 0, 0, int(255 * self.darkness_intensity))
        painter.setPen(text_color)
        painter.drawText(QRectF(0, center_y + 250 * scale, self.width(), 40 * scale),
                        Qt.AlignCenter, "SISTEMA ATIVO")
    
    def mousePressEvent(self, event):
        self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        delta = event.globalPosition().toPoint() - self.old_pos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.old_pos = event.globalPosition().toPoint()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DarkCrystalAnimation()
    window.show()
    sys.exit(app.exec_()) 