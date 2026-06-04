import streamlit as st
import pandas as pd
import os
from datetime import datetime


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

st.set_page_config(page_title="Mundial&Me Live 🏆", page_icon="🏆", layout="wide")

# --- BLOCCO LOCK FASE ELIMINATORIA ---
st.markdown("<br>", unsafe_allow_html=True)
st.warning("⏳ **TABELLONE IN FASE DI PREPARAZIONE** ⏳")

st.markdown("""
    <div style='background-color: #ffffff; padding: 20px; border-radius: 8px; border-left: 5px solid #ff9900; text-align: center;'>
        <h3 style='color: #111111; margin: 0;'>🔒 Accesso Temporaneamente Sospeso</h3>
        <p style='color: #555555; font-size: 14px; margin-top: 10px;'>
            Le urne dei gironi sono ancora calde! Il grande tabellone ad albero della fase eliminatoria 
            verrà sbloccato automaticamente non appena saranno decretate le 32 squadre qualificate.
        </p>
        <span style='font-size: 30px;'>🏅🏃‍♂️⚽</span>
    </div>
""", unsafe_allow_html=True)

# Blocca l'esecuzione del resto del codice nella pagina
st.stop()
#--- FINE BLOCCO


ELIMINATORIE_FILE = "predizioni_eliminatorie.csv"
if not os.path.exists(ELIMINATORIE_FILE):
    pd.DataFrame(columns=["Data", "Utente_Telegram", "Fase", "Slot_Tabellone", "Squadra_Pronosticata"]).to_csv(ELIMINATORIE_FILE, index=False)

# --- DIZIONARIO BANDIERINE PER UN IMPATTO GRAFICO DA RICEVITORIA ---
FLAGS = {
    "Messico": "🇲🇽", "Sudafrica": "🇿🇦", "Corea del Sud": "🇰🇷", "Rep. Ceca": "🇨🇿",
    "Canada": "🇨🇦", "Bosnia ed Erzegovina": "🇧🇦", "Qatar": "🇶🇦", "Svizzera": "🇨🇭",
    "Brasile": "🇧🇷", "Marocco": "🇲🇦", "Haiti": "🇭🇹", "Scozia": "🏴󠁧󠁢󠁳󠁣󠁴󠁿",
    "Stati Uniti": "🇺🇸", "Paraguay": "🇵🇾", "Australia": "🇦🇺", "Turchia": "🇹🇷",
    "Germania": "🇩🇪", "Curaçao": "🇨🇼", "Costa d'Avorio": "🇨🇮", "Ecuador": "🇪🇨",
    "Paesi Bassi": "🇳🇱", "Giappone": "🇯🇵", "Svezia": "🇸🇪", "Tunisia": "🇹🇳",
    "Belgio": "🇧🇪", "Egitto": "🇪🇬", "Iran": "🇮🇷", "Nuova Zelanda": "🇳🇿",
    "Spagna": "🇪🇸", "Capo Verde": "🇨🇻", "Arabia Saudita": "🇸🇦", "Uruguay": "🇺🇾",
    "Francia": "🇫🇷", "Senegal": "🇸🇳", "Iraq": "🇮🇶", "Norvegia": "🇳🇴",
    "Argentina": "🇦🇷", "Algeria": "🇩🇿", "Austria": "🇦🇹", "Giordania": "🇯🇴",
    "Portogallo": "🇵🇹", "RD del Congo": "🇨🇩", "Uzbekistan": "🇺🇿", "Colombia": "🇨🇴",
    "Inghilterra": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "Croazia": "🇭🇷", "Ghana": "🇬🇭", "Panama": "🇵🇦"
}

def label_with_flag(team_name):
    if team_name in ["-", "Selected..."] or "Vinc." in team_name or "Perdente" in team_name or "Finalista" in team_name:
        return team_name
    return f"{FLAGS.get(team_name, '⚽')} {team_name}"

# --- HEADER VINTAGE COORDINATO CON BRAND SEPARATO ---
# col_logo, col_titolo = st.columns([1, 5])
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
#             <p style='color: #555555; font-weight: bold; font-family: monospace; letter-spacing: 3px; margin: 0; font-size: 12px;'>\" IL TABELLONE VISIVO AD ALBERO DELLE FASI FINALI \"</p>
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

telegram_user = st.text_input("💬 Inserisci il tuo Nome Utente Telegram per sbloccare il Tabellone:", placeholder="@nickname_inserito")

if telegram_user:
    st.caption("🚀 Compila da sinistra verso destra: le scelte sbloccheranno i turni successivi in tempo reale con le bandiere ufficiali!")

    # --- ACCOPPIAMENTI STRUTTURALI REALI ---
    accoppiamenti_S = [
        {"id": "S1", "label": "1E vs 3A/B/C/D/F", "d1": "Messico", "d2": "Sudafrica"},
        {"id": "S2", "label": "1I vs 3C/D/F/G/H", "d1": "Corea del Sud", "d2": "Rep. Ceca"},
        {"id": "S3", "label": "2A vs 2B", "d1": "Canada", "d2": "Bosnia"},
        {"id": "S4", "label": "1F vs 2C", "d1": "Stati Uniti", "d2": "Paraguay"},
        {"id": "S5", "label": "2K vs 2L", "d1": "Qatar", "d2": "Svizzera"},
        {"id": "S6", "label": "1H vs 2J", "d1": "Brasile", "d2": "Marocco"},
        {"id": "S7", "label": "1D vs 3B/E/F/I/J", "d1": "Haiti", "d2": "Scozia"},
        {"id": "S8", "label": "1G vs 3A/E/H/I/J", "d1": "Australia", "d2": "Turchia"},
        {"id": "S9", "label": "1C vs 2F", "d1": "Germania", "d2": "Curaçao"},
        {"id": "S10", "label": "2E vs 2I", "d1": "Costa d'Avorio", "d2": "Ecuador"},
        {"id": "S11", "label": "1A vs 3C/E/F/H/I", "d1": "Paesi Bassi", "d2": "Giappone"},
        {"id": "S12", "label": "1L vs 3E/H/I/J/K", "d1": "Svezia", "d2": "Tunisia"},
        {"id": "S13", "label": "1J vs 2H", "d1": "Belgio", "d2": "Egitto"},
        {"id": "S14", "label": "2D vs 2G", "d1": "Iran", "d2": "Nuova Zelanda"},
        {"id": "S15", "label": "1B vs 3E/G/I/J", "d1": "Spagna", "d2": "Capo Verde"},
        {"id": "S16", "label": "1K vs 3D/E/I/J/L", "d1": "Arabia Saudita", "d2": "Uruguay"}
    ]

    # Geometria orizzontale a 5 colonne parallele
    col_sed, col_ott, col_qua, col_sem, col_fin = st.columns([2.2, 2, 2, 2, 2.2])

    vincenti_sedicesimi = {}
    vincenti_ottavi = {}
    vincenti_quarti = {}

    # --- COLONNA 1: SEDICESIMI ---
    with col_sed:
        st.markdown("<p style='text-align:center; font-weight:bold; background-color:#009933; color:white; padding:5px; border-radius:4px;'>Sedicesimi</p>", unsafe_allow_html=True)
        for idx, acc in enumerate(accoppiamenti_S):
            with st.container(border=True):
                st.markdown(f"<small style='color:#009933;'><b>Match {idx+1:02d}</b><br>{acc['label']}</small>", unsafe_allow_html=True)
                
                options = ["-", acc["d1"], acc["d2"]]
                vincitore = st.selectbox(
                    "Vince:", options, 
                    format_func=label_with_flag,
                    key=f"sed_{acc['id']}", label_visibility="collapsed"
                )
                vincenti_sedicesimi[acc['id']] = vincitore

    # --- COLONNA 2: OTTAVI DI FINALE ---
    with col_ott:
        st.markdown("<p style='text-align:center; font-weight:bold; background-color:#eef2f7; padding:5px; border-radius:4px;'>Ottavi di Finale</p>", unsafe_allow_html=True)
        collegamenti_ottavi = [("S1", "S2"), ("S3", "S4"), ("S5", "S6"), ("S7", "S8"), ("S9", "S10"), ("S11", "S12"), ("S13", "S14"), ("S15", "S16")]
        
        for i, (s1, s2) in enumerate(collegamenti_ottavi):
            st.markdown("<div style='margin-top: 36px;'></div>", unsafe_allow_html=True)
            with st.container(border=True):
                op1 = vincenti_sedicesimi[s1] if vincenti_sedicesimi[s1] != "-" else f"Vinc. Match {(i*2)+1}"
                op2 = vincenti_sedicesimi[s2] if vincenti_sedicesimi[s2] != "-" else f"Vinc. Match {(i*2)+2}"
                
                st.markdown(f"<small style='color:#333;'><b>Ottavo {i+1}</b></small>", unsafe_allow_html=True)
                
                # Se le opzioni cambiano a monte, forziamo la pulizia
                current_options = ["-", op1, op2]
                vincitore = st.selectbox(
                    "Vince:", current_options,
                    format_func=label_with_flag,
                    key=f"ott_O{i+1}", label_visibility="collapsed"
                )
                vincenti_ottavi[f"O{i+1}"] = vincitore

    # --- COLONNA 3: QUARTI DI FINALE ---
    with col_qua:
        st.markdown("<p style='text-align:center; font-weight:bold; background-color:#eef2f7; padding:5px; border-radius:4px;'>Quarti</p>", unsafe_allow_html=True)
        collegamenti_quarti = [("O1", "O2"), ("O3", "O4"), ("O5", "O6"), ("O7", "O8")]
        
        for i, (o1, o2) in enumerate(collegamenti_quarti):
            st.markdown("<div style='margin-top: 122px;'></div>", unsafe_allow_html=True)
            with st.container(border=True):
                op1 = vincenti_ottavi[o1] if vincenti_ottavi[o1] != "-" else f"Vinc. Ottavo {(i*2)+1}"
                op2 = vincenti_ottavi[o2] if vincenti_ottavi[o2] != "-" else f"Vinc. Ottavo {(i*2)+2}"
                
                st.markdown(f"<small style='color:#333;'><b>Quarto {i+1}</b></small>", unsafe_allow_html=True)
                
                current_options = ["-", op1, op2]
                vincitore = st.selectbox(
                    "Vince:", current_options,
                    format_func=label_with_flag,
                    key=f"qua_Q{i+1}", label_visibility="collapsed"
                )
                vincenti_quarti[f"Q{i+1}"] = vincitore

    # --- COLONNA 4: SEMIFINALI ---
    with col_sem:
        st.markdown("<p style='text-align:center; font-weight:bold; background-color:#eef2f7; padding:5px; border-radius:4px;'>Semifinali</p>", unsafe_allow_html=True)
        collegamenti_semi = [("Q1", "Q2"), ("Q3", "Q4")]
        vincenti_semi = {}
        
        for i, (q1, q2) in enumerate(collegamenti_semi):
            st.markdown("<div style='margin-top: 305px;'></div>", unsafe_allow_html=True)
            with st.container(border=True):
                op1 = vincenti_quarti[q1] if vincenti_quarti[q1] != "-" else f"Vinc. Quarto {(i*2)+1}"
                op2 = vincenti_quarti[q2] if vincenti_quarti[q2] != "-" else f"Vinc. Quarto {(i*2)+2}"
                
                st.markdown(f"<small style='color:#333;'><b>Semifinale {i+1}</b></small>", unsafe_allow_html=True)
                
                current_options = ["-", op1, op2]
                vincitore = st.selectbox(
                    "Vince:", current_options,
                    format_func=label_with_flag,
                    key=f"sem_S{i+1}", label_visibility="collapsed"
                )
                vincenti_semi[f"S{i+1}"] = vincitore

    # --- COLONNA 5: FINALE E TERZO POSTO ---
    with col_fin:
        st.markdown("<p style='text-align:center; font-weight:bold; background-color:#009933; color:white; padding:5px; border-radius:4px;'>👑 Finali</p>", unsafe_allow_html=True)
        
        # Finale 1° Posto
        st.markdown("<div style='margin-top: 395px;'></div>", unsafe_allow_html=True)
        with st.container(border=True):
            f1 = vincenti_semi["S1"] if vincenti_semi["S1"] != "-" else "Finalista 1"
            f2 = vincenti_semi["S2"] if vincenti_semi["S2"] != "-" else "Finalista 2"
            st.markdown("<b style='color:#009933;'>🥇 1° POSTO</b>", unsafe_allow_html=True)
            
            campione = st.selectbox(
                "Campione:", ["-", f1, f2],
                format_func=label_with_flag,
                key="fin_CAMPIONE", label_visibility="collapsed"
            )
            
        # Finale 3° Posto
        st.markdown("<div style='margin-top: 155px;'></div>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown("<b style='color:#ff9900;'>🥉 3° POSTO</b>", unsafe_allow_html=True)
            
            # Calcolo intelligente dei perdenti reali delle semifinali
            op_p1 = "Perdente Semi 1"
            if vincenti_semi["S1"] != "-":
                op_p1 = collegamenti_semi[0][1] if vincenti_semi["S1"] == vincenti_quarti[collegamenti_semi[0][0]] else collegamenti_semi[0][0]
                op_p1 = vincenti_quarti[op_p1]
                
            op_p2 = "Perdente Semi 2"
            if vincenti_semi["S2"] != "-":
                op_p2 = collegamenti_semi[1][1] if vincenti_semi["S2"] == vincenti_quarti[collegamenti_semi[1][0]] else collegamenti_semi[1][0]
                op_p2 = vincenti_quarti[op_p2]

            terzo_posto = st.selectbox(
                "Terzo:", ["-", op_p1, op_p2],
                format_func=label_with_flag,
                key="fin_TERZO", label_visibility="collapsed"
            )

    # --- SALVATAGGIO MATRICE PULITO ---
    st.markdown("<br><hr>", unsafe_allow_html=True)
    if st.button("🟢 CONVALIDA E REGISTRA IL TABELLONE COMPLETO 🟢", use_container_width=True):
        if "-" in list(vincenti_sedicesimi.values()) or "-" in list(vincenti_ottavi.values()) or "-" in list(vincenti_quarti.values()) or "-" in [vincenti_semi["S1"], vincenti_semi["S2"], campione, terzo_posto]:
            st.error("❌ Errore: Il tabellone presenta dei blocchi vuoti ('-'). Seleziona tutti i passaggi fino alla finale per confermare!")
        else:
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            righe = []
            for k, v in vincenti_sedicesimi.items(): righe.append({"Data": ts, "Utente_Telegram": telegram_user, "Fase": "Sedicesimi", "Slot_Tabellone": k, "Squadra_Pronosticata": v})
            for k, v in vincenti_ottavi.items(): righe.append({"Data": ts, "Utente_Telegram": telegram_user, "Fase": "Ottavi", "Slot_Tabellone": k, "Squadra_Pronosticata": v})
            for k, v in vincenti_quarti.items(): righe.append({"Data": ts, "Utente_Telegram": telegram_user, "Fase": "Quarti", "Slot_Tabellone": k, "Squadra_Pronosticata": v})
            righe.append({"Data": ts, "Utente_Telegram": telegram_user, "Fase": "Semifinale", "Slot_Tabellone": "S1", "Squadra_Pronosticata": vincenti_semi["S1"]})
            righe.append({"Data": ts, "Utente_Telegram": telegram_user, "Fase": "Semifinale", "Slot_Tabellone": "S2", "Squadra_Pronosticata": vincenti_semi["S2"]})
            righe.append({"Data": ts, "Utente_Telegram": telegram_user, "Fase": "Campione", "Slot_Tabellone": "FINALE", "Squadra_Pronosticata": campione})
            righe.append({"Data": ts, "Utente_Telegram": telegram_user, "Fase": "Terzo_Posto", "Slot_Tabellone": "3POSTO", "Squadra_Pronosticata": terzo_posto})
            
            pd.DataFrame(righe).to_csv(ELIMINATORIE_FILE, mode='a', header=False, index=False)
            st.success("🎯 Capolavoro salvato! Condividi lo screenshot nel gruppo!")
            st.balloons()
else:
    st.info("💡 Inserisci il tuo Username Telegram in alto per sbloccare il tabellone grafico.")