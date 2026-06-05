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
# --- BRANDING HEADER ---
# --- BRANDING HEADER ---
col_left, col_center, col_right = st.columns([1, 2, 1])
with col_center:
    st.image("Mundial&Me Logo Nero.png", use_container_width=True)
    
    # CSS per icone professionali
    st.markdown("""
    <style>
        .social-icons-wrapper { 
            display: flex; justify-content: center; gap: 20px; margin: 10px 0 20px 0; 
        }
        .icon-link { 
            display: flex; align-items: center; justify-content: center;
            width: 30px; height: 30px; transition: transform 0.2s;
        }
        .icon-link:hover { transform: scale(1.15); }
        .icon-link svg { width: 100%; height: 100%; }
    </style>
    
    <div class="social-icons-wrapper">
        <a href="https://t.me/+SAwDw59_ym7swlzf" class="icon-link" target="_blank" rel="noopener noreferrer">
            <svg viewBox="0 0 24 24" fill="#0088cc"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-1.46-.96-2.28-1.56-3.7-2.52-1.63-1.1-.57-1.71.35-2.67.24-.25 4.39-4.01 4.47-4.35.01-.04.02-.2-.09-.28-.11-.08-.26-.05-.37-.03-.16.04-2.73 1.74-7.72 5.09-.72.48-1.38.71-1.96.69-.64-.02-1.87-.36-2.79-.66-1.28-.42-2.31-.64-2.23-1.35.03-.27.4-.54 1.1-.82 6.84-2.97 11.45-4.96 13.84-5.99 6.59-2.82 7.96-3.32 8.87-3.34.2 0 .64.05.93.28.24.19.3.42.33.59.03.18.06.63.02 1.19z"/></svg>
        </a>
        <a href="https://twitch.tv/juvandmeofficial" class="icon-link" target="_blank" rel="noopener noreferrer">
            <svg viewBox="0 0 24 24" fill="#9146ff"><path d="M11.57 2.14L9 4.71H4v11.57h4v3.43h2.57l2.57-3.43h2.57l5.14-5.14V2.14h-9.43zM16.29 13.71h-2.57l-2.57 3.43v-3.43H6.43V6.43h9.86v7.28z"/></svg>
        </a>
        <a href="https://www.youtube.com/@juvme8305" class="icon-link" target="_blank" rel="noopener noreferrer">
            <svg viewBox="0 0 24 24" fill="#ff0000"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.377.505 9.377.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
        </a>
        <a href="https://x.com/juvandme" class="icon-link" target="_blank" rel="noopener noreferrer">
            <svg viewBox="0 0 24 24" fill="#000000"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
        </a>
    </div>
""", unsafe_allow_html=True)

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
    if st.button("🎰 APRI TOTO&ME LIVE", use_container_width=True, type="primary"):
        st.switch_page("pages/2_Schedina_Live.py")
        
    st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
    st.caption("📱 **Sei da Mobile?** I pulsanti qui sopra sono fatti apposta per saltare subito al voto dal tuo smartphone!")

st.markdown("---")
st.caption("✨ Sviluppato con passione per la community Juv&me. Che il miglior tipster vinca!")