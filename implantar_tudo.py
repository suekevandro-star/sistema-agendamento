#!/usr/bin/env python3
"""
IMPLANTAR_TUDO_FINAL.py - A Versão Definitiva
Atualiza todos os arquivos do projeto com TODAS as melhorias planejadas:
- Tema Dark/Light
- Destaques visuais (Bella em Roxo)
- Fluxo de Turno (Dia/Noite)
- Meus Agendamentos com persistência
- Painel com sliders visuais
"""

from pathlib import Path
import json

PASTA = Path(r"D:\Projeto Empresas")

# ==========================================
# 1. INDEX.HTML (Completo e Atualizado)
# ==========================================
INDEX_HTML = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Clínica Sorriso - Atendimento Virtual</title>
    <link rel="stylesheet" href="style.css">
    <link rel="stylesheet" href="configuracoes_bot.css?v=5">
</head>
<body>
    <div id="app-container">

        <!-- TELA 0: ENTRADA -->
        <div id="tela-entrada" class="tela ativa">
            <!-- Botão Tema -->
            <button onclick="alternarTema()" id="btn-tema" class="btn-flutuante">🌙</button>
            
            <div class="box-empresa">
                <h1 id="nome-empresa-display">Clínica <span class="destaque-nome">SORRISO</span></h1>
                <span class="subtitulo-empresa">Assistente Virtual</span>
            </div>
            <div class="row-bot-info">
                <div class="box-foto-bot">
                    <img src="bot.png" alt="Bella" onerror="this.src='https://ui-avatars.com/api/?name=Bella&background=8b5cf6&color=fff&size=150'">
                </div>
                <div class="box-msg-bot">
                    <p class="msg-bot-principal">"OLÁ! BEM-VINDO(A)!<br>EU SOU A <span class="destaque-bella">BELLA</span>, SUA ASSISTENTE VIRTUAL."</p>
                    <p class="msg-bot-secundaria">Para começarmos, qual é o seu nome completo?</p>
                </div>
            </div>
            <div class="box-orientacao">
                <strong>DIGITE SEU NOME ABAIXO</strong>
            </div>
            <div class="box-input-nome">
                <input type="text" id="input-nome-cliente" placeholder="Seu nome aqui..." autocomplete="name">
            </div>
            <button onclick="iniciarSistema()" class="btn-grande btn-primario">✅ CONTINUAR</button>
        </div>

        <!-- TELA 1: BOAS-VINDAS -->
        <div id="tela-boas-vindas" class="tela">
            <div class="header-box">
                <h1>Olá, <span id="nome-cliente-destaque">...</span>!</h1>
                <p class="msg-intro">Como posso ajudar você hoje?</p>
            </div>
            <!-- Botão Condicional de Agendamentos -->
            <button id="btn-meus-agendamentos" onclick="navegar('tela-agendamentos')" class="btn-grande btn-terciario" style="display: none;">
                 VER MEUS AGENDAMENTOS
            </button>
            <div class="botoes-acao">
                <button onclick="navegar('tela-servicos')" class="btn-grande btn-primario">📅 AGENDAR AGORA</button>
                <button onclick="navegar('tela-servicos')" class="btn-grande btn-secundario">📋 SERVIÇOS</button>
                <button onclick="alert('Transfira para humano...')" class="btn-grande btn-terciario">👤 ATENDENTE</button>
            </div>
        </div>

        <!-- TELA 2: SERVIÇOS -->
        <div id="tela-servicos" class="tela">
            <div class="header-simples">
                <button onclick="navegar('tela-boas-vindas')" class="btn-voltar">← Voltar</button>
                <h2>Nossos <span class="destaque-nome">SERVIÇOS</span></h2>
            </div>
            <div class="lista-servicos">
                <div class="card-servico" onclick="selecionarServico('Corte Masculino')">
                    <span class="emoji">✂️</span>
                    <div class="info"><strong>Corte Masculino</strong><span class="detalhes">R$ 35,00</span></div>
                </div>
                <div class="card-servico" onclick="selecionarServico('Barba Completa')">
                    <span class="emoji">🧔</span>
                    <div class="info"><strong>Barba Completa</strong><span class="detalhes">R$ 25,00</span></div>
                </div>
            </div>
        </div>

        <!-- TELA 3: DATA -->
        <div id="tela-data" class="tela">
            <div class="header-simples">
                <button onclick="navegar('tela-servicos')" class="btn-voltar">← Voltar</button>
                <h2>Escolha o Dia</h2>
            </div>
            <div class="lista-datas">
                <div class="card-data" onclick="selecionarData('Hoje, Segunda')">
                    <span class="emoji">📆</span>
                    <div class="info"><strong>HOJE</strong><span class="detalhes">Segunda-feira</span></div>
                </div>
                <div class="card-data" onclick="selecionarData('Amanhã, Terça')">
                    <span class="emoji"></span>
                    <div class="info"><strong>AMANHÃ</strong><span class="detalhes">Terça-feira</span></div>
                </div>
                <div class="card-data" onclick="selecionarData('Outro Dia')">
                    <span class="emoji">️</span>
                    <div class="info"><strong>OUTRO DIA</strong><span class="detalhes">Calendário</span></div>
                </div>
            </div>
        </div>

        <!-- TELA 4: CALENDÁRIO -->
        <div id="tela-calendario" class="tela">
            <div class="header-simples">
                <button onclick="navegar('tela-data')" class="btn-voltar">← Voltar</button>
                <h2>Calendário</h2>
            </div>
            <div class="calendario-wrapper">
                <div class="calendario-header">
                    <button onclick="mudarMes(-1)" class="btn-nav-cal"></button>
                    <span id="mes-ano-cal"></span>
                    <button onclick="mudarMes(1)" class="btn-nav-cal">▶</button>
                </div>
                <div class="calendario-semanas"><div>D</div><div>S</div><div>T</div><div>Q</div><div>Q</div><div>S</div><div>S</div></div>
                <div class="calendario-dias" id="calendario-dias"></div>
            </div>
        </div>

        <!-- TELA 5: TURNO (NOVA) -->
        <div id="tela-turno" class="tela">
            <div class="header-simples">
                <button onclick="navegar('tela-data')" class="btn-voltar">← Voltar</button>
                <h2>Qual período prefere?</h2>
            </div>
            <p class="texto-orientacao">Para: <span id="turno-data-display" class="destaque-texto">...</span></p>
            <div class="grid-turnos">
                <button onclick="selecionarTurno('dia')" class="card-turno dia">
                    <span class="emoji-grande"></span>
                    <strong>DIA</strong>
                    <small>09:00 às 18:00</small>
                </button>
                <button onclick="selecionarTurno('noite')" class="card-turno noite">
                    <span class="emoji-grande">🌙</span>
                    <strong>NOITE</strong>
                    <small>18:00 às 21:00</small>
                </button>
            </div>
        </div>

        <!-- TELA 6: HORÁRIO -->
        <div id="tela-horario" class="tela">
            <div class="header-simples">
                <button onclick="navegar('tela-turno')" class="btn-voltar">← Voltar</button>
                <h2>Horários (<span id="turno-atual-display">Dia</span>)</h2>
            </div>
            <p class="texto-orientacao">Escolha um horário:</p>
            <div class="lista-horarios" id="lista-horarios-dinamica">
                <!-- Preenchido via JS -->
            </div>
        </div>

        <!-- TELA 7: WHATSAPP -->
        <div id="tela-whatsapp" class="tela">
            <div class="header-simples">
                <button onclick="navegar('tela-horario')" class="btn-voltar">← Voltar</button>
                <h2>Confirmar</h2>
            </div>
            <div class="input-group">
                <label>Seu WhatsApp:</label>
                <input type="tel" id="input-telefone" placeholder="(XX) 9XXXX-XXXX" oninput="mascararTelefone(this)">
            </div>
            <button onclick="confirmarAgendamento()" class="btn-grande btn-primario">✅ FINALIZAR</button>
        </div>

        <!-- TELA 8: SUCESSO -->
        <div id="tela-sucesso" class="tela">
            <div class="header-sucesso">
                <span class="emoji-grande"></span>
                <h2>AGENDADO COM SUCESSO!</h2>
            </div>
            <div class="card-resumo">
                <p>👤 <span id="resumo-nome">...</span></p>
                <p>✂️ <span class="destaque-nome" id="resumo-servico">...</span></p>
                <p>📅 <span id="resumo-data">...</span></p>
                <p> <span id="resumo-hora">...</span></p>
            </div>
            
            <button onclick="reagendarAgora()" class="btn-grande btn-secundario">📅 REAGENDAR</button>
            <button onclick="cancelarAgora()" class="btn-grande btn-cancelar">❌ CANCELAR</button>
            <button onclick="window.location.reload()" class="btn-grande btn-terciario">🏠 INÍCIO</button>
        </div>

        <!-- TELA 9: MEUS AGENDAMENTOS -->
        <div id="tela-agendamentos" class="tela">
            <div class="header-simples">
                <button onclick="navegar('tela-boas-vindas')" class="btn-voltar">← Voltar</button>
                <h2>Meus Agendamentos</h2>
            </div>
            <div id="lista-agendamentos"></div>
            <div id="msg-sem-agendamento" style="display:none; text-align:center; padding:40px 0;">
                <span class="emoji-grande">📭</span>
                <p>Nenhum agendamento encontrado.</p>
                <button onclick="navegar('tela-servicos')" class="btn-grande btn-primario" style="margin-top:15px;">FAZER AGENDAMENTO</button>
            </div>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

# ==========================================
# 2. STYLE.CSS (Completo)
# ==========================================
STYLE_CSS = """:root {
    --cor-primaria: #2563eb;
    --cor-secundaria: #8b5cf6;
    --cor-fundo: #f1f5f9;
    --cor-cartao: #ffffff;
    --cor-texto: #0f172a;
    --cor-texto-light: #64748b;
    --borda: #e2e8f0;
    --sombra: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

body.modo-escuro {
    --cor-primaria: #3b82f6;
    --cor-secundaria: #a78bfa;
    --cor-fundo: #0f172a;
    --cor-cartao: #1e293b;
    --cor-texto: #f8fafc;
    --cor-texto-light: #94a3b8;
    --borda: #334155;
    --sombra: 0 4px 20px rgba(0, 0, 0, 0.5);
}

* { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', system-ui, sans-serif; }
body { background: var(--cor-fundo); color: var(--cor-texto); min-height: 100vh; display: flex; justify-content: center; transition: background 0.3s, color 0.3s; }
#app-container { width: 100%; max-width: 480px; background: var(--cor-cartao); min-height: 100vh; padding: 20px; box-shadow: var(--sombra); position: relative; transition: background 0.3s; }
.tela { display: none; animation: fadeIn 0.3s; }
.tela.ativa { display: block; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

/* Botão Tema */
.btn-flutuante { position: absolute; top: 20px; right: 20px; background: var(--cor-cartao); border: 1px solid var(--borda); border-radius: 50%; width: 40px; height: 40px; font-size: 20px; cursor: pointer; z-index: 10; box-shadow: var(--sombra); display: flex; align-items: center; justify-content: center; }

/* Destaques */
.destaque-nome { color: var(--cor-primaria); font-weight: 800; }
.destaque-bella { background: linear-gradient(135deg, #8b5cf6, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; }

/* Layout Geral */
.box-empresa { text-align: center; padding: 20px; background: linear-gradient(to bottom, #eff6ff, transparent); border-radius: 16px; margin-bottom: 20px; }
.box-empresa h1 { font-size: 24px; color: var(--cor-texto); }
.row-bot-info { display: flex; gap: 15px; align-items: center; margin-bottom: 20px; }
.box-foto-bot { width: 80px; height: 80px; border-radius: 50%; overflow: hidden; border: 3px solid var(--cor-secundaria); flex-shrink: 0; background: white; }
.box-foto-bot img { width: 100%; height: 100%; object-fit: cover; }
.box-msg-bot { flex: 1; background: var(--cor-fundo); padding: 15px; border-radius: 12px; border-left: 4px solid var(--cor-secundaria); }
.msg-bot-principal { font-weight: 700; color: var(--cor-primaria); text-transform: uppercase; font-size: 12px; line-height: 1.4; }
.msg-bot-secundaria { margin-top: 5px; color: var(--cor-texto-light); font-size: 13px; }

/* Inputs e Botões */
.btn-grande { width: 100%; padding: 16px; border-radius: 12px; border: none; font-weight: 700; font-size: 15px; cursor: pointer; margin-bottom: 10px; transition: transform 0.1s; }
.btn-grande:active { transform: scale(0.98); }
.btn-primario { background: var(--cor-primaria); color: white; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3); }
.btn-secundario { background: var(--cor-fundo); color: var(--cor-texto); border: 1px solid var(--borda); }
.btn-terciario { background: white; color: var(--cor-texto); border: 1px solid var(--borda); }
.btn-cancelar { background: #fee2e2; color: #b91c1c; border: 1px solid #fca5a5; }
input { width: 100%; padding: 15px; border-radius: 12px; border: 1px solid var(--borda); background: var(--cor-fundo); color: var(--cor-texto); font-size: 16px; }
input:focus { outline: none; border-color: var(--cor-primaria); }

/* Turnos */
.grid-turnos { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 20px; }
.card-turno { background: white; border: 2px solid var(--borda); border-radius: 16px; padding: 20px; text-align: center; cursor: pointer; transition: 0.2s; }
.card-turno.dia:hover { border-color: #f59e0b; background: #fffbeb; }
.card-turno.noite:hover { border-color: #3b82f6; background: #eff6ff; }
.emoji-grande { font-size: 40px; display: block; margin-bottom: 10px; }

/* Cards Serviços/Dados */
.card-servico, .card-data { display: flex; align-items: center; gap: 15px; background: white; padding: 15px; border-radius: 12px; border: 1px solid var(--borda); margin-bottom: 12px; cursor: pointer; }
.card-servico:hover { border-color: var(--cor-primaria); }
.emoji { font-size: 24px; }
.info { flex: 1; }
.info strong { display: block; color: var(--cor-texto); }
.detalhes { font-size: 12px; color: var(--cor-texto-light); }

/* Calendário */
.calendario-wrapper { background: white; padding: 15px; border-radius: 12px; border: 1px solid var(--borda); }
.calendario-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; font-weight: bold; }
.btn-nav-cal { background: var(--cor-fundo); border: none; padding: 5px 10px; border-radius: 6px; cursor: pointer; color: var(--cor-texto); }
.calendario-semanas { display: grid; grid-template-columns: repeat(7, 1fr); text-align: center; font-weight: bold; font-size: 12px; margin-bottom: 10px; color: var(--cor-texto-light); }
.calendario-dias { display: grid; grid-template-columns: repeat(7, 1fr); gap: 5px; }
.dia-cal { padding: 10px; text-align: center; border-radius: 8px; cursor: pointer; font-size: 14px; }
.dia-cal:hover { background: var(--cor-fundo); }
.dia-cal.selecionado { background: var(--cor-primaria); color: white; }

/* Horários */
.lista-horarios { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
.btn-slot { padding: 12px; background: white; border: 1px solid var(--borda); border-radius: 8px; cursor: pointer; font-weight: 600; color: var(--cor-texto); }
.btn-slot:hover { border-color: var(--cor-primaria); color: var(--cor-primaria); }

/* Resumo e Agendamentos */
.card-resumo { background: var(--cor-fundo); padding: 20px; border-radius: 12px; margin-bottom: 20px; }
.card-resumo p { margin-bottom: 8px; font-size: 15px; border-bottom: 1px dashed var(--borda); padding-bottom: 5px; }
.card-agendamento { background: white; border-left: 4px solid var(--cor-secundaria); padding: 15px; border-radius: 8px; margin-bottom: 10px; box-shadow: var(--sombra); }

/* Modo Escuro Ajustes */
body.modo-escuro .card-turno { background: var(--cor-cartao); }
body.modo-escuro .card-turno.dia:hover { background: #422006; border-color: #f59e0b; }
body.modo-escuro .card-turno.noite:hover { background: #172554; border-color: #3b82f6; }
body.modo-escuro .card-servico, body.modo-escuro .card-data { background: var(--cor-cartao); }
body.modo-escuro .calendario-wrapper { background: var(--cor-cartao); }
body.modo-escuro .dia-cal:hover { background: #334155; }
body.modo-escuro .btn-slot { background: var(--cor-cartao); }
body.modo-escuro .btn-flutuante { background: var(--cor-cartao); border-color: var(--borda); }
"""

# ==========================================
# 3. SCRIPT.JS (Completo)
# ==========================================
SCRIPT_JS = r"""// Configurações Globais
let temaAtual = localStorage.getItem('tema-sistema') || 'claro';
let dadosAgendamento = {};
let agendamentosDoCliente = JSON.parse(localStorage.getItem('meus_agendamentos')) || [];
let turnoEscolhido = '';
let mesAtual = new Date().getMonth();
let anoAtual = new Date().getFullYear();

const horariosPorTurno = {
    'dia': ['09:00', '10:00', '11:00', '14:00', '15:00', '16:00', '17:00'],
    'noite': ['18:00', '18:30', '19:00', '19:30', '20:00']
};

// Inicialização
window.onload = function() {
    if (temaAtual === 'escuro') {
        document.body.classList.add('modo-escuro');
        document.getElementById('btn-tema').innerText = '☀️';
    }
    verificarAgendamentos();
};

// Navegação
function navegar(idTela) {
    document.querySelectorAll('.tela').forEach(t => t.classList.remove('ativa'));
    document.getElementById(idTela).classList.add('ativa');
    
    if (idTela === 'tela-calendario') renderCalendario();
    if (idTela === 'tela-boas-vindas') verificarAgendamentos();
}

// Tema
function alternarTema() {
    document.body.classList.toggle('modo-escuro');
    const btn = document.getElementById('btn-tema');
    const isDark = document.body.classList.contains('modo-escuro');
    btn.innerText = isDark ? '☀️' : '';
    localStorage.setItem('tema-sistema', isDark ? 'escuro' : 'claro');
}

// Lógica do Sistema
function iniciarSistema() {
    const nome = document.getElementById('input-nome-cliente').value.trim();
    if (nome.length < 3) return alert('Digite seu nome completo');
    dadosAgendamento.nome = nome;
    document.getElementById('nome-cliente-destaque').innerText = nome;
    navegar('tela-boas-vindas');
}

function selecionarServico(servico) {
    dadosAgendamento.servico = servico;
    navegar('tela-data');
}

function selecionarData(opcao) {
    if (opcao === 'Outro Dia') { navegar('tela-calendario'); return; }
    dadosAgendamento.data = opcao;
    document.getElementById('turno-data-display').innerText = opcao;
    navegar('tela-turno');
}

function selecionarTurno(turno) {
    turnoEscolhido = turno;
    document.getElementById('turno-atual-display').innerText = turno === 'dia' ? 'Dia ' : 'Noite 🌙';
    const lista = document.getElementById('lista-horarios-dinamica');
    lista.innerHTML = '';
    horariosPorTurno[turno].forEach(hora => {
        const btn = document.createElement('button');
        btn.className = 'btn-slot';
        btn.innerText = hora;
        btn.onclick = () => selecionarHora(hora);
        lista.appendChild(btn);
    });
    navegar('tela-horario');
}

function selecionarHora(hora) {
    dadosAgendamento.hora = hora;
    navegar('tela-whatsapp');
}

function mascararTelefone(input) {
    let v = input.value.replace(/\D/g, "").slice(0, 11);
    v = v.replace(/^(\d{2})(\d)/g, "($1) $2");
    v = v.replace(/(\d)(\d{4})$/, "$1-$2");
    input.value = v;
}

function confirmarAgendamento() {
    const tel = document.getElementById('input-telefone').value;
    if (tel.length < 14) return alert('Telefone inválido');
    
    dadosAgendamento.telefone = tel;
    dadosAgendamento.turno = turnoEscolhido;
    
    // Salvar na lista
    agendamentosDoCliente.push({...dadosAgendamento, status: 'Confirmado'});
    localStorage.setItem('meus_agendamentos', JSON.stringify(agendamentosDoCliente));
    
    // Atualizar Tela de Sucesso
    document.getElementById('resumo-nome').innerText = dadosAgendamento.nome;
    document.getElementById('resumo-servico').innerText = dadosAgendamento.servico;
    document.getElementById('resumo-data').innerText = dadosAgendamento.data;
    document.getElementById('resumo-hora').innerText = `${dadosAgendamento.hora} (${turnoEscolhido === 'dia' ? 'Dia' : 'Noite'})`;
    
    navegar('tela-sucesso');
}

// Agendamentos e Cancelamentos
function verificarAgendamentos() {
    const btn = document.getElementById('btn-meus-agendamentos');
    const listaDiv = document.getElementById('lista-agendamentos');
    const msgDiv = document.getElementById('msg-sem-agendamento');
    
    if (agendamentosDoCliente.length > 0) {
        btn.style.display = 'block';
        listaDiv.style.display = 'block';
        msgDiv.style.display = 'none';
        
        listaDiv.innerHTML = agendamentosDoCliente.map((ag, index) => `
            <div class="card-agendamento">
                <strong>${ag.servico}</strong>
                <div>${ag.data} às ${ag.hora}</div>
                <div style="font-size:12px; color:var(--cor-texto-light); margin-top:5px;">${ag.nome}</div>
                <button onclick="cancelarItem(${index})" style="background:#fee2e2; color:#b91c1c; border:none; padding:5px 10px; border-radius:6px; margin-top:5px; font-size:12px; cursor:pointer;">Cancelar</button>
            </div>
        `).join('');
    } else {
        btn.style.display = 'none';
        listaDiv.style.display = 'none';
        msgDiv.style.display = 'block';
    }
}

function cancelarItem(index) {
    if(confirm('Cancelar este agendamento?')) {
        agendamentosDoCliente.splice(index, 1);
        localStorage.setItem('meus_agendamentos', JSON.stringify(agendamentosDoCliente));
        verificarAgendamentos();
    }
}

function cancelarAgora() {
    if(confirm('Tem certeza?')) {
        agendamentosDoCliente.pop(); // Remove o último
        localStorage.setItem('meus_agendamentos', JSON.stringify(agendamentosDoCliente));
        alert('Cancelado.');
        window.location.reload();
    }
}

function reagendarAgora() {
    agendamentosDoCliente.pop(); // Remove o último para fazer outro
    localStorage.setItem('meus_agendamentos', JSON.stringify(agendamentosDoCliente));
    navegar('tela-servicos');
}

// Calendário
function renderCalendario() {
    const container = document.getElementById('calendario-dias');
    container.innerHTML = '';
    document.getElementById('mes-ano-cal').innerText = new Date(anoAtual, mesAtual).toLocaleDateString('pt-BR', {month:'long', year:'numeric'});
    
    const firstDay = new Date(anoAtual, mesAtual, 1).getDay();
    const daysInMonth = new Date(anoAtual, mesAtual + 1, 0).getDate();
    
    for(let i=0; i<firstDay; i++) container.innerHTML += '<div></div>';
    
    for(let d=1; d<=daysInMonth; d++) {
        const el = document.createElement('div');
        el.className = 'dia-cal';
        el.innerText = d;
        el.onclick = () => {
            document.querySelectorAll('.dia-cal').forEach(e => e.classList.remove('selecionado'));
            el.classList.add('selecionado');
            dadosAgendamento.data = `${d}/${mesAtual+1}/${anoAtual}`;
            document.getElementById('turno-data-display').innerText = dadosAgendamento.data;
            setTimeout(() => navegar('tela-turno'), 200);
        };
        container.appendChild(el);
    }
}
function mudarMes(d) { mesAtual += d; if(mesAtual>11){mesAtual=0; anoAtual++;} if(mesAtual<0){mesAtual=11; anoAtual--;} renderCalendario(); }
"""

# ==========================================
# 4. PAINEL.HTML (Com Sliders)
# ==========================================
PAINEL_HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Painel Administrativo</title>
    <link rel="stylesheet" href="style.css">
    <style>
        body { background: #f1f5f9; }
        .painel-wrap { max-width: 1000px; margin: 30px auto; background: white; border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); overflow: hidden; }
        .painel-header { background: linear-gradient(135deg, #2563eb, #8b5cf6); color: white; padding: 30px; text-align: center; }
        .painel-header h1 { margin: 0; font-size: 28px; }
        .tabs { display: flex; background: #f8fafc; border-bottom: 1px solid #e2e8f0; }
        .tab-btn { flex: 1; padding: 15px; border: none; background: none; font-weight: 600; cursor: pointer; color: #64748b; transition: 0.2s; }
        .tab-btn:hover { background: #e2e8f0; }
        .tab-btn.ativo { background: white; color: #2563eb; border-bottom: 3px solid #2563eb; }
        .conteudo { padding: 30px; min-height: 400px; }
        .aba { display: none; }
        .aba.ativo { display: block; }
        
        /* Sliders Config */
        .config-card { background: #eff6ff; padding: 20px; border-radius: 12px; border: 1px solid #bfdbfe; margin-bottom: 20px; }
        .slider-group { margin-bottom: 20px; }
        .slider-group label { display: block; font-weight: bold; margin-bottom: 8px; color: #1e40af; }
        input[type=range] { width: 100%; cursor: pointer; }
        .preview-box { display: flex; align-items: center; justify-content: center; background: white; padding: 20px; border-radius: 8px; margin-top: 15px; border: 2px dashed #3b82f6; }
        .btn-salvar { background: #2563eb; color: white; border: none; padding: 12px 24px; border-radius: 8px; font-weight: bold; cursor: pointer; width: 100%; margin-top: 15px; }
        .btn-salvar:hover { background: #1d4ed8; }
    </style>
</head>
<body>
    <div class="painel-wrap">
        <header class="painel-header">
            <h1>⚙️ Painel Administrativo</h1>
            <p>Gerencie o sistema e o visual da Bella</p>
        </header>
        <div class="tabs">
            <button class="tab-btn ativo" onclick="mudarAba('agendamentos', this)">Agendamentos</button>
            <button class="tab-btn" onclick="mudarAba('atendimento', this)">Atendimento</button>
            <button class="tab-btn" onclick="mudarAba('profissionais', this)">Profissionais</button>
            <button class="tab-btn" onclick="mudarAba('servicos', this)">Serviços</button>
            <button class="tab-btn" onclick="mudarAba('configuracoes', this)">Configurações</button>
        </div>
        <div class="conteudo">
            <div id="agendamentos" class="aba ativo">
                <h2>📅 Lista de Agendamentos</h2>
                <p>Conectado ao banco <code>agenda.db</code> (Em breve)</p>
            </div>
            <div id="atendimento" class="aba">
                <h2>💬 Atendimento ao Vivo</h2>
                <p>Chat em tempo real com clientes.</p>
            </div>
            <div id="profissionais" class="aba">
                <h2>👨‍⚕️ Profissionais</h2>
                <p>Gestão de equipe e horários.</p>
            </div>
            <div id="servicos" class="aba">
                <h2>✂️ Catálogo de Serviços</h2>
                <p>Preços e durações.</p>
            </div>
            
            <!-- ABA CONFIGURAÇÕES -->
            <div id="configuracoes" class="aba">
                <h2>🎨 Aparência Visual</h2>
                <div class="config-card">
                    <div class="slider-group">
                        <label>📏 Tamanho da Foto: <span id="val-tamanho">100px</span></label>
                        <input type="range" id="slider-tamanho" min="60" max="160" value="100" oninput="atualizarPreview()">
                    </div>
                    <div class="slider-group">
                        <label>🔍 Zoom do Rosto: <span id="val-zoom">100%</span></label>
                        <input type="range" id="slider-zoom" min="80" max="150" value="100" oninput="atualizarPreview()">
                    </div>
                    
                    <div class="preview-box">
                        <div id="preview-bella" style="width:100px; height:100px; border-radius:50%; overflow:hidden; border:3px solid #2563eb; background:white;">
                            <img src="bot.png" id="img-preview" style="width:100%; height:100%; object-fit:cover; transform:scale(1); transition:0.3s;" onerror="this.src='https://ui-avatars.com/api/?name=Bella&background=8b5cf6&color=fff'">
                        </div>
                    </div>
                    <button class="btn-salvar" onclick="salvarCSS()">💾 Aplicar e Baixar CSS</button>
                </div>
            </div>
        </div>
    </div>
    <script>
        function mudarAba(id, btn) {
            document.querySelectorAll('.aba').forEach(a => a.classList.remove('ativo'));
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('ativo'));
            document.getElementById(id).classList.add('ativo');
            btn.classList.add('ativo');
        }

        function atualizarPreview() {
            const t = document.getElementById('slider-tamanho').value;
            const z = document.getElementById('slider-zoom').value;
            document.getElementById('val-tamanho').innerText = t + 'px';
            document.getElementById('val-zoom').innerText = z + '%';
            
            const prev = document.getElementById('preview-bella');
            const img = document.getElementById('img-preview');
            prev.style.width = t + 'px';
            prev.style.height = t + 'px';
            img.style.transform = `scale(${z/100})`;
        }

        function salvarCSS() {
            const t = document.getElementById('slider-tamanho').value;
            const z = document.getElementById('slider-zoom').value;
            
            const css = `
.box-foto-bot { width: ${t}px !important; height: ${t}px !important; border: 4px solid var(--cor-secundaria) !important; border-radius: 50% !important; overflow: hidden !important; }
.box-foto-bot img { width: 100% !important; height: 100% !important; object-fit: cover !important; transform: scale(${z/100}) !important; }
`;
            const blob = new Blob([css], {type: 'text/css'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'configuracoes_bot.css';
            a.click();
            
            // Salva preferencia
            localStorage.setItem('bella-tamanho', t);
            localStorage.setItem('bella-zoom', z);
            alert('CSS Baixado! Mova para a pasta do projeto.');
        }

        // Carrega valores salvos
        window.onload = () => {
            const t = localStorage.getItem('bella-tamanho');
            const z = localStorage.getItem('bella-zoom');
            if(t) { document.getElementById('slider-tamanho').value = t; atualizarPreview(); }
            if(z) { document.getElementById('slider-zoom').value = z; atualizarPreview(); }
        };
    </script>
</body>
</html>"""

# ==========================================
# 5. FUNÇÃO DE EXECUÇÃO
# ==========================================
def salvar(nome, conteudo):
    try:
        with open(PASTA / nome, 'w', encoding='utf-8') as f:
            f.write(conteudo)
        print(f"✅ {nome} atualizado!")
    except Exception as e:
        print(f"❌ Erro em {nome}: {e}")

def main():
    print("🚀 INICIANDO IMPLANTAÇÃO TOTAL...")
    print("="*40)
    salvar("index.html", INDEX_HTML)
    salvar("style.css", STYLE_CSS)
    salvar("script.js", SCRIPT_JS)
    salvar("painel.html", PAINEL_HTML)
    
    # Cria CSS base do bot vazio para não dar erro de 404 se não tiver sido gerado ainda
    salvar("configuracoes_bot.css", "/* Gerado pelo painel */")
    
    print("="*40)
    print("✨ SUCESSO! Tudo está atualizado.")
    print("1. Abra index.html para ver o novo visual.")
    print("2. Abra painel.html para configurar o zoom da Bella.")
    print("3. O sistema agora salva os agendamentos no navegador!")

if __name__ == "__main__":
    main()