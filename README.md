# Documentação do Wissen

## Introdução

O projeto Wissen é um sistema integrado que combina a classificação de perfis de aprendizagem e um sistema de recomendação educacional, personalizado para estudantes de Física. A personalização visa aumentar o engajamento e a eficácia no aprendizado, utilizando métodos de machine learning e sistemas inteligentes para entender e adaptar-se aos estilos de aprendizagem dos usuários.

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

## Parte de Aprendizado de Máquina

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

## 📝 Sobre o Projeto

#### **3.2.4 Geração de Dados Sintéticos**

Devido à limitação do dataset real (47 amostras), foram geradas amostras sintéticas utilizando um **GAN** (Generative Adversarial Network) para balancear os dados entre os perfis.

---

## **4. Modelagem de Classificação**

Três modelos principais foram utilizados para classificar os perfis:

### **4.1 MLP (Multi-Layer Perceptron)**

#### Configuração:

- **Ativação:** `tanh`
- **Camadas ocultas:** (100,)
- **Otimizador:** `adam`

#### Resultados:

- **Acurácia:** 99,39% com os dados balanceados gerados pelo GAN.

---

### **4.2 DNN (Deep Neural Network)**

#### Configuração:

- **Camadas:**
  - Input layer: Dimensão do dataset normalizado.
  - 2 camadas ocultas com 256 e 128 neurônios.
  - Output layer: Softmax para 4 classes (uma para cada perfil).
- **Função de perda:** `categorical_crossentropy`
- **Otimizador:** `adam`
- **Épocas:** 50
- **Batch size:** 32

#### Resultados:

- A DNN apresentou excelente desempenho em detecção de padrões mais complexos nos dados.

---

### **4.3 ELM (Extreme Learning Machine)**

#### Configuração:

- **Camadas:**
  - Input layer com número de neurônios igual à dimensão dos dados.
  - Hidden layer: 500 neurônios com ativação `relu`.
  - Output layer linear.
- **Treinamento:** Utiliza solução direta da pseudo-inversa para ajustar os pesos.

#### Resultados:

- Modelo altamente eficiente em termos de tempo de treinamento.
- Performa bem em datasets médios, especialmente quando balanceados.

---

## **5. Sistema de Recomendação Educacional**

### **5.1 Estrutura de Dados**

#### Tabelas:

1. **Conteúdos Educacionais**
   - Informações sobre os conteúdos disponíveis e os perfis aos quais são mais adequados.
2. **Perfis de Alunos**
   - Dados dos alunos, incluindo seus perfis de aprendizagem e níveis de conhecimento.
3. **Interações**
   - Registros de interação dos alunos com os conteúdos (ex.: avaliações).

---

### **5.2 Abordagem de Recomendação**

#### **5.2.1 Filtragem Baseada em Conteúdo**

Recomenda conteúdos com base na similaridade entre as tags dos conteúdos e o perfil do aluno.

# Desenvovimento do projeto Wissen na versão Mobile usando o React Native (Parte Mobile)

## 🔧 Pré-requisitos

Certifique-se de ter os seguintes itens instalados em sua máquina:

- Node.js >= 14.17.0
- npm ou yarn

## 🚀 Instalação

```bash
# Clone o repositório
git clone https://github.com/usuario/projeto.git

# Acesse o diretório do projeto
cd projeto

# Instale as dependências
npm install

# Ou instale cada umas dependências separadamente
npm install @react-navigation/native
npm install @react-navigation/native-stack
npx expo install react-native-screens react-native-safe-area-context
npm install @react-navigation/material-top-tabs react-native-tab-view
npx expo install react-native-pager-view
npm install styled-components

# Execute o comando abaixo para evitar conflitos de versões do react e react-dom:
npm install react@18.3.1 react-dom@18.3.1
```

## ⚙️ Rodando o Projeto

Para rodar o projeto execute o comando:

```
npx expo start
```
