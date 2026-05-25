import boto3
from botocore.exceptions import ClientError

s3 = boto3.client("s3")
BUCKETS = ('raw-bucket', 'processed-bucket')

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

# Crear raw-bucket y processed-bucket
create_buckets(s3, BUCKETS)

# TODO: Crear la cola SQS (create_queue)