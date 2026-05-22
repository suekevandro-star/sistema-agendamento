# =====================================================
# 📦 MASTER SERVER - BACKEND COMPLETO
# Sistema de Agendamento + Bot WhatsApp
# =====================================================

# ─────────────────────────────────────────────────────
# 🔧 IMPORTAÇÕES E CONFIGURAÇÕES GLOBAIS
# ─────────────────────────────────────────────────────
import os, json, hashlib
from pathlib import Path
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import FastAPI, Request, Form, Query
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import sqlite3

# Configurações do sistema
MASTER_PASSWORD = os.getenv("ADMIN_PASSWORD", "evandro123")
PORT = int(os.getenv("PORT", 10000))
TZ_SP = timezone(timedelta(hours=-3))
PROJECT_DIR = Path(__file__).parent

# Diretório do banco de dados
def get_db_dir():
    db_path = Path("/tmp/sistema_agenda") if os.getenv("RENDER") or os.name == 'posix' else PROJECT_DIR
    db_path.mkdir(parents=True, exist_ok=True)
    return db_path

DB_DIR = get_db_dir()
DB_FILE = DB_DIR / "agenda.db"

# ─────────────────────────────────────────────────────
# 💾 GERENCIAMENTO DE SESSÕES DO BOT
# ─────────────────────────────────────────────────────
class SessionStore:
    """Armazena o estado das conversas do bot por sessão"""
    def __init__(self):
        self.cache = {}
        self.file_path = DB_DIR / "sessoes_bot.json"
        self._load()
    
    def _load(self):
        try:
            if self.file_path.exists():
                with open(self.file_path, "r", encoding="utf-8") as f:
                    self.cache = json.load(f)
        except: self.cache = {}
    
    def _save(self):
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self.cache, f)
        except: pass
    
    def get(self, k, d=None): return self.cache.get(k, d)
    def set(self, k, v): self.cache[k] = v; self._save()
    def delete(self, k): self.cache.pop(k, None); self._save()

sessions = SessionStore()

# ─────────────────────────────────────────────────────
# 🗄️ CONEXÃO COM BANCO DE DADOS
# ─────────────────────────────────────────────────────
USE_POSTGRES = False
db_url = os.getenv("DATABASE_URL", "")

if db_url and (db_url.startswith("postgres://") or db_url.startswith("postgresql://")):
    try:
        import psycopg2
        from psycopg2.extras import RealDictCursor
        conn_test = psycopg2.connect(db_url); conn_test.close()
        USE_POSTGRES = True
    except: USE_POSTGRES = False

def get_db():
    """Retorna conexão com o banco (PostgreSQL ou SQLite)"""
    if USE_POSTGRES:
        try: return psycopg2.connect(db_url, cursor_factory=RealDictCursor)
        except: pass
    conn = sqlite3.connect(DB_FILE, timeout=10.0)
    conn.row_factory = sqlite3.Row
    return conn

def _get(row, f):
    """Acessa campo de forma segura em dict ou tuple"""
    if row is None: return None
    try: return row.get(f)
    except: return row[f]

def _p(): return "%s" if USE_POSTGRES else "?"

def get_config_hash(cfg_dict: dict) -> str:
    """Gera hash curto para detectar mudanças na config"""
    return hashlib.md5(json.dumps(cfg_dict, sort_keys=True).encode()).hexdigest()[:8]

# ─────────────────────────────────────────────────────
# 🏗️ INICIALIZAÇÃO DO BANCO DE DADOS
# ─────────────────────────────────────────────────────
def init_db():
    """Cria tabelas se não existirem"""
    print(f"🗄️ CAMINHO DO BANCO: {DB_FILE}")
    try:
        conn = get_db(); c = conn.cursor()
        if USE_POSTGRES:
            c.execute("CREATE TABLE IF NOT EXISTS clinicas (id SERIAL PRIMARY KEY, nome TEXT, config JSONB)")
        else:
            c.executescript('''
                CREATE TABLE IF NOT EXISTS clinicas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    nome TEXT, 
                    config TEXT
                );
                CREATE TABLE IF NOT EXISTS profissionais (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    clinica_id INT, 
                    nome TEXT, 
                    especialidade TEXT, 
                    pausas TEXT DEFAULT '[]'
                );
                CREATE TABLE IF NOT EXISTS servicos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    clinica_id INT, 
                    nome TEXT, 
                    preco TEXT, 
                    duracao INT DEFAULT 60, 
                    icone TEXT DEFAULT '🦷'
                );
                CREATE TABLE IF NOT EXISTS agendamentos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    clinica_id INT, 
                    session_id TEXT, 
                    paciente TEXT, 
                    telefone TEXT, 
                    servico_id INT, 
                    data TEXT, 
                    hora TEXT, 
                    status TEXT DEFAULT 'confirmado', 
                    observacoes TEXT
                );
                CREATE TABLE IF NOT EXISTS solicitacoes_atendimento (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    clinica_id INT, 
                    session_id TEXT, 
                    nome_paciente TEXT, 
                    mensagem TEXT, 
                    data_hora TEXT, 
                    status TEXT DEFAULT 'pendente', 
                    resposta_atendente TEXT, 
                    observacoes TEXT
                );
                CREATE TABLE IF NOT EXISTS profissional_servicos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    profissional_id INT, 
                    servico_id INT, 
                    ativo INT DEFAULT 1
                );
                CREATE TABLE IF NOT EXISTS admin_config (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    email TEXT, 
                    whatsapp TEXT, 
                    instagram TEXT
                );
                CREATE TABLE IF NOT EXISTS mensagens_chat (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    ticket_id INT, 
                    remetente TEXT, 
                    mensagem TEXT, 
                    data_hora TEXT, 
                    lida INT DEFAULT 0
                );
            ''')
            # Adiciona colunas faltantes (migração)
            for col, tbl in [
                ('session_id', 'solicitacoes_atendimento'),
                ('resposta_atendente', 'solicitacoes_atendimento'),
                ('observacoes', 'solicitacoes_atendimento'),
                ('session_id', 'agendamentos'),
                ('telefone', 'agendamentos'),
                ('icone', 'servicos')
            ]:
                try: c.execute(f"ALTER TABLE {tbl} ADD COLUMN {col} TEXT")
                except: pass
        conn.commit(); conn.close()
        print("✅ Banco atualizado!")
    except Exception as e: print(f"❌ Erro init_db: {e}")

def seed():
    """Insere dados iniciais se necessário"""
    try:
        conn = get_db(); c = conn.cursor()
        c.execute("SELECT id FROM clinicas")
        for cl in c.fetchall():
            cid = cl['id'] if isinstance(cl, dict) else cl[0]
            if c.execute(f"SELECT COUNT(*) FROM servicos WHERE clinica_id={_p()}", (cid,)).fetchone()[0] == 0:
                for n,p,d,icone in [("Consulta","100",30,"🩺"),("Limpeza","150",45,"🦷")]: 
                    c.execute(f"INSERT INTO servicos (clinica_id, nome, preco, duracao, icone) VALUES ({_p()}, {_p()}, {_p()}, {_p()}, {_p()})", (cid,n,p,d,icone))
        conn.commit(); conn.close()
    except: pass

# ─────────────────────────────────────────────────────
# 🌐 CONFIGURAÇÃO DO FASTAPI
# ─────────────────────────────────────────────────────
app = FastAPI(title="Sistema de Agendamento", version="1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Inicializa ao iniciar o servidor
init_db(); seed()

# ─────────────────────────────────────────────────────
# 🔐 ROTAS DE AUTENTICAÇÃO
# ─────────────────────────────────────────────────────
@app.get("/login", response_class=HTMLResponse)
async def login_page():
    return FileResponse(PROJECT_DIR / "torre.html")

@app.post("/verificar")
async def verificar_senha(request: Request, senha: str = Form(...)):
    if senha == MASTER_PASSWORD:
        r = RedirectResponse(url="/torre", status_code=302)
        r.set_cookie("admin_auth", "ok", httponly=True, path="/", samesite="lax")
        return r
    return RedirectResponse(url="/login?erro=1")

@app.middleware("http")
async def check_auth(req, call_next):
    return await call_next(req)

# ─────────────────────────────────────────────────────
# 📄 ROTAS DE PÁGINAS HTML
# ─────────────────────────────────────────────────────
@app.get("/torre", response_class=HTMLResponse)
async def torre(): return FileResponse(PROJECT_DIR / "torre.html")

@app.get("/painel", response_class=HTMLResponse)
async def painel(): return FileResponse(PROJECT_DIR / "painel.html")

@app.get("/simulador", response_class=HTMLResponse)
async def simulador(): return FileResponse(PROJECT_DIR / "simulador.html")

# Rota para servir arquivos estáticos (CSS, JS, imagens)
@app.get("/style.css", response_class=HTMLResponse)
async def style_css():
    return FileResponse(PROJECT_DIR / "style.css")

@app.get("/script.js")
async def script_js():
    return FileResponse(PROJECT_DIR / "script.js")

@app.get("/bot.png")
async def bot_image():
    return FileResponse(PROJECT_DIR / "bot.png")

@app.get("/", response_class=HTMLResponse)
async def index(): 
    return FileResponse(PROJECT_DIR / "index.html")

# ─────────────────────────────────────────────────────
# 🏥 ROTAS: CLÍNICAS E CONFIGURAÇÕES
# ─────────────────────────────────────────────────────
@app.get("/api/clinicas")
async def listar_clinicas():
    """Lista todas as clínicas cadastradas"""
    try:
        conn = get_db(); c = conn.cursor()
        c.execute("SELECT id, nome, config FROM clinicas")
        rows = c.fetchall(); conn.close()
        return [{
            "id": _get(r,'id'), 
            "nome": _get(r,'nome'), 
            "config": json.loads(_get(r,'config')) if isinstance(_get(r,'config'), str) else _get(r,'config')
        } for r in rows]
    except Exception as e: return {"error": str(e)}

@app.post("/api/clinicas")
async def criar_clinica(req: Request):
    """Cria nova clínica com dados iniciais"""
    try:
        d = await req.json()
        nm = d.get("nome", "Nova")
        cfg = {"inicio":"08:00","fim":"18:00","intervalo":0}
        
        conn = get_db(); c = conn.cursor()
        c.execute(f"INSERT INTO clinicas (nome, config) VALUES ({_p()}, {_p()})", (nm, json.dumps(cfg)))
        cid = c.lastrowid if not USE_POSTGRES else c.fetchone()['id']
        
        # Cria profissional padrão
        c.execute(f"INSERT INTO profissionais (clinica_id, nome, especialidade) VALUES ({_p()}, {_p()}, {_p()})", 
                 (cid, "Profissional Padrão", "Geral"))
        
        # Cria serviços padrão
        for nome, preco, dur, icone in [('Consulta Inicial', '100', 30, '🩺'), ('Limpeza Completa', '150', 45, '🦷')]:
            c.execute(f"INSERT INTO servicos (clinica_id, nome, preco, duracao, icone) VALUES ({_p()}, {_p()}, {_p()}, {_p()}, {_p()})", 
                     (cid, nome, preco, dur, icone))
        
        conn.commit(); conn.close()
        return {"success": True, "id": cid}
    except Exception as e: return {"error": str(e)}

@app.get("/api/c/{cid}/config")
async def get_config(cid: int):
    """
    Retorna configurações de uma clínica.
    ✅ CORREÇÃO: nome_clinica vem SEMPRE da coluna 'nome' da tabela
    """
    try:
        conn = get_db(); c = conn.cursor()
        c.execute(f"SELECT nome, config FROM clinicas WHERE id={_p()}", (cid,))
        row = c.fetchone(); conn.close()
        
        # Valores padrão
        default = {
            "inicio":"08:00", "fim":"18:00", "intervalo":0,
            "fuso":"America/Sao_Paulo",
            "dias":["seg","ter","qua","qui","sex","sab"],
            "nome_bot":"Bella",
            "msg_boas_vindas":"Olá, bem-vindo(a) à {clinica}. Eu sou a {bot}. Como posso ajudar?"
        }
        
        if not row: 
            return {"nome_clinica": "Clínica", "nome": "Clínica", **default}
        
        # 🏢 Nome vem DA COLUNA 'nome' (garantido, não do JSON)
        nome_da_tabela = row['nome'] or "Clínica"
        
        # Parse do config JSON
        cfg_raw = row['config']
        cfg = {}
        if cfg_raw:
            try:
                cfg = json.loads(cfg_raw) if isinstance(cfg_raw, str) else cfg_raw
            except: cfg = {}
        
        # 🗑️ Remove chaves conflitantes do JSON para não sobrescrever o nome
        cfg.pop('nome_clinica', None)
        cfg.pop('nome', None)
        
        # ✅ Monta retorno: nome_da_tabela TEM PRIORIDADE MÁXIMA
        resultado = {}
        resultado.update(default)      # 1. Valores padrão
        resultado.update(cfg)          # 2. Configs do JSON
        resultado['nome_clinica'] = nome_da_tabela  # 3. Nome da tabela (SOBRESCREVE tudo)
        resultado['nome'] = nome_da_tabela          # 4. Fallback
        
        return resultado
    except Exception as e: 
        print(f"❌ Erro get_config: {e}")
        return {"error": str(e)}

@app.put("/api/c/{cid}/config")
async def update_config(cid: int, req: Request):
    """
    Atualiza configurações de uma clínica.
    ✅ CORREÇÃO: nome_clinica é salvo na coluna 'nome' da tabela
    """
    try:
        d = await req.json()
        conn = get_db(); c = conn.cursor()
        
        # 🏢 SALVA O NOME NA COLUNA 'nome' DA TABELA PRINCIPAL
        if 'nome_clinica' in d and d['nome_clinica']:
            c.execute(f"UPDATE clinicas SET nome={_p()} WHERE id={_p()}", 
                     (d['nome_clinica'], cid))
            print(f"✅ [BACKEND] Nome atualizado: {d['nome_clinica']}")
        
        # 📦 Carrega config JSON existente para merge
        c.execute(f"SELECT config FROM clinicas WHERE id={_p()}", (cid,))
        row = c.fetchone()
        old = {}
        try: 
            if row and row['config']: 
                old = row['config'] if isinstance(row['config'], dict) else json.loads(row['config'])
        except: pass
        
        # 🔀 Merge: mantém configs antigas + aplica novas (exceto nome_clinica)
        new_cfg = {**old, **{k:v for k,v in d.items() if k != 'nome_clinica'}}
        new_cfg.pop('nome_clinica', None)  # Garante que não vai no JSON
        
        # Valores padrão se não existirem
        if 'nome_bot' not in new_cfg: new_cfg['nome_bot'] = old.get('nome_bot', 'Bella')
        if 'msg_boas_vindas' not in new_cfg: new_cfg['msg_boas_vindas'] = old.get('msg_boas_vindas', '')
        if 'allow_avatar_change' not in new_cfg: new_cfg['allow_avatar_change'] = False
        
        # Salva config JSON
        c.execute(f"UPDATE clinicas SET config={_p()} WHERE id={_p()}", 
                 (json.dumps(new_cfg, ensure_ascii=False), cid))
        
        conn.commit()
        
        # 🔐 Verificação: confirma que o nome foi salvo corretamente
        c.execute(f"SELECT nome FROM clinicas WHERE id={_p()}", (cid,))
        verify = c.fetchone()
        nome_confirmado = verify['nome'] if verify else "N/A"
        print(f"🔐 [VERIFICAÇÃO] Nome CONFIRMADO no banco: '{nome_confirmado}'")
        
        conn.close()
        return {"success": True, "nome_confirmado": nome_confirmado}
        
    except Exception as e: 
        print(f"❌ [BACKEND] Erro update_config: {e}")
        return {"error": str(e)}

# ─────────────────────────────────────────────────────
# 📅 ROTAS: AGENDA E AGENDAMENTOS
# ─────────────────────────────────────────────────────
@app.get("/api/c/{cid}/agenda")
async def get_agenda(cid: int, data: str = None, search: str = None, prof_id: str = None):
    """Lista agendamentos com filtros"""
    try:
        conn = get_db(); c = conn.cursor()
        query = f"""
            SELECT a.id, a.paciente, a.servico_id, a.data, a.hora, a.status, a.observacoes, p.nome as prof_nome 
            FROM agendamentos a 
            LEFT JOIN profissionais p ON a.profissional_id=p.id 
            WHERE a.clinica_id={_p()}
        """
        params = [cid]
        if prof_id: query += f" AND a.profissional_id={_p()}"; params.append(prof_id)
        query += " ORDER BY a.data, a.hora"
        
        c.execute(query, tuple(params))
        rows = c.fetchall(); conn.close()
        
        result = []
        for r in rows:
            dt = str(_get(r,'data') or ''); hr = str(_get(r,'hora') or '')
            if data and not dt.startswith(data): continue
            if search and search.lower() not in str(_get(r,'paciente')).lower(): continue
            result.append({
                "id": _get(r,'id'), 
                "paciente": _get(r,'paciente'), 
                "servico_id": _get(r,'servico_id'), 
                "inicio": f"{dt} {hr}", 
                "status": _get(r,'status') or 'confirmado', 
                "observacoes": _get(r,'observacoes') or '', 
                "profissional": _get(r,'prof_nome')
            })
        return {"agendamentos": result}
    except Exception as e: return {"error": str(e), "agendamentos": []}

@app.put("/api/agendamento/{aid}")
async def atualizar_agendamento(aid: int, req: Request):
    """Atualiza status ou observações de um agendamento"""
    try:
        d = await req.json()
        conn = get_db(); c = conn.cursor()
        fields, vals = [], []
        if 'status' in d: fields.append(f"status={_p()}"); vals.append(d['status'])
        if 'observacoes' in d: fields.append(f"observacoes={_p()}"); vals.append(d['observacoes'])
        if fields: 
            vals.append(aid)
            c.execute(f"UPDATE agendamentos SET {', '.join(fields)} WHERE id={_p()}", tuple(vals))
            conn.commit()
        conn.close()
        return {"success": True}
    except Exception as e: return {"error": str(e)}

@app.delete("/api/agendamento/{aid}")
async def deletar_agendamento(aid: int):
    """Exclui um agendamento"""
    try: 
        conn = get_db(); c = conn.cursor()
        c.execute(f"DELETE FROM agendamentos WHERE id={_p()}", (aid,))
        conn.commit(); conn.close()
        return {"success": True}
    except Exception as e: return {"error": str(e)}

# ─────────────────────────────────────────────────────
# 👨‍⚕️ ROTAS: PROFISSIONAIS
# ─────────────────────────────────────────────────────
@app.get("/api/c/{cid}/profissionais")
async def listar_profissionais(cid: int):
    """Lista profissionais de uma clínica"""
    try: 
        conn = get_db(); c = conn.cursor()
        c.execute(f"SELECT id, nome, especialidade, pausas FROM profissionais WHERE clinica_id={_p()}", (cid,))
        rows = c.fetchall(); conn.close()
        return [{
            "id":_get(p,'id'), 
            "nome":_get(p,'nome'), 
            "especialidade":_get(p,'especialidade'), 
            "pausas": json.loads(_get(p,'pausas')) if isinstance(_get(p,'pausas'), str) else (_get(p,'pausas') or [])
        } for p in rows]
    except Exception as e: return {"error": str(e)}

@app.post("/api/c/{cid}/profissionais")
async def criar_profissional(cid: int, req: Request):
    """Cria novo profissional"""
    try:
        d = await req.json()
        conn = get_db(); c = conn.cursor()
        c.execute(f"INSERT INTO profissionais (clinica_id, nome, especialidade) VALUES ({_p()}, {_p()}, {_p()})", 
                 (cid, d['nome'], d.get('especialidade','')))
        pid = c.lastrowid if not USE_POSTGRES else c.fetchone()['id']
        conn.commit(); conn.close()
        return {"success": True, "id": pid}
    except Exception as e: return {"error": str(e)}

@app.put("/api/profissionais/{pid}")
async def atualizar_profissional(pid: int, req: Request):
    """Atualiza dados de um profissional"""
    try:
        d = await req.json()
        conn = get_db(); c = conn.cursor()
        c.execute(f"UPDATE profissionais SET nome={_p()}, especialidade={_p()}, pausas={_p()} WHERE id={_p()}", 
                 (d['nome'], d.get('especialidade',''), json.dumps(d.get('pausas',[])), pid))
        conn.commit(); conn.close()
        return {"success": True}
    except Exception as e: return {"error": str(e)}

@app.delete("/api/profissionais/{pid}")
async def deletar_profissional(pid: int):
    """Exclui um profissional"""
    try: 
        conn = get_db(); c = conn.cursor()
        c.execute(f"DELETE FROM profissionais WHERE id={_p()}", (pid,))
        conn.commit(); conn.close()
        return {"success": True}
    except Exception as e: return {"error": str(e)}

# ─────────────────────────────────────────────────────
# 📋 ROTAS: SERVIÇOS
# ─────────────────────────────────────────────────────
@app.get("/api/c/{cid}/servicos")
async def listar_servicos(cid: int):
    """Lista serviços de uma clínica"""
    try: 
        conn = get_db(); c = conn.cursor()
        c.execute(f"SELECT id, nome, preco, duracao, icone FROM servicos WHERE clinica_id={_p()}", (cid,))
        rows = c.fetchall(); conn.close()
        return [{
            "id":_get(r,'id'),
            "nome":_get(r,'nome'),
            "preco":_get(r,'preco'),
            "duracao":_get(r,'duracao'),
            "icone":_get(r,'icone') or '🦷'
        } for r in rows]
    except Exception as e: return {"error": str(e)}

@app.post("/api/c/{cid}/servicos")
async def salvar_servico(cid: int, req: Request):
    """Cria ou atualiza serviço"""
    try: 
        d = await req.json()
        conn = get_db(); c = conn.cursor()
        c.execute(f"INSERT INTO servicos (clinica_id, nome, preco, duracao, icone) VALUES ({_p()}, {_p()}, {_p()}, {_p()}, {_p()})", 
                 (cid,d['nome'],d['preco'],d['duracao'], d.get('icone','🦷')))
        conn.commit(); conn.close()
        return {"success": True}
    except Exception as e: return {"error": str(e)}

@app.put("/api/servicos/{sid}")
async def atualizar_servico(sid: int, req: Request):
    """Atualiza serviço existente"""
    try: 
        d = await req.json()
        conn = get_db(); c = conn.cursor()
        c.execute(f"UPDATE servicos SET nome={_p()}, preco={_p()}, duracao={_p()}, icone={_p()} WHERE id={_p()}", 
                 (d['nome'],d['preco'],d['duracao'], d.get('icone','🦷'),sid))
        conn.commit(); conn.close()
        return {"success": True}
    except Exception as e: return {"error": str(e)}

@app.delete("/api/servicos/{sid}")
async def deletar_servico(sid: int):
    """Exclui serviço"""
    try: 
        conn = get_db(); c = conn.cursor()
        c.execute(f"DELETE FROM servicos WHERE id={_p()}", (sid,))
        conn.commit(); conn.close()
        return {"success": True}
    except Exception as e: return {"error": str(e)}

# ─────────────────────────────────────────────────────
# 💬 ROTAS: ATENDIMENTOS / TICKETS
# ─────────────────────────────────────────────────────
@app.get("/api/c/{cid}/atendimentos")
async def get_atendimentos(cid: int, status: str = None):
    """Lista solicitações de atendimento"""
    try:
        conn = get_db(); c = conn.cursor()
        query = f"SELECT id, session_id, nome_paciente, mensagem, status, data_hora, resposta_atendente, observacoes FROM solicitacoes_atendimento WHERE clinica_id={_p()}"
        params = [cid]
        if status and status != 'todos': query += f" AND status={_p()}"; params.append(status)
        query += " ORDER BY data_hora DESC"
        
        c.execute(query, tuple(params))
        rows = c.fetchall(); conn.close()
        return [{
            "id": _get(r,'id'), 
            "session_id": _get(r,'session_id'), 
            "paciente": _get(r,'nome_paciente'), 
            "motivo": _get(r,'mensagem'), 
            "status": _get(r,'status') or 'pendente', 
            "data_hora": _get(r,'data_hora'), 
            "resposta": _get(r,'resposta_atendente'), 
            "observacoes": _get(r,'observacoes')
        } for r in rows]
    except Exception as e: return {"error": str(e)}

@app.post("/atendimento/{ticket_id}/responder")
async def responder_ticket(ticket_id: int, req: Request):
    """Atendente responde uma solicitação"""
    try:
        d = await req.json()
        msg = d.get("mensagem", "").strip()
        if not msg: return {"error": "Mensagem vazia"}
        conn = get_db(); c = conn.cursor()
        c.execute(f"UPDATE solicitacoes_atendimento SET resposta_atendente={_p()}, status='respondido' WHERE id={_p()}", 
                 (msg, ticket_id))
        conn.commit(); conn.close()
        return {"success": True}
    except Exception as e: return {"error": str(e)}

@app.post("/api/atendimento/{ticket_id}/status")
async def atualizar_status_ticket(ticket_id: int, req: Request):
    """Atualiza status de um ticket"""
    try:
        d = await req.json()
        if not d.get("status"): return {"error": "Status inválido"}
        conn = get_db(); c = conn.cursor()
        c.execute(f"UPDATE solicitacoes_atendimento SET status={_p()}, observacoes={_p()} WHERE id={_p()}", 
                 (d["status"], d.get("observacoes"), ticket_id))
        conn.commit(); conn.close()
        return {"success": True}
    except Exception as e: return {"error": str(e)}

@app.delete("/api/atendimento/{ticket_id}")
async def deletar_ticket(ticket_id: int):
    """Exclui ticket"""
    try: 
        conn = get_db(); c = conn.cursor()
        c.execute(f"DELETE FROM solicitacoes_atendimento WHERE id={_p()}", (ticket_id,))
        conn.commit(); conn.close()
        return {"success": True}
    except Exception as e: return {"error": str(e)}

@app.get("/api/sessao/resposta")
async def check_resposta_atendente(sid: Optional[str] = Query(None)):
    """Verifica se há resposta pendente para uma sessão"""
    try:
        if not sid: return {"resposta": None}
        conn = get_db(); c = conn.cursor()
        c.execute(f"SELECT id, resposta_atendente FROM solicitacoes_atendimento WHERE session_id={_p()} AND status='respondido'", (sid,))
        row = c.fetchone()
        if row:
            resposta = _get(row, 'resposta_atendente')
            ticket_id = _get(row, 'id')
            c.execute(f"UPDATE solicitacoes_atendimento SET status='pendente', resposta_atendente=NULL WHERE id={_p()}", (ticket_id,))
            conn.commit()
        else: resposta = None
        conn.close()
        return {"resposta": resposta}
    except Exception as e: return {"resposta": None}

# ─────────────────────────────────────────────────────
# 🤖 BOT WHATSAPP - FLUXO DE CONVERSA
# ─────────────────────────────────────────────────────
@app.post("/mensagem")
async def receber_mensagem(req: Request):
    """Endpoint principal do bot WhatsApp"""
    try:
        body = await req.json()
        txt = body.get("text","").strip()
        sid = body.get("session_id","default")
        cid_req = body.get("clinica_id",1)
        
        # Inicia nova sessão
        if txt in ["INICIAR", "0"]:
            sessions.delete(sid)
            sessions.set(sid, {"step":"inicio", "ja_saudado":False, "clinica_id":cid_req})
        
        s = sessions.get(sid) or {"step":"inicio", "ja_saudado":False, "clinica_id":cid_req}
        sessions.set(sid, s)
        cid = s.get("clinica_id", 1)
        step = s.get("step", "inicio")
        
        # Carrega config da clínica
        conn = get_db(); c = conn.cursor()
        nome_clinica = "Clínica"; bot_name = "Bella"; msg_custom = ""; config_hash = ""
        try:
            c.execute(f"SELECT nome, config FROM clinicas WHERE id={_p()}", (cid,))
            r = c.fetchone()
            if r:
                nome_clinica = _get(r, 'nome') or "Clínica"  # ← Nome da coluna
                cfg_raw = _get(r, 'config')
                cfg = cfg_raw if isinstance(cfg_raw, dict) else (json.loads(cfg_raw) if cfg_raw and isinstance(cfg_raw, str) else {})
                bot_name = str(cfg.get('nome_bot', 'Bella')).strip()
                msg_custom = str(cfg.get('msg_boas_vindas', '') or '').strip()
                config_hash = get_config_hash(cfg)
        except: pass

        sync_meta = {"bot_name": bot_name, "clinica_nome": nome_clinica, "msg_boas_vindas": msg_custom, "config_hash": config_hash}
        
        menu_botoes = [
            {"texto": "📅 QUERO AGENDAR", "payload": "agendamento"},
            {"texto": "📋 Serviços", "payload": "2"},
            {"texto": "📅 Meus Agendamentos", "payload": "3"},
            {"texto": "👤 Atendente", "payload": "4"}
        ]
        
        def resp(txt, botoes=None, **kwargs):
            return {"resposta": txt, "botoes": botoes, **kwargs}
        
        # === FLUXO DA CONVERSA ===
        
        if txt == "INICIAR":
            s["step"] = "pedindo_nome"; s["ja_saudado"] = True
            sessions.set(sid, s)
            return resp(f"***👋 OLÁ! BEM-VINDO(A)!***\n***Eu sou a {bot_name}, sua assistente virtual.***\n\nPara começarmos, qual é o seu nome completo?", **sync_meta)

        elif step == "pedindo_nome":
            nome_digitado = txt.strip().title()
            if len(nome_digitado) < 3:
                return resp("***Por favor, digite seu nome completo:***", **sync_meta)
            s["nome_paciente"] = nome_digitado; s["step"] = "menu_principal"
            sessions.set(sid, s)
            return resp(f"***Prazer, {nome_digitado}! 😊***\n\n***Como posso te ajudar?***", botoes=menu_botoes, **sync_meta)

        elif step == "menu_principal":
            if txt == "agendamento":
                s["step"] = "agendamento_servico"; sessions.set(sid, s)
                servicos = c.execute("SELECT id, nome, icone FROM servicos WHERE clinica_id=? LIMIT 6", (cid_req,)).fetchall()
                botoes = [{"texto": f"{r[2]} {r[1]}", "payload": f"serv:{r[0]}"} for r in servicos]
                botoes.append({"texto": "← Menu", "payload": "menu_principal"})
                return resp("*Qual serviço deseja agendar?*", botoes=botoes, **sync_meta)
            elif txt in ["2", "Serviços"]:
                sv = c.execute("SELECT id, nome, preco, duracao FROM servicos WHERE clinica_id=?", (cid_req,)).fetchall()
                if sv:
                    msg = "*📋 NOSSOS SERVIÇOS:*\n\n" + "\n".join([f"*{i}.* {x[1]} (R$ {x[2]})" for i,x in enumerate(sv,1)])
                    return resp(msg, botoes=menu_botoes, **sync_meta)
                return resp("*Nenhum serviço disponível.*", botoes=menu_botoes, **sync_meta)
            elif txt == "3":
                return resp("*📅 MEUS AGENDAMENTOS*\n\n*Consulte seus agendamentos no painel ou aguarde a confirmação.*", botoes=menu_botoes, **sync_meta)
            elif txt in ["4", "Atendente"]:
                nome_paciente = s.get("nome_paciente", "Cliente")
                try:
                    agora = datetime.now(TZ_SP).strftime("%Y-%m-%d %H:%M")
                    c.execute(f"INSERT INTO solicitacoes_atendimento (clinica_id, session_id, nome_paciente, mensagem, data_hora, status) VALUES ({_p()}, {_p()}, {_p()}, {_p()}, {_p()}, 'pendente')", 
                             (cid_req, sid, nome_paciente, f"👤 *{nome_paciente}* solicitou atendimento", agora))
                    conn.commit()
                    return resp(f"*✅ SOLICITAÇÃO ENVIADA!*\n\n*Um atendente da {nome_clinica} retornará em breve.*", botoes=menu_botoes, **sync_meta)
                except Exception as e:
                    return resp(f"*❌ Erro:* {e}", botoes=menu_botoes, **sync_meta)
            else:
                return resp(f"*Prazer, {s.get('nome_paciente', 'Cliente')}! Como posso te ajudar?*", botoes=menu_botoes, **sync_meta)

        elif step == "agendamento_servico" and txt.startswith("serv:"):
            try:
                serv_id = int(txt.split(":")[1])
                s["serv_id"] = serv_id; s["step"] = "agendamento_dia"; sessions.set(sid, s)
                serv_nome = c.execute("SELECT nome FROM servicos WHERE id=?", (serv_id,)).fetchone()
                nome_serv = serv_nome[0] if serv_nome else "Serviço"
                s["nome_servico"] = nome_serv
                botoes = [
                    {"texto": "📆 HOJE", "payload": "dia:hoje"},
                    {"texto": "📆 AMANHÃ", "payload": "dia:amanha"},
                    {"texto": "📅 Outro dia", "payload": "dia:outro"},
                    {"texto": "← Menu", "payload": "menu_principal"}
                ]
                conn.close()
                return resp(f"*Você escolheu: {nome_serv}*\n\n*Para qual dia prefere?*", botoes=botoes, **sync_meta)
            except Exception as e:
                conn.close()
                return resp(f"*Erro ao processar serviço:* {str(e)}", botoes=menu_botoes, **sync_meta)

        elif step == "agendamento_dia" and txt.startswith("dia:"):
            dia = txt.split(":")[1]; s["dia"] = dia; s["step"] = "agendamento_hora"; sessions.set(sid, s)
            horarios = ["08:00", "09:00", "10:00", "14:00", "15:00", "16:00"]
            botoes = [{"texto": f"🕒 {h}", "payload": f"hora:{h}"} for h in horarios]
            botoes.append({"texto": "← Voltar", "payload": "agendamento_servico"})
            label = "Hoje" if dia=="hoje" else "Amanhã" if dia=="amanha" else "o dia escolhido"
            return resp(f"*Horários disponíveis para {label}:*", botoes=botoes, **sync_meta)

        elif step == "agendamento_hora" and txt.startswith("hora:"):
            hora = txt.split(":")[1]; s["hora"] = hora; s["step"] = "agendamento_confirmar"; sessions.set(sid, s)
            botoes = [
                {"texto": "✅ SIM, CONFIRMAR", "payload": "confirma_sim"},
                {"texto": "❌ NÃO, VOLTAR", "payload": "agendamento_dia"},
                {"texto": "← Menu", "payload": "menu_principal"}
            ]
            msg = f"*Resumo do Agendamento:*\n\n* Serviço:* {s.get('nome_servico')}\n* Dia:* {s.get('dia')}\n* Horário:* {hora}\n\n*Está tudo certo?*"
            return resp(msg, botoes=botoes, **sync_meta)

        elif txt == "confirma_sim":
            s["step"] = "pedindo_telefone"; sessions.set(sid, s)
            return resp("*Perfeito! Para te enviar um lembrete, qual seu WhatsApp?*\n\n*Digite apenas números (ex: 11999887766):*", 
                       botoes=[{"texto": "← Voltar", "payload": "agendamento_hora"}], **sync_meta)

        elif step == "pedindo_telefone":
            tel = txt.strip()
            if not tel.isdigit() or len(tel) < 10:
                return resp("*Ops! Parece que faltou número.*\n\n*Digite apenas números (ex: 11999887766):*", 
                           botoes=[{"texto": "← Voltar", "payload": "agendamento_hora"}], **sync_meta)
            try:
                c.execute("INSERT INTO agendamentos (clinica_id, session_id, paciente, telefone, servico_id, data, hora, status) VALUES (?, ?, ?, ?, ?, ?, ?, 'confirmado')", 
                         (cid_req, sid, s.get("nome_paciente"), tel, s.get("serv_id"), s.get("dia"), s.get("hora")))
                conn.commit()
                s["step"] = "menu_principal"; sessions.set(sid, s)
                return resp("*🎉 AGENDADO COM SUCESSO!*\n\n*Você receberá um lembrete no WhatsApp.*\n\n*Posso ajudar em mais algo?*", botoes=menu_botoes, **sync_meta)
            except Exception as e:
                return resp(f"*❌ Erro ao salvar:* {e}", botoes=menu_botoes, **sync_meta)
        
        conn.close()
        return resp(f"*Olá! Como posso ajudar?*", botoes=menu_botoes, **sync_meta)
        
    except Exception as e: 
        return {"resposta": f"❌ Erro: {str(e)[:100]}"}

# ==========================================
# 🌐 API DE CONFIGURAÇÕES GLOBAIS (SYNC NA NUVEM)
# ==========================================
# 📍 ADICIONADO: Rotas para sincronização de configs entre painel e site

@app.get("/api/config")
async def get_config_global():
    """
    Retorna configurações globais do sistema.
    Usa clinica_id=1 como padrão para sistema single-tenant.
    Estrutura retornada:
    {
        "nome_empresa": "Evandro Suek",
        "subtitulo": "Sistemas Automatizados",
        "nome_bot": "Bella",
        "fuso_horario": "America/Sao_Paulo",
        "horarios_dia": { "segunda": {"ativo": true, "inicio": "08:00", "fim": "17:00"}, ... }
    }
    """
    try:
        conn = get_db()
        c = conn.cursor()
        
        # Busca config da clínica principal (id=1)
        c.execute(f"SELECT nome, config FROM clinicas WHERE id={_p()}", (1,))
        row = c.fetchone()
        conn.close()
        
        # Valores padrão (fallback se não houver config salva)
        default_config = {
            "nome_empresa": "Evandro Suek",
            "subtitulo": "Sistemas Automatizados de Atendimento",
            "nome_bot": "Bella",
            "fuso_horario": "America/Sao_Paulo",
            "horarios_dia": {
                "segunda": {"ativo": True, "inicio": "08:00", "fim": "17:00"},
                "terca": {"ativo": True, "inicio": "08:00", "fim": "17:00"},
                "quarta": {"ativo": True, "inicio": "08:00", "fim": "17:00"},
                "quinta": {"ativo": True, "inicio": "08:00", "fim": "17:00"},
                "sexta": {"ativo": True, "inicio": "08:00", "fim": "16:00"},
                "sabado": {"ativo": True, "inicio": "08:00", "fim": "13:00"},
                "domingo": {"ativo": False, "inicio": "09:00", "fim": "12:00"}
            }
        }
        
        if not row:
            return default_config
        
        # Parse do config JSON armazenado
        config_json = {}
        if row[1]:
            try:
                config_json = json.loads(row[1]) if isinstance(row[1], str) else row[1]
            except:
                config_json = {}
        
        # Monta resposta: padrão + config salva (a salva sobrescreve o padrão)
        result = default_config.copy()
        result.update({
            "nome_empresa": row[0] or default_config["nome_empresa"],
            **{k: v for k, v in config_json.items() if k in default_config}
        })
        
        return result
        
    except Exception as e:
        print(f"❌ Erro get_config_global: {e}")
        return {"error": str(e)}

@app.post("/api/config")
async def save_config_global(request: Request):
    """
    Salva configurações globais no banco de dados.
    Recebe JSON com: nome_empresa, subtitulo, nome_bot, fuso_horario, horarios_dia
    Usa clinica_id=1 como padrão para sistema single-tenant.
    """
    try:
        data = await request.json()
        conn = get_db()
        c = conn.cursor()
        
        # Verifica se já existe registro para id=1
        c.execute(f"SELECT id FROM clinicas WHERE id={_p()}", (1,))
        exists = c.fetchone()
        
        # Separa: nome_empresa vai na coluna 'nome', resto vai no JSON 'config'
        nome_empresa = data.get("nome_empresa", "Evandro Suek")
        
        # Campos que serão armazenados DENTRO do JSON config
        config_fields = {
            "subtitulo": data.get("subtitulo", "Sistemas Automatizados de Atendimento"),
            "nome_bot": data.get("nome_bot", "Bella"),
            "fuso_horario": data.get("fuso_horario", "America/Sao_Paulo"),
            "horarios_dia": data.get("horarios_dia", {})
        }
        
        if exists:
            # Atualiza registro existente
            c.execute(f"UPDATE clinicas SET nome={_p()}, config={_p()} WHERE id={_p()}",
                     (nome_empresa, json.dumps(config_fields, ensure_ascii=False), 1))
        else:
            # Cria novo registro com id=1
            c.execute(f"INSERT INTO clinicas (id, nome, config) VALUES ({_p()}, {_p()}, {_p()})",
                     (1, nome_empresa, json.dumps(config_fields, ensure_ascii=False)))
        
        conn.commit()
        conn.close()
        
        return {"success": True, "message": "Configurações salvas com sucesso!"}
        
    except Exception as e:
        print(f"❌ Erro save_config_global: {e}")
        return {"error": str(e)}, 500

# ==========================================
# 🚀 INICIALIZAÇÃO DO SERVIDOR
# ==========================================
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="warning")