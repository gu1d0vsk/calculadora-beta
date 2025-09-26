import streamlit as st
import datetime
import json
import pandas as pd
import time

# --- Funções de Lógica ---

def formatar_hora_input(input_str):
    """Formata a entrada de hora (HHMM ou HH:MM) para o formato HH:MM."""
    if not input_str:
        return ""
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

def formatar_duracao(minutos, sinal=False):
    """Formata uma duração em minutos para o formato Xh Ymin."""
    if minutos is None:
        return "0h 0min"
    
    prefixo = ""
    if sinal:
        prefixo = "+ " if minutos >= 0 else "- "
        minutos = abs(minutos)

    horas = int(minutos // 60)
    mins = int(minutos % 60)
    return f"{prefixo}{horas}h {mins}min"

# --- Funções de Estado e Histórico ---

def inicializar_estado():
    """Inicializa o session_state se ainda não existir."""
    if 'history' not in st.session_state:
        st.session_state.history = {}
    
    if 'selected_date' not in st.session_state:
        st.session_state.selected_date = datetime.date.today()

    # Inicializa as chaves para os campos de texto
    keys = ['entrada_str', 'saida_almoco_str', 'retorno_almoco_str', 'saida_real_str']
    for key in keys:
        if key not in st.session_state:
            st.session_state[key] = ""

def carregar_dia_selecionado():
    """Carrega os dados do dia selecionado do histórico para os campos de input."""
    date_key = st.session_state.selected_date.strftime('%Y-%m-%d')
    day_data = st.session_state.history.get(date_key, {})
    
    st.session_state.entrada_str = day_data.get('entrada', '')
    st.session_state.saida_almoco_str = day_data.get('saida_almoco', '')
    st.session_state.retorno_almoco_str = day_data.get('retorno_almoco', '')
    st.session_state.saida_real_str = day_data.get('saida_real', '')

def salvar_dia_no_historico(dados_calculados):
    """Salva os dados do dia atual no histórico."""
    date_key = st.session_state.selected_date.strftime('%Y-%m-%d')
    
    st.session_state.history[date_key] = {
        "entrada": st.session_state.entrada_str,
        "saida_almoco": st.session_state.saida_almoco_str,
        "retorno_almoco": st.session_state.retorno_almoco_str,
        "saida_real": st.session_state.saida_real_str,
        "trabalho_liquido": dados_calculados['trabalho_liquido_minutos'],
        "saldo_dia": dados_calculados['saldo_banco_horas_minutos']
    }
    st.toast(f"✅ Dia {st.session_state.selected_date.strftime('%d/%m')} salvo!")


def excluir_dia_do_historico(date_key):
    """Exclui um dia do histórico."""
    if date_key in st.session_state.history:
        del st.session_state.history[date_key]
        st.toast(f"🗑️ Dia {datetime.datetime.strptime(date_key, '%Y-%m-%d').strftime('%d/%m')} excluído.")


def calcular_banco_de_horas_total():
    """Calcula o saldo total do banco de horas."""
    if not st.session_state.history:
        return 0
    
    total_saldo = sum(data.get('saldo_dia', 0) for data in st.session_state.history.values() if data.get('saldo_dia') is not None)
    return total_saldo

# --- Interface do Web App com Streamlit ---
st.set_page_config(page_title="Calculadora de Jornada", layout="centered")

# Inicializa o estado da sessão
inicializar_estado()

# Injeção de CSS para customização
st.markdown("""
<style>
    .main .block-container { max-width: 800px; }
    .main-title { font-size: 2.2rem !important; font-weight: bold; text-align: center; }
    .sub-title { color: gray; text-align: center; font-size: 1.5rem !important; }
    div[data-testid="stButton"] > button { background-color: rgb(92, 228, 136); color: #FFFFFF; width: 100%; }
    div[data-testid="stTextInput"] input { border-radius: 1.5rem !important; text-align: center; }
    .main div[data-testid="stTextInput"] > label { text-align: center; width: 100%; display: block; }
    .results-container { animation: fadeIn 0.5s ease-out forwards; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }
    .custom-warning, .custom-error { border-radius: 1.5rem; padding: 1rem; margin-top: 1rem; text-align: center; }
    .custom-warning { background-color: rgba(255, 170, 0, 0.15); border: 1px solid #ffaa00; color: #31333f; }
    .custom-error { background-color: rgba(255, 108, 108, 0.15); border: 1px solid rgb(255, 108, 108); color: rgb(255, 75, 75); }
    div[data-testid="stHeading"] a { display: none !important; }
    .section-container { text-align: center; }
    
    .metric-custom { background-color: #F0F2F6; border-radius: 1.5rem; padding: 1rem; text-align: center; height: 100%; display: flex; flex-direction: column; justify-content: center; color: #31333f; }
    .metric-almoco { background-color: #E8E8E8; }
    .metric-saldo-pos { background-color: rgba(92, 228, 136, 0.6); }
    .metric-saldo-neg { background-color: rgba(255, 108, 108, 0.6); }
    .metric-custom .label { font-size: 0.875rem; margin-bottom: 0.25rem; color: #5a5a5a; }
    .metric-custom .value { font-size: 1.5rem; font-weight: 600; color: #31333f; }
    .metric-saldo-pos .value, .metric-saldo-neg .value { color: #FFFFFF; }
    .metric-saldo-pos .label, .metric-saldo-neg .label { color: rgba(255, 255, 255, 0.85); }

    .metrics-grid-container { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.75rem; margin-top: 1rem;}
    @media (max-width: 640px) { .metrics-grid-container { grid-template-columns: repeat(2, 1fr); } }
    @media (max-width: 400px) { .metrics-grid-container { grid-template-columns: 1fr; } }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">Calculadora de Jornada de Trabalho</p>', unsafe_allow_html=True)

st.markdown('<p class="sub-title">Selecione e preencha os dados do dia</p>', unsafe_allow_html=True)

# Layout dos campos de entrada
col_buffer_1, col_main, col_buffer_2 = st.columns([1, 6, 1])
with col_main:
    st.date_input(
        "Selecione o Dia",
        key='selected_date',
        on_change=carregar_dia_selecionado,
        max_value=datetime.date.today()
    )
    
    st.session_state.entrada_str = st.text_input("Entrada", value=st.session_state.entrada_str)
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.saida_almoco_str = st.text_input("Saída Almoço", value=st.session_state.saida_almoco_str)
    with col2:
        st.session_state.retorno_almoco_str = st.text_input("Volta Almoço", value=st.session_state.retorno_almoco_str)
    st.session_state.saida_real_str = st.text_input("Saída", value=st.session_state.saida_real_str)

    calculate_clicked = st.button("Calcular / Visualizar Dia")

# Placeholder para os resultados
results_placeholder = st.empty()

if calculate_clicked:
    if not st.session_state.entrada_str:
        results_placeholder.warning("Por favor, preencha pelo menos o horário de entrada.")
    else:
        try:
            hora_entrada = datetime.datetime.strptime(formatar_hora_input(st.session_state.entrada_str), "%H:%M")
            
            # --- Lógica de Previsões ---
            previsoes_html = "<div class='section-container'><h3>Previsões de Saída</h3>"
            limite_saida = hora_entrada.replace(hour=20, minute=0, second=0, microsecond=0)
            duracao_almoço_previsao = 0
            if st.session_state.saida_almoco_str and st.session_state.retorno_almoco_str:
                saida_almoco_prev = datetime.datetime.strptime(formatar_hora_input(st.session_state.saida_almoco_str), "%H:%M")
                retorno_almoco_prev = datetime.datetime.strptime(formatar_hora_input(st.session_state.retorno_almoco_str), "%H:%M")
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

            previsoes_html += f"""
            <p>
            <b>Mínimo {texto_desc_5h}:</b> {hora_saida_5h.strftime('%H:%M')} ({minutos_intervalo_5h:.0f}min de intervalo)<br>
            <b>Jornada Padrão {texto_desc_8h}:</b> {hora_saida_8h.strftime('%H:%M')} ({minutos_intervalo_demais:.0f}min de almoço)<br>
            <b>Máximo {texto_desc_10h}:</b> {hora_saida_10h.strftime('%H:%M')} ({minutos_intervalo_demais:.0f}min de almoço)
            </p></div>
            """
            
            # --- Lógica de Resumo do Dia ---
            dados_calculados_dia = {}
            warnings_html = ""
            if st.session_state.saida_real_str:
                hora_saida_real = datetime.datetime.strptime(formatar_hora_input(st.session_state.saida_real_str), "%H:%M")
                if hora_saida_real < hora_entrada: raise ValueError("A Saída deve ser depois da Entrada.")

                saida_almoco, retorno_almoco, duracao_almoco_minutos_real = None, None, 0
                if st.session_state.saida_almoco_str and st.session_state.retorno_almoco_str:
                    saida_almoco = datetime.datetime.strptime(formatar_hora_input(st.session_state.saida_almoco_str), "%H:%M")
                    retorno_almoco = datetime.datetime.strptime(formatar_hora_input(st.session_state.retorno_almoco_str), "%H:%M")
                    if retorno_almoco < saida_almoco: raise ValueError("A volta do almoço deve ser depois da saída.")
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
                
                dados_calculados_dia = {
                    "trabalho_liquido_minutos": trabalho_liquido_minutos,
                    "saldo_banco_horas_minutos": saldo_banco_horas_minutos,
                    "tempo_nucleo_minutos": tempo_nucleo_minutos,
                    "duracao_almoco_minutos_real": duracao_almoco_minutos_real,
                    "termo_intervalo_real": termo_intervalo_real
                }

                if tempo_nucleo_minutos < 300:
                    warnings_html += '<div class="custom-warning">Atenção: Não cumpriu as 5h obrigatórias no período núcleo.</div>'
                # ... (outros avisos)

            # --- Renderização dos Resultados ---
            with results_placeholder.container():
                st.markdown(previsoes_html, unsafe_allow_html=True)
                
                if dados_calculados_dia:
                    st.markdown("<hr>", unsafe_allow_html=True)
                    st.markdown("<div class='section-container'><h3>Resumo do Dia</h3></div>", unsafe_allow_html=True)
                    
                    saldo_css = "metric-saldo-pos" if dados_calculados_dia['saldo_banco_horas_minutos'] >= 0 else "metric-saldo-neg"
                    metrics_grid = f"""
                    <div class="metrics-grid-container">
                        <div class="metric-custom"><div class="label">Total Trabalhado</div><div class="value">{formatar_duracao(dados_calculados_dia['trabalho_liquido_minutos'])}</div></div>
                        <div class="metric-custom"><div class="label">Tempo no Núcleo</div><div class="value">{formatar_duracao(dados_calculados_dia['tempo_nucleo_minutos'])}</div></div>
                        <div class="metric-custom metric-almoco"><div class="label">Tempo de {dados_calculados_dia['termo_intervalo_real']}</div><div class="value">{dados_calculados_dia['duracao_almoco_minutos_real']:.0f}min</div></div>
                        <div class="metric-custom {saldo_css}"><div class="label">Saldo do Dia</div><div class="value">{formatar_duracao(dados_calculados_dia['saldo_banco_horas_minutos'], sinal=True)}</div></div>
                    </div>
                    """
                    st.markdown(metrics_grid, unsafe_allow_html=True)

                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        st.button(
                            "Salvar no Histórico",
                            on_click=salvar_dia_no_historico,
                            args=(dados_calculados_dia,),
                            use_container_width=True
                        )
                    
                    # --- Seção do Banco de Horas Total ---
                    st.markdown("---")
                    st.markdown("<div class='section-container'><h3>Banco de Horas Total</h3></div>", unsafe_allow_html=True)
                    saldo_total_minutos = calcular_banco_de_horas_total()
                    
                    # Colunas para centralizar a métrica
                    m_col1, m_col2, m_col3 = st.columns([1, 2, 1])
                    with m_col2:
                        st.metric(
                            label="Saldo Acumulado",
                            value=formatar_duracao(abs(saldo_total_minutos)),
                            delta=formatar_duracao(saldo_total_minutos, sinal=True),
                        )

                st.markdown(warnings_html, unsafe_allow_html=True)
        
        except ValueError as e:
            results_placeholder.error(f"Erro de formato: {e}")
        except Exception as e:
            results_placeholder.error(f"Ocorreu um erro inesperado: {e}")

# --- Seção de Histórico ---
with st.expander("Ver Histórico de Registros", expanded=True):
    if not st.session_state.history:
        st.info("Nenhum registro salvo ainda.")
    else:
        history_list = []
        for date_str, data in st.session_state.history.items():
            history_list.append({
                "Data": datetime.datetime.strptime(date_str, '%Y-%m-%d').strftime('%d/%m/%Y'),
                "Entrada": data.get('entrada', ''), "Saída": data.get('saida_real', ''),
                "Trabalhado": formatar_duracao(data.get('trabalho_liquido')),
                "Saldo do Dia": formatar_duracao(data.get('saldo_dia'), sinal=True),
            })
        
        df = pd.DataFrame(history_list).sort_values(by="Data", key=lambda x: pd.to_datetime(x, format='%d/%m/%Y'), ascending=False)
        st.dataframe(df, hide_index=True, use_container_width=True)
        
        st.write("Para excluir um dia, selecione-o no seletor de data acima e clique no botão abaixo.")
        date_key_to_delete = st.session_state.selected_date.strftime('%Y-%m-%d')
        if st.button(f"Excluir o dia {st.session_state.selected_date.strftime('%d/%m/%Y')}", type="secondary"):
            excluir_dia_do_historico(date_key_to_delete)
            st.rerun()

# --- Seção de Importar/Exportar ---
with st.expander("Importar / Exportar Histórico"):
    st.download_button(
        label="📥 Baixar Histórico (JSON)",
        data=json.dumps(st.session_state.history, indent=2),
        file_name=f"historico_jornada_{datetime.date.today()}.json",
        mime="application/json"
    )

    uploaded_file = st.file_uploader("📤 Carregar Histórico (JSON)", type="json")
    if uploaded_file is not None:
        try:
            new_history = json.load(uploaded_file)
            if isinstance(new_history, dict):
                st.session_state.history = new_history
                st.success("Histórico carregado com sucesso!")
                st.rerun()
            else:
                st.error("Arquivo JSON inválido.")
        except json.JSONDecodeError:
            st.error("Erro ao ler o arquivo.")

