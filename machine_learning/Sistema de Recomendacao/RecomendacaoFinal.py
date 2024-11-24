import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Mock dos dados
# Perfil do aluno com tags relacionadas
aluno_perfil = {
    "id": 1,
    "nome": "Aluno Exemplo",
    "tags": "física cinestésico energia trabalho experimentos"
}

# Base de conteúdos (exemplo fictício)
conteudos = pd.DataFrame([
    {"id": 1, "titulo": "Introdução à Energia", "tags": "física energia trabalho calor"},
    {"id": 2, "titulo": "Simulação de Experimentos", "tags": "experimentos cinestésico física prática"},
    {"id": 3, "titulo": "História da Física Moderna", "tags": "física história teoria"},
    {"id": 4, "titulo": "Dinâmica e Movimento", "tags": "cinemática cinestésico movimento força"},
    {"id": 5, "titulo": "A Matemática na Física", "tags": "matemática física teoria cálculo"},
])

# Vetorização das tags
vectorizer = TfidfVectorizer()
tags_corpus = conteudos['tags'].tolist() + [aluno_perfil['tags']]
tfidf_matrix = vectorizer.fit_transform(tags_corpus)

# Calcula similaridade de cosseno
similaridade = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

# Adiciona os valores de similaridade à base de conteúdos
conteudos['similaridade'] = similaridade.flatten()

# Ordena os conteúdos pela similaridade (maior para menor)
conteudos_recomendados = conteudos.sort_values(by='similaridade', ascending=False)

# Mostra os conteúdos recomendados
print("Conteúdos recomendados para o aluno:")
print(conteudos_recomendados[['titulo', 'tags', 'similaridade']])
