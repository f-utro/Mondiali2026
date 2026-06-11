import streamlit as st
import pandas as pd
import os
import json
import gspread

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.set_page_config(page_title="Classifica Ufficiale 🏆", page_icon="🏆", layout="wide")

# --- CONFIGURAZIONE GOOGLE SHEETS (GSPREAD) ---
URL_FOGLIO = "https://docs.google.com/spreadsheets/d/1eplWbGsR3lpAPawatIBuSp5ts20K4Nn-_QUqvE2Md-g/edit"
path_json_locale = "credenziali_google.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

CALENDARIO_GIORNATE = {
        "Giornata 1 (11 - 17 Giugno)": [
            {"t1": "Messico", "t2": "Sudafrica", "ora": "21:00", "data": "11/06"},
            {"t1": "Corea del Sud", "t2": "Rep. Ceca", "ora": "02:00", "data": "12/06"},
            {"t1": "Canada", "t2": "Bosnia ed Erzegovina", "ora": "21:00", "data": "12/06"},
            {"t1": "Stati Uniti", "t2": "Paraguay", "ora": "01:00", "data": "13/06"},
            {"t1": "Qatar", "t2": "Svizzera", "ora": "20:00", "data": "13/06"},
            {"t1": "Brasile", "t2": "Marocco", "ora": "00:00", "data": "14/06"},
            {"t1": "Haiti", "t2": "Scozia", "ora": "03:00", "data": "14/06"},
            {"t1": "Australia", "t2": "Turchia", "ora": "06:00", "data": "14/06"},
            {"t1": "Germania", "t2": "Curaçao", "ora": "17:00", "data": "14/06"},
            {"t1": "Paesi Bassi", "t2": "Giappone", "ora": "20:00", "data": "14/06"},
            {"t1": "Costa d'Avorio", "t2": "Ecuador", "ora": "01:00", "data": "15/06"},
            {"t1": "Svezia", "t2": "Tunisia", "ora": "04:00", "data": "15/06"},
            {"t1": "Belgio", "t2": "Egitto", "ora": "21:00", "data": "15/06"},
            {"t1": "Iran", "t2": "Nuova Zelanda", "ora": "03:00", "data": "16/06"},
            {"t1": "Spagna", "t2": "Capo Verde", "ora": "18:00", "data": "15/06"},
            {"t1": "Arabia Saudita", "t2": "Uruguay", "ora": "00:00", "data": "16/06"},
            {"t1": "Francia", "t2": "Senegal", "ora": "21:00", "data": "16/06"},
            {"t1": "Iraq", "t2": "Norvegia", "ora": "00:00", "data": "17/06"},
            {"t1": "Argentina", "t2": "Algeria", "ora": "03:00", "data": "17/06"},
            {"t1": "Austria", "t2": "Giordania", "ora": "06:00", "data": "17/06"},
            {"t1": "Inghilterra", "t2": "Croazia", "ora": "22:00", "data": "17/06"},
            {"t1": "Ghana", "t2": "Panama", "ora": "01:00", "data": "18/06"},
            {"t1": "Portogallo", "t2": "RD del Congo", "ora": "18:00", "data": "17/06"},
            {"t1": "Uzbekistan", "t2": "Colombia", "ora": "04:00", "data": "18/06"}
        ],
        "Giornata 2 (18 - 23 Giugno)": [
            {"t1": "Rep. Ceca", "t2": "Sudafrica", "ora": "18:00", "data": "18/06"},
            {"t1": "Messico", "t2": "Corea del Sud", "ora": "01:00", "data": "19/06"},
            {"t1": "Svizzera", "t2": "Bosnia ed Erzegovina", "ora": "18:00", "data": "18/06"},
            {"t1": "Canada", "t2": "Qatar", "ora": "21:00", "data": "18/06"},
            {"t1": "Scozia", "t2": "Marocco", "ora": "23:00", "data": "19/06"},
            {"t1": "Brasile", "t2": "Haiti", "ora": "03:00", "data": "20/06"},
            {"t1": "Stati Uniti", "t2": "Australia", "ora": "21:00", "data": "19/06"},
            {"t1": "Turchia", "t2": "Paraguay", "ora": "06:00", "data": "20/06"},
            {"t1": "Germania", "t2": "Costa d'Avorio", "ora": "22:00", "data": "20/06"},
            {"t1": "Ecuador", "t2": "Curaçao", "ora": "02:00", "data": "21/06"},
            {"t1": "Paesi Bassi", "t2": "Svezia", "ora": "18:00", "data": "20/06"},
            {"t1": "Tunisia", "t2": "Giappone", "ora": "04:00", "data": "21/06"},
            {"t1": "Belgio", "t2": "Iran", "ora": "21:00", "data": "21/06"},
            {"t1": "Nuova Zelanda", "t2": "Egitto", "ora": "03:00", "data": "22/06"},
            {"t1": "Spagna", "t2": "Arabia Saudita", "ora": "18:00", "data": "21/06"},
            {"t1": "Uruguay", "t2": "Capo Verde", "ora": "00:00", "data": "22/06"},
            {"t1": "Francia", "t2": "Iraq", "ora": "23:00", "data": "22/06"},
            {"t1": "Norvegia", "t2": "Senegal", "ora": "02:00", "data": "23/06"},
            {"t1": "Argentina", "t2": "Austria", "ora": "19:00", "data": "22/06"},
            {"t1": "Giordania", "t2": "Algeria", "ora": "05:00", "data": "23/06"},
            {"t1": "Portogallo", "t2": "Uzbekistan", "ora": "18:00", "data": "23/06"},
            {"t1": "Colombia", "t2": "RD del Congo", "ora": "02:00", "data": "24/06"},
            {"t1": "Inghilterra", "t2": "Ghana", "ora": "22:00", "data": "23/06"},
            {"t1": "Panama", "t2": "Croazia", "ora": "01:00", "data": "24/06"}
        ],
        "Giornata 3 (24 - 27 Giugno)": [
            {"t1": "Rep. Ceca", "t2": "Messico", "ora": "01:00", "data": "25/06"},
            {"t1": "Sudafrica", "t2": "Corea del Sud", "ora": "01:00", "data": "25/06"},
            {"t1": "Svizzera", "t2": "Canada", "ora": "18:00", "data": "24/06"},
            {"t1": "Bosnia ed Erzegovina", "t2": "Qatar", "ora": "18:00", "data": "24/06"},
            {"t1": "Scozia", "t2": "Brasile", "ora": "00:00", "data": "25/06"},
            {"t1": "Marocco", "t2": "Haiti", "ora": "00:00", "data": "25/06"},
            {"t1": "Turchia", "t2": "Stati Uniti", "ora": "04:00", "data": "26/06"},
            {"t1": "Paraguay", "t2": "Australia", "ora": "04:00", "data": "26/06"},
            {"t1": "Curaçao", "t2": "Costa d'Avorio", "ora": "22:00", "data": "25/06"},
            {"t1": "Ecuador", "t2": "Germania", "ora": "23:00", "data": "25/06"},
            {"t1": "Giappone", "t2": "Svezia", "ora": "01:00", "data": "26/06"},
            {"t1": "Tunisia", "t2": "Paesi Bassi", "ora": "23:00", "data": "25/06"},
            {"t1": "Egitto", "t2": "Iran", "ora": "03:00", "data": "27/06"},
            {"t1": "Nuova Zelanda", "t2": "Belgio", "ora": "03:00", "data": "27/06"},
            {"t1": "Capo Verde", "t2": "Arabia Saudita", "ora": "00:00", "data": "27/06"},
            {"t1": "Uruguay", "t2": "Spagna", "ora": "00:00", "data": "27/06"},
            {"t1": "Norvegia", "t2": "Francia", "ora": "21:00", "data": "26/06"},
            {"t1": "Senegal", "t2": "Iraq", "ora": "21:00", "data": "26/06"},
            {"t1": "Algeria", "t2": "Austria", "ora": "04:00", "data": "28/06"},
            {"t1": "Giordania", "t2": "Argentina", "ora": "04:00", "data": "28/06"},
            {"t1": "Colombia", "t2": "Portogallo", "ora": "23:30", "data": "27/06"},
            {"t1": "RD del Congo", "t2": "Uzbekistan", "ora": "02:30", "data": "28/06"},
            {"t1": "Panama", "t2": "Inghilterra", "ora": "23:00", "data": "27/06"},
            {"t1": "Croazia", "t2": "Ghana", "ora": "23:00", "data": "27/06"}
            ]
    }

from datetime import datetime
from zoneinfo import ZoneInfo

# def filtra_giocate_valide(df_live):
#     giocate_valide = []
#     fuso_roma = ZoneInfo("Europe/Rome")
#     anno = 2026 # Fissato per il torneo
    
#     for _, row in df_live.iterrows():
#         partita_nome = row["Partita"]
        
#         # 1. Recupero orario inizio partita dal calendario
#         orario_inizio = None
#         for giornata in CALENDARIO_GIORNATE:
#             for match in CALENDARIO_GIORNATE[giornata]:
#                 match_str = f"{match['t1']} vs {match['t2']}"
#                 if match_str == partita_nome:
#                     # Parsing della stringa oraria
#                     data_str = f"{anno}/{match['data']} {match['ora']}"
#                     dt_naive = datetime.strptime(data_str, '%Y/%d/%m %H:%M')
#                     # Rendiamo l'orario inizio consapevole del fuso
#                     orario_inizio = dt_naive.replace(tzinfo=fuso_roma)
#                     break
        
#         # 2. Parsing della data giocata dal CSV
#         try:
#             # Assumiamo che data_giocata nel CSV sia in UTC o locale, 
#             # se non ha fuso orario, gli assegniamo quello di Roma
#             dt_giocata_naive = datetime.strptime(row["Data_Invio"], '%Y-%m-%d %H:%M:%S')
#             data_giocata = dt_giocata_naive.replace(tzinfo=fuso_roma)
#         except:
#             continue

#         # 3. Confronto (ora entrambi gli oggetti sono 'aware')
#         if orario_inizio and data_giocata < orario_inizio:
#             giocate_valide.append(row)
            
#     return pd.DataFrame(giocate_valide)

def filtra_giocate_valide(df_live):
    giocate_valide = []
    fuso_roma = ZoneInfo("Europe/Rome")
    anno = 2026
    
    st.write("--- LOG DI DEBUG FILTRO ---")
    
    for _, row in df_live.iterrows():
        partita_nome = row["Partita"]
        orario_inizio = None
        
        # 1. Trova orario in calendario
        for giornata in CALENDARIO_GIORNATE:
            for match in CALENDARIO_GIORNATE[giornata]:
                if f"{match['t1']} vs {match['t2']}" == partita_nome:
                    data_str = f"{anno}/{match['data']} {match['ora']}"
                    dt_naive = datetime.strptime(data_str, '%Y/%d/%m %H:%M')
                    orario_inizio = dt_naive.replace(tzinfo=fuso_roma)
                    break
        
        # 2. Parsing Data Invio
        try:
            dt_invio = datetime.strptime(row["Data"], '%Y-%m-%d %H:%M:%S')
            data_giocata = dt_invio.replace(tzinfo=fuso_roma)
        except Exception as e:
            st.write(f"Errore parsing data {row['Data']}: {e}")
            continue

        # 3. Confronto con STAMPA (Questo ti dirà la verità!)
        if orario_inizio and data_giocata < orario_inizio:
     #       st.success(f"VALIDA: {partita_nome} (Invio: {data_giocata} < Inizio: {orario_inizio})")
            giocate_valide.append(row)
      #  else:
      #      st.error(f"SCARTATA: {partita_nome} (Invio: {data_giocata} >= Inizio: {orario_inizio})")
    #st.write(len(pd.DataFrame(giocate_valide)))      
    return pd.DataFrame(giocate_valide)

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

# Connessione al foglio master Google Sheets
gc = inizializza_gspread()
sh = gc.open_by_url(URL_FOGLIO)


# --- HEADER VINTAGE TOTOCALCIO COORDINATO ---
# col_logo, col_titolo = st.columns([1, 4])
# with col_logo:
#     st.markdown("""
#         <div style='border: 3px solid #009933; padding: 10px; text-align: center; border-radius: 5px; background-color: #f0fbf2;'>
#             <span style='color: #009933; font-weight: bold; font-size: 14px; font-family: sans-serif;'>CONCORSO</span><br>
#             <span style='color: #009933; font-weight: bold; font-size: 32px; line-height: 32px; font-family: monospace;'>J&M</span>
#         </div>
#     """, unsafe_allow_html=True)

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

# 🔄 CARICAMENTO DATI IN DIRETTA DA GOOGLE SHEETS
ws_risultati = sh.worksheet("RisultatiUfficiali")
ws_live = sh.worksheet("SchedineLive")
ws_gironi = sh.worksheet("Gironi")

try:
    df_res = pd.DataFrame(ws_risultati.get_all_records())
    df_live = filtra_giocate_valide(pd.DataFrame(ws_live.get_all_records()))
    df_gironi = pd.DataFrame(ws_gironi.get_all_records())
except Exception as e:
    st.error(f"Errore nel caricamento delle tabelle da Google Sheets: {e}")
    df_res = pd.DataFrame(columns=["Tipo", "Chiave_Evento", "Valore_1", "Valore_2"])
    df_live = pd.DataFrame()
    df_gironi = pd.DataFrame()

# --- BLOCCO DI CALCOLO DINAMICO ---
punteggi_utenti = {}

if not df_res.empty:
    #partite_reali = dict(zip(df_res[df_res['Tipo']=='Partita']['Chiave_Evento'], df_res[df_res['Tipo']=='Partita']['Valore_1']))
    #risultati_reali = dict(zip(df_res[df_res['Tipo']=='Partita']['Chiave_Evento'], df_res[df_res['Tipo']=='Partita']['Valore_2']))
    #partite_reali = {str(k).strip().lower(): str(v).strip() for k, v in zip(df_res[df_res['Tipo']=='Partita']['Chiave_Evento'], df_res[df_res['Tipo']=='Partita']['Valore_1'])}
    partite_reali = dict(zip(df_res[df_res['Tipo']=='Partita']['Chiave_Evento'], df_res[df_res['Tipo']=='Partita']['Valore_1']))
    risultati_reali = {str(k).strip().lower(): str(v).strip() for k, v in zip(df_res[df_res['Tipo']=='Partita']['Chiave_Evento'], df_res[df_res['Tipo']=='Partita']['Valore_2'])}
    podio_gironi = dict(zip(df_res[df_res['Tipo']=='Pos_Girone']['Chiave_Evento'], zip(df_res[df_res['Tipo']=='Pos_Girone']['Valore_1'], df_res[df_res['Tipo']=='Pos_Girone']['Valore_2'])))
    squadre_eliminate = df_res[df_res['Tipo']=='Eliminatoria']['Valore_2'].str.lower().str.strip().tolist()
    fasi_eliminate = dict(zip(df_res[df_res['Tipo']=='Eliminatoria']['Valore_2'].str.lower().str.strip(), df_res[df_res['Tipo']=='Eliminatoria']['Valore_1']))

    st.write("Chiavi risultati:", list(partite_reali.keys()))
    st.write("Tipi presenti nel file Risultati:", df_res['Tipo'].unique())        
    #st.write("Chiave esempio predizioni:", str(df_live.iloc[0]['Partita']).strip().lower())
    if not df_live.empty:
       st.write("Chiave esempio predizioni:", str(df_live.iloc[0]['Partita']).strip().lower())
    else:
       st.warning("⚠️ Il DataFrame df_live è vuoto! Nessuna giocata trovata dopo il filtro.")


    # 1. Calcolo da Schedine Live (Esito e Totogol)
    if not df_live.empty:
        df_live = df_live.sort_values(by="Data")
        df_live_grouped = df_live.groupby(['Utente_Telegram', 'Partita']).last().reset_index()

        st.write("--- DEBUG DELLE CHIAVI NEL DIZIONARIO RISULTATI ---")
# Stampiamo le prime 5 chiavi per vedere come sono scritte
        chiavi_test = list(partite_reali.keys())
        st.write(f"Chiavi caricate: {chiavi_test[:5]}")

# Controlliamo la partita specifica che fallisce
        # Sostituisci il tuo blocco del ciclo for con questo:
        for _, row in df_live_grouped.iterrows():
            u = row['Utente_Telegram']
            p = str(row['Partita']).strip().lower()
    
    # 1. Inizializzazione sicura dell'utente
            if u not in punteggi_utenti:
               punteggi_utenti[u] = {"Gironi_1X2": 0, "Risultati_Esatti": 0, "Podio_Bonus": 0, "Eliminatorie": 0, "Totale": 0}
    
    # 2. Controllo esistenza partita nel dizionario
            if p in partite_reali:
               reale_segno = str(partite_reali[p]).strip()
               prono_segno = str(row['Pronostico_Segno']).strip()
        
            if reale_segno == prono_segno:
               punteggi_utenti[u]["Gironi_1X2"] += 1
            
        # Controllo risultato esatto
            reale_ris = str(risultati_reali.get(p, "")).strip()
            prono_risultato = str(row.get('Pronostico_Risultato', '')).strip()
        
            if prono_risultato and prono_risultato == reale_ris:
               punteggi_utenti[u]["Risultati_Esatti"] += 3
        
        # for _, row in df_live_grouped.iterrows():
        #     u = row['Utente_Telegram']
        #     p = row['Partita']
        #     #prono_segno = str(row['Pronostico_Segno']).strip()
        #     #prono_risultato = str(row['Pronostico_Resultato'] if 'Pronostico_Resultato' in row else row.get('Pronostico_Risultato', '')).strip()
        #     prono_segno = str(row['Pronostico_Segno']).strip()
        #     prono_risultato = str(row.get('Pronostico_Risultato', '')).strip() # Corretto 'Risultato'
            
        #     if u not in punteggi_utenti:
        #         punteggi_utenti[u] = {"Gironi_1X2": 0, "Risultati_Esatti": 0, "Podio_Bonus": 0, "Eliminatorie": 0, "Totale": 0}
            
        #     #if p in partite_reali and str(partite_reali[p]).strip() == prono_segno:
        #     #    punteggi_utenti[u]["Gironi_1X2"] += 1
        #     #if prono_risultato.strip() !='':             
        #     #            if p in risultati_reali and str(risultati_reali[p]).strip() == prono_risultato:
        #     #                punteggi_utenti[u]["Risultati_Esatti"] += 3
        #     # 3. Confronto debuggato
        #     if p in partite_reali:
        #        reale_segno = partite_reali[p]
        #        if reale_segno == prono_segno:
        #           punteggi_utenti[u]["Gironi_1X2"] += 1
            
        #        if prono_risultato: # Se l'utente ha messo un risultato
        #           reale_ris = risultati_reali.get(p, "")
        #           if reale_ris == prono_risultato:
        #              punteggi_utenti[u]["Risultati_Esatti"] += 3

    # 2. Calcolo Classifica Finali Gironi (Bonus Podio +2)
    if not df_gironi.empty:
        df_gironi = df_gironi.sort_values(by="Data")
        
        for u, gruppo_utente in df_gironi.groupby('Utente_Telegram'):
            if u not in punteggi_utenti:
                punteggi_utenti[u] = {"Gironi_1X2": 0, "Risultati_Esatti": 0, "Podio_Bonus": 0, "Eliminatorie": 0, "Totale": 0}
            
            ultimo_timestamp = gruppo_utente["Data"].max()
            ultime_giocate_g = gruppo_utente[gruppo_utente["Data"] == ultimo_timestamp]
            
            for chiave_g, (r1, r2) in podio_gironi.items():
                lettera = chiave_g.replace("Pos_Girone_", "")
                giocate_del_girone = ultime_giocate_g[ultime_giocate_g["Girone"] == lettera] if "Girone" in ultime_giocate_g.columns else pd.DataFrame()
                
                if not giocate_del_girone.empty:
                    p1 = str(giocate_del_girone[giocate_del_girone["Posizione"].astype(str) == "1"]["Squadra_Pronosticata"].values[0]).strip() if not giocate_del_girone[giocate_del_girone["Posizione"].astype(str) == "1"].empty else ""
                    p2 = str(giocate_del_girone[giocate_del_girone["Posizione"].astype(str) == "2"]["Squadra_Pronosticata"].values[0]).strip() if not giocate_del_girone[giocate_del_girone["Posizione"].astype(str) == "2"].empty else ""
                    
                    if p1 == str(r1).strip() and p2 == str(r2).strip():
                        punteggi_utenti[u]["Podio_Bonus"] += 2

            # 3. Calcolo Punti Tabellone Intero per le Fasi Eliminatorie
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

# --- MOSTRA LA TABELLA CLASSIFICA ---
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
    #df_c["Pos."] = df_c["Pos"].apply(lambda x: "🥇 1°" if x==1 else "🥈 2°" if x==2 else "🥉 3°" if x==3 else f"🏃 {x}°")
    df_c["Pos."] = df_c["Pos."].apply(lambda x: "🥇 1°" if x==1 else "🥈 2°" if x==2 else "🥉 3°" if x==3 else f"🏃 {x}°")
    st.markdown("### 🏁 CLASSIFICA GENERALE TOTOJUVE&ME")
    
    # --- RENDERING HTML/CSS OTTIMIZZATO SENZA SCROLL ---
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
            font-weight: 700;
            text-transform: uppercase;
            font-size: 11px;
            letter-spacing: 0.8px;
        }
        .classifica-header th {
            padding: 14px 6px;
            text-align: center;
            color: #ffffff !important; /* Forza il testo bianco per il contrasto */
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
    st.info("⏳ In attesa del caricamento delle giocate e dei dati dell'Admin per calcolare la classifica.")
