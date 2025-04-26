# Exemplos de Uso das Animações

Este documento contém exemplos práticos de como utilizar as animações do QuantumUI-Animations em diferentes contextos.

## Exemplo Básico

Aqui está um exemplo simples de como usar o componente de Assistente Fantasmagórico:

```python
import sys
from PySide6.QtWidgets import QApplication
from voxy_animation import GhostlyAssistantWidget

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Criar e exibir widget
    ghost = GhostlyAssistantWidget()
    ghost.show()
    
    # Alternar estados
    ghost.set_listening(True)  # Modo de escuta
    # ghost.set_listening(False)  # Modo de fala (padrão)
    
    sys.exit(app.exec())
```

## Integração com Reconhecimento de Voz

Exemplo de como integrar com uma biblioteca de reconhecimento de voz:

```python
import sys
import speech_recognition as sr
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QThread, Signal
from matrix_assistant import MatrixAssistant

class VoiceRecognitionThread(QThread):
    voice_detected = Signal(str)
    
    def run(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            while True:
                try:
                    audio = recognizer.listen(source, timeout=5)
                    text = recognizer.recognize_google(audio)
                    self.voice_detected.emit(text)
                except Exception as e:
                    print(f"Erro na captura de voz: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    matrix_ui = MatrixAssistant()
    matrix_ui.show()
    
    # Criar e iniciar thread de reconhecimento de voz
    voice_thread = VoiceRecognitionThread()
    voice_thread.voice_detected.connect(lambda text: matrix_ui.set_listening(False))
    voice_thread.start()
    
    sys.exit(app.exec())
```

## Uso em Dashboard

Exemplo de como usar uma animação como parte de um dashboard:

```python
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QWidget
from PySide6.QtCore import Qt
from dark_crystal_animation import CrystalWidget

class DashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard Futurístico")
        self.resize(1200, 800)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout(central_widget)
        
        # Seção de estatísticas (lado esquerdo)
        stats_widget = QWidget()
        stats_layout = QVBoxLayout(stats_widget)
        
        stats_title = QLabel("Estatísticas do Sistema")
        stats_title.setStyleSheet("font-size: 24px; color: #0CF;")
        stats_layout.addWidget(stats_title)
        
        # Adicionar mais estatísticas aqui
        for i in range(5):
            stat = QLabel(f"Estatística {i+1}: {random.randint(50, 99)}%")
            stat.setStyleSheet("font-size: 18px; color: #0FF;")
            stats_layout.addWidget(stat)
        
        stats_layout.addStretch()
        main_layout.addWidget(stats_widget, 2)
        
        # Seção de visualização (lado direito)
        crystal = CrystalWidget()
        main_layout.addWidget(crystal, 3)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DashboardWindow()
    window.show()
    sys.exit(app.exec())
```

## Customização de Cores

Exemplo de como customizar as cores de uma animação:

```python
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QColor
from biometric_scanner import BiometricScannerWidget

class CustomBiometricScanner(BiometricScannerWidget):
    def __init__(self):
        super().__init__()
        
        # Customizar cores
        self.primary_color = QColor(0, 150, 255)  # Azul
        self.secondary_color = QColor(0, 255, 150)  # Verde água
        self.background_color = QColor(10, 10, 30)  # Azul escuro
        
        # Você pode ajustar outras propriedades aqui
        self.scan_speed = 1.5  # Mais rápido
        self.particle_count = 50  # Mais partículas

if __name__ == "__main__":
    app = QApplication(sys.argv)
    scanner = CustomBiometricScanner()
    scanner.show()
    sys.exit(app.exec())
```

## Criando uma Animação Personalizada

Exemplo básico de como criar sua própria animação seguindo o padrão do projeto:

```python
import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QRadialGradient
from PySide6.QtCore import Qt, QTimer, QPointF
from math import cos, sin, pi

class MyCustomAnimation(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Minha Animação")
        self.resize(800, 600)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        # Variáveis de animação
        self.time = 0
        self.elements = []
        self.setup_elements()
        
        # Timer para animação
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(16)  # ~60 FPS
    
    def setup_elements(self):
        # Configurar elementos de animação
        pass
    
    def update_animation(self):
        self.time += 0.05
        # Atualizar elementos
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Desenhar animação
        
    def mousePressEvent(self, event):
        self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        delta = event.globalPosition().toPoint() - self.old_pos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.old_pos = event.globalPosition().toPoint()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyCustomAnimation()
    window.show()
    sys.exit(app.exec())
```

## Dicas de Desempenho

Para animações mais suaves:

1. Reduza a complexidade do desenho em telas menores
2. Use `QGraphicsView` para animações muito complexas
3. Considere pré-renderizar elementos estáticos
4. Ajuste o intervalo de timer baseado na capacidade do sistema 