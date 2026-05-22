#!/usr/bin/env python3
"""
Gerador Automático - Sistema de Atendimento Virtual
Cria/atualiza os arquivos HTML, CSS e JS no D:\Projeto Empresas
"""

import os
import webbrowser
from pathlib import Path

# ==========================================
# CONFIGURAÇÃO
# ==========================================
PASTA_PROJETO = Path(r"D:\Projeto Empresas")

# ==========================================
# CONTEÚDOS DOS ARQUIVOS
# ==========================================

HTML_CONTENT = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Atendimento Virtual</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div id="app-container">

        <!-- TELA 1: BOAS-VINDAS -->
        <div id="tela-boas-vindas" class="tela ativa">
            <div class="header-box">
                <h1 id="nome-cliente-destaque">Carregando...</h1>
                <p class="msg-intro">Olá! Como posso ajudar?</p>
            </div>
            <div class="botoes-acao">
                <button onclick="navegar('tela-servicos')" class="btn-grande btn-primario">📅 QUERO AGENDAR</button>
                <button onclick="navegar('tela-servicos')" class="btn-grande btn-secundario"> VER SERVIÇOS</button>
                <button onclick="alert('Transferindo...')" class="btn-grande btn-terciario"> FALAR COM PESSOA</button>
            </div>
        </div>

        <!-- TELA 2: LISTA DE SERVIÇOS -->
        <div id="tela-servicos" class="tela">
            <div class="header-simples">
                <button onclick="navegar('tela-boas-vindas')" class="btn-voltar">← Voltar</button>
                <h2>Nossos Serviços</h2>
            </div>
            <div class="lista-servicos">
                <div class="card-servico" onclick="selecionarServico('Corte Masculino')">
                    <span class="emoji">✂️</span>
                    <div class="info"><strong>Corte Masculino</strong><span class="detalhes">R$ 35,00 • 30 min</span></div>
                </div>
                <div class="card-servico" onclick="selecionarServico('Barba Completa')">
                    <span class="emoji"></span>
                    <div class="info"><strong>Barba Completa</strong><span class="detalhes">R$ 25,00</span></div>
                </div>
            </div>
        </div>

        <!-- TELA 3: ESCOLHER DATA -->
        <div id="tela-data" class="tela">
            <div class="header-simples">
                <button onclick="navegar('tela-servicos')" class="btn-voltar">← Voltar</button>
                <h2>Escolha o Dia</h2>
            </div>
            <p class="texto-orientacao">Serviço: <span id="servico-escolhido" class="destaque-texto">...</span></p>
            <div class="lista-datas">
                <div class="card-data" onclick="selecionarData('Hoje, Segunda')">
                    <span class="emoji">📆</span>
                    <div class="info"><strong>HOJE</strong><span class="detalhes">Segunda-feira</span></div>
                </div>
                <div class="card-data" onclick="selecionarData('Amanhã, Terça')">
                    <span class="emoji">📆</span>
                    <div class="info"><strong>AMANHÃ</strong><span class="detalhes">Terça-feira</span></div>
                </div>
                <div class="card-data" onclick="selecionarData('Outro Dia')">
                    <span class="emoji">🗓️</span>
                    <div class="info"><strong>OUTRO DIA</strong><span class="detalhes">Escolher no calendário</span></div>
                </div>
            </div>
        </div>

        <!-- TELA 4: ESCOLHER HORÁRIO -->
        <div id="tela-horario" class="tela">
            <div class="header-simples">
                <button onclick="navegar('tela-data')" class="btn-voltar">← Voltar</button>
                <h2>Horários Disponíveis</h2>
            </div>
            <p class="texto-orientacao">Para: <span id="data-escolhida" class="destaque-texto">...</span></p>
            <div class="lista-horarios">
                <button class="btn-slot" onclick="selecionarHora('14:00')">🕐 14:00</button>
                <button class="btn-slot" onclick="selecionarHora('14:30')">🕑 14:30</button>
                <button class="btn-slot" onclick="selecionarHora('15:00')"> 15:00</button>
                <button class="btn-slot" onclick="selecionarHora('15:30')"> 15:30</button>
            </div>
        </div>

        <!-- TELA 5: TELEFONE -->
        <div id="tela-whatsapp" class="tela">
            <div class="header-simples">
                <button onclick="navegar('tela-horario')" class="btn-voltar">← Voltar</button>
                <h2>Seu WhatsApp</h2>
            </div>
            <p class="texto-orientacao">Precisamos do seu contato para confirmar.</p>
            <div class="input-group">
                <label>Digite seu número:</label>
                <input type="tel" id="input-telefone" placeholder="(XX) 9XXXX-XXXX" oninput="mascararTelefone(this)">
            </div>
            <button onclick="confirmarAgendamento()" class="btn-grande btn-primario" style="margin-top: 30px;">✅ CONFIRMAR AGENDAMENTO</button>
        </div>

        <!-- TELA 6: SUCESSO -->
        <div id="tela-sucesso" class="tela">
            <div class="header-sucesso">
                <span class="emoji-grande">🎉</span>
                <h2>Agendado com Sucesso!</h2>
            </div>
            <div class="card-resumo">
                <p>👤 <span id="resumo-nome">...</span></p>
                <p>️ <span id="resumo-servico">...</span></p>
                <p> <span id="resumo-data">...</span></p>
                <p>🕒 <span id="resumo-hora">...</span></p>
                <p>📞 <span id="resumo-whatsapp">...</span></p>
            </div>
            <button onclick="alert('Enviado para o painel do atendente!')" class="btn-grande btn-secundario">👤 Falar com Atendente</button>
            <button onclick="window.location.reload()" class="btn-grande btn-terciario">🏠 Voltar ao Início</button>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

CSS_CONTENT = """:root {
    --cor-primaria: #2563eb;
    --cor-fundo: #f1f5f9;
    --cor-cartao: #ffffff;
    --cor-texto: #0f172a;
    --borda-raio: 12px;
}
* { margin: 0; padding: 0; box-sizing: border-box; font-family: system-ui, sans-serif; }
body { background-color: var(--cor-fundo); display: flex; justify-content: center; min-height: 100vh; }
#app-container { background-color: var(--cor-cartao); width: 100%; max-width: 480px; min-height: 100vh; position: relative; overflow: hidden; box-shadow: 0 0 20px rgba(0,0,0,0.1); }

/* Telas */
.tela { display: none; padding: 20px; animation: fadeIn 0.3s ease; }
.tela.ativa { display: block; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

/* Elementos Gerais */
.header-box { text-align: center; padding: 30px 0; background: #eff6ff; border-radius: var(--borda-raio); margin-bottom: 20px; }
.header-simples { display: flex; align-items: center; gap: 10px; margin-bottom: 20px; }
#nome-cliente-destaque { font-size: 28px; font-weight: 800; color: #1e3a8a; margin-bottom: 5px; }

/* Botões */
.btn-grande { width: 100%; padding: 16px; font-size: 16px; font-weight: bold; border: none; border-radius: var(--borda-raio); margin-bottom: 12px; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 10px; }
.btn-primario { background-color: var(--cor-primaria); color: white; box-shadow: 0 4px 6px rgba(37, 99, 235, 0.3); }
.btn-secundario { background-color: #e2e8f0; color: var(--cor-texto); }
.btn-terciario { background-color: #ffffff; border: 1px solid #cbd5e1; color: var(--cor-texto); }
.btn-voltar { background: none; border: none; font-size: 16px; color: var(--cor-primaria); cursor: pointer; font-weight: bold; }

/* Cards e Listas */
.card-servico, .card-data { background: white; border: 1px solid #cbd5e1; border-radius: var(--borda-raio); padding: 15px; margin-bottom: 15px; display: flex; align-items: center; gap: 15px; cursor: pointer; }
.card-servico:active, .card-data:active { transform: scale(0.98); background-color: #f8fafc; }

/* Botões de Horário */
.lista-horarios { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.btn-slot { padding: 15px; background: white; border: 1px solid var(--cor-primaria); border-radius: var(--borda-raio); color: var(--cor-primaria); font-weight: bold; cursor: pointer; font-size: 16px; }
.btn-slot:active { background: var(--cor-primaria); color: white; }

/* Input */
.input-group { margin-bottom: 20px; }
.input-group label { display: block; margin-bottom: 8px; font-weight: bold; color: var(--cor-texto); }
.input-group input { width: 100%; padding: 15px; font-size: 18px; border: 2px solid #cbd5e1; border-radius: var(--borda-raio); text-align: center; }
.input-group input:focus { border-color: var(--cor-primaria); outline: none; }

/* Sucesso */
.header-sucesso { text-align: center; margin-bottom: 30px; }
.emoji-grande { font-size: 60px; display: block; margin-bottom: 10px; }
.card-resumo { background: #f0f9ff; padding: 20px; border-radius: var(--borda-raio); margin-bottom: 30px; text-align: left; border: 1px solid #bae6fd; }
.card-resumo p { margin-bottom: 8px; font-size: 16px; color: #334155; }
.texto-orientacao { text-align: center; color: #64748b; margin-bottom: 20px; }
.destaque-texto { color: var(--cor-primaria); font-weight: bold; }
"""

JS_CONTENT = """// Dados do agendamento
let dadosAgendamento = { nome: "Yaire Suek", servico: "", data: "", hora: "", telefone: "" };

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById('nome-cliente-destaque').innerText = formatarNome(dadosAgendamento.nome);
});

function formatarNome(nome) { return nome.replace(/\\b\\w/g, l => l.toUpperCase()); }

function navegar(idTela) {
    document.querySelectorAll('.tela').forEach(t => t.classList.remove('ativa'));
    document.getElementById(idTela).classList.add('ativa');
}

function selecionarServico(nome) {
    dadosAgendamento.servico = nome;
    document.getElementById('servico-escolhido').innerText = nome;
    navegar('tela-data');
}

function selecionarData(data) {
    dadosAgendamento.data = data;
    document.getElementById('data-escolhida').innerText = data;
    navegar('tela-horario');
}

function selecionarHora(hora) {
    dadosAgendamento.hora = hora;
    navegar('tela-whatsapp');
}

function mascararTelefone(input) {
    let valor = input.value.replace(/\\D/g, "");
    if (valor.length > 11) valor = valor.slice(0, 11);
    if (valor.length > 7) input.value = `(${valor.slice(0,2)}) ${valor.slice(2,7)}-${valor.slice(7)}`;
    else if (valor.length > 2) input.value = `(${valor.slice(0,2)}) ${valor.slice(2)}`;
    else if (valor.length > 0) input.value = `(${valor}`;
}

function confirmarAgendamento() {
    const telInput = document.getElementById('input-telefone').value;
    if (telInput.length < 14) { alert("Por favor, digite o número completo."); return; }
    dadosAgendamento.telefone = telInput;
    document.getElementById('resumo-nome').innerText = dadosAgendamento.nome;
    document.getElementById('resumo-servico').innerText = dadosAgendamento.servico;
    document.getElementById('resumo-data').innerText = dadosAgendamento.data;
    document.getElementById('resumo-hora').innerText = dadosAgendamento.hora;
    document.getElementById('resumo-whatsapp').innerText = dadosAgendamento.telefone;
    navegar('tela-sucesso');
}
"""

# ==========================================
# FUNÇÕES DE EXECUÇÃO
# ==========================================

def salvar_arquivo(caminho: Path, conteudo: str):
    """Salva o conteúdo no arquivo especificado"""
    caminho.write_text(conteudo, encoding="utf-8")
    print(f"  {caminho.name}")

def main():
    print("\n🚀 Gerador Automático - Atendimento Virtual")
    print("="*40)
    
    # Cria a pasta se não existir
    PASTA_PROJETO.mkdir(parents=True, exist_ok=True)
    print(f" Pasta: {PASTA_PROJETO}")
    
    # Arquivos a serem criados/atualizados
    arquivos = {
        "index.html": HTML_CONTENT,
        "style.css": CSS_CONTENT,
        "script.js": JS_CONTENT
    }
    
    print("📝 Gerando arquivos...")
    for nome, conteudo in arquivos.items():
        salvar_arquivo(PASTA_PROJETO / nome, conteudo)
    
    print("\n✅ Sucesso! Todos os arquivos foram criados.")
    print(f"📍 Local: {PASTA_PROJETO}")
    
    # Abre no navegador
    caminho_html = PASTA_PROJETO / "index.html"
    print("\n🌐 Abrindo no navegador...")
    webbrowser.open(f"file:///{caminho_html.as_posix()}")

if __name__ == "__main__":
    main()