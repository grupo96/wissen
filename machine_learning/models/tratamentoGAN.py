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

# Codificar respostas textuais em números
label_encoders = {}
for coluna in colunas_respostas:
    le = LabelEncoder()
    data_respostas[coluna] = le.fit_transform(data_respostas[coluna].astype(str))
    label_encoders[coluna] = le

# Normalizar os dados para o intervalo [0, 1]
data_normalizada = (data_respostas - data_respostas.min()) / (data_respostas.max() - data_respostas.min())
data_normalizada = data_normalizada.fillna(0).values

# Exibir uma amostra para verificar
print(data_normalizada[:5])

# Configuração inicial do GAN
def criar_gan(input_dim, latent_dim):
    # Gerador
    gerador = tf.keras.Sequential([
        layers.Dense(128, activation='relu', input_dim=latent_dim),
        layers.BatchNormalization(),
        layers.Dense(256, activation='relu'),
        layers.BatchNormalization(),
        layers.Dense(input_dim, activation='tanh')
    ])

    # Discriminador
    discriminador = tf.keras.Sequential([
        layers.Dense(256, activation='relu', input_dim=input_dim),
        layers.Dropout(0.3),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(1, activation='sigmoid')
    ])

    # Compilar o discriminador
    discriminador.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # GAN combinando gerador e discriminador
    discriminador.trainable = False
    gan = tf.keras.Sequential([gerador, discriminador])
    gan.compile(optimizer='adam', loss='binary_crossentropy')

    return gerador, discriminador, gan

# Dimensões
input_dim = len(colunas_respostas)  # Número de colunas de entrada
latent_dim = 100  # Dimensão do espaço latente

# Criar os componentes do GAN
gerador, discriminador, gan = criar_gan(input_dim, latent_dim)

# Mostrar resumos
gerador.summary()
discriminador.summary()

# Pré-processar os dados (normalizar)
data_normalizada = (data_respostas - data_respostas.min()) / (data_respostas.max() - data_respostas.min())
data_normalizada = data_normalizada.fillna(0).values

# Função para treinar o GAN
def treinar_gan(gerador, discriminador, gan, dados_reais, epochs, batch_size):
    for epoch in range(epochs):
        # Criar amostras reais
        idx = np.random.randint(0, dados_reais.shape[0], batch_size)
        amostras_reais = dados_reais[idx]

        # Criar amostras falsas
        ruido = np.random.normal(0, 1, (batch_size, latent_dim))
        amostras_falsas = gerador.predict(ruido)

        # Combinar os rótulos
        rótulos_reais = np.ones((batch_size, 1))
        rótulos_falsos = np.zeros((batch_size, 1))

        # Treinar o discriminador
        d_loss_real = discriminador.train_on_batch(amostras_reais, rótulos_reais)
        d_loss_fake = discriminador.train_on_batch(amostras_falsas, rótulos_falsos)

        # Treinar o gerador
        ruido = np.random.normal(0, 1, (batch_size, latent_dim))
        rótulos_invertidos = np.ones((batch_size, 1))
        g_loss = gan.train_on_batch(ruido, rótulos_invertidos)

        # Mostrar progresso
        if epoch % 100 == 0:
            print(f"Epoch {epoch}/{epochs} | D Loss: {d_loss_real[0]}, G Loss: {g_loss}")

# Treinar o GAN
treinar_gan(gerador, discriminador, gan, data_normalizada, epochs=100, batch_size=32)

# Gerar novas amostras
num_amostras = 100
ruido = np.random.normal(0, 1, (num_amostras, latent_dim))
amostras_sinteticas = gerador.predict(ruido)

# Denormalizar os dados sintéticos
amostras_denormalizadas = amostras_sinteticas.copy()
for i, col in enumerate(data_respostas.columns):
    # Ajusta os valores de cada coluna com base nos mínimos e máximos originais
    amostras_denormalizadas[:, i] = (
        amostras_denormalizadas[:, i] * (data_respostas[col].max() - data_respostas[col].min())
        + data_respostas[col].min()
    )

# Converter as amostras denormalizadas para um DataFrame
df_sintetico = pd.DataFrame(amostras_denormalizadas, columns=data_respostas.columns)

# Concatenar as novas amostras com os dados originais
df_completo = pd.concat([data_respostas, df_sintetico], ignore_index=True)

# Salvar os dados em um arquivo .ods
df_completo.to_excel("dados_ampliados.ods", engine="odf", index=False)
print("Dados gerados e salvos em 'dados_ampliados.ods'.")

# Função para desnormalizar e limitar os valores ao intervalo original
def desnormalizar_e_limitar(dados_sinteticos, data_respostas):
    dados_denormalizados = dados_sinteticos.copy()
    for i, coluna in enumerate(data_respostas.columns):
        # Desnormaliza
        dados_denormalizados[:, i] = (
            dados_denormalizados[:, i] * (data_respostas[coluna].max() - data_respostas[coluna].min())
            + data_respostas[coluna].min()
        )
        # Limita os valores ao intervalo original
        dados_denormalizados[:, i] = np.clip(dados_denormalizados[:, i], data_respostas[coluna].min(), data_respostas[coluna].max())
    return dados_denormalizados

# Função para converter os dados sintéticos de volta para as alternativas textuais
def converter_para_respostas_textuais(dados_sinteticos, label_encoders, data_respostas):
    # Desnormaliza e limita os dados sintéticos
    dados_denormalizados = desnormalizar_e_limitar(dados_sinteticos, data_respostas)
    
    # Converte os valores numéricos de volta para as alternativas textuais
    dados_textuais = pd.DataFrame(dados_denormalizados, columns=data_respostas.columns)
    for coluna in dados_textuais.columns:
        le = label_encoders[coluna]  # Recupera o LabelEncoder usado para esta coluna
        dados_textuais[coluna] = le.inverse_transform(dados_textuais[coluna].astype(int))  # Converte os números de volta para as alternativas
    
    return dados_textuais

# Gerar novas amostras com o GAN
num_amostras = 40000
ruido = np.random.normal(0, 1, (num_amostras, latent_dim))
amostras_sinteticas = gerador.predict(ruido)

# Converter os dados sintéticos para as alternativas originais
df_sintetico_textual = converter_para_respostas_textuais(amostras_sinteticas, label_encoders, data_respostas)

# Concatenar os dados sintéticos convertidos com os dados originais
df_completo_textual = pd.concat([data_respostas, df_sintetico_textual], ignore_index=True)

# Salvar os dados com alternativas textuais no arquivo .ods
df_completo_textual.to_excel("dados_ampliados_textuais.ods", engine="odf", index=False)
print("Dados com alternativas textuais gerados e salvos em 'dados_ampliados_textuais.ods'.")


# 1. Carregar os dados reais (dados coletados)
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


# 2. Concatenar os dados reais (47 primeiros dados) com os dados sintéticos convertidos
df_completo_textual = pd.concat([data_respostas, df_sintetico_textual], ignore_index=True)

# 3. Salvar o arquivo combinado
df_completo_textual.to_excel("dados_ampliados_textuais_combinados.ods", engine="odf", index=False)
print("Dados combinados e salvos em 'dados_ampliados_textuais_combinados.ods'.")
