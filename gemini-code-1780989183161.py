st.write("---")
st.subheader("🛠️ Zone Admin")
# Mot de passe simple pour éviter que n'importe quel internaute efface tout
mot_de_passe = st.text_input("Mot de passe admin :", type="password")

if mot_de_passe == "mon_code_secret": # Change ce mot de passe
    if st.button("🔴 Réinitialiser la mémoire"):
        memoire = {}
        sauvegarder_memoire(memoire)
        st.success("La mémoire a été vidée avec succès !")
        st.rerun()