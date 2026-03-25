import streamlit as st
import pandas as pd
import plotly.express as px
import networkx as nx
import plotly.graph_objects as go
import numpy as np
import random

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="GitHub Analytics Dashboard", layout="wide")

st.title("🚀 GitHub Collaboration & Health Dashboard")

# ---------------------------
# LOAD DATA
# ---------------------------
df = pd.read_csv("github_100_repos.csv")

# ---------------------------
# HANDLE MISSING VALUES
# ---------------------------
df = df.fillna(0)

# ---------------------------
# FEATURE ENGINEERING
# ---------------------------
df["issue_resolution_rate"] = df["closed_issues"] / (df["open_issues"] + df["closed_issues"] + 1)
df["commit_efficiency"] = df["commits"] / (df["contributors"] + 1)

# ---------------------------
# HEALTH SCORE (IMPROVED)
# ---------------------------
df["health_score"] = (
    0.25 * (df["commit_efficiency"] / df["commit_efficiency"].max()) +
    0.25 * df["issue_resolution_rate"] +
    0.25 * df["pr_merge_rate"] +
    0.25 * (df["contributors"] / df["contributors"].max())
)

# ---------------------------
# SIDEBAR FILTERS
# ---------------------------
st.sidebar.header("🔍 Filters")

selected_repo = st.sidebar.selectbox("Select Repository", df["repo"])

min_commits = st.sidebar.slider("Minimum Commits", 0, int(df["commits"].max()), 0)

filtered_df = df[df["commits"] >= min_commits]

row = df[df["repo"] == selected_repo].iloc[0]

# ---------------------------
# KPI CARDS
# ---------------------------
st.subheader("📊 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("⭐ Stars", int(row["stars"]))
col2.metric("👥 Contributors", int(row["contributors"]))
col3.metric("📦 Commits", int(row["commits"]))
col4.metric("🔀 PR Merge Rate", round(row["pr_merge_rate"], 2))

# ---------------------------
# HEALTH SCORE DISPLAY
# ---------------------------
st.subheader("💚 Health Score")

score = row["health_score"]

if score > 0.7:
    st.success(f"{score*100:.2f}% → Healthy ✅")
elif score > 0.4:
    st.warning(f"{score*100:.2f}% → Moderate ⚠️")
else:
    st.error(f"{score*100:.2f}% → Poor ❌")

# ---------------------------
# TOP REPOSITORIES
# ---------------------------
st.subheader("🏆 Top 10 Healthy Repositories")

top10 = filtered_df.sort_values("health_score", ascending=False).head(10)

fig1 = px.bar(
    top10,
    x="repo",
    y="health_score",
    color="health_score",
    title="Top Performing Repositories"
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------------------
# SCATTER PLOT
# ---------------------------
st.subheader("📈 Contributors vs Commits")

fig2 = px.scatter(
    filtered_df,
    x="contributors",
    y="commits",
    size="health_score",
    color="health_score",
    hover_name="repo",
    title="Collaboration Analysis"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------------------
# TIME TREND (SIMULATED)
# ---------------------------
st.subheader("📅 Activity Trend")

df["activity_trend"] = np.random.randint(50, 200, size=len(df))

fig3 = px.line(
    df.head(10),
    x="repo",
    y="activity_trend",
    title="Repository Activity Trend"
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------------------
# CONTRIBUTOR ANALYSIS
# ---------------------------
st.subheader("👥 Contributor Analysis")

top_contributors = df.sort_values("contributors", ascending=False).head(10)

fig4 = px.bar(
    top_contributors,
    x="repo",
    y="contributors",
    title="Top Contributor-heavy Repositories"
)

st.plotly_chart(fig4, use_container_width=True)

# ---------------------------
# CORRELATION HEATMAP
# ---------------------------
st.subheader("📊 Correlation Heatmap")

corr = df[["commits", "contributors", "pr_merge_rate", "health_score"]].corr()

fig5 = px.imshow(corr, text_auto=True, title="Feature Correlation")

st.plotly_chart(fig5, use_container_width=True)

# ---------------------------
# REALISTIC NETWORK GRAPH
# ---------------------------
st.subheader("🌐 Collaboration Network")

G = nx.Graph()

contributors = [f"Dev{i}" for i in range(10)]

for repo in df["repo"].head(10):
    assigned = random.sample(contributors, k=3)
    for dev in assigned:
        G.add_node(dev)
        G.add_node(repo)
        G.add_edge(dev, repo)

pos = nx.spring_layout(G, seed=42)

edge_x, edge_y = [], []
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x += [x0, x1, None]
    edge_y += [y0, y1, None]

node_x, node_y = [], []
for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)

fig6 = go.Figure()

fig6.add_trace(go.Scatter(
    x=edge_x, y=edge_y,
    mode='lines',
    line=dict(width=1, color='gray'),
    hoverinfo='none'
))

fig6.add_trace(go.Scatter(
    x=node_x, y=node_y,
    mode='markers+text',
    text=list(G.nodes()),
    textposition="top center",
    marker=dict(size=12, color='skyblue')
))

fig6.update_layout(showlegend=False)

st.plotly_chart(fig6, use_container_width=True)

# ---------------------------
# INSIGHTS
# ---------------------------
st.subheader("💡 Insights")

high = df[df["health_score"] > 0.7]
low = df[df["health_score"] < 0.4]

st.write(f"✅ Healthy Projects: {len(high)}")
st.write(f"⚠️ Moderate Projects: {len(df) - len(high) - len(low)}")
st.write(f"❌ Poor Projects: {len(low)}")

st.write(f"🔥 Best Repo: {df.loc[df['health_score'].idxmax(), 'repo']}")
st.write(f"📉 Weakest Repo: {df.loc[df['health_score'].idxmin(), 'repo']}")

# ---------------------------
# DATA TABLE
# ---------------------------
st.subheader("📄 Dataset")
st.dataframe(df)
