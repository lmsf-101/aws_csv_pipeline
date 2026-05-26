import boto3
from botocore.exceptions import ClientError

s3 = boto3.client("s3")
RAW_BUCKET = 'raw-bucket'
FINAL_BUCKET = 'processed-bucket'
BUCKETS = (RAW_BUCKET, FINAL_BUCKET)

# Función para generar buckets, según la tupla de nombres
def create_buckets(s3_client, buckets: tuple[str]):

    for bucket in buckets:
        try:
            response = s3_client.create_bucket(
                Bucket=bucket
            )
        except ClientError as err:
            # Si hay error, recuperar su código
            error_code = err.response['Error']['Code']

            # Si se trata de un bucket previamente creado por el usuario, avisar
            if error_code == 'BucketAlreadyOwnedByYou':
                print(f" El bucket {bucket} ya existe")

            # Si es un error totalmente distinto, arrojar el error particular
            else:
                print(f"Ocurrio un error al momento de crear bucket : {bucket}")
                raise err
        else:
            print(f"Bucket '{bucket}' creado de forma exitosa.")


sqs = boto3.client("sqs")
QUEUE_NAME = "csv_queue"

# Función para generar una nueva cola SQS
def create_sqs_queue(sqs_client, queue_name):
    try:
        sqs_response = sqs_client.create_queue(
            QueueName=queue_name
        )
    except ClientError as err:
        if err.response['Error']['Code'] == 'QueueNameExists':
            print(f"La cola {queue_name} ya existe. Omitiendo operación")
        else:
            print(f"Ocurrio un error al crear la cola : '{queue_name}'")
            raise err
    else:
        print(f"Cola '{queue_name}' creada de forma exitosa")
        queue_URL = sqs_response['QueueUrl']
        return queue_URL

# Funcion para recuperar el ARN de la cola generada en base de su URL
def get_queue_ARN(sqs_client, queue_URL):
    response = sqs_client.get_queue_attributes(
        QueueUrl=queue_URL,
        AttributeNames=[
            'QueueArn'
        ]
    )

    return response["Attributes"]['QueueArn']

# Crear raw-bucket y processed-bucket
create_buckets(s3, BUCKETS)

# Crear cola SQS 'csv_queue'
queue_url = create_sqs_queue(sqs, QUEUE_NAME)
print(queue_url)

# Obtener ARN de 'csv_queue' a base de su URL
queue_arn = get_queue_ARN(sqs, queue_url)
print(queue_arn)