from typing import Final

COMPANY_NAME: Final[str] = 'cyberark'
BOTO3: Final[str] = 'boto3'
DOCUMENTS_FOLDER: Final[str] = "documents"
DB_FOLDER: Final[str] = "db"

# Define the folder for storing database
SOURCE_DIRECTORY_BOTO3_DOCS = f'{DOCUMENTS_FOLDER}/docs_{BOTO3}/'
SOURCE_DIRECTORY_COMPANY_DOCS = f'{DOCUMENTS_FOLDER}/docs_{COMPANY_NAME}/'

PERSIST_DIRECTORY_BOTO3_DB = f'{DB_FOLDER}/db_{BOTO3}'
PERSIST_DIRECTORY_COMPANY_DB = f'{DB_FOLDER}/db_{COMPANY_NAME}'
