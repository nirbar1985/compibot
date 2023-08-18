import os

from dotenv import load_dotenv
from langchain.document_loaders import CSVLoader, Docx2txtLoader, PDFMinerLoader, TextLoader, UnstructuredExcelLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

from compibot.constants import PERSIST_DIRECTORY_BOTO3_DB, PERSIST_DIRECTORY_COMPANY_DB, SOURCE_DIRECTORY_BOTO3_DOCS, \
    SOURCE_DIRECTORY_COMPANY_DOCS

load_dotenv('.env')

DOCUMENT_MAP = {
    ".txt": TextLoader,
    ".md": TextLoader,
    ".py": TextLoader,
    ".pdf": PDFMinerLoader,
    ".csv": CSVLoader,
    ".xls": UnstructuredExcelLoader,
    ".xlsx": UnstructuredExcelLoader,
    ".docx": Docx2txtLoader,
    ".doc": Docx2txtLoader,
}

# directory='docs'


def load_docs(source_directory):
    documents = []
    # Iterate through files in the source_directory
    for file in os.listdir(source_directory):
        file_ext = os.path.splitext(file)[1]  # Get file extension
        if file_ext in DOCUMENT_MAP:
            # Create the complete file path
            file_path = os.path.join(source_directory, file)

            # Initialize and use the appropriate loader
            loader = DOCUMENT_MAP[file_ext](file_path)
            documents.extend(loader.load())

    return documents


def split_docs(documents, chunk_size=500, chunk_overlap=20):
    # Split the documents into smaller chunks
    text_splitter = CharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return text_splitter.split_documents(documents)


def process_docs_and_persist(source_directory, persist_directory):
    documents = load_docs(source_directory=source_directory)
    print(f'Number of loaded documents are [{len(documents)}]')

    chunks = split_docs(documents)
    print(f'Number of chunks are [{len(chunks)}]')

    vectordb = Chroma.from_documents(chunks, embedding=OpenAIEmbeddings(), persist_directory=persist_directory)
    vectordb.persist()


def main():
    # Process boto3 docs
    process_docs_and_persist(
        source_directory=SOURCE_DIRECTORY_BOTO3_DOCS,
        persist_directory=PERSIST_DIRECTORY_BOTO3_DB,
    )

    # Process company docs
    process_docs_and_persist(
        source_directory=SOURCE_DIRECTORY_COMPANY_DOCS,
        persist_directory=PERSIST_DIRECTORY_COMPANY_DB,
    )


if __name__ == "__main__":
    main()
