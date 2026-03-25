import streamlit as st
import pandas as pd
import plotly.express as px
import networkx as nx
import matplotlib.pyplot as plt

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="GitHub Project Health Dashboard",
    page_icon="🚀",
    layout="wide"
)

# -----------------------------
# CUSTOM CSS (Aesthetic UI)
# -----------------------------
st.markdown("""
<style>
.metric-card {
    background-color: #0f172a;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    color: white;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.3);
}

.metric-title {
    font-size: 18px;
    color: #94a3b8;
}

.metric-value {
    font-size: 28px;
    font-weight: bold;
}

.dashboard-title {
    text-align:center;
    font-size:40px;
    font-weight:bold;
}

.section-title {
    font-size:24px;
    margin-top:30px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("github_100_repos.csv")

# -----------------------------
# HEADER
# -----------------------------
st.markdown("<div class='dashboard-title'>🚀 GitHub Project Health Dashboard</div>", unsafe_allow_html=True)
st.write("Monitor repository health, contribution activity, and collaboration insights.")

st.divider()

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("🔎 Repository Filter")
repo = st.sidebar.selectbox("Select Repository", df["repo"])

row = df[df["repo"] == repo].iloc[0]

# -----------------------------
# KPI METRICS
# -----------------------------
st.markdown("<div class='section-title'>📊 Repository Metrics</div>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

col1.metric("⭐ Stars", row["stars"])
col2.metric("👥 Contributors", row["contributors"])
col3.metric("📦 Commits", row["commits"])
col4.metric("🔀 PR Merge Rate", f"{row['pr_merge_rate']:.2f}")

# -----------------------------
# HEALTH SCORE
# -----------------------------
st.markdown("<div class='section-title'>💚 Health Score</div>", unsafe_allow_html=True)

score = row["health_score"]

progress = int(score * 100)
st.progress(progress)

if score > 0.7:
    st.success(f"Repository Health: {progress}% — Healthy 🚀")
elif score > 0.4:
    st.warning(f"Repository Health: {progress}% — Moderate ⚠️")
else:
    st.error(f"Repository Health: {progress}% — Poor ❌")

# -----------------------------
# CHARTS SECTION
# -----------------------------
st.markdown("<div class='section-title'>📈 Repository Insights</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

# Top repositories
with col1:

    top10 = df.sort_values("health_score", ascending=False).head(10)

    fig = px.bar(
        top10,
        x="repo",
        y="health_score",
        color="health_score",
        title="Top 10 Healthy Repositories",
        color_continuous_scale="viridis"
    )

    fig.update_layout(xaxis_tickangle=-45)

    st.plotly_chart(fig, use_container_width=True)

# Scatter plot
with col2:

    fig2 = px.scatter(
        df,
        x="contributors",
        y="commits",
        size="health_score",
        color="health_score",
        hover_name="repo",
        title="Contributors vs Commits",
        color_continuous_scale="plasma"
    )

    st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# NETWORK GRAPH
# -----------------------------
st.markdown("<div class='section-title'>🌐 Collaboration Network</div>", unsafe_allow_html=True)

G = nx.Graph()

for i in range(min(20, len(df))):
    G.add_node(df["repo"][i])
    if i > 0:
        G.add_edge(df["repo"][i-1], df["repo"][i])

plt.figure(figsize=(10,6))
pos = nx.spring_layout(G)

nx.draw(
    G, pos,
    with_labels=True,
    node_size=1500,
    node_color="#6366f1",
    font_size=8,
    font_color="white",
    edge_color="gray"
)

st.pyplot(plt)

# -----------------------------
# DATASET PREVIEW
# -----------------------------
st.markdown("<div class='section-title'>📄 Repository Dataset</div>", unsafe_allow_html=True)

st.dataframe(df, use_container_width=True)
