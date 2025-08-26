#!/usr/bin/env python3
"""
Ferramenta de Automação para Copiar Transcrições do YouTube
Baseada no guia do arquivo-base.md
"""

import asyncio
import time
import random
from playwright.async_api import async_playwright
import pyperclip
import argparse
import sys

class YouTubeTranscriptionCopier:
    def __init__(self, headless=False):
        self.headless = headless
        self.browser = None
        self.page = None
    
    async def inicializar_navegador(self):
        """Inicializa o navegador com configurações otimizadas"""
        playwright = await async_playwright().start()
        
        # Configurações para evitar detecção de bot
        self.browser = await playwright.chromium.launch(
            headless=self.headless,
            args=[
                '--no-sandbox',
                '--disable-blink-features=AutomationControlled',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor'
            ]
        )
        
        # Criar contexto com user agent real
        context = await self.browser.new_context(
            user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        self.page = await context.new_page()
        
        # Remover propriedades que indicam automação
        await self.page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
        """)
    
    async def simular_comportamento_humano(self, min_delay=1, max_delay=3):
        """Simula comportamento humano com atrasos aleatórios"""
        delay = random.uniform(min_delay, max_delay)
        await asyncio.sleep(delay)
    
    async def acessar_video_youtube(self, url_video):
        """Acessa o vídeo do YouTube especificado"""
        print(f"🎥 Acessando vídeo: {url_video}")
        await self.page.goto(url_video)
        await self.page.wait_for_load_state('networkidle')
        await self.simular_comportamento_humano()
    
    async def expandir_descricao(self):
        """Clica no botão 'Mais' para expandir a descrição"""
        print("📝 Expandindo descrição do vídeo...")
        
        # Lista de seletores para tentar encontrar o botão "mais"
        seletores_mais = [
            'tp-yt-paper-button#expand',
            'ytd-text-inline-expander tp-yt-paper-button#expand',
            'tp-yt-paper-button[id="expand"]',
            'button#expand',
            'tp-yt-paper-button:has-text("...mais")',
            'tp-yt-paper-button:has-text("mais")',
            '[role="button"]#expand',
            '[role="button"]:has-text("...mais")'
        ]
        
        for seletor in seletores_mais:
            try:
                print(f"🔍 Tentando seletor para 'mais': {seletor}")
                botao_mais = self.page.locator(seletor).first
                await botao_mais.wait_for(state='visible', timeout=5000)
                await botao_mais.click()
                await self.simular_comportamento_humano()
                print("✅ Descrição expandida com sucesso")
                return
            except Exception as e:
                print(f"⚠️  Seletor {seletor} falhou: {e}")
                continue
        
        # Se nenhum seletor funcionou, tenta buscar por texto na página
        try:
            print("🔍 Tentando buscar por texto '...mais' na página...")
            await self.page.get_by_text("...mais").first.click()
            await self.simular_comportamento_humano()
            print("✅ Descrição expandida com sucesso")
        except:
            try:
                print("🔍 Tentando buscar por texto 'mais' na página...")
                await self.page.get_by_text("mais").first.click()
                await self.simular_comportamento_humano()
                print("✅ Descrição expandida com sucesso")
            except Exception as e:
                print(f"⚠️  Botão 'Mais' não encontrado ou já expandido: {e}")
    
    async def abrir_transcricao(self):
        """Clica em 'Mostrar transcrição'"""
        print("📋 Abrindo transcrição...")
        
        # Lista de seletores para tentar
        seletores = [
            '#structured-description button:has-text("Mostrar transcrição")',
            '#structured-description button:has-text("Show transcript")',
            'button:has-text("Mostrar transcrição")',
            'button:has-text("Show transcript")',
            'button[aria-label*="transcrição"]',
            'button[aria-label*="transcript"]',
            '[role="button"]:has-text("Mostrar transcrição")',
            '[role="button"]:has-text("Show transcript")'
        ]
        
        for seletor in seletores:
            try:
                print(f"🔍 Tentando seletor: {seletor}")
                botao_transcricao = self.page.locator(seletor).first
                await botao_transcricao.wait_for(state='visible', timeout=5000)
                await botao_transcricao.click()
                await self.simular_comportamento_humano(2, 4)
                print("✅ Transcrição aberta com sucesso")
                return
            except Exception as e:
                print(f"⚠️  Seletor {seletor} falhou: {e}")
                continue
        
        # Se nenhum seletor funcionou, tenta buscar por texto na página
        try:
            print("🔍 Tentando buscar por texto na página...")
            await self.page.get_by_text("Mostrar transcrição").first.click()
            await self.simular_comportamento_humano(2, 4)
            print("✅ Transcrição aberta com sucesso")
        except:
            try:
                await self.page.get_by_text("Show transcript").first.click()
                await self.simular_comportamento_humano(2, 4)
                print("✅ Transcrição aberta com sucesso")
            except Exception as e:
                print(f"❌ Erro ao abrir transcrição: {e}")
                raise
    
    async def ocultar_timestamps(self):
        """Remove os carimbos de data/hora da transcrição"""
        print("⏰ Ocultando carimbos de data/hora...")
        
        try:
            # Procura pelo menu de três pontos na transcrição
            menu_pontos = self.page.locator('button[aria-label*="menu"], button:has([d*="M12,8c1.1,0,2,-0.9,2,-2s-0.9,-2,-2,-2"])')
            await menu_pontos.wait_for(state='visible', timeout=10000)
            await menu_pontos.click()
            await self.simular_comportamento_humano()
            
            # Clica na opção para alternar timestamps
            opcao_timestamp = self.page.locator('text="Alternar carimbos de data/hora", text="Toggle timestamps"')
            await opcao_timestamp.wait_for(state='visible', timeout=5000)
            await opcao_timestamp.click()
            await self.simular_comportamento_humano()
            print("✅ Carimbos de data/hora ocultados")
        except Exception as e:
            print(f"⚠️  Erro ao ocultar timestamps (pode já estar oculto): {e}")
    
    async def copiar_transcricao(self):
        """Seleciona e copia toda a transcrição"""
        print("📋 Copiando transcrição...")
        
        try:
            # Localiza o container da transcrição - usando primeiro elemento
            container_transcricao = self.page.locator('#segments-container').first
            await container_transcricao.wait_for(state='visible', timeout=10000)
            
            # Extrai o texto diretamente dos segmentos da transcrição
            segmentos = await self.page.locator('#segments-container ytd-transcript-segment-renderer').all()
            
            texto_completo = []
            for segmento in segmentos:
                try:
                    # Pega apenas o texto, ignorando timestamps
                    texto_segmento = await segmento.locator('.segment-text').inner_text()
                    if texto_segmento.strip():
                        texto_completo.append(texto_segmento.strip())
                except:
                    # Se não conseguir pegar o texto do segmento, tenta pegar todo o texto
                    texto_segmento = await segmento.inner_text()
                    # Remove timestamps (formato 0:00, 1:23, etc.)
                    import re
                    texto_limpo = re.sub(r'\d{1,2}:\d{2}', '', texto_segmento).strip()
                    if texto_limpo:
                        texto_completo.append(texto_limpo)
            
            if texto_completo:
                resultado = ' '.join(texto_completo)
                print(f"✅ Transcrição extraída com sucesso! ({len(resultado)} caracteres)")
                return resultado
            else:
                raise Exception("Nenhum texto foi encontrado nos segmentos")
                
        except Exception as e:
            print(f"❌ Erro ao copiar transcrição: {e}")
            # Tenta método alternativo - selecionar tudo na área da transcrição
            try:
                print("🔄 Tentando método alternativo...")
                
                # Clica na área da transcrição e seleciona tudo
                await self.page.locator('#segments-container').first.click()
                await self.simular_comportamento_humano(0.5, 1)
                await self.page.keyboard.press('Control+a')
                await self.simular_comportamento_humano(0.5, 1)
                
                # Obtém o texto selecionado
                texto_selecionado = await self.page.evaluate('''
                    () => {
                        const selection = window.getSelection();
                        return selection.toString();
                    }
                ''')
                
                if texto_selecionado:
                    # Remove timestamps do texto selecionado
                    import re
                    texto_limpo = re.sub(r'\d{1,2}:\d{2}', '', texto_selecionado)
                    texto_limpo = re.sub(r'\s+', ' ', texto_limpo).strip()
                    print(f"✅ Transcrição copiada via método alternativo! ({len(texto_limpo)} caracteres)")
                    return texto_limpo
                else:
                    raise Exception("Nenhum texto foi selecionado")
                    
            except Exception as e2:
                print(f"❌ Erro no método alternativo: {e2}")
                raise
    
    async def processar_video(self, url_video):
        """Executa todo o processo de extração da transcrição"""
        try:
            await self.inicializar_navegador()
            await self.acessar_video_youtube(url_video)
            await self.expandir_descricao()
            await self.abrir_transcricao()
            await self.ocultar_timestamps()
            texto = await self.copiar_transcricao()
            
            return texto
            
        except Exception as e:
            print(f"❌ Erro durante o processamento: {e}")
            return None
        finally:
            if self.browser:
                await self.browser.close()
    
    async def fechar(self):
        """Fecha o navegador"""
        if self.browser:
            await self.browser.close()

async def main():
    parser = argparse.ArgumentParser(description='Ferramenta para copiar transcrições do YouTube')
    parser.add_argument('url', help='URL do vídeo do YouTube')
    parser.add_argument('--headless', action='store_true', help='Executar em modo headless (sem interface gráfica)')
    parser.add_argument('--output', '-o', help='Arquivo para salvar a transcrição')
    
    args = parser.parse_args()
    
    # Validação básica da URL
    if 'youtube.com/watch' not in args.url and 'youtu.be/' not in args.url:
        print("❌ Erro: URL deve ser um vídeo do YouTube válido")
        sys.exit(1)
    
    print("🚀 Iniciando ferramenta de cópia de transcrição do YouTube")
    print("📌 Baseada no guia do arquivo-base.md")
    print("-" * 60)
    
    copier = YouTubeTranscriptionCopier(headless=args.headless)
    
    try:
        texto_transcricao = await copier.processar_video(args.url)
        
        if texto_transcricao:
            # Copia para a área de transferência do sistema
            pyperclip.copy(texto_transcricao)
            print("📋 Texto copiado para a área de transferência!")
            
            # Salva em arquivo se especificado
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(texto_transcricao)
                print(f"💾 Transcrição salva em: {args.output}")
            
            print("\n" + "="*60)
            print("✅ PROCESSO CONCLUÍDO COM SUCESSO!")
            print("="*60)
            
        else:
            print("\n" + "="*60)
            print("❌ FALHA NO PROCESSO")
            print("="*60)
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⏹️  Processo interrompido pelo usuário")
        await copier.fechar()
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        await copier.fechar()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
