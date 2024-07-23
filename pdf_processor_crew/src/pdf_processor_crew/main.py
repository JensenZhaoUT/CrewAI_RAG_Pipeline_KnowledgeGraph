import os
from crewai import Crew, Process
from pdf_processor_crew.agents import DocumentAgents
from pdf_processor_crew.tasks import DocumentTasks

def run():
    # Define the relative paths
    relative_pdf_path = './src/pdf_processor_crew/RAG_Document.pdf'
    relative_save_dir = './extracted_tables'
    extracted_txt = './extracted_tables/RAG_Document.txt'
    json_file_path = './parsed_tables'
    parsed_tables = './parsed_tables/all_parsed_tables.json'
    retrieved_file_path = './parsed_tables/retrieved_info.json'
    
    # Convert to absolute paths
    pdf_path = os.path.abspath(relative_pdf_path)
    save_dir = os.path.abspath(relative_save_dir)
    json_file_path = os.path.abspath(json_file_path)
    parsed_tables = os.path.abspath(parsed_tables)
    extracted_txt = os.path.abspath(extracted_txt)
    
    # # Print the absolute paths
    # print(f"PDF path: {pdf_path}")
    # print(f"Save directory: {save_dir}")
    # print(f"JSON save directory: {json_file_path}")
    
    # Ensure save_dir exists
    os.makedirs(save_dir, exist_ok=True)
    os.makedirs(json_file_path, exist_ok=True)

    # Check if the PDF file exists
    if not os.path.isfile(pdf_path):
        print(f"Error: The file '{pdf_path}' does not exist.")
        return
    
    print("Loading PDF document...")
    inputs = {
        'path_to_pdf': pdf_path,
        'path_to_save_dir': save_dir,
        'extracted_txt': extracted_txt,
        'json_file_path': json_file_path, 
        'parsed_tables': parsed_tables,
        'retrieved_file_path': retrieved_file_path
    }

    user_query = input("Please enter your query: ")

    # Initialize agents and tasks
    agents = DocumentAgents()
    tasks = DocumentTasks()

    # Initialize agents
    document_ingestion_agent = agents.document_ingestion_agent()
    table_parsing_agent = agents.table_parsing_agent()
    user_prompt_handling_agent = agents.user_prompt_handling_agent()
    rag_integration_agent = agents.rag_integration_agent()
    knowledge_graph_generation_agent = agents.knowledge_graph_generation_agent()

    # Initialize tasks
    document_ingestion_task = tasks.document_ingestion_task(
        agent=document_ingestion_agent,
        path_to_pdf=inputs['path_to_pdf'],
        path_to_save_dir=inputs['path_to_save_dir']
    )

    table_parsing_task = tasks.table_parsing_task(
        agent=table_parsing_agent,
        path_to_save_dir=inputs['path_to_save_dir'],
        json_file_path=inputs['json_file_path']
    )

    rag_integration_task = tasks.rag_integration_task(
        agent=rag_integration_agent,
        user_query=user_query,
        text_file_path=inputs['extracted_txt']
    )

    knowledge_graph_generation_task = tasks.knowledge_graph_generation_task(
        agent=knowledge_graph_generation_agent,
        retrieved_file_path=inputs['retrieved_file_path'],
        path_to_save_dir=inputs['path_to_save_dir']
    )

    # Create and run the Crew for the first two tasks
    crew = Crew(
        agents=[rag_integration_agent],
        tasks=[rag_integration_task],
        process=Process.sequential,
        verbose=True,
    )

    # Kick off the Crew pipeline for the first two tasks
    result = crew.kickoff()

    print("\nInitial processing completed. Results:\n", result)

    # # Prompt the user for input
    # user_query = input("Please enter your query: ")

    # # Initialize the user prompt handling task
    # user_prompt_handling_task = tasks.user_prompt_handling_task(
    #     agent=user_prompt_handling_agent,
    #     user_query=user_query
    # )

    # # Run the user prompt handling task
    # crew = Crew(
    #     agents=[user_prompt_handling_agent],
    #     tasks=[user_prompt_handling_task],
    #     process=Process.sequential,
    #     verbose=True,
    # )

    # result = crew.kickoff()
    # print("\nUser prompt processing completed. Results:\n", result)

if __name__ == "__main__":
    run()