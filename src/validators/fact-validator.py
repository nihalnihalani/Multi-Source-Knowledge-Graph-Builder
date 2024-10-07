from langchain.llms import OpenAI
from typing import Dict, Any

class FactValidator:
    def __init__(self, config: Dict[str, Any]):
        self.llm = OpenAI(temperature=config['llm']['temperature'])
        
    def validate_fact(self, fact: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a fact using LLM cross-referencing."""
        prompt = self._create_validation_prompt(fact)
        validation_result = self.llm(prompt)
        return self._process_validation_result(validation_result)
    
    def _create_validation_prompt(self, fact: Dict[str, Any]) -> str:
        """Create a prompt for fact validation."""
        return f"Validate the following fact: {fact['text']} is a {fact['type']}. Respond with 'True' if correct, 'False' if incorrect."
    
    def _process_validation_result(self, result: str) -> Dict[str, Any]:
        """Process the validation result."""
        is_valid = result.strip().lower() == 'true'
        return {
            "is_valid": is_valid,
            "confidence_score": 1.0 if is_valid else 0.0
        }
