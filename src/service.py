from transformers import pipeline
import networkx as nx
from langchain.schema import Document
from typing import List, Dict
from models import Entity

class CyberSecurityRag:
    def __init__(self):
        self.graph = nx.MultiDiGraph()
        self.llm = pipeline("text-generation", model="gpt2")
        self.documentStore = []
    
    async def processText(self, text: str) -> List[Dict]:
        prompt = f"Extract key entities (IP, hostnames, vulnerabilities, services) from this text: {text}"
        response = self.llm(prompt, max_new_tokens=50, num_return_sequences=1)
        return [{"entity": entity.strip()} for entity in response[0]['generated_text'].split("\n")]

    async def updateGraph(self, entities: List[Entity]):
        for entity in entities:
            if "type" not in entity.properties:
                entity.properties["type"] = entity.type

            entityData = entity.dict()
            self.graph.add_node(entity.id, **entityData)

            for rel in entity.relationships:
                self.graph.add_edge(
                    entity.id,
                    rel.targetId,
                    type=rel.type,
                    **rel.properties
                )

        self._updateDocumentStore()
    
    def _updateDocumentStore(self):
        documents = []
        for node in self.graph.nodes(data=True):
            nodeData = {
                "id": node[0],
                "type": node[1].get("type", "unknown"),
                **node[1]
            }
            documents.append(
                Document(
                    pageContent=str(nodeData),
                    metadata={"nodeId": node[0]}
                )
            )
        
        self.documentStore.extend(documents)
    
    async def query(self, question: str) -> str:
        docs = self._retrieveDocumentsForQuery(question)
        context = "\n".join(doc.pageContent for doc in docs)
        prompt = f"Based on this context, answer the question: {context}\nQuestion: {question}"
        response = self.llm(prompt, max_length=150, num_return_sequences=1)
        return response[0]['generated_text']

    def _retrieveDocumentsForQuery(self, query: str) -> List[Document]:
        return self.documentStore[:3]
