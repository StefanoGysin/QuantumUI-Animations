import sys
import math
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QRadialGradient, QPainterPath
from PySide6.QtCore import Qt, QTimer, QPointF, QRectF


class VariantAssistantWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Assistente Criativo")
        self.resize(800, 600)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Variáveis de animação
        self.angle = 0
        self.pulse = 0
        self.energy = 0.5
        self.hue = 0

        # Configurar timer para animação a aproximadamente 60 FPS
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(16)

    def update_animation(self):
        self.angle = (self.angle + 2) % 360
        self.pulse += 0.1
        self.energy = 0.5 + 0.3 * math.sin(self.pulse)
        self.hue = (self.hue + 1) % 360
        self.update()

    def draw_spinning_circles(self, painter, center_x, center_y):
        num_circles = 4
        for i in range(num_circles):
            radius = 50 + i * 40
            # Cor dinâmica baseada no hue e index
            color = QColor.fromHsl((self.hue + i * 30) % 360, 200, 150)
            gradient = QRadialGradient(center_x, center_y, radius)
            gradient.setColorAt(0, color.lighter(150))
            gradient.setColorAt(1, color.darker(150))
            painter.setBrush(gradient)
            painter.setPen(Qt.NoPen)
            # Deslocamento circular para efeito de vibração
            offset = 10 * math.sin(math.radians(self.angle + i * 40))
            painter.drawEllipse(QPointF(center_x + offset, center_y + offset), radius, radius)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        width = self.width()
        height = self.height()
        center_x = width / 2
        center_y = height / 2

        # Fundo dinâmico com gradiente radial
        bg_gradient = QRadialGradient(center_x, center_y, max(width, height) / 2)
        bg_color = QColor.fromHsl(self.hue, 150, 50, 150)
        bg_gradient.setColorAt(0, bg_color)
        bg_gradient.setColorAt(1, QColor(0, 0, 0, 0))
        painter.fillRect(0, 0, width, height, bg_gradient)

        # Desenhar círculos giratórios
        self.draw_spinning_circles(painter, center_x, center_y)

        # Desenhar texto central com efeito de brilho
        font = QFont("Arial", 32, QFont.Bold)
        painter.setFont(font)
        text = "Assistente Criativo"
        text_rect = QRectF(center_x - 200, center_y - 40, 400, 80)
        # Efeito de brilho através de múltiplas camadas de texto
        for i in range(8, 0, -1):
            glow_pen = QPen(QColor(255, 255, 255, max(20, 255 - i * 30)))
            glow_pen.setWidth(i)
            painter.setPen(glow_pen)
            painter.drawText(text_rect.translated(i * 0.5, i * 0.5), Qt.AlignCenter, text)
        # Texto principal
        painter.setPen(QPen(QColor(255, 255, 255)))
        painter.drawText(text_rect, Qt.AlignCenter, text)

        # Desenhar indicação de status usando energia dinâmica
        status = "Ativo" if self.energy > 0.7 else "Inativo"
        font_status = QFont("Arial", 14)
        painter.setFont(font_status)
        status_rect = QRectF(center_x - 50, center_y + 50, 100, 30)
        painter.setPen(QPen(QColor(200, 200, 200)))
        painter.drawText(status_rect, Qt.AlignCenter, status)

    def mousePressEvent(self, event):
        self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        delta = event.globalPosition().toPoint() - self.old_pos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.old_pos = event.globalPosition().toPoint()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VariantAssistantWidget()
    window.show()
    sys.exit(app.exec()) 