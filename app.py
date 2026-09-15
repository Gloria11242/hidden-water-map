import streamlit as st
import pandas as pd
import plotly.express as px

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="The Hidden Water Map",
    page_icon="💧",
    layout="wide"
)

st.markdown("""
<style>
.block-container{padding-top:2rem;max-width:1500px}
section[data-testid="stSidebar"]{background:#f5f9fc;border-right:1px solid #dce6ed}
.hero{background:linear-gradient(135deg,#eaf5f7,#f7fbfc);border:1px solid #d7e5e9;border-radius:20px;padding:28px 32px;margin-bottom:22px}
.hero-title{font-size:2.6rem;font-weight:800;color:#12304a}
.hero-subtitle{font-size:1.15rem;color:#496576;margin:5px 0 14px}
.hero-tag{display:inline-block;background:#dff2ea;color:#176b52;border-radius:999px;padding:7px 14px;font-weight:700;font-size:.82rem}
.kpi-card{min-height:165px;border:1px solid #dce6ed;border-radius:18px;padding:19px 20px;box-shadow:0 4px 14px rgba(18,48,74,.07);margin-bottom:12px}
.kpi-blue{background:linear-gradient(145deg,#edf5ff,#fbfdff)}
.kpi-green{background:linear-gradient(145deg,#edf9f4,#fbfffd)}
.kpi-orange{background:linear-gradient(145deg,#fff6e9,#fffdf9)}
.kpi-purple{background:linear-gradient(145deg,#f4f0ff,#fcfbff)}
.kpi-icon{font-size:1.45rem}.kpi-label{font-size:.78rem;font-weight:750;color:#587083;text-transform:uppercase;letter-spacing:.45px}
.kpi-value{font-size:2rem;font-weight:800;color:#16344d;line-height:1.05;margin:5px 0 7px}
.kpi-caption{font-size:.8rem;color:#667b8a;line-height:1.4}
.insight-card{background:linear-gradient(135deg,#12304a,#1e536c);color:white;border-radius:18px;padding:18px 23px;margin:8px 0 22px;box-shadow:0 5px 16px rgba(18,48,74,.12)}
.insight-label{font-size:.73rem;font-weight:800;text-transform:uppercase;letter-spacing:1px;opacity:.78}
.insight-text{font-size:1.1rem;font-weight:650;line-height:1.45;margin-top:4px}
.section-title{color:#12304a;font-weight:800}
div[data-testid="stMetric"]{background:#f8fbfd;border:1px solid #e1e9ee;border-radius:14px;padding:10px 13px}

/* ===== Executive dashboard polish ===== */
body { background: #f7f9fb; }
.main .block-container { background: #f7f9fb; }
[data-testid="stSidebar"] .stRadio > div { gap: 4px; }
[data-testid="stSidebar"] .stRadio label {
    border-radius: 10px;
    padding: 7px 10px;
    color: #29445a;
    font-weight: 600;
}
[data-testid="stSidebar"] .stRadio label:hover { background: #e9f2ff; }
.dashboard-meta {
    display:flex; justify-content:flex-end; gap:18px; color:#6a7d8d;
    font-size:.78rem; margin:-8px 0 12px;
}
.hero-image {
    position:relative;
    overflow:hidden;
    min-height:245px;
    border-radius:20px;
    background:
      linear-gradient(90deg, rgba(11,43,62,.88) 0%, rgba(11,43,62,.55) 45%, rgba(11,43,62,.16) 100%),
      linear-gradient(135deg,#8eb7a4 0%,#d6e4cc 42%,#789c7e 100%);
    padding:34px 38px;
    color:white;
    box-shadow:0 7px 24px rgba(18,48,74,.12);
}
.hero-image:after {
    content:"";
    position:absolute; right:-80px; top:-100px; width:420px; height:420px;
    border-radius:50%;
    background:radial-gradient(circle,rgba(255,255,255,.20),transparent 62%);
}
.hero-kicker {font-size:.78rem;font-weight:800;letter-spacing:1.5px;text-transform:uppercase;opacity:.82}
.hero-big {font-size:2.65rem;font-weight:850;line-height:1.05;margin-top:7px;letter-spacing:-1px}
.hero-small {font-size:1.08rem;max-width:680px;margin-top:10px;line-height:1.45;opacity:.95}
.hero-quote {
    position:absolute; right:28px; bottom:25px; width:310px;
    background:rgba(8,34,48,.78); border-left:4px solid #7ee0b5;
    border-radius:12px; padding:15px 18px; font-style:italic; font-size:.92rem;
    z-index:2;
}
.dashboard-title {font-size:1.7rem;font-weight:800;color:#12304a;margin:18px 0 5px}
.dashboard-subtitle {color:#647989;font-size:.9rem;margin-bottom:14px}
.card-row {display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin:12px 0 20px}
.exec-card {border-radius:17px;padding:18px 16px;min-height:165px;border:1px solid #dce6ed;box-shadow:0 4px 15px rgba(18,48,74,.06)}
.exec-card .num {font-size:1.9rem;font-weight:850;color:#173a56;margin:5px 0}
.exec-card .lbl {font-size:.78rem;font-weight:800;color:#526c7d}
.exec-card .cap {font-size:.72rem;line-height:1.35;color:#718493}
.card-blue{background:#eef6ff}.card-red{background:#fff0f0}.card-green{background:#edf9f3}.card-orange{background:#fff6e8}.card-purple{background:#f4f0ff}
.map-shell {background:white;border:1px solid #dfe7ed;border-radius:18px;padding:18px 18px 8px;box-shadow:0 3px 12px rgba(18,48,74,.05)}
.small-note {background:#edf6ff;border-radius:12px;padding:13px 15px;color:#345b74;font-size:.82rem}
@media(max-width:1000px){.card-row{grid-template-columns:repeat(2,1fr)}.hero-quote{position:static;width:auto;margin-top:18px}.hero-image{min-height:310px}}

/* ===== Final presentation polish ===== */
[data-testid="stDataFrame"] { border-radius: 14px; overflow: hidden; }
.stPlotlyChart { border-radius: 14px; }
[data-testid="stSidebar"] { padding-top: 1rem; }
@media (max-width: 700px) {
  .hero-big { font-size: 2rem; }
  .hero-image { padding: 25px 22px; }
  .dashboard-title { font-size: 1.4rem; }
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# CONSTANTS
# ============================================================

WS_DEFAULT = 50      # project water-stress threshold (%)
AGRI_DEFAULT = 75    # project agricultural-dependence threshold (%)

# Cosmetic label only — never used for filtering/joins, which still use
# the raw "Maize (corn)" value so the CSVs are never modified.
CROP_LABELS = {"Maize (corn)": "Maize"}


def crop_label(crop: str) -> str:
    return CROP_LABELS.get(crop, crop)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    dashboard = pd.read_csv("hidden_water_map_dashboard.csv")
    summary = pd.read_csv("hidden_water_map_summary.csv")
    country_risk = pd.read_csv("hidden_water_map_country_risk.csv")
    return dashboard, summary, country_risk


dashboard, summary, country_risk = load_data()

CROPS = sorted(dashboard["Crop"].unique())

# ============================================================
# SIDEBAR — GLOBAL CONTROLS
# ============================================================

st.sidebar.header("Explore the data")

if "ws_threshold" not in st.session_state:
    st.session_state.ws_threshold = WS_DEFAULT
if "agri_threshold" not in st.session_state:
    st.session_state.agri_threshold = AGRI_DEFAULT


def reset_defaults():
    st.session_state.ws_threshold = WS_DEFAULT
    st.session_state.agri_threshold = AGRI_DEFAULT


crop_display_options = ["All crops"] + [crop_label(c) for c in CROPS]
selected_crop_label = st.sidebar.selectbox("Focus crop", crop_display_options)
label_to_crop = {crop_label(c): c for c in CROPS}
selected_crop = None if selected_crop_label == "All crops" else label_to_crop[selected_crop_label]

st.sidebar.slider(
    "Water-stress threshold (%)",
    min_value=0, max_value=150, step=5,
    key="ws_threshold",
    help="Countries at or above this level are treated as severely water-stressed. "
         "Project default is 50% — stricter than the SDG 6.4.2 standard of 25%."
)

st.sidebar.slider(
    "Agricultural-dependence threshold (%)",
    min_value=0, max_value=100, step=5,
    key="agri_threshold",
    help="Share of total water withdrawals used for agriculture. Project default is 75%."
)

country_list = sorted(country_risk["Country"].unique())
selected_country = st.sidebar.selectbox("Country profile", ["None"] + country_list)

st.sidebar.button("Reset to project defaults", on_click=reset_defaults, use_container_width=True)

ws_threshold = st.session_state.ws_threshold
agri_threshold = st.session_state.agri_threshold
is_custom_threshold = (ws_threshold != WS_DEFAULT) or (agri_threshold != AGRI_DEFAULT)

st.sidebar.divider()
st.sidebar.caption(
    "Data: FAOSTAT crop production & FAO AQUASTAT water indicators, 2022. "
    "Team Query Queens — Women in Data Datathon 2026."
)

# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="hero-image">
  <div class="hero-kicker">Food Today · Water Tomorrow</div>
  <div class="hero-big">The Hidden Water Map</div>
  <div class="hero-small">
    Where food production depends on water systems under structural pressure.
    Exploring the intersection of water stress and agricultural dependence
    across matched countries and five major crops.
  </div>
  <div class="hero-quote">
    “Water stress is not necessarily a production problem today —
    it is a resilience problem for tomorrow.”
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="dashboard-meta"><span>FAOSTAT & AQUASTAT · 2022</span><span>Countries: 185</span><span>Crops: 5</span></div>',
    unsafe_allow_html=True
)

# ============================================================
# ACT 1 — THE PARADOX (KPIs)
# ============================================================

st.markdown("### High production does not mean a resilient food system.")

n_countries = dashboard["Country"].nunique()
n_hotspot_countries = dashboard.loc[
    dashboard["Risk_Category"] == "High-pressure hotspot", "Country"
].nunique()
sugar_exposure = summary.loc[summary["Crop"] == "Sugar cane", "Production_Exposed_%"].iloc[0]
coverage_min = summary["Water_Data_Coverage_%"].min()
coverage_max = summary["Water_Data_Coverage_%"].max()

st.markdown('<div class="dashboard-title">Key Insights at a Glance</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="card-row">
  <div class="exec-card card-blue">
    <div>🌐</div><div class="num">{n_hotspot_countries}</div>
    <div class="lbl">Countries at High Pressure</div>
    <div class="cap">Meet both water stress ≥50% and agricultural dependence ≥75%.</div>
  </div>
  <div class="exec-card card-red">
    <div>💧</div><div class="num">≥50%</div>
    <div class="lbl">Severe Water Stress</div>
    <div class="cap">Project threshold used to identify high-pressure countries.</div>
  </div>
  <div class="exec-card card-green">
    <div>🌱</div><div class="num">{sugar_exposure:.1f}%</div>
    <div class="lbl">Highest Crop Exposure</div>
    <div class="cap">Sugar cane — share of global production in water-stressed countries.</div>
  </div>
  <div class="exec-card card-orange">
    <div>🌾</div><div class="num">{len(CROPS)}</div>
    <div class="lbl">Focus Crops</div>
    <div class="cap">Sugar cane, rice, wheat, potatoes and maize.</div>
  </div>
  <div class="exec-card card-purple">
    <div>🗄️</div><div class="num">{coverage_min:.0f}%–{coverage_max:.0f}%</div>
    <div class="lbl">Data Coverage</div>
    <div class="cap">Varies by crop. See Methodology for details.</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="insight-card">
  <div class="insight-label">Core finding</div>
  <div class="insight-text">
    High agricultural output does not necessarily mean a resilient food system.
    Current production can coexist with substantial water-system pressure.
  </div>
</div>
""", unsafe_allow_html=True)

st.info(
    "How to read this dashboard: start with the Pressure Map, then move to Crop Exposure "
    "and the India–Pakistan proof case. The thresholds are adjustable for exploration, "
    "but the project findings use the default 50% / 75% thresholds."
)

if is_custom_threshold:
    st.info(
        f"⚠️ Custom thresholds in use ({ws_threshold}% water stress, {agri_threshold}% "
        f"agricultural dependence) — not the project's validated definition "
        f"(≥{WS_DEFAULT}% / ≥{AGRI_DEFAULT}%). Charts below reflect your custom selection."
    )

st.divider()

# ============================================================
# ACT 2 — THE PRESSURE MAP
# ============================================================

st.markdown('<h2 class="section-title">2. The Pressure Map — Where Water Stress Meets Agricultural Dependence</h2>', unsafe_allow_html=True)

view_col1, view_col2 = st.columns([4, 1])
with view_col2:
    map_view = st.selectbox(
        "View by",
        ["Both thresholds (default)", "Water stress", "Agricultural dependence"],
        key="map_view"
    )

st.markdown(
    f"""
    The map classifies matched countries using the selected thresholds:
    **{ws_threshold}% water stress** and **{agri_threshold}% agricultural dependence**.
    High-pressure countries meet both conditions. This is a **project definition,
    not an official FAO risk index**.
    """
)

plot_df = country_risk.copy()

plot_df["Status"] = "Does not meet thresholds"
plot_df.loc[
    (plot_df["Water_Stress"] >= ws_threshold) &
    (plot_df["Agriculture_Withdrawal_Share"] >= agri_threshold),
    "Status"
] = "High pressure"
plot_df.loc[
    (plot_df["Water_Stress"] >= ws_threshold) &
    (plot_df["Agriculture_Withdrawal_Share"] < agri_threshold),
    "Status"
] = "High water stress only"
plot_df.loc[
    (plot_df["Water_Stress"] < ws_threshold) &
    (plot_df["Agriculture_Withdrawal_Share"] >= agri_threshold),
    "Status"
] = "High agricultural dependence only"

status_order = [
    "High pressure",
    "High water stress only",
    "High agricultural dependence only",
    "Does not meet thresholds",
]

if map_view == "Water stress":
    fig_risk = px.choropleth(
        plot_df,
        locations="Country",
        locationmode="country names",
        color="Water_Stress",
        color_continuous_scale="YlOrRd",
        range_color=(0, max(100, float(plot_df["Water_Stress"].max()))),
        hover_name="Country",
        hover_data={
            "Water_Stress": ":.1f",
            "Agriculture_Withdrawal_Share": ":.1f",
        },
        labels={"Water_Stress": "Water stress (%)"},
    )
    fig_risk.update_coloraxes(colorbar_title="Water stress (%)")
else:
    if map_view == "Agricultural dependence":
        fig_risk = px.choropleth(
            plot_df,
            locations="Country",
            locationmode="country names",
            color="Agriculture_Withdrawal_Share",
            color_continuous_scale="YlOrBr",
            range_color=(0, 100),
            hover_name="Country",
            hover_data={
                "Water_Stress": ":.1f",
                "Agriculture_Withdrawal_Share": ":.1f",
            },
            labels={"Agriculture_Withdrawal_Share": "Agricultural dependence (%)"},
        )
        fig_risk.update_coloraxes(colorbar_title="Agricultural dependence (%)")
    else:
        fig_risk = px.choropleth(
            plot_df,
            locations="Country",
            locationmode="country names",
            color="Status",
            category_orders={"Status": status_order},
            color_discrete_map={
                "High pressure": "#e3262e",
                "High water stress only": "#f28c28",
                "High agricultural dependence only": "#f4d03f",
                "Does not meet thresholds": "#aeb8c2",
            },
            hover_name="Country",
            hover_data={
                "Water_Stress": ":.1f",
                "Agriculture_Withdrawal_Share": ":.1f",
                "Status": True,
            },
        )
        fig_risk.update_layout(legend_title_text="Country status")

fig_risk.update_geos(
    showframe=False,
    showcoastlines=False,
    showland=True,
    landcolor="#e6ebef",
    bgcolor="rgba(0,0,0,0)",
    projection_type="natural earth",
)
fig_risk.update_layout(
    height=540,
    margin=dict(l=0, r=0, t=5, b=0),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
)

st.markdown('<div class="map-shell">', unsafe_allow_html=True)
st.plotly_chart(fig_risk, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    f'<div class="small-note">💡 <b>{len(plot_df[(plot_df["Water_Stress"] >= ws_threshold) & (plot_df["Agriculture_Withdrawal_Share"] >= agri_threshold)])}</b> '
    f'of <b>{plot_df["Country"].nunique()}</b> countries currently meet both selected thresholds.</div>',
    unsafe_allow_html=True,
)

st.caption(
    "The map classifies countries using the two selected thresholds. "
    "Water-stress values above 100% are retained under the SDG 6.4.2 methodology."
)


st.divider()

# ============================================================
# ACT 3 — FIVE-CROP FOOD EXPOSURE
# ============================================================

st.markdown('<h2 class="section-title">3. Food Production Exposure Across All Five Crops</h2>', unsafe_allow_html=True)

st.markdown(
    """
    Share of 2022 global production located in countries with **severe water
    stress (project threshold: ≥50%)**. This is not a forecast of crop loss —
    it describes where production currently sits.
    """
)

summary_display = summary.copy()
summary_display["Crop_Label"] = summary_display["Crop"].apply(crop_label)

fig_exposure = px.bar(
    summary_display.sort_values("Production_Exposed_%", ascending=True),
    x="Production_Exposed_%",
    y="Crop_Label",
    orientation="h",
    text="Production_Exposed_%",
    custom_data=["Water_Data_Coverage_%"],
    labels={"Production_Exposed_%": "Production exposed (%)", "Crop_Label": ""},
)

fig_exposure.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside",
    hovertemplate="%{y}<br>Exposed: %{x:.1f}%<br>Water-stress data coverage: %{customdata[0]:.1f}%<extra></extra>",
)
fig_exposure.update_layout(height=420, margin=dict(l=20, r=60, t=30, b=20))
st.plotly_chart(fig_exposure, use_container_width=True)

cov_cols = st.columns(5)
for col, (_, row) in zip(cov_cols, summary_display.sort_values("Production_Exposed_%", ascending=False).iterrows()):
    col.caption(f"**{row['Crop_Label']}**\ncoverage: {row['Water_Data_Coverage_%']:.0f}%")

st.caption(
    "Exposure refers to production located in countries with water stress ≥50%; "
    "it is not a forecast of crop loss. Coverage indicates the share of each crop's "
    "production for which matching water-stress data exists — interpret exposure "
    "together with coverage, especially for potatoes and wheat."
)

st.divider()

# ============================================================
# ACT 4 — COUNTRY HOTSPOTS (broad view, before India/Pakistan)
# ============================================================

st.header("4. Country Hotspots")

st.markdown(
    "Countries currently meeting **both** thresholds selected in the sidebar. "
    "India and Pakistan are two of several — not the only two."
)

hotspots = country_risk[
    (country_risk["Water_Stress"] >= ws_threshold)
    & (country_risk["Agriculture_Withdrawal_Share"] >= agri_threshold)
].copy()

if selected_crop:
    crop_prod = dashboard.loc[dashboard["Crop"] == selected_crop, ["Country", "Global_Production_Share_%"]]
    hotspots = hotspots.merge(crop_prod, on="Country", how="left")
    hotspots["Global_Production_Share_%"] = hotspots["Global_Production_Share_%"].fillna(0)
    hotspots = hotspots.rename(columns={"Global_Production_Share_%": f"{crop_label(selected_crop)} global share (%)"})
    sort_col = f"{crop_label(selected_crop)} global share (%)"
    hotspots = hotspots.sort_values(sort_col, ascending=False)
else:
    hotspots = hotspots.sort_values("Water_Stress", ascending=False)

st.markdown("**Hotspot table**", unsafe_allow_html=True)
st.dataframe(
    hotspots[[c for c in hotspots.columns if c not in ("Stress_Level", "Agriculture_Dependence")]]
    .rename(columns={"Water_Stress": "Water stress (%)", "Agriculture_Withdrawal_Share": "Agricultural dependence (%)"}),
    use_container_width=True,
    hide_index=True,
)

st.caption(
    f"{len(hotspots)} of {country_risk['Country'].nunique()} countries currently meet "
    f"water stress ≥{ws_threshold}% and agricultural dependence ≥{agri_threshold}%."
)

st.divider()

# ============================================================
# ACT 5 — INDIA + PAKISTAN DEEP DIVE
# ============================================================

st.header("5. India and Pakistan — A Proof Case, Not the Whole Story")

st.markdown(
    "India and Pakistan are highlighted because they combine substantial food "
    "production with severe water stress **and** high agricultural dependence — "
    "the same pattern shown for the broader hotspot set above."
)

india = country_risk.loc[country_risk["Country"] == "India"].iloc[0]
pakistan = country_risk.loc[country_risk["Country"] == "Pakistan"].iloc[0]


def hotspot_card(country_name: str, row: pd.Series) -> str:
    if selected_crop:
        share_row = dashboard[(dashboard["Country"] == country_name) & (dashboard["Crop"] == selected_crop)]
        crop_txt = crop_label(selected_crop)
        share = share_row["Global_Production_Share_%"].iloc[0] if not share_row.empty else 0.0
        share_clause = f", while producing {share:.1f}% of global {crop_txt} production"
    else:
        share_clause = ""
    meets = row["Water_Stress"] >= ws_threshold and row["Agriculture_Withdrawal_Share"] >= agri_threshold
    verdict = "meets" if meets else "does not currently meet"
    return (
        f"**{country_name}** combines {row['Water_Stress']:.1f}% water stress and "
        f"{row['Agriculture_Withdrawal_Share']:.1f}% agricultural withdrawal dependence"
        f"{share_clause}. It {verdict} both selected hotspot thresholds "
        f"(≥{ws_threshold}% water stress, ≥{agri_threshold}% agricultural dependence)."
    )


col1, col2 = st.columns(2)
with col1:
    st.subheader("India")
    m1, m2 = st.columns(2)
    m1.metric("Water stress", f"{india['Water_Stress']:.1f}%")
    m2.metric("Agricultural withdrawal share", f"{india['Agriculture_Withdrawal_Share']:.1f}%")
    st.markdown(hotspot_card("India", india))

with col2:
    st.subheader("Pakistan")
    m1, m2 = st.columns(2)
    m1.metric("Water stress", f"{pakistan['Water_Stress']:.1f}%")
    m2.metric("Agricultural withdrawal share", f"{pakistan['Agriculture_Withdrawal_Share']:.1f}%")
    st.markdown(hotspot_card("Pakistan", pakistan))

st.markdown("**Combined global production share, India + Pakistan (validated, from `summary.csv`)**")

ip_chart_df = summary_display[["Crop_Label", "India_Pakistan_Global_Share_%"]].sort_values(
    "India_Pakistan_Global_Share_%", ascending=True
)

fig_ip = px.bar(
    ip_chart_df,
    x="India_Pakistan_Global_Share_%",
    y="Crop_Label",
    orientation="h",
    text="India_Pakistan_Global_Share_%",
    labels={"India_Pakistan_Global_Share_%": "Combined global production share (%)", "Crop_Label": ""},
)
fig_ip.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
fig_ip.update_layout(height=380, margin=dict(l=20, r=60, t=30, b=20))
st.plotly_chart(fig_ip, use_container_width=True)

st.caption(
    "This chart reads directly from the validated summary table — it is not recomputed "
    "from country-crop rows, so it cannot drift from the numbers reported elsewhere in this analysis."
)

st.markdown(
    "**Five-crop comparison:** India + Pakistan account for "
    "**21.6% of global sugar cane, 15.3% of rice, 8.9% of wheat, "
    "8.6% of potatoes, and 2.5% of maize production.**"
)

st.divider()

# ============================================================
# ACT 6 — DYNAMIC HOTSPOT EXPLORER
# ============================================================

st.header("6. Dynamic Hotspot Explorer")

st.markdown(
    "Adjust the crop and thresholds in the sidebar to see which country currently "
    "leads the selected crop's production among hotspot countries."
)

if selected_crop:
    lead = hotspots.copy()
    sort_col = f"{crop_label(selected_crop)} global share (%)"
    if sort_col in lead.columns and not lead.empty and lead[sort_col].max() > 0:
        top_row = lead.sort_values(sort_col, ascending=False).iloc[0]
        top_country_risk = country_risk.loc[country_risk["Country"] == top_row["Country"]].iloc[0]
        st.markdown(hotspot_card(top_row["Country"], top_country_risk))
    else:
        st.markdown("No hotspot country currently has recorded production for this crop.")
else:
    st.markdown("Select a specific crop in the sidebar to generate a hotspot explanation.")

st.caption(
    "This explanation is generated directly from the filtered data above using a fixed "
    "template — it is an analytical exploration, not a machine-learning prediction or an "
    "official risk classification."
)

st.divider()

# ============================================================
# ACT 7 — COUNTRY PROFILE
# ============================================================

if selected_country != "None":
    st.header(f"7. Country Profile — {selected_country}")

    c_row = country_risk.loc[country_risk["Country"] == selected_country].iloc[0]
    c1, c2, c3 = st.columns(3)
    c1.metric("Water stress", f"{c_row['Water_Stress']:.1f}%")
    c2.metric("Agricultural withdrawal share", f"{c_row['Agriculture_Withdrawal_Share']:.1f}%")
    meets = c_row["Water_Stress"] >= ws_threshold and c_row["Agriculture_Withdrawal_Share"] >= agri_threshold
    c3.metric("Meets selected hotspot thresholds", "Yes" if meets else "No")

    c_crops = dashboard.loc[dashboard["Country"] == selected_country].copy()
    if not c_crops.empty:
        c_crops["Crop_Label"] = c_crops["Crop"].apply(crop_label)
        fig_c = px.bar(
            c_crops.sort_values("Global_Production_Share_%", ascending=True),
            x="Global_Production_Share_%", y="Crop_Label", orientation="h",
            text="Global_Production_Share_%",
            labels={"Global_Production_Share_%": "Global production share (%)", "Crop_Label": ""},
        )
        fig_c.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
        fig_c.update_layout(height=320, margin=dict(l=20, r=60, t=30, b=20))
        st.plotly_chart(fig_c, use_container_width=True)
    else:
        st.caption("No focus-crop production recorded for this country in the 2022 dataset.")

    st.divider()

# ============================================================
# ACT 8 — CROP PROFILE
# ============================================================

if selected_crop:
    st.header(f"8. Crop Profile — {crop_label(selected_crop)}")

    s_row = summary.loc[summary["Crop"] == selected_crop].iloc[0]
    c1, c2, c3 = st.columns(3)
    c1.metric("2022 global production", f"{s_row['Global_Production']:,.0f} t")
    c2.metric("Production exposed to severe stress", f"{s_row['Production_Exposed_%']:.1f}%")
    c3.metric("Water-stress data coverage", f"{s_row['Water_Data_Coverage_%']:.1f}%")

    top_producers = dashboard.loc[dashboard["Crop"] == selected_crop].sort_values(
        "Global_Production_Share_%", ascending=False
    ).head(10)
    fig_top = px.bar(
        top_producers.sort_values("Global_Production_Share_%", ascending=True),
        x="Global_Production_Share_%", y="Country", orientation="h",
        text="Global_Production_Share_%",
        labels={"Global_Production_Share_%": "Global production share (%)", "Country": ""},
    )
    fig_top.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig_top.update_layout(height=420, margin=dict(l=20, r=60, t=30, b=20))
    st.plotly_chart(fig_top, use_container_width=True)
    st.caption("Top 10 producing countries for this crop, 2022.")

    st.divider()

# ============================================================
# ACT 9 — DECISION SUPPORT
# ============================================================

st.header("9. Why This Matters")

a1, a2, a3 = st.columns(3)
with a1:
    st.markdown("**Policymakers**")
    st.caption("Identify food-producing regions where water-system pressure may warrant resilience planning.")
with a2:
    st.markdown("**Food companies**")
    st.caption("Understand where supply chains depend heavily on water-stressed production systems.")
with a3:
    st.markdown("**Banks & insurers**")
    st.caption("Use water-pressure indicators as an additional context variable for agricultural exposure assessment.")

st.markdown("**Potential action areas — not guaranteed solutions**")
st.markdown(
    """
    - Irrigation efficiency improvements
    - Crop-water productivity gains
    - Crop planning aligned with local water availability
    - Water-use monitoring in high-dependence regions
    - Agricultural diversification away from water-intensive crops where feasible
    - Water-risk assessment integrated into food supply-chain decisions
    - Longer-term resilience planning for hotspot regions
    """
)

st.divider()

# ============================================================
# METHODOLOGY & CAVEATS
# ============================================================

st.header("Methodology & Caveats")

st.markdown(
    f"""
    **Data sources:** FAOSTAT crop production data; FAO AQUASTAT water-stress and
    agricultural-withdrawal indicators. **Analysis year:** 2022.

    **Severe water stress:** ≥50% (project analytical threshold — stricter than the
    SDG 6.4.2 standard of 25%). **High agricultural dependence:** ≥75% of total water
    withdrawals. **High-pressure hotspot:** meets both — this is a project definition,
    not an official FAO risk index.

    **Coverage varies by crop** ({coverage_min:.0f}%–{coverage_max:.0f}%) — exposure
    percentages should be read together with coverage, not in isolation.

    **Values above 100%:** Under the SDG 6.4.2 methodology, water-stress values
    can exceed 100% when withdrawals exceed available renewable freshwater after
    environmental requirements. These values are retained rather than clipped.

    **Country coverage:** the dashboard analyses countries with recorded production
    in at least one focus crop and matched water indicators. Some countries have
    production or water data without a corresponding record in the other source.

    **This is an observational, cross-sectional analysis.** It does not claim that
    water stress causes lower production, and it is not a forecast of future
    production loss. Regional aggregates were intentionally excluded from
    country-level analysis. Agricultural withdrawal share measures water
    *withdrawal*, not consumption.

    """
)

st.caption("The Hidden Water Map — Query Queens | Women in Data Datathon 2026")
