from typing import Dict, Any
from ..scrapers.web_scraper import WebScraper
from ..extractors.entity_extractor import EntityExtractor
from ..extractors.relationship_extractor import RelationshipExtractor
from ..validators.fact_validator import FactValidator
from ..graph.knowledge_graph import KnowledgeGraph

class PipelineOrchestrator:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.scraper = WebScraper(config)
        self.entity_extractor = EntityExtractor()
        self.relationship_extractor = RelationshipExtractor(config)
        self.fact_validator = FactValidator(config)
        self.knowledge_graph = KnowledgeGraph(
            config['neo4j']['uri'],
            config['neo4j']['user'],
            config['neo4j']['password']
        )
    
    def process_source(self, source: Dict[str, Any]) -> None:
        """Process a single source and update the knowledge graph."""
        # 1. Scrape data
        raw_data = self.scraper.scrape(source['url'])
        
        # 2. Extract entities and relationships
        for item in raw_data:
            clean_data = self.scraper.clean(item)
            entities = self.entity_extractor.extract_entities(clean_data['text'])
            relationships = self.relationship_extractor.extract_relationships(
                entities, clean_data['text']
            )
            
            # 3. Validate facts
            validated_entities = []
            for entity in entities:
                validation_result = self.fact_validator.validate_fact(entity)
                if validation_result['is_valid']:
                    validated_entities.append({
                        **entity,
                        'confidence_score': validation_result['confidence_score']
                    })
            
            # 4. Update knowledge graph
            for entity in validated_entities:
                self.knowledge_graph.add_entity(entity)
            
            for relationship in relationships:
                if relationship['from_id'] in [e['text'] for e in validated_entities] and \
                   relationship['to_id'] in [e['text'] for e in validated_entities]:
                    self.knowledge_graph.add_relationship(relationship)
