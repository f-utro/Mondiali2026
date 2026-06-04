# import streamlit as st

# st.set_page_config(page_title="Fanta Mondiali Community 🏆", page_icon="⚽", layout="centered")

# # --- TITOLO PRINCIPALE ---
# st.title("🏆 Il Gioco dei Mondiali ⚽")
# st.write("Benvenuto nella piattaforma ufficiale dei pronostici della nostra community!")

# st.markdown("---")

# # --- GUIDA VISIVA ALLA NAVIGAZIONE (A prova di smartphone) ---
# st.subheader("📍 Come Giocare?")

# # Box informativo per spiegare dove trovare il menu da mobile e desktop
# st.info("""
# 🧭 **IMPORTANTE DA MOBILE:** Se sei da smartphone, clicca sulla **freccetta in alto a sinistra ( 🧭 o ☰ )** per aprire il menu laterale e viaggiare tra le pagine!
# """)

# col1, col2 = st.columns(2)

# with col1:
#     st.markdown("""
#     ### 📊 1. Fase a Gironi
#     * **Dove:** Nel menu a sinistra ➡️ **1_Gironi**
#     * **Cos'è:** Indovina chi arriva 1° e 2° in ogni girone.
#     * **⏰ SCADENZA:** Puoi votare o modificare solo fino al fischio d'inizio della prima partita del Mondiale! Poi la pagina verrà blindata. 🔒
#     """)

# with col2:
#     st.markdown("""
#     ### 🔥 2. Schedina Live (1X2)
#     * **Dove:** Nel menu a sinistra ➡️ **2_Schedina_Live**
#     * **Cos'è:** Le sfide flash giorno per giorno. Pronostica l'esito dei big match.
#     * **Quando:** Sempre attiva durante tutto il torneo, partita per partita! ⏱️
#     """)

# st.markdown("---")

# # --- FOCUS SULLA FASE AD ELIMINAZIONE DIRETTA ---
# st.subheader("⚡ Prossimamente: Fase a Eliminazione Diretta")
# st.warning("""
# 🏁 **Cosa succede dopo i gironi?** 
# Non appena si conosceranno le squadre qualificate ufficiali, sbloccheremo una nuova pagina con il **Tabellone dei Playoff (dagli Ottavi alla Finalissima)**! 

# Lì il gioco si farà serio: dovrai decretare chi passa il turno fino ad indovinare il Campione del Mondo. Più andrai avanti nel tabellone, più i punti accumulati saranno pesanti per la classifica finale!
# """)

# st.markdown("---")

# # --- REGOLAMENTO E PUNTEGGI ---
# st.subheader("🎯 Sistema di Punteggio")

# st.markdown("""
# Non c'è nessun obbligo di partecipazione a tutte le fasi! Puoi decidere di giocare solo i Gironi o solo le Schedine Live. **Tuttavia, chi partecipa a ogni fase del gioco accumulerà molti più punti per la classifica generale!**

# Ecco come si fanno i punti in questa prima fase:

# * **🥇 Fase a Gironi:**
#   * **+3 Punti** per ogni squadra azzeccata nella *posizione esatta* (es. avevi messo Italia 1ª ed finisce 1ª).
#   * **+1 Punto** se indovini la squadra che passa il turno ma nella *posizione sbagliata* (es. avevi messo Francia 1ª ma si qualifica come 2ª).

# * **⏱️ Schedina Live (1X2):**
#   * **+1 Punto** per ogni segno esatto (1, X o 2) indovinato sulle partite standard.
#   * **+3 Punti (Bonus)** se indovini il segno esatto di un **Big Match** contrassegnato in bacheca!
# """)

# # --- SEZIONE CLASSIFICA RAPIDA ---
# st.markdown("---")
# st.subheader("🏆 La Classifica è attiva!")
# st.write("Vuoi vedere chi sta dominando la community? Vai alla pagina ➡️ **Classifica** nel menu laterale!")

# st.success("💡 Fai click in alto a sinistra, seleziona 'Gironi' e piazza i tuoi primi pronostici prima che scada il tempo!")

import streamlit as st

st.set_page_config(
    page_title="Mundial&Me  - Home 🏆",
    page_icon="favicon.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Nasconde il menu di Streamlit (che contiene il link GitHub e il profilo)
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)



# --- FORZATURA SFONDO VINTAGE SCHEDINA ROSA ---
st.markdown("""
    <style>
    /* 1. Sfondo Rosa Vintage */
    .stApp {
        background-color: #f9ebdf !important;
    }

    /* 2. Forza i testi generici in Nero Scuro, escludendo i bottoni */
    .stApp p, .stApp span, .stApp li, .stApp label, .stApp h1, .stApp h2, .stApp h3, .stApp h4 {
        color: #111111 !important;
    }

    /* 3. BLINDATURA BOTTONI (Risolve il problema su Mobile) */
    /* Bottone 1: APRI SCHEDINA GIRONI (Sfondo Antracite Scuro, Scritta Bianca) */
    div.stButton > button:first-child, [data-testid="stBaseButton-secondary"] {
        background-color: #1e2229 !important;
        color: #ffffff !important;
        border: 1px solid #1e2229 !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        font-weight: bold !important;
        width: 100% !important; /* Forza la larghezza piena comoda su mobile */
        display: block !important;
    }
    
    /* Assicuriamoci che il testo dentro il bottone rimanga tassativamente bianco */
    div.stButton > button p, div.stButton > button span {
        color: #ffffff !important;
    }

    /* Effetto al passaggio del dito/mouse sui bottoni per dare feedback */
    div.stButton > button:hover {
        background-color: #009933 !important; /* Diventa verde TotoJuve al passaggio! */
        color: #ffffff !important;
        border-color: #009933 !important;
    }

    /* 4. Box interni dei match sempre bianchi puliti */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff !important;
        border-radius: 8px !important;
        padding: 15px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    }

    /* 5. Forza la chiusura della barra laterale */
    @media (max-width: 768px) {
        [data-testid="stSidebar"] {
            margin-left: -21rem;
        }
    }
    </style>
""", unsafe_allow_html=True)



# --- HEADER VINTAGE TOTOCALCIO ---
# col_logo, col_titolo = st.columns([1, 4])
# with col_logo:
#     # st.markdown("""
#     #     <div style='border: 3px solid #009933; padding: 10px; text-align: center; border-radius: 5px; background-color: #f0fbf2;'>
#     #         <span style='color: #009933; font-weight: bold; font-size: 14px; font-family: sans-serif;'>CONCORSO</span><br>
#     #         <span style='color: #009933; font-weight: bold; font-size: 32px; line-height: 32px; font-family: monospace;'>J&M</span>
#     #     </div>
#     # """, unsafe_allow_html=True)
#      st.image("Mundial&Me Logo Nero.png", use_container_width=True)
    
# with col_titolo:
#     st.markdown("""
#         <div style='text-align: center;'>
#             <h1 style='font-family: "Brush Script MT", cursive, sans-serif; font-size: 58px; margin: 0; font-style: italic; line-height: 1.1;'>
#                 <span style='color: #009933;'>Toto</span><span style='color: #111111;'>Juve&Me</span>
#             </h1>
#             <p style='color: #555555; font-weight: bold; font-family: monospace; letter-spacing: 3px; margin: 0; font-size: 12px;'>\" AL SERVIZIO DELLO SPORT BIANCONERO \"</p>
#         </div>
#     """, unsafe_allow_html=True)

# st.markdown("<hr style='border: 1px solid #009933;'>", unsafe_allow_html=True)
# --- BRANDING HEADER ---
# Creiamo 3 colonne: quella centrale conterrà il logo, le laterali gestiscono lo spazio
col_left, col_center, col_right = st.columns([2, 1, 2])

with col_center:
    # Usiamo il logo "Nero" perché contiene già il nome del brand
    st.image("Mundial&Me Logo Nero.png", use_container_width=True)

# Separatore grafico che riprende il colore verde del tema
st.markdown("<hr style='border: 1px solid #009933; margin: 15px 0;'>", unsafe_allow_html=True)

# --- CORPO DELLA HOME PAGE ---
st.markdown("### 🌟 Benvenuto nel Gioco Pronostici Ufficiale della Community!")
st.write(
    "Metti alla prova la tua competenza calcistica per questo Mondiale. "
    "Compila i tuoi pannelli, sfida gli altri membri del canale e scala la classifica generale! 🚀"
)

st.markdown("<br>", unsafe_allow_html=True)

# Layout a due colonne per dividere le istruzioni dalle sezioni di gioco
col_info, col_navigazione = st.columns([5, 4])

with col_info:
    with st.container(border=True):
        st.markdown("### 📜 REGOLAMENTO E ATTRIBUZIONE PUNTEGGI")
        st.write(
        "Per garantire la massima trasparenza, ecco come vengono calcolati i punti "
        "durante tutto il corso del torneo, dalla fase a gironi fino alla finalissima. "
        "Ricorda: nella fase a eliminazione diretta ti verrà chiesto di pronosticare l'intero tabellone! 🚀"
         )
        # --- FASE A GIRONI ---
        st.markdown("#### ⚽ 1. FASE A GIRONI")
        st.markdown(
            """
        * **Esito Esatto (1X2)**: **+1 Punto** ➡️ Se indovini chi vince o il pareggio.
        * **Risultato Esatto**: **+3 Punti** ➡️ Se indovini il risultato esatto (es. 2-1, 1-0).
        * **Combinazione Perfetta (1X2 + Risultato)**: **+4 Punti** totali se li indovini entrambi per la singola partita.
        """
        )

        # --- FASE A ELIMINAZIONE DIRETTA ---
        st.markdown("#### 🏆 2. FASE A ELIMINAZIONE DIRETTA (Fino alla Finale)")
        st.write(
            "Prima dell'inizio degli ottavi di finale, dovrai compilare l'intero tabellone cartellone "
            "pronosticando il cammino completo delle squadre fino all'assegnazione della coppa. I punti vengono assegnati così:"
        )
        st.markdown(
            """
        * **Passaggio Turno Indovinato**: **+2 Punti** ➡️ Per ogni Passaggio del turno indovinato (Ottavi ➡️ Quarti ➡️ Semifinale).
        * **Finalista Indovinata**: **+4 Punti** ➡️ Per ogni squadra finalista indovinata.
        * **Vincitore Torneo**: **+7 Punti** ➡️ Se indovini la squadra che solleverà il trofeo.
        """
        )

        # --- BONUS COMMUNITY ---
        st.markdown("#### 💎 3. BONUS EXTRA CHIUSURA GIRONI")
        st.markdown(
            """
        * **Podio Girone Esatto**: **+2 Punti** ➡️ Se indovini l'esatto ordine di arrivo delle prime due classificate del girone.
        """
        )

        st.info("💡 *Nota: Tutti i pronostici della fase eliminatoria sono 'fissi' una volta convalidati prima degli ottavi. Segui l'avanzamento e la spinta della tua schedina nella dashboard!*")

with col_navigazione:
    st.markdown("#### 🚀 ACCESSO RAPIDO AI VOTI")
    st.write("Clicca direttamente qui sotto per entrare nelle schede di gioco senza usare il menu laterale:")
    
    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
    
    # Pulsante gigante per la Fase a Gironi
    if st.button("📊 APRI SCHEDINA GIRONI", use_container_width=True, type="secondary"):
        st.switch_page("pages/1_Gironi.py")
        
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    
    # Pulsante gigante per la Schedina Live (Totocalcio Style)
    if st.button("🎰 APRI TOTOCALCIO LIVE", use_container_width=True, type="primary"):
        st.switch_page("pages/2_Schedina_Live.py")
        
    st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
    st.caption("📱 **Sei da Mobile?** I pulsanti qui sopra sono fatti apposta per saltare subito al voto dal tuo smartphone!")

st.markdown("---")
st.caption("✨ Sviluppato con passione per la community Juv&me. Che il miglior tipster vinca!")