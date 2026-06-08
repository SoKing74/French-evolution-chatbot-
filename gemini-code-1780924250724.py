import streamlit as st
import json
import os

# Fichier de mémoire partagé par les internautes
FICHIER_MEMOIRE = "memoire_collective.json"

def charger_memoire():
    if os.path.exists(FICHIER_MEMOIRE):
        try:
            with open(FICHIER_MEMOIRE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def sauvegarder_memoire(memoire):
    with open(FICHIER_MEMOIRE, "w", encoding="utf-8") as f:
        json.dump(memoire, f, ensure_ascii=False, indent=4)

# Initialisation de la mémoire et de l'état du bot
memoire = charger_memoire()

if "mot_en_attente" not in st.session_state:
    st.session_state.mot_en_attente = None

# ---- INTERFACE UTILISATEUR ----
st.title("🤖 Le Chatbot Évolutif Collectif")
st.write("Ce chatbot ne sait rien au départ. Parlez-lui pour construire sa mémoire !")

# Barre latérale pour les Conditions d'Utilisation
with st.sidebar:
    st.header("⚖️ Conditions d'Utilisation")
    st.markdown("""
    En participant à l'évolution de ce chatbot, vous acceptez les règles suivantes :
    * **Respect et bienveillance :** Ne lui apprenez pas d'insultes, de propos haineux ou inappropriés.
    * **Données publiques :** Tout ce que vous lui expliquez est stocké et peut être affiché aux autres utilisateurs. Ne partagez pas d'informations privées (nom, adresse, mots de passe).
    * **Modération :** Le créateur se réserve le droit de réinitialiser la mémoire en cas d'abus.
    """)
    
    st.write("---")
    if st.button("Afficher les mots connus"):
        st.subheader("🧠 Mots dans la base de données :")
        if memoire:
            for m, d in memoire.items():
                st.write(f"• **{m}** : {d}")
        else:
            st.write("Le bot est encore totalement vide.")

# Zone de discussion
message_user = st.text_input("Écrivez votre message ici :", key="input_user")

if message_user:
    message = message_user.lower().strip()
    reponse = ""

    # Cas 1 : Le bot attend une explication
    if st.session_state.mot_en_attente:
        mot_appris = st.session_state.mot_en_attente
        memoire[mot_appris] = message
        sauvegarder_memoire(memoire)
        reponse = f"Merci ! J'ai enregistré : **{mot_appris}** signifie maintenant *'{message}'* pour tout le monde."
        st.session_state.mot_en_attente = None # Réinitialisation

    # Cas 2 : Recherche de mots connus
    else:
        mots = message.split()
        trouve = False
        for mot in mots:
            if mot in memoire:
                reponse = f"Ah, je connais le mot **{mot}** ! On m'a appris que c'est : *{memoire[mot]}*"
                trouve = True
                break
        
        # Cas 3 : Le bot ne connaît rien, il demande à apprendre
        if not trouve:
            mots_interessants = [m for m in mots if len(m) > 3]
            if mots_interessants:
                ce_mot = mots_interessants[0]
                st.session_state.mot_en_attente = ce_mot
                reponse = f"Je ne connais pas le mot **{ce_mot}**. Pouvez-vous m'expliquer ce que c'est ?"
            else:
                reponse = "Je ne comprends pas vos mots... Essayez de faire une phrase plus longue !"

    # Affichage de la réponse du bot
    st.info(reponse)