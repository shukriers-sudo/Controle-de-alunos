# CONTROLE-DE-ALUNOS

Sistema de controle de alunos desenvolvido em Python com Streamlit.

## Instalação

1. Clone o repositório:
   ```
   git clone https://github.com/seu-usuario/CONTROLE-DE-ALUNOS.git
   ```

2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

## Execução

Execute o comando:
```
streamlit run app.py
```

## Uso

- **Adicionar Aluno**: Preencha o formulário com nome, matrícula, curso, email e telefone. Clique em "Adicionar".
- **Consultar Alunos**: Visualize a lista de alunos, busque por nome, matrícula ou curso, e ordene por coluna.
- **Editar Aluno**: Selecione um aluno da lista, edite os dados e clique em "Atualizar".
- **Apagar Aluno**: Selecione um aluno, confirme a exclusão e clique em "Apagar".

## Funcionalidades

- CRUD completo: Adicionar, Consultar, Editar e Apagar alunos.
- Persistência em CSV.
- Validações de campos obrigatórios e unicidade de matrícula.
- Interface responsiva com Streamlit.
