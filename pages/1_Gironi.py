import streamlit as st
import pandas as pd
import os
from datetime import datetime
import json
import os
import gspread

# URL univoco del tuo foglio Google di TotoJuve&Me
URL_FOGLIO = "https://docs.google.com/spreadsheets/d/1eplWbGsR3lpAPawatIBuSp5ts20K4Nn-_QUqvE2Md-g/edit"

# Logica di autenticazione ibrida (Locale JSON / Cloud Secrets)
path_json_locale = "credenziali_google.json"
# Definiamo i permessi (Scopes) necessari per Google
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

@st.cache_resource
def inizializza_gspread():
    if os.path.exists(path_json_locale):
        return gspread.service_account(filename=path_json_locale, scopes=SCOPES)
    else:
        # Recuperiamo la chiave dai secrets ed eseguiamo una pulizia approfondita
        pkey = st.secrets["private_key"]
        
        # Se la chiave è su più righe, ricostruiamo la stringa con i \n espliciti richiesti dall'API di Google
        if "\n" in pkey and "\\n" not in pkey:
            pkey = pkey.replace("\n", "\\n")
            
        credenziali_cloud = {
            "type": "service_account",
            "project_id": st.secrets["project_id"],
            "private_key_id": st.secrets["private_key_id"],
            "private_key": pkey.replace("\\n", "\n"), # Ripristina i line-break corretti per gspread
            "client_email": st.secrets["client_email"],
            "client_id": st.secrets["client_id"],
            "auth_uri": st.secrets["auth_uri"],
            "token_uri": st.secrets["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["client_x509_cert_url"]
        }
        return gspread.service_account_from_dict(credenziali_cloud, scopes=SCOPES)
    
# Ottieni il client client autenticato
gc = inizializza_gspread()
# Apri il foglio principale
sh = gc.open_by_url(URL_FOGLIO)

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Mundial&Me Live -Fase a Gironi 🏆", page_icon="🏆", layout="wide", initial_sidebar_state="collapsed")


# --- FILE DATABASE ---
GIRONI_FILE = "predizioni_gironi.csv"
if not os.path.exists(GIRONI_FILE):
    pd.DataFrame(columns=["Data", "Utente_Telegram", "Girone", "Posizione", "Squadra_Pronosticata"]).to_csv(GIRONI_FILE, index=False)

# --- DIZIONARIO CODICI ISO DELLE BANDIERE HD ---
FLAG_CODES = {
    # Gruppo A
    "Messico": "mx", "Sudafrica": "za", "Corea del Sud": "kr", "Rep. Ceca": "cz",
    # Gruppo B
    "Canada": "ca", "Bosnia ed Erzegovina": "ba", "Qatar": "qa", "Svizzera": "ch",
    # Gruppo C
    "Brasile": "br", "Marocco": "ma", "Haiti": "ht", "Scozia": "gb-sct",
    # Gruppo D
    "Stati Uniti": "us", "Paraguay": "py", "Australia": "au", "Turchia": "tr",
    # Gruppo E
    "Germania": "de", "Curaçao": "cw", "Costa d'Avorio": "ci", "Ecuador": "ec",
    # Gruppo F
    "Olanda": "nl", "Giappone": "jp", "Svezia": "se", "Tunisia": "tn",
    # Gruppo G
    "Belgio": "be", "Egitto": "eg", "Iran": "ir", "Nuova Zelanda": "nz",
    # Gruppo H
    "Spagna": "es", "Capo Verde": "cv", "Arabia Saudita": "sa", "Uruguay": "uy",
    # Gruppo I
    "Francia": "fr", "Senegal": "sn", "Iraq": "iq", "Norvegia": "no",
    # Gruppo J
    "Argentina": "ar", "Algeria": "dz", "Austria": "at", "Giordania": "jo",
    # Gruppo K
    "Portogallo": "pt", "Rep. Dem. del Congo": "cd", "Uzbekistan": "uz", "Colombia": "co",
    # Gruppo L
    "Inghilterra": "gb-eng", "Croazia": "hr", "Ghana": "gh", "Panama": "pa"
}

def get_flag_url(team_name):
    code = FLAG_CODES.get(team_name)
    if not code:
        return "https://flagcdn.com/w80/un.png"
    return f"https://flagcdn.com/w80/{code}.png"

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
# --- STILE CSS COMPLETO (Design Premium TotoJuve) ---
st.markdown("""
    <style>
    .stApp { background-color: #f9ebdf !important; }
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp p, .stApp span, .stApp label, .stApp li {
        color: #111111 !important;
    }
    
    /* Box Elenco Squadre Mini-Card */
    .team-row {
        display: flex;
        align-items: center;
        gap: 12px;
        background: #ffffff;
        padding: 8px 14px;
        border-radius: 8px;
        margin-bottom: 6px;
        border: 1px solid #e9d9cb;
    }

    /* Badge dei gironi in alto */
    .badge-container { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 15px; }
    .girone-badge { 
        padding: 6px 12px; border-radius: 20px; font-weight: bold; font-size: 13px;
        background-color: #ffffff; border: 1px solid #ccc; color: #444444;
    }
    .girone-badge.active { background-color: #009933 !important; color: #ffffff !important; border-color: #009933 !important; }
    .girone-badge.done { background-color: #e2f0d9 !important; border-color: #009933 !important; color: #009933 !important; }

    /* Selectbox moderne */
    div[data-baseweb="select"] > div { background-color: #ffffff !important; color: #111111 !important; border: 1px solid #009933 !important; border-radius: 8px !important;}

    /* Contenitore principale a scheda */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff !important; border-radius: 16px !important;
        padding: 22px !important; box-shadow: 0 4px 15px rgba(0,0,0,0.04) !important;
    }

    /* Display Tabellino Grafico Qualificate */
    .podium-container {
        display: flex;
        flex-direction: row;
        justify-content: center;
        gap: 15px;
        background: #ffffff;
        padding: 12px;
        border-radius: 12px;
        border: 1px solid #ebdccf;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.02);
        margin-top: 5px;
    }
    .podium-slot {
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        background: #fdf8f4;
        padding: 10px 14px;
        border-radius: 8px;
        border: 1px solid #e9d9cb;
    }
    .podium-slot.empty {
        background: #fafafa;
        border: 1px dashed #cccccc;
        color: #888888;
        font-style: italic;
    }

    /* Pulsantiera */
    div.stButton > button {
        background-color: #1e2229 !important; color: #ffffff !important; border-radius: 8px !important;
        padding: 12px 20px !important; font-weight: bold !important; width: 100% !important; border: none !important;
        box-shadow: 0 3px 6px rgba(0,0,0,0.1) !important;
    }
    div.stButton > button p, div.stButton > button span { color: #ffffff !important; }
    div.stButton > button:hover { background-color: #009933 !important; }

    @media (max-width: 768px) { 
        [data-testid="stSidebar"] { margin-left: -21rem; }
        .podium-container { flex-direction: column; gap: 8px; }
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER TOTOJUVE ---
# Rimuovi il vecchio blocco 'with col_logo' e 'with col_titolo' 
# e sostituiscilo con questo:

# Aumentiamo la proporzione del logo e centriamo il contenuto
# col1, col2 = st.columns([1, 4]) 

# with col1:
#     st.image("Mundial&Me Logo Nero.png", use_container_width=True)

# with col2:
#     st.markdown("""
#         <div style="margin-top: 20px;">
#             <h1 style="margin: 0; font-size: 28px;">Mundial&Me</h1>
#             <p style="margin: 0; color: #555;">Il portale ufficiale dei pronostici</p>
#         </div>
#     """, unsafe_allow_html=True)

# st.markdown("<hr style='margin-top: 10px; margin-bottom: 20px; border: 1px solid #009933;'>", unsafe_allow_html=True)

# Proporzione [2, 1, 2] -> La colonna centrale è 1/5 della larghezza totale
# col_left, col_center, col_right = st.columns([2, 1, 2])

# with col_center:
#     st.image("Mundial&Me Logo Nero.png", use_container_width=True)

def reset_al_main():
    # Riporta l'utente alla vista principale "GIOCA"
    st.session_state.pagina_corrente = "GIOCA"
    # Rimuove eventuali selezioni attive (es. se era nel form di una partita)
    if "partita_attiva" in st.session_state:
        del st.session_state.partita_attiva
    # Reset della ricevuta se necessario
    st.session_state.mostra_ricevuta = False
    # Ricarica la pagina per applicare il reset
    st.rerun()
# --- BRANDING HEADER ---
# --- HEADER CON ICONE STANDARD E LOGO CLICCABILE ---

# 1. Creiamo un contenitore centrale
col_left, col_center, col_right = st.columns([1, 2, 1])

with col_center:
    # Logo cliccabile
    st.markdown(
        """
        <div style="text-align: center;">
            <a href="https://mundialandme.streamlit.app/" target="_self">
                <img src="https://raw.githubusercontent.com/f-utro/Mondiali2026/main/Mundial&Me%20Logo%20Nero.png" width="200">
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Spazio tra logo e icone
    st.write(" ")
    
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
# --- LOGIN UTENTE ---
telegram_user = st.text_input("💬 Inserisci il tuo Username Telegram per giocare:", placeholder="@tuo_nickname")

if telegram_user:
    # squadre_gironi = {
    #     "A": ["Messico", "Sudafrica", "Corea del Sud", "Rep. Ceca"],
    #     "B": ["Canada", "Bosnia", "Qatar", "Svizzera"],
    #     "C": ["Germania", "Curaçao", "Costa d'Avorio", "Ecuador"],
    #     "D": ["Stati Uniti", "Paraguay", "Haiti", "Scozia"],
    #     "E": ["Brasile", "Marocco", "Australia", "Turchia"],
    #     "F": ["Paesi Bassi", "Giappone", "Svezia", "Tunisia"],
    #     "G": ["Belgio", "Egitto", "Iran", "Nuova Zelanda"],
    #     "H": ["Spagna", "Capo Verde", "Arabia Saudita", "Uruguay"]
    # }
    squadre_gironi = {
    "Gruppo A": ["Messico", "Sudafrica", "Corea del Sud", "Rep. Ceca"],
    "Gruppo B": ["Canada", "Bosnia ed Erzegovina", "Qatar", "Svizzera"],
    "Gruppo C": ["Brasile", "Marocco", "Haiti", "Scozia"],
    "Gruppo D": ["Stati Uniti", "Paraguay", "Australia", "Turchia"],
    "Gruppo E": ["Germania", "Curaçao", "Costa d'Avorio", "Ecuador"],
    "Gruppo F": ["Olanda", "Giappone", "Svezia", "Tunisia"],
    "Gruppo G": ["Belgio", "Egitto", "Iran", "Nuova Zelanda"],
    "Gruppo H": ["Spagna", "Capo Verde", "Arabia Saudita", "Uruguay"],
    "Gruppo I": ["Francia", "Senegal", "Iraq", "Norvegia"],
    "Gruppo J": ["Argentina", "Algeria", "Austria", "Giordania"],
    "Gruppo K": ["Portogallo", "Rep. Dem. del Congo", "Uzbekistan", "Colombia"],
    "Gruppo L": ["Inghilterra", "Croazia", "Ghana", "Panama"]
}
    
    lista_lettere = list(squadre_gironi.keys())

    if "current_index" not in st.session_state:
        st.session_state.current_index = 0
    if "scelte_salvate" not in st.session_state:
        st.session_state.scelte_salvate = {let: {"1": "-", "2": "-"} for let in lista_lettere}

    # --- BADGE DI AVANZAMENTO IN ALTO ---
    badge_html = '<div class="badge-container">'
    for idx, let in enumerate(lista_lettere):
        scelte = st.session_state.scelte_salvate[let]
        status_class = ""
        icon = "⏳"
        if idx == st.session_state.current_index:
            status_class = "active"
            icon = "🎯"
        elif scelte["1"] != "-" and scelte["2"] != "-":
            status_class = "done"
            icon = "✅"
        badge_html += f'<div class="girone-badge {status_class}">{let} {icon}</div>'
    badge_html += '</div>'
    st.markdown(badge_html, unsafe_allow_html=True)

    # --- SCHERMATA DI COMPILAZIONE ---
    if st.session_state.current_index < len(lista_lettere):
        lettera_corrente = lista_lettere[st.session_state.current_index]
        liste_squadre = squadre_gironi[lettera_corrente]

        with st.container(border=True):
            st.markdown(f"""
                <div style='text-align: center; margin-bottom: 15px;'>
                    <h2 style='color: #009933; margin: 0; font-family: sans-serif; font-weight: 800; letter-spacing: 1px;'>
                        🏆 {lettera_corrente}
                    </h2>
                    <p style='color: #666666; font-size: 12px; margin: 2px 0 0 0; font-weight: bold; text-transform: uppercase;'>Scegli le due squadre che passano il turno</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Griglia nazioni con bandiere grafiche reali
            cols_squadre = st.columns(4)
            for i, sq in enumerate(liste_squadre):
                with cols_squadre[i]:
                    st.markdown(f"""
                        <div class="team-row">
                            <img src="{get_flag_url(sq)}" width="30" style="border-radius:3px; box-shadow: 1px 1px 3px rgba(0,0,0,0.15)">
                            <span style="font-weight:bold; font-size:14px;">{sq}</span>
                        </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Caricamento e gestione selectbox
            default_1 = st.session_state.scelte_salvate[lettera_corrente]["1"]
            idx_default_1 = liste_squadre.index(default_1) + 1 if default_1 in liste_squadre else 0

            opzioni_1 = ["-"] + liste_squadre
            p1 = st.selectbox("🥇 Scegli la 1ª Classificata (Vincitrice):", opzioni_1, index=idx_default_1, key=f"select_1_{lettera_corrente}")
            
            opzioni_2 = ["-"] + [sq for sq in liste_squadre if sq != p1]
            default_2 = st.session_state.scelte_salvate[lettera_corrente]["2"]
            idx_default_2 = opzioni_2.index(default_2) if default_2 in opzioni_2 else 0
            
            p2 = st.selectbox("🥈 Scegli la 2ª Classificata:", opzioni_2, index=idx_default_2, key=f"select_2_{lettera_corrente}")

            st.session_state.scelte_salvate[lettera_corrente]["1"] = p1
            st.session_state.scelte_salvate[lettera_corrente]["2"] = p2

            # --- STRINGHE HTML COMPATTE SENZA "\n" (Risolve definitivamente il problema di rendering) ---
            if p1 != "-":
                html_slot_1 = f'<div class="podium-slot" style="border-left: 4px solid #009933;"><span style="font-weight: bold; font-size: 13px;">🥇 1ª:</span><img src="{get_flag_url(p1)}" width="26" style="border-radius:2px; box-shadow: 1px 1px 2px rgba(0,0,0,0.1)"><span style="font-weight: bold; color: #009933; font-size: 14px;">{p1}</span></div>'
            else:
                html_slot_1 = '<div class="podium-slot empty">🥇 Primo Posto...</div>'

            if p2 != "-":
                html_slot_2 = f'<div class="podium-slot" style="border-left: 4px solid #111111;"><span style="font-weight: bold; font-size: 13px;">🥈 2ª:</span><img src="{get_flag_url(p2)}" width="26" style="border-radius:2px; box-shadow: 1px 1px 2px rgba(0,0,0,0.1)"><span style="font-weight: bold; color: #111111; font-size: 14px;">{p2}</span></div>'
            else:
                html_slot_2 = '<div class="podium-slot empty">🥈 Secondo Posto...</div>'

            # Costruiamo il blocco finale iniettando le stringhe flat, senza a capo intermedi
            full_podium_html = f'<div class="podium-container">{html_slot_1}{html_slot_2}</div><br>'
            st.markdown(full_podium_html, unsafe_allow_html=True)

            # --- CONTROLLI ---
            col_back, col_next = st.columns(2)
            with col_back:
                if st.session_state.current_index > 0:
                    if st.button("⬅️ Torna Indietro"):
                        st.session_state.current_index -= 1
                        st.rerun()
            with col_next:
                if p1 != "-" and p2 != "-":
                    testo_btn = "Conferma e Prosegui ➡️" if st.session_state.current_index < len(lista_lettere) - 1 else "🏁 Mostra il Riepilogo Finale"
                    if st.button(testo_btn):
                        if st.session_state.current_index < len(lista_lettere) - 1:
                            st.session_state.current_index += 1
                        else:
                            st.session_state.current_index = len(lista_lettere)
                        st.rerun()

    # --- SCHERMATA DI RIEPILOGO FINALE ---
    else:
        with st.container(border=True):
            st.markdown("<h3 style='text-align: center; margin-bottom: 5px;'>📝 RIEPILOGO DELLA TUA SCHEDINA</h3>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #555555; font-size: 14px; margin-bottom:20px;'>Fai lo screenshot a questo riquadro per condividerlo sul gruppo! 📸</p>", unsafe_allow_html=True)
            
            col_tab1, col_tab2 = st.columns(2)
            
            for idx, let in enumerate(lista_lettere):
                scelte = st.session_state.scelte_salvate[let]
                s1, s2 = scelte["1"], scelte["2"]
                
                card_html = f"""
                <div style='background-color: #ffffff; border-left: 6px solid #009933; border-radius: 8px; padding: 14px; margin-bottom: 12px; box-shadow: 0 3px 8px rgba(0,0,0,0.06); border: 1px solid #ebdccf;'>
                    <div style='font-weight: bold; color: #111111; font-size: 16px; margin-bottom: 8px; border-bottom: 1px dashed #dddddd; padding-bottom: 4px; display:flex; justify-content:space-between; align-items:center;'>
                        <span style='font-family: sans-serif; font-weight: 700;'>⚽ {let}</span>
                        <span style='font-size: 10px; background-color: #e2f0d9; color: #009933; padding: 2px 8px; border-radius: 10px; font-weight: bold;'>COMPLETATO</span>
                    </div>
                    <div style='display: flex; justify-content: space-between; align-items: center; font-size: 14px; margin-bottom: 6px;'>
                        <span style='color: #666666;'>🥇 1ª Classificata:</span>
                        <div style='display: flex; align-items: center; gap: 6px; font-weight: bold;'>
                            <img src="{get_flag_url(s1)}" width="24" style="border-radius:2px; box-shadow: 1px 1px 2px rgba(0,0,0,0.1)">
                            <span style='color: #009933;'>{s1}</span>
                        </div>
                    </div>
                    <div style='display: flex; justify-content: space-between; align-items: center; font-size: 14px;'>
                        <span style='color: #666666;'>🥈 2ª Classificata:</span>
                        <div style='display: flex; align-items: center; gap: 6px; font-weight: bold;'>
                            <img src="{get_flag_url(s2)}" width="24" style="border-radius:2px; box-shadow: 1px 1px 2px rgba(0,0,0,0.1)">
                            <span style='color: #111111;'>{s2}</span>
                        </div>
                    </div>
                </div>
                """
                if idx % 2 == 0:
                    with col_tab1: st.markdown(card_html, unsafe_allow_html=True)
                else:
                    with col_tab2: st.markdown(card_html, unsafe_allow_html=True)
                        
            st.markdown("<br><hr style='border: 1px dashed #009933;'>", unsafe_allow_html=True)
            
            col_modifica, col_salva = st.columns(2)
            with col_modifica:
                if st.button("🔄 Modifica i Gironi", use_container_width=True):
                    st.session_state.current_index = 0
                    st.rerun()
            with col_salva:
               if st.button("🚀 CONVALIDA E INVIA LA SCHEDINA 🚀", use_container_width=True):
                    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    nuove_righe = []
                    for let in lista_lettere:
                        scelte = st.session_state.scelte_salvate[let]
                        nuove_righe.append({"Data": ts, "Utente_Telegram": telegram_user, "Girone": let, "Posizione": "1", "Squadra_Pronosticata": scelte["1"]})
                        nuove_righe.append({"Data": ts, "Utente_Telegram": telegram_user, "Girone": let, "Posizione": "2", "Squadra_Pronosticata": scelte["2"]})
                    
                    # 1. TRASFORMA IN DATAFRAME I NUOVI DATI
                    df_nuovo = pd.DataFrame(nuove_righe)
                    
                    # 2. LEGGI I DATI ESISTENTI DALLA SCHEDA "Gironi"
                    worksheet = sh.worksheet("Gironi")
                    try:
                        records = worksheet.get_all_records()
                        df_esistente = pd.DataFrame(records)
                    except Exception:
                        # Se la scheda è vuota o dà errore, creiamo una struttura base
                        df_esistente = pd.DataFrame(columns=["Data", "Utente_Telegram", "Girone", "Posizione", "Squadra_Pronosticata"])
                        
                    # 3. UNISCI E AGGIORNA IL FOGLIO GOOGLE
                    df_finale = pd.concat([df_esistente, df_nuovo], ignore_index=True)

                   
                    # Svuota la scheda (mantenendo la struttura) e riscrivi tutto il DataFrame aggiornato
                    worksheet.clear()
                    worksheet.update([df_finale.columns.values.tolist()] + df_finale.fillna("").values.tolist())
                    
                    st.success("🎯 Schedina inserita! Fai lo screenshot alle tue card qui sopra e vedi chi vince sul gruppo!")
                    st.balloons()
else:
    st.info("💡 Inserisci il tuo Username Telegram in alto per sbloccare la schedina.")