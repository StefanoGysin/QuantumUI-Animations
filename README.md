# 🌌 QuantumUI-Animations

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![PySide6](https://img.shields.io/badge/PySide6-6.6.1-green)

<p align="center">
  <img src="docs/images/preview.gif" alt="QuantumUI Preview" width="650" />
  <br>
  <i>Uma coleção de interfaces de usuário futurísticas e animações visuais avançadas</i>
</p>

## 🚀 Visão Geral

QuantumUI-Animations é uma biblioteca de componentes visuais e animações para criar interfaces de usuário futurísticas e imersivas. Inspirada em filmes de ficção científica e interfaces holográficas, esta coleção oferece elementos visuais dinâmicos que podem ser integrados em aplicações desktop ou utilizados como inspiração para projetos de design de interface.

## ✨ Características

- **Animações Fluidas**: Movimento suave e orgânico para uma experiência visual cativante
- **Efeitos Visuais Avançados**: Gradientes, partículas, ondas e efeitos de iluminação
- **Interfaces Temáticas**: Várias opções estéticas (Matrix, Cristal, Fantasma, Biométrica)
- **Customizável**: Adaptável para diferentes tamanhos de tela e estilos visuais
- **Leve**: Otimizado para desempenho mesmo com efeitos visuais complexos
- **Cross-Platform**: Funciona em Windows, macOS e Linux

## 📋 Estilos Disponíveis

- **🌐 Assistente Fantasmagórico**: Interface etérea com ondas e partículas luminosas
- **💎 Cristal Sombrio**: Visualização estilo cristal com auras e partículas energéticas
- **🖥️ Matrix**: Interface estilo cyberpunk com caracteres caindo e estética verde digital
- **🔍 Scanner Biométrico**: Visualização de reconhecimento biométrico com análise de padrões
- **🤖 IA Assistant**: Interface futurística para assistentes de IA com feedback visual

## 🛠️ Tecnologia

Esta biblioteca utiliza:
- **PySide6**: Framework Qt para Python
- **Matemática Avançada**: Funções trigonométricas para animações orgânicas
- **Gradientes e Caminhos**: Renderização avançada de formas e cores

## ⚙️ Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/QuantumUI-Animations.git
cd QuantumUI-Animations

# Instale as dependências
pip install -r requirements.txt
```

## 🚀 Como Usar

Cada animação pode ser executada individualmente:

```bash
# Assistente Fantasmagórico
python voxy_animation.py

# Interface Matrix
python matrix_assistant.py

# Cristal Sombrio
python assistant_animation.py

# Scanner Biométrico
python biometric_scanner.py
```

Você também pode importar os componentes em seus próprios projetos:

```python
from voxy_animation import GhostlyAssistantWidget

# Crie uma aplicação com interface fantasmagórica
app = QApplication(sys.argv)
ghostly_ui = GhostlyAssistantWidget()
ghostly_ui.show()
sys.exit(app.exec())
```

## 📂 Estrutura do Projeto

```
QuantumUI-Animations/
│
├── voxy_animation.py            # Assistente Fantasmagórico
├── assistant_animation.py       # Cristal Sombrio
├── dark_crystal_animation.py    # Variação do Cristal
├── matrix_assistant.py          # Interface Matrix
├── biometric_scanner.py         # Scanner Biométrico
├── assistant_animation_ai.py    # Interface IA 
├── requirements.txt             # Dependências
└── README.md                    # Documentação
```

## 🎨 Galeria

<p align="center">
  <img src="docs/images/ghost.jpg" alt="Ghostly Assistant" width="200" />
  <img src="docs/images/crystal.jpg" alt="Crystal Interface" width="200" />
  <img src="docs/images/matrix.jpg" alt="Matrix Interface" width="200" />
</p>

## 🔮 Inspiração e Uso

Este projeto serve como:
- Conceitos de design para interfaces futurísticas
- Componentes visuais para aplicações desktop
- Base para dashboards e visualizações de dados
- Elementos decorativos para apresentações ou streams

## 📜 Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).

## 🙏 Agradecimentos

- Inspirado por interfaces de filmes de ficção científica
- Desenvolvido com base em técnicas avançadas de animação digital
- Comunidade Qt e Python por ferramentas e documentação

---

<p align="center">
  <i>Explore o futuro da interface do usuário com QuantumUI-Animations</i>
</p> 