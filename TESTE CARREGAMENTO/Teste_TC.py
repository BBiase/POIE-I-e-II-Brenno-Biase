import subprocess
import ollama
from time import time

OLLAMA_MODEL = "phi4:14b"  
QTD_TESTES = 60
ARQUIVO_SAIDA = "resultados_carregamento.txt"

def registrar_linha(texto):
    with open(ARQUIVO_SAIDA, "a", encoding="utf-8") as f:
        f.write(texto + "\n")

registrar_linha("")
registrar_linha(f"============ {OLLAMA_MODEL} ============")
registrar_linha(f"Quantidade de testes de carregamento: {QTD_TESTES}")

for i in range(1, QTD_TESTES + 1):
    print(f"[{i}/{QTD_TESTES}] Derrubando modelo...", flush=True)

    # Derruba o modelo
    try:
        subprocess.run(["ollama", "stop", OLLAMA_MODEL], check=True)
    except subprocess.CalledProcessError:
        print("Aviso: não foi possível parar o modelo (talvez não estivesse carregado).")

    print("Carregando modelo...", flush=True)
    tempo_inicio = time()

    try:
        _ = ollama.generate(model=OLLAMA_MODEL, prompt="Bom dia")
    except Exception as e:
        print("Aviso: erro durante carregamento do Ollama.", e)

    tempo_total = time() - tempo_inicio

    print(f"Tempo do teste {i}: {tempo_total:.2f} segundos")

    # Registra no arquivo
    registrar_linha(f"{i}-TC:{tempo_total:.2f}")

print("\nFinalizado! Resultados salvos em:", ARQUIVO_SAIDA)
