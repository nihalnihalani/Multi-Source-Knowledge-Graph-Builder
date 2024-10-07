from neo4j import GraphDatabase
from typing import Dict, List, Any

class KnowledgeGraph:
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        
    def add_entity(self, entity: Dict[str, Any]) -> None:
        """Add an entity to the knowledge graph."""
        with self.driver.session() as session:
            session.write_transaction(self._create_entity, entity)
    
    def add_relationship(self, relationship: Dict[str, Any]) -> None:
        """Add a relationship to the knowledge graph."""
        with self.driver.session() as session:
            session.write_transaction(self._create_relationship, relationship)
    
    def update_confidence_score(self, entity_id: str, new_score: float) -> None:
        """Update confidence score for an entity."""
        with self.driver.session() as session:
            session.write_transaction(self._update_score, entity_id, new_score)
    
    @staticmethod
    def _create_entity(tx, entity: Dict[str, Any]) -> None:
        query = """
        MERGE (e:Entity {id: $id})
        SET e += $properties
        """
        tx.run(query, id=entity['id'], properties=entity)
    
    @staticmethod
    def _create_relationship(tx, relationship: Dict[str, Any]) -> None:
        query = """
        MATCH (e1:Entity {id: $from_id})
        MATCH (e2:Entity {id: $to_id})
        MERGE (e1)-[r:RELATES {type: $type}]->(e2)
        SET r += $properties
        """
        tx.run(query, 
               from_id=relationship['from_id'],
               to_id=relationship['to_id'],
               type=relationship['type'],
               properties=relationship['properties'])
    
    @staticmethod
    def _update_score(tx, entity_id: str, new_score: float) -> None:
        query = """
        MATCH (e:Entity {id: $id})
        SET e.confidence_score = $new_score
        """
        tx.run(query, id=entity_id, new_score=new_score)
