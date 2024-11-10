# Cyber Security Graph Based RAG System Integrated with FastAPI 

## Documentation

### Project Overview

##### Cyber Security Graph-Based RAG System Integrated with FastAPI is a modern, secure web application developed using FastAPI. It assists cybersecurity analysts in analyzing network properties, vulnerabilities, and issues in servers and applications. The system leverages a graph-based approach to visualize relationships and exploit data, providing detailed and actionable insights. By using the RAG system, it categorizes vulnerabilities and risks based on severity, helping analysts identify and address potential threats efficiently. The application offers an intuitive interface for monitoring, diagnosing, and responding to cybersecurity risks effectively.

### System Flowchart

![System Flowchart](/images/serviceLayer.jpg)

### API Flowchart

![System Flowchart](/images/apiflowchart.jpg)


## What Expected?

#### 1. Define Graph Structure for Cybersecurity Data
#### 2. Environment Setup
#### 3. Build the Graph RAG Pipeline
#### 4. Inference Pipeline for Question Answering
#### 5. Deploy on AWS
#### 6. Correct Solutions and accurate answers

## What i compromised?
#### 1. AWS Deployment:
##### Reason: I have used my entire free tier, so I am unable to deploy it on AWS.
#### 2. Correct Solutions and accurate answers
##### Reason: The OpenAI API is not functioning, so I opted for GPT-2, which takes more time to process and sometimes provides irrelevant responses. These could be improved through prompt optimization.


## Installation in Local System

1. clone the project
```bash
git clone https://github.com/saiguptha2003/Cyber-Security-Graph-Based-RAG-System-.git

```
2. a. Installation of Poetry Tool for Linux
``` bash
curl -sSL https://install.python-poetry.org | python3 -

```
2. b. Installation of Poetry Tool for Windows
``` bash
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

```
3. Intialize the poetry to the project
```bash
 peotry init 
```
4. Activate the Poetry Virtual Environment
```bash
poetry shell
```
5. install the dependencies through Poetry tool
```bash
poetry install
```
or 

```bash
pip install requirements.txt
```

there the pyproject file will be used as the lookup file
6. change directory to src
```bash
cd src
```
7. Start FastAPI Server
```bash
uvicorn app.main:app --reload
```


