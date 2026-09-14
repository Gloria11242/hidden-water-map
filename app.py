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

st.title("💧 The Hidden Water Map")
st.markdown("#### Where today's food production depends on water systems under structural pressure")
st.caption("FAOSTAT & FAO AQUASTAT · 2022 analysis")

st.divider()

# ============================================================
# ACT 1 — THE PARADOX (KPIs)
# ============================================================

st.markdown("### High production does not mean a resilient food system.")

n_countries = dashboard["Country"].nunique()
n_hotspot_countries = country_risk.loc[
    (country_risk["Water_Stress"] >= st.session_state.ws_threshold)
    & (country_risk["Agriculture_Withdrawal_Share"] >= st.session_state.agri_threshold),
    "Country"
].nunique()
sugar_exposure = summary.loc[summary["Crop"] == "Sugar cane", "Production_Exposed_%"].iloc[0]
coverage_min = summary["Water_Data_Coverage_%"].min()
coverage_max = summary["Water_Data_Coverage_%"].max()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Severe water stress", "≥50%")
    st.caption("Project threshold — stricter than SDG 6.4.2's 25% standard")

with col2:
    st.metric("Highest crop exposure", f"{sugar_exposure:.1f}%")
    st.caption("Sugar cane — 2022 production in countries with water stress ≥50%")

with col3:
    st.metric("High-pressure countries", f"{n_hotspot_countries}")
    st.caption("Meet both project hotspot thresholds")

with col4:
    st.metric("Data coverage", f"{coverage_min:.0f}%–{coverage_max:.0f}%")
    st.caption("Varies by crop — see Methodology")

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

st.header("2. The Pressure Map — Where Water Stress Meets Agricultural Dependence")

st.markdown(
    """
    Each point is a country. The vertical and horizontal lines mark the water-stress
    and agricultural-dependence thresholds selected in the sidebar. Countries in the
    upper-right combine both conditions — a **high-pressure hotspot (project
    definition, not an official FAO index)**.
    """
)

plot_df = country_risk.copy()
plot_df["Highlight"] = plot_df["Country"].apply(
    lambda c: c if c in ("India", "Pakistan") else "Other countries"
)

fig_risk = px.scatter(
    plot_df,
    x="Water_Stress",
    y="Agriculture_Withdrawal_Share",
    hover_name="Country",
    color="Highlight",
    color_discrete_map={
        "India": "#c0392b",
        "Pakistan": "#16a085",
        "Other countries": "#b0b7bd",
    },
    labels={
        "Water_Stress": "Water stress (%, log scale)",
        "Agriculture_Withdrawal_Share": "Agricultural withdrawal share (%)",
    },
)

fig_risk.update_xaxes(type="log")
fig_risk.add_vline(x=ws_threshold, line_dash="dash", line_color="#555",
                    annotation_text=f"{ws_threshold}% stress threshold")
fig_risk.add_hline(y=agri_threshold, line_dash="dash", line_color="#555",
                    annotation_text=f"{agri_threshold}% agricultural dependence threshold")

for c in ("India", "Pakistan"):
    row = country_risk.loc[country_risk["Country"] == c].iloc[0]
    fig_risk.add_annotation(
        x=row["Water_Stress"], y=row["Agriculture_Withdrawal_Share"],
        text=c, showarrow=True, arrowhead=2, ax=30, ay=-30, font=dict(size=12, color="#222")
    )

fig_risk.update_layout(height=550, legend_title_text="")
st.plotly_chart(fig_risk, use_container_width=True)

st.caption(
    "Water stress is shown on a log scale because some countries have values far above 100%. "
    "Under the SDG 6.4.2 methodology, values above 100% can occur when withdrawals exceed "
    "available renewable freshwater after environmental requirements. These values are not "
    "automatically data errors."
)

st.divider()

# ============================================================
# ACT 3 — FIVE-CROP FOOD EXPOSURE
# ============================================================

st.header("3. Food Production Exposure, Across All Five Crops")

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
    - Crop diversification where feasible and aligned with local water availability
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

    **Water stress above 100% can occur** under the SDG 6.4.2 methodology when
    withdrawals exceed available renewable freshwater after environmental requirements.
    These values are retained rather than clipped; they should be interpreted as a
    measure of pressure, not as a claim about a specific water source.

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
