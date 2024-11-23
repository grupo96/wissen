from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Carrega o modelo e o tokenizer
def carregar_falcon7b():
    modelo = "tiiuae/falcon-7b"
    tokenizer = AutoTokenizer.from_pretrained(modelo)
    
    # Define o token de preenchimento como o token de fim de sequência (eos_token)
    tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        modelo,
        torch_dtype=torch.float16,  # Use float16 se estiver usando GPU com suporte
        device_map="auto"          # Configura automaticamente para GPU se disponível
    )
    return tokenizer, model

def gerar_texto_falcon(prompt, max_length=200, temperature=0.7):
    tokenizer, model = carregar_falcon7b()
    
    # Prepara a entrada
    device = "cuda" if torch.cuda.is_available() else "cpu"
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True).to(device)
    
    # Gera o texto
    outputs = model.generate(
        **inputs,
        max_length=max_length,
        temperature=temperature,
        do_sample=True
    )
    
    # Decodifica e retorna o texto gerado
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Teste do gerador
comando = "Explain the basic concepts of uniformly accelerated motion in physics."
conteudo = gerar_texto_falcon(comando)
print("Generated content:")
print(conteudo)
