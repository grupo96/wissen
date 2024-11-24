# wissen

### Estrutura de Diretórios e Funcionamento

1. **Frontend (React)**:

   - Diretório: `/frontend`
   - **Descrição**: Armazena o código do React e a estrutura da interface do usuário.
   - **Importante**: Divida componentes em subpastas organizadas (`/components`, `/pages`, `/assets` para imagens ou estilos).
   - **Exemplo de estrutura**:
     ```
     /frontend
     ├── public/
     ├── src/
     │   ├── components/
     │   ├── pages/
     │   ├── assets/
     │   └── index.js
     └── package.json
     ```
2. **Backend (Django)**:

   - Diretório: `/backend`
   - **Descrição**: Contém o código principal do Django (APIs, autenticação, e lógica de negócios).
   - **Importante**: Organize os apps específicos dentro do Django em `/apps`, mantendo arquivos de configuração e gerenciadores de rotas separados.
   - **Exemplo de estrutura**:
     ```
     /backend
     ├── apps/
     │   ├── core/           # App principal
     │   ├── users/          # Gestão de usuários e autenticação
     ├── settings/           # Configurações do Django
     └── manage.py
     ```
3. **Machine Learning (ML)**:

   - Diretório: `/machine_learning`
   - **Descrição**: Contém os scripts, notebooks e modelos para aprendizado de máquina, com subdiretórios para organização dos dados e modelos.
   - **Importante**: Separe datasets, scripts de pré-processamento, e notebooks de análise para facilitar manutenção e atualizações.
   - **Exemplo de estrutura**:
     ```
     /machine_learning
     ├── models/
     ├── notebooks/
     └── preprocessing/
     ```

### Fluxo de Commits e Importância de Commits Estruturados

1. **Não Commitar Diretamente na `main`**:

   - **Motivo**: A `main` deve sempre conter o código mais estável e pronto para deploy. Commits diretos podem introduzir bugs.
   - **Como Proceder**:
     - Crie branches para cada nova feature, correção ou atualização (`feature/nome-da-feature`, `fix/descricao-do-bug`).
     - Realize testes antes de pedir uma revisão e aprovação para merge na `main`.
2. **Instruções de Commit**:

   - **Mensagens de Commit**: Use mensagens descritivas e objetivas (`"Adiciona página de login"`, `"Corrige erro de autenticação"`).
   - **Push e Pull Requests**:
     - Faça `push` para a branch que criou e sempre abra uma Pull Request (PR) para que o código seja revisado antes do merge.
     - Atribua revisores na PR e documente o que foi feito para facilitar a avaliação.


### **Documentação do Projeto: Classificação de Perfis de Aprendizagem e Sistema de Recomendação Educacional para Ensino de Física**

---

## **1. Introdução**

Este projeto integra dois componentes principais:

1. **Classificação de perfis de aprendizagem** : Determina o perfil de um aluno (Visual, Auditivo, Cinestésico ou Digital) com base em suas respostas a um questionário.
2. **Sistema de Recomendação Educacional** : Sugere conteúdos específicos de física adaptados ao perfil de aprendizagem de cada aluno, utilizando uma abordagem híbrida (filtragem baseada em conteúdo e colaborativa).

Objetivo principal: **Personalizar o ensino de física** com base nas preferências e estilos de aprendizagem dos alunos, aumentando o engajamento e a eficácia do aprendizado.

---

## **2. Etapa 1: Classificação dos Perfis de Aprendizagem**

### **2.1 Coleta e Pré-processamento dos Dados**

Os dados são coletados por meio de um questionário onde os alunos reordenam alternativas de acordo com suas preferências. Cada alternativa está associada a um perfil de aprendizagem.

* **Estrutura do dataset** :
* Perguntas: 5 colunas representando as questões do questionário.
* Respostas: Ordenadas pelos alunos de mais para menos preferidas.
* Perfis: Classificados como Visual, Auditivo, Cinestésico ou Digital.

### **2.2 Classificação do Perfil**

O perfil de aprendizagem de cada aluno é calculado somando pontos atribuídos a cada alternativa com base em sua posição. A lógica é implementada da seguinte forma:

```python
def calcular_perfil(row):
    contagem_perfis = {"Visual": 0, "Cinestésico": 0, "Auditivo": 0, "Digital": 0}
    for resposta in row:
        alternativas = resposta.split(';')
        for idx, alternativa in enumerate(alternativas):
            perfil = alternativas_perfil.get(alternativa.strip())
            if perfil:
                pontuacao = 4 - idx  # Pontuação inversamente proporcional à posição
                contagem_perfis[perfil] += pontuacao
    return max(contagem_perfis, key=contagem_perfis.get)
```

---

## **3. Etapa 2: Sistema de Recomendação Educacional**

### **3.1 Estrutura da Base de Dados**

Três datasets principais foram criados para suportar o sistema de recomendação:

1. **Conteúdos Educacionais** :
   Inclui o título, tags associadas (conceitos ou tipos de conteúdo) e o perfil mais adequado para o conteúdo.| id | título                         | tags                           | perfil       |
   | -- | ------------------------------- | ------------------------------ | ------------ |
   | 1  | Vídeo: Leis de Newton          | movimento, forças, animação | Visual       |
   | 2  | Podcast: História da Gravidade | história, conceitos, áudio   | Auditivo     |
   | 3  | Experimento: Plano Inclinado    | experimento, prática          | Cinestésico |
2. **Perfis de Alunos** :
   Contém o nome do aluno, o perfil de aprendizagem identificado e seu nível de conhecimento.| id | nome  | perfil       | nível         |
   | -- | ----- | ------------ | -------------- |
   | 1  | João | Visual       | Iniciante      |
   | 2  | Maria | Cinestésico | Intermediário |
3. **Interações** :
   Registra as interações de cada aluno com os conteúdos.| aluno_id | conteudo_id | rating |
   | -------- | ----------- | ------ |
   | 1        | 1           | 5      |
   | 2        | 3           | 4      |

---

### **3.2 Abordagens de Recomendação**

#### **Filtragem Baseada em Conteúdo**

Recomenda conteúdos com base no perfil do aluno e na similaridade entre as tags dos conteúdos.

```python
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def recomendar_conteudos_por_conteudo(perfil_aluno):
    conteudos_filtrados = conteudos_fisica[conteudos_fisica['perfil'] == perfil_aluno]
    tags_matrix = CountVectorizer().fit_transform(conteudos_filtrados['tags'])
    similaridades = cosine_similarity(tags_matrix, tags_matrix)
    recomendacoes = conteudos_filtrados.iloc[similaridades.sum(axis=0).argsort()[::-1]]
    return recomendacoes[['id', 'titulo']]
```

---

#### **Filtragem Colaborativa**

Recomenda conteúdos com base em interações de outros alunos com perfis semelhantes.

```python
from sklearn.metrics.pairwise import cosine_similarity

def recomendar_conteudos_por_colaboracao(aluno_id):
    matriz_interacao = pd.pivot_table(interacoes, index='aluno_id', columns='conteudo_id', values='rating').fillna(0)
    similaridade_alunos = cosine_similarity(matriz_interacao)
    similaridades_aluno = similaridade_alunos[aluno_id - 1]
    recomendacoes = matriz_interacao.T.dot(similaridades_aluno).sort_values(ascending=False)
    return recomendacoes.index
```

---

#### **Sistema Híbrido**

Combina os resultados das duas abordagens para gerar recomendações mais completas.

```python
def sistema_recomendacao_hibrido(aluno_id, perfil_aluno):
    conteudos_baseado_em_conteudo = recomendar_conteudos_por_conteudo(perfil_aluno)
    conteudos_colaborativo = recomendar_conteudos_por_colaboracao(aluno_id)
    recomendacoes_finais = pd.concat([
        conteudos_fisica[conteudos_fisica['id'].isin(conteudos_baseado_em_conteudo['id'])],
        conteudos_fisica[conteudos_fisica['id'].isin(conteudos_colaborativo)]
    ]).drop_duplicates()
    return recomendacoes_finais[['id', 'titulo']]
```

---

### **3.3 Exemplo de Recomendação**

Exemplo de execução para um aluno com perfil  **Visual** :

```python
aluno_id = 1
perfil_aluno = alunos.loc[alunos['id'] == aluno_id, 'perfil'].values[0]
recomendacoes = sistema_recomendacao_hibrido(aluno_id, perfil_aluno)
print(f"Recomendações para o aluno {alunos.loc[alunos['id'] == aluno_id, 'nome'].values[0]}:\n", recomendacoes)
```

Saída:

```
Recomendações para o aluno João:
    id                          título
0   1         Vídeo: Leis de Newton
4   4  Simulação: Circuitos Elétricos
```

---

## **4. Resultados Esperados**

* **Personalização** : Recomendações alinhadas ao estilo de aprendizagem do aluno.
* **Aumento de Engajamento** : Alunos mais motivados a explorar conteúdos adaptados.
* **Facilidade de Expansão** : O sistema pode ser facilmente ajustado para outros tópicos de ensino.

---

## **5. Possibilidades Futuras**

1. **Adição de Gamificação** :

* Adicionar desafios ou premiações com base nos conteúdos consumidos.

1. **Integração com Redes Neurais** :

* Utilizar redes neurais para melhorar a filtragem colaborativa.

1. **Expansão para Outras Disciplinas** :

* Ajustar para diferentes áreas do conhecimento.
