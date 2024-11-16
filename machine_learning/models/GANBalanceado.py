import pandas as pd
import re
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers # type: ignore
from sklearn.preprocessing import LabelEncoder

# Função para remover acentos
def remover_acentos(texto):
    texto = re.sub(r'[áàãâä]', 'a', texto)
    texto = re.sub(r'[éèêë]', 'e', texto)
    texto = re.sub(r'[íìîï]', 'i', texto)
    texto = re.sub(r'[óòõôö]', 'o', texto)
    texto = re.sub(r'[úùûü]', 'u', texto)
    texto = re.sub(r'[ç]', 'c', texto)
    texto = re.sub(r'[ñ]', 'n', texto)
    return texto

# Carregar o arquivo .ods
file_path = 'Descubra seu estilo de aprendizagem.ods'
data = pd.read_excel(file_path, engine='odf')

# Padronizar os nomes das colunas
data.columns = [remover_acentos(col).replace(" ", "_").lower().rstrip(":") for col in data.columns]

# Selecionar colunas relevantes
colunas_respostas = [
    'como_eu_tomo_decisoes_importantes_na_minha_vida', 
    'tenho_facilidade_quando', 
    'o_que_eu_percebo_primeiro_em_um_ambiente_novo', 
    'se_vou_a_um_supermercado...', 
    'se_eu_for_passar_ferias_em_uma_ilha_deserta_com_certeza_terei_comigo'
]
data_respostas = data[colunas_respostas]

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

# Função para calcular o perfil
def calcular_perfil(row):
    contagem_perfis = {"Visual": 0, "Cinestésico": 0, "Auditivo": 0, "Digital": 0}
    for resposta in row:
        alternativas = resposta.split(';')
        for idx, alternativa in enumerate(alternativas):
            perfil = alternativas_perfil.get(alternativa.strip())
            if perfil:
                pontuacao = 4 - idx
                contagem_perfis[perfil] += pontuacao
    return max(contagem_perfis, key=contagem_perfis.get)

# Adicionar coluna de perfil
data['perfil'] = data[colunas_respostas].apply(calcular_perfil, axis=1)

# Contar a quantidade de perfis
contagem_perfis = data['perfil'].value_counts().to_dict()
perfil_menos_representado = min(contagem_perfis, key=contagem_perfis.get)

# Codificar respostas em números
label_encoders = {}
for coluna in colunas_respostas:
    le = LabelEncoder()
    data_respostas[coluna] = le.fit_transform(data_respostas[coluna].astype(str))
    label_encoders[coluna] = le

# Normalizar os dados
data_normalizada = (data_respostas - data_respostas.min()) / (data_respostas.max() - data_respostas.min())
data_normalizada = data_normalizada.fillna(0).values

# Configuração do GAN
def criar_gan(input_dim, latent_dim):
    gerador = tf.keras.Sequential([
        layers.Dense(128, activation='relu', input_dim=latent_dim),
        layers.BatchNormalization(),
        layers.Dense(256, activation='relu'),
        layers.BatchNormalization(),
        layers.Dense(input_dim, activation='tanh')
    ])
    discriminador = tf.keras.Sequential([
        layers.Dense(256, activation='relu', input_dim=input_dim),
        layers.Dropout(0.3),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(1, activation='sigmoid')
    ])
    discriminador.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    discriminador.trainable = False
    gan = tf.keras.Sequential([gerador, discriminador])
    gan.compile(optimizer='adam', loss='binary_crossentropy')
    return gerador, discriminador, gan

# Dimensões
input_dim = data_normalizada.shape[1]
latent_dim = 100

# Criar o GAN
gerador, discriminador, gan = criar_gan(input_dim, latent_dim)

# Função para treinar o GAN
def treinar_gan(gerador, discriminador, gan, dados_reais, epochs, batch_size, perfil_alvo=None):
    for epoch in range(epochs):
        # Criar amostras reais
        idx = np.random.randint(0, dados_reais.shape[0], batch_size)
        amostras_reais = dados_reais[idx]

        # Criar amostras falsas
        ruido = np.random.normal(0, 1, (batch_size, latent_dim))
        amostras_falsas = gerador.predict(ruido)

        # Rótulos
        rótulos_reais = np.ones((batch_size, 1))
        rótulos_falsos = np.zeros((batch_size, 1))

        # Treinar o discriminador
        d_loss_real = discriminador.train_on_batch(amostras_reais, rótulos_reais)
        d_loss_fake = discriminador.train_on_batch(amostras_falsas, rótulos_falsos)

        # Treinar o gerador
        ruido = np.random.normal(0, 1, (batch_size, latent_dim))
        g_loss = gan.train_on_batch(ruido, np.ones((batch_size, 1)))

        # Progresso
        if epoch % 100 == 0:
            print(f"Epoch {epoch}/{epochs} | D Loss: {d_loss_real[0]}, G Loss: {g_loss}")

# Treinar o GAN com foco no perfil menos representado
#treinar_gan(gerador, discriminador, gan, data_normalizada, epochs=200, batch_size=32)

# Gerar novas amostras para o perfil menos representado

num_amostras = 1000
ruido = np.random.normal(0, 1, (num_amostras, latent_dim))
amostras_sinteticas = gerador.predict(ruido)

# Denormalizar e converter para alternativas textuais
def denormalizar_e_converter(dados_sinteticos, label_encoders, data_respostas):
    dados_denormalizados = dados_sinteticos.copy()
    for i, coluna in enumerate(data_respostas.columns):
        dados_denormalizados[:, i] = (
            dados_denormalizados[:, i] * (data_respostas[coluna].max() - data_respostas[coluna].min())
            + data_respostas[coluna].min()
        )
        dados_denormalizados[:, i] = np.clip(dados_denormalizados[:, i], data_respostas[coluna].min(), data_respostas[coluna].max())
    dados_textuais = pd.DataFrame(dados_denormalizados, columns=data_respostas.columns)
    for coluna in dados_textuais.columns:
        le = label_encoders[coluna]
        dados_textuais[coluna] = le.inverse_transform(dados_textuais[coluna].astype(int))
    return dados_textuais

# Função para treinar o GAN por perfil
def treinar_gan_por_perfil(gerador, discriminador, gan, dados_reais, epochs, batch_size, perfil_alvo, data):
    print(f"Treinando GAN para o perfil: {perfil_alvo}")
    # Filtrar dados do perfil específico
    idx_perfil = data[data['perfil'] == perfil_alvo].index
    dados_perfil = dados_reais[idx_perfil]

    for epoch in range(epochs):
        # Criar amostras reais
        idx = np.random.randint(0, dados_perfil.shape[0], batch_size)
        amostras_reais = dados_perfil[idx]

        # Criar amostras falsas
        ruido = np.random.normal(0, 1, (batch_size, latent_dim))
        amostras_falsas = gerador.predict(ruido)

        # Rótulos
        rótulos_reais = np.ones((batch_size, 1))
        rótulos_falsos = np.zeros((batch_size, 1))

        # Treinar o discriminador
        d_loss_real = discriminador.train_on_batch(amostras_reais, rótulos_reais)
        d_loss_fake = discriminador.train_on_batch(amostras_falsas, rótulos_falsos)

        # Treinar o gerador
        ruido = np.random.normal(0, 1, (batch_size, latent_dim))
        g_loss = gan.train_on_batch(ruido, np.ones((batch_size, 1)))

        # Progresso
        if epoch % 100 == 0:
            print(f"Perfil: {perfil_alvo} | Epoch {epoch}/{epochs} | D Loss: {d_loss_real[0]}, G Loss: {g_loss}")

# Gerar dados balanceados
def gerar_dados_balanceados(gerador, discriminador, gan, data, data_normalizada, label_encoders, num_amostras_por_perfil, epochs, batch_size):
    perfis_unicos = data['perfil'].unique()
    amostras_sinteticas_totais = []

    for perfil in perfis_unicos:
        # Treinar o GAN para o perfil atual
        treinar_gan_por_perfil(gerador, discriminador, gan, data_normalizada, epochs, batch_size, perfil, data)

        # Gerar amostras para o perfil atual
        ruido = np.random.normal(0, 1, (num_amostras_por_perfil, latent_dim))
        amostras_sinteticas = gerador.predict(ruido)
        amostras_sinteticas_totais.append((perfil, amostras_sinteticas))

    return amostras_sinteticas_totais

# Gerar amostras balanceadas
num_amostras_por_perfil = 1000  # Quantidade de amostras por perfil
epochs = 200
batch_size = 32

# Gera dados balanceados por perfil
dados_balanceados = gerar_dados_balanceados(gerador, discriminador, gan, data, data_normalizada, label_encoders, num_amostras_por_perfil, epochs, batch_size)

# Processar e denormalizar as amostras geradas
dados_sinteticos_balanceados = []
for perfil, amostras in dados_balanceados:
    df_denormalizado = denormalizar_e_converter(amostras, label_encoders, data_respostas)
    df_denormalizado['perfil'] = perfil  # Adicionar o rótulo do perfil
    dados_sinteticos_balanceados.append(df_denormalizado)

df_sintetico_textual = denormalizar_e_converter(amostras_sinteticas, label_encoders, data_respostas)

# Concatenar e salvar os dados
df_completo_textual = pd.concat([data[colunas_respostas], df_sintetico_textual], ignore_index=True)
df_completo_textual.to_excel("dados_balanceados_textuais.ods", engine="odf", index=False)
print("Dados balanceados gerados e salvos em 'dados_balanceados_textuais.ods'.")
