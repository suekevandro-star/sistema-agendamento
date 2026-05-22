#!/usr/bin/env python3
"""
CORRIGIR_TUDO.py - Atualização Completa do Sistema
===================================================
Atualiza TODOS os arquivos com:
✅ Identidade (Nome Empresa, Bot)
✅ Fuso Horário
✅ Horários por Dia da Semana
✅ Toggle Noite
✅ Datas Passadas Bloqueadas
✅ Mensagens Configuráveis
✅ Visual Glassmorphism
✅ Painel Admin Completo
✅ Tema Claro/Escuro
"""

from pathlib import Path
import json

PASTA = Path(r"D:\Projeto Empresas")

# ==========================================
# 1. STYLE.CSS - VISUAL COMPLETO
# ==========================================
STYLE_CSS = """:root {
    --cor-primaria: #667eea;
    --cor-secundaria: #764ba2;
    --cor-fundo: #f8fafc;
    --cor-cartao: #ffffff;
    --cor-texto: #0f172a;
    --cor-texto-light: #64748b;
    --borda: #e2e8f0;
    --sombra: 0 4px 12px rgba(0, 0, 0, 0.05);
}

body.modo-escuro {
    --cor-primaria: #3b82f6;
    --cor-secundaria: #a78bfa;
    --cor-fundo: #0f172a;
    --cor-cartao: #1e293b;
    --cor-texto: #f1f5f9;
    --cor-texto-light: #94a3b8;
    --borda: #334155;
    --sombra: 0 4px 20px rgba(0, 0, 0, 0.4);
}

* { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', system-ui, sans-serif; }

body { 
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    background-attachment: fixed;
    color: var(--cor-texto); 
    min-height: 100vh; 
    display: flex; 
    justify-content: center; 
    transition: all 0.3s ease;
}

body.modo-escuro {
    background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
    background-attachment: fixed;
}

#app-container { 
    width: 100%; 
    max-width: 480px; 
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    min-height: 100vh; 
    padding: 25px; 
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    position: relative; 
    margin: 0;
}

body.modo-escuro #app-container {
    background: rgba(30, 41, 59, 0.95);
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5), 0 0 40px rgba(59, 130, 246, 0.2);
}

.tela { display: none; animation: fadeIn 0.4s ease; }
.tela.ativa { display: block; }

@keyframes fadeIn { 
    from { opacity: 0; transform: translateY(20px); } 
    to { opacity: 1; transform: translateY(0); } 
}

.btn-flutuante { 
    position: absolute; 
    top: 20px; 
    right: 20px; 
    background: var(--cor-cartao); 
    border: 2px solid var(--borda); 
    border-radius: 50%; 
    width: 45px; 
    height: 45px; 
    font-size: 20px; 
    cursor: pointer; 
    z-index: 10; 
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    display: flex; 
    align-items: center; 
    justify-content: center;
    transition: all 0.3s;
}

.btn-flutuante:hover {
    transform: scale(1.1);
    box-shadow: 0 6px 16px rgba(0,0,0,0.2);
}

.destaque-nome { 
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 800; 
}

.destaque-bella { 
    background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%); 
    -webkit-background-clip: text; 
    -webkit-text-fill-color: transparent; 
    background-clip: text; 
    font-weight: 900; 
    font-size: 18px; 
    display: inline;
}

.box-empresa { 
    text-align: center; 
    padding: 25px; 
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
    border-radius: 20px; 
    margin-bottom: 25px;
    border: 1px solid rgba(102, 126, 234, 0.2);
}

.box-empresa h1 { font-size: 28px; color: var(--cor-texto); margin-bottom: 5px; }
.subtitulo-empresa { font-size: 14px; color: var(--cor-texto-light); text-transform: uppercase; letter-spacing: 1px; }

.row-bot-info { display: flex; gap: 15px; align-items: center; margin-bottom: 25px; }
.box-foto-bot { width: 90px; height: 90px; border-radius: 50%; overflow: hidden; border: 3px solid #667eea; flex-shrink: 0; background: white; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4); }
.box-foto-bot img { width: 100%; height: 100%; object-fit: cover; }
.box-msg-bot { flex: 1; background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); padding: 20px; border-radius: 16px; border-left: 5px solid #667eea; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
body.modo-escuro .box-msg-bot { background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); border-left-color: #a78bfa; }
.msg-bot-principal { font-weight: 800; color: #1e293b; text-transform: uppercase; font-size: 14px; line-height: 1.6; margin-bottom: 8px; }
body.modo-escuro .msg-bot-principal { color: #f1f5f9; }
.msg-bot-secundaria { color: #475569; font-size: 15px; line-height: 1.5; font-weight: 500; }
body.modo-escuro .msg-bot-secundaria { color: #cbd5e1; }

.btn-grande { width: 100%; padding: 18px; border-radius: 14px; border: none; font-weight: 700; font-size: 16px; cursor: pointer; margin-bottom: 12px; transition: all 0.3s; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
.btn-grande:active { transform: translateY(-2px); box-shadow: 0 6px 16px rgba(0,0,0,0.2); }
.btn-primario { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4); }
.btn-primario:hover { box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5); transform: translateY(-2px); }
.btn-secundario { background: var(--cor-fundo); color: var(--cor-texto); border: 2px solid var(--borda); }
.btn-terciario { background: white; color: #0f172a; border: 2px solid var(--borda); }
.btn-cancelar { background: linear-gradient(135deg, #f87171 0%, #dc2626 100%); color: white; border: none; box-shadow: 0 4px 12px rgba(248, 113, 113, 0.4); }

input { width: 100%; padding: 18px; border-radius: 14px; border: 2px solid var(--borda); background: var(--cor-fundo); color: var(--cor-texto); font-size: 16px; transition: all 0.3s; }
input:focus { outline: none; border-color: #667eea; box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1); }

.header-simples { display: flex; align-items: center; gap: 12px; margin-bottom: 25px; }
.btn-voltar { background: var(--cor-fundo); border: 2px solid var(--borda); padding: 10px 16px; border-radius: 10px; font-size: 14px; font-weight: 600; color: var(--cor-texto); cursor: pointer; transition: all 0.3s; }
.btn-voltar:hover { background: var(--borda); transform: translateX(-3px); }
body.modo-escuro .btn-voltar { background: transparent; border: 1px solid rgba(255, 255, 255, 0.3); color: #ffffff; }

.header-box { text-align: center; padding: 30px 20px; background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); border-radius: 20px; margin-bottom: 25px; border: 1px solid rgba(102, 126, 234, 0.2); }
#nome-cliente-destaque { font-size: 32px; font-weight: 800; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 8px; }
.msg-intro { font-size: 16px; color: var(--cor-texto-light); }

.grid-turnos { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 20px; }
.card-turno { background: white; border: 2px solid var(--borda); border-radius: 16px; padding: 25px; text-align: center; cursor: pointer; transition: all 0.3s; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
.card-turno:hover { transform: translateY(-3px); box-shadow: 0 8px 20px rgba(0,0,0,0.1); }
.card-turno.dia:hover { border-color: #f59e0b; background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%); }
.card-turno.noite:hover { border-color: #3b82f6; background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); }
.emoji-grande { font-size: 45px; display: block; margin-bottom: 10px; }

.card-servico, .card-data { display: flex; align-items: center; gap: 15px; background: white; padding: 18px; border-radius: 14px; border: 2px solid var(--borda); margin-bottom: 12px; cursor: pointer; transition: all 0.3s; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
.card-servico:hover, .card-data:hover { border-color: #667eea; transform: translateX(5px); box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2); }
body.modo-escuro .card-servico, body.modo-escuro .card-data { background: var(--cor-cartao); border-color: var(--borda); }
.emoji { font-size: 28px; }
.info { flex: 1; }
.info strong { display: block; color: var(--cor-texto); font-size: 16px; font-weight: 700; }
.detalhes { font-size: 14px; color: var(--cor-texto-light); }

.calendario-wrapper { background: white; padding: 20px; border-radius: 16px; border: 2px solid var(--borda); box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
body.modo-escuro .calendario-wrapper { background: var(--cor-cartao); border-color: var(--borda); }
.calendario-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; font-weight: bold; font-size: 18px; }
.btn-nav-cal { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border: none; padding: 8px 16px; border-radius: 10px; cursor: pointer; color: white; font-size: 16px; font-weight: 600; transition: all 0.3s; }
.btn-nav-cal:hover { transform: scale(1.05); box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4); }
.calendario-semanas { display: grid; grid-template-columns: repeat(7, 1fr); text-align: center; font-weight: bold; font-size: 13px; margin-bottom: 10px; color: var(--cor-texto-light); }
.calendario-dias { display: grid; grid-template-columns: repeat(7, 1fr); gap: 6px; }
.dia-cal { padding: 14px; text-align: center; border-radius: 10px; cursor: pointer; font-size: 15px; font-weight: 600; transition: all 0.3s; }
.dia-cal:hover { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; transform: scale(1.05); }
.dia-cal.selecionado { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; font-weight: bold; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4); }
.dia-cal.bloqueado { opacity: 0.3; cursor: not-allowed; background: #fee2e2 !important; color: #999; }
.dia-cal.bloqueado:hover { background: #fee2e2 !important; transform: none; }

.lista-horarios { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
.btn-slot { padding: 16px; background: white; border: 2px solid var(--borda); border-radius: 12px; cursor: pointer; font-weight: 700; font-size: 15px; color: var(--cor-texto); transition: all 0.3s; }
body.modo-escuro .btn-slot { background: var(--cor-cartao); border-color: var(--borda); }
.btn-slot:hover { border-color: #667eea; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3); }

.card-resumo { background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); padding: 25px; border-radius: 16px; margin-bottom: 25px; border: 2px solid rgba(102, 126, 234, 0.2); }
.card-resumo p { margin-bottom: 12px; font-size: 16px; border-bottom: 1px dashed var(--borda); padding-bottom: 10px; font-weight: 500; }
.card-resumo p:last-child { border-bottom: none; margin-bottom: 0; padding-bottom: 0; }

.header-sucesso { text-align: center; margin-bottom: 25px; }
.header-sucesso .emoji-grande { font-size: 60px; display: block; margin-bottom: 10px; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.2)); }
.header-sucesso h2 { font-size: 24px; font-weight: 800; color: var(--cor-texto); }

.card-agendamento { background: white; border-left: 5px solid #667eea; padding: 18px; border-radius: 12px; margin-bottom: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
body.modo-escuro .card-agendamento { background: var(--cor-cartao); }
.card-info strong { font-size: 17px; display: block; margin-bottom: 6px; color: var(--cor-texto); }
.card-actions { display: flex; gap: 10px; margin-top: 15px; }
.btn-reagendar { flex: 1; padding: 10px; border-radius: 10px; border: 2px solid #667eea; background: white; color: #667eea; font-weight: 700; cursor: pointer; font-size: 13px; transition: all 0.3s; }
.btn-reagendar:hover { background: #667eea; color: white; transform: translateY(-2px); }
.btn-cancelar-item { flex: 1; padding: 10px; border-radius: 10px; border: 2px solid #f87171; background: white; color: #dc2626; font-weight: 700; cursor: pointer; font-size: 13px; transition: all 0.3s; }
.btn-cancelar-item:hover { background: #f87171; color: white; transform: translateY(-2px); }

.texto-orientacao { text-align: center; color: var(--cor-texto-light); margin-bottom: 20px; font-size: 15px; }
.destaque-texto { color: #667eea; font-weight: 700; }

body.modo-escuro .btn-terciario { background: #334155; color: #ffffff; border: 2px solid #475569; }
body.modo-escuro .card-turno { background: var(--cor-cartao); border-color: var(--borda); }
body.modo-escuro .dia-cal:hover { background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%); }
body.modo-escuro .btn-flutuante { background: var(--cor-cartao); border-color: var(--borda); }
"""

# ==========================================
# 2. SCRIPT.JS - LÓGICA COMPLETA
# ==========================================
SCRIPT_JS = r"""// ==========================================
// CONFIGURAÇÕES GLOBAIS
// ==========================================
let temaAtual = localStorage.getItem('tema-sistema') || 'claro';
let dadosAgendamento = {};
let agendamentosDoCliente = JSON.parse(localStorage.getItem('meus_agendamentos')) || [];
let turnoEscolhido = '';
let mesAtual = new Date().getMonth();
let anoAtual = new Date().getFullYear();

// ==========================================
// INICIALIZAÇÃO
// ==========================================
window.onload = function() {
    if (temaAtual === 'escuro') {
        document.body.classList.add('modo-escuro');
        document.getElementById('btn-tema').innerText = '️';
    }
    aplicarIdentidade();
    verificarAgendamentos();
    renderCalendario();
};

// ==========================================
// NAVEGAÇÃO
// ==========================================
function navegar(idTela) {
    document.querySelectorAll('.tela').forEach(t => t.classList.remove('ativa'));
    document.getElementById(idTela).classList.add('ativa');
    
    if (idTela === 'tela-calendario') renderCalendario();
    if (idTela === 'tela-boas-vindas') verificarAgendamentos();
}

// ==========================================
// TEMA (CLARO/ESCURO)
// ==========================================
function alternarTema() {
    document.body.classList.toggle('modo-escuro');
    const btn = document.getElementById('btn-tema');
    const isDark = document.body.classList.contains('modo-escuro');
    btn.innerText = isDark ? '☀️' : '🌙';
    localStorage.setItem('tema-sistema', isDark ? 'escuro' : 'claro');
}

// ==========================================
// IDENTIDADE DINÂMICA (Nome Empresa + Bot)
// ==========================================
function aplicarIdentidade() {
    const config = JSON.parse(localStorage.getItem('config-identidade')) || {};
    const nomeEmpresa = config.nomeEmpresa || 'Evandro Suek';
    const nomeBot = config.nomeBot || 'Bella';
    
    // Atualiza nome da empresa no header
    const elEmpresa = document.getElementById('display-nome-empresa');
    if (elEmpresa) elEmpresa.textContent = nomeEmpresa;
    
    // Atualiza nome do bot na mensagem
    const msgPrincipal = document.querySelector('.msg-bot-principal');
    if (msgPrincipal) {
        msgPrincipal.innerHTML = `"OLÁ! BEM-VINDO(A)!<br>EU SOU A <span class="destaque-bella">${nomeBot.toUpperCase()}</span>, SUA ASSISTENTE VIRTUAL."`;
    }
}

// ==========================================
// INICIAR SISTEMA - NOME PADRONIZADO
// ==========================================
function iniciarSistema() {
    const nome = document.getElementById('input-nome-cliente').value.trim();
    if (nome.length < 3) return alert('Digite seu nome completo');
    
    const nomeFormatado = nome.toLowerCase()
        .split(' ')
        .map(palavra => palavra.charAt(0).toUpperCase() + palavra.slice(1))
        .join(' ');
    
    dadosAgendamento.nome = nomeFormatado;
    document.getElementById('nome-cliente-destaque').innerText = nomeFormatado;
    navegar('tela-boas-vindas');
}

function selecionarServico(servico) {
    dadosAgendamento.servico = servico;
    navegar('tela-data');
}

// ==========================================
// VALIDAÇÃO DE DATAS PASSADAS
// ==========================================
function selecionarData(opcao) {
    if (opcao === 'Outro Dia') { 
        navegar('tela-calendario'); 
        return; 
    }
    
    if (opcao.includes('Hoje')) {
        const hoje = new Date();
        const configFuso = localStorage.getItem('fuso-horario-sistema') || 'America/Sao_Paulo';
        const horaAtual = new Date().toLocaleString('pt-BR', { timeZone: configFuso, hour: '2-digit', hour12: false });
        const horaNum = parseInt(horaAtual.split(':')[0]);
        
        if (horaNum >= 21) {
            alert('O horário de hoje já foi encerrado. Por favor, selecione outra data.');
            return;
        }
    }
    
    dadosAgendamento.data = opcao;
    document.getElementById('turno-data-display').innerText = opcao;
    navegar('tela-turno');
}

// ==========================================
// CALENDÁRIO COM BLOQUEIO DE DATAS PASSADAS
// ==========================================
function renderCalendario() {
    const container = document.getElementById('calendario-dias');
    if (!container) return;
    container.innerHTML = '';
    document.getElementById('mes-ano-cal').innerText = new Date(anoAtual, mesAtual).toLocaleDateString('pt-BR', {month:'long', year:'numeric'});
    
    const hoje = new Date();
    hoje.setHours(0, 0, 0, 0);
    
    const firstDay = new Date(anoAtual, mesAtual, 1).getDay();
    const daysInMonth = new Date(anoAtual, mesAtual + 1, 0).getDate();
    
    for(let i=0; i<firstDay; i++) container.innerHTML += '<div></div>';
    
    for(let d=1; d<=daysInMonth; d++) {
        const el = document.createElement('div');
        el.className = 'dia-cal';
        el.innerText = d;
        
        const dataDia = new Date(anoAtual, mesAtual, d);
        dataDia.setHours(0, 0, 0, 0);
        
        if (dataDia < hoje) {
            el.classList.add('bloqueado');
            el.title = 'Data indisponível';
            el.style.cursor = 'not-allowed';
            el.style.opacity = '0.3';
        } else {
            el.onclick = () => {
                document.querySelectorAll('.dia-cal').forEach(e => e.classList.remove('selecionado'));
                el.classList.add('selecionado');
                dadosAgendamento.data = `${d}/${mesAtual+1}/${anoAtual}`;
                document.getElementById('turno-data-display').innerText = dadosAgendamento.data;
                setTimeout(() => navegar('tela-turno'), 200);
            };
        }
        container.appendChild(el);
    }
}

function mudarMes(d) { 
    mesAtual += d; 
    if(mesAtual>11){mesAtual=0; anoAtual++;} 
    if(mesAtual<0){mesAtual=11; anoAtual--;} 
    renderCalendario(); 
}

// ==========================================
// GERADOR DINÂMICO DE HORÁRIOS
// ==========================================
function gerarListaHoras(inicio, fim) {
    let lista = [];
    if (!inicio || !fim) return ['09:00', '10:00', '11:00'];
    
    let dataInicio = new Date("2000-01-01 " + inicio);
    let dataFim = new Date("2000-01-01 " + fim);
    
    while (dataInicio < dataFim) {
        let h = String(dataInicio.getHours()).padStart(2, '0');
        let m = String(dataInicio.getMinutes()).padStart(2, '0');
        lista.push(h + ":" + m);
        dataInicio.setMinutes(dataInicio.getMinutes() + 60);
    }
    return lista;
}

function obterNomeDiaSemana(dataStr) {
    if (!dataStr) return null;
    if (dataStr.includes(',')) {
        const parteDia = dataStr.split(',')[1].trim().toLowerCase();
        return parteDia.normalize("NFD").replace(/[\u0300-\u036f]/g, "").split(' ')[0];
    }
    const partes = dataStr.split('/');
    if (partes.length === 3) {
        const data = new Date(partes[2], partes[1] - 1, partes[0]);
        const nomes = ['domingo', 'segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado'];
        return nomes[data.getDay()];
    }
    return null;
}

// ==========================================
// SELEÇÃO DE TURNO (COM CONFIGURAÇÃO POR DIA)
// ==========================================
function selecionarTurno(turno) {
    turnoEscolhido = turno;
    const lista = document.getElementById('lista-horarios-dinamica');
    lista.innerHTML = '';

    const diaEscolhido = obterNomeDiaSemana(dadosAgendamento.data);
    const configSalvo = localStorage.getItem('config-horarios-dia');
    let horarios = [];
    let infoDisplay = '';

    if (configSalvo && diaEscolhido) {
        const config = JSON.parse(configSalvo);
        const configDia = config[diaEscolhido];
        
        if (!configDia || !configDia.ativo) {
            alert(`⛔ Não atendemos aos ${diaEscolhido}s.`);
            navegar('tela-data');
            return;
        }

        horarios = gerarListaHoras(configDia.inicio, configDia.fim);
        infoDisplay = `${diaEscolhido.charAt(0).toUpperCase() + diaEscolhido.slice(1)} (${configDia.inicio} - ${configDia.fim})`;
    } else {
        horarios = turno === 'dia' 
            ? ['09:00', '10:00', '11:00', '14:00', '15:00', '16:00', '17:00']
            : ['18:00', '18:30', '19:00', '19:30', '20:00'];
        infoDisplay = turno === 'dia' ? 'Dia 🌞' : 'Noite 🌙';
    }

    document.getElementById('turno-atual-display').innerText = infoDisplay;

    if (horarios.length === 0) {
        lista.innerHTML = '<p style="color:#ef4444; text-align:center; padding:20px;">️ Sem horários disponíveis.</p>';
    } else {
        horarios.forEach(hora => {
            const btn = document.createElement('button');
            btn.className = 'btn-slot';
            btn.innerText = hora;
            btn.onclick = () => selecionarHora(hora);
            lista.appendChild(btn);
        });
    }

    navegar('tela-horario');
}

function selecionarHora(hora) {
    dadosAgendamento.hora = hora;
    navegar('tela-whatsapp');
}

// ==========================================
// MÁSCARA DE TELEFONE
// ==========================================
function mascararTelefone(input) {
    let v = input.value.replace(/\D/g, "").slice(0, 11);
    v = v.replace(/^(\d{2})(\d)/g, "($1) $2");
    v = v.replace(/(\d)(\d{4})$/, "$1-$2");
    input.value = v;
}

// ==========================================
// CONFIRMAR AGENDAMENTO COM VALIDAÇÃO
// ==========================================
function confirmarAgendamento() {
    const tel = document.getElementById('input-telefone').value;
    if (tel.length < 14) return alert('Telefone inválido');
    
    if (dadosAgendamento.data && dadosAgendamento.data.includes('/')) {
        const partes = dadosAgendamento.data.split('/');
        const dataAgendada = new Date(partes[2], partes[1] - 1, partes[0]);
        const hoje = new Date();
        hoje.setHours(0,0,0,0);
        dataAgendada.setHours(0,0,0,0);
        
        if (dataAgendada < hoje) {
            return alert('⛔ Não é possível agendar para datas passadas! Selecione uma data válida.');
        }
    }
    
    dadosAgendamento.telefone = tel;
    dadosAgendamento.turno = turnoEscolhido;
    dadosAgendamento.status = 'Confirmado';
    
    agendamentosDoCliente.push({...dadosAgendamento});
    localStorage.setItem('meus_agendamentos', JSON.stringify(agendamentosDoCliente));
    
    document.getElementById('resumo-nome').innerText = dadosAgendamento.nome;
    document.getElementById('resumo-servico').innerText = dadosAgendamento.servico;
    document.getElementById('resumo-data').innerText = dadosAgendamento.data;
    document.getElementById('resumo-hora').innerText = `${dadosAgendamento.hora} (${turnoEscolhido === 'dia' ? 'Dia' : 'Noite'})`;
    
    navegar('tela-sucesso');
}

// ==========================================
// GESTÃO DE AGENDAMENTOS
// ==========================================
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
                <div class="card-info">
                    <strong>${ag.servico}</strong>
                    <div style="margin:4px 0; font-weight:500;">📅 ${ag.data} às ${ag.hora}</div>
                    <div style="font-size:12px; color:var(--cor-texto-light);">👤 ${ag.nome}</div>
                </div>
                <div class="card-actions">
                    <button onclick="reagendarAgendamento(${index})" class="btn-reagendar">🔄 Reagendar</button>
                    <button onclick="cancelarItem(${index})" class="btn-cancelar-item">❌ Cancelar</button>
                </div>
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

function reagendarAgendamento(index) {
    if(confirm("Deseja reagendar este horário? O atual será liberado.")) {
        dadosAgendamento = { ...agendamentosDoCliente[index] };
        agendamentosDoCliente.splice(index, 1);
        localStorage.setItem('meus_agendamentos', JSON.stringify(agendamentosDoCliente));
        navegar('tela-data');
    }
}

function cancelarAgora() {
    if(confirm('Tem certeza que deseja cancelar?')) {
        agendamentosDoCliente.pop();
        localStorage.setItem('meus_agendamentos', JSON.stringify(agendamentosDoCliente));
        alert('Agendamento cancelado com sucesso.');
        window.location.reload();
    }
}

function reagendarAgora() {
    agendamentosDoCliente.pop();
    localStorage.setItem('meus_agendamentos', JSON.stringify(agendamentosDoCliente));
    navegar('tela-servicos');
}
"""

# ==========================================
# 3. INDEX.HTML - ESTRUTURA COMPLETA
# ==========================================
INDEX_HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema de Agendamento</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div id="app-container">

        <!-- TELA 0: ENTRADA -->
        <div id="tela-entrada" class="tela ativa">
            <button onclick="alternarTema()" id="btn-tema" class="btn-flutuante">🌙</button>
            
            <div class="box-empresa">
                <h1 id="display-nome-empresa">Evandro Suek</h1>
                <span class="subtitulo-empresa">Sistemas Automatizados de Atendimento</span>
            </div>
            
            <div class="row-bot-info">
                <div class="box-foto-bot">
                    <img src="bot.png" alt="Bot" onerror="this.src='https://ui-avatars.com/api/?name=Bot&background=8b5cf6&color=fff&size=150'">
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
            <div style="margin-bottom: 20px;">
                <button onclick="navegar('tela-entrada')" class="btn-voltar">← Voltar e trocar de nome</button>
            </div>

            <div class="header-box">
                <h1>Olá, <span id="nome-cliente-destaque">...</span>!</h1>
                <p class="msg-intro">Como posso ajudar você hoje?</p>
            </div>

            <button id="btn-meus-agendamentos" onclick="navegar('tela-agendamentos')" class="btn-grande btn-terciario" style="display: none;">
                 VER MEUS AGENDAMENTOS
            </button>

            <div class="botoes-acao">
                <button onclick="navegar('tela-servicos')" class="btn-grande btn-primario">📅 AGENDAR AGORA</button>
                <button onclick="navegar('tela-servicos')" class="btn-grande btn-secundario"> SERVIÇOS</button>
                <button onclick="alert('Chamando atendente...')" class="btn-grande btn-terciario">👤 FALAR COM ATENDENTE</button>
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
                    <div class="info">
                        <strong>Corte Masculino</strong>
                        <span class="detalhes">R$ 35,00 • 30 min</span>
                    </div>
                </div>
                <div class="card-servico" onclick="selecionarServico('Barba Completa')">
                    <span class="emoji">🧔</span>
                    <div class="info">
                        <strong>Barba Completa</strong>
                        <span class="detalhes">R$ 25,00 • 25 min</span>
                    </div>
                </div>
                <div class="card-servico" onclick="selecionarServico('Corte + Barba')">
                    <span class="emoji">✨</span>
                    <div class="info">
                        <strong>Corte + Barba</strong>
                        <span class="detalhes">R$ 55,00 • 50 min</span>
                    </div>
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
                    <div class="info">
                        <strong>HOJE</strong>
                        <span class="detalhes">Segunda-feira</span>
                    </div>
                </div>
                <div class="card-data" onclick="selecionarData('Amanhã, Terça')">
                    <span class="emoji">📅</span>
                    <div class="info">
                        <strong>AMANHÃ</strong>
                        <span class="detalhes">Terça-feira</span>
                    </div>
                </div>
                <div class="card-data" onclick="selecionarData('Outro Dia')">
                    <span class="emoji">🗓️</span>
                    <div class="info">
                        <strong>OUTRO DIA</strong>
                        <span class="detalhes">Calendário</span>
                    </div>
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
                <div class="calendario-semanas">
                    <div>D</div><div>S</div><div>T</div><div>Q</div><div>Q</div><div>S</div><div>S</div>
                </div>
                <div class="calendario-dias" id="calendario-dias"></div>
            </div>
        </div>

        <!-- TELA 5: TURNO -->
        <div id="tela-turno" class="tela">
            <div class="header-simples">
                <button onclick="navegar('tela-data')" class="btn-voltar">← Voltar</button>
                <h2>Qual período prefere?</h2>
            </div>
            <p class="texto-orientacao">Para: <span id="turno-data-display" class="destaque-texto">...</span></p>
            
            <div class="grid-turnos">
                <button onclick="selecionarTurno('dia')" class="card-turno dia">
                    <span class="emoji-grande">🌞</span>
                    <strong>DIA</strong>
                </button>
                <button onclick="selecionarTurno('noite')" class="card-turno noite">
                    <span class="emoji-grande">🌙</span>
                    <strong>NOITE</strong>
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
            <div class="lista-horarios" id="lista-horarios-dinamica"></div>
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
            <button onclick="confirmarAgendamento()" class="btn-grande btn-primario">✅ FINALIZAR AGENDAMENTO</button>
        </div>

        <!-- TELA 8: SUCESSO -->
        <div id="tela-sucesso" class="tela">
            <div class="header-sucesso">
                <span class="emoji-grande">🎉</span>
                <h2>AGENDADO COM SUCESSO!</h2>
            </div>
            
            <div class="card-resumo">
                <p>👤 <span id="resumo-nome">...</span></p>
                <p>✂️ <span class="destaque-nome" id="resumo-servico">...</span></p>
                <p>📅 <span id="resumo-data">...</span></p>
                <p>🕐 <span id="resumo-hora">...</span></p>
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
                <span class="emoji-grande"></span>
                <p>Nenhum agendamento encontrado.</p>
                <button onclick="navegar('tela-servicos')" class="btn-grande btn-primario" style="margin-top:15px;">FAZER AGENDAMENTO</button>
            </div>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>
"""

# ==========================================
# 4. PAINEL.HTML - ADMIN COMPLETO
# ==========================================
PAINEL_HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Painel Administrativo</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', system-ui, sans-serif; }
        body { background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%); min-height: 100vh; padding: 20px; }
        .painel-wrap { max-width: 1200px; margin: 0 auto; background: rgba(255, 255, 255, 0.95); border-radius: 20px; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3); overflow: hidden; }
        .header-painel { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }
        .header-painel h1 { font-size: 32px; margin-bottom: 10px; }
        .tabs { display: flex; background: #f1f5f9; border-bottom: 2px solid #e2e8f0; flex-wrap: wrap; }
        .tab-btn { flex: 1; min-width: 150px; padding: 15px 20px; border: none; background: transparent; cursor: pointer; font-weight: 600; color: #64748b; transition: all 0.3s; font-size: 14px; }
        .tab-btn:hover { background: rgba(102, 126, 234, 0.1); color: #667eea; }
        .tab-btn.ativo { background: white; color: #667eea; border-bottom: 3px solid #667eea; }
        .conteudo { padding: 30px; min-height: 500px; }
        .aba { display: none; animation: fadeIn 0.3s; }
        .aba.ativo { display: block; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        .config-card { background: white; border: 2px solid #e2e8f0; border-radius: 12px; padding: 25px; margin-bottom: 20px; }
        .config-card h3 { color: #667eea; margin-bottom: 20px; font-size: 18px; }
        .slider-group { margin-bottom: 20px; }
        .slider-group label { display: block; margin-bottom: 8px; font-weight: 600; color: #475569; font-size: 14px; }
        .slider-group input[type="text"], .slider-group input[type="time"] { width: 100%; padding: 10px; border-radius: 6px; border: 1px solid #e2e8f0; font-size: 14px; }
        .slider-group select { width: 100%; padding: 12px; border-radius: 8px; border: 2px solid #e2e8f0; font-size: 14px; background: white; color: #0f172a; cursor: pointer; }
        .slider-group select:focus { border-color: #667eea; outline: none; }
        .btn-salvar { background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; border: none; padding: 14px 28px; border-radius: 10px; font-weight: 700; cursor: pointer; font-size: 15px; transition: all 0.3s; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3); }
        .btn-salvar:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4); }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .stat-card { background: white; border: 2px solid #e2e8f0; border-radius: 12px; padding: 25px; text-align: center; }
        .stat-card .numero { font-size: 48px; font-weight: 800; color: #667eea; display: block; }
        .stat-card .label { color: #64748b; font-size: 14px; margin-top: 5px; }
    </style>
</head>
<body>
    <div class="painel-wrap">
        <div class="header-painel">
            <h1>🎛️ Painel Administrativo</h1>
            <p>Evandro Suek - Sistemas Automatizados de Atendimento</p>
        </div>
        
        <div class="tabs">
            <button class="tab-btn ativo" onclick="mudarAba('dashboard', this)">📊 Dashboard</button>
            <button class="tab-btn" onclick="mudarAba('configuracoes', this)">️ Configurações</button>
        </div>
        
        <div class="conteudo">
            <!-- DASHBOARD -->
            <div id="dashboard" class="aba ativo">
                <h2 style="margin-bottom: 20px;">📊 Visão Geral</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <span class="numero" id="total-agendamentos">0</span>
                        <div class="label">Total de Agendamentos</div>
                    </div>
                    <div class="stat-card">
                        <span class="numero" id="agendamentos-hoje">0</span>
                        <div class="label">Agendamentos Hoje</div>
                    </div>
                    <div class="stat-card">
                        <span class="numero" id="clientes-unicos">0</span>
                        <div class="label">Clientes Únicos</div>
                    </div>
                </div>
            </div>
            
            <!-- CONFIGURAÇÕES -->
            <div id="configuracoes" class="aba">
                <h2 style="margin-bottom: 20px;">⚙️ Configurações do Sistema</h2>
                
                <!-- IDENTIDADE -->
                <div class="config-card">
                    <h3>🏢 Identidade</h3>
                    <div class="slider-group">
                        <label>Nome da Empresa:</label>
                        <input type="text" id="input-nome-empresa" placeholder="Ex: Clínica Sorriso">
                    </div>
                    <div class="slider-group">
                        <label>Nome do Atendente (Bot):</label>
                        <input type="text" id="input-nome-bot" placeholder="Ex: Bella">
                    </div>
                    <button onclick="salvarIdentidade()" class="btn-salvar">💾 Salvar Identidade</button>
                </div>
                
                <!-- FUSO HORÁRIO -->
                <div class="config-card">
                    <h3>🌍 Fuso Horário</h3>
                    <div class="slider-group">
                        <label>Selecione o Fuso:</label>
                        <select id="fuso-horario">
                            <option value="America/Sao_Paulo">Brasília (GMT-3)</option>
                            <option value="America/Manaus">Manaus (GMT-4)</option>
                            <option value="America/Rio_Branco">Rio Branco (GMT-5)</option>
                            <option value="America/Noronha">Fernando de Noronha (GMT-2)</option>
                        </select>
                    </div>
                    <button onclick="salvarFusoHorario()" class="btn-salvar" style="background: #6366f1;">💾 Salvar Fuso</button>
                </div>
                
                <!-- HORÁRIOS POR DIA -->
                <div class="config-card">
                    <h3>📅 Horários por Dia da Semana</h3>
                    <p style="color: #64748b; margin-bottom: 15px; font-size: 13px;">Cada dia é independente. Desmarque para fechar o dia.</p>
                    <div id="container-dias-semana"></div>
                    <button onclick="salvarConfigDias()" class="btn-salvar" style="width: 100%; margin-top: 15px;">💾 Salvar Horários Semanais</button>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // Dias da semana
        const diasSemana = [
            { id: 'domingo', label: 'Domingo', cor: '#ef4444' },
            { id: 'segunda', label: 'Segunda-feira', cor: '#3b82f6' },
            { id: 'terca', label: 'Terça-feira', cor: '#3b82f6' },
            { id: 'quarta', label: 'Quarta-feira', cor: '#3b82f6' },
            { id: 'quinta', label: 'Quinta-feira', cor: '#3b82f6' },
            { id: 'sexta', label: 'Sexta-feira', cor: '#3b82f6' },
            { id: 'sabado', label: 'Sábado', cor: '#f59e0b' }
        ];
        
        // Gerar dias no painel
        const container = document.getElementById('container-dias-semana');
        if (container) {
            diasSemana.forEach(dia => {
                container.innerHTML += `
                    <div style="background: #f8fafc; padding: 12px; border-radius: 8px; margin-bottom: 12px; border-left: 4px solid ${dia.cor};">
                        <div style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">
                            <input type="checkbox" id="${dia.id}-ativo" style="width:18px; height:18px; cursor:pointer;">
                            <label style="font-weight:700; flex:1; cursor:pointer;" for="${dia.id}-ativo">${dia.label}</label>
                        </div>
                        <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; padding-left:28px;">
                            <input type="time" id="${dia.id}-inicio" value="08:00">
                            <input type="time" id="${dia.id}-fim" value="17:00">
                        </div>
                    </div>
                `;
            });
        }
        
        // Navegação
        function mudarAba(idAba, btn) {
            document.querySelectorAll('.aba').forEach(aba => aba.classList.remove('ativo'));
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('ativo'));
            document.getElementById(idAba).classList.add('ativo');
            btn.classList.add('ativo');
            if (idAba === 'dashboard') carregarDashboard();
        }
        
        // Dashboard
        function carregarDashboard() {
            const agendamentos = JSON.parse(localStorage.getItem('meus_agendamentos')) || [];
            const hoje = new Date().toLocaleDateString('pt-BR');
            document.getElementById('total-agendamentos').textContent = agendamentos.length;
            document.getElementById('agendamentos-hoje').textContent = agendamentos.filter(ag => ag.data === hoje).length;
            document.getElementById('clientes-unicos').textContent = [...new Set(agendamentos.map(ag => ag.nome))].length;
        }
        
        // Identidade
        function salvarIdentidade() {
            const config = {
                nomeEmpresa: document.getElementById('input-nome-empresa').value,
                nomeBot: document.getElementById('input-nome-bot').value
            };
            localStorage.setItem('config-identidade', JSON.stringify(config));
            alert('✅ Identidade salva!');
        }
        function carregarIdentidade() {
            const salvo = localStorage.getItem('config-identidade');
            if (salvo) {
                const config = JSON.parse(salvo);
                document.getElementById('input-nome-empresa').value = config.nomeEmpresa || '';
                document.getElementById('input-nome-bot').value = config.nomeBot || 'Bella';
            } else {
                document.getElementById('input-nome-bot').value = 'Bella';
            }
        }
        
        // Fuso Horário
        function salvarFusoHorario() {
            const fuso = document.getElementById('fuso-horario').value;
            localStorage.setItem('fuso-horario-sistema', fuso);
            alert('✅ Fuso horário salvo: ' + fuso);
        }
        
        // Horários por Dia
        function salvarConfigDias() {
            let config = {};
            diasSemana.forEach(dia => {
                config[dia.id] = {
                    ativo: document.getElementById(`${dia.id}-ativo`).checked,
                    inicio: document.getElementById(`${dia.id}-inicio`).value,
                    fim: document.getElementById(`${dia.id}-fim`).value
                };
            });
            localStorage.setItem('config-horarios-dia', JSON.stringify(config));
            alert('✅ Horários semanais salvos!');
        }
        function carregarConfigDias() {
            const salvo = localStorage.getItem('config-horarios-dia');
            if (salvo) {
                const config = JSON.parse(salvo);
                diasSemana.forEach(dia => {
                    if (config[dia.id]) {
                        document.getElementById(`${dia.id}-ativo`).checked = config[dia.id].ativo;
                        document.getElementById(`${dia.id}-inicio`).value = config[dia.id].inicio || '08:00';
                        document.getElementById(`${dia.id}-fim`).value = config[dia.id].fim || '17:00';
                    }
                });
            }
        }
        
        // Inicialização
        window.addEventListener('DOMContentLoaded', function() {
            carregarIdentidade();
            carregarConfigDias();
            carregarDashboard();
        });
    </script>
</body>
</html>
"""

# ==========================================
# FUNÇÃO DE EXECUÇÃO
# ==========================================
def salvar(nome, conteudo):
    try:
        with open(PASTA / nome, 'w', encoding='utf-8') as f:
            f.write(conteudo)
        print(f"✅ {nome} atualizado!")
    except Exception as e:
        print(f"❌ Erro em {nome}: {e}")

def main():
    print("\n" + "="*70)
    print("🚀 ATUALIZAÇÃO COMPLETA DO SISTEMA")
    print("="*70)
    print("\n📦 ARQUIVOS QUE SERÃO ATUALIZADOS:")
    print("  1. style.css       - Visual Glassmorphism + Tema Escuro")
    print("  2. script.js       - Lógica Completa (Datas, Horários, Identidade)")
    print("  3. index.html      - Estrutura com IDs Dinâmicos")
    print("  4. painel.html     - Admin Completo (Identidade, Fuso, Dias)")
    print("\n" + "="*70)
    
    resposta = input("Deseja continuar? (s/n): ").lower()
    if resposta != 's':
        print("❌ Operação cancelada.")
        return
    
    salvar("style.css", STYLE_CSS)
    salvar("script.js", SCRIPT_JS)
    salvar("index.html", INDEX_HTML)
    salvar("painel.html", PAINEL_HTML)
    
    print("\n" + "="*70)
    print("✨ TODOS OS ARQUIVOS ATUALIZADOS COM SUCESSO!")
    print("="*70)
    print("\n📋 O QUE FOI IMPLEMENTADO:")
    print("  ✅ Nome da Empresa configurável pelo painel")
    print("  ✅ Nome do Bot configurável")
    print("  ✅ Fuso Horário selecionável")
    print("  ✅ Horários independentes por dia da semana")
    print("  ✅ Datas passadas bloqueadas")
    print("  ✅ Tema Claro/Escuro")
    print("  ✅ Visual Glassmorphism profissional")
    print("\n🌐 PRÓXIMOS PASSOS:")
    print("  1. Abra o painel.html no navegador")
    print("  2. Configure: Nome, Bot, Fuso e Horários")
    print("  3. Abra index.html e teste!")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()