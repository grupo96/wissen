import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV
from sklearn.linear_model import LogisticRegression
from category_encoders import TargetEncoder
from sklearn.metrics import accuracy_score, classification_report
from imblearn.over_sampling import SMOTE
import unidecode
import numpy as np
import matplotlib.pyplot as plt

# Carregar o arquivo .ods
file_path = 'dados_ampliados_textuais_combinados.ods'
data = pd.read_excel(file_path, engine='odf')

# Remover acentos, substituir espaços por underscore, converter para minúsculas e remover ':' no final das colunas
data.columns = [unidecode.unidecode(col).replace(" ", "_").lower().rstrip(":") for col in data.columns]

# Selecionar as colunas de respostas
colunas_respostas = [
    'como_eu_tomo_decisoes_importantes_na_minha_vida', 
    'tenho_facilidade_quando', 
    'o_que_eu_percebo_primeiro_em_um_ambiente_novo', 
    'se_vou_a_um_supermercado...', 
    'se_eu_for_passar_ferias_em_uma_ilha_deserta_com_certeza_terei_comigo'
]

# Mapeamento de alternativas para os perfis
alternativas_perfil = {
    "Após ouvir várias ideias, sigo a que me soou melhor.": "Auditivo",
    "Somente tomo a decisão após analisar o assunto em detalhes.": "Digital",
    "Sempre sigo minha intuição e meus instintos.": "Cinestésico",
    "Procuro seguir pelo caminho que me parece melhor.": "Visual",
    "Vou falar de assuntos importantes ressaltando o que é importante.": "Digital",
    "Vou mexer no aplicativo de áudio ou música.": "Auditivo",
    "Vou escolher materiais confortáveis ou ergonômicos.": "Cinestésico",
    "Vou trabalhar com cores. Sei combinar bem as cores": "Visual",
    "A disposição dos móveis e seus formatos.": "Digital",
    "A textura das superfícies.": "Cinestésico",
    "As combinações de cores e intensidade da iluminação.": "Visual",
    "O som ambiente, o barulho dos equipamentos e as vozes ao redor.": "Auditivo",
    "Gosto de perguntar a opinião das pessoas sobre algum produto.": "Auditivo",
    "Procuro pegar no produto, sentir o peso, sentir sua forma.": "Cinestésico",
    "Sempre pego primeiro aqueles que me chamam mais a atenção.": "Visual",
    "Leio os rótulos, vejo as especificações, data de validade.": "Digital",
    "Uma rede de dormir confortável e um bom chinelo.": "Cinestésico",
    "Um binóculo e um óculos de sol.": "Visual",
    "Um MP3 com minhas músicas preferidas.": "Auditivo",
    "Uma bússola e um mapa.": "Digital"
}

def calcular_perfil(row):
    contagem_perfis = {"Visual": 0, "Cinestésico": 0, "Auditivo": 0, "Digital": 0}
    
    for resposta in row:
        alternativas = resposta.split(';')
        
        for idx, alternativa in enumerate(alternativas):
            perfil = alternativas_perfil.get(alternativa.strip())
            if perfil:
                pontuacao = 4 - idx
                contagem_perfis[perfil] += pontuacao

    # Multiplica cada total por 2
    for perfil in contagem_perfis:
        contagem_perfis[perfil] *= 2

    perfil_final = max(contagem_perfis, key=contagem_perfis.get)
    return perfil_final

# Aplicar a função para calcular o perfil em cada linha
data['perfil'] = data[colunas_respostas].apply(calcular_perfil, axis=1)
print("Dataset com coluna de perfil:\n", data[['perfil']])

# Codificar o perfil para o modelo
label_encoder = LabelEncoder()
data['perfil_encoded'] = label_encoder.fit_transform(data['perfil'])

# Manter apenas as colunas relevantes para o modelo
X = data[colunas_respostas]
y = data['perfil_encoded']

# Dividir em conjuntos de treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Inicializar o TargetEncoder e o StandardScaler
encoder = TargetEncoder()
scaler = StandardScaler()

# Aplicar o encoder e o escalador aos dados de treino
X_train_encoded = encoder.fit_transform(X_train, y_train)
X_train_encoded_scaled = scaler.fit_transform(X_train_encoded)

# Transformar o conjunto de teste
X_test_encoded = encoder.transform(X_test)
X_test_encoded_scaled = scaler.transform(X_test_encoded)

# Aplicar o SMOTE para lidar com o desbalanceamento
smote = SMOTE(k_neighbors=1)
X_resampled, y_resampled = smote.fit_resample(X_train_encoded_scaled, y_train)

# Definir a grade de hiperparâmetros para LogisticRegression
param_grid = {
    'C': [0.01, 0.1, 1, 10],
    'solver': ['lbfgs', 'liblinear'],
    'class_weight': ['balanced', None]
}

# Inicializar o modelo LogisticRegression
logistic = LogisticRegression(max_iter=1000)

# Configurar o GridSearchCV com StratifiedKFold
kf = StratifiedKFold(n_splits=5)
grid_search = GridSearchCV(estimator=logistic, param_grid=param_grid, scoring='accuracy', cv=kf, n_jobs=-1)
grid_search.fit(X_resampled, y_resampled)

# Treinar o melhor modelo encontrado
best_model = grid_search.best_estimator_
best_model.fit(X_resampled, y_resampled)

# Fazer previsões e avaliar o modelo
y_pred = best_model.predict(X_test_encoded_scaled)
print("Acurácia:", accuracy_score(y_test, y_pred))

# Gerar o relatório de classificação incluindo todas as classes
print("Relatório de Classificação:\n", classification_report(
    y_test, y_pred, target_names=label_encoder.classes_, labels=np.unique(y_test)
))

# Contagem dos perfis para gráfico de pizza
perfil_counts = data['perfil'].value_counts()
labels = perfil_counts.index
sizes = perfil_counts.values

# Plotar gráfico de pizza
plt.figure(figsize=(8, 8))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
plt.title('Distribuição de Perfis de Aprendizagem')
plt.show()

print("Melhores Hiperparâmetros:", grid_search.best_params_)
