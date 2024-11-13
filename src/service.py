from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
import networkx as nx
from langchain.schema import Document
from typing import List, Dict, Union
from models import Entity

class CyberSecurityRag:
    def __init__(self):
        self.graph = nx.MultiDiGraph()
        self.llm = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.documentStore = []

    async def processText(self, text: str) -> List[Dict[str, Union[str, Dict]]]:
        prompt = f"Extract key entities (IP, hostnames, vulnerabilities, services) from this text: {text}"
        ner_results = self.llm(text)
        
        entities = []
        for result in ner_results:
            if result['entity_group'] in ["IP", "HOSTNAME", "VULNERABILITY", "SERVICE"]:
                entities.append({
                    "entity": result['word'],
                    "type": result['entity_group']
                })
        return entities

    async def updateGraph(self, text: str):
        entities = await self.processText(text)
        
        for entity_data in entities:
            entity_id = entity_data['entity']
            
            if not self.graph.has_node(entity_id):
                self.graph.add_node(entity_id, **entity_data)
            else:
                existing_data = self.graph.nodes[entity_id]
                existing_data.update(entity_data)
        
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
        
        self.documentStore = documents

    async def query(self, question: str) -> str:
        docs = self._retrieveDocumentsForQuery(question)
        context = "\n".join(doc.pageContent for doc in docs)
        prompt = f"Based on this context, answer the question: {context}\nQuestion: {question}"
        
        response = self.llm(prompt, max_length=150, num_return_sequences=1)
        return response[0]['generated_text']

    def _retrieveDocumentsForQuery(self, query: str) -> List[Document]:
        query_embedding = self.embedding_model.encode(query)
        doc_embeddings = [self.embedding_model.encode(doc.pageContent) for doc in self.documentStore]
        similarities = util.pytorch_cos_sim(query_embedding, doc_embeddings).squeeze(0)
        
        top_k_indices = similarities.topk(3).indices
        relevant_docs = [self.documentStore[idx] for idx in top_k_indices]
        
        return relevant_docs
