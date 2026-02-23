import requests
# Ajout de 'request' à la liste des imports
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')

# --- Déposez votre code à partir d'ici : ---

# Ajout de methods=["GET", "POST"] pour autoriser la réception du formulaire
@app.route("/contact", methods=["GET", "POST"])
def MaPremiereAPI():
    # Si l'utilisateur a cliqué sur "Envoyer" (Méthode POST)
    if request.method == "POST":
        prenom = request.form.get("prenom")
        nom = request.form.get("nom")
        message = request.form.get("message")
        
        # On ouvre un fichier (il sera créé automatiquement s'il n'existe pas)
        with open("messages.txt", "a", encoding="utf-8") as fichier:
            fichier.write(f"De: {prenom} {nom}\n")
            fichier.write(f"Message: {message}\n")
            fichier.write("-" * 30 + "\n")
            
        # Message de confirmation basique affiché à l'écran
        return "Merci ! Votre message a bien été enregistré."
        
    # Si l'utilisateur arrive simplement sur la page (Méthode GET)
    return render_template('contact.html')

# --- Requête API pour météo --- 

@app.get("/paris")
def api_paris():
    url = "https://api.open-meteo.com/v1/forecast?latitude=48.8566&longitude=2.3522&hourly=temperature_2m"
    response = requests.get(url)
    data = response.json()

    times = data.get("hourly", {}).get("time", [])
    temps = data.get("hourly", {}).get("temperature_2m", [])

    n = min(len(times), len(temps))
    result = [
        {"datetime": times[i], "temperature_c": temps[i]}
        for i in range(n)
    ]

    return jsonify(result)

# --- Requête api pour graphique --- 

@app.route("/rapport")
def mongraphique():
    return render_template("graphique.html")

# --- Requête api pour histogramme ---

@app.route("/histogramme")
def monhistogramme():
    return render_template("histogramme.html")

@app.route("/atelier")
def atelier():
    return render_template("atelier.html")

# Ne rien mettre après ce commentaire
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
