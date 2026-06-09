st.write("---")
st.subheader("🛠️ Zone Admin")

mot_de_passe = st.text_input("Mot de passe admin :", type="password")

if mot_de_passe == "prk": 
    if st.button("🔴 Réinitialiser la mémoire"):
        memoire = {}
        sauvegarder_memoire(memoire)
        st.success("La mémoire a été vidée avec succès !")
        st.rerun()
