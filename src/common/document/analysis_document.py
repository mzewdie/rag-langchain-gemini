from dataclasses import dataclass

@dataclass
class AnalysisDocument:
    filename: str
    content: str
    document_type: str
    pages: int
    metadata: dict
    
    def __str__(self):
        return f"{self.filename} in __str__ ({len(self.content)} characters)"
    
    def __repr__(self):
        return (
            f"AnalysisDocument(in __repr__"
            f"filename='{self.filename}', "
            f"type='{self.document_type}', "
            f"chars={len(self.content)}, "
            f"metadata={self.metadata})"
        )