import os
import time
import json
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_experimental.sql import SQLDatabaseChain
from langchain_openai import ChatOpenAI, OpenAI
from database import setup_database, insert_db


load_dotenv()
# setup llm
llm = ChatOpenAI(model="gpt-4o", temperature=0)
llm_gpt3 = OpenAI(model="gpt-3.5-turbo-instruct", temperature=0)

UPLOAD_FOLDER = './resumes'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def test(catalog):
    db = setup_database(catalog)
    print('tables', json.dumps(db.get_context(), indent=4))

def analize(catalog):
    db = setup_database(catalog)

    db_chain = SQLDatabaseChain.from_llm(llm=llm_gpt3, db=db, use_query_checker=True, verbose=False)


    files = read_files()
    for file in files:
        if file.endswith('.pdf'):
            print('file', file)
            response = db_chain.invoke("Dame el valor máximo del primary key para la tabla principal del esquema")
            primary_key = response['result']
            print("primary_key", primary_key)

            response = analize_file(file, primary_key, db.get_context())
            response = response.replace("```sql", "")
            response = response.replace("```", "")
            response = response.replace("\\'", "")
            queries = response.split('\n;')

            for query in queries:
                if query:
                    insert_db(catalog, query)
                    time.sleep(1)

def analize_file(file, primary_key, db_schema):
    loader = PyPDFLoader(file)

    document_fragments = loader.load()

    content = ""
    for document in document_fragments:
        content += document.page_content

    if content == "":
        return ""
    else:
        messages = [
            {"role": "system", "content": "Eres experto en Recursos humanos y bases de datos postgresql"},
            {"role": "user", "content": [
                {"type": "text", "text": f"""
                        Tomando en cuenta el siguiente esquema de base de datos:
                        Schema: {db_schema}
    
                        Analiza el siguiente archivo:
                        Archivo: {content}
                        
                        Retorna un array de sentencias INSERT en orden correcto para almacenar la información requerida 
                        por el Schema no expliques el resultado, procedimiento ni recomendaciones.
                        
                        Este es el último valor de primary key para la tabla principal, incrementalo y utilizalo en el primer insert
                        PrimaryKey: {primary_key}
                        
                        Para los siguientes inserts asegurate utilizar siempre sentencias con ids dinámicos
                        
                        Double check the Postgres query above for common mistakes, including: 
                         - Using static ids for secondary inserts
                         - Dont use RETURNING INTO to get the id of the newly inserted registry 
                         - Dont use WITH to get the id of the newly inserted registry
                         - Confirm constraints and keys in every sentence and previews inserts
                         - Handling case sensitivity, e.g. using ILIKE instead of LIKE
                         - Ensuring the join columns are correct
                         - Casting values to the appropriate type
                         - Ensuring not violate not-null constraint
                         - Ignore inserts if table not exists
                         - Escape invalid characters like quotes or double quotes and others
                        
                        Rewrite the query here if there are any mistakes. If it looks good as it is, just reproduce the original query.
                    """}
            ]}
        ]

        ai_message = llm.invoke(messages)
        return ai_message.content


def read_files():
    files = []
    for dirpath, dirnames, filenames in os.walk("./resumes"):
        for filename in filenames:
            files.append(os.path.join(dirpath, filename))
    return files

