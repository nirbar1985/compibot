from typing import Final

COMPANY_NAME: Final[str] = 'cyberark'
BOTO3: Final[str] = 'boto3'
DOCUMENTS_FOLDER: Final[str] = 'documents'
DB_FOLDER: Final[str] = 'db'

SOURCE_DIRECTORY_BOTO3_DOCS: Final[str] = f'{DOCUMENTS_FOLDER}/docs_{BOTO3}/'
SOURCE_DIRECTORY_COMPANY_DOCS: Final[str] = f'{DOCUMENTS_FOLDER}/docs_{COMPANY_NAME}/'

PERSIST_DIRECTORY_BOTO3_DB: Final[str] = f'{DB_FOLDER}/db_{BOTO3}'
PERSIST_DIRECTORY_COMPANY_DB: Final[str] = f'{DB_FOLDER}/db_{COMPANY_NAME}'
