import streamlit as st
import pandas as pd
import plotly.express as px
import networkx as nx
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("github_100_repos.csv")

st.title("🚀 GitHub Project Health Dashboard")

# Sidebar
repo = st.selectbox("Select Repository", df["repo"])

row = df[df["repo"] == repo].iloc[0]

# Metrics
st.metric("⭐ Stars", row["stars"])
st.metric("👥 Contributors", row["contributors"])
st.metric("📦 Commits", row["commits"])
st.metric("🔀 PR Merge Rate", round(row["pr_merge_rate"], 2))

# Health Score
st.subheader("💚 Health Score")

score = row["health_score"]

if score > 0.7:
    st.success(f"{score*100:.2f}% Healthy")
elif score > 0.4:
    st.warning(f"{score*100:.2f}% Moderate")
else:
    st.error(f"{score*100:.2f}% Poor")

# Top Repos Chart
st.subheader("📊 Top 10 Repositories")

top10 = df.sort_values("health_score", ascending=False).head(10)
st.bar_chart(top10.set_index("repo")["health_score"])

# Scatter Plot
st.subheader("📈 Contributors vs Commits")

fig = px.scatter(df, x="contributors", y="commits",
                 size="health_score", hover_name="repo")
st.plotly_chart(fig)

# Network Graph
st.subheader("🌐 Collaboration Network")

G = nx.Graph()

for i in range(min(20, len(df))):
    G.add_node(df["repo"][i])
    if i > 0:
        G.add_edge(df["repo"][i-1], df["repo"][i])

plt.figure(figsize=(8,6))
nx.draw(G, with_labels=True, node_size=800, font_size=8)
st.pyplot(plt)

# Data preview
st.subheader("📄 Dataset")
st.dataframe(df)