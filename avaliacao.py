import streamlit as st
from datetime import datetime
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from utils.data_manager import create_dataframes, load_or_create_dataframes, calcular_desempenho, save_dataframes
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Configuração da página
st.set_page_config(page_title="Plataforma de Avaliação Pedagógica Municipal", layout="wide")
with open("styles.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Cabeçalho para mudança de tela (opção de cadastro de aluno, cadastro de escola, consulta de aluno, acesso a material didático, acesso a provas, acesso a gabaritos)
# Adicionar logo no canto superior esquerdo
# Carregar ou criar os dataframes
with st.spinner("Carregando dados..."):
    dataframes = load_or_create_dataframes()

df_aluno = dataframes['df_aluno']
df_escola = dataframes['df_escola']
df_prova = dataframes['df_prova']
df_gabarito = dataframes['df_gabarito']
# Botões de navegação
if "page" not in st.session_state:
    st.session_state.page = "home"

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.image("logo-evolutiva.jpg", use_container_width=False, width=145)

with col2:
    with st.expander("Cadastro", expanded=False): 
        st.write("Selecione uma das opções abaixo:")
        if st.button("Aluno", key="cadastro_aluno", use_container_width=True):
            st.session_state.page = "cadastro_aluno"
        if st.button("Escola", key="cadastro_escola", use_container_width=True): 
            st.session_state.page = "cadastro_escola"
        if st.button("Prova", key="cadastro_prova", use_container_width=True):
            st.session_state.page = "cadastro_prova"
        if st.button("Gabarito", key="cadastro_gabarito", use_container_width=True):
            st.session_state.page = "cadastro_gabarito"

with col3:
    with st.expander("Consulta", expanded=False): 
        st.write("Selecione uma das opções abaixo:")
        if st.button("Geral", key="consulta_geral", use_container_width=True):
            st.session_state.page = "consulta_geral"
        if st.button("Escola", key="consulta_escola", use_container_width=True):
            st.session_state.page = "consulta_escola"
        if st.button("Série", key="consulta_serie", use_container_width=True): 
            st.session_state.page = "consulta_serie"
        if st.button("Disciplina", key="consulta_disciplina", use_container_width=True):
            st.session_state.page = "consulta_disciplina"
        if st.button("Zona", key="consulta_zona", use_container_width=True):
            st.session_state.page = "consulta_zona"
        if st.button("Gênero", key="consulta_genero", use_container_width=True):
            st.session_state.page = "consulta_genero"
        if st.button("Aluno", key="consulta_aluno", use_container_width=True):
            st.session_state.page = "consulta_aluno"

with col4:
    with st.expander("Material Didático", expanded=False):
        st.write("Selecione uma das opções abaixo:")
        if st.button("E-books", key="material_ebooks", use_container_width=True):
            st.session_state.page = "material_ebooks"
        if st.button("Vídeos", key="material_videos", use_container_width=True):
            st.session_state.page = "material_videos"
        if st.button("Exercícios Práticos", key="material_exercicios", use_container_width=True):
            st.session_state.page = "material_exercicios"

with col5:
    with st.expander("Pedagógico", expanded=False):
        st.write("Selecione uma das opções abaixo:")
        if st.button("Cronograma", key="pedagogico_cronograma", use_container_width=True):
            st.session_state.page = "pedagogico_cronograma"
        if st.button("Conteúdo Programático", key="pedagogico_conteudo", use_container_width=True):
            st.session_state.page = "pedagogico_conteudo"

with col6:
    with st.expander("Acesso", expanded=False):
        st.write("Selecione uma das opções abaixo:")
        if st.button("Gestor", key="acesso_gestor", use_container_width=True):
            st.session_state.page = "acesso_gestor"
        if st.button("Professor", key="acesso_professor", use_container_width=True):
            st.session_state.page = "acesso_professor"
        if st.button("Aluno", key="acesso_aluno", use_container_width=True):
            st.session_state.page = "acesso_aluno"
        if st.button("Secretário", key="acesso_secretario", use_container_width=True):
            st.session_state.page = "acesso_secretario"
        if st.button("Prefeito", key="acesso_prefeito", use_container_width=True):
            st.session_state.page = "acesso_prefeito"

if st.session_state.page == "home":
    st.title("Plataforma de Avaliação Pedagógica Municipal")
    st.write("""
    1. Conhecimento  
    2. Pensamento Científico, Crítico e Criativo  
    3. Repertório Cultural  
    4. Comunicação  
    5. Cultura Digital  
    6. Trabalho e Projeto de Vida  
    7. Argumentação  
    8. Autoconhecimento e Autocuidado  
    9. Empatia e Cooperação  
    10. Responsabilidade e Cidadania
    """)

# Exibir o formulário apenas quando o botão "Cadastro de Aluno" for clicado
if st.session_state.page == "cadastro_aluno":
    # Título da página
    st.title("Cadastro de Aluno")
    # Campos de entrada
    with st.form("cadastro_form"):
        st.header("Informações do Aluno")
        
        col1, col2 = st.columns(2)

        with col1:
            # Nome
            nome = st.text_input("Nome do Aluno", placeholder="Digite o nome completo")

        with col2:
            # Data de Nascimento
            data_nascimento = st.date_input(
                "Data de Nascimento", 
                min_value=datetime(1900, 1, 1), 
                max_value=datetime.today(), 
                format="DD/MM/YYYY"
            )

        col1, col2 = st.columns(2)
        with col1:
        # Gênero
            genero = st.selectbox("Gênero", options=["Selecione o gênero", "Masculino", "Feminino"])
        with col2:
            serie = st.selectbox("Série", options=["Selecione uma série", "1º Ano", "2º Ano", "3º Ano", "4º Ano", "5º Ano", "6º Ano", "7º Ano", "8º Ano", "9º Ano", "1º Ano Médio", "2º Ano    Médio", "3º Ano Médio"])

        # Nome da Escola
        if not df_escola.empty:
            nome_escola = st.selectbox(
            "Nome da Escola",
            options=["Selecione a escola"] + df_escola["nomeEscola"].dropna().unique().tolist()
            )
        else:
            nome_escola = st.text_input("Nome da Escola", placeholder="Digite o nome da escola")

        col1, col2 = st.columns(2)

        with col1:
            # Zona Rural ou Urbana
            zona = st.radio("Localização da Escola", options=["Zona Urbana", "Zona Rural"])

        # Laudo
        st.subheader("Laudo Médico/Especialista")
        opcoes_laudo = [
            "Autismo", "TDAH", "TOD", "Esquizofrenia", "Deficiência Intelectual",
            "Baixa Acuidade Visual", "Surdocegueira", "Outros"
        ]
        laudo_selecionado = st.multiselect("Selecione as condições (se aplicável)", opcoes_laudo)
        outros_laudo = st.text_input("Outros (especificação)(se aplicável)", max_chars=100)

        # Botão de envio
        submitted = st.form_submit_button("Enviar")

        # Processamento do formulário
        if submitted:
            # Verifica se todos os campos obrigatórios foram preenchidos
            if not nome or genero == "Selecione o gênero" or serie == "Selecione uma série" or not zona or not nome_escola:
                st.error("Por favor, preencha todos os campos obrigatórios.")
            else:
                st.success("Formulário enviado com sucesso!")
                st.write("### Resumo do Cadastro")
                st.write(f"**Nome:** {nome}")
                st.write(f"**Gênero:** {genero}")
                st.write(f"**Série:** {serie}")
                st.write(f"**Zona:** {zona}")
                st.write(f"**Nome da Escola:** {nome_escola}")
                st.write(f"**Data de Nascimento:** {data_nascimento.strftime('%d/%m/%Y')}")
                st.write(f"**Laudo Médico/Especialista:** {', '.join(laudo_selecionado) if laudo_selecionado else 'Nenhum'}")
                if "Outros" in laudo_selecionado and outros_laudo:
                    st.write(f"**Outros (especificação):** {outros_laudo}")

                dataframes = load_or_create_dataframes()
                # Gerar um ID único para o aluno
                id_aluno = len(df_aluno) + 1 if not df_aluno.empty else 1

                # Criar um dicionário com os dados do aluno
                novo_aluno = {
                    "id_aluno": id_aluno,
                    "nomeAluno": nome,
                    "dataNascimento": data_nascimento.strftime('%Y-%m-%d'),
                    "genero": genero,
                    "serie": serie,
                    "nomeEscola": nome_escola,
                    "localizacaoEscola": zona,
                    "laudoMedico": ", ".join(laudo_selecionado) if laudo_selecionado else None
                }

                # Adicionar o novo aluno ao dataframe
                df_aluno = pd.concat([df_aluno, pd.DataFrame([novo_aluno])], ignore_index=True)

                # Exibir mensagem de sucesso
                st.write("Aluno cadastrado com sucesso no sistema!")
                st.write("#### DataFrame de Alunos Atualizado:")
                st.dataframe(df_aluno, use_container_width=True)
                save_dataframes({'df_aluno': df_aluno, 'df_escola': df_escola, 'df_prova': dataframes['df_prova'], 'df_gabarito': dataframes['df_gabarito']})

if st.session_state.page == "cadastro_escola":
    st.title("Cadastro de Escola")
    st.write("Esta página é para o cadastro de escolas.")
    # Adicione aqui o código para o cadastro de escolas
    # Esta seção pode incluir campos como Nome da Escola, Endereço, Telefone, Email, etc.
    # Além disso, pode haver validações e um botão para salvar as informações no banco de dados.
    # Exemplo de campos:
    with st.form("cadastro_escola_form"):
        nome_escola = st.text_input("Nome da Escola", placeholder="Digite o nome da escola")
        endereco = st.text_input("Endereço", placeholder="Digite o endereço da escola")
        telefone = st.text_input("Telefone", placeholder="Digite o telefone da escola")
        email = st.text_input("Email", placeholder="Digite o email da escola")
        
        submitted = st.form_submit_button("Enviar")
        
        if submitted:
            if not nome_escola or not endereco or not telefone or not email:
                st.error("Por favor, preencha todos os campos obrigatórios.")
            else:
                st.success("Cadastro de Escola enviado com sucesso!")
                st.write(f"**Nome da Escola:** {nome_escola}")
                st.write(f"**Endereço:** {endereco}")
                st.write(f"**Telefone:** {telefone}")
                st.write(f"**Email:** {email}")
            
                # Adicionar lógica para salvar os dados no banco de dados ou em um arquivo
                dataframes = load_or_create_dataframes()
                # Gerar um ID único para a escola
                id_escola = len(df_escola) + 1 if not df_escola.empty else 1

                # Criar um dicionário com os dados da escola
                nova_escola = {
                    "id_escola": id_escola,
                    "nomeEscola": nome_escola,
                    "endereco": endereco,
                    "telefone": telefone,
                    "email": email
                }

                # Adicionar a nova escola ao dataframe
                df_escola = pd.concat([df_escola, pd.DataFrame([nova_escola])], ignore_index=True)

                # Exibir mensagem de sucesso
                st.write("Escola cadastrada com sucesso no sistema!")
                st.write("#### DataFrame de Escolas Atualizado:")
                st.dataframe(df_escola, use_container_width=True)
                save_dataframes({'df_aluno': df_aluno, 'df_escola': df_escola, 'df_prova': dataframes['df_prova'], 'df_gabarito': dataframes['df_gabarito']})

if st.session_state.page == "cadastro_prova":
    st.title("Cadastro de Prova")
    

    # Informações do Aluno
    st.subheader("Informações do Aluno")
    # ID do Aluno
    id_aluno = st.selectbox(
        "ID do Aluno",
        options=df_aluno["id_aluno"].tolist() if not df_aluno.empty else [],
        placeholder="Selecione o ID do aluno"
    )
    # Nome do Aluno
    # Buscar o nome do aluno automaticamente pelo ID selecionado
    if id_aluno:
        nome_aluno = df_aluno.loc[df_aluno["id_aluno"] == id_aluno, "nomeAluno"].values[0] if not df_aluno.empty and id_aluno in df_aluno["id_aluno"].values else ""
    else:
        nome_aluno = ""
    st.text_input("Nome do Aluno", value=nome_aluno, disabled=True)
    # Área de Conhecimento e Matéria
    st.subheader("Áreas de Conhecimento")
    col1, col2 = st.columns(2)

    with col1:
        materia = [
            "Selecione uma matéria",
            "Português",
            "Inglês",
            "Arte",
            "Educação Física",
            "Espanhol",
            "Matemática",
            "História",
            "Geografia",
            "Ciências",
            "Religião"
        ]
        materia_selecionada = st.selectbox("Matéria", options=materia)
    with col2:
        serie_prova = st.selectbox("Série", options=["Selecione uma série", "1º Ano", "2º Ano", "3º Ano", "4º Ano", "5º Ano", "6º Ano", "7º Ano", "8º Ano", "9º Ano", "1º Ano Médio", "2º Ano Médio", "3º Ano Médio"])
            
     # Questões
    st.subheader("Respostas das Questões")
    cols = st.columns(5)
    questoes = {}
    for i in range(1, 6):
        with cols[i - 1]:
            resposta = st.selectbox(
                f"Questão {i}", options=["A", "B", "C", "D", "E"], key=f"q{i}"
            )
            questoes[f"Questão {i}"] = resposta
    cols = st.columns(5)
    for i in range(6, 11):
        with cols[i - 6]:
            resposta = st.selectbox(
                f"Questão {i}", options=["A", "B", "C", "D", "E"], key=f"q{i}"
            )
            questoes[f"Questão {i}"] = resposta

    # Botão de envio
    submitted = st.button("Enviar Respostas")

    if submitted:
        # Verifica se o nome do aluno foi preenchido
        if not id_aluno or not nome_aluno or materia_selecionada == "Selecione uma matéria"  or serie_prova == "Selecione uma série":
           st.error("Por favor, preencha todos os campos obrigatórios.")
        else:  
            st.success("Respostas enviadas com sucesso!")
            st.write("### Resumo do Cadastro")
            st.write(f"**ID do Aluno:** {id_aluno}")
            st.write(f"**Nome do Aluno:** {nome_aluno}")
            st.write(f"**Matéria:** {materia_selecionada}")
            st.write(f"**Série:** {serie_prova}")
            for questao, resposta in questoes.items():
                st.write(f"**{questao}:** {resposta}")

            # Adicionar lógica para salvar os dados no banco de dados ou em um arquivo
            dataframes = load_or_create_dataframes()
            # Gerar um ID único para a escola
            id_prova = len(df_prova) + 1 if not df_prova.empty else 1
            # Criar um dicionário com os dados da prova
            nova_prova = {
                "id_prova": id_prova,
                "id_aluno": id_aluno,
                "nomeAluno": nome_aluno,
                "materia": materia_selecionada,
                "serie": serie_prova,
                "questao_1": questoes["Questão 1"],
                "questao_2": questoes["Questão 2"],
                "questao_3": questoes["Questão 3"],
                "questao_4": questoes["Questão 4"],
                "questao_5": questoes["Questão 5"],
                "questao_6": questoes["Questão 6"],
                "questao_7": questoes["Questão 7"],
                "questao_8": questoes["Questão 8"],
                "questao_9": questoes["Questão 9"],
                "questao_10": questoes["Questão 10"]
            }
            # Adicionar a nova prova ao dataframe
            df_prova = pd.concat([df_prova, pd.DataFrame([nova_prova])], ignore_index=True)
            # Exibir mensagem de sucesso
            st.write("Prova cadastrada com sucesso no sistema!")
            st.write("#### DataFrame de Provas Atualizado:")
            st.dataframe(df_prova, use_container_width=True)
            save_dataframes({'df_aluno': df_aluno, 'df_escola': df_escola, 'df_prova': df_prova, 'df_gabarito': df_gabarito})

if st.session_state.page == "cadastro_gabarito":
    st.title("Cadastro de Gabarito")
    # Área de Conhecimento e Matéria
    st.subheader("Áreas de Conhecimento")
    col1, col2 = st.columns(2)

    with col1:
        materia = [
            "Selecione uma matéria",
            "Português",
            "Inglês",
            "Arte",
            "Educação Física",
            "Espanhol",
            "Matemática",
            "História",
            "Geografia",
            "Ciências",
            "Religião"
        ]
        materia_selecionada = st.selectbox("Matéria", options=materia)
    with col2:
        serie_prova = st.selectbox("Série", options=["Selecione uma série", "1º Ano", "2º Ano", "3º Ano", "4º Ano", "5º Ano", "6º Ano", "7º Ano", "8º Ano", "9º Ano", "1º Ano Médio", "2º Ano Médio", "3º Ano Médio"])
            
     # Questões
    st.subheader("Respostas das Questões")
    cols = st.columns(5)
    questoes = {}
    for i in range(1, 6):
        with cols[i - 1]:
            resposta = st.selectbox(
                f"Questão {i}", options=["A", "B", "C", "D", "E"], key=f"q{i}"
            )
            questoes[f"Questão {i}"] = resposta
    cols = st.columns(5)
    for i in range(6, 11):
        with cols[i - 6]:
            resposta = st.selectbox(
                f"Questão {i}", options=["A", "B", "C", "D", "E"], key=f"q{i}"
            )
            questoes[f"Questão {i}"] = resposta

    # Botão de envio
    submitted = st.button("Enviar Respostas")

    if submitted:
        # Verifica se o nome do aluno foi preenchido
        if materia_selecionada == "Selecione uma matéria" or serie_prova == "Selecione uma série":
           st.error("Por favor, preencha todos os campos obrigatórios.")
        else:  
            st.success("Respostas enviadas com sucesso!")
            st.write("### Resumo do Cadastro")
            st.write(f"**Matéria:** {materia_selecionada}")
            st.write(f"**Série:** {serie_prova}")
            for questao, resposta in questoes.items():
                st.write(f"**{questao}:** {resposta}")

            # Adicionar lógica para salvar os dados no banco de dados ou em um arquivo
            dataframes = load_or_create_dataframes()
            # Gerar um ID único para a escola
            id_gabarito = len(df_gabarito) + 1 if not df_gabarito.empty else 1
            # Criar um dicionário com os dados da prova
            novo_gabarito = {
                "id_gabarito": id_gabarito,
                "materia": materia_selecionada,
                "serie": serie_prova,
                "questao_1": questoes["Questão 1"],
                "questao_2": questoes["Questão 2"],
                "questao_3": questoes["Questão 3"],
                "questao_4": questoes["Questão 4"],
                "questao_5": questoes["Questão 5"],
                "questao_6": questoes["Questão 6"],
                "questao_7": questoes["Questão 7"],
                "questao_8": questoes["Questão 8"],
                "questao_9": questoes["Questão 9"],
                "questao_10": questoes["Questão 10"]
            }
            # Adicionar a nova escola ao dataframe
            df_gabarito = pd.concat([df_gabarito, pd.DataFrame([novo_gabarito])], ignore_index=True)
            # Exibir mensagem de sucesso
            st.write("Gabarito cadastrado com sucesso no sistema!")
            st.write("#### DataFrame de Gabaritos Atualizado:")
            st.dataframe(df_gabarito, use_container_width=True)
            save_dataframes({'df_aluno': df_aluno, 'df_escola': df_escola, 'df_prova': df_prova, 'df_gabarito': df_gabarito})

if st.session_state.page == "consulta_aluno":
    st.title("Consulta de Aluno")
    st.write("Esta página é para a consulta de alunos.")
    # Adicione aqui o código para a consulta de alunos
    # Esta seção pode incluir campos como Nome do Aluno, Data de Nascimento, etc.
    # Além disso, pode haver validações e um botão para buscar as informações no banco de dados.
    # Exemplo de campos:
    with st.form("consulta_aluno_form"):
        nome_aluno = st.text_input("Nome do Aluno", placeholder="Digite o nome completo")
        data_nascimento = st.date_input(
            "Data de Nascimento", 
            min_value=datetime(1900, 1, 1), 
            max_value=datetime.today(), 
            format="DD/MM/YYYY"
        )
        
        submitted = st.form_submit_button("Consultar")
        
        if submitted:
            if not nome_aluno or not data_nascimento:
                st.error("Por favor, preencha todos os campos obrigatórios.")
            else:
                st.success("Consulta realizada com sucesso!")
                st.write(f"**Nome do Aluno:** {nome_aluno}")
                st.write(f"**Data de Nascimento:** {data_nascimento.strftime('%d/%m/%Y')}")

if st.session_state.page == "consulta_geral":
    st.title("Consulta Geral")
    st.write("Esta página é para a consulta geral de informações.")
    # Adicione aqui o código para a consulta geral
    # Esta seção pode incluir campos como Nome, Data de Nascimento, etc.
    # Além disso, pode haver validações e um botão para buscar as informações no banco de dados.
    # Exemplo de campos:
     # Carregar ou criar os dataframes
    with st.spinner("Carregando dados..."):
        dataframes = load_or_create_dataframes()
    
    # Calcular métricas de desempenho
    with st.spinner("Calculando desempenho..."):
        try:
            df_resultados = calcular_desempenho(df_prova, df_gabarito)
        except Exception as e:
            st.error(f"Erro ao calcular desempenho: {e}")
            st.stop()
    
    # Divisão do dashboard em abas
    tab1, tab2, tab3, tab4 = st.tabs(["Visão Geral", "Desempenho por Matéria", "Desempenho por Série", "Análises Específicas"])
    
    #--------------------------
    # TAB 1: VISÃO GERAL
    #--------------------------
    with tab1:
        # Visão geral - Métricas
        st.subheader("Métricas Gerais")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total de Alunos", len(df_aluno))
        with col2:
            st.metric("Total de Escolas", len(df_escola))
        with col3:
            st.metric("Total de Provas", len(df_prova))
        with col4:
            if not df_resultados.empty:
                nota_media = round(df_resultados['nota'].mean(), 2)
                st.metric("Nota Média Geral", f"{nota_media:.2f}")
            else:
                st.metric("Nota Média Geral", "N/A")
        
        # Distribuição de alunos por série
        st.subheader("Distribuição de alunos por série")
        fig, ax = plt.subplots(figsize=(10, 6))
        alunos_por_serie = df_aluno['serie'].value_counts().sort_index()
        sns.barplot(x=alunos_por_serie.index, y=alunos_por_serie.values, ax=ax)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig)
        
        # Visualizações de distribuição
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Distribuição por Gênero")
            fig, ax = plt.subplots()
            genero_counts = df_aluno['genero'].value_counts()
            ax.pie(genero_counts, labels=genero_counts.index, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            st.pyplot(fig)
            
        with col2:
            st.subheader("Localização das Escolas")
            fig, ax = plt.subplots()
            localizacao_counts = df_aluno['localizacaoEscola'].value_counts()
            ax.pie(localizacao_counts, labels=localizacao_counts.index, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            st.pyplot(fig)

        st.subheader("DataFrames do Sistema")
        st.write("**DataFrame de Escolas:**")
        st.dataframe(df_escola, use_container_width=True)
        st.write("**DataFrame de Alunos:**")
        st.dataframe(df_aluno, use_container_width=True)
        st.write("**DataFrame de Provas:**")
        st.dataframe(df_prova, use_container_width=True)
        st.write("**DataFrame de Gabaritos:**")
        st.dataframe(df_gabarito, use_container_width=True)
    
    #--------------------------
    # TAB 2: DESEMPENHO POR MATÉRIA
    #--------------------------
    with tab2:
        st.subheader("Desempenho por Matéria")
        
        if not df_resultados.empty:
            # Desempenho médio por matéria
            desempenho_por_materia = df_resultados.groupby('materia')['nota'].mean().sort_values(ascending=False)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x=desempenho_por_materia.index, y=desempenho_por_materia.values, ax=ax)
            plt.xticks(rotation=45, ha='right')
            plt.ylabel('Nota Média')
            plt.tight_layout()
            st.pyplot(fig)
            
            # Filtro por matéria
            materia_selecionada = st.selectbox(
                "Selecione uma matéria para análise detalhada",
                sorted(df_resultados['materia'].unique())
            )
            
            # Análise detalhada da matéria selecionada
            st.subheader(f"Análise de {materia_selecionada}")
            
            # Filtrar dados para a matéria selecionada
            df_materia = df_resultados[df_resultados['materia'] == materia_selecionada]
            
            # Estatísticas descritivas
            col1, col2, col3 = st.columns(3)
            col1.metric("Nota Média", f"{df_materia['nota'].mean():.2f}")
            col2.metric("Nota Mínima", f"{df_materia['nota'].min():.2f}")
            col3.metric("Nota Máxima", f"{df_materia['nota'].max():.2f}")
            
            # Distribuição das notas
            st.write("Distribuição das notas")
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.histplot(df_materia['nota'], bins=10, kde=True, ax=ax)
            plt.xlabel('Nota')
            plt.ylabel('Frequência')
            st.pyplot(fig)
            
            # Desempenho por série na matéria selecionada
            desempenho_por_serie = df_materia.groupby('serie')['nota'].mean().sort_index()
            
            st.write(f"Desempenho por série em {materia_selecionada}")
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x=desempenho_por_serie.index, y=desempenho_por_serie.values, ax=ax)
            plt.xticks(rotation=45, ha='right')
            plt.ylabel('Nota Média')
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.info("Não há dados de resultados disponíveis para análise.")
    
    #--------------------------
    # TAB 3: DESEMPENHO POR SÉRIE
    #--------------------------
    with tab3:
        st.subheader("Desempenho por Série")
        
        if not df_resultados.empty:
            # Desempenho médio por série
            desempenho_por_serie = df_resultados.groupby('serie')['nota'].mean().sort_index()
            
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x=desempenho_por_serie.index, y=desempenho_por_serie.values, ax=ax)
            plt.xticks(rotation=45, ha='right')
            plt.ylabel('Nota Média')
            plt.tight_layout()
            st.pyplot(fig)
            
            # Filtro por série
            serie_selecionada = st.selectbox(
                "Selecione uma série para análise detalhada",
                sorted(df_resultados['serie'].unique())
            )
            
            # Análise detalhada da série selecionada
            st.subheader(f"Análise do {serie_selecionada}")
            
            # Filtrar dados para a série selecionada
            df_serie = df_resultados[df_resultados['serie'] == serie_selecionada]
            
            # Desempenho por matéria na série selecionada
            desempenho_por_materia = df_serie.groupby('materia')['nota'].mean().sort_values(ascending=False)
            
            st.write(f"Desempenho por matéria no {serie_selecionada}")
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x=desempenho_por_materia.index, y=desempenho_por_materia.values, ax=ax)
            plt.xticks(rotation=45, ha='right')
            plt.ylabel('Nota Média')
            plt.tight_layout()
            st.pyplot(fig)
            
            # Top 5 alunos da série
            st.write(f"Top 5 alunos com melhor desempenho no {serie_selecionada}")
            top_alunos = df_serie.groupby('nomeAluno')['nota'].mean().sort_values(ascending=False).head(5)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x=top_alunos.index, y=top_alunos.values, ax=ax)
            plt.xticks(rotation=45, ha='right')
            plt.ylabel('Nota Média')
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.info("Não há dados de resultados disponíveis para análise.")
    
    #--------------------------
    # TAB 4: ANÁLISES ESPECÍFICAS
    #--------------------------
    with tab4:
        st.subheader("Análises Específicas")
        
        # Análise de alunos com laudos médicos
        if not df_resultados.empty and 'laudoMedico' in df_aluno.columns:
            st.write("Desempenho de Alunos com Laudos Médicos")
            
            # Mesclar resultados com dados de alunos para ter informação de laudo
            df_merged = df_resultados.merge(df_aluno[['id_aluno', 'laudoMedico']], on='id_aluno')
            
            # Agrupar por status de laudo e calcular média
            desempenho_por_laudo = df_merged.groupby('laudoMedico')['nota'].mean()
            
            # Criar dataframe para visualização
            df_laudo = pd.DataFrame({
                'Status': ['Com Laudo Médico', 'Sem Laudo Médico'],
                'Nota Média': [
                    desempenho_por_laudo.get(True, 0),
                    desempenho_por_laudo.get(False, 0)
                ]
            })
            
            # Plotar
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.barplot(x='Status', y='Nota Média', data=df_laudo, ax=ax)
            plt.ylim(0, 10)
            st.pyplot(fig)
            
            # Tabela de desempenho por laudo e matéria
            st.subheader("Desempenho por Matéria e Status de Laudo Médico")
            desempenho_detalhado = df_merged.groupby(['materia', 'laudoMedico'])['nota'].mean().reset_index()
            desempenho_detalhado['laudoMedico'] = desempenho_detalhado['laudoMedico'].map({True: 'Com Laudo', False: 'Sem Laudo'})
            desempenho_detalhado = desempenho_detalhado.pivot(index='materia', columns='laudoMedico', values='nota').reset_index()
            st.dataframe(desempenho_detalhado, use_container_width=True)
        
        # Tabela de resultados detalhados
        st.subheader("Resultados Detalhados")
        
        # Filtros
        col1, col2, col3 = st.columns(3)
        with col1:
            materias = ['Todas'] + sorted(df_resultados['materia'].unique().tolist() if not df_resultados.empty else [])
            materia_selecionada = st.selectbox("Filtrar por Matéria", materias, key="materia_filter")
        
        with col2:
            series = ['Todas'] + sorted(df_resultados['serie'].unique().tolist() if not df_resultados.empty else [])
            serie_selecionada = st.selectbox("Filtrar por Série", series, key="serie_filter")
        
        with col3:
            ordem = st.selectbox("Ordenar por", ["Nota (maior para menor)", "Nota (menor para maior)"])
        
        # Aplicar filtros
        if not df_resultados.empty:
            df_filtrado = df_resultados.copy()
            
            if materia_selecionada != 'Todas':
                df_filtrado = df_filtrado[df_filtrado['materia'] == materia_selecionada]
            
            if serie_selecionada != 'Todas':
                df_filtrado = df_filtrado[df_filtrado['serie'] == serie_selecionada]
            
            # Ordenar
            if ordem == "Nota (maior para menor)":
                df_filtrado = df_filtrado.sort_values('nota', ascending=False)
            else:
                df_filtrado = df_filtrado.sort_values('nota', ascending=True)
            
            # Exibir tabela
            colunas_exibir = ['id_aluno', 'nomeAluno', 'serie', 'materia', 'acertos', 'total_questoes', 'nota']
            st.dataframe(df_filtrado[colunas_exibir], use_container_width=True)
            
            # Download dos dados em PDF

            def gerar_pdf(dataframe):
                buffer = BytesIO()
                pdf = canvas.Canvas(buffer, pagesize=letter)
                pdf.setFont("Helvetica", 10)
                width, height = letter
                x_offset, y_offset = 50, height - 50
                line_height = 15

                pdf.drawString(x_offset, y_offset, "Resultados Filtrados")
                y_offset -= 20

                colunas = dataframe.columns.tolist()
                pdf.drawString(x_offset, y_offset, " | ".join(colunas))
                y_offset -= line_height

                for _, row in dataframe.iterrows():
                    linha = " | ".join(str(row[col]) for col in colunas)
                    pdf.drawString(x_offset, y_offset, linha)
                    y_offset -= line_height
                    if y_offset < 50:  # Nova página se necessário
                        pdf.showPage()
                        pdf.setFont("Helvetica", 10)
                        y_offset = height - 50

                pdf.save()
                buffer.seek(0)
                return buffer

            if not df_filtrado.empty:
                pdf_buffer = gerar_pdf(df_filtrado[colunas_exibir])
                st.download_button(
                    label="📥 Baixar Dados Filtrados (PDF)",
                    data=pdf_buffer,
                    file_name="resultados_filtrados.pdf",
                    mime="application/pdf",
                )
        else:
            st.info("Nenhum resultado disponível para exibição.")

if st.session_state.page == "consulta_escola":
    st.title("Consulta de Escola")
    st.write("Esta página é para a consulta de escolas.")
    # Adicione aqui o código para a consulta de escolas
    # Esta seção pode incluir campos como Nome da Escola, Endereço, Telefone, Email, etc.
    # Além disso, pode haver validações e um botão para buscar as informações no banco de dados.
    # Exemplo de campos:
    with st.form("consulta_escola_form"):
        nome_escola = st.text_input("Nome da Escola", placeholder="Digite o nome da escola")
        
        submitted = st.form_submit_button("Consultar")
        
        if submitted:
            if not nome_escola:
                st.error("Por favor, preencha o campo obrigatório.")
            else:
                st.success("Consulta de Escola realizada com sucesso!")
                st.write(f"**Nome da Escola:** {nome_escola}")

if st.session_state.page == "consulta_serie":
    st.title("Consulta de Série")
    st.write("Esta página é para a consulta de séries.")
    # Adicione aqui o código para a consulta de séries
    # Esta seção pode incluir campos como Nome da Série, Ano, etc.
    # Além disso, pode haver validações e um botão para buscar as informações no banco de dados.
    # Exemplo de campos:
    with st.form("consulta_serie_form"):
        nome_serie = st.selectbox("Série", options=["Selecione uma série", "1º Ano", "2º Ano", "3º Ano", "4º Ano", "5º Ano", "6º Ano", "7º Ano", "8º Ano", "9º Ano", "1º Ano Médio", "2º Ano Médio", "3º Ano Médio"])
        
        submitted = st.form_submit_button("Consultar")
        
        if submitted:
            if not nome_serie:
                st.error("Por favor, preencha o campo obrigatório.")
            else:
                st.success("Consulta de Série realizada com sucesso!")
                st.write(f"**Nome da Série:** {nome_serie}")

if st.session_state.page == "consulta_disciplina":
    st.title("Consulta de Disciplina")
    st.write("Esta página é para a consulta de disciplinas.")
    materia = [
            "Selecione uma matéria",
            "Português",
            "Inglês",
            "Arte",
            "Educação Física",
            "Espanhol",
            "Matemática",
            "História",
            "Geografia",
            "Ciências",
            "Religião"
        ]
    with st.form("consulta_disciplina_form"):
        nome_disciplina = materia_selecionada = st.selectbox("Matéria", options=materia)
        submitted = st.form_submit_button("Consultar")
        if submitted:
            if not nome_disciplina:
                st.error("Por favor, preencha o campo obrigatório.")
            else:
                st.success("Consulta de Disciplina realizada com sucesso!")
                st.write(f"**Nome da Disciplina:** {nome_disciplina}")

if st.session_state.page == "consulta_zona":
    st.title("Consulta de Zona")
    st.write("Esta página é para a consulta de zonas.")
    # Adicione aqui o código para a consulta de zonas
    # Esta seção pode incluir campos como Zona Rural ou Urbana, Nome da Escola, etc.
    # Além disso, pode haver validações e um botão para buscar as informações no banco de dados.
    # Exemplo de campos:
    with st.form("consulta_zona_form"):
        zona = st.radio("Localização da Escola", options=["Zona Urbana", "Zona Rural"])
        
        submitted = st.form_submit_button("Consultar")
        
        if submitted:
            if not zona:
                st.error("Por favor, preencha o campo obrigatório.")
            else:
                st.success("Consulta de Zona realizada com sucesso!")
                st.write(f"**Localização da Escola:** {zona}")

if st.session_state.page == "consulta_genero":
    st.title("Consulta de Gênero")
    st.write("Esta página é para a consulta de gêneros.")
    # Adicione aqui o código para a consulta de gêneros
    # Esta seção pode incluir campos como Gênero, Nome da Escola, etc.
    # Além disso, pode haver validações e um botão para buscar as informações no banco de dados.
    # Exemplo de campos:
    with st.form("consulta_genero_form"):
        genero = st.selectbox("Gênero", options=["Selecione o gênero", "Masculino", "Feminino"])
        
        submitted = st.form_submit_button("Consultar")
        
        if submitted:
            if not genero:
                st.error("Por favor, preencha o campo obrigatório.")
            else:
                st.success("Consulta de Gênero realizada com sucesso!")
                st.write(f"**Gênero:** {genero}")                

if st.session_state.page == "material_ebooks":
    st.title("Material Didático - E-books")
    st.write("Esta página é para o acesso a E-books.")
    # Adicione aqui o código para o acesso a E-books
    # Esta seção pode incluir links ou arquivos para download de E-books.

if st.session_state.page == "material_videos":
    st.title("Material Didático - Vídeos")
    st.write("Esta página é para o acesso a vídeos.")
    # Adicione aqui o código para o acesso a vídeos
    col1, col2 = st.columns(2)

    with col1:
        st.video("https://youtu.be/ZR_Ou01WsK0?si=cKVZa4We_CCCiBHU")

    with col2:
        st.video("https://www.youtube.com/watch?v=C00IHVngcfo")

if st.session_state.page == "material_exercicios":
    st.title("Material Didático - Exercícios Práticos")
    st.write("Esta página é para o acesso a exercícios práticos.")
    # Adicione aqui o código para o acesso a exercícios práticos
    # Esta seção pode incluir links ou arquivos para download de exercícios práticos.
    # Adicionar um exemplo de PDF para download
    st.subheader("Exemplo de Exercícios Práticos")
    # Seleção de série e matéria
    serie = st.selectbox("Selecione a Série", options=["Selecione uma série", "1º Ano", "2º Ano", "3º Ano", "4º Ano", "5º Ano", "6º Ano", "7º Ano", "8º Ano", "9º Ano", "1º Ano Médio", "2º Ano Médio", "3º Ano Médio"])
    materia = st.selectbox("Selecione a Matéria", 
                           options=[
                            "Selecione uma matéria",
                            "Português",
                            "Inglês",
                            "Arte",
                            "Educação Física",
                            "Espanhol",
                            "Matemática",
                            "História",
                            "Geografia",
                            "Ciências",
                            "Religião"])

    if serie != "Selecione uma série" and materia != "Selecione uma matéria":
        # Caminho dinâmico para o arquivo PDF com base na série e matéria selecionadas
        pdf_file_path = os.path.join(os.getcwd(), "Materiais", serie, materia.lower(), f"{serie}-{materia.upper()}.pdf")

        if os.path.exists(pdf_file_path):
            with open(pdf_file_path, "rb") as pdf_file:
                st.download_button(
                    label=f"📥 Baixar Exercícios Práticos ({serie} - {materia})",
                    data=pdf_file.read(),
                    file_name=f"{serie}-{materia.upper()}.pdf",
                    mime="application/pdf",
                )
        else:
            st.error("O arquivo PDF não foi encontrado. Por favor, verifique o caminho.")
    else:
        st.info("Por favor, selecione a Série e a Matéria para acessar o material.")


if st.session_state.page == "pedagogico_cronograma":
    st.title("Cronograma Pedagógico")
    st.write("Esta página é para o acesso ao cronograma pedagógico.")
    # Adicione aqui o código para o acesso ao cronograma pedagógico
    # Esta seção pode incluir links ou arquivos para download do cronograma pedagógico.

if st.session_state.page == "pedagogico_conteudo":
    st.title("Conteúdo Programático")
    st.write("Esta página é para o acesso ao conteúdo programático.")
    # Adicione aqui o código para o acesso ao conteúdo programático
    # Esta seção pode incluir links ou arquivos para download do conteúdo programático.

if st.session_state.page == "acesso_gestor":
    st.title("Acesso - Gestor")
    st.write("Esta página é para o login do gestor.")
    # Adicione aqui o código para o acesso do gestor
    with st.form("login_gestor_form"):
        username = st.text_input("Usuário", placeholder="Digite seu usuário")
        password = st.text_input("Senha", type="password", placeholder="Digite sua senha")
        
        submitted = st.form_submit_button("Entrar")
        
        if submitted:
            if not username or not password:
                st.error("Por favor, preencha todos os campos obrigatórios.")
            else:
                # Aqui você pode adicionar a lógica de autenticação
                # Exemplo: verificar usuário e senha em um banco de dados
                if username == "gestor" and password == "1234":  # Exemplo de validação simples
                    st.success("Login realizado com sucesso!")
                    st.write(f"Bem-vindo, {username}!")
                else:
                    st.error("Usuário ou senha inválidos.")
    # Esta seção pode incluir informações ou links relevantes para o gestor.

if st.session_state.page == "acesso_professor":
    st.title("Acesso - Professor")
    st.write("Esta página é para o login do professor.")
    # Adicione aqui o código para o acesso do professor
    with st.form("login_professor_form"):
        username = st.text_input("Usuário", placeholder="Digite seu usuário")
        password = st.text_input("Senha", type="password", placeholder="Digite sua senha")
        
        submitted = st.form_submit_button("Entrar")
        
        if submitted:
            if not username or not password:
                st.error("Por favor, preencha todos os campos obrigatórios.")
            else:
                # Aqui você pode adicionar a lógica de autenticação
                # Exemplo: verificar usuário e senha em um banco de dados
                if username == "professor" and password == "1234":  # Exemplo de validação simples
                    st.success("Login realizado com sucesso!")
                    st.write(f"Bem-vindo, {username}!")
                else:
                    st.error("Usuário ou senha inválidos.")
    # Esta seção pode incluir informações ou links relevantes para o professor.

if st.session_state.page == "acesso_aluno":
    st.title("Acesso - Aluno")
    st.write("Esta página é para o login do aluno.")    
    # Adicione aqui o código para o acesso do aluno
    with st.form("login_aluno_form"):
        username = st.text_input("Usuário", placeholder="Digite seu usuário")
        password = st.text_input("Senha", type="password", placeholder="Digite sua senha")
        
        submitted = st.form_submit_button("Entrar")
        
        if submitted:
            if not username or not password:
                st.error("Por favor, preencha todos os campos obrigatórios.")
            else:
                # Aqui você pode adicionar a lógica de autenticação
                # Exemplo: verificar usuário e senha em um banco de dados
                if username == "aluno" and password == "1234":  # Exemplo de validação simples
                    st.success("Login realizado com sucesso!")
                    st.write(f"Bem-vindo, {username}!")
                else:
                    st.error("Usuário ou senha inválidos.")
    # Esta seção pode incluir informações ou links relevantes para o aluno.

if st.session_state.page == "acesso_secretario":
    st.title("Acesso - Secretário")
    st.write("Esta página é para o login do secretário.")
    # Adicione aqui o código para o acesso do secretário
    with st.form("login_secretario_form"):
        username = st.text_input("Usuário", placeholder="Digite seu usuário")
        password = st.text_input("Senha", type="password", placeholder="Digite sua senha")
        
        submitted = st.form_submit_button("Entrar")
        
        if submitted:
            if not username or not password:
                st.error("Por favor, preencha todos os campos obrigatórios.")
            else:
                # Aqui você pode adicionar a lógica de autenticação
                # Exemplo: verificar usuário e senha em um banco de dados
                if username == "secretario" and password == "1234":  # Exemplo de validação simples
                    st.success("Login realizado com sucesso!")
                    st.write(f"Bem-vindo, {username}!")
                else:
                    st.error("Usuário ou senha inválidos.")
    # Esta seção pode incluir informações ou links relevantes para o secretário.

if st.session_state.page == "acesso_prefeito":
    st.title("Acesso - Prefeito")
    st.write("Esta página é para o login do prefeito.")
    # Adicione aqui o código para o acesso do prefeito
    with st.form("login_prefeito_form"):
        username = st.text_input("Usuário", placeholder="Digite seu usuário")
        password = st.text_input("Senha", type="password", placeholder="Digite sua senha")
        
        submitted = st.form_submit_button("Entrar")
        
        if submitted:
            if not username or not password:
                st.error("Por favor, preencha todos os campos obrigatórios.")
            else:
                # Aqui você pode adicionar a lógica de autenticação
                # Exemplo: verificar usuário e senha em um banco de dados
                if username == "prefeito" and password == "1234":
                    st.success("Login realizado com sucesso!")
                    st.write(f"Bem-vindo, {username}!")
                else:
                    st.error("Usuário ou senha inválidos.")
    # Esta seção pode incluir informações ou links relevantes para o prefeito.
