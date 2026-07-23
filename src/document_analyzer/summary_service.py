from pathlib import Path
class SummaryService:
    
    def __init__(self) -> str:
        pass
    
    def generate_prompt(self, document) ->str:
        prompt = Path(
            "src/common/prompts/summary_prompt.md"
        ).read_text(encoding="utf-8")

        #return prompt.replace("{{document}}",
        #    document.content)
        
        prompt = prompt.replace(
            "{{document}}",
            document.content,)
        
        if "{{document}}" in prompt:
            raise ValueError(
                "Document placeholder was not replaced.")
            
        if not document.content.strip():
            raise ValueError(
                "Document content is empty.")
        return prompt
    