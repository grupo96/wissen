from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.layers import Dense, Dropout # type: ignore
from tensorflow.keras.utils import to_categorical # type: ignore
from sklearn.preprocessing import OneHotEncoder, StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from imblearn.over_sampling import SMOTE
import numpy as np
import pandas as pd
import unidecode

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

# Codificar o perfil para o modelo
label_encoder = LabelEncoder()
data['perfil_encoded'] = label_encoder.fit_transform(data['perfil'])

# Manter apenas as colunas relevantes para o modelo
X = data[colunas_respostas]
y = data['perfil_encoded']

# Dividir em conjuntos de treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Pré-processamento (codificação e normalização)
encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
scaler = StandardScaler()

X_encoded = encoder.fit_transform(X.select_dtypes(include=['object']))
X_transformed = scaler.fit_transform(np.concatenate([X.select_dtypes(exclude=['object']).values, X_encoded], axis=1))

# Balanceamento com SMOTE
smote = SMOTE(k_neighbors=1)
X_resampled, y_resampled = smote.fit_resample(X_transformed, y)

# Dividir em conjuntos de treino e teste novamente
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

# Codificar rótulos como one-hot para o modelo DNN
y_train_encoded = to_categorical(y_train)
y_test_encoded = to_categorical(y_test)

# Construir o modelo DNN
model = Sequential([
    Dense(128, input_dim=X_train.shape[1], activation='relu'),
    Dropout(0.2),
    Dense(64, activation='relu'),
    Dropout(0.2),
    Dense(y_train_encoded.shape[1], activation='softmax')  # Saída para classificação multi-classe
])

# Compilar o modelo
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Treinar o modelo
model.fit(X_train, y_train_encoded, epochs=50, batch_size=32, validation_split=0.2, verbose=1)

# Avaliar o modelo
loss, accuracy = model.evaluate(X_test, y_test_encoded, verbose=0)
y_pred = np.argmax(model.predict(X_test), axis=1)

print(f"Acurácia: {accuracy * 100:.2f}%")
print("Relatório de Classificação:\n", classification_report(y_test, y_pred))
model.save('modelo_dnn_otimizado.h5')
