import streamlit as st
import datetime
import time

# --- Dados de Eventos ---
FERIADOS_2025 = {
    datetime.date(2025, 1, 1): "Confraternização Universal",
    datetime.date(2025, 1, 20): "Dia de São Sebastião (RJ)",
    datetime.date(2025, 3, 3): "Ponto Facultativo de Carnaval",
    datetime.date(2025, 3, 4): "Carnaval",
    datetime.date(2025, 3, 5): "Ponto Facultativo de Carnaval",
    datetime.date(2025, 4, 18): "Paixão de Cristo",
    datetime.date(2025, 4, 21): "Tiradentes",
    datetime.date(2025, 4, 23): "Dia de São Jorge (RJ)",
    datetime.date(2025, 5, 1): "Dia do Trabalho",
    datetime.date(2025, 5, 2): "Compensação (Dia Ponte)",
    datetime.date(2025, 6, 19): "Corpus Christi",
    datetime.date(2025, 6, 20): "Compensação (Dia Ponte)",
    datetime.date(2025, 9, 7): "Independência do Brasil",
    datetime.date(2025, 10, 12): "Nossa Senhora Aparecida",
    datetime.date(2025, 11, 2): "Finados",
    datetime.date(2025, 11, 15): "Proclamação da República",
    datetime.date(2025, 11, 20): "Dia da Consciência Negra",
    datetime.date(2025, 11, 21): "Compensação (Dia Ponte)",
    datetime.date(2025, 12, 24): "Ponto Facultativo de Natal",
    datetime.date(2025, 12, 25): "Natal",
    datetime.date(2025, 12, 26): "Compensação (Dia Ponte)",
    datetime.date(2025, 12, 31): "Ponto Facultativo de Ano Novo",
}

DATAS_PAGAMENTO_VA_VR = {
    datetime.date(2025, 1, 30): "Crédito do VA/VR (Ref. Fevereiro)",
    datetime.date(2025, 2, 28): "Crédito do VA/VR (Ref. Março)",
    datetime.date(2025, 3, 28): "Crédito do VA/VR (Ref. Abril)",
    datetime.date(2025, 4, 30): "Crédito do VA/VR (Ref. Maio)",
    datetime.date(2025, 5, 30): "Crédito do VA/VR (Ref. Junho)",
    datetime.date(2025, 6, 30): "Crédito do VA/VR (Ref. Julho)",
    datetime.date(2025, 7, 30): "Crédito do VA/VR (Ref. Agosto)",
    datetime.date(2025, 8, 29): "Crédito do VA/VR (Ref. Setembro)",
    datetime.date(2025, 9, 30): "Crédito do VA/VR (Ref. Outubro)",
    datetime.date(2025, 10, 30): "Crédito do VA/VR (Ref. Novembro)",
    datetime.date(2025, 11, 28): "Crédito do VA/VR (Ref. Dezembro)",
    datetime.date(2025, 12, 30): "Crédito do VA/VR (Ref. Janeiro/26)",
}

DATAS_LIMITE_BENEFICIOS = {
    datetime.date(2025, 1, 10): "Data limite para benefícios (Janeiro)",
    datetime.date(2025, 2, 10): "Data limite para benefícios (Fevereiro)",
    datetime.date(2025, 3, 11): "Data limite para benefícios (Março)",
    datetime.date(2025, 4, 10): "Data limite para benefícios (Abril)",
    datetime.date(2025, 5, 12): "Data limite para benefícios (Maio)",
    datetime.date(2025, 6, 10): "Data limite para benefícios (Junho)",
    datetime.date(2025, 7, 10): "Data limite para benefícios (Julho)",
    datetime.date(2025, 8, 11): "Data limite para benefícios (Agosto)",
    datetime.date(2025, 9, 10): "Data limite para benefícios (Setembro)",
    datetime.date(2025, 10, 10): "Data limite para benefícios (Outubro)",
    datetime.date(2025, 11, 10): "Data limite para benefícios (Novembro)",
    datetime.date(2025, 12, 10): "Data limite para benefícios (Dezembro)",
}

DATAS_PAGAMENTO_SALARIO = {
    datetime.date(2025, 1, 30): "Pagamento de Salário (Janeiro)",
    datetime.date(2025, 2, 28): "Pagamento de Salário (Fevereiro)",
    datetime.date(2025, 3, 28): "Pagamento de Salário (Março)",
    datetime.date(2025, 4, 30): "Pagamento de Salário (Abril)",
    datetime.date(2025, 5, 30): "Pagamento de Salário (Maio)",
    datetime.date(2025, 6, 30): "Pagamento de Salário (Junho)",
    datetime.date(2025, 7, 30): "Pagamento de Salário (Julho)",
    datetime.date(2025, 8, 29): "Pagamento de Salário (Agosto)",
    datetime.date(2025, 9, 30): "Pagamento de Salário (Setembro)",
    datetime.date(2025, 10, 30): "Pagamento de Salário (Outubro)",
    datetime.date(2025, 11, 28): "Pagamento de Salário (Novembro)",
    datetime.date(2025, 12, 30): "Pagamento de Salário (Dezembro)",
}

DATAS_PAGAMENTO_13 = {
    datetime.date(2025, 1, 10): "Adiantamento 1ª parcela do 13º Salário",
    datetime.date(2025, 11, 28): "13º Salário (para quem não pediu adiantamento)",
    datetime.date(2025, 12, 19): "2ª parcela do 13º Salário",
}

DATAS_ADIANTAMENTO_SALARIO = {
    datetime.date(2025, 1, 15): "Adiantamento Salarial (Janeiro)",
    datetime.date(2025, 2, 14): "Adiantamento Salarial (Fevereiro)",
    datetime.date(2025, 3, 14): "Adiantamento Salarial (Março)",
    datetime.date(2025, 4, 15): "Adiantamento Salarial (Abril)",
    datetime.date(2025, 5, 15): "Adiantamento Salarial (Maio)",
    datetime.date(2025, 6, 13): "Adiantamento Salarial (Junho)",
    datetime.date(2025, 7, 15): "Adiantamento Salarial (Julho)",
    datetime.date(2025, 8, 15): "Adiantamento Salarial (Agosto)",
    datetime.date(2025, 9, 15): "Adiantamento Salarial (Setembro)",
    datetime.date(2025, 10, 15): "Adiantamento Salarial (Outubro)",
    datetime.date(2025, 11, 14): "Adiantamento Salarial (Novembro)",
    datetime.date(2025, 12, 12): "Adiantamento Salarial (Dezembro)",
}

# --- Funções de Lógica ---

def verificar_eventos_proximos():
    """Verifica se há eventos nos próximos 3 dias e retorna mensagens."""
    hoje = datetime.date.today()
    mensagens = []
    eventos_agrupados = {}

    # Agrupa todos os eventos por data para evitar sobrescrita
    todos_os_dicionarios = [FERIADOS_2025, DATAS_PAGAMENTO_VA_VR, DATAS_LIMITE_BENEFICIOS, DATAS_PAGAMENTO_SALARIO, DATAS_PAGAMENTO_13, DATAS_ADIANTAMENTO_SALARIO]
    for d in todos_os_dicionarios:
        for data, nome in d.items():
            if data not in eventos_agrupados:
                eventos_agrupados[data] = []
            eventos_agrupados[data].append(nome)

    for data_evento, lista_nomes in sorted(eventos_agrupados.items()):
        delta = data_evento - hoje
        if 0 <= delta.days <= 3:
            # Determina o emoji com base na prioridade do evento
            if any("Crédito" in s or "Pagamento" in s or "13º" in s or "Adiantamento" in s for s in lista_nomes):
                emoji = "💰"
            elif any("Data limite" in s for s in lista_nomes):
                emoji = "❗️"
            else:
                emoji = "🗓️"

            # Cria um nome de evento combinado e mais limpo
            nomes_limpos = [s.split('(')[0].strip() for s in lista_nomes]
            nome_evento_final = " e ".join(nomes_limpos)

            if delta.days == 0:
                mensagem = f"{emoji} Hoje é {nome_evento_final}!"
            elif delta.days == 1:
                mensagem = f"{emoji} Amanhã é {nome_evento_final}!"
            else:
                mensagem = f"{emoji} Faltam {delta.days} dias para {nome_evento_final}!"
            mensagens.append(mensagem)
    return mensagens

def formatar_hora_input(input_str):
    """Formata a entrada de hora (HHMM ou HH:MM) para o formato HH:MM."""
    input_str = input_str.strip()
    if ':' in input_str:
        return input_str
    
    if len(input_str) == 3:
        input_str = '0' + input_str
    if len(input_str) != 4 or not input_str.isdigit():
        raise ValueError("Formato de hora inválido.")
    
    return f"{input_str[:2]}:{input_str[2:]}"

def calcular_tempo_nucleo(entrada, saida, saida_almoco, retorno_almoco):
    """Calcula o tempo trabalhado dentro do horário núcleo (9h às 18h)."""
    nucleo_inicio = entrada.replace(hour=9, minute=0, second=0, microsecond=0)
    nucleo_fim = entrada.replace(hour=18, minute=0, second=0, microsecond=0)
    
    inicio_trabalho_nucleo = max(entrada, nucleo_inicio)
    fim_trabalho_nucleo = min(saida, nucleo_fim)
    
    if inicio_trabalho_nucleo >= fim_trabalho_nucleo:
        return 0
        
    tempo_bruto_nucleo_segundos = (fim_trabalho_nucleo - inicio_trabalho_nucleo).total_seconds()
    tempo_bruto_nucleo_minutos = tempo_bruto_nucleo_segundos / 60
    
    tempo_almoco_nucleo_minutos = 0
    if saida_almoco and retorno_almoco:
        inicio_almoco_nucleo = max(saida_almoco, nucleo_inicio)
        fim_almoco_nucleo = min(retorno_almoco, nucleo_fim)
        if inicio_almoco_nucleo < fim_almoco_nucleo:
            tempo_almoco_nucleo_segundos = (fim_almoco_nucleo - inicio_almoco_nucleo).total_seconds()
            tempo_almoco_nucleo_minutos = tempo_almoco_nucleo_segundos / 60
            
    tempo_liquido_nucleo = tempo_bruto_nucleo_minutos - tempo_almoco_nucleo_minutos
    return max(0, tempo_liquido_nucleo)

def formatar_duracao(minutos):
    """Formata uma duração em minutos para o formato Xh Ymin."""
    if minutos < 0:
        minutos = 0
    horas = int(minutos // 60)
    mins = int(minutos % 60)
    return f"{horas}h {mins}min"

# --- Interface do Web App com Streamlit ---
st.set_page_config(page_title="Calculadora de Jornada", layout="centered")

# Injeção de CSS para customização
st.markdown("""
<style>
    /* Diminui o padding superior da página */
    div.block-container {
        padding-top: 4rem;
    }

    /* Limita a largura do container principal */
    .main .block-container {
        max-width: 800px;
    }
    /* Estiliza o título principal customizado */
    .main-title {
        font-size: 2.2rem !important;
        font-weight: bold;
        text-align: center;
    }
    
    /* Estiliza o subtítulo customizado */
    .sub-title {
        color: gray;
        text-align: center;
        font-size: 1.5rem !important;
    }

    /* Centraliza e anima o botão para evitar o 'salto' */
    div[data-testid="stButton"] {
        display: flex;
        justify-content: center;
        opacity: 0;
        animation: fadeInSmooth 0.5s ease-out 0.1s forwards;
    }

    /* Estiliza o botão de cálculo */
    div[data-testid="stButton"] > button {
        background-color: rgb(221, 79, 5);
        color: #FFFFFF;
        width: 100%;
        border-radius: 4rem;
    }
    /* Arredonda as caixas de input e centraliza os labels */
    div[data-testid="stTextInput"] input {
        border-radius: 1.5rem !important;
        text-align: center;
        font-weight: 600;
    }
    .main div[data-testid="stTextInput"] > label {
        text-align: center !important; /* Força a centralização para sobrescrever temas */
        width: 100%;
        display: block;
    }

    /* Animação de fade-in para os resultados */
    .results-container {
        animation: fadeIn 0.5s ease-out forwards;
    }
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(15px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Animação de fade-in para o botão */
    @keyframes fadeInSmooth {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Estilos para notificação de eventos */
    .event-notification {
        background-color: rgba(57, 94, 94, 0.2);
        border: 1px solid rgb(57, 94, 94);
        border-radius: 1.5rem;
        padding: 0.75rem;
        text-align: center;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
        color: #005051; /* Cor para o tema claro (padrão) */
    }

    /* Streamlit adiciona a classe 'theme-dark' em um elemento pai quando o tema escuro está ativo */
    .theme-dark .event-notification {
        color: #dd4f05; /* Cor para o tema escuro */
    }

    /* Estilos para alertas customizados */
    .custom-warning, .custom-error {
        border-radius: 1.5rem;
        padding: 1rem;
        margin-top: 1rem;
        text-align: center;
    }
    .custom-warning {
        background-color: rgba(255, 170, 0, 0.15);
        border: 1px solid #ffaa00;
        color: #31333f;
    }
    .custom-error {
        background-color: rgba(255, 108, 108, 0.15);
        border: 1px solid rgb(255, 108, 108);
        color: rgb(255, 75, 75);
    }
    .custom-error p {
        margin: 0.5rem 0 0 0;
    }

    /* Oculta o ícone de âncora/link nos cabeçalhos de forma mais específica */
    div[data-testid="stHeading"] a {
        display: none !important;
    }

    /* Remove estilos padrão que podem causar conflito */
    div[data-testid="stMetric"] {
        background-color: transparent !important;
        padding: 0 !important;
    }
    div[data-testid="stMetric"] [data-testid="stMetricLabel"] p,
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: inherit !important;
    }

    /* Estilo para centralizar texto dentro das seções de resultado */
    .section-container {
        text-align: center;
    }

    /* Estilos para a métrica customizada (agora usada para todos os quadros) */
    .metric-custom {
        background-color: #F0F2F6; /* Cor de fundo padrão */
        border-radius: 4rem;
        padding: 1rem;
        text-align: center;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        color: #31333f; /* Cor do texto padrão */
    }
    .metric-almoco {
        background-color: rgb(255, 201, 173); /* Fundo para o almoço */
    }
    /* Cores para caixas de saldo e previsões */
    .metric-saldo-pos { background-color: rgb(84, 198, 121); }
    .metric-saldo-neg { background-color: rgb(255, 108, 108); }
    .metric-minimo { background-color: rgb(57, 94, 94); } /* Ciano Escuro */
    .metric-padrao { background-color: rgb(0, 80, 81); } 
    .metric-maximo { background-color: rgb(221, 79, 5); } 
    
    .metric-custom .label {
        font-size: 0.875rem; /* 14px */
        margin-bottom: 0.25rem;
        color: #5a5a5a;
    }
    .metric-custom .value {
        font-size: 1.5rem; /* 24px */
        font-weight: 900;
        color: #31333f;
    }
    .metric-custom .details {
        font-size: 0.75rem; /* 12px */
        margin-top: 0.25rem;
        color: #5a5a5a;
    }

    /* Cor de texto branca para caixas coloridas */
    .metric-saldo-pos .value, .metric-saldo-neg .value,
    .metric-minimo .value, .metric-padrao .value, .metric-maximo .value {
        color: #FFFFFF;
    }
    .metric-saldo-pos .label, .metric-saldo-neg .label,
    .metric-minimo .label, .metric-padrao .label, .metric-maximo .label,
    .metric-minimo .details, .metric-padrao .details, .metric-maximo .details {
        color: rgba(255, 255, 255, 0.85);
    }

    /* Container para as métricas de previsão */
    .predictions-grid-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.75rem;
    }
    /* Container para as métricas de resumo */
    .summary-grid-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 0.75rem; /* Espaçamento entre os quadros */
    }

    /* Responsividade para grids */
    @media (max-width: 640px) {
        .predictions-grid-container {
            grid-template-columns: repeat(2, 1fr); /* Duas colunas */
        }
        /* Reordena as previsões no mobile */
        .predictions-grid-container .metric-minimo { order: 2; }
        .predictions-grid-container .metric-padrao {
            order: 1; /* Padrão vem primeiro */
            grid-column: 1 / -1; /* Ocupa a largura toda */
        }
        .predictions-grid-container .metric-maximo { order: 3; }
        
        .summary-grid-container {
            grid-template-columns: repeat(2, 1fr); /* Passa para 2 colunas */
        }
    }

    /* Estilos gerais para classes instáveis do Streamlit */
    .st-bv {    font-weight: 800;}
    .st-ay {    font-size: 1.3rem;}
    .st-aw {    border-bottom-right-radius: 1.5rem;}
    .st-av {    border-top-right-radius: 1.5rem;}
    .st-au {    border-bottom-left-radius: 1.5rem;}
    .st-at {    border-top-left-radius: 1.5rem;}
</style>
""", unsafe_allow_html=True)


st.markdown('<p class="main-title">Calculadora de Jornada de Trabalho</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Informe seus horários para calcular a jornada diária</p>', unsafe_allow_html=True)

# --- Seção de Avisos de Eventos ---
mensagens_eventos = verificar_eventos_proximos()
if mensagens_eventos:
    for msg in mensagens_eventos:
        st.markdown(f'<div class="event-notification">{msg}</div>', unsafe_allow_html=True)

# Layout dos campos de entrada com colunas para limitar a largura
col_buffer_1, col_main, col_buffer_2 = st.columns([1, 6, 1])
with col_main:
    entrada_str = st.text_input("Entrada", key="entrada", help="formatos aceitos:\nHMM, HHMM ou HH:MM")
    col1, col2 = st.columns(2)
    with col1:
        saida_almoco_str = st.text_input("Saída para o Almoço", key="saida_almoco")
    with col2:
        retorno_almoco_str = st.text_input("Volta do Almoço", key="retorno_almoco")
    saida_real_str = st.text_input("Saída", key="saida_real")

    # Botão centralizado via CSS
    calculate_clicked = st.button("Calcular")

# Placeholder para os resultados
results_placeholder = st.empty()

if 'show_results' not in st.session_state:
    st.session_state.show_results = False

if calculate_clicked:
    st.session_state.show_results = True

if st.session_state.show_results:
    if not entrada_str:
        st.warning("Por favor, preencha pelo menos o horário de entrada.")
        st.session_state.show_results = False # Reseta para não mostrar na próxima recarga
    else:
        try:
            hora_entrada = datetime.datetime.strptime(formatar_hora_input(entrada_str), "%H:%M")

            # --- Lógica de cálculo das previsões ---
            limite_saida = hora_entrada.replace(hour=20, minute=0, second=0, microsecond=0)
            duracao_almoço_previsao = 0
            if saida_almoco_str and retorno_almoco_str:
                saida_almoco_prev = datetime.datetime.strptime(formatar_hora_input(saida_almoco_str), "%H:%M")
                retorno_almoco_prev = datetime.datetime.strptime(formatar_hora_input(retorno_almoco_str), "%H:%M")
                duracao_almoço_previsao = (retorno_almoco_prev - saida_almoco_prev).total_seconds() / 60
            
            minutos_intervalo_5h = max(15, duracao_almoço_previsao)
            hora_nucleo_inicio = hora_entrada.replace(hour=9, minute=0)
            hora_base_5h = max(hora_entrada, hora_nucleo_inicio)
            hora_saida_5h_calculada = hora_base_5h + datetime.timedelta(hours=5, minutes=minutos_intervalo_5h)
            hora_saida_5h = min(hora_saida_5h_calculada, limite_saida)
            
            minutos_intervalo_demais = max(30, duracao_almoço_previsao)
            hora_saida_8h_calculada = hora_entrada + datetime.timedelta(hours=8, minutes=minutos_intervalo_demais)
            hora_saida_8h = min(hora_saida_8h_calculada, limite_saida)

            hora_saida_10h_calculada = hora_entrada + datetime.timedelta(hours=10, minutes=minutos_intervalo_demais)
            hora_saida_10h = min(hora_saida_10h_calculada, limite_saida)

            duracao_5h_min = (hora_saida_5h - hora_entrada).total_seconds() / 60 - minutos_intervalo_5h
            duracao_8h_min = (hora_saida_8h - hora_entrada).total_seconds() / 60 - minutos_intervalo_demais
            duracao_10h_min = (hora_saida_10h - hora_entrada).total_seconds() / 60 - minutos_intervalo_demais
            
            texto_desc_5h = f"({formatar_duracao(duracao_5h_min)})" if hora_saida_5h_calculada > limite_saida else "(5h no núcleo)"
            texto_desc_8h = f"({formatar_duracao(duracao_8h_min)})" if hora_saida_8h_calculada > limite_saida else "(8h)"
            texto_desc_10h = f"({formatar_duracao(duracao_10h_min)})" if hora_saida_10h_calculada > limite_saida else "(10h)"

            # --- Construção do HTML de Previsões ---
            predictions_html = f"""
            <div class='section-container'>
                <h3>Previsões de Saída</h3>
                <div class="predictions-grid-container">
                    <div class="metric-custom metric-minimo">
                        <div class="label">Mínimo {texto_desc_5h}</div>
                        <div class="value">{hora_saida_5h.strftime('%H:%M')}</div>
                        <div class="details">{minutos_intervalo_5h:.0f}min de intervalo</div>
                    </div>
                    <div class="metric-custom metric-padrao">
                        <div class="label">Jornada Padrão {texto_desc_8h}</div>
                        <div class="value">{hora_saida_8h.strftime('%H:%M')}</div>
                        <div class="details">{minutos_intervalo_demais:.0f}min de almoço</div>
                    </div>
                    <div class="metric-custom metric-maximo">
                        <div class="label">Máximo {texto_desc_10h}</div>
                        <div class="value">{hora_saida_10h.strftime('%H:%M')}</div>
                        <div class="details">{minutos_intervalo_demais:.0f}min de almoço</div>
                    </div>
                </div>
            </div>
            """
            
            # --- Lógica para o Resumo do Dia ---
            warnings_html = ""
            if saida_real_str:
                hora_saida_real = datetime.datetime.strptime(formatar_hora_input(saida_real_str), "%H:%M")
                if hora_saida_real < hora_entrada:
                    raise ValueError("A Saída deve ser depois da Entrada.")

                saida_almoco, retorno_almoco, duracao_almoco_minutos_real = None, None, 0
                if saida_almoco_str and retorno_almoco_str:
                    saida_almoco = datetime.datetime.strptime(formatar_hora_input(saida_almoco_str), "%H:%M")
                    retorno_almoco = datetime.datetime.strptime(formatar_hora_input(retorno_almoco_str), "%H:%M")
                    if retorno_almoco < saida_almoco:
                        raise ValueError("A volta do almoço deve ser depois da saída para o almoço.")
                    duracao_almoco_minutos_real = (retorno_almoco - saida_almoco).total_seconds() / 60

                trabalho_bruto_minutos = (hora_saida_real - hora_entrada).total_seconds() / 60
                tempo_trabalhado_efetivo = trabalho_bruto_minutos - duracao_almoco_minutos_real

                if tempo_trabalhado_efetivo > 360: min_intervalo_real, termo_intervalo_real = 30, "almoço"
                elif tempo_trabalhado_efetivo > 240: min_intervalo_real, termo_intervalo_real = 15, "intervalo"
                else: min_intervalo_real, termo_intervalo_real = 0, "intervalo"

                duracao_almoço_para_calculo = max(min_intervalo_real, duracao_almoco_minutos_real)
                trabalho_liquido_minutos = trabalho_bruto_minutos - duracao_almoço_para_calculo
                saldo_banco_horas_minutos = trabalho_liquido_minutos - 480
                tempo_nucleo_minutos = calcular_tempo_nucleo(hora_entrada, hora_saida_real, saida_almoco, retorno_almoco)
                
                # --- Construção dos Avisos ---
                if tempo_nucleo_minutos < 300:
                    warnings_html += '<div class="custom-warning">Atenção: Não cumpriu as 5h obrigatórias no período núcleo.</div>'

                lista_de_avisos = []
                if min_intervalo_real > 0 and duracao_almoco_minutos_real < min_intervalo_real:
                    lista_de_avisos.append(f"{termo_intervalo_real.capitalize()} foi inferior a {min_intervalo_real} minutos")
                if trabalho_liquido_minutos > 600:
                    lista_de_avisos.append("Jornada de trabalho excedeu 10 horas")
                if hora_saida_real.time() > datetime.time(20, 0):
                    lista_de_avisos.append("Saída registrada após as 20h")

                if lista_de_avisos:
                    motivo_header = "Motivo" if len(lista_de_avisos) == 1 else "Motivos"
                    motivos_texto = "<br>".join(lista_de_avisos)
                    warnings_html += f"""
                    <div class="custom-error">
                        <b>‼️ PERMANÊNCIA NÃO AUTORIZADA ‼️</b>
                        <p><b>{motivo_header}:</b></p>
                        <p>{motivos_texto}</p>
                    </div>
                    """
            
            # --- Seção de Renderização ---
            with results_placeholder.container():
                st.markdown(f'<div class="results-container">{predictions_html}</div>', unsafe_allow_html=True)

                if saida_real_str:
                    st.markdown("<hr>", unsafe_allow_html=True)
                    st.markdown("<div class='section-container'><h3>Resumo do Dia</h3></div>", unsafe_allow_html=True)
                    
                    # Layout das métricas com grid responsivo
                    saldo_css_class = "metric-saldo-pos" if saldo_banco_horas_minutos >= 0 else "metric-saldo-neg"
                    sinal = "+" if saldo_banco_horas_minutos >= 0 else "-"
                    
                    summary_grid_html = f"""
                    <div class="summary-grid-container">
                        <div class="metric-custom">
                            <div class="label">Total Trabalhado</div>
                            <div class="value">{formatar_duracao(trabalho_liquido_minutos)}</div>
                        </div>
                        <div class="metric-custom">
                            <div class="label">Tempo no Núcleo</div>
                            <div class="value">{formatar_duracao(tempo_nucleo_minutos)}</div>
                        </div>
                        <div class="metric-custom metric-almoco">
                            <div class="label">Tempo de {termo_intervalo_real}</div>
                            <div class="value">{duracao_almoco_minutos_real:.0f}min</div>
                        </div>
                        <div class="metric-custom {saldo_css_class}">
                            <div class="label">Saldo do Dia</div>
                            <div class="value">{sinal} {formatar_duracao(abs(saldo_banco_horas_minutos))}</div>
                        </div>
                    </div>
                    """
                    st.markdown(summary_grid_html, unsafe_allow_html=True)

                # Exibe os avisos (se houver)
                st.markdown(warnings_html, unsafe_allow_html=True)
            
            # Script para rolagem suave (opcional, mas bom para UX)
            scroll_script = """
                <script>
                    setTimeout(function() {
                        const resultsEl = window.parent.document.querySelector('.results-container');
                        if (resultsEl) {
                            resultsEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
                        }
                    }, 100);
                </script>
            """
            st.components.v1.html(scroll_script, height=0)

        except ValueError as e:
            st.error(f"Erro: {e}")
        except Exception as e:
            st.error(f"Ocorreu um erro inesperado: {e}")
        finally:
            st.session_state.show_results = False # Reseta para a próxima recarga


