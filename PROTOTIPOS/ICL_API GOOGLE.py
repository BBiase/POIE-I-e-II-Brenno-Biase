# =========================
# ICL + Avaliação com Gemini
# =========================

import ollama
from time import time
from google import genai

# Cliente da API Google Gemini
client = genai.Client(api_key="API KEY GOOGLE AQUI")

# Função de avaliação automática com Gemini
def avaliar_com_gemini(regulamento, pergunta, resposta):
    solicitacao = f'''
    Você é um avaliador. Sua tarefa é analisar respostas dadas a perguntas
    sobre um regulamento. Use a seguinte escala de classificação:

    0 = Predominantemente em outro idioma
    1 = Completamente equivocado (alucinação)
    2 = Desvio de contexto
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

# =========================
# Início do processo
# =========================

# Tempo de carregamento do modelo local (ollama)
tempo_carregamento = time()
resultado = ollama.generate(model="phi4:14b", prompt="Bom dia")
tempo_carregamento = time() - tempo_carregamento

# Regulamento
contexto = open('regulamento_regular.txt', encoding='utf-8').readlines()
contexto = "".join(contexto)

# Lista de perguntas
perguntas = [
    '1-O que significa TCC?',
    '2-Quais são os objetivos da monografia?',
    '3-Quais são as atribuições do coordenador?',
    '4-O que o aluno deve fazer se não encontrar um orientador?',
    '5-Quem deve escrever a monografia?',
    '6-Quanto o aluno deve tirar para ser aprovado no TCC?',
    '7-O aluno que tirar nota 7 está aprovado?',
    '8-Quantos orientandos cada orientador pode ter?' 
]

# Loop automático pelas perguntas
for pergunta_original in perguntas:
    # Monta prompt para o modelo local
    pergunta = f"Considere o contexto abaixo e responda em português a pergunta a seguir:\n\nContexto:\n{contexto}\n\nPergunta: {pergunta_original}"

    # Mede o tempo de resposta do modelo local
    tempo_resposta = time()
    resultado = ollama.generate(model="phi4:14b", prompt=pergunta) 
    tempo_resposta = time() - tempo_resposta

    # Extrai a resposta
    resposta = resultado["response"]

    # Avaliação automática com Gemini
    cl_ia = avaliar_com_gemini(contexto, pergunta_original, resposta)

    # Exibe na tela
    print("\n\n=============================================================\n\n")
    print(f"Pergunta: {pergunta_original}")
    print(f"Resposta: {resposta}")
    print(f"Classificação IA (Google Gemini): {cl_ia}")
    print("\n\n=============================================================\n\n")

    # Salva no arquivo
    with open('saida.txt', 'a', encoding="utf-8") as arquivo:
        arquivo.write(f"TC:{tempo_carregamento}\n")               # Tempo de carregamento
        arquivo.write(f"PE:{pergunta_original}\n")                # Pergunta feita
        arquivo.write(f"TR:{tempo_resposta}\n")                   # Tempo de resposta
        arquivo.write(f"RE:{resposta.replace('\n', ' ')}\n")      # Resposta (linha única)
        arquivo.write(f"CL_IA:{cl_ia}\n\n")                       # Classificação da IA
