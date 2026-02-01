import streamlit as st
import pandas as pd

st.set_page_config(page_title="Busca Aluno FSA", page_icon="🔍")

# Link de exportação direta (mais estável)
URL = "https://docs.google.com/spreadsheets/d/1yurzw28SK7rF6LPpbKYShICY0QgexeFbv0ShVbwUkjc/export?format=csv&gid=672132072"

@st.cache_data(ttl=10) # Cache curto para testar agora
def carregar_dados():
    # Tenta ler o CSV ignorando problemas de formatação
    return pd.read_csv(URL, on_bad_lines='skip', engine='python')

st.title("🔍 Busca Rápida de Alunos")

try:
    df = carregar_dados()
    
    # Limpa nomes de colunas (remove espaços e põe em minúsculo)
    df.columns = [str(c).strip().lower() for c in df.columns]
    
    nome_busca = st.text_input("Digite o nome do aluno:")

    if nome_busca:
        # Filtra na primeira ou segunda coluna (onde costuma estar o nome)
        # Usamos 'case=False' para não importar se é maiúsculo ou minúsculo
        mask = df.apply(lambda row: row.astype(str).str.contains(nome_busca, case=False).any(), axis=1)
        resultado = df[mask]
        
        if not resultado.empty:
            for _, aluno in resultado.iterrows():
                # Tenta encontrar a coluna de série/turma automaticamente
                colunas = list(aluno.index)
                serie_val = "Não encontrada"
                for c in colunas:
                    if 'serie' in c or 'turma' in c or 'curso' in c:
                        serie_val = aluno[c]
                        break
                
                st.markdown(f"""
                <div style="background-color: #ffffff; padding: 15px; border-radius: 10px; border-left: 5px solid #1e3a8a; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); margin-bottom: 10px;">
                    <p style="color: #666; margin: 0; font-size: 0.8em;">ALUNO:</p>
                    <p style="color: #1e3a8a; margin: 0; font-size: 1.2em; font-weight: bold;">{str(aluno.iloc[1]).upper()}</p>
                    <p style="color: #666; margin: 5px 0 0 0; font-size: 0.8em;">SÉRIE/TURMA:</p>
                    <p style="color: #333; margin: 0; font-weight: bold;">{serie_val}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("Nenhum registro encontrado.")

except Exception as e:
    st.error(f"Erro técnico: {e}")
    st.info("💡 Certifique-se de que a planilha está 'Compartilhada' como 'Qualquer pessoa com o link pode ler'.")
