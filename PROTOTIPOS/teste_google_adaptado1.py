from google import genai

client = genai.Client(api_key="API GOOGLE AQUI")

regulamento = 'Para ser aprovado na disciplina, o aluno precisa obter média igual ou superior a 8 (oito). Essa média será igual à soma de duas notas parciais, AP1 e AP2, dividida por 2. A nota de AP1 é composta pela soma da nota da primeira prova, P1, mais a nota de participações durante as aulas, E1. Caso a soma de P1+E1 supere a nota dez, assume-se que AP1=10. O mesmo se aplica a AP2, que é formada pela soma da nota da segunda prova, P2, mais as participações em sala de aula, E2.'

pergunta = "Se um aluno tirar 7 de P1, 4 de E1, 4 de P2 e 1 de E2, ele está aprovado?"

resposta1 = "The student didn't get approved." # 0
resposta2 = "Sim, o aluno está aprovado com média 8." # 1
resposta3 = "O aluno fez as duas provas e participou das aulas." # 2
resposta4 = "O aluno foi aprovado com média 7.5" # 3
resposta5 = "O istudanti si reprovo com média 7.5" # 4
resposta6 = "Não, o aluno está reprovado com média 7.5." #5

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

Respostas a avaliar: 
Resposta 1: {resposta1}
Resposta 2: {resposta2}
Resposta 3: {resposta3}
Resposta 4: {resposta4}
Resposta 5: {resposta5}
Resposta 6: {resposta6}

Retorne apenas 6 números de 0 a 5, separados por vírgula e sem espaços entre eles.
'''

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=solicitacao
)

print(response.text)
