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
    "Messico": "mx", "Sudafrica": "za", "Corea del Sud": "kr", "Rep. Ceca": "cz",
    "Canada": "ca", "Bosnia": "ba", "Stati Uniti": "us", "Paraguay": "py",
    "Qatar": "qa", "Svizzera": "ch", "Brasile": "br", "Marocco": "ma",
    "Haiti": "ht", "Scozia": "gb-sct", "Australia": "au", "Turchia": "tr",
    "Germania": "de", "Curaçao": "cw", "Costa d'Avorio": "ci", "Ecuador": "ec",
    "Paesi Bassi": "nl", "Giappone": "jp", "Svezia": "se", "Tunisia": "tn",
    "Belgio": "be", "Egitto": "eg", "Iran": "ir", "Nuova Zelanda": "nz",
    "Spagna": "es", "Capo Verde": "cv", "Arabia Saudita": "sa", "Uruguay": "uy"
}

def get_flag_url(team_name):
    code = FLAG_CODES.get(team_name)
    if not code:
        return "https://flagcdn.com/w80/un.png"
    return f"https://flagcdn.com/w80/{code}.png"

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
col_left, col_center, col_right = st.columns([2, 1, 2])

with col_center:
    # Mostriamo l'immagine. Purtroppo non è cliccabile direttamente.
    # Quindi mettiamo un tasto "Home" subito sotto o sopra il logo.
    st.image("Mundial&Me Logo Nero.png", use_container_width=True)
    
    # Questo è il modo più pulito: un bottone "Home" che richiama la funzione
    if st.button("🏠 Home", use_container_width=True, on_click=reset_al_main):
        pass

# Separatore discreto
st.markdown("<hr style='border: 0.5px solid #e0e0e0; margin: 15px 0;'>", unsafe_allow_html=True)
# --- LOGIN UTENTE ---
telegram_user = st.text_input("💬 Inserisci il tuo Username Telegram per giocare:", placeholder="@tuo_nickname")

if telegram_user:
    squadre_gironi = {
        "A": ["Messico", "Sudafrica", "Corea del Sud", "Rep. Ceca"],
        "B": ["Canada", "Bosnia", "Qatar", "Svizzera"],
        "C": ["Germania", "Curaçao", "Costa d'Avorio", "Ecuador"],
        "D": ["Stati Uniti", "Paraguay", "Haiti", "Scozia"],
        "E": ["Brasile", "Marocco", "Australia", "Turchia"],
        "F": ["Paesi Bassi", "Giappone", "Svezia", "Tunisia"],
        "G": ["Belgio", "Egitto", "Iran", "Nuova Zelanda"],
        "H": ["Spagna", "Capo Verde", "Arabia Saudita", "Uruguay"]
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
        badge_html += f'<div class="girone-badge {status_class}">Girone {let} {icon}</div>'
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
                        🏆 GRUPPO {lettera_corrente}
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
                        <span style='font-family: sans-serif; font-weight: 700;'>⚽ GRUPPO {let}</span>
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