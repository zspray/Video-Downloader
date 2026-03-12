# 🎬 Video Downloader

Um aplicativo desktop moderno com interface gráfica para baixar vídeos do YouTube, TikTok, Instagram e outras plataformas. Desenvolvido em Python utilizando `Tkinter` e impulsionado pelo poderoso motor do `yt-dlp`.

A interface apresenta um tema escuro moderno.

## ✨ Funcionalidades

* **Download Multiplataforma**: Suporte nativo a diversas redes sociais (YouTube, TikTok, etc).
* **Seleção de Qualidade e Formato**: Baixe na melhor qualidade disponível (MP4), escolha resoluções específicas (1080p, 720p) ou extraia apenas o áudio (MP3).
* **Análise Avançada**: Um painel de visualização em árvore (Treeview) para listar todos os formatos, codecs, taxas de bits e tamanhos de arquivo disponíveis antes de baixar.
* **Informações em Tempo Real**: Pré-visualização da miniatura (thumbnail) do vídeo, título, autor, duração e número de visualizações.
* **Interface Responsiva**: Processos pesados rodam em threads separadas, garantindo que a interface gráfica não trave (freeze) durante os downloads.
* **Pronto para Executável**: Código otimizado (`multiprocessing.freeze_support` e travas de sistema) para evitar loops de janelas ao compilar com ferramentas como o PyInstaller.

## 🚀 Pré-requisitos

1. **Python 3.8+** instalado no seu sistema.
2. **FFmpeg** (Altamente Recomendado): O `yt-dlp` depende do FFmpeg para juntar as faixas de vídeo e áudio nas resoluções mais altas (como 1080p ou 4K). 
   * Baixe o FFmpeg e adicione-o ao `PATH` do seu Windows ou coloque o executável na mesma pasta do projeto.

## 📦 Instalação e Uso (Modo Script)

1. Clone ou baixe este repositório.
2. Abra o terminal na pasta do projeto e instale as dependências:
   ```bash
   pip install -r requirements.txt