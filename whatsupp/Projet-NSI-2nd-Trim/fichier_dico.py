from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import sys
from bs4 import BeautifulSoup  # Importer BeautifulSoup pour parser le HTML

# Configurer le navigateur WebDriver
options = webdriver.ChromeOptions()
options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
chrome_driver_binary = "/usr/local/bin/chromedriver"
driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)

# Ouvrir la page de connexion
driver.get("https://chat.deepseek.com/sign_in")

# Entrer l'adresse e-mail
email_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Phone number / email address']")
email_input.send_keys("karl.rahuel@gmail.com")

# Entrer le mot de passe
password_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Password']")
password_input.send_keys("azertyuiop")

# Cocher la case à cocher
checkbox = driver.find_element(By.CSS_SELECTOR, ".ds-checkbox")
checkbox.click()

# Cliquer sur le bouton de connexion
login_button = driver.find_element(By.CSS_SELECTOR, "div.ds-button.ds-button--primary.ds-button--filled.ds-button--rect.ds-button--block.ds-button--l.ds-sign-up-form__register-button")
login_button.click()

# Attendre que la page charge complètement
time.sleep(2)  # Ajuster selon la vitesse de connexion et la structure de la page

# Aller à la page cible après la connexion
driver.get("https://chat.deepseek.com/sign_in")

# Remplir et envoyer le formulaire sur la page cible
dev_prompt = "Utilise le Markdown pour structurer le texte sans faire de zones de code sauf pour le cas ou la question demande un bout de code ou un code entier."
user_prompt = "Donne moi un exemple de code Python qui utilise la bibliothèque BeautifulSoup pour parser du HTML."
prompt = user_prompt + ". " + dev_prompt


textarea_input = driver.find_element(By.CSS_SELECTOR, "textarea#chat-input")
textarea_input.send_keys(prompt)
textarea_input.send_keys(Keys.RETURN)

# Vérifier en boucle que l'élément contenant la réponse apparaisse
response_payload = ""
old_response_payload = ""
timeout_timer = 0
max_timeout = 20  # Temps max d'attente
finish = True

def html_to_markdown(html):
    """ Convertit le HTML en Markdown """
    soup = BeautifulSoup(html, "html.parser")

    # Remplacer les <strong> par du texte en gras Markdown
    for bold in soup.find_all("strong"):
        bold.replace_with(f"**{bold.text}**")

    # Remplacer les <em> par du texte en italique Markdown
    for italic in soup.find_all("em"):
        italic.replace_with(f"*{italic.text}*")

    # Remplacer les <h1>, <h2>, <h3> par des titres Markdown
    for h1 in soup.find_all("h1"):
        h1.replace_with(f"# {h1.text}\n")
    for h2 in soup.find_all("h2"):
        h2.replace_with(f"## {h2.text}\n")
    for h3 in soup.find_all("h3"):
        h3.replace_with(f"### {h3.text}\n")

    # Traiter les listes ordonnées <ol> et <li> (avec <p> et <strong> à l'intérieur)
    for ol in soup.find_all("ol"):
        start = ol.get("start", 1)  # Numéro de départ de la liste (par défaut 1)
        for idx, li in enumerate(ol.find_all("li"), start=start):
            # Traiter les balises <p> et <strong> à l'intérieur de chaque <li>
            p_tags = li.find_all("p")
            li_text = ""
            for p in p_tags:
                # Ajouter un double saut de ligne pour chaque paragraphe <p>
                p_text = p.get_text("\n").strip()
                li_text += f"{p_text}\n\n"  # Ajouter un saut de ligne entre chaque paragraphe

            # Ajouter l'élément à la liste en format Markdown
            li.replace_with(f"{idx}. {li_text.strip()}")  # La numérotation est ajoutée en Markdown

    # Traiter les listes non ordonnées <ul>
    for ul in soup.find_all("ul"):
        for li in ul.find_all("li"):
            li.replace_with(f"- {li.text}\n")

    # Remplacer les balises <code> par du code inline Markdown
    for code in soup.find_all("code"):
        code.replace_with(f"`{code.text}`")

    # Remplacer les balises <pre> par des blocs de code Markdown
    for pre in soup.find_all("pre"):
        pre.replace_with(f"```\n{pre.text}\n```\n")

    # Ajouter un saut de ligne pour chaque <br>
    for br in soup.find_all("br"):
        br.replace_with("\n")

    # Ajouter des doubles sauts de ligne pour chaque <p> (paragraphes)
    for p in soup.find_all("p"):
        p.insert_before("\n\n")  # Ajout de double saut de ligne avant chaque <p>

    return soup.get_text().strip()


while finish:
    try:
        response_element = driver.find_element(By.CSS_SELECTOR, "div.ds-markdown.ds-markdown--block")
        html_content = response_element.get_attribute("innerHTML")  # Récupérer le HTML
        markdown_content = html_to_markdown(html_content).strip()  # Convertir en Markdown

        # Détecter uniquement la nouvelle partie ajoutée
        if markdown_content != old_response_payload:
            new_text = markdown_content[len(old_response_payload):]  # Extraire la partie ajoutée
            print(new_text, end="", flush=True)  # Affichage sans bufferisation
            old_response_payload = markdown_content  # Mise à jour
            timeout_timer = 0  # Réinitialisation du compteur si nouveau texte

        if timeout_timer > max_timeout:
            finish = False
        else:
            timeout_timer += 1

        time.sleep(0.01)

    except:
        continue  # Continuer en cas d'erreur (élément non trouvé, etc.)

print("\n")
# Fermer le navigateur
driver.quit()
