import streamlit as st
from html import escape

# ==========================================================
# SIMULADOR DE FILA - CAIXA DE BANCO
# Estrutura de Dados: FILA (FIFO)
# Aplicação Streamlit
# ==========================================================

st.set_page_config(
    page_title="Simulador de Fila - Banco",
    page_icon="🏦",
    layout="wide"
)

# ----------------------------------------------------------
# ESTILO VISUAL
# ----------------------------------------------------------
st.markdown("""
<style>
    .stApp {
        background: #0b1220;
        color: #f1f5f9;
    }
    [data-testid="stSidebar"] {
        background: #111827;
    }
    .top-label {
        color: #22d3ee;
        font-size: .82rem;
        font-weight: 800;
        letter-spacing: .08em;
        text-transform: uppercase;
    }
    .main-title {
        color: #f1f5f9;
        font-size: 2.15rem;
        font-weight: 800;
        margin: .15rem 0 .25rem 0;
    }
    .subtitle {
        color: #b6c5d6;
        font-size: 1rem;
        margin-bottom: 1.3rem;
    }
    .metric-card {
        background: #142338;
        border: 1px solid #263b54;
        border-radius: 14px;
        padding: 14px 17px;
        min-height: 85px;
    }
    .metric-label {
        color: #9fb2c8;
        font-size: .82rem;
    }
    .metric-value {
        color: #f8fafc;
        font-size: 1.65rem;
        font-weight: 800;
    }
    .queue-wrap {
        background: #0f1b2d;
        border: 1px solid #263b54;
        border-radius: 16px;
        padding: 22px 18px;
        margin: 12px 0 18px 0;
        overflow-x: auto;
    }
    .queue-row {
        display: flex;
        align-items: center;
        gap: 10px;
        min-width: max-content;
        padding: 8px 2px 14px 2px;
    }
    .person-card {
        min-width: 112px;
        padding: 15px 12px;
        text-align: center;
        border: 2px solid #34d399;
        border-radius: 13px;
        background: #193047;
        color: #f8fafc;
    }
    .person-card .position {
        color: #a7f3d0;
        font-size: .75rem;
        font-weight: 700;
        margin-bottom: 4px;
    }
    .person-card .person-name {
        font-size: 1rem;
        font-weight: 800;
        overflow-wrap: anywhere;
    }
    .queue-arrow {
        color: #22d3ee;
        font-size: 1.8rem;
        font-weight: 800;
    }
    .cashier-card {
        min-width: 135px;
        padding: 17px 14px;
        text-align: center;
        border: 2px solid #fbbf24;
        border-radius: 13px;
        background: #193047;
        color: #f8fafc;
        font-weight: 800;
        font-size: 1.05rem;
    }
    .empty-card {
        color: #94a3b8;
        border: 1px dashed #64748b;
        border-radius: 12px;
        padding: 18px 24px;
    }
    .explain-card {
        background: #142338;
        border: 1px solid #263b54;
        border-left: 7px solid #34d399;
        border-radius: 14px;
        padding: 17px 19px;
        min-height: 125px;
    }
    .explain-card.exit {
        border-left-color: #fb7185;
    }
    .explain-title {
        font-size: 1.12rem;
        font-weight: 800;
        margin-bottom: 9px;
    }
    .explain-text {
        color: #f1f5f9;
        font-size: 1rem;
    }
    div.stButton > button, div.stFormSubmitButton > button {
        border-radius: 10px;
        font-weight: 700;
        min-height: 2.7rem;
    }
    .small-note {
        color: #9fb2c8;
        font-size: .88rem;
    }
</style>
""", unsafe_allow_html=True)


# ----------------------------------------------------------
# CLASSE DA FILA
# ----------------------------------------------------------
class FilaBanco:
    def __init__(self):
        self.fila = []
        self.proxima_senha = 1
        self.em_atendimento = None

    def entrar_na_fila(self, nome):
        pessoa = {
            "senha": self.proxima_senha,
            "nome": nome
        }
        self.fila.append(pessoa)
        self.proxima_senha += 1
        return pessoa

    def chamar_proximo(self):
        if len(self.fila) == 0:
            return None

        # Remove o primeiro elemento: regra FIFO.
        self.em_atendimento = self.fila.pop(0)
        return self.em_atendimento


# ----------------------------------------------------------
# ESTADO PERSISTENTE DA APLICAÇÃO
# ----------------------------------------------------------
def inicializar_estado():
    if "fila_banco" not in st.session_state:
        banco = FilaBanco()
        for nome in ["Ana", "Bruno", "Carla", "Daniel"]:
            banco.entrar_na_fila(nome)
        st.session_state.fila_banco = banco

    if "aviso" not in st.session_state:
        st.session_state.aviso = None


inicializar_estado()
banco = st.session_state.fila_banco


# ----------------------------------------------------------
# CABEÇALHO
# ----------------------------------------------------------
st.markdown('<div class="top-label">FILAS • ESTRUTURA DE DADOS</div>',
            unsafe_allow_html=True)
st.markdown('<div class="main-title">Fila na prática: atendimento bancário</div>',
            unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">A ordem de chegada organiza o atendimento. '
    'A fila segue a regra FIFO: primeiro a entrar, primeiro a sair.</div>',
    unsafe_allow_html=True
)


# ----------------------------------------------------------
# INDICADORES
# ----------------------------------------------------------
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">Pessoas aguardando</div>'
        f'<div class="metric-value">{len(banco.fila)}</div></div>',
        unsafe_allow_html=True
    )
with c2:
    proxima = f"{banco.proxima_senha:03d}"
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">Próxima senha</div>'
        f'<div class="metric-value">{proxima}</div></div>',
        unsafe_allow_html=True
    )
with c3:
    nome_atual = escape(banco.em_atendimento["nome"]) if banco.em_atendimento else "Ninguém"
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">Último chamado ao caixa</div>'
        f'<div class="metric-value" style="font-size:1.35rem">{nome_atual}</div></div>',
        unsafe_allow_html=True
    )


# ----------------------------------------------------------
# VISUALIZAÇÃO DA FILA
# ----------------------------------------------------------
st.subheader("Visualização da fila")

itens = []
if banco.fila:
    for posicao, pessoa in enumerate(banco.fila, start=1):
        itens.append(
            '<div class="person-card">'
            f'<div class="position">{posicao}º LUGAR • SENHA {pessoa["senha"]:03d}</div>'
            f'<div class="person-name">{escape(pessoa["nome"])}</div>'
            '</div>'
        )
else:
    itens.append('<div class="empty-card">Não há pessoas aguardando na fila.</div>')

fila_html = (
    '<div class="queue-wrap"><div class="queue-row">'
    + '<span style="color:#34d399;font-weight:800;margin-right:4px">INÍCIO</span>'
    + '<span class="queue-arrow">→</span>'.join(itens)
    + '<span class="queue-arrow">→</span>'
    + '<div class="cashier-card">CAIXA</div>'
    + '</div></div>'
)
st.markdown(fila_html, unsafe_allow_html=True)

if banco.em_atendimento:
    st.info(
        f"Último cliente chamado: senha {banco.em_atendimento['senha']:03d} — "
        f"{banco.em_atendimento['nome']}"
    )
else:
    st.caption("Ainda não houve chamada para o caixa.")


# ----------------------------------------------------------
# OPERAÇÕES: ENTRADA E SAÍDA
# ----------------------------------------------------------
st.subheader("Operações da fila")
col_entrada, col_saida = st.columns(2)

with col_entrada:
    st.markdown(
        '<div class="explain-card">'
        '<div class="explain-title" style="color:#34d399">ENTRADA • ENQUEUE</div>'
        '<div class="explain-text">Uma nova pessoa entra no final da fila.</div>'
        '</div>',
        unsafe_allow_html=True
    )
    with st.form("form_entrada", clear_on_submit=True):
        nome = st.text_input("Nome da pessoa", placeholder="Ex.: Eduardo")
        adicionar = st.form_submit_button("Adicionar ao final da fila",
                                          use_container_width=True)
    if adicionar:
        nome = nome.strip()
        if not nome:
            st.session_state.aviso = ("erro", "Digite o nome da pessoa.")
        else:
            pessoa = banco.entrar_na_fila(nome)
            st.session_state.aviso = (
                "sucesso",
                f"{pessoa['nome']} entrou no final da fila. Senha {pessoa['senha']:03d}."
            )
        st.rerun()

with col_saida:
    st.markdown(
        '<div class="explain-card exit">'
        '<div class="explain-title" style="color:#fb7185">SAÍDA • DEQUEUE</div>'
        '<div class="explain-text">O caixa chama e retira a primeira pessoa da fila.</div>'
        '</div>',
        unsafe_allow_html=True
    )
    st.write("")
    st.write("")
    if st.button("Chamar próximo cliente", use_container_width=True):
        pessoa = banco.chamar_proximo()
        if pessoa is None:
            st.session_state.aviso = ("erro", "A fila está vazia. Não há clientes para chamar.")
        else:
            st.session_state.aviso = (
                "sucesso",
                f"Senha {pessoa['senha']:03d} — {pessoa['nome']} foi chamada para o caixa."
            )
        st.rerun()


# ----------------------------------------------------------
# MENSAGENS DA OPERAÇÃO
# ----------------------------------------------------------
if st.session_state.aviso:
    tipo, mensagem = st.session_state.aviso
    if tipo == "sucesso":
        st.success(mensagem)
    elif tipo == "erro":
        st.error(mensagem)
    else:
        st.info(mensagem)


# ----------------------------------------------------------
# DETALHES DA FILA E REGRA FIFO
# ----------------------------------------------------------
with st.expander("Ver fila completa e senhas"):
    if banco.fila:
        st.dataframe(
            [
                {
                    "Posição": posicao,
                    "Senha": f"{pessoa['senha']:03d}",
                    "Cliente": pessoa["nome"]
                }
                for posicao, pessoa in enumerate(banco.fila, start=1)
            ],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.write("Fila vazia.")

with st.expander("Entenda a regra FIFO"):
    st.markdown("""
    **FIFO — First In, First Out**

    Em português: **Primeiro a Entrar, Primeiro a Sair.**

    - **Entrada (enqueue):** adiciona uma pessoa no final da fila.
    - **Saída (dequeue):** retira a pessoa que está no início da fila.
    - **Exemplo:** se Ana chegou antes de Bruno, Ana será chamada primeiro.
    """)

# ----------------------------------------------------------
# CONTROLES ADICIONAIS
# ----------------------------------------------------------
st.divider()
col_reset, col_clear, col_info = st.columns([1, 1, 2])

with col_reset:
    if st.button("Restaurar fila inicial", use_container_width=True):
        novo_banco = FilaBanco()
        for nome_inicial in ["Ana", "Bruno", "Carla", "Daniel"]:
            novo_banco.entrar_na_fila(nome_inicial)
        st.session_state.fila_banco = novo_banco
        st.session_state.aviso = ("info", "Fila inicial restaurada.")
        st.rerun()

with col_clear:
    if st.button("Esvaziar fila", use_container_width=True):
        banco.fila.clear()
        st.session_state.aviso = ("info", "Todos os clientes aguardando foram removidos.")
        st.rerun()

with col_info:
    st.markdown(
        '<div class="small-note">Atenção: a pessoa chamada é removida do início da fila. '
        'Novos clientes sempre entram no final. Isso demonstra a regra FIFO.</div>',
        unsafe_allow_html=True
    )

st.caption("Simulador didático de Estrutura de Dados • Fila FIFO")
