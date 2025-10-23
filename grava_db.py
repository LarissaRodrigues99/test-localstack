import boto3
import json

def lambda_handler(event, context):
    s3 = boto3.client('s3', endpoint_url="http://localhost:4566")
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")

    table = dynamodb.Table('NotasFiscais')

    # Captura o nome do bucket e o arquivo enviado
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        print(f"Lendo arquivo {key} do bucket {bucket}...")

        # Lê o conteúdo do arquivo JSON
        response = s3.get_object(Bucket=bucket, Key=key)
        data = json.loads(response['Body'].read().decode('utf-8'))

        # Se o arquivo for uma lista de notas
        if isinstance(data, list):
            for item in data:
                table.put_item(Item=item)
        else:
            table.put_item(Item=data)

        print(f"✅ Dados inseridos na tabela NotasFiscais")

    return {"statusCode": 200, "body": "Processamento concluído"}