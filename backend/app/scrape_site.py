import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

BASE_URL = "https://ensea.ed.ci/"
PAGES = [
    "/",
    "/ENSEA",
    "/FORMATION INITIALE",
    "/FORMATION CONTINUE",
    "/FORMATION DOCTORALE",
]

OUTPUT_DIR = "../../documents_ecole"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "site_ecole.txt")

def nettoyer_html(soup):
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()
    return soup.get_text(separator="\n")

def scraper():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    contenu_total = []

    for page in PAGES:
        url = urljoin(BASE_URL, page)
        print(f"🔎 Scraping : {url}")

        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        texte = nettoyer_html(soup)
        texte = "\n".join(l.strip() for l in texte.splitlines() if len(l.strip()) > 30)

        contenu_total.append(f"\n===== PAGE : {url} =====\n")
        contenu_total.append(texte)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(contenu_total))

    print("✅ Données du site sauvegardées.")

if __name__ == "__main__":
    scraper()
