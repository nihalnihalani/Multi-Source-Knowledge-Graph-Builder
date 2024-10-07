from transformers import pipeline
from typing import List, Dict, Any

class EntityExtractor:
    def __init__(self, model_name: str = "dbmdz/bert-large-cased-finetuned-conll03-english"):
        self.ner_pipeline = pipeline("ner", model=model_name)
        
    def extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """Extract named entities from text."""
        entities = self.ner_pipeline(text)
        return self._process_entities(entities)
    
    def _process_entities(self, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process and format extracted entities."""
        processed_entities = []
        for entity in entities:
            processed_entity = {
                "text": entity['word'],
                "type": entity['entity'],
                "score": entity['score'],
                "start": entity['start'],
                "end": entity['end']
            }
            processed_entities.append(processed_entity)
        return processed_entities
