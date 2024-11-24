import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

# Perfis e conteúdos
conteudos = pd.DataFrame([
    {'id': 1, 'titulo': 'Apostila de Design Gráfico', 'tags': 'cores iluminação design', 'perfil': 'Visual'},
    {'id': 2, 'titulo': 'Podcast sobre Empatia', 'tags': 'voz emoções histórias', 'perfil': 'Auditivo'},
    {'id': 3, 'titulo': 'Exercícios Físicos Práticos', 'tags': 'movimento tátil ergonomia', 'perfil': 'Cinestésico'},
    {'id': 4, 'titulo': 'Curso de Planilhas Avançadas', 'tags': 'detalhes análise lógica', 'perfil': 'Digital'}
])

interacoes = pd.DataFrame([
    {'usuario_id': 1, 'conteudo_id': 1, 'rating': 5},
    {'usuario_id': 1, 'conteudo_id': 3, 'rating': 3},
    {'usuario_id': 2, 'conteudo_id': 2, 'rating': 4},
    {'usuario_id': 3, 'conteudo_id': 4, 'rating': 5}
])

# 1. Filtragem Baseada em Conteúdo
def recomendar_por_conteudo(usuario_id, perfil_usuario):
    # Seleciona conteúdos do mesmo perfil
    conteudos_filtrados = conteudos[conteudos['perfil'] == perfil_usuario]
    
    # Gera matriz de similaridade
    count_vectorizer = CountVectorizer()
    tags_matrix = count_vectorizer.fit_transform(conteudos_filtrados['tags'])
    similaridades = cosine_similarity(tags_matrix, tags_matrix)
    
    # Recomenda conteúdos baseados na similaridade
    recomendacoes = conteudos_filtrados.iloc[similaridades.sum(axis=0).argsort()[::-1]]
    return recomendacoes[['id', 'titulo']]

# 2. Filtragem Colaborativa
def recomendar_por_colaboracao(usuario_id):
    # Cria matriz de usuário-conteúdo
    matriz_interacao = pd.pivot_table(interacoes, index='usuario_id', columns='conteudo_id', values='rating').fillna(0)
    
    # Similaridade entre usuários
    similaridade_usuarios = cosine_similarity(matriz_interacao)
    
    # Obtém usuários similares
    similaridades_usuario = similaridade_usuarios[usuario_id - 1]
    
    # Recomenda conteúdos com base na média ponderada
    recomendacoes = matriz_interacao.T.dot(similaridades_usuario).sort_values(ascending=False)
    return recomendacoes.index

# 3. Recomendação Híbrida
def sistema_hibrido(usuario_id, perfil_usuario):
    # Combina recomendações
    conteudos_por_conteudo = recomendar_por_conteudo(usuario_id, perfil_usuario)
    conteudos_por_colaboracao = recomendar_por_colaboracao(usuario_id)
    
    # Combina resultados
    recomendacoes_finais = pd.concat([
        conteudos[conteudos['id'].isin(conteudos_por_conteudo['id'])],
        conteudos[conteudos['id'].isin(conteudos_por_colaboracao)]
    ]).drop_duplicates()
    
    return recomendacoes_finais[['id', 'titulo']]

# Usuário exemplo
perfil_usuario = 'Visual'  # Obtido pela classificação
usuario_id = 1  # ID do usuário

# Exibe recomendações
recomendacoes = sistema_hibrido(usuario_id, perfil_usuario)
print("Recomendações para o usuário:\n", recomendacoes)
