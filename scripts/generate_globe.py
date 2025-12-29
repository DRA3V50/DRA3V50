# scripts/generate_globe.py
import json
import plotly.graph_objects as go

# Load node/coverage data
with open("coverage.json") as f:
    data = json.load(f)

lats, lons, labels, colors = [], [], [], []
for node in data["nodes"]:
    lats.append(node["lat"])
    lons.append(node["lon"])
    labels.append(node["name"])
    colors.append(node.get("attack_stage_color", "#5cb3ff"))

fig = go.Figure(go.Scattergeo(
    lat=lats,
    lon=lons,
    text=labels,
    mode='markers+text',
    marker=dict(size=8, color=colors, line=dict(width=1, color='white')),
    textposition="top center"
))

fig.update_layout(
    geo=dict(
        showland=True, landcolor="#0a0f1a",
        showcountries=True, countrycolor="#1e2a45",
        showocean=True, oceancolor="#0f1726"
    ),
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#a0c8ff"),
)

# Optional: Add FBI-eye marker at center
fig.add_layout_image(
    dict(
        source="https://i.imgur.com/YOUR_EYE_ICON.png",
        xref="paper", yref="paper",
        x=0.5, y=0.5, sizex=0.1, sizey=0.1,
        xanchor="center", yanchor="middle",
        layer="above"
    )
)

# Save interactive HTML
fig.write_html("assets/globe_live.html")
print("Globe generated successfully!")

