from app import  init_app
init_app()
import streamlit as st
from utils import get_assembly_ai_transcriber, get_weaviate_client
from streamlit_elements import elements, mui

wv_client = get_weaviate_client()

concept_to_search = st.text_input("concept_to_search")

if concept_to_search and st.button("search"):
    response = wv_client.query.get(
        class_name=st.secrets.weaviate.index_class,
        properties=["note", "title", "image"],
    ).with_near_text(content={
        "concepts": [concept_to_search]
    }).with_additional(["distance"]).do()


else:
    response = wv_client.query.get(
        class_name=st.secrets.weaviate.index_class,
        properties=["note", "title", "image"],
    ).do()

# st.write(response)
with elements("my_elements"):
    for ndx, data in enumerate(response["data"]["Get"][st.secrets.weaviate.index_class]):
        with mui.Card(key=f"card_{ndx}",
                      sx={"display": "flex",
                          "flexDirection": "column",
                          "borderRadius": 3,
                          "overflow": "hidden"},
                      elevation=1):
            mui.CardHeader(
                title=data["title"],
            )
            mui.CardMedia(
                component="img",
                height=194,
                image=data["image"],
            )

            with mui.CardContent(sx={"flex": 1}):
                mui.Typography(data["note"])
