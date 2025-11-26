from google import genai

client = genai.Client(api_key="API KEY GOOGLE AQUI ")

regulamento = 'Para ser aprovado na disciplina, o aluno precisa obter média igual ou superior a 8 (oito). Essa média será igual à soma de duas notas parciais, AP1 e AP2, dividida por 2. A nota de AP1 é composta pela soma da nota da primeira prova, P1, mais a nota de participações durante as aulas, E1. Caso a soma de P1+E1 supere a nota dez, assume-se que AP1=10. O mesmo se aplica a AP2, que é formada pela soma da nota da segunda prova, P2, mais as participações em sala de aula, E2.'

pergunta = "Se um aluno tirar 7 de P1, 4 de E1, 4 de P2 e 1 de E2, ele está aprovado?"

# resposta = "The student didn't get approved." # 0
# resposta = "Sim, o aluno está aprovado com média 8." # 1
# resposta = "O aluno fez as duas provas e participou das aulas." # 2
# resposta = "O aluno foi aprovado com média 7.5" # 3
# resposta = "O istudanti si reprovo com média 7.5" # 4
resposta = "Não, o aluno está reprovado com média 7.5." #5

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

print(response.text)
