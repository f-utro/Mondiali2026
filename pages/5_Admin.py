import streamlit as st
import pandas as pd
import os
import json
import gspread

st.set_page_config(page_title="Pannello Admin 🛠️", page_icon="⚙️", layout="wide")

# --- CONFIGURAZIONE GOOGLE SHEETS (GSPREAD) ---
URL_FOGLIO = "https://docs.google.com/spreadsheets/d/1eplWbGsR3lpAPawatIBuSp5ts20K4Nn-_QUqvE2Md-g/edit"
path_json_locale = "credenziali_google.json"
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
    
# Connessione al foglio master
gc = inizializza_gspread()
sh = gc.open_by_url(URL_FOGLIO)

def get_admin_password():
    gc = inizializza_gspread() # La tua funzione già esistente
    sh = gc.open_by_url(URL_FOGLIO)
    ws = sh.worksheet("AdminConfig")
    data = ws.get_all_records()
    # Trova il valore dove Parametro è 'pwd_admin'
    row = next(item for item in data if item["Parametro"] == "pwd_admin")
    return str(row["Valore"])


# --- SICUREZZA ACCESSO ADMIN ---
PASSWORD_ADMIN = get_admin_password() #st.secrets["passwords"]["admin_password"]

if "is_admin" not in st.session_state:
    st.session_state["is_admin"] = False

if not st.session_state["is_admin"]:
    st.title("🔒 Accesso Amministratore")
    pwd = st.text_input("Inserisci la password di gestione:", type="password")
    if st.button("Accedi"):
        if pwd == PASSWORD_ADMIN:
            st.session_state["is_admin"] = True
            st.rerun()
        else:
            st.error("Password errata!")
else:
    # --- PANNELLO ADMIN ATTIVO ---
    st.title("🛠️ Pannello di Controllo Organizzatore — Juv&Me")
    st.write("Centrale di comando per gestire la community, inserire i risultati ufficiali e lanciare i post su Telegram.")
    
    # 🔄 CARICAMENTO DATI REALI PER IL CALCOLO LIVE DELLA CLASSIFICA
    ws_risultati = sh.worksheet("RisultatiUfficiali")
    ws_live = sh.worksheet("SchedineLive")
    ws_gironi = sh.worksheet("Gironi")
    
    try:
        df_res = pd.DataFrame(ws_risultati.get_all_records())
        df_live = pd.DataFrame(ws_live.get_all_records())
        df_gironi = pd.DataFrame(ws_gironi.get_all_records())
    except Exception as e:
        st.error(f"Errore nel caricamento delle tabelle da Google Sheets: {e}")
        df_res = pd.DataFrame(columns=["Tipo", "Chiave_Evento", "Valore_1", "Valore_2"])
        df_live = pd.DataFrame()
        df_gironi = pd.DataFrame()

    # --- DATI E STRUTTURA DEL TORNEO ---
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

    # Generazione automatica della lista partite dal calendario
    LISTA_PARTITE_COMPLETE = []
    for g_nome, match_list in CALENDARIO_GIORNATE.items():
        for m in match_list:
            LISTA_PARTITE_COMPLETE.append(f"{m['t1']} vs {m['t2']}")

    GRUPPI = sorted(list(squadre_gironi.keys()))

    # --- MOTORE DI CALCOLO INTERNO (Sincronizzato con Classifica) ---
    punteggi_utenti = {}
    if not df_res.empty:
        partite_reali = dict(zip(df_res[df_res['Tipo']=='Partita']['Chiave_Evento'], df_res[df_res['Tipo']=='Partita']['Valore_1']))
        risultati_reali = dict(zip(df_res[df_res['Tipo']=='Partita']['Chiave_Evento'], df_res[df_res['Tipo']=='Partita']['Valore_2']))
        podio_gironi = dict(zip(df_res[df_res['Tipo']=='Pos_Girone']['Chiave_Evento'], zip(df_res[df_res['Tipo']=='Pos_Girone']['Valore_1'], df_res[df_res['Tipo']=='Pos_Girone']['Valore_2'])))
        squadre_eliminate = df_res[df_res['Tipo']=='Eliminatoria']['Valore_2'].str.lower().str.strip().tolist()
        fasi_eliminate = dict(zip(df_res[df_res['Tipo']=='Eliminatoria']['Valore_2'].str.lower().str.strip(), df_res[df_res['Tipo']=='Eliminatoria']['Valore_1']))

        if not df_live.empty:
            df_live_sorted = df_live.sort_values(by="Data")
            df_live_grouped = df_live_sorted.groupby(['Utente_Telegram', 'Partita']).last().reset_index()
            for _, row in df_live_grouped.iterrows():
                u = row['Utente_Telegram']
                p = row['Partita']
                prono_segno = str(row['Pronostico_Segno']).strip()
                prono_risultato = str(row.get('Pronostico_Risultato', '')).strip()
                
                if u not in punteggi_utenti:
                    punteggi_utenti[u] = 0
                if p in partite_reali and str(partite_reali[p]).strip() == prono_segno:
                    punteggi_utenti[u] += 1
                if p in risultati_reali and str(resultados_reali := risultati_reali[p]).strip() == prono_risultato:
                    punteggi_utenti[u] += 3

        if not df_gironi.empty:
            df_gironi_sorted = df_gironi.sort_values(by="Data")
            df_gironi_last = df_gironi_sorted.groupby('Utente_Telegram').last().reset_index()
            for _, row in df_gironi_last.iterrows():
                u = row['Utente_Telegram']
                if u not in punteggi_utenti:
                    punteggi_utenti[u] = 0
                
                for chiave_g, (r1, r2) in podio_gironi.items():
                    lettera = chiave_g.replace("Pos_Girone_", "")
                    p1 = str(row.get(f"Girone_{lettera}_1", "")).strip()
                    p2 = str(row.get(f"Girone_{lettera}_2", "")).strip()
                    if p1 == str(r1).strip() and p2 == str(r2).strip():
                        punteggi_utenti[u] += 2

                for colonna_campo in row.index:
                    if "Girone_" in colonna_campo:
                        squadra_scelta = str(row[colonna_campo]).lower().strip()
                        if squadra_scelta in squadre_eliminate:
                            fase_raggiunta = fasi_eliminate[squadra_scelta]
                            if fase_raggiunta in ["Ottavi", "Quarti", "Semifinale"]:
                                punteggi_utenti[u] += 2
                            elif fase_raggiunta == "Finalista":
                                punteggi_utenti[u] += 4
                            elif fase_raggiunta == "Campione":
                                punteggi_utenti[u] += 7

    # Conversione in DataFrame ordinato
    if punteggi_utenti:
        df_classifica_reale = pd.DataFrame(list(punteggi_utenti.items()), columns=["Utente_Telegram", "Punti"])
        df_classifica_reale = df_classifica_reale.sort_values(by="Punti", ascending=False).reset_index(drop=True)
    else:
        df_classifica_reale = pd.DataFrame(columns=["Utente_Telegram", "Punti"])

    # --- CREAZIONE TABS INTERFACCIA ---
    tab1, tab2, tab3, tab4 = st.tabs(["📲 Telegram Post", "🕵️‍♂️ Ispezione Giocate", "📝 Inserimento Esiti", "💾 Backup & Export"])

    # ==========================================
    # TAB 1: GENERATORE TELEGRAM REALE
    # ==========================================
    with tab1:
        st.subheader("📢 Generatore Post per la Chat Telegram")
        st.write("Genera la classifica attuale calcolata in tempo reale da Google Sheets, pronta da copiare.")
        
        if df_classifica_reale.empty:
            st.warning("⚠️ Nessun punteggio calcolato. Inserisci almeno un risultato reale nell'area esiti per sbloccare il testo.")
        else:
            if st.button("Genera Testo Classifica 📲", use_container_width=True):
                media_punti = df_classifica_reale["Punti"].mean()
                
                testo_telegram = "🏆 *AGGIORNAMENTO TOTO JUVE&ME* 🏆\n\n"
                testo_telegram += "Ecco la classifica ufficiale aggiornata in tempo reale! 👇🔥\n\n"
                
                for i, row in df_classifica_reale.iterrows():
                    medaglia = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "🏃‍♂️"
                    trend = "🚀" if row['Punti'] > media_punti + 3 else "⬆️" if row['Punti'] >= media_punti else "🔻"
                    
                    testo_telegram += f"{medaglia} {i+1}. @{row['Utente_Telegram']} — *{row['Punti']} PT* ({trend})\n"
                    
                testo_telegram += "\n💬 Chi sta gufando e chi salirà al prossimo turno?\n"
                testo_telegram += "🔗 Gioca la prossima schedina live qui: [Link della tua App]"
                
                st.text_area("Copia questo testo e incollalo nel gruppo Telegram:", value=testo_telegram, height=300)

    # ==========================================
    # TAB 2: ISPEZIONE GIOCATE UTENTI
    # ==========================================
    with tab2:
        st.subheader("🕵️‍♂️ Controllo e Ispezione Schedine")
        st.write("Seleziona un utente della community per vedere nel dettaglio cosa ha giocato.")
        
        tutti_utenti = sorted(list(set(df_live["Utente_Telegram"].tolist() + df_gironi["Utente_Telegram"].tolist()))) if not df_live.empty or not df_gironi.empty else []
        
        if not tutti_utenti:
            st.info("Nessun utente ha ancora inviato pronostici.")
        else:
            utente_scelto = st.selectbox("Scegli l'utente da controllare:", tutti_utenti)
            
            col_g, col_l = st.columns(2)
            with col_g:
                st.markdown("**🔮 Pronostici Gironi (Ultimo Invio Completo):**")
                if not df_gironi.empty:
                    giocate_utente_g = df_gironi[df_gironi["Utente_Telegram"] == utente_scelto]
                    
                    if not giocate_utente_g.empty:
                        ultimo_timestamp = giocate_utente_g["Data"].max()
                        giocate_g_complete = giocate_utente_g[giocate_utente_g["Data"] == ultimo_timestamp]
                        
                        st.dataframe(
                            giocate_g_complete.drop(columns=["Data", "Utente_Telegram"], errors="ignore"), 
                            use_container_width=True, 
                            hide_index=True
                        )
                    else:
                        st.caption("Nessun pronostico gironi trovato per questo utente.")
                else:
                    st.caption("Tabella gironi vuota.")
                    
            with col_l:
                st.markdown("**⚽ Schedine Live (Ultime giocate inserite):**")
                if not df_live.empty:
                    giocate_l = df_live[df_live["Utente_Telegram"] == utente_scelto].sort_values(by="Data", ascending=False)
                    if not giocate_l.empty:
                        st.dataframe(giocate_l, use_container_width=True, hide_index=True)
                    else:
                        st.caption("Nessuna giocata live trovata per questo utente.")
                else:
                    st.caption("Tabella live vuota.")

    # ==========================================
    # TAB 3: INSERIMENTO ESITI (MIGLIORATO CON SELECTBOX)
    # ==========================================
    with tab3:
        st.subheader("📝 Registrazione Risultati Ufficiali")
        st.write("Registra qui i risultati dei match giocati e i verdetti dei gironi. Saranno scritti direttamente su Google Sheets.")
        
        scelta_admin = st.radio("Cosa vuoi aggiornare?", ["Partite Live", "Classifiche Gironi"], horizontal=True)
        st.markdown("---")

        if scelta_admin == "Partite Live":
            with st.form("form_partite"):
                st.markdown("### ⚽ Esito Incontro")
                p_scelta = st.selectbox("Seleziona il Match:", LISTA_PARTITE_COMPLETE)
                
                c1, c2 = st.columns(2)
                with c1:
                    segno_reale = st.selectbox("Segno Finale (1X2):", ["1", "X", "2"])
                with c2:
                    ris_reale = st.text_input("Risultato Esatto (Formato es. 2-1 o 0-0):")
                
                if st.form_submit_button("💾 Salva Risultato Partita"):
                    if not ris_reale.strip():
                        st.error("⚠️ Inserisci il risultato esatto prima di salvare!")
                    else:
                        if not df_res.empty:
                            df_res = df_res[df_res['Chiave_Evento'] != p_scelta]
                        
                        nuovo_dato = pd.DataFrame([{"Tipo": "Partita", "Chiave_Evento": p_scelta, "Valore_1": segno_reale, "Valore_2": ris_reale}])
                        df_res = pd.concat([df_res, nuovo_dato], ignore_index=True)
                        
                        ws_risultati.clear()
                        ws_risultati.update([df_res.columns.values.tolist()] + df_res.fillna("").values.tolist())
                        st.success(f"✅ Risultato di {p_scelta} salvato con successo!")
                        st.rerun()

        elif scelta_admin == "Classifiche Gironi":
            # Usiamo uno stratagemma fuori dal form per intercettare il cambio di girone a runtime
            g_scelto = st.selectbox("Seleziona il Girone da registrare:", GRUPPI)
            
            # Recuperiamo la lista di squadre associate a quel girone specifico
            squadre_del_girone = squadre_gironi[g_scelto]
            
            with st.form("form_gironi_dinamico"):
                st.markdown(f"### 🏆 Posizioni Finali Gruppo {g_scelto}")
                
                c1, c2 = st.columns(2)
                with c1:
                    # Menu a tendina vincolato alle sole squadre del girone
                    p1 = st.selectbox(f"🥇 1ª Classificata Gruppo {g_scelto}:", squadre_del_girone, key="pos1_sel")
                with c2:
                    # Mostriamo le stesse squadre ma è possibile intercettare se l'utente mette la stessa
                    p2 = st.selectbox(f"🥈 2ª Classificata Gruppo {g_scelto}:", squadre_del_girone, key="pos2_sel")
                
                if st.form_submit_button("🏆 Conferma Posizioni Girone"):
                    if p1 == p2:
                        st.error("⚠️ Errore: La prima e la seconda classificata devono essere due squadre distinte!")
                    else:
                        chiave = f"Pos_Girone_{g_scelto}"
                        
                        if not df_res.empty:
                            df_res = df_res[df_res['Chiave_Evento'] != chiave]
                        
                        nuovo_dato = pd.DataFrame([{"Tipo": "Pos_Girone", "Chiave_Evento": chiave, "Valore_1": p1, "Valore_2": p2}])
                        df_res = pd.concat([df_res, nuovo_dato], ignore_index=True)
                        
                        ws_risultati.clear()
                        ws_risultati.update([df_res.columns.values.tolist()] + df_res.fillna("").values.tolist())
                        st.success(f"🚀 Classifica del Gruppo {g_scelto} registrata con successo su Sheets!")
                        st.rerun()

    # ==========================================
    # TAB 4: BACKUP & DATA AUDIT
    # ==========================================
    with tab4:
        st.subheader("💾 Esporta e Salva i Dati delle Giocate")
        st.write("Scarica i dati grezzi in formato CSV per tenerli al sicuro sul tuo PC come backup storico.")
        
        c1, c2 = st.columns(2)
        with c1:
            if not df_live.empty:
                csv_live = df_live.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Scarica Backup Schedine Live (CSV)", data=csv_live, file_name="backup_schedine_live.csv", mime="text/csv", use_container_width=True)
        with c2:
            if not df_gironi.empty:
                csv_gironi = df_gironi.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Scarica Backup Gironi (CSV)", data=csv_gironi, file_name="backup_gironi.csv", mime="text/csv", use_container_width=True)
