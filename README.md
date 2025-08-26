# 🎥 Ferramenta de Automação para Cópia de Transcrições do YouTube

Esta ferramenta automatiza o processo de copiar transcrições de vídeos do YouTube, seguindo as melhores práticas descritas no arquivo-base.md.

## 🚀 Características

- **Automação Completa**: Automatiza todos os 8 passos manuais necessários para copiar uma transcrição
- **Baseada em Playwright**: Utiliza a ferramenta mais recomendada para automação de sites dinâmicos
- **Comportamento Humano**: Simula atrasos e movimentos naturais para evitar detecção
- **Flexível**: Suporte para modo headless e salvamento em arquivo
- **Robusta**: Tratamento de erros e recuperação automática

## 📋 Processo Automatizado

A ferramenta automatiza exatamente os passos descritos na tarefa:

1. ✅ Acessa o YouTube e abre o vídeo especificado
2. ✅ Clica no botão "Mais" para expandir a descrição
3. ✅ Clica em "Mostrar transcrição"
4. ✅ Clica no ícone de três pontos e seleciona "Alternar carimbos de data/hora"
5. ✅ Seleciona todo o texto da transcrição automaticamente
6. ✅ Copia o texto para a área de transferência
7. ✅ Opcionalmente salva em arquivo
8. ✅ Exibe confirmação de sucesso

## 🛠️ Instalação

### Instalação Automática (Recomendada)

```bash
chmod +x install.sh
./install.sh
```

### Instalação Manual

1. **Instalar dependências Python:**
```bash
pip3 install -r requirements.txt
```

2. **Instalar navegadores do Playwright:**
```bash
python3 -m playwright install
```

## 📖 Como Usar

### Uso Básico
```bash
python3 main.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Uso Avançado
```bash
# Executar em modo headless (sem interface gráfica)
python3 main.py "https://www.youtube.com/watch?v=VIDEO_ID" --headless

# Salvar transcrição em arquivo
python3 main.py "https://www.youtube.com/watch?v=VIDEO_ID" --output transcricao.txt

# Combinar opções
python3 main.py "https://www.youtube.com/watch?v=VIDEO_ID" --headless --output transcricao.txt
```

## 🎯 Exemplos Práticos

### Exemplo 1: Cópia Simples
```bash
python3 main.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```
- Abre o navegador visualmente
- Executa todo o processo automaticamente
- Copia o texto para a área de transferência

### Exemplo 2: Processamento em Lote
```bash
python3 main.py "https://www.youtube.com/watch?v=VIDEO1" --headless --output video1.txt
python3 main.py "https://www.youtube.com/watch?v=VIDEO2" --headless --output video2.txt
```

## 🔧 Opções de Linha de Comando

| Opção | Descrição |
|-------|-----------|
| `url` | URL do vídeo do YouTube (obrigatório) |
| `--headless` | Executa sem interface gráfica (mais rápido) |
| `--output FILE` | Salva a transcrição no arquivo especificado |

## 🛡️ Recursos de Segurança

Seguindo as recomendações do arquivo-base.md, a ferramenta implementa:

- **Simulação de Comportamento Humano**: Atrasos aleatórios entre ações
- **User Agent Real**: Usa user agent de navegador real
- **Remoção de Indicadores de Automação**: Remove propriedades que indicam bot
- **Tratamento de Erros**: Recuperação automática de falhas temporárias

## 🔍 Solução de Problemas

### Erro: "Transcrição não encontrada"
- Verifique se o vídeo possui transcrição disponível
- Alguns vídeos podem ter transcrições desabilitadas

### Erro: "Botão não encontrado"
- O YouTube pode ter alterado a interface
- Tente executar sem `--headless` para ver o que está acontecendo

### Erro: "Navegador não inicializa"
- Execute: `python3 -m playwright install`
- Verifique se tem permissões suficientes

## 🏗️ Arquitetura

A ferramenta segue a **Abordagem de Ferramenta Dedicada com API** recomendada no arquivo-base.md:

- ✅ **Previsibilidade**: Comportamento consistente e confiável
- ✅ **Baixo Custo**: Sem dependência de APIs pagas de IA
- ✅ **Performance**: Otimizada para esta tarefa específica
- ✅ **Controle Total**: Lógica explícita e auditável

## 📊 Vantagens sobre Métodos Manuais

| Aspecto | Manual | Automatizado |
|---------|--------|--------------|
| Tempo | ~2-3 minutos | ~30 segundos |
| Precisão | Sujeito a erro humano | 100% consistente |
| Escalabilidade | Limitada | Ilimitada |
| Repetibilidade | Cansativo | Effortless |

## 🤝 Contribuições

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para detalhes.

## 🙏 Agradecimentos

- Baseado nas recomendações técnicas do arquivo-base.md
- Utiliza Playwright para automação robusta
- Inspirado na necessidade de automatizar tarefas repetitivas
