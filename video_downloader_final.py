#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Video Downloader - Interface GUI Final
Tema moderno escuro com inspiração em Maps4Study
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path
import threading
import sys
import json
import multiprocessing 
from PIL import Image, ImageTk
from io import BytesIO
import requests
import yt_dlp # Motor interno

class VideoDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 Video Downloader")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Cores (tema escuro inspirado em Maps4Study)
        self.bg_dark = "#0f1419"
        self.bg_card = "#1a1f2e"
        self.fg_light = "#ffffff"
        self.accent_purple = "#7c3aed"
        self.accent_purple_hover = "#9d4edd"
        self.bg_input = "#252d3d"
        self.text_secondary = "#a0aec0"
        
        self.root.configure(bg=self.bg_dark)
        self.setup_styles()
        
        self.url_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Pronto")
        self.is_downloading = False
        self.video_data = None
        
        # Configurações
        self.quality_var = tk.StringVar(value="best[ext=mp4]/best")
        self.format_var = tk.StringVar(value="Melhor MP4")
        
        self.create_ui()
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background=self.bg_dark)
        style.configure('TLabel', background=self.bg_dark, foreground=self.fg_light)
        style.configure('TLabelFrame', background=self.bg_dark, foreground=self.fg_light)
        style.configure('TLabelFrame.Label', background=self.bg_dark, foreground=self.fg_light)
        style.configure('TButton', background=self.bg_card, foreground=self.fg_light, borderwidth=0, relief='flat', padding=10)
        style.map('TButton', background=[('active', self.accent_purple_hover)])
        style.configure('Accent.TButton', background=self.accent_purple, foreground=self.fg_light, borderwidth=0, relief='flat', padding=10)
        style.map('Accent.TButton', background=[('active', self.accent_purple_hover)])
        style.configure('TCombobox', fieldbackground=self.bg_input, background=self.bg_input, foreground=self.fg_light)
        style.map('TCombobox', fieldbackground=[('readonly', self.bg_input)], background=[('readonly', self.bg_input)])
        style.configure('TText', background=self.bg_input, foreground=self.fg_light)
        
    def create_ui(self):
        header = tk.Frame(self.root, bg=self.bg_dark)
        header.pack(fill='x', padx=0, pady=0)
        top_bar = tk.Frame(self.root, bg=self.accent_purple, height=3)
        top_bar.pack(fill='x', side='top')
        header_content = tk.Frame(self.root, bg=self.bg_dark)
        header_content.pack(fill='x', padx=25, pady=20)
        tk.Label(header_content, text="🎬 Video Downloader", font=('Segoe UI', 24, 'bold'), bg=self.bg_dark, fg=self.fg_light).pack(anchor='w')
        tk.Label(header_content, text="Baixe vídeos do YouTube, TikTok e Instagram em qualquer formato e resolução", font=('Segoe UI', 10), bg=self.bg_dark, fg=self.text_secondary).pack(anchor='w', pady=(5, 0))
        
        url_frame = tk.Frame(self.root, bg=self.bg_dark)
        url_frame.pack(fill='x', padx=25, pady=20)
        tk.Label(url_frame, text="URL do Vídeo", font=('Segoe UI', 11, 'bold'), bg=self.bg_dark, fg=self.fg_light).pack(anchor='w', pady=(0, 8))
        url_entry = tk.Entry(url_frame, textvariable=self.url_var, font=('Segoe UI', 10), bg=self.bg_input, fg=self.fg_light, insertbackground=self.accent_purple, relief='flat', bd=0)
        url_entry.pack(fill='x', padx=12, pady=10)
        url_entry.configure(highlightthickness=1, highlightbackground=self.accent_purple)
        
        btn_frame = tk.Frame(self.root, bg=self.bg_dark)
        btn_frame.pack(fill='x', padx=25, pady=10)
        def create_button(parent, text, command, accent=False):
            return tk.Button(parent, text=text, command=command, font=('Segoe UI', 11, 'bold'), bg=self.accent_purple if accent else self.bg_card, fg=self.fg_light, relief='flat', bd=0, padx=24, pady=12, cursor='hand2', activebackground=self.accent_purple_hover)
        
        create_button(btn_frame, "🔍 Informações", self.get_info).pack(side='left', padx=5)
        create_button(btn_frame, "⬇️ Download", self.start_download, accent=True).pack(side='left', padx=5)
        create_button(btn_frame, "📊 Formatos", self.show_formats).pack(side='left', padx=5)
        
        config_frame = tk.Frame(self.root, bg=self.bg_card, relief='flat', bd=0)
        config_frame.pack(fill='x', padx=25, pady=15)
        config_inner = tk.Frame(config_frame, bg=self.bg_card)
        config_inner.pack(fill='x', padx=15, pady=12)
        tk.Label(config_inner, text="Formato:", font=('Segoe UI', 10, 'bold'), bg=self.bg_card, fg=self.fg_light).pack(side='left', padx=(0, 10))
        quality_combo = ttk.Combobox(config_inner, textvariable=self.format_var, values=["Melhor MP4", "Melhor (qualquer formato)", "Vídeo HD + Áudio", "Apenas Áudio (MP3)", "1080p Full HD", "720p HD", "480p SD", "360p Low"], state='readonly', width=30, font=('Segoe UI', 9))
        quality_combo.pack(side='left', padx=5)
        quality_combo.bind('<<ComboboxSelected>>', self.on_quality_change)
        self.cmd_label = tk.Label(config_inner, text=f"Comando: -f {self.quality_var.get()}", font=('Segoe UI', 8), bg=self.bg_card, fg=self.text_secondary)
        self.cmd_label.pack(side='left', padx=15)
        
        info_frame = tk.Frame(self.root, bg=self.bg_card, relief='flat', bd=0)
        info_frame.pack(fill='x', padx=25, pady=10)
        tk.Label(info_frame, text="Informações do Vídeo", font=('Segoe UI', 10, 'bold'), bg=self.bg_card, fg=self.fg_light).pack(anchor='w', padx=15, pady=(10, 5))
        info_content = tk.Frame(info_frame, bg=self.bg_card)
        info_content.pack(fill='x', padx=15, pady=(0, 10))
        self.info_text = tk.Text(info_content, height=4, width=50, font=('Segoe UI', 9), bg=self.bg_input, fg=self.fg_light, relief='flat', bd=1, insertbackground=self.accent_purple)
        self.info_text.pack(side='left', fill='both', expand=True, padx=(0, 10))
        thumb_container = tk.Frame(info_content, bg=self.bg_input, width=120, height=90)
        thumb_container.pack(side='left', padx=5)
        thumb_container.pack_propagate(False)
        self.thumb_label = tk.Label(thumb_container, text="Miniatura\nindisponível", bg=self.bg_input, fg=self.text_secondary, font=('Segoe UI', 8))
        self.thumb_label.pack(fill='both', expand=True)
        
        log_frame = tk.Frame(self.root, bg=self.bg_card, relief='flat', bd=0)
        log_frame.pack(fill='both', expand=True, padx=25, pady=10)
        tk.Label(log_frame, text="Log", font=('Segoe UI', 10, 'bold'), bg=self.bg_card, fg=self.fg_light).pack(anchor='w', padx=15, pady=(10, 5))
        self.log = scrolledtext.ScrolledText(log_frame, height=8, font=('Courier', 9), bg=self.bg_input, fg=self.fg_light, relief='flat', bd=1, insertbackground=self.accent_purple)
        self.log.pack(fill='both', expand=True, padx=15, pady=(0, 10))
        
        status_frame = tk.Frame(self.root, bg=self.bg_dark)
        status_frame.pack(fill='x', padx=25, pady=10)
        ttk.Label(status_frame, textvariable=self.status_var, font=('Segoe UI', 9)).pack(anchor='w')

    def log_msg(self, msg):
        self.log.insert('end', f"{msg}\n")
        self.log.see('end')
        self.root.update()

    def on_quality_change(self, event=None):
        selection = self.format_var.get()
        quality_map = {"Melhor MP4": "best[ext=mp4]/best", "Melhor (qualquer formato)": "best", "Vídeo HD + Áudio": "bestvideo+bestaudio/best", "Apenas Áudio (MP3)": "bestaudio/best", "1080p Full HD": "best[height<=1080]/best", "720p HD": "best[height<=720]/best", "480p SD": "best[height<=480]/best", "360p Low": "best[height<=360]/best"}
        self.quality_var.set(quality_map.get(selection, "best[ext=mp4]/best"))
        self.cmd_label.config(text=f"Comando: -f {self.quality_var.get()}")
        self.log_msg(f"📝 Formato alterado para: {selection}")

    def show_formats(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("Erro", "Insira uma URL!")
            return
        self.log_msg("\n" + "="*50)
        self.log_msg("🔍 Obtendo formatos disponíveis...")
        def fetch_formats():
            try:
                ydl_opts = {'quiet': True, 'no_warnings': True}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    data = ydl.extract_info(url, download=False)
                    formats = data.get('formats', [])
                    self.root.after(0, lambda: self.show_formats_window(formats))
                    self.log_msg("✅ Janela de formatos aberta!")
            except Exception as e:
                self.log_msg(f"❌ Erro: {e}")
        threading.Thread(target=fetch_formats, daemon=True).start()

    def show_formats_window(self, formats):
        win = tk.Toplevel(self.root)
        win.title("📊 Formatos Disponíveis")
        win.geometry("1200x650")
        win.configure(bg=self.bg_dark)
        label_frame = tk.Frame(win, bg=self.bg_dark)
        label_frame.pack(fill='x', padx=15, pady=12)
        ttk.Label(label_frame, text=f"Total: {len(formats)} formatos | Selecione um formato", font=('Segoe UI', 11, 'bold')).pack(anchor='w')
        frame = ttk.Frame(win)
        frame.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        tree = ttk.Treeview(frame, columns=('ID', 'Ext', 'Resolução', 'FPS', 'Tamanho', 'Codec', 'Bitrate'), height=20)
        tree.column('#0', width=0, stretch='no')
        for col in tree['columns']: tree.heading(col, text=col); tree.column(col, width=100, anchor='center')
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        def format_size(size):
            if not size: return "N/A"
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024: return f"{size:.1f}{unit}"
                size /= 1024
            return "N/A"
        valid_formats = [fmt for fmt in formats if fmt.get('vcodec') != 'none' or fmt.get('acodec') != 'none']
        sorted_formats = sorted(valid_formats, key=lambda x: (-(x.get('height') or 0), -(x.get('fps') or 0), -(x.get('filesize') or 0)))
        for fmt in sorted_formats:
            tags = ('video_audio',) if fmt.get('vcodec') != 'none' and fmt.get('acodec') != 'none' else (('video',) if fmt.get('vcodec') != 'none' else ('audio',))
            tree.insert('', 'end', values=(fmt.get('format_id', ''), fmt.get('ext', ''), fmt.get('resolution', 'N/A'), str(fmt.get('fps', 'N/A')), format_size(fmt.get('filesize', 0)), fmt.get('vcodec', 'unknown')[:40], fmt.get('format_note', '')), tags=tags)
        tree.tag_configure('video_audio', background='#1b8a3e', foreground='#ffffff')
        tree.tag_configure('video', background='#1565c0', foreground='#ffffff')
        tree.tag_configure('audio', background='#e65100', foreground='#ffffff')
        btn_frame = tk.Frame(win, bg=self.bg_dark)
        btn_frame.pack(fill='x', padx=15, pady=15)
        def use_format():
            sel = tree.selection()
            if not sel: return
            val = tree.item(sel[0])['values']
            self.quality_var.set(str(val[0])); self.format_var.set("Personalizado")
            self.cmd_label.config(text=f"Comando: -f {val[0]}")
            self.log_msg(f"✅ Formato selecionado: {val[0]}")
            win.destroy()
        tk.Button(btn_frame, text="✅ Usar Selecionado", command=use_format, font=('Segoe UI', 11, 'bold'), bg=self.accent_purple, fg=self.fg_light, relief='flat', padx=28, pady=12).pack(side='left', padx=5)
        tk.Button(btn_frame, text="❌ Fechar", command=win.destroy, font=('Segoe UI', 11, 'bold'), bg=self.bg_card, fg=self.fg_light, relief='flat', padx=28, pady=12).pack(side='left', padx=5)

    def get_info(self):
        url = self.url_var.get().strip()
        if not url: messagebox.showwarning("Erro", "Insira uma URL!"); return
        self.log_msg("\n" + "="*50); self.log_msg(f"🔄 Obtendo informações de: {url}")
        def fetch():
            try:
                ydl_opts = {'quiet': True, 'no_warnings': True}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    data = ydl.extract_info(url, download=False)
                    self.video_data = data
                    self.root.after(0, lambda: self._update_info_ui(data))
            except Exception as e:
                self.log_msg(f"❌ Erro: {e}"); self.status_var.set("❌ Erro")
        threading.Thread(target=fetch, daemon=True).start()

    def _update_info_ui(self, data):
        self.info_text.delete('1.0', 'end')
        info = f"Título: {data.get('title', 'N/A')[:40]}\nAutor: {data.get('uploader', 'N/A')[:30]}\nDuração: {data.get('duration', 0)} seg\nViews: {data.get('view_count', 0):,}"
        self.info_text.insert('1.0', info)
        self.load_thumbnail(data); self.log_msg("✅ Informações obtidas!")
        self.status_var.set("✅ Pronto para baixar")

    def load_thumbnail(self, data):
        try:
            url = data.get('thumbnail') or (data.get('thumbnails')[-1]['url'] if data.get('thumbnails') else None)
            if url:
                res = requests.get(url, timeout=10)
                if res.status_code == 200:
                    img = Image.open(BytesIO(res.content))
                    img.thumbnail((120, 90), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    self.thumb_label.config(image=photo, text=""); self.thumb_label.image = photo
        except Exception as e: self.log_msg(f"⚠️ Erro thumbnail: {str(e)[:50]}")

    def start_download(self):
        if not self.video_data: messagebox.showwarning("Erro", "Obtenha info primeiro!"); return
        folder = filedialog.askdirectory(initialdir=str(Path.home() / "Downloads"))
        if not folder: return
        self.is_downloading = True; self.log_msg("\n" + "="*50); self.log_msg("🎬 Iniciando download...")
        def download():
            try:
                ydl_opts = {
                    'format': self.quality_var.get(),
                    'outtmpl': f'{folder}/%(title)s.%(ext)s',
                    'quiet': True,
                    'no_warnings': True
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([self.url_var.get()])
                self.log_msg("✅ Download concluído!"); self.status_var.set("✅ Concluído!")
                messagebox.showinfo("Sucesso", "Vídeo baixado!")
            except Exception as e: self.log_msg(f"❌ {e}"); self.status_var.set("❌ Erro")
            finally: self.is_downloading = False
        threading.Thread(target=download, daemon=True).start()

def main():
    multiprocessing.freeze_support()
    
    # === A TRAVA MÁGICA CONTRA O LOOP DE JANELAS ===
    # Verifica se NÃO é um executável congelado. 
    # Se for um .exe, ele pula o auto_setup e o loop morre aqui.
    if not getattr(sys, 'frozen', False):
        try:
            from auto_setup import ensure_yt_dlp
            ensure_yt_dlp()
        except Exception as e:
            print(f"Aviso auto_setup: {e}")

    root = tk.Tk()
    app = VideoDownloader(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()