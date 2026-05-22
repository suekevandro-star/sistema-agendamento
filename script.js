// ==========================================
// CONFIGURAÇÕES GLOBAIS
// ==========================================
var dadosAgendamento = { nome: '', servico: '', data: '', hora: '', turno: '' };
var mesAtual = new Date().getMonth();
var anoAtual = new Date().getFullYear();
var turnoEscolhido = '';

// ==========================================
// 🔑 ISOLAMENTO POR USUÁRIO (PRIVACIDADE)
// ==========================================
function getChaveUsuario(nome) {
    if (!nome) return 'anonimo';
    return nome.trim().toLowerCase().replace(/\s+/g, '_');
}

// ==========================================
// NAVEGAÇÃO SIMPLES
// ==========================================
function navegar(idTela) {
    var telas = document.querySelectorAll('.tela');
    for (var i = 0; i < telas.length; i++) {
        telas[i].style.display = 'none';
        telas[i].className = telas[i].className.replace(' ativa', '');
    }
    var alvo = document.getElementById(idTela);
    if (alvo) {
        alvo.style.display = 'block';
        alvo.className += ' ativa';
        window.scrollTo(0, 0);
    }
    if (idTela === 'tela-agendamentos') verificarAgendamentos();
    if (idTela === 'tela-calendario') renderCalendario();
}

// ==========================================
// 1. ENTRADA + VALIDAÇÃO DE NOME COMPLETO
// ==========================================
function iniciarSistema() {
    var input = document.getElementById('input-nome-cliente');
    if (!input) return;

    var nome = input.value.trim();
    if (nome.indexOf(' ') === -1 || nome.length < 4) {
        alert('⚠️ Digite seu NOME COMPLETO.\nEx: Maria Silva');
        input.focus();
        return;
    }

    var partes = nome.split(' ');
    var formatado = [];
    for (var i = 0; i < partes.length; i++) {
        if (partes[i].length > 0) {
            formatado.push(partes[i].charAt(0).toUpperCase() + partes[i].slice(1).toLowerCase());
        }
    }
    var nomeFinal = formatado.join(' ');

    dadosAgendamento.nome = nomeFinal;
    
    var destaque = document.getElementById('nome-cliente-destaque');
    if (destaque) destaque.innerText = nomeFinal;

    navegar('tela-boas-vindas');
}

// ==========================================
// 2. FLUXO DE AGENDAMENTO
// ==========================================
function selecionarServico(servico) {
    dadosAgendamento.servico = servico;
    navegar('tela-data');
}

function selecionarData(opcao) {
    if (opcao === 'Outro Dia') { 
        navegar('tela-calendario'); 
        return; 
    }
    dadosAgendamento.data = opcao;
    document.getElementById('turno-data-display').innerText = opcao;
    navegar('tela-turno');
}

function renderCalendario() {
    var container = document.getElementById('calendario-dias');
    if (!container) return;
    container.innerHTML = '';

    document.getElementById('mes-ano-cal').innerText = new Date(anoAtual, mesAtual).toLocaleDateString('pt-BR', { month: 'long', year: 'numeric' });

    var hoje = new Date();
    hoje.setHours(0, 0, 0, 0);

    var firstDay = new Date(anoAtual, mesAtual, 1).getDay();
    var daysInMonth = new Date(anoAtual, mesAtual + 1, 0).getDate();

    for (var i = 0; i < firstDay; i++) {
        container.innerHTML += '<div></div>';
    }

    for (var d = 1; d <= daysInMonth; d++) {
        var el = document.createElement('div');
        el.className = 'dia-cal';
        el.innerText = d;

        var dataDia = new Date(anoAtual, mesAtual, d);
        dataDia.setHours(0, 0, 0, 0);

        if (dataDia < hoje) {
            el.className += ' bloqueado';
            el.style.opacity = '0.3';
            el.style.cursor = 'not-allowed';
        } else {
            el.onclick = function() {
                var diaSelecionado = this.innerText;
                var dataFormatada = diaSelecionado + '/' + (mesAtual + 1) + '/' + anoAtual;
                dadosAgendamento.data = dataFormatada;
                document.getElementById('turno-data-display').innerText = dataFormatada;
                navegar('tela-turno');
            };
        }
        container.appendChild(el);
    }
}

function mudarMes(d) {
    mesAtual += d;
    if (mesAtual > 11) { mesAtual = 0; anoAtual++; }
    if (mesAtual < 0) { mesAtual = 11; anoAtual--; }
    renderCalendario();
}

function selecionarTurno(turno) {
    turnoEscolhido = turno;
    var lista = document.getElementById('lista-horarios-dinamica');
    lista.innerHTML = '';

    var horarios = turno === 'dia' 
        ? ['09:00', '10:00', '11:00', '14:00', '15:00', '16:00', '17:00']
        : ['18:00', '18:30', '19:00', '19:30', '20:00'];

    document.getElementById('turno-atual-display').innerText = turno === 'dia' ? 'Dia 🌞' : 'Noite 🌙';

    for (var i = 0; i < horarios.length; i++) {
        var btn = document.createElement('button');
        btn.className = 'btn-slot';
        btn.innerText = horarios[i];
        btn.onclick = (function(h) {
            return function() { selecionarHora(h); };
        })(horarios[i]);
        lista.appendChild(btn);
    }

    navegar('tela-horario');
}

function selecionarHora(hora) {
    dadosAgendamento.hora = hora;
    dadosAgendamento.turno = turnoEscolhido;
    navegar('tela-whatsapp');
}

function mascararTelefone(input) {
    var v = input.value.replace(/\D/g, "").slice(0, 11);
    v = v.replace(/^(\d{2})(\d)/g, "($1) $2");
    v = v.replace(/(\d)(\d{4})$/, "$1-$2");
    input.value = v;
}

// ==========================================
// 3. CONFIRMAÇÃO
// ==========================================
function confirmarAgendamento() {
    var tel = document.getElementById('input-telefone').value;
    if (tel.length < 14) {
        alert('Telefone inválido.');
        return;
    }

    var chave = getChaveUsuario(dadosAgendamento.nome);
    var listaSalva = localStorage.getItem('agenda_' + chave);
    var lista = listaSalva ? JSON.parse(listaSalva) : [];

    for (var i = 0; i < lista.length; i++) {
        if (lista[i].data === dadosAgendamento.data && lista[i].hora === dadosAgendamento.hora) {
            alert('⚠️ Horário indisponível!');
            return;
        }
    }

    lista.push({
        id: Date.now(),
        nome: dadosAgendamento.nome,
        servico: dadosAgendamento.servico,
        data: dadosAgendamento.data,
        hora: dadosAgendamento.hora,
        turno: dadosAgendamento.turno,
        telefone: tel
    });

    localStorage.setItem('agenda_' + chave, JSON.stringify(lista));

    document.getElementById('resumo-nome').innerText = dadosAgendamento.nome;
    document.getElementById('resumo-servico').innerText = dadosAgendamento.servico;
    document.getElementById('resumo-data').innerText = dadosAgendamento.data;
    document.getElementById('resumo-hora').innerText = dadosAgendamento.hora + ' (' + (dadosAgendamento.turno === 'dia' ? 'Dia' : 'Noite') + ')';

    navegar('tela-sucesso');
}

// ==========================================
// 4. MEUS AGENDAMENTOS + CANCELAR
// ==========================================
function verificarAgendamentos() {
    var btn = document.getElementById('btn-meus-agendamentos');
    var listaDiv = document.getElementById('lista-agendamentos');
    var msgDiv = document.getElementById('msg-sem-agendamento');

    if (!dadosAgendamento.nome) {
        if (btn) btn.style.display = 'none';
        if (listaDiv) listaDiv.style.display = 'none';
        if (msgDiv) msgDiv.style.display = 'block';
        return;
    }

    var chave = getChaveUsuario(dadosAgendamento.nome);
    var listaSalva = localStorage.getItem('agenda_' + chave);
    var lista = listaSalva ? JSON.parse(listaSalva) : [];

    if (lista.length > 0) {
        if (btn) btn.style.display = 'block';
        if (listaDiv) {
            listaDiv.style.display = 'block';
            listaDiv.innerHTML = '';

            for (var i = 0; i < lista.length; i++) {
                var ag = lista[i];
                var card = document.createElement('div');
                card.className = 'card-agendamento';
                card.innerHTML = 
                    '<div class="card-info">' +
                        '<strong>' + ag.servico + '</strong>' +
                        '<div>📅 ' + ag.data + ' às ' + ag.hora + '</div>' +
                        '<div style="font-size:12px;">👤 ' + ag.nome + '</div>' +
                    '</div>' +
                    '<div class="card-actions">' +
                        '<button onclick="reagendarAgendamento(' + ag.id + ')" class="btn-reagendar">🔄 Reagendar</button>' +
                        '<button onclick="cancelarItem(' + ag.id + ')" class="btn-cancelar">❌ Cancelar</button>' +
                    '</div>';
                listaDiv.appendChild(card);
            }
        }
        if (msgDiv) msgDiv.style.display = 'none';
    } else {
        if (btn) btn.style.display = 'none';
        if (listaDiv) listaDiv.style.display = 'none';
        if (msgDiv) msgDiv.style.display = 'block';
    }
}

function cancelarItem(id) {
    if (!confirm('Tem certeza que deseja cancelar?')) return;
    
    var chave = getChaveUsuario(dadosAgendamento.nome);
    var listaSalva = localStorage.getItem('agenda_' + chave);
    var lista = listaSalva ? JSON.parse(listaSalva) : [];
    
    lista = lista.filter(function(item) { return item.id !== id; });
    localStorage.setItem('agenda_' + chave, JSON.stringify(lista));
    
    verificarAgendamentos();
    alert('✅ Agendamento cancelado.');
}

// ==========================================
// 5. REAGENDAMENTO (LÓGICA NOVA)
// ==========================================
function reagendarAgendamento(id) {
    if (!confirm('Cancelar agendamento atual e escolher novo horário?')) {
        return; // Mantém agendado se clicar em Não
    }

    var chave = getChaveUsuario(dadosAgendamento.nome);
    var listaSalva = localStorage.getItem('agenda_' + chave);
    var lista = listaSalva ? JSON.parse(listaSalva) : [];

    lista = lista.filter(function(item) { return item.id !== id; });
    localStorage.setItem('agenda_' + chave, JSON.stringify(lista));

    dadosAgendamento = { nome: dadosAgendamento.nome, servico: '', data: '', hora: '', turno: '' };
    navegar('tela-servicos');
}

function reagendarAgora() {
    navegar('tela-servicos');
}

function cancelarAgora() {
    if (confirm('Tem certeza que deseja cancelar?')) {
        alert('Agendamento cancelado.');
        window.location.reload();
    }
}

// ==========================================
// 🌓 MODO CLARO/ESCURO
// ==========================================
function alternarTema() {
    document.body.classList.toggle('modo-escuro');
    var isDark = document.body.classList.contains('modo-escuro');
    document.getElementById('btn-tema').innerText = isDark ? '☀️' : '🌙';
    localStorage.setItem('tema-preferido', isDark ? 'escuro' : 'claro');
}

function atualizarLabelsDias() {
    var dias = ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado'];
    var hoje = new Date();
    var amanha = new Date(hoje);
    amanha.setDate(amanha.getDate() + 1);
    
    var labelHoje = document.getElementById('label-hoje');
    var labelAmanha = document.getElementById('label-amanha');
    if (labelHoje) labelHoje.textContent = dias[hoje.getDay()] + '-feira';
    if (labelAmanha) labelAmanha.textContent = dias[amanha.getDay()] + '-feira';
}

// ==========================================
// 🤖 ZOOM DO BOT (RESTAURADO)
// ==========================================
function aplicarConfigBotVisual() {
    try {
        var areaSize = localStorage.getItem('bot-area-size') || '90';
        var zoomLevel = localStorage.getItem('bot-zoom') || '100';
        
        var botContainer = document.querySelector('.box-foto-bot');
        var botImg = document.querySelector('.box-foto-bot img');
        
        if (botContainer) {
            botContainer.style.width = areaSize + 'px';
            botContainer.style.height = areaSize + 'px';
            botContainer.style.minWidth = areaSize + 'px';
            botContainer.style.minHeight = areaSize + 'px';
        }
        
        if (botImg) {
            botImg.style.transform = 'scale(' + (zoomLevel / 100) + ')';
            botImg.style.webkitTransform = 'scale(' + (zoomLevel / 100) + ')';
            botImg.style.transition = 'transform 0.2s ease';
        }
        
        var rowBotInfo = document.querySelector('.row-bot-info');
        if (rowBotInfo) {
            rowBotInfo.style.minHeight = (parseInt(areaSize) + 30) + 'px';
        }
        
    } catch (e) {
        console.log('Erro config bot:', e);
    }
}

// ==========================================
// INICIALIZAÇÃO
// ==========================================
window.addEventListener('DOMContentLoaded', function() {
    var temaSalvo = localStorage.getItem('tema-preferido');
    if (temaSalvo === 'escuro') {
        document.body.classList.add('modo-escuro');
        document.getElementById('btn-tema').innerText = '☀️';
    }

    renderCalendario();
    atualizarLabelsDias();
    aplicarConfigBotVisual();
});