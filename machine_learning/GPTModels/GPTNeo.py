from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Carrega o modelo e o tokenizer
def carregar_modelo_gpt_neo():
    modelo = "tiiuae/falcon-7b"
    tokenizer = AutoTokenizer.from_pretrained(modelo)
    model = AutoModelForCausalLM.from_pretrained(modelo)
    return tokenizer, model

# Gera texto com GPT-Neo
def gerar_texto_gpt_neo(prompt, max_length=300, temperature=0.7):
    tokenizer, model = carregar_modelo_gpt_neo()
    inputs = tokenizer(prompt, return_tensors="pt")
    
    # Geração de texto
    outputs = model.generate(
        inputs.input_ids,
        max_length=max_length,
        temperature=temperature,
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        early_stopping=True
    )
    
    # Decodifica o texto gerado
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
# Função para gerar conteúdo introdutório

def gerar_conteudo_cinematica_gpt_neo(comando):
    prompt = f"Explique de forma clara e didática os conceitos básicos de {comando} para alunos do ensino médio."
    conteudo = gerar_texto_gpt_neo(prompt)
    return conteudo

# Teste do gerador
comando = "movimento uniformemente variado"
conteudo = gerar_conteudo_cinematica_gpt_neo(comando)
print("Conteúdo gerado:")
print(conteudo)

# Função para gerar exercícios
def gerar_exercicios_cinematica_gpt_neo(topico, dificuldade="média"):
    prompt = (
        f"Crie 3 exercícios sobre {topico} de nível {dificuldade} para alunos do ensino médio."
        " Incluir as respostas detalhadas."
    )
    exercicios = gerar_texto_gpt_neo(prompt)
    return exercicios

# Teste de exercícios
topico = "movimento uniformemente acelerado"
exercicios = gerar_exercicios_cinematica_gpt_neo(topico)
print("Exercícios gerados:")
print(exercicios)
