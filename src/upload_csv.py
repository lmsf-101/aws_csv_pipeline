import boto3
from botocore.exceptions import ClientError
from create_infrastructure import RAW_BUCKET
from pathlib import Path

WORKING_DIR = Path(__file__).resolve().parent.parent
SAMPLE_CSV_FILE_PATH = WORKING_DIR / "tests" / "data" / "sample_file.csv"
S3_CLIENT = boto3.client("s3")


# Función para subir el archivo CSV a bucket de S3
def upload_csv_to_bucket(s3_client, bucket, file_path):
    try:
        s3_client.upload_file(
            Filename=file_path,
            Bucket=bucket,
            # TODO: Organizar por prefijos con fecha
            Key=Path(file_path).name
        )
    except FileNotFoundError as file_error:
        print(f"No se pudo encontrar el archivo '{file_path}'")
        print(file_error)
    except ClientError as client_err:
        print(f"Ocurrio un error del cliente S3 al momento de subir el archivo '{file_path}'")
        print(client_err)
    else:
        print(f"Subido archivo '{file_path}' hacia bucket {bucket}!")

upload_csv_to_bucket(S3_CLIENT, RAW_BUCKET, SAMPLE_CSV_FILE_PATH)