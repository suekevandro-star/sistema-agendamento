#!/usr/bin/env python3
"""Atualizador Automático - Sistema com 5 Caixas"""
from pathlib import Path
import webbrowser

PASTA = Path(r"D:\Projeto Empresas")

HTML_CODE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Atendimento Virtual</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div id="app-container">
        <div id="tela-entrada" class="tela ativa">
            <div class="box-empresa">
                <h1 id="nome-empresa-display">Clínica Sorriso</h1>
                <span class="subtitulo-empresa">Assistente Virtual</span>
            </div>
            <div class="row-bot-info">
                <div class="box-foto-bot">
                    <img src="bot.png" alt="Bot" onerror="this.src='https://ui-avatars.com/api/?name=Bella&background=2563eb&color=fff&size=150'">
                </div>
                <div class="box-msg-bot">
                    <p>"Olá! Sou a Bella. <br>Como posso ajudar você hoje?"</p>
                </div>
            </div>
            <div class="box-orientacao">
                <strong>INICIAR - DIGITE SEU NOME</strong>
                <small>(Para começarmos nosso atendimento)</small>
            </div>
            <div class="box-input-nome">
                <input type="text" id="input-nome-cliente" placeholder="Digite seu nome aqui..." autocomplete="name">
            </div>
            <button onclick="iniciarSistema()" class="btn-grande btn-primario" style="margin-top: 20px;">✅ CONTINUAR</button>
        </div>

        <div id="tela-boas-vindas" class="tela">
            <div class="header-box">
                <h1 id="nome-cliente-destaque">...</h1>
                <p class="msg-intro">Olá! Como posso ajudar?</p>
            </div>
            <div class="botoes-acao">
                <button onclick="navegar('tela-servicos')" class="btn-grande btn-primario">📅 QUERO AGENDAR</button>
                <button onclick="navegar('tela-servicos')" class="btn-grande btn-secundario">📋 VER SERVIÇOS</button>
                <button onclick="alert('Transferindo...')" class="btn-grande btn-terciario">👤 FALAR COM PESSOA</button>
            </div>
        </div>

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
                    <span class="emoji">🧔</span>
                    <div class="info"><strong>Barba Completa</strong><span class="detalhes">R$ 25,00</span></div>
                </div>
            </div>
        </div>

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

        <div id="tela-calendario" class="tela">
            <div class="header-simples">
                <button onclick="navegar('tela-data')" class="btn-voltar">← Voltar</button>
                <h2>Selecione a Data</h2>
            </div>
            <div class="calendario-wrapper">
                <div class="calendario-header">
                    <button onclick="mudarMes(-1)" class="btn-nav-cal">◀</button>
                    <span id="mes-ano-cal"></span>
                    <button onclick="mudarMes(1)" class="btn-nav-cal">▶</button>
                </div>
                <div class="calendario-semanas">
                    <div>Dom</div><div>Seg</div><div>Ter</div><div>Qua</div><div>Qui</div><div>Sex</div><div>Sáb</div>
                </div>
                <div class="calendario-dias" id="calendario-dias"></div>
            </div>
        </div>

        <div id="tela-horario" class="tela">
            <div class="header-simples">
                <button onclick="navegar('tela-data')" class="btn-voltar">← Voltar</button>
                <h2>Horários Disponíveis</h2>
            </div>
            <p class="texto-orientacao">Para: <span id="data-escolhida" class="destaque-texto">...</span></p>
            <div class="lista-horarios">
                <button class="btn-slot" onclick="selecionarHora('14:00')">🕐 14:00</button>
                <button class="btn-slot" onclick="selecionarHora('14:30')">🕑 14:30</button>
                <button class="btn-slot" onclick="selecionarHora('15:00')">🕒 15:00</button>
                <button class="btn-slot" onclick="selecionarHora('15:30')">🕓 15:30</button>
            </div>
        </div>

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

        <div id="tela-sucesso" class="tela">
            <div class="header-sucesso">
                <span class="emoji-grande">🎉</span>
                <h2>Agendado com Sucesso!</h2>
            </div>
            <div class="card-resumo">
                <p>👤 <span id="resumo-nome">...</span></p>
                <p>✂️ <span id="resumo-servico">...</span></p>
                <p>📅 <span id="resumo-data">...</span></p>
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

CSS_CODE = """:root {
    --cor-primaria: #2563eb;
    --cor-fundo: #f1f5f9;
    --cor-cartao: #ffffff;
    --cor-texto: #0f172a;
    --borda-raio: 12px;
}
* { margin: 0; padding: 0; box-sizing: border-box; font-family: system-ui, sans-serif; }
body { background-color: var(--cor-fundo); display: flex; justify-content: center; min-height: 100vh; }
#app-container { background-color: var(--cor-cartao); width: 100%; max-width: 480px; min-height: 100vh; position: relative; overflow: hidden; box-shadow: 0 0 20px rgba(0,0,0,0.1); padding: 20px; }
.tela { display: none; animation: fadeIn 0.3s ease; }
.tela.ativa { display: block; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
.box-empresa { text-align: center; background: #eff6ff; padding: 20px; border-radius: var(--borda-raio); margin-bottom: 20px; border: 2px solid #dbeafe; }
.box-empresa h1 { font-size: 24px; color: #1e3a8a; font-weight: 800; margin-bottom: 5px; }
.subtitulo-empresa { font-size: 14px; color: #64748b; text-transform: uppercase; letter-spacing: 1px; }
.row-bot-info { display: flex; gap: 15px; align-items: center; margin-bottom: 25px; }
.box-foto-bot { width: 80px; height: 80px; border-radius: 50%; overflow: hidden; border: 3px solid var(--cor-primaria); flex-shrink: 0; background: #fff; }
.box-foto-bot img { width: 100%; height: 100%; object-fit: cover; }
.box-msg-bot { flex: 1; background: #f8fafc; padding: 15px; border-radius: var(--borda-raio); border-left: 4px solid var(--cor-primaria); }
.box-msg-bot p { font-size: 14px; color: #334155; line-height: 1.4; font-style: italic; }
.box-orientacao { background: #fff; padding: 15px; border-radius: var(--borda-raio); border: 1px dashed #cbd5e1; margin-bottom: 15px; text-align: center; }
.box-orientacao strong { display: block; font-size: 16px; color: var(--cor-texto); margin-bottom: 5px; }
.box-orientacao small { color: #64748b; font-size: 12px; }
.box-input-nome input { width: 100%; padding: 18px; font-size: 18px; border: 2px solid #cbd5e1; border-radius: var(--borda-raio); text-align: center; transition: 0.3s; }
.box-input-nome input:focus { border-color: var(--cor-primaria); outline: none; box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.1); }
.header-box { text-align: center; padding: 30px 0; background: #eff6ff; border-radius: var(--borda-raio); margin-bottom: 20px; }
.header-simples { display: flex; align-items: center; gap: 10px; margin-bottom: 20px; }
#nome-cliente-destaque { font-size: 28px; font-weight: 800; color: #1e3a8a; margin-bottom: 5px; }
.btn-grande { width: 100%; padding: 16px; font-size: 16px; font-weight: bold; border: none; border-radius: var(--borda-raio); margin-bottom: 12px; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 10px; }
.btn-primario { background-color: var(--cor-primaria); color: white; box-shadow: 0 4px 6px rgba(37, 99, 235, 0.3); }
.btn-secundario { background-color: #e2e8f0; color: var(--cor-texto); }
.btn-terciario { background-color: #ffffff; border: 1px solid #cbd5e1; color: var(--cor-texto); }
.btn-voltar { background: none; border: none; font-size: 16px; color: var(--cor-primaria); cursor: pointer; font-weight: bold; }
.card-servico, .card-data { background: white; border: 1px solid #cbd5e1; border-radius: var(--borda-raio); padding: 15px; margin-bottom: 15px; display: flex; align-items: center; gap: 15px; cursor: pointer; }
.card-servico:active, .card-data:active { transform: scale(0.98); background-color: #f8fafc; }
.calendario-wrapper { background: #fff; padding: 15px; border-radius: var(--borda-raio); border: 1px solid #cbd5e1; margin-bottom: 20px; }
.calendario-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
#mes-ano-cal { font-weight: bold; font-size: 18px; text-transform: capitalize; }
.btn-nav-cal { background: #eff6ff; border: none; font-size: 18px; cursor: pointer; color: var(--cor-primaria); padding: 8px 12px; border-radius: 8px; }
.btn-nav-cal:active { background: #dbeafe; }
.calendario-semanas { display: grid; grid-template-columns: repeat(7, 1fr); text-align: center; margin-bottom: 8px; }
.calendario-semanas div { font-weight: bold; color: #64748b; font-size: 12px; padding: 5px 0; }
.calendario-dias { display: grid; grid-template-columns: repeat(7, 1fr); gap: 6px; }
.dia-cal { padding: 12px 0; text-align: center; border-radius: 8px; cursor: pointer; font-weight: 500; transition: 0.2s; }
.dia-cal:hover { background-color: #eff6ff; }
.dia-cal.selecionado { background-color: var(--cor-primaria); color: white; font-weight: bold; }
.dia-cal.hoje { border: 2px solid var(--cor-primaria); }
.dia-cal.vazio { cursor: default; }
.dia-cal.vazio:hover { background: transparent; }
.lista-horarios { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.btn-slot { padding: 15px; background: white; border: 1px solid var(--cor-primaria); border-radius: var(--borda-raio); color: var(--cor-primaria); font-weight: bold; cursor: pointer; font-size: 16px; }
.btn-slot:active { background: var(--cor-primaria); color: white; }
.input-group { margin-bottom: 20px; }
.input-group label { display: block; margin-bottom: 8px; font-weight: bold; color: var(--cor-texto); }
.input-group input { width: 100%; padding: 15px; font-size: 18px; border: 2px solid #cbd5e1; border-radius: var(--borda-raio); text-align: center; }
.input-group input:focus { border-color: var(--cor-primaria); outline: none; }
.header-sucesso { text-align: center; margin-bottom: 30px; }
.emoji-grande { font-size: 60px; display: block; margin-bottom: 10px; }
.card-resumo { background: #f0f9ff; padding: 20px; border-radius: var(--borda-raio); margin-bottom: 30px; text-align: left; border: 1px solid #bae6fd; }
.card-resumo p { margin-bottom: 8px; font-size: 16px; color: #334155; }
.texto-orientacao { text-align: center; color: #64748b; margin-bottom: 20px; }
.destaque-texto { color: var(--cor-primaria); font-weight: bold; }
"""

JS_CODE = """let dadosAgendamento = { nome: "", servico: "", data: "", hora: "", telefone: "" };
let mesAtual = new Date().getMonth();
let anoAtual = new Date().getFullYear();

function formatarNome(nome) { return nome.replace(/\\b\\w/g, l => l.toUpperCase()); }

function navegar(idTela) {
    document.querySelectorAll('.tela').forEach(t => t.classList.remove('ativa'));
    document.getElementById(idTela).classList.add('ativa');
    if(idTela === 'tela-calendario') renderCalendario();
}

function iniciarSistema() {
    const nomeInput = document.getElementById('input-nome-cliente').value.trim();
    if (nomeInput.length < 3) { alert("Por favor, digite seu nome completo."); return; }
    dadosAgendamento.nome = formatarNome(nomeInput);
    document.getElementById('nome-cliente-destaque').innerText = dadosAgendamento.nome;
    navegar('tela-boas-vindas');
}

function selecionarServico(nome) {
    dadosAgendamento.servico = nome;
    document.getElementById('servico-escolhido').innerText = nome;
    navegar('tela-data');
}

function selecionarData(opcao) {
    if (opcao === 'Outro Dia') { navegar('tela-calendario'); }
    else {
        dadosAgendamento.data = opcao;
        document.getElementById('data-escolhida').innerText = `📅 ${opcao}`;
        navegar('tela-horario');
    }
}

function renderCalendario() {
    const container = document.getElementById('calendario-dias');
    container.innerHTML = '';
    const nomeMes = new Date(anoAtual, mesAtual).toLocaleDateString('pt-BR', { month: 'long', year: 'numeric' });
    document.getElementById('mes-ano-cal').innerText = nomeMes;
    const primeiroDia = new Date(anoAtual, mesAtual, 1).getDay();
    const diasNoMes = new Date(anoAtual, mesAtual + 1, 0).getDate();
    const hoje = new Date();
    for (let i = 0; i < primeiroDia; i++) {
        const vazio = document.createElement('div');
        vazio.className = 'dia-cal vazio';
        container.appendChild(vazio);
    }
    for (let d = 1; d <= diasNoMes; d++) {
        const diaEl = document.createElement('div');
        diaEl.className = 'dia-cal';
        diaEl.innerText = d;
        if (d === hoje.getDate() && mesAtual === hoje.getMonth() && anoAtual === hoje.getFullYear()) {
            diaEl.classList.add('hoje');
        }
        diaEl.onclick = () => selecionarDia(d, diaEl);
        container.appendChild(diaEl);
    }
}

function mudarMes(delta) {
    mesAtual += delta;
    if (mesAtual > 11) { mesAtual = 0; anoAtual++; }
    if (mesAtual < 0) { mesAtual = 11; anoAtual--; }
    renderCalendario();
}

function selecionarDia(dia, elemento) {
    const diaFmt = dia.toString().padStart(2, '0');
    const mesFmt = (mesAtual + 1).toString().padStart(2, '0');
    dadosAgendamento.data = `${diaFmt}/${mesFmt}/${anoAtual}`;
    document.querySelectorAll('.dia-cal').forEach(el => el.classList.remove('selecionado'));
    elemento.classList.add('selecionado');
    setTimeout(() => {
        document.getElementById('data-escolhida').innerText = `📅 ${dadosAgendamento.data}`;
        navegar('tela-horario');
    }, 300);
}

function selecionarHora(hora) { dadosAgendamento.hora = hora; navegar('tela-whatsapp'); }

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

# Atualizar arquivos
arquivos = {
    "index.html": HTML_CODE,
    "style.css": CSS_CODE,
    "script.js": JS_CODE
}

print("🔄 Atualizando sistema...")
for nome, codigo in arquivos.items():
    caminho = PASTA / nome
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(codigo)
    print(f"✅ {nome} atualizado")

print("\n🎉 Sistema atualizado com sucesso!")
print("📂 Arquivos em:", PASTA)

# Abrir no navegador
webbrowser.open(f"file:///{(PASTA / 'index.html').as_posix()}")
print("🌐 Abrindo no navegador...")