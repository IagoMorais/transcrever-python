#!/bin/bash

# Script de Instalação da Ferramenta de Cópia de Transcrições do YouTube
# Autor: Assistente IA
# Data: $(date)

echo "🎥 Instalando Ferramenta de Cópia de Transcrições do YouTube..."
echo "================================================================"

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale Python 3.7 ou superior."
    exit 1
fi

echo "✅ Python encontrado: $(python3 --version)"

# Verificar se pip está instalado
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 não encontrado. Instalando pip..."
    sudo apt-get update
    sudo apt-get install -y python3-pip
fi

echo "✅ pip encontrado: $(pip3 --version)"

# Verificar se python3-full está instalado
echo "🔧 Verificando python3-full..."
if ! dpkg -l | grep -q python3-full; then
    echo "📦 Instalando python3-full..."
    sudo apt-get update
    sudo apt-get install -y python3-full python3-venv
fi

# Remover ambiente virtual existente se estiver corrompido
if [ -d "venv" ] && [ ! -f "venv/bin/activate" ]; then
    echo "🗑️ Removendo ambiente virtual corrompido..."
    rm -rf venv
fi

# Criar ambiente virtual
echo "📦 Criando ambiente virtual..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Ambiente virtual criado"
else
    echo "✅ Ambiente virtual já existe"
fi

# Ativar ambiente virtual
echo "🔄 Ativando ambiente virtual..."
source venv/bin/activate

# Atualizar pip
echo "⬆️ Atualizando pip..."
python -m pip install --upgrade pip

# Instalar dependências
echo "📥 Instalando dependências..."
if [ -f "requirements.txt" ]; then
    python -m pip install -r requirements.txt
    echo "✅ Dependências instaladas com sucesso"
else
    echo "❌ Arquivo requirements.txt não encontrado"
    exit 1
fi

# Instalar Playwright browsers
echo "🌐 Instalando navegadores do Playwright..."
python -m playwright install chromium

# Verificar instalação
echo "🔍 Verificando instalação..."
python3 -c "import playwright; print('✅ Playwright instalado')"
python3 -c "import tkinter; print('✅ Tkinter disponível')"
python3 -c "import asyncio; print('✅ Asyncio disponível')"

# Criar script de execução
echo "📝 Criando scripts de execução..."

# Script para interface gráfica
cat > run_gui.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python3 gui.py
EOF

# Script para linha de comando
cat > run_cli.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python3 main.py "$@"
EOF

# Tornar scripts executáveis
chmod +x run_gui.sh
chmod +x run_cli.sh

echo ""
echo "🎉 Instalação concluída com sucesso!"
echo "================================================================"
echo ""
echo "📋 Como usar:"
echo "  Interface Gráfica: ./run_gui.sh"
echo "  Linha de Comando:  ./run_cli.sh <URL_DO_VIDEO>"
echo ""
echo "📁 Arquivos criados:"
echo "  - venv/           (ambiente virtual)"
echo "  - run_gui.sh      (executar interface gráfica)"
echo "  - run_cli.sh      (executar linha de comando)"
echo ""
echo "🔧 Para ativar manualmente o ambiente virtual:"
echo "  source venv/bin/activate"
echo ""
echo "📖 Para mais informações, consulte o README.md"
echo ""
echo "✨ Pronto para usar! Execute ./run_gui.sh para começar."
