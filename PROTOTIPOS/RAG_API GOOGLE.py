# =========================
# RAG (FAISS + ICL) + Avaliação com Gemini
# =========================

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from time import time
import os
from google import genai

# Cliente da API Google Gemini
client = genai.Client(api_key="API GOOGLE AQUI")

# Função de avaliação automática com Gemini
def avaliar_com_gemini(regulamento, pergunta, resposta):
    solicitacao = f'''
    Você é um avaliador. Sua tarefa é analisar respostas dadas a perguntas
    sobre um regulamento. Use a seguinte escala de classificação:

    0 = Predominantemente em outro idioma
    1 = Completamente equivocado (alucinação)
    2 = Desvio de contextos
    3 = Parcialmente correto
    4 = Correto (mas prolixo ou com português errado)
    5 = Completamente correto

    Regulamento: {regulamento}

    Pergunta: {pergunta}

    Resposta a avaliar: {resposta}

    Retorne apenas um número de 0 a 5.
    '''
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=solicitacao
    )
    return response.text.strip()

# -----------------------------
# Configurações
# -----------------------------
log_file = "resultados_faiss_offline.txt"
dados_file = "regulamento_regular.txt"
modelo_nome = "phi4:14b"

# -----------------------------
# Contador de perguntas
# -----------------------------
contador_pe = 1

# -----------------------------
# Carregar modelo local de embeddings (offline)
# -----------------------------
tempo_inicio = time()
model = SentenceTransformer('multi-qa-mpnet-base-dot-v1')  # modelo mais preciso
tempo_fim = time()
tc_modelo = tempo_fim - tempo_inicio

print("Bom dia! O modelo de embeddings foi carregado com sucesso!")
print(f"TC: {tc_modelo:.6f} s\n")

# -----------------------------
# Função para gerar embeddings
# -----------------------------
def gerar_embedding(texto):
    return model.encode(texto)

# -----------------------------
# Função para carregar/criar índice FAISS
# -----------------------------
def carregar_indice(dados, index_file="index.faiss"):
    if not os.path.exists(index_file):
        embeddings = np.array([gerar_embedding(texto) for texto in dados]).astype('float32')
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)
        faiss.write_index(index, index_file)
        print("Índice FAISS criado e salvo.")
    else:
        index = faiss.read_index(index_file)
        print("Índice FAISS carregado do disco.")
    return index

# -----------------------------
# Função para buscar resposta
# -----------------------------
def buscar_resposta(pergunta, dados, index, qtd=5):
    embedding_pergunta = gerar_embedding(pergunta)
    embedding_pergunta = np.array(embedding_pergunta, dtype='float32').reshape(1, -1)
    dist, indices = index.search(embedding_pergunta, qtd)
    respostas = [dados[indices[0][i]] for i in range(len(indices[0]))]
    return " ".join(respostas)  # resposta em linha única

# -----------------------------
# Carregar dados do arquivo
# -----------------------------
with open(dados_file, 'r', encoding='utf-8') as f:
    dados = [linha.strip() for linha in f.readlines() if linha.strip()]

# -----------------------------
# Criar ou carregar índice FAISS
# -----------------------------
index = carregar_indice(dados)

# -----------------------------
# Perguntas de teste
# -----------------------------
perguntas = [
    "O que significa TCC?",    
    "Quais são os objetivos da monografia?",
    "Quais são as atribuições do coordenador?",
    "O que o aluno deve fazer se não encontrar um orientador?",
    "Quem deve escrever a monografia?",
    "Quanto o aluno deve tirar para ser aprovado em TCC?",
    "O aluno que tirar nota 7 está aprovado?",
    "Quantos orientandos cada orientador pode ter?"
]

# -----------------------------
# Executar perguntas automaticamente
# -----------------------------
for pergunta_usuario in perguntas:
    print(f"PE: {pergunta_usuario}")

    tempo_resposta_inicio = time()
    resposta = buscar_resposta(pergunta_usuario, dados, index, qtd=5)
    tempo_resposta = time() - tempo_resposta_inicio

    # Avaliação automática com Gemini
    cl_ia = avaliar_com_gemini(" ".join(dados), pergunta_usuario, resposta)

    # Mostrar resultado
    print(f"RE: {resposta}")
    print(f"TR: {tempo_resposta:.6f} s")
    print(f"CL_IA (Google Gemini): {cl_ia}\n")

    # Salvar no arquivo
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"TC:{tc_modelo:.6f}\n")
        f.write(f"PE:{contador_pe}-{pergunta_usuario}\n")
        f.write(f"TR:{tempo_resposta:.6f}\n")
        f.write(f"RE:{resposta}\n")
        f.write(f"CL_IA:{cl_ia}\n\n")

    contador_pe += 1
