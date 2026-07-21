from src.common.document.pdf_loader import PDFLoader
from src.common.document.docx_loader import DOCXLoader


class DocumentFactory:
    
    @staticmethod
    def create(file):
        
        extension=file = file.name.split(".")[-1]
        if extension == "pdf":
            return PDFLoader()
        
        if extension== "docx":
            return DOCXLoader()