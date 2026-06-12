import streamlit as st
import pandas as pd
import numpy as np
import networkx as nx
import plotly.express as px
import plotly.graph_objects as go
from pyvis.network import Network
import streamlit.components.v1 as components
import os

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Delhivery Graph Intelligence Dashboard",
    page_icon="📦",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

.main {
    background-color: #0e1117;
}

h1, h2, h3 {
    color: white;
}

.metric-container {
    background-color: #1c1f26;
    padding: 15px;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("📦 Optimizing Delivery ETAs with Graph-Based Network Intelligence")

st.markdown("""
### Delhivery Logistics Intelligence System

This dashboard provides:

- Graph-based logistics network intelligence
- Bottleneck hub detection
- Delayed corridor analysis
- Graph-enhanced ETA prediction insights
- FTL vs Carting recommendation framework
- Revenue-at-risk analysis
- Operations strategy recommendations
""")

# ---------------------------------------------------
# LOAD FILES
# ---------------------------------------------------

folder = "graph_project_outputs"

hub_df = pd.read_csv(f"{folder}/hub_bottleneck_scores.csv")
corridor_df = pd.read_csv(f"{folder}/graph_corridor_data.csv")
delayed_corridors = pd.read_csv(f"{folder}/delayed_corridors.csv")
comparison = pd.read_csv(f"{folder}/model_performance_comparison.csv")
route_analysis = pd.read_csv(f"{folder}/ftl_vs_carting_analysis.csv")
recommendation_summary = pd.read_csv(f"{folder}/route_type_recommendation_summary.csv")
top_hubs = pd.read_csv(f"{folder}/top_5_bottleneck_hubs.csv")
revenue_hubs = pd.read_csv(f"{folder}/top_5_revenue_hubs.csv")

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

section = st.sidebar.radio(
    "Navigation",
    [
        "Executive Overview",
        "Network Graph",
        "Bottleneck Hubs",
        "Delayed Corridors",
        "ETA Model Performance",
        "FTL vs Carting",
        "Revenue Impact",
        "Strategy Memo"
    ]
)

# ---------------------------------------------------
# EXECUTIVE OVERVIEW
# ---------------------------------------------------

if section == "Executive Overview":

    st.header("📊 Executive Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Hubs",
        len(hub_df)
    )

    col2.metric(
        "Total Corridors",
        len(corridor_df)
    )

    col3.metric(
        "Delayed Corridors",
        len(delayed_corridors)
    )

    col4.metric(
        "Top Bottleneck Score",
        round(top_hubs["bottleneck_score"].max(), 2)
    )

    st.markdown("---")

    st.subheader("Top 5 Bottleneck Hubs")

    fig = px.bar(
        top_hubs,
        x="bottleneck_score",
        y="hub",
        orientation="h",
        color="bottleneck_score",
        title="Top 5 Bottleneck Hubs"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Model Performance Comparison")

    fig2 = px.bar(
        comparison,
        x="Model",
        y="MAE",
        color="Model",
        title="MAE Comparison"
    )

    st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------
# NETWORK GRAPH
# ---------------------------------------------------

elif section == "Network Graph":

    st.header("🌐 Logistics Network Graph")

    st.markdown("""
    Facilities are modeled as nodes and movement corridors as directed edges.
    """)

    G = nx.DiGraph()

    sample_corridors = corridor_df.head(300)

    for _, row in sample_corridors.iterrows():

        G.add_edge(
            row["source_name"],
            row["destination_name"],
            weight=row["median_delay_ratio"]
        )

    net = Network(
        height="700px",
        width="100%",
        bgcolor="#111111",
        font_color="white",
        directed=True
    )

    net.from_nx(G)

    net.save_graph("graph.html")

    HtmlFile = open("graph.html", "r", encoding="utf-8")
    source_code = HtmlFile.read()

    components.html(source_code, height=700)

# ---------------------------------------------------
# BOTTLENECK HUBS
# ---------------------------------------------------

elif section == "Bottleneck Hubs":

    st.header("🚨 Bottleneck Hub Analysis")

    st.dataframe(top_hubs)

    fig = px.bar(
        top_hubs,
        x="hub",
        y="total_delay_contribution",
        color="bottleneck_score",
        title="Delay Contribution by Hub"
    )

    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.scatter(
        hub_df,
        x="betweenness_centrality",
        y="total_sla_breaches",
        size="bottleneck_score",
        color="bottleneck_score",
        hover_name="hub",
        title="Graph Risk vs SLA Breaches"
    )

    st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------
# DELAYED CORRIDORS
# ---------------------------------------------------

elif section == "Delayed Corridors":

    st.header("⛔ Chronic Delay Corridors")

    st.markdown("""
    Corridors where actual delivery time exceeds OSRM estimates by more than 20%.
    """)

    st.dataframe(delayed_corridors.head(20))

    top_corridors = delayed_corridors.head(10).copy()

    top_corridors["corridor"] = (
        top_corridors["source_name"]
        + " → " +
        top_corridors["destination_name"]
    )

    fig = px.bar(
        top_corridors,
        x="median_delay_ratio",
        y="corridor",
        orientation="h",
        color="median_delay_ratio",
        title="Top Delayed Corridors"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# MODEL PERFORMANCE
# ---------------------------------------------------

elif section == "ETA Model Performance":

    st.header("🤖 ETA Prediction Benchmarking")

    st.subheader("Model Comparison")

    st.dataframe(comparison)

    fig1 = px.bar(
        comparison,
        x="Model",
        y="MAE",
        color="Model",
        title="Mean Absolute Error Comparison"
    )

    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.bar(
        comparison,
        x="Model",
        y="15% Accuracy",
        color="Model",
        title="Business Accuracy Metric"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.success("""
    Graph-enhanced ETA prediction outperforms the baseline model by leveraging
    network structure, bottleneck intelligence, and corridor-level risk.
    """)

# ---------------------------------------------------
# FTL VS CARTING
# ---------------------------------------------------

elif section == "FTL vs Carting":

    st.header("🚚 FTL vs Carting Decision Framework")

    st.dataframe(route_analysis)

    fig = px.bar(
        route_analysis,
        x="route_type",
        y="avg_delay_ratio",
        color="route_type",
        title="Average Delay Ratio by Route Type"
    )

    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.pie(
        recommendation_summary,
        names="recommended_route_type",
        values="count",
        title="Recommended Route-Type Distribution"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.info("""
    High-risk corridors with elevated graph bottleneck scores are recommended
    for FTL movement to reduce SLA breaches and transit variability.
    """)

# ---------------------------------------------------
# REVENUE IMPACT
# ---------------------------------------------------

elif section == "Revenue Impact":

    st.header("💰 Revenue-at-Risk Analysis")

    st.dataframe(revenue_hubs)

    fig = px.bar(
        revenue_hubs,
        x="source_name",
        y="revenue_at_risk",
        color="revenue_at_risk",
        title="Revenue at Risk by Hub"
    )

    st.plotly_chart(fig, use_container_width=True)

    total_risk = revenue_hubs["revenue_at_risk"].sum()

    st.metric(
        "Total Revenue at Risk",
        f"₹ {total_risk:,.0f}"
    )

    st.success("""
    Upgrading the top bottleneck hubs can significantly reduce
    late deliveries and recover revenue at risk.
    """)

# ---------------------------------------------------
# STRATEGY MEMO
# ---------------------------------------------------

elif section == "Strategy Memo":

    st.header("📄 Network Operations Strategy Memo")

    memo_path = f"{folder}/network_operations_strategy_memo.txt"

    with open(memo_path, "r", encoding="utf-8") as f:
        memo = f.read()

    st.text_area(
        "Strategy Memo",
        memo,
        height=600
    )

    st.download_button(
        label="Download Strategy Memo",
        data=memo,
        file_name="network_operations_strategy_memo.txt",
        mime="text/plain"
    )


