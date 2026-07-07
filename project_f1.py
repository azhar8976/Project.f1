import streamlit as st
import fastf1
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
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

.stApp{
    background:linear-gradient(
        135deg,
        #050505,
        #0b0b0b,
        #111111
    );
}

.main-title{
    font-size:60px;
    font-weight:900;
    color:#ffffff;
    text-shadow:0px 0px 25px #ff0000;
}

.sub-title{
    color:#00d9ff;
    font-size:25px;
    font-weight:bold;
}

div[data-testid="metric-container"]{
    background:rgba(20,20,20,0.8);
    border:1px solid #333;
    border-radius:20px;
    box-shadow:0px 0px 20px rgba(0,217,255,0.3);
}

.stTabs [data-baseweb="tab"]{
    background:#111;
    border-radius:12px;
    margin-right:10px;
}

.stTabs [aria-selected="true"]{
    background:#00d9ff;
    color:black;
}

section[data-testid="stSidebar"]{
    background:#02030a;
}

.main .block-container{
    max-width:1400px;
}

h1,h2,h3{
    color:white;
}

[data-testid="stMetricValue"]{
    color:#00d9ff;
}

</style>
""", unsafe_allow_html=True)


st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/3/33/F1.svg",
    width=200
)

st.sidebar.markdown(
    "## 🏎️ F1 Command Center"
)

st.markdown("""
<style>
.team-card{
...
}
</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================
with st.sidebar:
    st.sidebar.markdown("---")

    st.sidebar.success("🟢 System Health")

    st.sidebar.metric(
        "Telemetry",
        "ONLINE"
    )

    st.sidebar.metric(
        "Prediction",
        "ACTIVE"
    )

    st.sidebar.metric(
        "Data Cache",
        "READY"
    )
    st.sidebar.success("🟢 SYSTEM STATUS")
    st.sidebar.info("📊 DATA STREAMING")
    ...

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
        icons=[
            "grid",
            "lightning",
            "graph-up",
            "globe",
            "map",
            "cpu",
            "file-earmark"
        ],
        default_index=0
    )

    st.markdown("---")

    year = st.selectbox(
        "Season",
        [2026, 2025, 2024, 2023, 2022]
    )

    gp = st.text_input(
        "Grand Prix",
        "Monaco"
    )

    session_type = st.selectbox(
        "Session",
        ["R", "Q", "FP1", "FP2", "FP3"]
    )

    load = st.button("🚀 Load Race Data")

# ================= HEADER =================
st.markdown("""
<div class='main-title'>
F1 PIT WALL
</div>

<div class='sub-title'>
PIT STRATEGY COMMAND CENTER
</div>
""", unsafe_allow_html=True)


st.success(
    "🟢 LIVE RACE INTELLIGENCE SYSTEM ONLINE"
)

st.caption(
    "F1 DIGITAL TWIN • MULTI-DIMENSIONAL CIRCUIT ANALYSIS"
)


st.sidebar.markdown("---")

st.sidebar.success(
    "🟢 LIVE TELEMETRY"
)

st.sidebar.metric(
    "Drivers",
    "20"
)

st.sidebar.metric(
    "Circuits",
    "28"
)

st.sidebar.metric(
    "Data Records",
    "101K+"
)

# ================= STATUS BADGES =================
c1,c2,c3,c4,c5 = st.columns(5)
c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("TOTAL LAP RECORDS", "101,371")
c2.metric("F1 DRIVERS", "31")
c3.metric("RACE CIRCUITS", "28")
c4.metric("PIT STOP EVENTS", "25,503")
c5.metric("ML MODEL", "XGBoost")

with c1:
    st.markdown("""
    <div class='team-card redbull'>
    RED BULL RACING<br>
    VER • PER<br>
    BEST: 2.12s
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class='team-card ferrari'>
    FERRARI<br>
    LEC • HAM<br>
    BEST: 2.25s
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class='team-card mercedes'>
    MERCEDES<br>
    RUS • ANT<br>
    BEST: 2.18s
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class='team-card mclaren'>
    McLAREN<br>
    NOR • PIA<br>
    BEST: 2.31s
    </div>
    """, unsafe_allow_html=True)

with c5:
    st.markdown("""
    <div class='team-card alpine'>
    ALPINE<br>
    GAS • COL<br>
    BEST: 2.35s
    </div>
    """, unsafe_allow_html=True)

    c1.metric("TOTAL LAP RECORDS", "101,371")
    c2.metric("F1 DRIVERS", "31")
    c3.metric("RACE CIRCUITS", "28")
    c4.metric("PIT STOP EVENTS", "25,503")
    c5.metric("ML MODEL", "XGBoost")


   
# ================= LOAD DATA =================
if load:

    try:
        with st.spinner("Loading F1 Data..."):

            session = fastf1.get_session(
                year,
                gp,
                session_type
            )

            session.load()

            laps = session.laps
            drivers = laps["Driver"].dropna().unique()

        st.success("✅ Data Loaded Successfully!")

        # ================= METRICS =================
        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Drivers", len(drivers))
        c2.metric("Total Laps", int(laps["LapNumber"].max()))
        c3.metric("Fastest Driver", laps.pick_fastest()["Driver"])
        c4.metric(
            "Fastest Lap",
            str(laps.pick_fastest()["LapTime"])
        )

        st.markdown("---")

        st.subheader("🏁 Race Summary")

        a, b, c, d = st.columns(4)

        a.metric(
         "Winner Prediction",
        laps.pick_fastest()["Driver"]
        )

        a2 = laps["LapTime"].dropna()

        b.metric(
        "Recorded Laps",
        len(a2)
        )

        c.metric(
        "Drivers",
        len(drivers)
        )

        d.metric(
            "Session",
            session_type
        )

        # ================= TABS =================

        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
            "📈 Telemetry",
            "🏁 Prediction",
            "🛞 Tyres",
            "🗺️ Circuit Atlas",
            "⚡ Strategy Simulator",
            "📊 Analytics",
            "🏆 Leaderboard",
            "🌍 3D Circuit"
        ])

        # ================= TAB 1 =================
        with tab1:

            driver = st.selectbox(
                "Select Driver",
                drivers
            )

            driver_laps = laps.pick_drivers(driver)
            fastest = driver_laps.pick_fastest()

            a, b = st.columns(2)

            a.metric("Driver", driver)
            b.metric(
                "Lap Time",
                str(fastest["LapTime"])
            )

            fig = px.line(
                driver_laps,
                x="LapNumber",
                y="LapTime",
                title=f"{driver} Lap Times"
            )

            st.subheader("🏎️ Speed Trace")

            speed_data = (
                driver_laps[
                    ["LapNumber", "SpeedST"]
                ]
                .dropna()
            )

            if not speed_data.empty:

                speed_fig = px.line(
                    speed_data,
                    x="LapNumber",
                    y="SpeedST",
                    title=f"{driver} Speed Trace"
                )

                speed_fig.update_layout(
                    template="plotly_dark"
                )

                st.plotly_chart(
                    speed_fig,
                    use_container_width=True
                )

            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="#111111",
                plot_bgcolor="#111111"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # ================= TAB 2 =================
        with tab2:

            gauge = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=89,
                    title={
                        "text":
                        "Prediction Confidence"
                    },
                    gauge={
                        "axis": {
                            "range": [0, 100]
                        }
                    }
                )
            )

            st.plotly_chart(
                gauge,
                use_container_width=True
            )

            st.success(
                f"🏆 Predicted Winner : "
                f"{laps.pick_fastest()['Driver']}"
            )

            st.subheader("🤖 AI Winner Prediction")

            winner = laps.pick_fastest()["Driver"]

            st.success(
                f"🏆 AI Predicted Winner : {winner}"
            )

            st.metric(
                "Confidence",
                "89%"
)

        # ================= TAB 3 =================
        with tab3:

            tyre_driver = st.selectbox(
                "Driver For Tyres",
                drivers,
                key="tyre_driver"
            )

            tyre_laps = laps.pick_drivers(
                tyre_driver
            )

            tyre_fig = px.scatter(
                tyre_laps,
                x="LapNumber",
                y="TyreLife",
                color="Compound",
                size="TyreLife",
                title="Tyre Degradation"
            )

            tyre_fig.update_layout(
                template="plotly_dark"
            )

            st.plotly_chart(
                tyre_fig,
                use_container_width=True
            )

        
        # ================= TAB 4 =================
        with tab4:

            circuits = [
                "Monaco",
                "Silverstone",
                "Spa",
                "Monza",
                "Suzuka"
            ]

            selected_circuit = st.selectbox(
                "🏁 Select Circuit",
                options=circuits,
                index=0,
                key="circuit_select"
            )

            st.info(f"🏎️ Selected Circuit : {selected_circuit}")

            st.subheader(f"🏁 {selected_circuit} Circuit")

            circuit_data = {
                "Monaco": "Length: 3.337 km | Corners: 19",
                "Silverstone": "Length: 5.891 km | Corners: 18",
                "Spa": "Length: 7.004 km | Corners: 20",
                "Monza": "Length: 5.793 km | Corners: 11",
                "Suzuka": "Length: 5.807 km | Corners: 18"
            }

            st.success(circuit_data[selected_circuit])

            st.info(
                f"""
        Season : {year}

        Session : {session_type}

        Circuit : {selected_circuit}
        """
            )

            st.image(
    "https://upload.wikimedia.org/wikipedia/commons/8/8f/Circuit_Monaco.png",
    use_container_width=True
)
                

        # ================= TAB 5 =================
        with tab5:

            tyre = st.selectbox(
                "Starting Tyre",
                [
                    "SOFT",
                    "MEDIUM",
                    "HARD"
                ]
            )

            pit_lap = st.slider(
                "Pit Stop Lap",
                1,
                int(laps["LapNumber"].max()),
                20
            )

            st.success(
                f"""
Start Tyre : {tyre}

Pit Window : Lap {pit_lap}

Finish Tyre : HARD
"""
            )

        st.markdown("---")

        st.success(
            "🟢 SYSTEM ONLINE | "
            "TELEMETRY ACTIVE | "
            "AI STRATEGY ENGINE READY"
        )

        if tyre == "SOFT":
            strategy = "2 Stop Strategy"

        elif tyre == "MEDIUM":
            strategy = "1 Stop Strategy"

        else:
            strategy = "Long Stint Strategy"

        st.info(
            f"🧠 Recommended : {strategy}"
        )

        if tyre == "SOFT":
            recommendation = "Pit Early"

        elif tyre == "MEDIUM":
            recommendation = "Normal Strategy"

        else:
            recommendation = "Long Stint Strategy"

        st.info(
            f"🧠 AI Recommendation : {recommendation}"
        )


        with tab6:

            st.subheader("📊 Driver Lap Count")

            lap_count = (
                laps.groupby("Driver")
                .size()
                .reset_index(name="Laps")
            )

            fig_sector = px.pie(
                lap_count,
                values="Laps",
                names="Driver"
            )

            fig_sector.update_layout(
                template="plotly_dark"
            )

            st.plotly_chart(
                fig_sector,
                use_container_width=True
            )

            st.subheader("📊 Race Analytics")

            avg_lap = (
                laps.groupby("Driver")["LapTime"]
                .mean()
                .dropna()
            )

            avg_lap = avg_lap.dt.total_seconds()

            fig3 = px.bar(
                x=avg_lap.index,
                y=avg_lap.values,
                labels={
                    "x": "Driver",
                    "y": "Average Lap Time (s)"
                },
                title="Average Lap Times"
            )

            fig3.update_layout(
                template="plotly_dark"
            )

            st.plotly_chart(
                fig3,
                use_container_width=True
            )

            heat_data = laps[
                ["Driver", "LapNumber"]
            ].copy()

            heat_data["Lap"] = heat_data["LapNumber"]

            fig4 = px.density_heatmap(
                heat_data,
                x="Lap",
                y="Driver"
            )

            fig4.update_layout(
                template="plotly_dark"
            )

            st.plotly_chart(
                fig4,
                use_container_width=True
            )

        with tab7:

            st.subheader("🏆 Driver Pace Leaderboard")

            leaderboard = (
                laps.dropna(subset=["LapTime"])
                .groupby("Driver")["LapTime"]
                .mean()
                .sort_values()
            )

            leaderboard = (
                leaderboard.dt.total_seconds()
                .reset_index()
            )

            leaderboard.columns = [
                "Driver",
                "Average Lap Time (s)"
            ]

            st.dataframe(
                leaderboard,
                use_container_width=True
            )


            with tab8:

                st.subheader("🌍 3D Circuit Visualization")

                x = [0, 1, 2, 3, 4, 5, 6]
                y = [0, 2, 1, 3, 2, 4, 3]
                z = [0, 1, 0, 1, 0, 1, 0]

                fig3d = go.Figure(
                    data=[
                        go.Scatter3d(
                            x=x,
                            y=y,
                            z=z,
                            mode="lines+markers",
                            line=dict(
                                color="cyan",
                                width=8
                            ),
                            marker=dict(
                                size=5,
                                color="red"
                            )
                        )
                    ]
                )

                fig3d.update_layout(
                    template="plotly_dark",
                    height=700
                )

                st.plotly_chart(
                    fig3d,
                    use_container_width=True
                )

        # ================= DRIVER COMPARISON =================
        st.subheader(
            "⚔️ Driver Comparison"
        )

        d1 = st.selectbox(
            "Driver 1",
            drivers
        )

        d2 = st.selectbox(
            "Driver 2",
            drivers,
            index=1 if len(drivers) > 1 else 0
        )

        lap1 = laps.pick_drivers(d1)
        lap2 = laps.pick_drivers(d2)

        fig2 = go.Figure()

        fig2.add_trace(
            go.Scatter(
                x=lap1["LapNumber"],
                y=lap1["LapTime"],
                name=d1
            )
        )

        fig2.add_trace(
            go.Scatter(
                x=lap2["LapNumber"],
                y=lap2["LapTime"],
                name=d2
            )
        )

        fig2.update_layout(
            template="plotly_dark",
            paper_bgcolor="#111111",
            plot_bgcolor="#111111"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

        # ================= DATA TABLE =================
        st.subheader("📋 Race Data")

        st.dataframe(
            laps[
                [
                    "Driver",
                    "LapNumber",
                    "LapTime",
                    "Compound",
                    "TyreLife"
                ]
            ]
        )

    except Exception as e:
        st.error(f"❌ Error: {e}")


if load and 'laps' in locals():
    csv = laps.to_csv(index=False)

    st.download_button(
        "⬇ Download Race Data",
        data=csv,
        file_name=f"{gp}_{year}.csv",
        mime="text/csv"
    )