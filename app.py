import streamlit as st
import pandas as pd

# Configuração da Página
st.set_page_config(page_title="Busca Aluno FSA", page_icon="🔍")

# CSS para o Card de Informação
st.markdown("""
    <style>
    .card {
        background-color: white; padding: 20px; border-radius: 12px;
        border-left: 8px solid #1e3a8a; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        color: #1e3a8a; margin-bottom: 15px;
    }
    .label { font-size: 0.8em; color: #666; font-weight: bold; }
    .info { font-size: 1.3em; font-weight: bold; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Link direto para os dados (Exportado como CSV)
URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQV4Cj-QnWSfJLD5I5TwNfEW6F0Ti_YFPve0yyzqOAW9clUyLlRvohv9ZKm7kGD7x6xTVo0qKlYohKl/pub?output=csv"

@st.cache_data(ttl=300)
def carregar_dados():
    return pd.read_csv(URL)

st.title("🔍 Busca Rápida de Alunos")

try:
    df = carregar_dados()
    # Limpa nomes de colunas
    df.columns = [c.strip().lower() for c in df.columns]
    
    # Busca reativa
    nome_busca = st.text_input("Digite o nome para pesquisar:", placeholder="Comece a digitar...")

    if nome_busca:
        # Filtra a lista
        filtro = df[df['nome'].astype(str).str.lower().str.contains(nome_busca.lower())]
        
        if not filtro.empty:
            for _, aluno in filtro.iterrows():
                # Tenta pegar a série/turma independente de como está escrito na planilha
                serie = aluno.get('serie', aluno.get('turma', aluno.get('série', 'Não informado')))
                
                st.markdown(f"""
                    <div class="card">
                        <div class="label">NOME DO ALUNO</div>
                        <div class="info">{aluno['nome'].upper()}</div>
                        <div class="label">SÉRIE / TURMA</div>
                        <div class="info">{serie}</div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("Aluno não encontrado.")
    else:
        st.info("💡 Dica: Digite apenas o primeiro nome para ver todos os resultados.")

except Exception as e:
    st.error("Erro ao carregar dados. Verifique se a planilha está 'Publicada na Web' como CSV.")
