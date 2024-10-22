import streamlit as st


# Adicionar a imagem centralizada no início da página
st.markdown("""
<div style="text-align: center;">
    <img src="https://i.imgur.com/Ti4ILVw.png" style="width: 20%;"/>
</div>
            

""", unsafe_allow_html=True)


st.divider()




st.page_link("pages/ad_selector.py", label="Criar lista de Seleção 🔗", icon=":material/list:")
