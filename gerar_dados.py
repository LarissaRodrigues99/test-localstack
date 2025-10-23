import json
import random
import uuid
from datetime import datetime

def gerar_nota():
    return {
        "id": str(uuid.uuid4()),
        "cliente": random.choice(["João Silva", "Maria Oliveira", "Carlos Souza", "Ana Santos"]),
        "valor": round(random.uniform(100, 1000), 2),
        "data_emissao": datetime.now().strftime("%Y-%m-%d")
    }

def main():
    notas = [gerar_nota() for _ in range(10)]

    with open("notas_fiscais_2025.json", "w", encoding="utf-8") as f:
        json.dump(notas, f, ensure_ascii=False, indent=4)

    print("✅ Arquivo notas_fiscais_2025.json gerado com sucesso!")

if __name__ == "__main__":
    main()