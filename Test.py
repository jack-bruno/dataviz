import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import joblib
from math import ceil

# Set the page layout to wide
st.set_page_config(layout="wide", page_icon="🌎", page_title="Project DataViz")

# Custom HTML for styling
st.markdown(
    """
   <style>
    /* Section principale */
    .main {
        background-color: #FFFFFF;  /* Blanc */
        padding: 10px;
    }

    /* Barre latérale */
    [data-testid="stSidebar"] {
        background: #A2D5F2;  /* Bleu ciel doux */
        color: #FFFFFF;  /* Texte blanc */
    }

    /* Paragraphes */
    p {
        color: #34495E;  /* Gris doux */
        font-family: 'Arial', sans-serif;
        font-size: 18px;
        font-weight: normal;
    }

    /* Boutons */
    .stButton button {
        background-color: #FF6F61;  /* Corail clair */
        color: #FFFFFF;  /* Texte blanc */
        font-family: 'Arial Black', sans-serif;
        border: none;
        padding: 10px;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background-color: #FFB6A1;  /* Corail pâle */
        color: #FFFFFF;  /* Texte blanc */
    }
    .stButton button:active {
        background-color: #E5533C;  /* Corail plus saturé */
        color: #FFFFFF;  /* Texte blanc */
    }

    /* Selectbox et sliders */
    .stSelectbox, .stSlider {
        color: #34495E;  /* Gris doux */
        font-family: 'Arial', sans-serif;
    }

    .stSelectbox div[role="listbox"] ul li, .stSlider .step {
        background: #DFF6F0;  /* Vert pastel clair pour les options */
        color: #34495E;  /* Gris doux */
    }

    .stSlider > div > div > div > div {
        background: #A2D5F2;  /* Bleu ciel clair pour les curseurs */
    }

    /* Boutons radio */
    input[type="radio"]:checked + div {
        background: #FF6F61 !important;  /* Corail clair pour les boutons activés */
        border-radius: 30px;
        color: #FFFFFF;  /* Texte blanc */
    }

    /* Champs d'entrée */
    input[type="text"], textarea {
        background-color: #FFFFFF;  /* Fond blanc */
        color: #34495E;  /* Texte gris doux */
        border: 1px solid #A2D5F2;  /* Bordure bleue pastel */
        border-radius: 5px;
        padding: 5px;
    }
    input[type="text"]:focus, textarea:focus {
        border-color: #FF6F61;  /* Bordure corail au focus */
        outline: none;
    }

    /* Checkbox */
    input[type="checkbox"]:checked + label {
        color: #FF6F61;  /* Corail clair pour les labels activés */
        font-weight: bold;
    }
</style>
    """,
    unsafe_allow_html=True
)

# Sidebar navigation
data = gpd.read_file("output_2.gpkg")
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Visualisation des données géospatiales", "Correlation Heatmap", "Graphiques Modèles"])

# Palette harmonisée pour les graphiques
main_bg_color = "#FFFFFF"  # Blanc
text_color = "#34495E"     # Gris doux
highlight_color = "#FF6F61"  # Corail clair
button_bg_color = "#A2D5F2"  # Bleu pastel
slider_color = "#A2D5F2"    # Bleu ciel doux

if page == "Visualisation des données géospatiales":
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Visualisation des données géospatiales")
    with col2:
        generate_button = st.button('Générer la carte')
    

    columns = ['arrêtés CAT NAT', 'Précipitation liquides', 'Températures', 'Evaporation', 'Evapotranspiration', 'Précipitations effectives', 'SWI']
    temps = ['dry', 'PRELIQ_MENS', 'T_MENS', 'EVAP_MENS', 'ETP_MENS', 'PE_MENS', 'SWI_MENS']
# Create a dictionary to map columns to temp values
    column_to_temp = dict(zip(columns, temps))
# Create the selectbox for columns
    selected_column = st.selectbox("Sélectionnez une colonne à visualiser :", columns , key="column_select")
# Get the corresponding temp value
    column = column_to_temp[selected_column]



    year = st.slider("Sélectionnez une année :", min_value=2019, max_value=2022, value=2019)
    map_placeholder = st.empty()

    if generate_button:
        try:
            temp = data[data.year == year]
            fig, ax = plt.subplots(figsize=(20, 10), facecolor=main_bg_color)
            temp.plot(column=column, cmap="YlOrBr", legend=True, ax=ax, edgecolor='none')
            plt.title(f"Carte thématique : {selected_column} pour l'année {year}", color=text_color)
            ax.set_facecolor(main_bg_color)
            plt.axis('off')
            map_placeholder.pyplot(fig)
        except Exception as e:
            st.error(f"Une erreur est survenue : {e}")

elif page == "Correlation Heatmap":
    st.title("Correlation Heatmap")
    temp = data[['dry', 'PRELIQ_MENS', 'T_MENS', 'EVAP_MENS', 'ETP_MENS', 'PE_MENS', 'SWI_MENS']]
    correlation_matrix = temp.corr()

    fig, ax = plt.subplots(figsize=(20, 10), facecolor=main_bg_color)
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", ax=ax, cbar_kws={'shrink': 0.75})
    plt.title("Linear Correlation Heatmap", color=text_color)
    ax.set_facecolor(main_bg_color)
    st.pyplot(fig)

elif page == "Graphiques Modèles":
    model = joblib.load('random_forest_classification_model.pkl')
    features = ['PRELIQ_MENS', 'T_MENS', 'EVAP_MENS', 'ETP_MENS', 'PE_MENS', 'SWI_MENS']
    col1, col2 = st.columns([3, 1])  # Largeur ajustée : 3/4 pour le titre et 1/4 pour le bouton
    with col1:
        codgeo = st.text_input('Entrez le code INSEE ', value='75056')
    with col2:
        predict_button = st.button('Prédire')  # Bouton aligné sur la droite

    st.title("Prédiction d'Arrêt de Sécheresse")
    #codgeo = st.text_input('Entrez le code INSEE ', value='75056')
    annee = st.slider('Sélectionnez l\'année', 2019, 2022, 2019)

    if predict_button :
        tempo = data[data.codgeo == codgeo]
        if len(tempo) > 0:
            tempo = tempo[tempo.year == annee]
            if len(tempo) > 0:
                tempo_features = tempo[['PRELIQ_MENS', 'T_MENS', 'EVAP_MENS', 'ETP_MENS', 'PE_MENS', 'SWI_MENS']]
                prediction = model.predict(tempo_features)
                tempo["temporaire"] = prediction

                
                probabilities = model.predict_proba(tempo_features)[0]
                classe = model.classes_

                st.subheader("Probabilités de survenance d'arrêt CATNAT:")
                fig, ax = plt.subplots()
                ax.pie(probabilities, labels=[f'Classe {classe[i]}: {probabilities[i]*100:.2f}%' for i in range(len(classe))], 
                       colors=[highlight_color, button_bg_color], startangle=90, wedgeprops=dict(width=0.3, edgecolor='w'))
                plt.axis('equal')
                st.pyplot(fig)

                st.subheader('Principales caractéristiques affectant la prédiction:')
                feature_importances = pd.Series(model.feature_importances_, index=features).sort_values(ascending=False)
                fig, ax = plt.subplots()
                ax.barh(feature_importances.index, feature_importances.values, color=[highlight_color, button_bg_color])
                ax.set_facecolor(main_bg_color)
                for spine in ax.spines.values():
                    spine.set_visible(False)
                ax.tick_params(left=False, bottom=False)
                st.pyplot(fig)

            else:
                st.warning("Aucune donnée pour cette année.")
        else:
            st.warning("Code INSEE non valide.")
