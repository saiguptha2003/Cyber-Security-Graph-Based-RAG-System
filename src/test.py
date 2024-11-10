import asyncio
from transformers import pipeline

class CyberRAG:
    def __init__(self, model_name="gpt2"):
        self.llm = pipeline("text-generation", model=model_name)
        
        # Sample list of vulnerabilities
        self.vulnerabilities = [
            {"id": "CVE-2021-1234", "description": "SQL Injection vulnerability in a web application."},
            {"id": "CVE-2022-5678", "description": "Cross-Site Scripting (XSS) vulnerability in a chat system."},
            {"id": "CVE-2023-9876", "description": "Buffer overflow vulnerability in a network service."},
            {"id": "CVE-2021-4321", "description": "Remote Code Execution (RCE) vulnerability in a file-sharing app."},
            {"id": "CVE-2020-1234", "description": "Privilege escalation vulnerability in Linux kernel."},
        ]
    
    async def query(self, question):
        # Check if the question is about vulnerabilities
        for vuln in self.vulnerabilities:
            if vuln["id"] in question:
                # Generate a response related to the found vulnerability
                response = f"Vulnerability ID: {vuln['id']}\nDescription: {vuln['description']}"
                return response
        
        # If no specific vulnerability is found, use the model to generate a general response
        prompt = f"Cybersecurity question: {question}\n"
        response = self.llm(prompt, max_new_tokens=50, num_return_sequences=1)
        return response[0]['generated_text']

async def main():
    cyber_rag = CyberRAG()

    # Sample questions to query the model
    questions = [
        "What is CVE-2021-1234?",
        "What vulnerabilities are associated with IP address 192.168.1.1?",
        "Tell me about CVE-2022-5678.",
        "What does a buffer overflow vulnerability mean?"
    ]
    
    for question in questions:
        # Get the response from the model
        response = await cyber_rag.query(question)
        print(f"Question: {question}")
        print("Response:")
        print(response)
        print("\n---\n")

if __name__ == "__main__":
    asyncio.run(main())
