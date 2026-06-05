import streamlit as st
import pandas as pd
import os
from datetime import datetime
import gspread


# --- INIZIALIZZAZIONE STATO (METTI QUESTO SUBITO DOPO GLI IMPORT) ---
if "cedola" not in st.session_state:
    st.session_state.cedola = {}
if "utente" not in st.session_state:
    st.session_state.utente = ""
if "giornata" not in st.session_state:
    st.session_state.giornata = "Giornata 1 (11 - 17 Giugno)"
if "pagina_corrente" not in st.session_state:
    st.session_state.pagina_corrente = "GIOCA"
if "match_idx" not in st.session_state:
    st.session_state.match_idx = None

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Mundial&Me Live", page_icon="⚽", layout="centered", initial_sidebar_state="collapsed")
# --- ENGINE CSS CUSTOM ---
st.markdown("""
<style>
    /* 1. Blocca la Dark Mode forzata del browser (fondamentale per mobile) */
    :root {
        color-scheme: light only;
    }

    /* 2. CONFIGURAZIONE BASE (LIGHT MODE) */
    .stApp { 
        background-color: #f9ebdf !important; 
    }
    
    h1, h2, h3, h4, h5, h6, p, div, span, label, li { 
        color: #000000 !important; 
    }

    /* 3. MEDIA QUERY PER DARK MODE (Opzionale, ma ora rispettata) */
    @media (prefers-color-scheme: dark) {
        :root { color-scheme: dark; }
        .stApp { background-color: #262730 !important; }
        h1, h2, h3, h4, h5, h6, p, div, span, label, li { color: #ffffff !important; }
        .telegram-ballon {
            background-color: #1e3a1e !important; 
            border: 1px solid #4a7c4a !important;
            color: #ffffff !important;
        }
    }

    /* 4. Nascondi elementi Streamlit */
    #MainMenu, footer, header { visibility: hidden !important; }

    /* 5. Componenti personalizzati */
    .telegram-ballon {
        background-color: #effdde; padding: 15px; border-radius: 15px;
        border-bottom-left-radius: 0; margin-bottom: 20px;
        border: 1px solid #c9e4b7; color: #000000; font-family: monospace;
    }
    .match-row { display: flex; justify-content: space-between; padding: 5px 0; border-bottom: 1px solid #dcdcdc; }
</style>
""", unsafe_allow_html=True)


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

def is_partita_aperta(match_dict):
    # Ricostruiamo la data intera usando le tue chiavi 'data' e 'ora'
    # Esempio: data="27/06", ora="17:00" -> anno=2026
    try:
        data_str = f"2026/{match_dict['data']} {match_dict['ora']}"
        inizio_partita = datetime.strptime(data_str, '%Y/%d/%m %H:%M')
        return datetime.now() < inizio_partita
    except Exception as e:
        print(f"Errore orario: {e}")
        return False # Se c'è un errore, per sicurezza blocchiamo la giocata
 
def is_giornata_valida(nome_giornata):
    # Estraiamo le date dal nome, es: "Giornata 1 (11 - 17 Giugno)"
    try:
        data_str = nome_giornata.split('(')[1].replace(')', '').split('-')[1].strip()
        # Assumiamo l'anno corrente (2026)
        data_fine = datetime.strptime(f"{data_str} 2026", "%d %B %Y")
        return data_fine >= datetime.now()
    except:
        return True # Se fallisce, mostra tutto per sicurezza
    
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
        if segno == "1" and gol_casa <= gol_trasf: return False, "Segno 1 richiede gol casa > gol trasferta."
        if segno == "2" and gol_trasf <= gol_casa: return False, "Segno 2 richiede gol trasferta > gol casa."
        if segno == "X" and gol_casa != gol_trasf: return False, "Segno X richiede pareggio."
        return True, ""
    except ValueError: return False, "Inserisci solo numeri separati da '-'."



def invia_a_sheets(cedola, utente):
    # 1. Connessione a Google Sheets
    # Assicurati di avere il file 'credentials.json' nella cartella del progetto
    ws = sh.worksheet("SchedineLive")
    
    data_invio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    righe_da_aggiungere = []
    
    for match, pronostico in cedola.items():
        righe_da_aggiungere.append([
            data_invio,
            utente,
            st.session_state.giornata, # O st.session_state.giornata
            match,
            pronostico["1X2"],
            pronostico["ris"]
        ])
    
    # 2. Scrittura Batch (più efficiente di append_row singolo)
    if righe_da_aggiungere:
        ws.append_rows(righe_da_aggiungere)

def vai_alla_home():
    st.session_state.pagina_corrente = "GIOCA"
    st.session_state.mostra_ricevuta = False
    # Eventuale pulizia dello stato partita
    if "partita_attiva" in st.session_state:
        del st.session_state.partita_attiva

# --- BRANDING HEADER ---
# --- INIZIALIZZAZIONE STATO ---

# --- BRANDING HEADER ---
# --- BRANDING HEADER ---
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
st.markdown("<br>", unsafe_allow_html=True)

# --- NAVIGAZIONE PRINCIPALE ---

# col_nav1, col_nav2 = st.columns(2)
# with col_nav1:
#     # if st.button("📝 COMPILA SCHEDINA", use_container_width=True):
#     #     st.session_state.pagina_corrente = "GIOCA"
#     #     st.rerun()
#     #     --- AREA INVIO (POSIZIONATA IN CIMA O SUBITO DOPO IL LOGO) ---
#     st.markdown("---")
#     # Usiamo un container per isolare l'invio
#     with st.container(border=True):
#         st.subheader("🚀 Controllo Cedola")
#         if not st.session_state.cedola:
#             st.write("La cedola è vuota.")
#         else:
#             if st.button("INVIA SCHEDINA DEFINITIVA", type="primary", use_container_width=True):
#                 # STAMPA IMMEDIATA A CONSOLE (Devi vedere questo nel terminale)
#                 print("--- CLICK RILEVATO ---") 
                
#                 # Debug visivo obbligatorio
#                 st.toast("Invio in corso...", icon="⏳")
                
#                 try:
#                     # Carichiamo gspread qui per essere sicuri
#                     # gc = gspread.service_account(filename='credentials.json')
#                     # sh = gc.open("Mondiali2026_Database")
#                     worksheet = sh.worksheet("SchedineLive")
                    
#                     ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#                     righe = [[ts, st.session_state.utente, st.session_state.giornata, k, v["1X2"], v["ris"]] 
#                             for k, v in st.session_state.cedola.items()]
                    
#                     worksheet.append_rows(righe)
                    
#                     st.session_state.cedola = {}
#                     st.success("✅ Salvato!")
#                     st.balloons()
#                     st.rerun()
#                 except Exception as e:
#                     st.error(f"ERRORE CRITICO: {e}")
# with col_nav2:
#     if st.button("🏆 CLASSIFICA LIVE", use_container_width=True):
#         st.session_state.pagina_corrente = "CLASSIFICA"
#         st.rerun()
# st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<hr style='margin-top:10px; margin-bottom:15px; border:0; border-top:1px solid #ebdccf;'>", unsafe_allow_html=True)


# --- INSERIMENTO NOME ---
st.session_state.utente = st.text_input("👤 Il tuo Nome Telegram", value=st.session_state.utente, placeholder="Es: @MarioRossi")

#
giornate_disponibili = [g for g in CALENDARIO_GIORNATE.keys() if is_giornata_valida(g)]

# Se non ci sono giornate future, mostriamo un avviso o l'ultima
if not giornate_disponibili:
    st.warning("Il torneo è concluso!")
    giornate_disponibili = list(CALENDARIO_GIORNATE.keys())

# --- SELECTBOX DINAMICO ---
# Impostiamo di default la prima della lista (la più vicina temporalmente)
giornata_scelta = st.selectbox(
    "📅 Seleziona il turno:", 
    options=giornate_disponibili,
    index=0 
)
st.session_state.giornata = giornata_scelta

# ==========================================
# SEZIONE GIOCO
# ==========================================
if st.session_state.pagina_corrente == "GIOCA":
  # --- CEDOLA STICKY (Sempre in alto) ---
    with st.container(border=True):
        st.subheader("🎫 La tua Cedola Live")
        if not st.session_state.cedola:
            st.info("La tua cedola è attualmente vuota. Seleziona una partita qui sotto!")
        else:
            # Visualizzazione "Ricevuta" per lo screenshot
            st.markdown(f"""
            <div style="background: #fdfdfd; border: 2px solid #333; padding: 15px; font-family: 'Courier New', monospace;">
                <h4 style="text-align:center; border-bottom: 1px solid #333;">RICEVUTA PROVVISORIA</h4>
                <p><b>Utente:</b> {st.session_state.utente}</p>
                {"".join([f"<p>{m} : <b>{v['1X2']} ({v['ris']})</b></p>" for m, v in st.session_state.cedola.items()])}
                <hr>
                <p style="text-align:center; font-size:10px;">FAI UNO SCREENSHOT E INVIALO SU TELEGRAM!</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🚀 INVIA SCHEDINA", type="primary", use_container_width=True):
                # LOGICA DI INVIO A GOOGLE SHEETS
                with st.spinner("Invio in corso..."):
                    invia_a_sheets(st.session_state.cedola, st.session_state.utente)
                st.success("✅ Schedina inviata! Fai lo screenshot e condividilo su Telegram!")
                st.balloons()
                
                # 3. NON svuotare subito la cedola!
                # Creiamo un bottone "Pulisci" che appare SOLO dopo l'invio riuscito
                if st.button("OK, ho fatto lo screenshot, pulisci tutto"):
                    st.session_state.cedola = {}
                    st.rerun()
                    
                # Fermiamo l'esecuzione qui per non far sparire la ricevuta
                st.stop()

    # --- LISTA PARTITE (Allineate) ---
    st.markdown("---")
    partite = CALENDARIO_GIORNATE[st.session_state.giornata]
    
    def get_flag(team_name):
        return FLAGS.get(team_name, {}).get("emoji", "⚽")

# --- LISTA PARTITE ---
    for i, m in enumerate(partite):
        match_key = f"{m['t1']} vs {m['t2']}"
        
        # Costruzione etichetta bottone
        f1 = get_flag(m['t1'])
        f2 = get_flag(m['t2'])
        btn_label = f"{f1} {m['t1']} vs {m['t2']} {f2}"
        
        # Centratura: Usiamo 3 colonne [1, 2, 1] per lasciare i lati vuoti
        col_l, col_c, col_r = st.columns([1, 4, 1])
        
        with col_c:
            if not is_partita_aperta(m):
                st.button(f"🔒 {btn_label}", disabled=True, use_container_width=True)
            else:
                if st.button(btn_label, key=f"btn_{i}", use_container_width=True):
                    st.session_state.match_idx = i
                    st.rerun()

        # Espansione form di inserimento (sempre centrata sotto il bottone)
        if st.session_state.match_idx == i:
            with st.container():
                st.markdown(f"<div style='text-align: center;'><h4>{btn_label}</h4></div>", unsafe_allow_html=True)
            with st.expander("📝 Inserisci Pronostico", expanded=True):
                c1, c2 = st.columns(2)
                with c1:
                    segno = st.radio("Segno", ["1", "X", "2"], horizontal=True, key=f"s_{i}")
                with c2:
                    ris = st.text_input("Ris. Esatto", key=f"r_{i}")
                
                if st.button("➕ Aggiungi alla Cedola", key=f"add_{i}"):
                    # Chiamiamo la funzione di convalida
                    is_valid, msg = convalida_risultato(segno, ris)
                    
                    if not st.session_state.utente:
                        st.error("Inserisci prima il tuo Nome Telegram!")
                    elif not is_valid:
                        # Mostriamo l'errore specifico (es. "Segno X richiede pareggio")
                        st.warning(f"⚠️ {msg}")
                    else:
                        # Tutto ok, aggiungiamo alla cedola
                        st.session_state.cedola[match_key] = {"1X2": segno, "ris": ris}
                        st.success("Aggiunto!")
                        st.rerun()
    # if st.button("🚀 INVIA SCHEDINA DEFINITIVA", type="primary", use_container_width=True):
    #     print(f"Debug: Utente = {st.session_state.utente}")
    #     print(f"Debug: Cedola = {st.session_state.cedola}")
    #     # Debug 1: Controlla cosa stiamo inviando
    #     st.write(f"Debug: Utente = {st.session_state.utente}")
    #     st.write(f"Debug: Cedola = {st.session_state.cedola}")
        
    #     if not st.session_state.utente:
    #         st.error("Errore: Il nome Telegram è vuoto!")
    #     elif not st.session_state.cedola:
    #         st.warning("Errore: La cedola è vuota!")
    #     else:
    #         try:
    #             # Debug 2: Conferma avvio invio
    #             st.info("Tentativo di invio al database...")
                
    #             # --- TUA FUNZIONE DI INVIO ---
    #             ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #             righe_da_aggiungere = []
                
    #             for match_key, voto in st.session_state.cedola.items():
    #                 righe_da_aggiungere.append([ts, st.session_state.utente, st.session_state.giornata, match_key, voto["1X2"], voto["ris"]])
                
    #             # Inizializza la connessione qui (o assicurati che 'sh' sia definito globalmente)
    #             # gc = gspread.service_account(filename='credentials.json')
    #             # sh = gc.open("Mondiali2026_Database")
                
    #             worksheet = sh.worksheet("SchedineLive")
    #             worksheet.append_rows(righe_da_aggiungere)
                
    #             # Reset
    #             st.session_state.cedola = {}
    #             st.success("✅ Inviato!")
    #             st.balloons()
    #             st.rerun()
                
    #         except Exception as e:
    #             # Questo è il punto critico: qui vedrai l'errore reale
    #             st.error(f"Errore tecnico: {e}")
    if st.button("🗑️ Svuota Schedina"):
        st.session_state.cedola = {}
        st.rerun()
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