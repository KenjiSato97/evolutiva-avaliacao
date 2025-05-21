import pandas as pd

def create_dataframes():
    """
    Cria e retorna os dataframes necessários para o sistema de avaliação escolar:
    - df_aluno: Informações dos alunos
    - df_escola: Cadastro de escolas
    - df_prova: Registros de provas realizadas pelos alunos
    - df_gabarito: Gabaritos das provas por série/matéria
    """
    
    # Criação do df_escola
    escolas = [
        {"id_escola": 1, "nomeEscola": "Escola Municipal Paulo Freire", 
         "endereco": "Rua das Flores, 123", "telefone": "(11) 3456-7890", "email": "paulofreire@edu.com"},
        {"id_escola": 2, "nomeEscola": "Colégio Estadual Machado de Assis", 
         "endereco": "Av. Principal, 456", "telefone": "(11) 2345-6789", "email": "machadodeassis@edu.com"}
    ]
    df_escola = pd.DataFrame(escolas)
    
    # Criação do df_aluno vazio
    df_aluno = pd.DataFrame(columns=[
        "id_aluno", "nomeAluno", "dataNascimento", "genero", 
        "serie", "nomeEscola", "localizacaoEscola", "laudoMedico"
    ])
    
    # Criação do df_prova vazio
    df_prova = pd.DataFrame(columns=[
        "id_prova", "id_aluno", "nomeAluno", "materia", "serie", 
        "questao_1", "questao_2", "questao_3", "questao_4", "questao_5", 
        "questao_6", "questao_7", "questao_8", "questao_9", "questao_10"
    ])
    
    # Criação do df_gabarito vazio
    df_gabarito = pd.DataFrame(columns=[
        "id_gabarito", "serie", "materia", 
        "questao_1", "questao_2", "questao_3", "questao_4", "questao_5", 
        "questao_6", "questao_7", "questao_8", "questao_9", "questao_10"
    ])
    df_aluno['id_aluno'] = df_aluno['id_aluno'].astype(int)
    
    return {
        'df_aluno': df_aluno,
        'df_escola': df_escola,
        'df_prova': df_prova,
        'df_gabarito': df_gabarito
    }

def load_or_create_dataframes():
    """
    Tenta carregar os dataframes de arquivos existentes,
    se não existirem, cria novos dataframes.
    """
    try:
        df_aluno = pd.read_parquet('data/df_aluno.parquet')
        df_escola = pd.read_parquet('data/df_escola.parquet')
        df_prova = pd.read_parquet('data/df_prova.parquet')
        df_gabarito = pd.read_parquet('data/df_gabarito.parquet')
        
        return {
            'df_aluno': df_aluno,
            'df_escola': df_escola,
            'df_prova': df_prova,
            'df_gabarito': df_gabarito
        }
    
    except (FileNotFoundError, Exception):
        # Se os arquivos não existirem, cria novos dataframes
        dataframes = create_dataframes()
        # Salva os dataframes
        save_dataframes(dataframes)
        return dataframes

def save_dataframes(dataframes):
    """
    Salva os dataframes em arquivos parquet para uso futuro.
    
    Args:
        dataframes (dict): Dicionário contendo os dataframes
    """
    import os
    
    # Criar pasta data se não existir
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Salvar cada dataframe
    for name, df in dataframes.items():
        df.to_parquet(f'data/{name}.parquet')
    
    print("Dataframes salvos com sucesso!")

def calcular_desempenho(df_prova, df_gabarito):
    """
    Calcula o desempenho dos alunos com base nas respostas e gabaritos
    
    Args:
        df_prova: DataFrame com as respostas dos alunos
        df_gabarito: DataFrame com as respostas corretas
        
    Returns:
        DataFrame com os resultados calculados
    """
    # Criar dataframe para armazenar os resultados
    resultados = []
    
    # Iterar sobre as provas
    for _, prova in df_prova.iterrows():
        # Encontrar o gabarito correspondente
        gabarito = df_gabarito[(df_gabarito['serie'] == prova['serie']) & 
                              (df_gabarito['materia'] == prova['materia'])]
        
        if len(gabarito) == 0:
            continue
            
        gabarito = gabarito.iloc[0]
        
        # Calcular acertos
        acertos = 0
        total_questoes = 0
        
        for i in range(1, 11):
            coluna_questao = f'questao_{i}'
            if coluna_questao in prova and coluna_questao in gabarito:
                total_questoes += 1
                if prova[coluna_questao] == gabarito[coluna_questao]:
                    acertos += 1
        
        # Calcular a nota (0 a 10)
        if total_questoes > 0:
            nota = (acertos / total_questoes) * 10
        else:
            nota = 0
            
        # Adicionar aos resultados
        resultado = {
            'id_prova': prova['id_prova'],
            'id_aluno': prova['id_aluno'],
            'nomeAluno': prova['nomeAluno'],
            'materia': prova['materia'],
            'serie': prova['serie'],
            'acertos': acertos,
            'total_questoes': total_questoes,
            'nota': nota
        }
        resultados.append(resultado)
    
    return pd.DataFrame(resultados)