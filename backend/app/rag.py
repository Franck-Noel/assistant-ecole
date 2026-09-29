import os
import chromadb
import google.generativeai as genai

# Configuration
CHROMA_PATH = "../ecole_db"
GENAI_API_KEY = os.getenv("GENAI_API_KEY")

# Initialisation Google Gemini
genai.configure(api_key=GENAI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-2.5-flash')

def obtenir_reponse(prompt, history, mode="Cloud (Gemini)"):
    """
    Version optimisée uniquement pour le Cloud
    """
    try:
        # 1. Recherche dans la base de données vectorielle (ChromaDB)
        client = chromadb.PersistentClient(path=CHROMA_PATH)
        collection = client.get_collection(name="infos_ecole")
        
        results = collection.query(query_texts=[prompt], n_results=4)
        context = "\n\n".join(results.get("documents", [[]])[0])

        # 2. Construction du Prompt Système
        system_prompt = f"""Tu es l'assistant officiel de l'ENSEA d'Abidjan. 
        Utilise exclusivement les informations suivantes pour répondre :
        {context}
        
        Si l'information n'est pas présente, oriente l'utilisateur vers le secrétariat.
        Réponds de manière chaleureuse et professionnelle."""

        # 3. Appel à Gemini
        # On peut inclure un résumé de l'historique pour la mémoire
        full_query = f"{system_prompt}\n\nQuestion de l'étudiant : {prompt}"
        
        response = gemini_model.generate_content(full_query)
        return response.text

    except Exception as e:
        if "429" in str(e):
            return "⚠️ Limite de requêtes atteinte (Quota Google). Réessayez dans une minute."
        return f"Erreur Cloud : {str(e)}"