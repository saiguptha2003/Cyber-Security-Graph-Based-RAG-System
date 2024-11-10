from datetime import datetime
import logging
from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel
from service import CyberSecurityRag

app = FastAPI()
cyberRag = CyberSecurityRag()

class Relationship(BaseModel):
    targetId: str
    type: str
    properties: dict | None = {}

class Entity(BaseModel):
    id: str
    type: str
    properties: dict
    relationships: List[Relationship]

class QueryRequest(BaseModel):
    question: str

class ProcessTextRequest(BaseModel):
    text: str

@app.post("/process_text/")
async def processText(request: ProcessTextRequest):
    try:
        extractedEntities = await cyberRag.process_text(request.text)
        return {"extractedEntities": extractedEntities}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/update_graph/")
async def updateGraph(entities: List[Entity]):
    try:
        await cyberRag.update_graph(entities)
        return {"message": "Graph updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query/")
async def query(request: QueryRequest):
    startTime = datetime.now()
    logging.info(f"Received query at {startTime}: {request}")

    try:
        response = await cyberRag.query(request.question)
        
        endTime = datetime.now()
        elapsedTime = endTime - startTime

        return {
            "response": response,
            "startTime": startTime.isoformat(),
            "endTime": endTime.isoformat(),
            "elapsedTime": str(elapsedTime)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
