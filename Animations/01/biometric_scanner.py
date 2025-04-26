import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QRadialGradient, QLinearGradient
from PySide6.QtCore import Qt, QTimer, QPointF, QRectF
from math import cos, sin, pi, sqrt

class BiometricScanner(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scanner Biométrico")
        self.resize(600, 600)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        # Estados da animação
        self.angle = 0
        self.scan_line = 0
        self.pulse = 0
        self.scan_active = True
        
        # Timer para animação
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(30)
    
    def update_animation(self):
        self.angle = (self.angle + 2) % 360
        self.pulse = (self.pulse + 0.1) % (2 * pi)
        
        # Movimento da linha de escaneamento
        if self.scan_active:
            self.scan_line = (self.scan_line + 3) % 200
        
        self.update()
    
    def draw_fingerprint(self, painter, center_x, center_y):
        # Desenhar padrões de impressão digital
        for i in range(8):
            radius = 50 + i * 15
            pen = QPen(QColor(0, 255, 200, 100 - i * 10))
            pen.setWidth(2)
            painter.setPen(pen)
            
            for j in range(0, 360, 20):
                angle = (j + self.angle + i * 10) * pi / 180
                next_angle = (j + 20 + self.angle + i * 10) * pi / 180
                
                x1 = center_x + radius * cos(angle)
                y1 = center_y + radius * sin(angle)
                x2 = center_x + radius * cos(next_angle)
                y2 = center_y + radius * sin(next_angle)
                
                # Adicionar ondulação
                wave = sin(angle * 3 + self.pulse) * 5
                y1 += wave
                y2 += wave
                
                painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Centro da tela
        center_x = self.width() / 2
        center_y = self.height() / 2
        
        # Gradiente de fundo
        gradient = QRadialGradient(center_x, center_y, 300)
        gradient.setColorAt(0, QColor(0, 40, 30, 30))
        gradient.setColorAt(1, QColor(0, 0, 0, 0))
        painter.fillRect(0, 0, self.width(), self.height(), gradient)
        
        # Círculo externo com segmentos
        radius = 200
        segments = 36
        for i in range(segments):
            angle = (i * 360 / segments + self.angle) * pi / 180
            next_angle = ((i + 1) * 360 / segments + self.angle) * pi / 180
            
            pen = QPen(QColor(0, 255, 200, 100))
            pen.setWidth(2)
            painter.setPen(pen)
            
            x1 = center_x + radius * cos(angle)
            y1 = center_y + radius * sin(angle)
            x2 = center_x + radius * cos(next_angle)
            y2 = center_y + radius * sin(next_angle)
            
            if i % 2 == 0:
                painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))
        
        # Desenhar impressão digital
        self.draw_fingerprint(painter, center_x, center_y)
        
        # Linha de escaneamento
        if self.scan_active:
            scan_gradient = QLinearGradient(0, center_y - 100 + self.scan_line,
                                          0, center_y - 98 + self.scan_line)
            scan_gradient.setColorAt(0, QColor(0, 255, 200, 0))
            scan_gradient.setColorAt(0.5, QColor(0, 255, 200, 150))
            scan_gradient.setColorAt(1, QColor(0, 255, 200, 0))
            
            painter.fillRect(QRectF(center_x - 150, center_y - 100 + self.scan_line,
                                  300, 2), scan_gradient)
        
        # Círculos de dados
        for i in range(8):
            angle = (self.angle + i * 45) * pi / 180
            radius = 150 + sin(self.pulse + i) * 10
            x = center_x + radius * cos(angle)
            y = center_y + radius * sin(angle)
            
            # Círculo de dados
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(0, 255, 200, 150))
            size = 5 + sin(self.pulse + i) * 2
            painter.drawEllipse(QPointF(x, y), size, size)
            
            # Texto de dados
            font = QFont("Courier New", 8)
            painter.setFont(font)
            painter.setPen(QColor(0, 255, 200, 150))
            text = f"BIO_{i:02X}"
            painter.drawText(QPointF(x + 10, y), text)
        
        # Texto central com efeito de escaneamento
        font = QFont("Arial", 30, QFont.Bold)
        painter.setFont(font)
        
        # Efeito de brilho
        for i in range(10):
            opacity = (10 - i) * 15
            y_offset = sin(self.pulse) * 3
            color = QColor(0, 255, 200, opacity)
            painter.setPen(color)
            painter.drawText(QRectF(center_x-150, center_y-20+y_offset-i/2, 300, 40),
                           Qt.AlignCenter, "Gysin-IA")
        
        # Status do escaneamento
        font.setPointSize(12)
        painter.setFont(font)
        status = "SCANNING BIOMETRICS..." if self.scan_active else "SCAN COMPLETE"
        painter.setPen(QColor(0, 255, 200, 200))
        painter.drawText(QRectF(center_x-150, center_y+50, 300, 30),
                        Qt.AlignCenter, status)

    def mousePressEvent(self, event):
        self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        delta = event.globalPosition().toPoint() - self.old_pos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.old_pos = event.globalPosition().toPoint()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BiometricScanner()
    window.show()
    sys.exit(app.exec_()) 