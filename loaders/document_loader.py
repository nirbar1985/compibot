import os
from typing import List

from langchain.document_loaders import CSVLoader, Docx2txtLoader, PDFMinerLoader, TextLoader, UnstructuredExcelLoader
from langchain.document_loaders.base import BaseLoader
from langchain.schema import Document

DOCUMENT_MAP = {
    '.txt': TextLoader,
    '.md': TextLoader,
    '.py': TextLoader,
    '.pdf': PDFMinerLoader,
    '.csv': CSVLoader,
    '.xls': UnstructuredExcelLoader,
    '.xlsx': UnstructuredExcelLoader,
    '.docx': Docx2txtLoader,
    '.doc': Docx2txtLoader,
}


class DocumentLoader(BaseLoader):

    def __init__(self, documents_path):
        self.__documents_path = documents_path

    def load(self) -> List[Document]:
        documents = []
        # Iterate through files in the source_directory
        for file in os.listdir(self.__documents_path):
            file_ext = os.path.splitext(file)[1]  # Get file extension
            if file_ext in DOCUMENT_MAP:
                # Create the complete file path
                file_path = os.path.join(self.__documents_path, file)

                # Initialize and use the appropriate loader
                loader = DOCUMENT_MAP[file_ext](file_path)
                documents.extend(loader.load())

        return documents
