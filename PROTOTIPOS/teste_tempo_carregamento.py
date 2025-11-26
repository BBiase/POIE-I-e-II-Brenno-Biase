import subprocess
import ollama

from time import time
try:
    OLLAMA_MODEL = "gemma3:12b"
    for i in range(3):
        print("Derrubando...", flush=True)
        subprocess.run(["ollama", "stop", OLLAMA_MODEL], check=True)
        tempo = time()
        print("Carregandos...", flush=True)
        try:
            _ = ollama.generate(model=OLLAMA_MODEL, prompt="Bom dia")
        except Exception as e:
            print("Aviso: erro durante carregamento do Ollama.", e)

        tempo = time() - tempo
        print(tempo)
    #print("Servidor Ollama parado com sucesso.")
except subprocess.CalledProcessError as e:
    print(f"Erro ao tentar parar o Ollama: {e}")