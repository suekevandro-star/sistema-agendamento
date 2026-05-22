#!/usr/bin/env python3
"""
Script de Correção Automática do simulador.html
Corrige a estrutura HTML e adiciona os CSS corretamente
"""

from pathlib import Path

PASTA = Path(r"D:\Projeto Empresas")

# Conteúdo corrigido e completo do simulador.html
SIMULADOR_CORRIGIDO = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simulador de Atendimento</title>
    
    <!-- CSS Principal do Sistema -->
    <link rel="stylesheet" href="style.css">
    
    <!-- Configurações Visuais da Bella (Tamanho e Zoom) -->
    <link rel="stylesheet" href="configuracoes_bot.css">
    
    <style>
        :root {
            --primary: #3b82f6;
            --bg: #f8fafc;
            --card: #ffffff;
            --text: #1e293b;
            --msg-patient-bg: #dcfce7;
            --msg-patient-text: #14532d;
            --msg-agent-bg: #3b82f6;
            --msg-agent-text: #ffffff;
        }
        
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: system-ui, sans-serif; }
        
        body { 
            background: var(--bg); 
            color: var(--text); 
            display: flex; 
            flex-direction: column; 
            height: 100vh; 
        }

        /* Banner superior */
        .clinic-banner {
            background: var(--primary);
            color: white;
            padding: 1rem;
            text-align: center;
            font-weight: 700;
            font-size: 1.1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        /* Área do chat */
        .chat-container { 
            flex: 1; 
            overflow-y: auto; 
            padding: 1rem; 
            display: flex; 
            flex-direction: column; 
            gap: 0.8rem; 
        }
        
        .chat-msg { 
            max-width: 75%; 
            padding: 0.8rem 1rem; 
            border-radius: 14px; 
            font-size: 0.95rem; 
            line-height: 1.5; 
            word-wrap: break-word;
        }
        
        .chat-msg.patient { 
            background: var(--msg-patient-bg); 
            color: var(--msg-patient-text); 
            align-self: flex-start; 
            border-bottom-left-radius: 4px;
        }
        
        .chat-msg.agent { 
            background: var(--msg-agent-bg); 
            color: var(--msg-agent-text); 
            align-self: flex-end; 
            border-bottom-right-radius: 4px;
        }
        
        .chat-msg .meta { 
            font-size: 0.65rem; 
            opacity: 0.7; 
            margin-top: 4px; 
            text-align: right; 
        }

        /* Área de input */
        .input-area { 
            padding: 1rem; 
            background: var(--card); 
            border-top: 1px solid #e2e8f0; 
            display: flex; 
            gap: 0.8rem; 
        }
        
        .input-area input { 
            flex: 1; 
            padding: 0.9rem 1.2rem; 
            border-radius: 24px; 
            border: 1px solid #e2e8f0; 
            font-size: 0.95rem; 
        }
        
        .send-btn { 
            width: 46px; 
            height: 46px; 
            border-radius: 50%; 
            border: none; 
            background: var(--primary); 
            color: white; 
            font-size: 1.1rem; 
            cursor: pointer;
        }
        
        .send-btn:hover { background: #2563eb; }

        /* Botões de resposta rápida */
        .quick-btns { 
            display: flex; 
            gap: 0.5rem; 
            padding: 0.5rem 1rem; 
            overflow-x: auto; 
            background: var(--bg); 
        }
        
        .quick-btn { 
            background: white; 
            border: 1px solid #e2e8f0; 
            padding: 0.4rem 0.8rem; 
            border-radius: 16px; 
            font-size: 0.8rem; 
            cursor: pointer;
            white-space: nowrap;
        }
        
        .quick-btn:hover { 
            background: #f1f5f9; 
            border-color: var(--primary); 
        }

        /* Estilo para foto do bot no chat */
        .bot-avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            overflow: hidden;
            border: 2px solid var(--primary);
            margin-right: 8px;
        }
        
        .bot-avatar img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
    </style>
</head>

<body>
    <!-- Banner com nome da empresa -->
    <div class="clinic-banner" id="clinic-banner">
        🏥 Clínica Sorriso - Assistente Virtual
    </div>

    <!-- Área das mensagens -->
    <div class="chat-container" id="chat-container">
        <!-- Mensagem de boas-vindas -->
        <div class="chat-msg agent">
            <div class="bot-avatar">
                <img src="bot.png" alt="Bella" onerror="this.src='https://ui-avatars.com/api/?name=Bella&background=3b82f6&color=fff'">
            </div>
            <div>
                Olá! Sou a Bella, sua assistente virtual. Como posso ajudar você hoje?
                <div class="meta">Agora</div>
            </div>
        </div>
    </div>

    <!-- Botões de resposta rápida -->
    <div class="quick-btns" id="quick-btns">
        <button class="quick-btn" onclick="sendQuickMessage('Quero agendar um horário')">📅 Agendar</button>
        <button class="quick-btn" onclick="sendQuickMessage('Ver serviços e preços')">📋 Serviços</button>
        <button class="quick-btn" onclick="sendQuickMessage('Falar com atendente')">👤 Atendente</button>
        <button class="quick-btn" onclick="sendQuickMessage('Horário de funcionamento')">🕐 Horário</button>
    </div>

    <!-- Área de digitação -->
    <div class="input-area">
        <input type="text" id="user-input" placeholder="Digite sua mensagem..." onkeypress="if(event.key==='Enter') sendMessage()">
        <button class="send-btn" onclick="sendMessage()">➤</button>
    </div>

    <script>
        // Configurações
        const chatContainer = document.getElementById('chat-container');
        const userInput = document.getElementById('user-input');

        // Enviar mensagem rápida
        function sendQuickMessage(text) {
            userInput.value = text;
            sendMessage();
        }

        // Enviar mensagem
        function sendMessage() {
            const message = userInput.value.trim();
            if (!message) return;

            // Adiciona mensagem do usuário
            addMessage(message, 'patient');
            userInput.value = '';

            // Simula resposta do bot (aqui você integra com seu backend)
            setTimeout(() => {
                const resposta = gerarResposta(message);
                addMessage(resposta, 'agent');
            }, 1000);
        }

        // Adicionar mensagem ao chat
        function addMessage(text, type) {
            const msgDiv = document.createElement('div');
            msgDiv.className = `chat-msg ${type}`;
            
            if (type === 'agent') {
                msgDiv.innerHTML = `
                    <div class="bot-avatar">
                        <img src="bot.png" alt="Bella" onerror="this.src='https://ui-avatars.com/api/?name=Bella&background=3b82f6&color=fff'">
                    </div>
                    <div>
                        ${text}
                        <div class="meta">${new Date().toLocaleTimeString('pt-BR', {hour: '2-digit', minute:'2-digit'})}</div>
                    </div>
                `;
            } else {
                msgDiv.innerHTML = `
                    ${text}
                    <div class="meta">${new Date().toLocaleTimeString('pt-BR', {hour: '2-digit', minute:'2-digit'})}</div>
                `;
            }
            
            chatContainer.appendChild(msgDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }

        // Gerar resposta automática (simulação)
        function gerarResposta(mensagem) {
            const msg = mensagem.toLowerCase();
            
            if (msg.includes('agend') || msg.includes('horário')) {
                return "Ótimo! Para agendar, você pode clicar no botão 📅 Agendar ou me dizer qual serviço deseja e qual dia prefere!";
            }
            else if (msg.includes('serviço') || msg.includes('preço')) {
                return "Temos os seguintes serviços:\\n✂️ Corte Masculino - R$ 35\\n🧔 Barba Completa - R$ 25\\n💇 Combo Corte + Barba - R$ 50\\n\\nQual você gostaria?";
            }
            else if (msg.includes('atendente') || msg.includes('pessoa')) {
                return "Entendido! Vou transferir você para um de nossos atendentes humanos. Aguarde um momento...";
            }
            else if (msg.includes('horário') || msg.includes('funcionamento')) {
                return "Funcionamos:\\n📅 Seg a Sex: 9h às 18h\\n📅 Sáb: 9h às 13h";
            }
            else {
                return "Entendi! Como posso ajudar você com isso? Você pode me fazer perguntas sobre agendamentos, serviços ou preços.";
            }
        }

        // Mensagem de boas-vindas ao carregar
        window.onload = function() {
            console.log('✅ Simulador carregado com sucesso!');
            console.log('📸 Foto da Bella:', document.querySelector('.bot-avatar img').src);
        };
    </script>
</body>
</html>
"""

def corrigir_simulador():
    """Corrige o arquivo simulador.html"""
    caminho = PASTA / "simulador.html"
    
    try:
        # Salva o arquivo corrigido
        with open(caminho, 'w', encoding='utf-8') as f:
            f.write(SIMULADOR_CORRIGIDO)
        
        print("✅ simulador.html corrigido com sucesso!")
        print("📁 Arquivo salvo em:", caminho)
        print("\n🎯 O que foi corrigido:")
        print("   • Removida tag <head> duplicada")
        print("   • CSS organizado corretamente")
        print("   • Link para configuracoes_bot.css adicionado")
        print("   • Estrutura HTML padronizada")
        print("   • Chat funcional com respostas automáticas")
        print("\n🚀 Agora é só abrir o simulador.html no navegador!")
        
    except Exception as e:
        print(f"❌ Erro ao corrigir: {e}")

if __name__ == "__main__":
    print("="*60)
    print("🔧 CORRETOR AUTOMÁTICO - SIMULADOR.HTML")
    print("="*60)
    corrigir_simulador()
    print("="*60)