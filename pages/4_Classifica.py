import streamlit as st
import pandas as pd
import os
import json
import gspread

st.set_page_config(page_title="Classifica Ufficiale 🏆", page_icon="🏆", layout="wide")

# --- CONFIGURAZIONE GOOGLE SHEETS (GSPREAD) ---
URL_FOGLIO = "https://docs.google.com/spreadsheets/d/1eplWbGsR3lpAPawatIBuSp5ts20K4Nn-_QUqvE2Md-g/edit"
path_json_locale = "credenziali_google.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

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

from datetime import datetime

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
col_left, col_center, col_right = st.columns([2, 1, 2])

with col_center:
    # Usiamo il logo "Nero" perché contiene già il nome del brand
    st.image("Mundial&Me Logo Nero.png", use_container_width=True)

# Separatore grafico che riprende il colore verde del tema
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
    partite_reali = dict(zip(df_res[df_res['Tipo']=='Partita']['Chiave_Evento'], df_res[df_res['Tipo']=='Partita']['Valore_1']))
    risultati_reali = dict(zip(df_res[df_res['Tipo']=='Partita']['Chiave_Evento'], df_res[df_res['Tipo']=='Partita']['Valore_2']))
    podio_gironi = dict(zip(df_res[df_res['Tipo']=='Pos_Girone']['Chiave_Evento'], zip(df_res[df_res['Tipo']=='Pos_Girone']['Valore_1'], df_res[df_res['Tipo']=='Pos_Girone']['Valore_2'])))
    squadre_eliminate = df_res[df_res['Tipo']=='Eliminatoria']['Valore_2'].str.lower().str.strip().tolist()
    fasi_eliminate = dict(zip(df_res[df_res['Tipo']=='Eliminatoria']['Valore_2'].str.lower().str.strip(), df_res[df_res['Tipo']=='Eliminatoria']['Valore_1']))

    # 1. Calcolo da Schedine Live (Esito e Totogol)
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