import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QRadialGradient, QPainterPath
from PySide6.QtCore import Qt, QTimer, QPointF, QRectF
from math import cos, sin, pi, exp

class AIInterfaceWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interface Neural")
        self.resize(800, 600)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        # Variáveis de animação
        self.wave_offset = 0
        self.pulse = 0
        self.neural_time = 0
        self.conversation_phase = 0
        
        # Frases da conversa
        self.messages = [
            "Iniciando Interface Neural...",
            "Conectando com Gysin-IA...",
            "Processando dados...",
            "Analisando padrões...",
            "Sistema Online"
        ]
        self.current_message = 0
        self.message_progress = 0
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(30)
    
    def update_animation(self):
        self.wave_offset = (self.wave_offset + 0.1) % (2 * pi)
        self.pulse = (self.pulse + 0.05) % (2 * pi)
        self.neural_time += 0.02
        
        # Atualizar texto da conversa
        self.message_progress += 0.02
        if self.message_progress >= 1:
            self.message_progress = 0
            self.current_message = (self.current_message + 1) % len(self.messages)
            
        self.conversation_phase = (self.conversation_phase + 0.03) % (2 * pi)
        self.update()
    
    def draw_neural_connection(self, painter, start, end, intensity):
        path = QPainterPath()
        path.moveTo(start)
        
        # Criar curva neural com variação no tempo
        ctrl1 = QPointF(
            (start.x() + end.x())/2 + 30 * sin(self.neural_time + intensity),
            (start.y() + end.y())/2 + 30 * cos(self.neural_time + intensity)
        )
        ctrl2 = QPointF(
            (start.x() + end.x())/2 - 30 * cos(self.neural_time + intensity),
            (start.y() + end.y())/2 - 30 * sin(self.neural_time + intensity)
        )
        
        path.cubicTo(ctrl1, ctrl2, end)
        
        # Gradiente para a linha neural
        pen = QPen(QColor(180, 0, 255, int(100 * intensity)))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawPath(path)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Fundo com gradiente
        gradient = QRadialGradient(self.width()/2, self.height()/2, 400)
        gradient.setColorAt(0, QColor(40, 0, 60, 30))
        gradient.setColorAt(1, QColor(0, 0, 0, 0))
        painter.fillRect(0, 0, self.width(), self.height(), gradient)
        
        # Círculo central da IA
        center_x = self.width() / 2
        center_y = self.height() / 2
        
        # Anel externo pulsante
        pulse_size = 150 + sin(self.pulse) * 10
        pen = QPen(QColor(180, 0, 255, 100))
        pen.setWidth(3)
        painter.setPen(pen)
        painter.drawEllipse(QPointF(center_x, center_y), pulse_size, pulse_size)
        
        # Ondas de áudio
        num_waves = 50
        wave_height = 40
        for i in range(num_waves):
            x = i * (self.width() / num_waves)
            wave1 = wave_height * sin(self.wave_offset + i * 0.2) * exp(-abs(x - center_x) / 300)
            wave2 = wave_height * cos(self.wave_offset * 1.5 + i * 0.1) * exp(-abs(x - center_x) / 300)
            
            y1 = center_y - 180 + wave1
            y2 = center_y + 180 + wave2
            
            opacity = int(150 * exp(-abs(x - center_x) / 300))
            pen = QPen(QColor(200, 100, 255, opacity))
            pen.setWidth(2)
            painter.setPen(pen)
            
            if i > 0:
                painter.drawLine(QPointF(prev_x, prev_y1), QPointF(x, y1))
                painter.drawLine(QPointF(prev_x, prev_y2), QPointF(x, y2))
            
            prev_x, prev_y1, prev_y2 = x, y1, y2
        
        # Conexões neurais
        num_points = 8
        points = []
        for i in range(num_points):
            angle = i * (2 * pi / num_points) + self.neural_time
            radius = 100 + 20 * sin(self.pulse + i)
            x = center_x + radius * cos(angle)
            y = center_y + radius * sin(angle)
            points.append(QPointF(x, y))
            
            # Desenhar nó neural
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(200, 100, 255, 150))
            painter.drawEllipse(QPointF(x, y), 5, 5)
        
        # Desenhar conexões
        for i in range(num_points):
            for j in range(i + 1, num_points):
                intensity = abs(sin(self.neural_time + i + j))
                if intensity > 0.3:  # Só mostrar conexões fortes
                    self.draw_neural_connection(painter, points[i], points[j], intensity)
        
        # Texto da conversa
        font = QFont("Arial", 12, QFont.Bold)
        painter.setFont(font)
        
        current_text = self.messages[self.current_message]
        text_width = len(current_text) * self.message_progress
        display_text = current_text[:int(text_width)]
        
        # Efeito de digitação
        text_y = self.height() - 100
        pen = QPen(QColor(255, 255, 255))
        painter.setPen(pen)
        painter.drawText(QRectF(50, text_y, self.width() - 100, 30),
                        Qt.AlignLeft | Qt.AlignVCenter,
                        display_text)
        
        # Cursor piscante
        if sin(self.conversation_phase * 5) > 0:
            painter.drawText(QRectF(50 + len(display_text) * 7, text_y, 10, 30),
                           Qt.AlignLeft | Qt.AlignVCenter, "_")
        
        # Logo Gysin-IA
        font = QFont("Arial", 35, QFont.Bold)
        painter.setFont(font)
        
        # Efeito de brilho no texto
        for i in range(10):
            opacity = (10 - i) * 15
            pen = QPen(QColor(180, 0, 255, opacity))
            painter.setPen(pen)
            offset = i * 0.5
            painter.drawText(QRectF(center_x - 150, center_y - 20 - offset, 300, 40),
                           Qt.AlignCenter, "Gysin-IA")
        
        # Texto principal
        pen = QPen(QColor(255, 255, 255))
        painter.setPen(pen)
        painter.drawText(QRectF(center_x - 150, center_y - 20, 300, 40),
                        Qt.AlignCenter, "Gysin-IA")

    def mousePressEvent(self, event):
        self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        delta = event.globalPosition().toPoint() - self.old_pos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.old_pos = event.globalPosition().toPoint()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AIInterfaceWidget()
    window.show()
    sys.exit(app.exec_()) 