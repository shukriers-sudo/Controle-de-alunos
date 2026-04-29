import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Classe Aluno
class Aluno:
    def __init__(self, id, nome, matricula, curso, email, telefone, data_cadastro):
        self.id = id
        self.nome = nome
        self.matricula = matricula
        self.curso = curso
        self.email = email
        self.telefone = telefone
        self.data_cadastro = data_cadastro

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'matricula': self.matricula,
            'curso': self.curso,
            'email': self.email,
            'telefone': self.telefone,
            'data_cadastro': self.data_cadastro
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            d['id'], d['nome'], d['matricula'], d['curso'], d['email'], d['telefone'], d['data_cadastro']
        )

# Função para carregar dados do CSV
def carregar_dados():
    if not os.path.exists('alunos.csv'):
        # Cria DataFrame vazio com colunas
        return pd.DataFrame(columns=['id', 'nome', 'matricula', 'curso', 'email', 'telefone', 'data_cadastro'])
    try:
        df = pd.read_csv('alunos.csv')
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}. Recriando arquivo.")
        return pd.DataFrame(columns=['id', 'nome', 'matricula', 'curso', 'email', 'telefone', 'data_cadastro'])

# Função para salvar dados no CSV
def salvar_dados(df):
    try:
        df.to_csv('alunos.csv', index=False)
    except Exception as e:
        st.error(f"Erro ao salvar dados: {e}")

# Função para obter próximo ID
def get_next_id(df):
    if df.empty:
        return 1
    return int(df['id'].max()) + 1

# Interface principal
st.title("📚 Sistema de Controle de Alunos")

# Menu lateral
menu = st.sidebar.selectbox("Escolha uma opção", ["➕ Adicionar Aluno", "📋 Consultar Alunos", "✏️ Editar Aluno", "🗑️ Apagar Aluno"])

# Carregar dados
df = carregar_dados()

if menu == "➕ Adicionar Aluno":
    st.header("Adicionar Novo Aluno")
    with st.form("add_aluno"):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome *")
            matricula = st.text_input("Matrícula *")
            curso = st.text_input("Curso *")
        with col2:
            email = st.text_input("Email")
            telefone = st.text_input("Telefone")
        submitted = st.form_submit_button("➕ Adicionar")
        if submitted:
            if not nome or not matricula or not curso:
                st.error("Nome, Matrícula e Curso são obrigatórios.")
            elif matricula in df['matricula'].values:
                st.error("Matrícula já existe.")
            else:
                id = get_next_id(df)
                data_cadastro = datetime.now().strftime("%Y-%m-%d")
                aluno = Aluno(id, nome, matricula, curso, email, telefone, data_cadastro)
                df = pd.concat([df, pd.DataFrame([aluno.to_dict()])], ignore_index=True)
                salvar_dados(df)
                st.success("Aluno adicionado com sucesso!")
                st.rerun()  # Recarregar para atualizar

elif menu == "📋 Consultar Alunos":
    st.header("Consultar Alunos")
    busca = st.text_input("Buscar por nome, matrícula ou curso")
    ordenar_por = st.selectbox("Ordenar por", df.columns if not df.empty else ['id'])
    if busca:
        df_filtrado = df[df.apply(lambda row: busca.lower() in str(row).lower(), axis=1)]
    else:
        df_filtrado = df
    if not df_filtrado.empty:
        df_filtrado = df_filtrado.sort_values(by=ordenar_por)
    st.dataframe(df_filtrado)
    st.write(f"Total de alunos: {len(df)}")

elif menu == "✏️ Editar Aluno":
    st.header("Editar Aluno")
    if df.empty:
        st.warning("Nenhum aluno cadastrado.")
    else:
        opcoes = df.apply(lambda row: f"{row['id']} - {row['nome']}", axis=1).tolist()
        selecionado = st.selectbox("Selecione o aluno", opcoes)
        if selecionado:
            id_selecionado = int(selecionado.split(' - ')[0])
            aluno = df[df['id'] == id_selecionado].iloc[0]
            with st.form("edit_aluno"):
                col1, col2 = st.columns(2)
                with col1:
                    nome = st.text_input("Nome *", value=aluno['nome'])
                    matricula = st.text_input("Matrícula *", value=aluno['matricula'])
                    curso = st.text_input("Curso *", value=aluno['curso'])
                with col2:
                    email = st.text_input("Email", value=aluno['email'])
                    telefone = st.text_input("Telefone", value=aluno['telefone'])
                submitted = st.form_submit_button("✏️ Atualizar")
                if submitted:
                    if not nome or not matricula or not curso:
                        st.error("Nome, Matrícula e Curso são obrigatórios.")
                    elif matricula != aluno['matricula'] and matricula in df['matricula'].values:
                        st.error("Matrícula já existe.")
                    else:
                        df.loc[df['id'] == id_selecionado, ['nome', 'matricula', 'curso', 'email', 'telefone']] = [nome, matricula, curso, email, telefone]
                        salvar_dados(df)
                        st.success("Aluno atualizado com sucesso!")
                        st.rerun()

elif menu == "🗑️ Apagar Aluno":
    st.header("Apagar Aluno")
    if df.empty:
        st.warning("Nenhum aluno cadastrado.")
    else:
        opcoes = df.apply(lambda row: f"{row['id']} - {row['nome']}", axis=1).tolist()
        selecionado = st.selectbox("Selecione o aluno", opcoes)
        if selecionado:
            id_selecionado = int(selecionado.split(' - ')[0])
            st.warning("Confirme a exclusão marcando a caixa abaixo.")
            confirm = st.checkbox("Confirmar exclusão")
            if st.button("🗑️ Apagar") and confirm:
                df = df[df['id'] != id_selecionado]
                salvar_dados(df)
                st.success("Aluno apagado com sucesso!")
                st.rerun()

# Rodapé no sidebar
st.sidebar.markdown("---")
st.sidebar.write(f"Total de alunos ativos: {len(df)}")

if __name__ == "__main__":
    pass  # Streamlit roda automaticamente