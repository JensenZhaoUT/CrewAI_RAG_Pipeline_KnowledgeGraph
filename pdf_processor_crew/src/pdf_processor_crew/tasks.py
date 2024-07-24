from crewai import Task
from textwrap import dedent

class DocumentTasks:

    def document_ingestion_task(self, agent, path_to_pdf, path_to_save_dir):
        return Task(
            description=dedent(f"""
                Load and pre-process PDF documents in the path_to_pdf to extract the raw content of the file and save it into the Save directory as txt file.
                Next, extract tables from the same PDF document in the path_to_pdf and preprocess the tables and save the tables as CSV files in the Save directory. In second step, ensure accurate extraction of table data and convert it into structured formats
                for further analysis.
                PDF file: {path_to_pdf}
                Save directory: {path_to_save_dir}
            """),
            agent=agent,
            expected_output=dedent(f"""
                Document ingestion task completed.
            """)
        )

    def table_parsing_task(self, agent, path_to_save_dir, json_file_path):
        return Task(
            description=dedent(f"""
                Parse tables within the CSV filesto extract structured data. Identify headers,
                parse rows and columns, and relate superscripts in table columns to their references. Save the parsed resulst to a JSON file in json_file_path
                Ensure data integrity and handle any incomplete or corrupted tables.

                CSV file directory: {path_to_save_dir}
                JSON Save directory: {json_file_path}
            """),
            agent=agent,
            expected_output=dedent(f"""
                Table parsing task completed.
            """)
        )
    
    def user_prompt_handling_task(self, agent, user_query):
        return Task(
            description=dedent(f"""
                Process the user's query to refine and prepare it for efficient information retrieval.
                Use NLP techniques to analyze and understand the query, ensuring that it is properly formatted and structured for further processing by the system.
                
                User query: {user_query}
            """),
            agent=agent,
            expected_output=dedent(f"""
                User prompt processed.
            """)
        )
    
    def rag_integration_task(self, agent, user_query, text_file_path):
        return Task(
            description=dedent(f"""
                Integrate retrieval-augmented generation (RAG) to handle the user's complex query that requires information from multiple sources.
                Retrieve relevant data from the text file, then generate a comprehensive response to the query.
                
                User query: {user_query}
                Text file path: {text_file_path}
            """),
            agent=agent,
            expected_output=dedent(f"""
                RAG integration task completed.
            """)
        )
    
    def knowledge_graph_generation_task(self, agent, user_query, parsed_tables, path_to_save_dir):
        return Task(
            description=dedent(f"""
                Search the data in parsed_tables. Build a knowledge graph based on the results, save the knowledge graph to the save directory.
                user_query: {user_query}
                parsed_tables: {parsed_tables}
                Save directory: {path_to_save_dir}
            """),
            agent=agent,
            expected_output=dedent(f"""
                Knowledge graph generation task completed.
                Knowledge graph saved to: {path_to_save_dir}
            """)
        )