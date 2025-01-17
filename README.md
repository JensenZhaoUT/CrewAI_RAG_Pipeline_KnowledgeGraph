# CrewAI RAG Pipeline KnowledgeGraph
## Overview
*This project implements a pipeline to process a PDF document, extract relevant information, and generate responses to user queries using Llama3. The pipeline is designed to utilize CrewAI for managing agents and tasks and leverages BM25 for information retrieval from text data.*

### Project Structure
1. **Document Ingestion Agent:** Load and pre-process PDF documents, focusing on tables.
2. **Table Parsing Agent:** Parse tables within the documents to extract structured data.
3. **RAG Integration Agent:** Integrate MiniLM for query-based information retrieval.
4. **Knowledge Graph Generation Agent:** Generate a knowledge graph from the retrieved document evidence.

### Tools and Frameworks used/trialed in the project
1. **CrewAI**: The core framework used to build the agentic workflow and manage task execution.
2. **Ollama**: Utilized for language model operations, such as query processing and response generation.
3. **Camelot**: Used for extracting tables from PDF documents.
4. **LLM Sherpa**: LLM Sherpa provides strategic APIs with OCR to parse the pdf files
5. **NLTK**: Employed for NLP tasks, such as tokenization, stopword removal, and lemmatization.
6. **spaCy**: Used for NLP tasks, such as entity recognition and relationship extraction
7. **NetworkX and pyvis**: For constructing and visualizing knowledge graphs.

## Setup

### Prerequisites
1. **NVIDIA GPU with CUDA enabled:** Ensure CUDA is installed and configured properly.
2. **Linux Environment:** Preferably Ubuntu 20.04 or higher.
3. **RAM:** Greater than 16GB for handling large documents and processing.
4. **Docker Installed:** To run the pipeline in isolated containers.

> :memo: **Note**
>
> The process speed of the agents depends on the capability of the GPU and CPU. For reference, Ryzen7 4000 series CPU and NVIDIA 1650Ti is slow on exeucting the tasks.

### Local Installation

1. Clone the Repository
```bash
mkdir projects
cd projects
git clone https://github.com/JensenZhaoUT/CrewAI_RAG_Pipeline_KnowledgeGraph.git
```

2. Build and start the docker
```bash
cd CrewAI_RAG_Pipeline_KnowledgeGraph
bash build.bash
bash run.bash
```

> :memo: **Note**
>
> The dockerfile is fairly large and can long time to build since it's prepared to be ran without the poetry dependencies. That gives user dual option to run the project in Docker. Hence enhanced the customizability. 

3. Setup Large Language Model
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3
ollama create <your-model-name> -f ./Modelfile
```
Modify the <pdf_processor_crew/Modelfile> to the parameters you prefer
Change <ResponseGenerator.py> and <agents.py>'s line
```
model="crewai-llama3.1-8b"
```
to <your_model_name>.

> :memo: **Note**
>
> The Llama 3.1 seems to be unstable when executing some of the tasks. Fine tunning the parameters in the Modelfile could be necessary.

### Docker Setup
1. Install Poetry
```bash
cd pdf_processor_crew
poetry lock --no-update
poetry install
```

2. Start the project
```bash
poetry run pdf_processor_crew
```

> :memo: **Note**
>
> Even in the case that all the inputs are correct and consistent, the large language model could have different response.

