#!/usr/bin/env python3
"""
Interface Gráfica para a Ferramenta de Cópia de Transcrições do YouTube
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import asyncio
import threading
import sys
import os
from main import YouTubeTranscriptionCopier

class YouTubeTranscriptionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎥 Cópia de Transcrições do YouTube")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Variáveis
        self.url_var = tk.StringVar()
        self.output_file_var = tk.StringVar()
        self.headless_var = tk.BooleanVar(value=True)
        self.is_processing = False
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configura a interface do usuário"""
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="🎥 Ferramenta de Cópia de Transcrições do YouTube", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # URL do vídeo
        ttk.Label(main_frame, text="URL do Vídeo:").grid(row=1, column=0, sticky=tk.W, pady=5)
        url_entry = ttk.Entry(main_frame, textvariable=self.url_var, width=60)
        url_entry.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # Arquivo de saída
        ttk.Label(main_frame, text="Arquivo de Saída:").grid(row=2, column=0, sticky=tk.W, pady=5)
        output_entry = ttk.Entry(main_frame, textvariable=self.output_file_var, width=50)
        output_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 5))
        
        browse_button = ttk.Button(main_frame, text="Procurar...", command=self.browse_output_file)
        browse_button.grid(row=2, column=2, pady=5)
        
        # Opções
        options_frame = ttk.LabelFrame(main_frame, text="Opções", padding="10")
        options_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        options_frame.columnconfigure(0, weight=1)
        
        headless_check = ttk.Checkbutton(options_frame, text="Modo Headless (sem interface gráfica)", 
                                        variable=self.headless_var)
        headless_check.grid(row=0, column=0, sticky=tk.W)
        
        # Botões
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=4, column=0, columnspan=3, pady=20)
        
        self.process_button = ttk.Button(buttons_frame, text="🚀 Processar Vídeo", 
                                        command=self.start_processing)
        self.process_button.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_button = ttk.Button(buttons_frame, text="🗑️ Limpar", command=self.clear_fields)
        clear_button.pack(side=tk.LEFT, padx=(0, 10))
        
        help_button = ttk.Button(buttons_frame, text="❓ Ajuda", command=self.show_help)
        help_button.pack(side=tk.LEFT)
        
        # Barra de progresso
        self.progress_var = tk.StringVar(value="Pronto para processar")
        progress_label = ttk.Label(main_frame, textvariable=self.progress_var)
        progress_label.grid(row=5, column=0, columnspan=3, pady=(10, 5))
        
        self.progress_bar = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress_bar.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Área de log
        log_frame = ttk.LabelFrame(main_frame, text="Log de Execução", padding="5")
        log_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(7, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=80)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Área de resultado
        result_frame = ttk.LabelFrame(main_frame, text="Transcrição Copiada", padding="5")
        result_frame.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(8, weight=1)
        
        self.result_text = scrolledtext.ScrolledText(result_frame, height=10, width=80)
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
    def browse_output_file(self):
        """Abre diálogo para selecionar arquivo de saída"""
        filename = filedialog.asksaveasfilename(
            title="Salvar transcrição como...",
            defaultextension=".txt",
            filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")]
        )
        if filename:
            self.output_file_var.set(filename)
    
    def clear_fields(self):
        """Limpa todos os campos"""
        self.url_var.set("")
        self.output_file_var.set("")
        self.log_text.delete(1.0, tk.END)
        self.result_text.delete(1.0, tk.END)
        self.progress_var.set("Pronto para processar")
    
    def show_help(self):
        """Mostra janela de ajuda"""
        help_text = """
🎥 Ferramenta de Cópia de Transcrições do YouTube

Como usar:
1. Cole a URL do vídeo do YouTube no campo "URL do Vídeo"
2. (Opcional) Escolha um arquivo para salvar a transcrição
3. (Opcional) Desmarque "Modo Headless" para ver o navegador funcionando
4. Clique em "Processar Vídeo"

A ferramenta irá:
• Acessar o vídeo no YouTube
• Expandir a descrição
• Abrir a transcrição
• Remover os carimbos de data/hora
• Copiar todo o texto para a área de transferência
• Salvar em arquivo (se especificado)

Requisitos:
• Vídeo deve ter transcrição disponível
• Conexão com a internet
• Navegador Chromium (instalado automaticamente)

Dicas:
• Use modo headless para processamento mais rápido
• Desative headless se quiser ver o processo acontecendo
• A transcrição será copiada automaticamente para Ctrl+V
        """
        
        messagebox.showinfo("Ajuda", help_text)
    
    def log_message(self, message):
        """Adiciona mensagem ao log"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def start_processing(self):
        """Inicia o processamento em thread separada"""
        if self.is_processing:
            return
            
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Erro", "Por favor, insira a URL do vídeo")
            return
            
        if 'youtube.com/watch' not in url and 'youtu.be/' not in url:
            messagebox.showerror("Erro", "URL deve ser um vídeo do YouTube válido")
            return
        
        self.is_processing = True
        self.process_button.config(state='disabled', text="🔄 Processando...")
        self.progress_bar.start()
        self.log_text.delete(1.0, tk.END)
        self.result_text.delete(1.0, tk.END)
        
        # Executar em thread separada para não travar a UI
        thread = threading.Thread(target=self.process_video_thread, args=(url,))
        thread.daemon = True
        thread.start()
    
    def process_video_thread(self, url):
        """Processa o vídeo em thread separada"""
        try:
            # Criar novo loop de eventos para esta thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Executar o processamento
            result = loop.run_until_complete(self.process_video_async(url))
            
            # Atualizar UI no thread principal
            self.root.after(0, self.processing_complete, result)
            
        except Exception as e:
            self.root.after(0, self.processing_error, str(e))
    
    async def process_video_async(self, url):
        """Processa o vídeo de forma assíncrona"""
        copier = YouTubeTranscriptionCopier(headless=self.headless_var.get())
        
        # Redirecionar saída para o log
        import io
        import contextlib
        
        log_capture = io.StringIO()
        
        with contextlib.redirect_stdout(log_capture):
            texto = await copier.processar_video(url)
        
        # Capturar log
        log_output = log_capture.getvalue()
        
        # Atualizar log na UI
        self.root.after(0, self.update_log, log_output)
        
        return texto
    
    def update_log(self, log_output):
        """Atualiza o log na interface"""
        self.log_text.insert(tk.END, log_output)
        self.log_text.see(tk.END)
    
    def processing_complete(self, result):
        """Chamado quando o processamento é concluído"""
        self.is_processing = False
        self.process_button.config(state='normal', text="🚀 Processar Vídeo")
        self.progress_bar.stop()
        
        if result:
            self.progress_var.set("✅ Processamento concluído com sucesso!")
            
            # Mostrar resultado
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(1.0, result)
            
            # Salvar em arquivo se especificado
            output_file = self.output_file_var.get().strip()
            if output_file:
                try:
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(result)
                    self.log_message(f"💾 Transcrição salva em: {output_file}")
                except Exception as e:
                    self.log_message(f"❌ Erro ao salvar arquivo: {e}")
            
            # Copiar para área de transferência
            try:
                import pyperclip
                pyperclip.copy(result)
                self.log_message("📋 Texto copiado para a área de transferência!")
            except Exception as e:
                self.log_message(f"⚠️ Erro ao copiar para área de transferência: {e}")
            
            messagebox.showinfo("Sucesso", "Transcrição copiada com sucesso!")
            
        else:
            self.progress_var.set("❌ Falha no processamento")
            messagebox.showerror("Erro", "Falha ao processar o vídeo. Verifique o log para detalhes.")
    
    def processing_error(self, error_msg):
        """Chamado quando ocorre um erro no processamento"""
        self.is_processing = False
        self.process_button.config(state='normal', text="🚀 Processar Vídeo")
        self.progress_bar.stop()
        self.progress_var.set("❌ Erro no processamento")
        
        self.log_message(f"❌ Erro: {error_msg}")
        messagebox.showerror("Erro", f"Erro durante o processamento:\n{error_msg}")

def main():
    """Função principal da interface gráfica"""
    root = tk.Tk()
    app = YouTubeTranscriptionGUI(root)
    
    # Configurar ícone da janela (se disponível)
    try:
        root.iconbitmap('icon.ico')
    except:
        pass
    
    # Centralizar janela
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()
