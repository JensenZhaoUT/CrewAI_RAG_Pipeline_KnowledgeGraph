from crewai import Agent
from langchain_openai import ChatOpenAI
from .tools.PdfLoader import PDFLoader
from .tools.TableExtractor import TableExtractor
from .tools.TableParser import TableParser
from .tools.PromptProcessor import PromptProcessor
from .tools.ResponseGenerator import ResponseGenerator
from .tools.KnowledgeGraphBuilder import KnowledgeGraphBuilder
class DocumentAgents:

    def __init__(self):
        self.llm = ChatOpenAI(
            model="crewai-llama3.1-8b",
            base_url="http://localhost:11434/v1",
            api_key="NA"
        )

    def document_ingestion_agent(self):
        return Agent(
            role='Document Ingestion Agent',
            goal='Load and pre-process PDF documents, focusing on extracting tables for further processing.',
            backstory='With extensive experience in handling various document formats, you excel at efficiently extracting and organizing information from PDFs.',
            tools=[PDFLoader.LoadPdf, TableExtractor.ExtractTables],
            allow_delegation=False,
            verbose=True,
            llm=self.llm,
        )
    
    def table_parsing_agent(self) -> Agent:
        return Agent(
            role='Table Parsing Agent',
            goal='Parse tables within the documents to extract structured data, including identifying headers and relating superscripts to their references.',
            backstory='As a seasoned data analyst, you have a knack for transforming raw table data into structured and meaningful information.',
            tools=[TableParser.ParseTable],
            allow_delegation=False,
            verbose=True,
            llm=self.llm,
        )
    
    def user_prompt_handling_agent(self) -> Agent:
        return Agent(
            role='User Prompt Handling Agent',
            goal='Process user queries and prepare them for efficient retrieval of relevant information. Pre-process user prompts using NLP techniques.',
            backstory='With a strong background in natural language processing, you excel at interpreting and refining user prompts to ensure accurate information retrieval.',
            tools=[PromptProcessor.HandlePrompt],
            allow_delegation=False,
            verbose=True,
            llm=self.llm,
        )
    
    def rag_integration_agent(self) -> Agent:
        return Agent(
            role='RAG Integration Agent',
            goal='Integrate retrieval-augmented generation (RAG) for handling complex queries that require information from text files.',
            backstory='With expertise in combining retrieval and generation techniques, you ensure comprehensive and accurate responses to user queries.',
            tools=[ResponseGenerator.GenerateResponse],
            allow_delegation=False,
            verbose=True,
            llm=self.llm,
        )
    
    def knowledge_graph_generation_agent(self) -> Agent:
        return Agent(
            role='Knowledge Graph Generation Agent',
            goal='Read the user query. Build a detailed knowledge graph based on the extracted data.',
            backstory='As a knowledge engineer, you are adept at creating structured representations of information that show the relationship between entities.',
            tools=[KnowledgeGraphBuilder.BuildGraph],
            allow_delegation=False,
            verbose=True,
            llm=self.llm,
        )
