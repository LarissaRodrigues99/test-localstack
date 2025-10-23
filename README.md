# 🧾 Projeto: Processamento de Notas Fiscais com AWS LocalStack

![Arquitetura do Projeto](./S3%20e%20Lambida.png)

## 📖 Visão Geral

Este projeto tem como objetivo demonstrar, de forma prática, o uso do **LocalStack** para simular serviços da **AWS** em ambiente local, permitindo desenvolver e testar aplicações que integram **Lambda**, **S3** e **DynamoDB** sem custo e sem precisar de uma conta na nuvem.  

A ideia central é automatizar o **processamento de notas fiscais**: sempre que um arquivo JSON é enviado para um bucket S3, uma função Lambda é acionada para ler os dados e gravá-los em uma tabela DynamoDB.

---

## 🧠 Conceito

O projeto recria um fluxo comum em arquiteturas **serverless (sem servidor)**, onde a infraestrutura é acionada sob demanda.  
Esse tipo de solução é ideal para sistemas que precisam processar arquivos, eventos ou dados em tempo real — como emissão de notas, relatórios ou logs de auditoria.

Com o **LocalStack**, é possível reproduzir esse ecossistema localmente, simulando:
- **Armazenamento de arquivos (S3)**
- **Execução de funções Lambda**
- **Persistência de dados (DynamoDB)**
- **Integrações por eventos e triggers**

---

## ⚙️ Arquitetura do Sistema

1. 🗂️ **S3 (notas-fiscais-upload)**  
   Repositório onde são armazenados os arquivos JSON contendo as notas fiscais.

2. ⚡ **Lambda (ProcessarNotasFiscais)**  
   Função que é automaticamente executada quando um novo arquivo é enviado ao S3.  
   Ela lê o arquivo, interpreta o conteúdo e insere os dados no DynamoDB.

3. 💾 **DynamoDB (NotasFiscais)**  
   Banco de dados NoSQL que armazena as notas processadas, contendo:
   - `id`: identificador único  
   - `cliente`: nome do cliente  
   - `valor`: valor da nota  
   - `data_emissao`: data em que a nota foi gerada  

4. 🧱 **LocalStack**  
   Ferramenta que simula a AWS localmente, permitindo o uso dos mesmos comandos e SDKs da nuvem real (AWS CLI, boto3, etc.).  

---

## 💻 Componentes do Projeto

### `gerar_dados.py`
Script responsável por **gerar dados fictícios de notas fiscais** e salvá-los em um arquivo JSON (`notas_fiscais_2025.json`).  
Isso simula o processo de criação ou recebimento de notas que seriam enviadas ao S3.  

```python
def gerar_nota():
    return {
        "id": str(uuid.uuid4()),
        "cliente": random.choice(["João Silva", "Maria Oliveira", "Carlos Souza", "Ana Santos"]),
        "valor": round(random.uniform(100, 1000), 2),
        "data_emissao": datetime.now().strftime("%Y-%m-%d")
    }
```

---

### `grava_db.py`
Código principal da **função Lambda**.  
Lê o conteúdo do arquivo enviado ao S3, decodifica o JSON e insere as notas na tabela DynamoDB.

```python
def lambda_handler(event, context):
    s3 = boto3.client('s3', endpoint_url="http://localhost:4566")
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")

    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        response = s3.get_object(Bucket=bucket, Key=key)
        data = json.loads(response['Body'].read().decode('utf-8'))

        if isinstance(data, list):
            for item in data:
                table.put_item(Item=item)
```

---

### `notification_roles.json`
Arquivo que define o **gatilho (trigger)** do S3 para invocar a função Lambda sempre que um objeto for criado.

```json
{
  "LambdaFunctionConfigurations": [
    {
      "LambdaFunctionArn": "arn:aws:lambda:us-east-1:000000000000:function:ProcessarNotasFiscais",
      "Events": ["s3:ObjectCreated:*"]
    }
  ]
}
```

---

### `HELP.txt`
Arquivo de apoio com todos os **comandos necessários para configuração e execução** do ambiente LocalStack, incluindo:
- Criação do bucket S3  
- Criação da tabela DynamoDB  
- Implantação da função Lambda  
- Configuração do trigger e API Gateway  

Esse arquivo é o guia prático do projeto.

---

## 🎯 Objetivo do Projeto

O principal objetivo é **demonstrar uma arquitetura completa e automatizada em ambiente simulado**, integrando diferentes serviços AWS.  
Isso possibilita o aprendizado e a validação de fluxos **serverless** reais sem depender da infraestrutura da Amazon.

Com isso, o projeto serve como:
- 🧩 **Prova de conceito** de integração entre serviços AWS  
- 🎓 **Exemplo educacional** para estudantes e desenvolvedores iniciantes  
- 💼 **Base de testes locais** antes de deploys em produção  

---

## 🧠 Conclusão

Este projeto mostra na prática como é possível:
- Criar aplicações **event-driven** (baseadas em eventos)
- Utilizar **AWS Lambda, S3 e DynamoDB** de forma integrada
- Simular todo o ambiente AWS localmente com o **LocalStack**
- Automatizar o processamento de arquivos JSON e o armazenamento de dados  

É uma demonstração clara do potencial do **modelo serverless**, com aplicações que escalam automaticamente, têm baixo custo e alta flexibilidade.  
