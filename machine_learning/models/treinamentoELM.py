from hpelm import ELM
from sklearn.preprocessing import OneHotEncoder, StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from imblearn.over_sampling import SMOTE
import numpy as np
import pandas as pd
import unidecode
# Carregar o arquivo .ods
output_directoryCSV = "./dados_ampliados_textuais_combinados.ods" 
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

# Pré-processamento (mantendo o mesmo fluxo do código anterior)
encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
scaler = StandardScaler()

X_encoded = encoder.fit_transform(X.select_dtypes(include=['object']))
X_transformed = scaler.fit_transform(np.concatenate([X.select_dtypes(exclude=['object']).values, X_encoded], axis=1))

# Balanceamento com SMOTE
smote = SMOTE(k_neighbors=1)
X_resampled, y_resampled = smote.fit_resample(X_transformed, y)

# Divisão dos dados
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

# Inicializando o ELM
input_dim = X_train.shape[1]  # Número de atributos de entrada
output_dim = len(np.unique(y))  # Número de classes
elm = ELM(input_dim, output_dim, classification="c", w=None)

# Codificar rótulos em formato one-hot
# Codificar rótulos em formato one-hot
y_train_encoded = encoder.fit_transform(y_train.to_numpy().reshape(-1, 1))
y_test_encoded = encoder.transform(y_test.to_numpy().reshape(-1, 1))



# Adicionar neurônios à camada oculta
num_neurons = 100  # Você pode ajustar esse número
elm.add_neurons(num_neurons, "sigm")  # Função de ativação sigmoide

# Treinar o modelo
elm.train(X_train, y_train_encoded, "c")

# Fazer previsões
y_pred = elm.predict(X_test)
y_pred_labels = np.argmax(y_pred, axis=1)  # Converter probabilidades para classes

# Avaliação
print("Acurácia:", accuracy_score(y_test, y_pred_labels))
print("Relatório de Classificação:\n", classification_report(y_test, y_pred_labels))
