import os
import webbrowser
import sys

# ==========================================
# CONFIGURAÇÕES DO PROJETO
# ==========================================
# Caminho onde você quer criar os arquivos (baseado na sua foto)
CAMINHO_PASTA = r"D:\Projeto Empresas"

# ==========================================
# CONTEÚDOS DOS ARQUIVOS (O Código Real)
# ==========================================

HTML_CONTENT = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <!-- Configuração para Mobile (Responsivo) -->
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Atendimento Virtual</title>
    <!-- Link para o arquivo de estilos -->
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <!-- CONTAINER PRINCIPAL (Simula a tela do celular) -->
    <div id="app-container">

        <!-- ========================================== -->
        <!-- TELA 1: BOAS-VINDAS                        -->
        <!-- ========================================== -->
        <div id="tela-boas-vindas" class="tela ativa">
            
            <!-- Cabeçalho com Nome (Editável via JS) -->
            <div class="header-box">
                <h1 id="nome-cliente-destaque">Carregando...</h1>
                <p class="msg-intro">Olá! Eu sou a assistente virtual. <br> Como posso ajudar?</p>
            </div>

            <!-- Botões de Ação (Grandes e Claros - UX Dona Maria) -->
            <div class="botoes-acao">
                <!-- Botão Agendar -->
                <button onclick="navegar('tela-servicos')" class="btn-grande btn-primario">
                    📅 QUERO AGENDAR
                </button>
                
                <!-- Botão Serviços -->
                <button onclick="navegar('tela-servicos')" class="btn-grande btn-secundario">
                     📋 VER SERVIÇOS
                </button>

                <!-- Botão Atendimento Humano -->
                <button onclick="alert('Conectando ao humano...')" class="btn-grande btn-terciario">
                    👤 FALAR COM PESSOA
                </button>
            </div>
        </div>


        <!-- ========================================== -->
        <!-- TELA 2: LISTA DE SERVIÇOS                  -->
        <!-- ========================================== -->
        <div id="tela-servicos" class="tela">
            <div class="header-simples">
                <button onclick="navegar('tela-boas-vindas')" class="btn-voltar">← Voltar</button>
                <h2>Nossos Serviços</h2>
            </div>

            <!-- Lista de Serviços (Exemplo Visual) -->
            <div class="lista-servicos">
                
                <!-- Card 1: Com Preço e Tempo -->
                <div class="card-servico" onclick="selecionarServico('Corte Masculino')">
                    <span class="emoji">✂️</span>
                    <div class="info">
                        <strong>Corte Masculino</strong>
                        <span class="detalhes">R$ 35,00 • 30 min</span>
                    </div>
                </div>

                <!-- Card 2: Apenas Nome (Preço/Tempo ocultos) -->
                <div class="card-servico" onclick="selecionarServico('Barba')">
                    <span class="emoji">🧔</span>
                    <div class="info">
                        <strong>Barba Completa</strong>
                        <!-- Sem detalhes, pois estão desligados no painel -->
                    </div>
                </div>

            </div>
        </div>

    </div>

    <!-- Link para o arquivo de lógica (JavaScript) -->
    <script src="script.js"></script>
</body>
</html>
"""

CSS_CONTENT = """/* =========================================
   CONFIGURAÇÕES GERAIS (Variáveis de Cores)
   ========================================= */
:root {
    --cor-primaria: #2563eb;   /* Azul Profissional */
    --cor-fundo: #f1f5f9;      /* Cinza bem claro */
    --cor-cartao: #ffffff;     /* Branco puro */
    --cor-texto: #0f172a;      /* Preto suave */
    --borda-raio: 12px;        /* Cantos arredondados */
}

/* Reset básico */
* { margin: 0; padding: 0; box-sizing: border-box; font-family: system-ui, sans-serif; }

body {
    background-color: var(--cor-fundo);
    display: flex;
    justify-content: center; /* Centraliza no PC */
    min-height: 100vh;
}

/* O "Celular" na tela */
#app-container {
    background-color: var(--cor-cartao);
    width: 100%;
    max-width: 480px; /* Limite de largura estilo mobile */
    min-height: 100vh;
    position: relative;
    overflow: hidden;
    box-shadow: 0 0 20px rgba(0,0,0,0.1);
}

/* =========================================
   GERENCIAMENTO DE TELAS
   ========================================= */
/* Esconde todas as telas por padrão */
.tela { display: none; padding: 20px; animation: fadeIn 0.3s ease; }

/* Mostra apenas a tela ativa */
.tela.ativa { display: block; }

/* =========================================
   COMPONENTES VISUAIS (UX Simplificada)
   ========================================= */

/* Caixa de Destaque do Nome */
.header-box {
    text-align: center;
    padding: 30px 0;
    background: #eff6ff; 
    border-radius: var(--borda-raio);
    margin-bottom: 30px;
}

#nome-cliente-destaque {
    font-size: 28px; 
    font-weight: 800; 
    color: #1e3a8a;
    margin-bottom: 10px;
}

/* Botões Grandes e Fáceis de Tocar */
.btn-grande {
    width: 100%;
    padding: 18px; /* Altura generosa */
    font-size: 16px;
    font-weight: bold;
    border: none;
    border-radius: var(--borda-raio);
    margin-bottom: 15px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
}

.btn-primario {
    background-color: var(--cor-primaria);
    color: white;
    box-shadow: 0 4px 6px rgba(37, 99, 235, 0.3);
}

.btn-secundario {
    background-color: #e2e8f0;
    color: var(--cor-texto);
}

.btn-terciario {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    color: var(--cor-texto);
}

/* Cards de Serviços */
.card-servico {
    background: white;
    border: 1px solid #cbd5e1;
    border-radius: var(--borda-raio);
    padding: 15px;
    margin-bottom: 15px;
    display: flex;
    align-items: center;
    gap: 15px;
    cursor: pointer;
    transition: transform 0.2s;
}

.card-servico:active { transform: scale(0.98); }

.emoji { font-size: 24px; }

/* Botão Voltar */
.btn-voltar {
    background: none;
    border: none;
    font-size: 16px;
    color: var(--cor-primaria);
    cursor: pointer;
    font-weight: bold;
}

/* Animação de entrada */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
"""

JS_CONTENT = """/* =========================================
   CONFIGURAÇÃO INICIAL E DADOS
   ========================================= */

// Simulando o nome digitado pelo usuário na tela anterior
let usuarioNomeDigitado = "yaire suek"; 

// Ao carregar a página, inicia o sistema
document.addEventListener("DOMContentLoaded", () => {
    inicializarSistema();
});

function inicializarSistema() {
    // 1. CORRIGIR O NOME (Capitalização Profissional)
    // Ex: "yaire suek" -> "Yaire Suek"
    const nomeFormatado = formatarNome(usuarioNomeDigitado);
    
    // Atualiza o HTML com o nome corrigido
    document.getElementById('nome-cliente-destaque').innerText = nomeFormatado;
}

/* =========================================
   FUNÇÕES UTILITÁRIAS (Helpers)
   ========================================= */

// Função que deixa a primeira letra de cada palavra maiúscula
function formatarNome(nome) {
    return nome.replace(/\\b\\w/g, l => l.toUpperCase());
}

/* =========================================
   NAVEGAÇÃO (Troca de Telas)
   ========================================= */

// Função única para trocar de tela sem recarregar o site
function navegar(idDaTela) {
    // 1. Esconde todas as telas
    const todasTelas = document.querySelectorAll('.tela');
    todasTelas.forEach(tela => tela.classList.remove('ativa'));

    // 2. Mostra apenas a tela desejada
    const telaAlvo = document.getElementById(idDaTela);
    if(telaAlvo) {
        telaAlvo.classList.add('ativa');
    }
}

/* =========================================
   LÓGICA DE SERVIÇOS
   ========================================= */

// Quando o cliente clica num serviço
function selecionarServico(nomeServico) {
    console.log("Serviço escolhido: " + nomeServico);
    
    // Futuro: Aqui chamaria a função de Agendamento
    alert("Você escolheu: " + nomeServico + ". (Próximo passo: Escolher Data/Hora)");
}
"""

# ==========================================
# LÓGICA DE CRIAÇÃO DOS ARQUIVOS
# ==========================================

def criar_arquivo(caminho, conteudo):
    """Cria o arquivo com o conteúdo especificado"""
    try:
        with open(caminho, 'w', encoding='utf-8') as f:
            f.write(conteudo)
        print(f"✅ Criado com sucesso: {os.path.basename(caminho)}")
    except Exception as e:
        print(f"❌ Erro ao criar {os.path.basename(caminho)}: {e}")

def main():
    print("🚀 INICIANDO INSTALAÇÃO DO PROJETO...")
    
    # Verifica se a pasta existe, se não, cria
    if not os.path.exists(CAMINHO_PASTA):
        print(f"📁 Criando pasta em: {CAMINHO_PASTA}")
        os.makedirs(CAMINHO_PASTA)
    else:
        print(f"📂 Pasta encontrada em: {CAMINHO_PASTA}")

    # Lista de arquivos para gerar
    arquivos = [
        ("index.html", HTML_CONTENT),
        ("style.css", CSS_CONTENT),
        ("script.js", JS_CONTENT)
    ]

    # Cria cada arquivo
    for nome_arquivo, conteudo in arquivos:
        caminho_completo = os.path.join(CAMINHO_PASTA, nome_arquivo)
        criar_arquivo(caminho_completo, conteudo)

    print("\n✨ TUDO PRONTO!")
    print(f"📂 Seus arquivos estão em: {CAMINHO_PASTA}")
    
    # Abre o navegador automaticamente
    caminho_html = os.path.join(CAMINHO_PASTA, "index.html")
    print("🌐 Abrindo no navegador...")
    
    # Converte para formato URL (file:///)
    url = f"file:///{caminho_html.replace(os.sep, '/')}"
    webbrowser.open(url)

if __name__ == "__main__":
    main()