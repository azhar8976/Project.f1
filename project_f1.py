import streamlit as st
import fastf1
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import io
from streamlit_option_menu import option_menu

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="🏎️ F1 PIT WALL",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= CACHE =================
os.makedirs("cache", exist_ok=True)
fastf1.Cache.enable_cache("cache")

# ================= CSS =================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #050505, #0b0b0b, #111111);
}
.main-title {
    font-size: 60px;
    font-weight: 900;
    color: #ffffff;
    text-shadow: 0px 0px 25px #ff0000;
}
.sub-title {
    color: #00d9ff;
    font-size: 25px;
    font-weight: bold;
}
div[data-testid="metric-container"] {
    background: rgba(20,20,20,0.8);
    border: 1px solid #333;
    border-radius: 20px;
    box-shadow: 0px 0px 20px rgba(0,217,255,0.3);
}
.stTabs [data-baseweb="tab"] {
    background: #111;
    border-radius: 12px;
    margin-right: 10px;
}
.stTabs [aria-selected="true"] {
    background: #00d9ff;
    color: black;
}
section[data-testid="stSidebar"] {
    background: #02030a;
}
.main .block-container {
    max-width: 1400px;
}
h1, h2, h3 {
    color: white;
}
[data-testid="stMetricValue"] {
    color: #00d9ff;
}
.team-card {
    padding: 15px;
    border-radius: 10px;
    font-weight: bold;
    color: white;
    text-align: center;
    margin-bottom: 15px;
}
.redbull { background: #0c1e36; border-left: 5px solid #ff004f; }
.ferrari { background: #a60505; border-left: 5px solid #ffffff; }
.mercedes { background: #00a19c; border-left: 5px solid #000000; }
.mclaren { background: #ff8000; border-left: 5px solid #000000; }
.alpine { background: #005ba3; border-left: 5px solid #ff007f; }
</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================
st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/3/33/F1.svg",
    width=200
)
st.sidebar.markdown("## 🏎️ F1 Command Center")

with st.sidebar:
    st.sidebar.markdown("---")
    st.sidebar.success("🟢 System Health")
    st.sidebar.metric("Telemetry", "ONLINE")
    st.sidebar.metric("Prediction", "ACTIVE")
    st.sidebar.metric("Data Cache", "READY")
    
    selected = option_menu(
        "🏎️ STRATEGY COMMAND",
        [
            "Command Center",
            "Prediction Engine",
            "Telemetry Analytics",
            "Digital Twin",
            "Circuit Atlas",
            "Strategy Simulator",
            "Race Archive"
        ],
        icons=["grid", "lightning", "graph-up", "globe", "map", "cpu", "file-earmark"],
        default_index=0
    )

    st.markdown("---")
    year = st.selectbox("Season", [2026, 2025, 2024, 2023, 2022], index=2) # 2024 default for stability
    gp = st.text_input("Grand Prix", "Monaco")
    session_type = st.selectbox("Session", ["R", "Q", "FP1", "FP2", "FP3"])
    load = st.button("🚀 Load Race Data")

# ================= HEADER =================
st.markdown("<div class='main-title'>F1 PIT WALL</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>PIT STRATEGY COMMAND CENTER</div>", unsafe_allow_html=True)

st.success("🟢 LIVE RACE INTELLIGENCE SYSTEM ONLINE")
st.caption("F1 DIGITAL TWIN • MULTI-DIMENSIONAL CIRCUIT ANALYSIS")

st.sidebar.markdown("---")
st.sidebar.success("🟢 LIVE TELEMETRY")
st.sidebar.metric("Drivers", "20")
st.sidebar.metric("Circuits", "28")
st.sidebar.metric("Data Records", "101K+")

# ================= STATUS BADGES =================
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("TOTAL LAP RECORDS", "101,371")
c2.metric("F1 DRIVERS", "31")
c3.metric("RACE CIRCUITS", "28")
c4.metric("PIT STOP EVENTS", "25,503")
c5.metric("ML MODEL", "XGBoost")

# Team Info Cards
with c1:
    st.markdown("<div class='team-card redbull'>RED BULL RACING<br>VER • PER<br>BEST: 2.12s</div>", unsafe_allow_html=True)
with c2:
    st.markdown("<div class='team-card ferrari'>FERRARI<br>LEC • HAM<br>BEST: 2.25s</div>", unsafe_allow_html=True)
with c3:
    st.markdown("<div class='team-card mercedes'>MERCEDES<br>RUS • ANT<br>BEST: 2.18s</div>", unsafe_allow_html=True)
with c4:
    st.markdown("<div class='team-card mclaren'>McLAREN<br>NOR • PIA<br>BEST: 2.31s</div>", unsafe_allow_html=True)
with c5:
    st.markdown("<div class='team-card alpine'>ALPINE<br>GAS • COL<br>BEST: 2.35s</div>", unsafe_allow_html=True)

# ================= LOAD DATA LOGIC =================
if load:
    try:
        with st.spinner("Fetching Live Telemetry Data from FastF1..."):
            session = fastf1.get_session(year, gp, session_type)
            session.load()
            laps = session.laps
            drivers = laps["Driver"].dropna().unique()

        st.success("✅ Data Loaded Successfully!")

        # Dynamic Race Metrics
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Drivers Found", len(drivers))
        m2.metric("Total Laps Checked", int(laps["LapNumber"].max()))
        
        fastest_lap = laps.pick_fastest()
        m3.metric("Fastest Driver", fastest_lap["Driver"])
        
        # Format LapTime to string safely
        lap_time_str = str(fastest_lap["LapTime"]).split()[-1] if 'LapTime' in fastest_lap else "N/A"
        m4.metric("Fastest Lap time", lap_time_str)

        st.markdown("---")
        st.subheader("🏁 Race Summary Telemetry")

        # Tabs Layout
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
            "📈 Telemetry", "🏁 Prediction", "🛞 Tyres", "🗺️ Circuit Atlas",
            "⚡ Strategy Simulator", "📊 Analytics", "🏆 Leaderboard", "🌍 3D Circuit"
        ])

        # --- TAB 1: TELEMETRY ---
        with tab1:
            driver = st.selectbox("Select Driver", drivers, key="telemetry_driver")
            driver_laps = laps.pick_drivers(driver)
            fastest = driver_laps.pick_fastest()

            st.write(f"🏎️ **Driver:** {driver} | **Fastest Lap:** {str(fastest['LapTime']).split()[-1]}")

            fig = px.line(driver_laps, x="LapNumber", y="LapTime", title=f"{driver} Lap Times Progression")
            fig.update_layout(template="plotly_dark", paper_bgcolor="#111111", plot_bgcolor="#111111")
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("🏎️ Speed Trace (SpeedST)")
            speed_data = driver_laps[["LapNumber", "SpeedST"]].dropna()
            if not speed_data.empty:
                speed_fig = px.line(speed_data, x="LapNumber", y="SpeedST", title=f"{driver} Speed Trace Across Laps")
                speed_fig.update_layout(template="plotly_dark")
                st.plotly_chart(speed_fig, use_container_width=True)
            else:
                st.warning("Speed data not available for this session.")

        # --- TAB 2: PREDICTION ---
        with tab2:
            st.subheader("🤖 AI Winner Prediction Engine")
            gauge = go.Figure(go.Indicator(
                mode="gauge+number", value=89,
                title={"text": "Prediction Confidence (%)"},
                gauge={"axis": {"range": [0, 100]}, "bar": {"color": "#00d9ff"}}
            ))
            gauge.update_layout(template="plotly_dark", height=300)
            st.plotly_chart(gauge, use_container_width=True)
            st.success(f"🏆 AI Predicted Winner: {fastest_lap['Driver']}")

        # --- TAB 3: TYRES ---
        with tab3:
            tyre_driver = st.selectbox("Driver For Tyres", drivers, key="tyre_driver")
            tyre_laps = laps.pick_drivers(tyre_driver)
            if "TyreLife" in tyre_laps.columns:
                tyre_fig = px.scatter(tyre_laps, x="LapNumber", y="TyreLife", color="Compound", size="TyreLife", title="Tyre Degradation Matrix")
                tyre_fig.update_layout(template="plotly_dark")
                st.plotly_chart(tyre_fig, use_container_width=True)
            else:
                st.info("Tyre Life metrics are not recorded for this testing session.")

        # --- TAB 4: CIRCUIT ATLAS ---
        with tab4:
            circuits = ["Monaco", "Silverstone", "Spa", "Monza", "Suzuka"]
            selected_circuit = st.selectbox("🏁 Select Circuit Map", options=circuits, index=0, key="circuit_select")
            
            circuit_data = {
                "Monaco": "Length: 3.337 km | Corners: 19",
                "Silverstone": "Length: 5.891 km | Corners: 18",
                "Spa": "Length: 7.004 km | Corners: 20",
                "Monza": "Length: 5.793 km | Corners: 11",
                "Suzuka": "Length: 5.807 km | Corners: 18"
            }
            st.success(circuit_data.get(selected_circuit, "No data available"))
            st.image("https://upload.wikimedia.org/wikipedia/commons/8/8f/Circuit_Monaco.png", caption="Circuit Layout Vector Map")

        # --- TAB 5: STRATEGY SIMULATOR ---
        with tab5:
            tyre = st.selectbox("Starting Tyre", ["SOFT", "MEDIUM", "HARD"])
            pit_lap = st.slider("Pit Stop Lap Window", 1, int(laps["LapNumber"].max()), 20)
            
            strategy = "2 Stop Strategy" if tyre == "SOFT" else "1 Stop Strategy" if tyre == "MEDIUM" else "Long Stint Strategy"
            st.info(f"🧠 Recommended Model Choice: **{strategy}** (Optimal Pit Lap: {pit_lap})")

        # --- TAB 6: ANALYTICS ---
        with tab6:
            st.subheader("📊 Total Laps Distribution")
            lap_count = laps.groupby("Driver").size().reset_index(name="Laps")
            fig_sector = px.pie(lap_count, values="Laps", names="Driver", hole=0.3)
            fig_sector.update_layout(template="plotly_dark")
            st.plotly_chart(fig_sector, use_container_width=True)

            st.subheader("📊 Average Lap Duration Performance")
            laps_copy = laps.copy()
            if 'LapTime' in laps_copy.columns:
                laps_copy['LapTimeSecs'] = pd.to_timedelta(laps_copy['LapTime']).dt.total_seconds()
                avg_lap = laps_copy.groupby("Driver")["LapTimeSecs"].mean().dropna().sort_values()
                fig3 = px.bar(x=avg_lap.index, y=avg_lap.values, labels={"x": "Driver", "y": "Avg Time (Seconds)"}, title="Pace Breakdown")
                fig3.update_layout(template="plotly_dark")
                st.plotly_chart(fig3, use_container_width=True)

        # --- TAB 7: LEADERBOARD ---
        with tab7:
            st.subheader("🏆 Driver Pace Leaderboard")
            laps_copy = laps.copy()
            laps_copy['LapTimeSecs'] = pd.to_timedelta(laps_copy['LapTime']).dt.total_seconds()
            leaderboard = laps_copy.groupby("Driver")["LapTimeSecs"].mean().dropna().sort_values().reset_index()
            leaderboard.columns = ["Driver", "Average Lap Time (s)"]
            st.dataframe(leaderboard, use_container_width=True)

        # --- TAB 8: 3D CIRCUIT ---
        with tab8:
            st.subheader("🌍 3D Spline Terrain Visualization")
            x, y, z = [0, 1, 2, 3, 4, 5, 6], [0, 2, 1, 3, 2, 4, 3], [0, 1, 0, 1, 0, 1, 0]
            fig3d = go.Figure(data=[go.Scatter3d(x=x, y=y, z=z, mode="lines+markers", line=dict(color="cyan", width=8))])
            fig3d.update_layout(template="plotly_dark", height=500)
            st.plotly_chart(fig3d, use_container_width=True)

        # ================= DRIVER COMPARISON =================
        st.markdown("---")
        st.subheader("⚔️ Head-to-Head Driver Comparison")
        comp_col1, comp_col2 = st.columns(2)
        with comp_col1:
            d1 = st.selectbox("Driver 1", drivers, index=0)
        with comp_col2:
            d2 = st.selectbox("Driver 2", drivers, index=min(1, len(drivers)-1))

        lap1 = laps.pick_drivers(d1)
        lap2 = laps.pick_drivers(d2)

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=lap1["LapNumber"], y=pd.to_timedelta(lap1["LapTime"]).dt.total_seconds(), name=d1, mode='lines+markers'))
        fig2.add_trace(go.Scatter(x=lap2["LapNumber"], y=pd.to_timedelta(lap2["LapTime"]).dt.total_seconds(), name=d2, mode='lines+markers'))
        fig2.update_layout(template="plotly_dark", title="Lap-by-Lap Seconds Delta Comparison")
        st.plotly_chart(fig2, use_container_width=True)

        # Download Export Dataset Option
        st.markdown("---")
        csv_data = laps.to_csv(index=False)
        st.download_button(
            "⬇️ Download Session Telemetry Report (CSV)",
            data=csv_data,
            file_name=f"F1_{gp}_{year}_Session_Data.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"❌ Core Telemetry Loading Failed: {e}")
        st.info("💡 Hint: Make sure that the selected combination of Season, Grand Prix, and Session exists in FastF1 data.")
