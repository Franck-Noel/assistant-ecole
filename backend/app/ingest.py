import os
import chromadb
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

CHROMA_PATH = "../ecole_db"
DOCS_PATH = "../documents_ecole"

def indexer_les_pdfs():
    # Connexion à la base vectorielle
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_or_create_collection(name="infos_ecole")
    
    if not os.path.exists(DOCS_PATH):
        os.makedirs(DOCS_PATH)
        return

    # Configuration du découpage de texte
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200,separators=["\n\n", "\n", ".", " ", ""])
    
    for fichier in os.listdir(DOCS_PATH):
        if fichier.endswith(".pdf"):
            print(f"Indexation de : {fichier}")
            reader = PdfReader(os.path.join(DOCS_PATH, fichier))
            texte = "".join([p.extract_text() for p in reader.pages if p.extract_text()])
            chunks = splitter.split_text(texte)
            
            # Upsert permet de ne pas dupliquer si le fichier est déjà là
            for i, chunk in enumerate(chunks):
                collection.upsert(
                    documents=[chunk], 
                    ids=[f"{fichier}_{i}"]
                )
    print("✅ Base de connaissances mise à jour.")