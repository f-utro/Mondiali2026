import streamlit as st
import pandas as pd
import os
from datetime import datetime
import gspread

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Mundial&Me Live", page_icon="⚽", layout="centered", initial_sidebar_state="collapsed")

# --- FILE DATABASE LOCALE (BACKUP) ---
LIVE_DATA_FILE = "schedine_live.csv"
if not os.path.exists(LIVE_DATA_FILE):
    pd.DataFrame(columns=["Data", "Utente_Telegram", "Giornata", "Partita", "Pronostico_Segno", "Pronostico_Risultato"]).to_csv(LIVE_DATA_FILE, index=False)

# --- DIZIONARIO EMOTICON BANDIERE ---
# FLAGS = {
#     "Messico": "🇲🇽", "Sudafrica": "🇿🇦", "Corea del Sud": "🇰🇷", "Rep. Ceca": "🇨🇿",
#     "Canada": "🇨🇦", "Bosnia ed Erzegovina": "🇧🇦", "Qatar": "🇶🇦", "Svizzera": "🇨🇭",
#     "Brasile": "🇧🇷", "Marocco": "🇲🇦", "Haiti": "🇭🇹", "Scozia": "🏴󠁧󠁢󠁳󠁣󠁴󠁿",
#     "Stati Uniti": "🇺🇸", "Paraguay": "🇵🇾", "Australia": "🇦🇺", "Turchia": "🇹🇷",
#     "Germania": "🇩🇪", "Curaçao": "🇨🇼", "Costa d'Avorio": "🇨🇮", "Ecuador": "🇪🇨",
#     "Paesi Bassi": "🇳🇱", "Giappone": "🇯🇵", "Svezia": "🇸🇪", "Tunisia": "🇹🇳",
#     "Belgio": "🇧🇪", "Egitto": "🇪🇬", "Iran": "🇮🇷", "Nuova Zelanda": "🇳🇿",
#     "Spagna": "🇪🇸", "Capo Verde": "🇨🇻", "Arabia Saudita": "🇸🇦", "Uruguay": "🇺🇾",
#     "Francia": "🇫🇷", "Senegal": "🇸🇳", "Iraq": "🇮🇶", "Norvegia": "🇳🇴",
#     "Argentina": "🇦🇷", "Algeria": "🇩🇿", "Austria": "🇦🇹", "Giordania": "🇯🇴",
#     "Portogallo": "🇵🇹", "RD del Congo": "🇨🇩", "Uzbekistan": "🇺🇿", "Colombia": "🇨🇴",
#     "Inghilterra": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "Croazia": "🇭🇷", "Ghana": "🇬🇭", "Panama": "🇵🇦"
# }

FLAGS = {
    "Messico": {"emoji": "🇲🇽", "code": "mx"},
    "Sudafrica": {"emoji": "🇿🇦", "code": "za"},
    "Corea del Sud": {"emoji": "🇰🇷", "code": "kr"},
    "Rep. Ceca": {"emoji": "🇨🇿", "code": "cz"},
    "Canada": {"emoji": "🇨🇦", "code": "ca"},
    "Bosnia ed Erzegovina": {"emoji": "🇧🇦", "code": "ba"},
    "Qatar": {"emoji": "🇶🇦", "code": "qa"},
    "Svizzera": {"emoji": "🇨🇭", "code": "ch"},
    "Brasile": {"emoji": "🇧🇷", "code": "br"},
    "Marocco": {"emoji": "🇲🇦", "code": "ma"},
    "Haiti": {"emoji": "🇭🇹", "code": "ht"},
    "Scozia": {"emoji": "🏴󠁧󠁢󠁳󠁣󠁴󠁿", "code": "gb-sct"},
    "Stati Uniti": {"emoji": "🇺🇸", "code": "us"},
    "Paraguay": {"emoji": "🇵🇾", "code": "py"},
    "Australia": {"emoji": "🇦🇺", "code": "au"},
    "Turchia": {"emoji": "🇹🇷", "code": "tr"},
    "Germania": {"emoji": "🇩🇪", "code": "de"},
    "Curaçao": {"emoji": "🇨🇼", "code": "cw"},
    "Costa d'Avorio": {"emoji": "🇨🇮", "code": "ci"},
    "Ecuador": {"emoji": "🇪🇨", "code": "ec"},
    "Paesi Bassi": {"emoji": "🇳🇱", "code": "nl"},
    "Giappone": {"emoji": "🇯🇵", "code": "jp"},
    "Svezia": {"emoji": "🇸🇪", "code": "se"},
    "Tunisia": {"emoji": "🇹🇳", "code": "tn"},
    "Belgio": {"emoji": "🇧🇪", "code": "be"},
    "Egitto": {"emoji": "🇪🇬", "code": "eg"},
    "Iran": {"emoji": "🇮🇷", "code": "ir"},
    "Nuova Zelanda": {"emoji": "🇳🇿", "code": "nz"},
    "Spagna": {"emoji": "🇪🇸", "code": "es"},
    "Capo Verde": {"emoji": "🇨🇻", "code": "cv"},
    "Arabia Saudita": {"emoji": "🇸🇦", "code": "sa"},
    "Uruguay": {"emoji": "🇺🇾", "code": "uy"},
    "Francia": {"emoji": "🇫🇷", "code": "fr"},
    "Senegal": {"emoji": "🇸🇳", "code": "sn"},
    "Iraq": {"emoji": "🇮🇶", "code": "iq"},
    "Norvegia": {"emoji": "🇳🇴", "code": "no"},
    "Argentina": {"emoji": "🇦🇷", "code": "ar"},
    "Algeria": {"emoji": "🇩🇿", "code": "dz"},
    "Austria": {"emoji": "🇦🇹", "code": "at"},
    "Giordania": {"emoji": "🇯🇴", "code": "jo"},
    "Portogallo": {"emoji": "🇵🇹", "code": "pt"},
    "RD del Congo": {"emoji": "🇨🇩", "code": "cd"},
    "Uzbekistan": {"emoji": "🇺🇿", "code": "uz"},
    "Colombia": {"emoji": "🇨🇴", "code": "co"},
    "Inghilterra": {"emoji": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "code": "gb-eng"},
    "Croazia": {"emoji": "🇭🇷", "code": "hr"},
    "Ghana": {"emoji": "🇬🇭", "code": "gh"},
    "Panama": {"emoji": "🇵🇦", "code": "pa"}
}

# Esempio logico:
def filtra_giocate_valide(df_live):
    giocate_valide = []
    ora_attuale = datetime.now()
    # Assumiamo l'anno corrente (2026)
    anno = ora_attuale.year
    
    for _, row in df_live.iterrows():
        # Recuperiamo la partita dalla riga del CSV
        partita_nome = row["Partita"]
        
        # Cerchiamo la partita nel calendario per trovare data e ora
        orario_inizio = None
        for giornata in CALENDARIO_GIORNATE:
            for match in CALENDARIO_GIORNATE[giornata]:
                match_str = f"{match['t1']} vs {match['t2']}"
                if match_str == partita_nome:
                    # Uniamo data e ora: "27/06" + "17:00" -> 2026-06-27 17:00:00
                    data_str = f"{anno}/{match['data']} {match['ora']}"
                    orario_inizio = datetime.strptime(data_str, '%Y/%d/%m %H:%M')
                    break
        
        # Data in cui l'utente ha inviato la giocata (deve essere presente nel CSV)
        try:
            data_giocata = datetime.strptime(row["Data_Invio"], '%Y-%m-%d %H:%M:%S')
        except:
            continue # Salta righe malformate

        # Filtro: Giocata deve essere precedente all'inizio partita
        if orario_inizio and data_giocata < orario_inizio:
            giocate_valide.append(row)
            
    return pd.DataFrame(giocate_valide)

def is_partita_aperta(orario_str):
    # Formato dell'orario nel calendario
    fmt = '%Y-%m-%d %H:%M:%S'
    inizio_partita = datetime.strptime(orario_str, fmt)
    # Ritorna True se la partita inizia tra più di 0 secondi
    return datetime.now() < inizio_partita

# Funzione corretta per ottenere l'URL immagine
def get_flag_link(team):
    return f"https://flagcdn.com/w40/{FLAGS.get(team, {'code': 'xx'})['code']}.png"

def get_flag(team):
    # Accediamo al dizionario FLAGS che hai definito
    # Estraiamo solo il valore della chiave 'code'
    data = FLAGS.get(team, {'emoji': '⚽', 'code': 'xx'})
    code = data.get('code', 'xx')
    return f"https://flagcdn.com/w40/{code}.png"

# Questa funzione serve SOLO per creare l'URL dell'immagine che st.image capisce
# def get_flag_link(team_name):
#     # Usiamo lo stesso dizionario che hai già, ma lo mappiamo ai codici FlagCDN
#     # Se il nome non è nel dizionario, usiamo 'xx' (bandiera generica)
#     mapping = {
#         "Messico": "mx", "Sudafrica": "za", "Corea del Sud": "kr", "Rep. Ceca": "cz",
#         "Canada": "ca", "Bosnia ed Erzegovina": "ba", "Qatar": "qa", "Svizzera": "ch",
#         "Brasile": "br", "Marocco": "ma", "Haiti": "ht", "Scozia": "gb-sct"
#         # ... aggiungi qui gli altri che ti servono nello stesso formato "Nome": "codice"
#     }
#     codice = mapping.get(team_name, "xx")
#     return f"https://flagcdn.com/w40/{codice}.png"

# --- CALENDARIO COMPLETO REINTEGRATO ---
CALENDARIO_GIORNATE = {
        "Giornata 1 (11 - 17 Giugno)": [
            {"t1": "Messico", "t2": "Sudafrica", "ora": "13:00", "data": "11/06"},
            {"t1": "Corea del Sud", "t2": "Rep. Ceca", "ora": "20:00", "data": "11/06"},
            {"t1": "Canada", "t2": "Bosnia ed Erzegovina", "ora": "15:00", "data": "12/06"},
            {"t1": "Stati Uniti", "t2": "Paraguay", "ora": "18:00", "data": "12/06"},
            {"t1": "Qatar", "t2": "Svizzera", "ora": "12:00", "data": "13/06"},
            {"t1": "Brasile", "t2": "Marocco", "ora": "18:00", "data": "13/06"},
            {"t1": "Haiti", "t2": "Scozia", "ora": "21:00", "data": "13/06"},
            {"t1": "Australia", "t2": "Turchia", "ora": "21:00", "data": "13/06"},
            {"t1": "Germania", "t2": "Curaçao", "ora": "12:00", "data": "14/06"},
            {"t1": "Paesi Bassi", "t2": "Giappone", "ora": "15:00", "data": "14/06"},
            {"t1": "Costa d'Avorio", "t2": "Ecuador", "ora": "19:00", "data": "14/06"},
            {"t1": "Svezia", "t2": "Tunisia", "ora": "20:00", "data": "14/06"},
            {"t1": "Belgio", "t2": "Egitto", "ora": "12:00", "data": "15/06"},
            {"t1": "Iran", "t2": "Nuova Zelanda", "ora": "18:00", "data": "15/06"},
            {"t1": "Spagna", "t2": "Capo Verde", "ora": "12:00", "data": "15/06"},
            {"t1": "Arabia Saudita", "t2": "Uruguay", "ora": "18:00", "data": "15/06"},
            {"t1": "Francia", "t2": "Senegal", "ora": "15:00", "data": "16/06"},
            {"t1": "Iraq", "t2": "Norvegia", "ora": "18:00", "data": "16/06"},
            {"t1": "Argentina", "t2": "Algeria", "ora": "20:00", "data": "16/06"},
            {"t1": "Austria", "t2": "Giordania", "ora": "21:00", "data": "16/06"},
            {"t1": "Inghilterra", "t2": "Croazia", "ora": "15:00", "data": "17/06"},
            {"t1": "Ghana", "t2": "Panama", "ora": "19:00", "data": "17/06"},
            {"t1": "Portogallo", "t2": "RD del Congo", "ora": "12:00", "data": "17/06"},
            {"t1": "Uzbekistan", "t2": "Colombia", "ora": "20:00", "data": "17/06"}
        ],
        "Giornata 2 (18 - 23 Giugno)": [
            {"t1": "Rep. Ceca", "t2": "Sudafrica", "ora": "12:00", "data": "18/06"},
            {"t1": "Messico", "t2": "Corea del Sud", "ora": "19:00", "data": "18/06"},
            {"t1": "Svizzera", "t2": "Bosnia ed Erzegovina", "ora": "12:00", "data": "18/06"},
            {"t1": "Canada", "t2": "Qatar", "ora": "15:00", "data": "18/06"},
            {"t1": "Scozia", "t2": "Marocco", "ora": "18:00", "data": "19/06"},
            {"t1": "Brasile", "t2": "Haiti", "ora": "21:00", "data": "19/06"},
            {"t1": "Stati Uniti", "t2": "Australia", "ora": "12:00", "data": "19/06"},
            {"t1": "Turchia", "t2": "Paraguay", "ora": "21:00", "data": "19/06"},
            {"t1": "Germania", "t2": "Costa d'Avorio", "ora": "16:00", "data": "20/06"},
            {"t1": "Ecuador", "t2": "Curaçao", "ora": "19:00", "data": "20/06"},
            {"t1": "Paesi Bassi", "t2": "Svezia", "ora": "12:00", "data": "20/06"},
            {"t1": "Tunisia", "t2": "Giappone", "ora": "22:00", "data": "20/06"},
            {"t1": "Belgio", "t2": "Iran", "ora": "12:00", "data": "21/06"},
            {"t1": "Nuova Zelanda", "t2": "Egitto", "ora": "18:00", "data": "21/06"},
            {"t1": "Spagna", "t2": "Arabia Saudita", "ora": "12:00", "data": "21/06"},
            {"t1": "Uruguay", "t2": "Capo Verde", "ora": "18:00", "data": "21/06"},
            {"t1": "Francia", "t2": "Iraq", "ora": "17:00", "data": "22/06"},
            {"t1": "Norvegia", "t2": "Senegal", "ora": "20:00", "data": "22/06"},
            {"t1": "Argentina", "t2": "Austria", "ora": "12:00", "data": "22/06"},
            {"t1": "Giordania", "t2": "Algeria", "ora": "20:00", "data": "22/06"},
            {"t1": "Portogallo", "t2": "Uzbekistan", "ora": "12:00", "data": "23/06"},
            {"t1": "Colombia", "t2": "RD del Congo", "ora": "20:00", "data": "23/06"},
            {"t1": "Inghilterra", "t2": "Ghana", "ora": "16:00", "data": "23/06"},
            {"t1": "Panama", "t2": "Croazia", "ora": "19:00", "data": "23/06"}
        ],
        "Giornata 3 (24 - 27 Giugno)": [
            {"t1": "Rep. Ceca", "t2": "Messico", "ora": "19:00", "data": "24/06"},
            {"t1": "Sudafrica", "t2": "Corea del Sud", "ora": "19:00", "data": "24/06"},
            {"t1": "Svizzera", "t2": "Canada", "ora": "12:00", "data": "24/06"},
            {"t1": "Bosnia ed Erzegovina", "t2": "Qatar", "ora": "12:00", "data": "24/06"},
            {"t1": "Scozia", "t2": "Brasile", "ora": "18:00", "data": "24/06"},
            {"t1": "Marocco", "t2": "Haiti", "ora": "18:00", "data": "24/06"},
            {"t1": "Turchia", "t2": "Stati Uniti", "ora": "19:00", "data": "25/06"},
            {"t1": "Paraguay", "t2": "Australia", "ora": "19:00", "data": "25/06"},
            {"t1": "Curaçao", "t2": "Costa d'Avorio", "ora": "16:00", "data": "25/06"},
            {"t1": "Ecuador", "t2": "Germania", "ora": "16:00", "data": "25/06"},
            {"t1": "Giappone", "t2": "Svezia", "ora": "18:00", "data": "25/06"},
            {"t1": "Tunisia", "t2": "Paesi Bassi", "ora": "18:00", "data": "25/06"},
            {"t1": "Egitto", "t2": "Iran", "ora": "20:00", "data": "26/06"},
            {"t1": "Nuova Zelanda", "t2": "Belgio", "ora": "20:00", "data": "26/06"},
            {"t1": "Capo Verde", "t2": "Arabia Saudita", "ora": "19:00", "data": "26/06"},
            {"t1": "Uruguay", "t2": "Spagna", "ora": "18:00", "data": "26/06"},
            {"t1": "Norvegia", "t2": "Francia", "ora": "15:00", "data": "26/06"},
            {"t1": "Senegal", "t2": "Iraq", "ora": "15:00", "data": "26/06"},
            {"t1": "Algeria", "t2": "Austria", "ora": "21:00", "data": "27/06"},
            {"t1": "Giordania", "t2": "Argentina", "ora": "21:00", "data": "27/06"},
            {"t1": "Colombia", "t2": "Portogallo", "ora": "19:30", "data": "27/06"},
            {"t1": "RD del Congo", "t2": "Uzbekistan", "ora": "19:30", "data": "27/06"},
            {"t1": "Panama", "t2": "Inghilterra", "ora": "17:00", "data": "27/06"},
            {"t1": "Croazia", "t2": "Ghana", "ora": "17:00", "data": "27/06"}
            ]
    }

# --- ENGINE CSS CUSTOM ---
st.markdown("""
<style>
    .stApp { background-color: #f9ebdf !important; }
    
    /* Contenitore del bottone personalizzato */
    .match-btn-content {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 12px !important;
        width: 100% !important;
    }
    
    /* Stile per le bandiere */
    .flag-icon { 
        width: 35px !important; 
        height: 25px !important; 
        object-fit: contain; 
        flex-shrink: 0; 
    }
    
    /* Stile per il testo */
    .match-text { 
        font-weight: bold !important; 
        font-size: 14px !important; 
    }
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
    /* Nasconde il menu di Streamlit (hamburger) */
    #MainMenu {visibility: hidden;}
    
    /* Nasconde il footer con "Made with Streamlit" */
    footer {visibility: hidden;}
    
    /* Nasconde l'header (se vuoi una pulizia totale) */
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)



path_json_locale = "credenziali_google.json"
URL_FOGLIO = "https://docs.google.com/spreadsheets/d/1eplWbGsR3lpAPawatIBuSp5ts20K4Nn-_QUqvE2Md-g/edit"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

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

gc = inizializza_gspread()
sh = gc.open_by_url(URL_FOGLIO)

def convalida_risultato(segno, risultato_str):
    if segno == "-" or not risultato_str: return True, ""
    if "-" not in risultato_str: return False, "Formato: 'GolCasa-GolTrasferta' (es. 2-1)."
    try:
        gol_casa, gol_trasf = map(int, risultato_str.split("-"))
        if segno == "1" and gol_casa <= gol_trasf: return False, "Incoerente con Segno 1."
        if segno == "2" and gol_trasf <= gol_casa: return False, "Incoerente con Segno 2."
        if segno == "X" and gol_casa != gol_trasf: return False, "Incoerente con Segno X."
        return True, ""
    except ValueError: return False, "Numeri non validi."

# --- BRANDING HEADER ---
# col_logo, col_titolo = st.columns([1.2, 4.8])
# with col_logo:
#     st.markdown('<div style="border: 3px solid #009933; padding: 6px; text-align: center; border-radius: 5px; background-color: #f0fbf2; margin-top: 5px;"><span style="color: #009933; font-weight: bold; font-size: 10px;">CONCORSO</span><br><span style="color: #009933; font-weight: bold; font-size: 24px; line-height: 24px; font-family: monospace;">J&M</span></div>', unsafe_allow_html=True)
# with col_titolo:
#     st.markdown('<div style="text-align: center;"><h1 style="font-family: \'Brush Script MT\', cursive; font-size: 42px; margin: 0; font-style: italic; line-height: 42px;"><span style="color: #009933;">Toto</span>Juve&Me</h1><p style="color: #555555; font-weight: bold; font-family: monospace; letter-spacing: 1px; margin: 0; font-size: 10px;">" AL SERVIZIO DELLO SPORT BIANCONERO "</p></div>', unsafe_allow_html=True)

# --- BRANDING HEADER ---
# Creiamo 3 colonne: quella centrale conterrà il logo, le laterali gestiscono lo spazio
# col_left, col_center, col_right = st.columns([2, 1, 2])

# with col_center:
#     # Usiamo il logo "Nero" perché contiene già il nome del brand
#     st.image("Mundial&Me Logo Nero.png", use_container_width=True)

def vai_alla_home():
    st.session_state.pagina_corrente = "GIOCA"
    st.session_state.mostra_ricevuta = False
    # Eventuale pulizia dello stato partita
    if "partita_attiva" in st.session_state:
        del st.session_state.partita_attiva

# --- BRANDING HEADER ---
col_left, col_center, col_right = st.columns([2, 1, 2])

with col_center:
    # Mostriamo l'immagine. Purtroppo non è cliccabile direttamente.
    # Quindi mettiamo un tasto "Home" subito sotto o sopra il logo.
    st.image("Mundial&Me Logo Nero.png", use_container_width=True)
    
    # Questo è il modo più pulito: un bottone "Home" che richiama la funzione
    st.link_button("🏠 Home", "https://mundialandme.streamlit.app/", use_container_width=True)

# Separatore grafico che riprende il colore verde del tema
st.markdown("<hr style='border: 1px solid #009933; margin: 15px 0;'>", unsafe_allow_html=True)
# --- STATO DELLA NAVIGAZIONE ---
if "pagina_corrente" not in st.session_state:
    st.session_state.pagina_corrente = "GIOCA"

st.markdown("<br>", unsafe_allow_html=True)

# --- NAVIGAZIONE PRINCIPALE ---
col_nav1, col_nav2 = st.columns(2)
with col_nav1:
    st.markdown(f'<div class="{"menu-active" if st.session_state.pagina_corrente == "GIOCA" else "menu-inactive"}">', unsafe_allow_html=True)
    if st.button("📝 COMPILA SCHEDINA", use_container_width=True):
        st.session_state.pagina_corrente = "GIOCA"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
with col_nav2:
    st.markdown(f'<div class="{"menu-active" if st.session_state.pagina_corrente == "CLASSIFICA" else "menu-inactive"}">', unsafe_allow_html=True)
    if st.button("🏆 CLASSIFICA LIVE", use_container_width=True):
        st.session_state.pagina_corrente = "CLASSIFICA"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<hr style='margin-top:10px; margin-bottom:15px; border:0; border-top:1px solid #ebdccf;'>", unsafe_allow_html=True)

# ==========================================
# SEZIONE GIOCO
# ==========================================
if st.session_state.pagina_corrente == "GIOCA":
    if "telegram_user" not in st.session_state: st.session_state.telegram_user = ""
    if "match_idx" not in st.session_state: st.session_state.match_idx = 0
    if "mostra_ricevuta" not in st.session_state: st.session_state.mostra_ricevuta = False

    if not st.session_state.telegram_user:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0; margin-bottom: 15px; font-weight: 800;'>🎟️ APRI SCHEDINA LIVE</h3>", unsafe_allow_html=True)
        
        # TORNA LA SELEZIONE DELLA GIORNATA COMPLETA
        giornata_selezionata = st.selectbox("📅 SELEZIONA IL CONCORSO:", list(CALENDARIO_GIORNATE.keys()))
        st.session_state.giornata = giornata_selezionata
        st.markdown("<br>", unsafe_allow_html=True)
        input_nome = st.text_input("NOME UTENTE TELEGRAM:", placeholder="Es. @JuvAndMe_User")

        
        
        if st.button("Accedi alla Schedina ➡️", use_container_width=True):
            if input_nome.strip():
                st.session_state.telegram_user = input_nome.strip()
                st.session_state.giocate_live = {f"{m['t1']}_vs_{m['t2']}": {"1X2": "-", "ris": ""} for m in CALENDARIO_GIORNATE[giornata_selezionata]}
                st.rerun()
            else:
                st.warning("⚠️ Inserisci il tuo username Telegram.")
        st.markdown('</div>', unsafe_allow_html=True)

    elif not st.session_state.mostra_ricevuta:
        partite = CALENDARIO_GIORNATE[st.session_state.giornata]
        st.markdown("<p style='font-weight: bold; margin-bottom: 8px; font-size: 13px; text-align: center;'>👉 Seleziona la partita da inserire/modificare:</p>", unsafe_allow_html=True)
        
        # --- BLOCCO CORRETTO DA SOSTITUIRE ---
#         DENSITA_COLONNE = 3
#         for riga_idx in range(0, len(partite), DENSITA_COLONNE):
#             cols = st.columns(DENSITA_COLONNE, gap="small")
#             for col_idx in range(DENSITA_COLONNE):
#                 match_idx = riga_idx + col_idx
#                 if match_idx < len(partite):
#                     m = partite[match_idx]
                    
#                     # All'interno del tuo ciclo, sostituisci il blocco con questo:
#                     with cols[col_idx]:
#                         m = partite[match_idx] # Partita corrente
                        
#                         # Crea una mini-riga per le bandiere
#                         # b1, b2, b3 = st.columns([1, 1, 1])
#                         # with b1: st.image(get_flag_link(m['t1']), width=30)
#                         # with b2: st.write("vs")
#                         # with b3: st.image(get_flag_link(m['t2']), width=30)
#                         # Invece di b1, b2, b3 = st.columns([1, 1, 1]) ...
# # Usa questa singola riga di markdown con stile HTML:

#                         link_id = f"btn_{match_idx}"
    
#                         # Questo HTML crea un rettangolo cliccabile che sembra un bottone
#                         # Al click, invia un segnale a Streamlit usando i query_params
#                         st.markdown(f"""
#                         <a href="?match_idx={match_idx}" style="text-decoration: none;">
#                             <div class="match-btn-custom" style="
#                                 display: flex; align-items: center; justify-content: center; gap: 15px;
#                                 background-color: #000000; border: 2px solid #00FF00; border-radius: 8px;
#                                 padding: 12px; color: white; font-weight: bold; width: 100%;
#                             ">
#                                 <img src="{get_flag_link(m['t1'])}" style="width: 35px; height: 25px;">
#                                 <span>{m['t1']} vs {m['t2']}</span>
#                                 <img src="{get_flag_link(m['t2'])}" style="width: 35px; height: 25px;">
#                             </div>
#                         </a>
#                         """, unsafe_allow_html=True)

#                         # # Il tuo bottone va subito dopo
#                         # if st.button(label_html, key=f"btn_{match_idx}", use_container_width=True):
#                         #     st.session_state.match_idx = match_idx
#                         #     st.rerun()
                            
#         if "match_idx" in st.query_params:
#             st.session_state.match_idx = int(st.query_params["match_idx"])
#             st.query_params.clear() # Pulisce l'URL
#             st.rerun()
                        #if corrente: st.markdown('</div>', unsafe_allow_html=True)
        # --- CICLO PARTITE ---
        for i, m in enumerate(partite):

            aperta = is_partita_aperta(m['orario'])
            # Usiamo un unico blocco HTML per tutto: Bandiere + "vs" + Bottone
            # Questo forza il browser a tenere tutto insieme su una riga
            if aperta:
                st.markdown(f"""
                <div style="
                    display: flex; flex-direction: column; align-items: center; 
                    margin-bottom: 25px; width: 100%;
                ">
                    <div style="
                        display: flex; align-items: center; justify-content: center; 
                        gap: 15px; margin-bottom: 5px;
                    ">
                        <img src="{get_flag_link(m['t1'])}" style="width: 35px; height: 25px;">
                        <span style="font-weight: bold;">vs</span>
                        <img src="{get_flag_link(m['t2'])}" style="width: 35px; height: 25px;">
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Il bottone sta subito sotto, integrato nel flusso
                if st.button(f"{m['t1']} - {m['t2']}", key=f"btn_{i}", use_container_width=True):
                    st.session_state.match_idx = i
                    st.rerun()
            else:
                st.button(f"🔒 {m['t1']} vs {m['t2']} (Chiusa)", disabled=True, key=f"btn_locked_{i}")
        st.markdown("<br>", unsafe_allow_html=True)
        # current_match = partite[st.session_state.match_idx]
        # key_match = f"{current_match['t1']}_vs_{current_match['t2']}"
        
        
        # st.markdown(f'<div class="match-card"><div class="match-header">⚽ MATCH CORRENTE (N.{st.session_state.match_idx+1})</div><div class="match-teams"><span>{get_flag(current_match["t1"])} {current_match["t1"]}</span><span style="color: #009933; margin: 0 10px;">-</span><span>{current_match["t2"]} {get_flag(current_match["t2"])}</span></div></div>', unsafe_allow_html=True)
        current_match = partite[st.session_state.match_idx]
        
        st.markdown(f'<div class="match-card"><div class="match-header">⚽ MATCH CORRENTE (N.{st.session_state.match_idx+1})</div>', unsafe_allow_html=True)
        
        # Allineamento a 5 colonne: [Bandiera1, Nome1, VS, Nome2, Bandiera2]
        c1, c2, c3, c4, c5 = st.columns([1, 2, 1, 2, 1])
        current_match = partite[st.session_state.match_idx]
       
        with c1: 
            st.image(get_flag_link(current_match['t1']), width=35)
        with c2: 
            st.markdown(f"**{current_match['t1']}**")
        with c3: 
            st.write("vs")
        with c4: 
            st.markdown(f"**{current_match['t2']}**") # <--- AGGIUNTO: Nome seconda squadra
        with c5: 
            st.image(get_flag_link(current_match['t2']), width=35) # <--- AGGIUNTO: Bandiera seconda squadra
        
       
        st.markdown('</div>', unsafe_allow_html=True)  
        key_match = f"{current_match['t1']}_vs_{current_match['t2']}"
        
        col_es, col_totogol = st.columns([1, 1])
        with col_es:
            st.markdown("<label style='font-weight: bold; font-size: 13px;'>📊 Segno 1X2:</label>", unsafe_allow_html=True)
            opzioni = ["-", "1", "X", "2"]
            def_1x2 = st.session_state.giocate_live[key_match]["1X2"]
            idx_1x2 = opzioni.index(def_1x2) if def_1x2 in opzioni else 0
            nuovo_segno = st.radio("Esito", opzioni, index=idx_1x2, key=f"rad_{key_match}", horizontal=True, label_visibility="collapsed")
            st.session_state.giocate_live[key_match]["1X2"] = nuovo_segno
            
        with col_totogol:
            st.markdown("<label style='font-weight: bold; font-size: 13px;'>🔢 Risultato Esatto:</label>", unsafe_allow_html=True)
            nuovo_ris = st.text_input("Risultato", value=st.session_state.giocate_live[key_match]["ris"], placeholder="Es. 2-1", key=f"txt_{key_match}", label_visibility="collapsed").strip()
            st.session_state.giocate_live[key_match]["ris"] = nuovo_ris

        valido, msg_errore = convalida_risultato(st.session_state.giocate_live[key_match]["1X2"], st.session_state.giocate_live[key_match]["ris"])
        if not valido and st.session_state.giocate_live[key_match]["ris"] != "":
            st.error(f"⚠️ {msg_errore}")
            pronostico_pronto = False
        else: pronostico_pronto = True

        st.markdown("<br>", unsafe_allow_html=True)
        col_btn_next, col_btn_save = st.columns(2)
        with col_btn_next:
            st.markdown('<div class="btn-next">', unsafe_allow_html=True)
            if st.session_state.match_idx < len(partite) - 1:
                if st.button("➡️ PROSSIMA PARTITA", use_container_width=True):
                    if pronostico_pronto:
                        st.session_state.match_idx += 1
                        st.rerun()
            else:
                st.button("🏁 ULTIMA PARTITA", disabled=True, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_btn_save:
            st.markdown('<div class="btn-save">', unsafe_allow_html=True)
            if st.button("📝 I Tuoi Pronostici", use_container_width=True):
                if pronostico_pronto:
                    st.session_state.mostra_ricevuta = True
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # --- CORREZIONE INTEGRALE E PARSING CORRETTO HTML SCONTRINO ---
    # --- BLOCCO RICEVUTA CORRETTO E BLINDATO SENZA TAG RAW ---
    else:
        partite = CALENDARIO_GIORNATE[st.session_state.giornata]
        telegram_user = st.session_state.telegram_user
        
        # Inizializziamo l'html su un'unica riga logica
        testo_ricevuta = (
            '<div style="background: #fff2cc; border: 2px solid #111111; padding: 20px; border-radius: 4px; box-shadow: 0 4px 15px rgba(0,0,0,0.08);">'
            '<div style="text-align: center; border-bottom: 2px dashed #111111; padding-bottom: 12px; margin-bottom: 18px;">'
            '<h3 style="margin: 0; font-family: monospace; font-weight: 900; letter-spacing: 2px;">RICEVUTA CONCORSO J&M</h3>'
            f'<p style="margin: 6px 0 0 0; font-size: 14px; font-family: monospace; font-weight: bold;">UTENTE: {telegram_user}</p>'
            f'<p style="margin: 2px 0 0 0; font-size: 11px; font-family: monospace; color: #777777;">{datetime.now().strftime("%d/%m/%Y %H:%M")}</p>'
            '</div>'
        )

        giocate_effettuate = 0
        for idx, m in enumerate(partite):
            k = f"{m['t1']}_vs_{m['t2']}"
            voto = st.session_state.giocate_live[k]
            
            # Filtro per mostrare solo i match compilati
            if voto['1X2'] == "-" or voto['1X2'] == "" or not voto['1X2']:
                continue
                
            giocate_effettuate += 1
            testo_ricevuta += (
                '<div style="display: flex; justify-content: space-between; align-items: center; font-family: monospace; font-size: 13px; padding: 6px 0; border-bottom: 1px dotted #bbbbbb;">'
                f'<span style="font-weight: bold; display: flex; align-items: center; gap: 5px;">'
                    f'{idx+1:02d}. '
                    f'<img src="{get_flag_link(m["t1"])}" style="width: 20px; height: 15px;"> '
                    f'{m["t1"][:10]} - {m["t2"][:10]} '
                    f'<img src="{get_flag_link(m["t2"])}" style="width: 20px; height: 15px;">'
                f'</span>'
                f'<span style="font-weight: 900; color: #cc0000; font-size: 14px;">[{voto["1X2"]}] ({voto["ris"]})</span>'
                '</div>'
            )

        if giocate_effettuate == 0:
            testo_ricevuta += '<p style="text-align:center; font-family:monospace; color:#cc0000; padding: 10px 0;">⚠️ Nessun pronostico inserito.</p>'

        testo_ricevuta += '</div>'
        
        # Pulizia totale dei ritorni a capo per evitare bug di rendering in Streamlit
        testo_ricevuta = testo_ricevuta.replace("\n", "")
        
        # Rendering finale
        st.markdown(testo_ricevuta, unsafe_allow_html=True)
        st.caption(f"Visualizzazione Smart: mostrati solo i {giocate_effettuate} match compilati.")
        
        c_mod, c_save = st.columns(2)
        with c_mod:
            if st.button("🔄 Torna a Modificare", use_container_width=True):
                st.session_state.mostra_ricevuta = False
                st.rerun()
        with c_save:
            st.markdown('<div class="btn-save">', unsafe_allow_html=True)
            if st.button("🚀 INVIA PRONOSTICI 🚀", use_container_width=True):
                righe = []
                ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                for m in partite:
                    k = f"{m['t1']}_vs_{m['t2']}"
                    voto = st.session_state.giocate_live[k]
                    righe.append({
                        "Data": ts, "Utente_Telegram": telegram_user, "Giornata": st.session_state.giornata,
                        "Partita": k, "Pronostico_Segno": voto["1X2"], "Pronostico_Risultato": voto["ris"]
                    })
                df_nuovo_live = pd.DataFrame(righe)
                worksheet = sh.worksheet("SchedineLive")
                try:
                    records = worksheet.get_all_records()
                    df_esistente_live = pd.DataFrame(records)
                except Exception:
                    df_esistente_live = pd.DataFrame(columns=["Data", "Utente_Telegram", "Giornata", "Partita", "Pronostico_Segno", "Pronostico_Risultato"])
                
                df_finale_live = pd.concat([df_esistente_live, df_nuovo_live], ignore_index=True)
                worksheet.clear()
                worksheet.update([df_finale_live.columns.values.tolist()] + df_finale_live.fillna("").values.tolist())
                st.success("Salvataggio completato sul Database!")
                st.balloons()
            st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# SEZIONE CLASSIFICHE
# ==========================================
# ==========================================
# SEZIONE 2: CLASSIFICA COMPUTATA "AL VOLO"
# ==========================================
# ==========================================
# SEZIONE CLASSIFICHE (COMPUTATA AL VOLO)
# ==========================================
# ==========================================
# SEZIONE CLASSIFICHE (GRAFICA AGGIORNATA)
# ==========================================
elif st.session_state.pagina_corrente == "CLASSIFICA":
    st.markdown("<h3 style='text-align: center; font-weight: 800; margin-bottom: 20px;'>🏆 Classifica Generale Live</h3>", unsafe_allow_html=True)
    
    try:
        ws_risultati = sh.worksheet("RisultatiUfficiali")
        ws_live = sh.worksheet("SchedineLive")
        ws_gironi = sh.worksheet("Gironi")

        df_res = pd.DataFrame(ws_risultati.get_all_records())
        df_live = filtra_giocate_valide(pd.DataFrame(ws_live.get_all_records()))
        df_gironi = pd.DataFrame(ws_gironi.get_all_records())

        punteggi_utenti = {}

        if not df_res.empty:
            partite_reali = dict(zip(df_res[df_res['Tipo']=='Partita']['Chiave_Evento'], df_res[df_res['Tipo']=='Partita']['Valore_1']))
            risultati_reali = dict(zip(df_res[df_res['Tipo']=='Partita']['Chiave_Evento'], df_res[df_res['Tipo']=='Partita']['Valore_2']))
            podio_gironi = dict(zip(df_res[df_res['Tipo']=='Pos_Girone']['Chiave_Evento'], zip(df_res[df_res['Tipo']=='Pos_Girone']['Valore_1'], df_res[df_res['Tipo']=='Pos_Girone']['Valore_2'])))
            squadre_eliminate = df_res[df_res['Tipo']=='Eliminatoria']['Valore_2'].str.lower().str.strip().tolist()
            fasi_eliminate = dict(zip(df_res[df_res['Tipo']=='Eliminatoria']['Valore_2'].str.lower().str.strip(), df_res[df_res['Tipo']=='Eliminatoria']['Valore_1']))

            if not df_live.empty:
                df_live = df_live.sort_values(by="Data")
                df_live_grouped = df_live.groupby(['Utente_Telegram', 'Partita']).last().reset_index()
                
                for _, row in df_live_grouped.iterrows():
                    u = row['Utente_Telegram']
                    p = row['Partita']
                    prono_segno = str(row['Pronostico_Segno']).strip()
                    prono_risultato = str(row['Pronostico_Resultato'] if 'Pronostico_Resultato' in row else row.get('Pronostico_Risultato', '')).strip()
                    
                    if u not in punteggi_utenti:
                        punteggi_utenti[u] = {"Gironi_1X2": 0, "Risultati_Esatti": 0, "Podio_Bonus": 0, "Eliminatorie": 0, "Totale": 0}
                    
                    if p in partite_reali and str(partite_reali[p]).strip() == prono_segno:
                        punteggi_utenti[u]["Gironi_1X2"] += 1
                    if p in risultati_reali and str(risultati_reali[p]).strip() == prono_risultato:
                        punteggi_utenti[u]["Risultati_Esatti"] += 3

            if not df_gironi.empty:
                df_gironi = df_gironi.sort_values(by="Data")
                for u, gruppo_utente in df_gironi.groupby('Utente_Telegram'):
                    if u not in punteggi_utenti:
                        punteggi_utenti[u] = {"Gironi_1X2": 0, "Risultati_Esatti": 0, "Podio_Bonus": 0, "Eliminatorie": 0, "Totale": 0}
                    
                    ultimo_timestamp = gruppo_utente["Data"].max()
                    ultime_giocate_g = gruppo_utente[gruppo_utente["Data"] == ultimo_timestamp]
                    
                    for chiave_g, (r1, r2) in podio_gironi.items():
                        # QUI: riga corretta senza il refuso 'rollback'
                        lettera = chiave_g.replace("Pos_Girone_", "")
                        giocate_del_girone = ultime_giocate_g[ultime_giocate_g["Girone"] == lettera] if "Girone" in ultime_giocate_g.columns else pd.DataFrame()
                        giocate_del_girone = ultime_giocate_g[ultime_giocate_g["Girone"] == lettera] if "Girone" in ultime_giocate_g.columns else pd.DataFrame()
                        
                        if not giocate_del_girone.empty:
                            p1 = str(giocate_del_girone[giocate_del_girone["Posizione"].astype(str) == "1"]["Squadra_Pronosticata"].values[0]).strip() if not giocate_del_girone[giocate_del_girone["Posizione"].astype(str) == "1"].empty else ""
                            p2 = str(giocate_del_girone[giocate_del_girone["Posizione"].astype(str) == "2"]["Squadra_Pronosticata"].values[0]).strip() if not giocate_del_girone[giocate_del_girone["Posizione"].astype(str) == "2"].empty else ""
                            if p1 == str(r1).strip() and p2 == str(r2).strip():
                                punteggi_utenti[u]["Podio_Bonus"] += 2

                    for _, row_g in ultime_giocate_g.iterrows():
                        squadra_scelta = str(row_g["Squadra_Pronosticata"]).lower().strip()
                        if squadra_scelta in squadre_eliminate:
                            fase_raggiunta = fasi_eliminate[squadra_scelta]
                            if fase_raggiunta in ["Ottavi", "Quarti", "Semifinale"]:
                                punteggi_utenti[u]["Eliminatorie"] += 2
                            elif fase_raggiunta == "Finalista":
                                punteggi_utenti[u]["Eliminatorie"] += 4
                            elif fase_raggiunta == "Campione":
                                punteggi_utenti[u]["Eliminatorie"] += 7

        if punteggi_utenti:
            for u in punteggi_utenti:
                punteggi_utenti[u]["Totale"] = (punteggi_utenti[u]["Gironi_1X2"] + 
                                                punteggi_utenti[u]["Risultati_Esatti"] + 
                                                punteggi_utenti[u]["Podio_Bonus"] + 
                                                punteggi_utenti[u]["Eliminatorie"])
                
            df_c = pd.DataFrame.from_dict(punteggi_utenti, orient='index').reset_index()
            df_c.columns = ["Utente Telegram", "Esiti 1X2", "Totogol", "Bonus Podio", "Tabellone", "PUNTEGGIO TOTALE"]
            df_c = df_c.sort_values(by="PUNTEGGIO TOTALE", ascending=False).reset_index(drop=True)
            
            df_c.index = df_c.index + 1
            df_c.insert(0, "Pos.", df_c.index)
            df_c["Pos."] = df_c["Pos."].apply(lambda x: "🥇 1°" if x==1 else "🥈 2°" if x==2 else "🥉 3°" if x==3 else f"🏃 {x}°")

            # INTERFACCIA STYLING STREAMLIT AVANZATA
            # --- RENDERING COMPATTO E ACCATTIVANTE IN HTML/CSS (NO SCROLL) ---
            # --- RENDERING HTML/CSS OTTIMIZZATO (CON CONTRASTO CORRETTO) ---
            html_classifica = """
            <style>
                .classifica-container {
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                    width: 100%;
                    margin: 15px 0;
                    border-collapse: separate;
                    border-spacing: 0;
                    background: #ffffff;
                    border-radius: 12px;
                    overflow: hidden;
                    box-shadow: 0 4px 16px rgba(0,0,0,0.06);
                    font-size: 13px;
                    border: 1px solid #e1e4e6;
                }
                .classifica-header {
                    background: linear-gradient(135deg, #009933, #007722);
                    color: #ffffff !important;
                    font-weight: 700;
                    text-transform: uppercase;
                    font-size: 11px;
                    letter-spacing: 0.8px;
                }
                .classifica-header th {
                    padding: 14px 6px;
                    text-align: center;
                    color: #ffffff !important; /* Forza il testo bianco per contrasto perfetto */
                    vertical-align: middle;
                }
                .classifica-header th.align-left {
                    text-align: left;
                    padding-left: 16px;
                }
                .classifica-row {
                    border-bottom: 1px solid #edf0f2;
                }
                .classifica-row:last-child {
                    border-bottom: none;
                }
                .classifica-row td {
                    padding: 12px 6px;
                    text-align: center;
                    color: #333333;
                    vertical-align: middle;
                }
                .classifica-row td.align-left {
                    text-align: left;
                    padding-left: 16px;
                    font-weight: 600;
                    color: #1a1a1a;
                }
                .pos-col { width: 14%; font-size: 14px; font-weight: bold; }
                .user-col { width: 32%; }
                .punti-col { width: 10%; font-weight: 500; }
                .tot-col { 
                    width: 14%; 
                    font-weight: 700; 
                    color: #009933; 
                    font-size: 15px; 
                    background-color: #f4fbf6;
                }
                /* Stile intestazione TOT per uniformità */
                .classifica-header th.tot-header {
                    background: #006611;
                    color: #ffffff !important;
                }
            </style>
            <table class="classifica-container">
                <tr class="classifica-header">
                    <th class="pos-col">POS</th>
                    <th class="user-col align-left">PARTECIPANTE</th>
                    <th class="punti-col">1X2</th>
                    <th class="punti-col">GOAL</th>
                    <th class="punti-col">PODIO</th>
                    <th class="punti-col">FASE</th>
                    <th class="tot-col tot-header">TOT</th>
                </tr>
            """

            for _, row in df_c.iterrows():
                pos = row["Pos."]
                utente = row["Utente Telegram"]
                p_1x2 = row["Esiti 1X2"]
                p_totogol = row["Totogol"]
                p_podio = row["Bonus Podio"]
                p_tabellone = row["Tabellone"]
                p_totale = row["PUNTEGGIO TOTALE"]

                html_classifica += f"""
                <tr class="classifica-row">
                    <td class="pos-col">{pos}</td>
                    <td class="user-col align-left">{utente}</td>
                    <td class="punti-col">{p_1x2}</td>
                    <td class="punti-col">{p_totogol}</td>
                    <td class="punti-col">{p_podio}</td>
                    <td class="punti-col">{p_tabellone}</td>
                    <td class="tot-col">{p_totale}</td>
                </tr>
                """

            html_classifica += "</table>"
            
            st.markdown(html_classifica.replace("\n", ""), unsafe_allow_html=True)
        else:
            st.info("⏳ In attesa del caricamento delle giocate per calcolare i dati live.")

    except Exception as e:
        st.error(f"⚠️ Errore nel calcolo della classifica: {e}")