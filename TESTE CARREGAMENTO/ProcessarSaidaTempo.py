import re
from openpyxl import Workbook

ARQUIVO_TXT = "resultados_carregamento.txt"
ARQUIVO_XLSX = "resultados_carregamento.xlsx"

# Regex para pegar modelos e testes
regex_modelo = re.compile(r"=+\s*(.+?)\s*=+")
regex_tempo = re.compile(r"(\d+)-TC:([\d\.,]+)")

dados = []

with open(ARQUIVO_TXT, "r", encoding="utf-8") as f:
    linhas = f.readlines()

modelo_atual = None

for linha in linhas:
    linha = linha.strip()

    # Detecta o bloco do modelo
    m = regex_modelo.search(linha)
    if m:
        modelo_atual = m.group(1)  # ex: gemma3:12b
        continue

    # Detecta linhas do tipo "3-TC:19.21"
    t = regex_tempo.search(linha)
    if t and modelo_atual:
        num_teste = int(t.group(1))
        tempo = t.group(2).replace(".", ",")  # ajusta vírgula se preferir
        dados.append([modelo_atual, num_teste, tempo])

# Criação da planilha
wb = Workbook()
ws = wb.active
ws.title = "Resultados"

# Cabeçalho
ws.append(["MD", "TESTE", "TC"])

# Adiciona linhas
for linha in dados:
    ws.append(linha)

# Salva Excel
wb.save(ARQUIVO_XLSX)

print(f"Planilha gerada com sucesso: {ARQUIVO_XLSX}")
