import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import os
import warnings
import sys
import path
warnings.filterwarnings("ignore")

# Streamlit Configuration
st.set_page_config(page_title="Dashboard", page_icon=":bar_chart:", layout="wide")



# Custom CSS for KPIs and UI
st.markdown("""
    <style>
            .kpi {
    text-align: center;
    font-size: 22px;
    margin: 20px 0;
    font-weight: bold;
    border: 3px solid transparent;
    border-radius: 15px;
    padding: 15px;
    position: relative;
    transition: all 0.3s ease-in-out;
}

.kpi:hover {
    border: 3px solid rgba(255, 69, 0, 1); /* Glowing border on hover */
    box-shadow: 0 0 15px rgba(255, 69, 0, 0.7); /* Subtle border glow */
}

.kpi:hover span {
    color: rgba(255, 69, 0, 1); /* Glowing text on hover */
    text-shadow: 0 0 10px rgba(255, 69, 0, 0.8); /* Glowing text effect */
}

.kpi span {
    font-size: 18px;
    transition: all 0.3s ease-in-out;
}


    </style>
""", unsafe_allow_html=True)

# Header
# st.title(":bar_chart: Trend-Forge Dashboard")
# st.markdown('<style>div.block-container{padding-top:2rem}</style>', unsafe_allow_html=True)

# Logo (Replace 'logo.png' with the path to your logo)

st.image("logo.png", width=570)


st.markdown('<style>div.block-container{padding-top:0rem}</style>', unsafe_allow_html=True)

st.markdown('<style>div.block-container{padding-bottom:2rem}</style>', unsafe_allow_html=True)
# Add custom CSS for upper-right alignment and hover glow
# Add custom CSS for hover glow effect
st.markdown("""
    <style>
        .header-title {
            font-size: 36px; /* Adjust title size */
            font-weight: bold;
            color: #333; /* Default text color */
            margin: 0;
            
            transition: all 0.3s ease-in-out; /* Smooth hover effect */
        }
        .header-title:hover {
            color: rgba(255, 69, 0, 1); /* Glowing text color */
            text-shadow: 0 0 2px rgba(255, 69, 0, 1); /* Glowing effect */
        }
    </style>
    <h1 class="header-title">Dashboard 📊</h1>
""", unsafe_allow_html=True)





# File Uploader
fl = st.file_uploader(":file_folder: Upload a file", type=(["csv", "xlsx"]))


# Reference columns from output.csv
# Reference columns from output.csv
# Reference columns from output.csv
expected_columns = [
    "_id", "Posting_Date", "Total_Reactions", "Total_Comments", "Total_Shares", 
    "Likes", "Loves", "Wows", "Hahas", "Sads", "Angrys", 
    "Is_Link", "Is_Photo", "Is_Status", "Is_Video", "Is_Carousel", "Is_Reel"
]



# File handling
if fl is not None:
    filename = fl.name
    st.write(f"Uploaded File: {filename}")
    df = pd.read_csv(fl, encoding="ISO-8859-1")
    
    # Check if columns match
    if set(df.columns) != set(expected_columns):
        st.warning("⚠️ Uploaded file's columns do not match the expected format of `output.csv`. Please refine your data.")
    else:
        st.subheader("Preview of Uploaded Data")
        st.dataframe(df.head(5))
else:
    # Use default data when no file is uploaded
    st.subheader("Preview of Default Data")
    file_path = os.path.join(os.path.dirname(__file__), "output.csv")#C:\Users\HP\Desktop\DASHBOARD\DASHBOARD\output.csv
    df = pd.read_csv("output.csv", encoding="ISO-8859-1")
    st.dataframe(df.head(5))


# Date Conversion
df["Posting_Date"] = pd.to_datetime(df["Posting_Date"], errors="coerce").dt.date



#Add styles for the sidebar button
st.markdown(
    """
    <style>
        .stButton > button {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            padding: 10px 20px;
            font-size: 16px;
            font-weight: bold;
            color: white;
            background: linear-gradient(to orange 15%,red 50%,violet);
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-shadow: 0 0 5px rgba(0, 0, 0, 0.5);
            box-shadow: 0 0 10px rgba(255, 69, 0, 0.8), 0 0 20px rgba(255, 215, 0, 0.7);
            margin-bottom: 20px;
            margin-top: 20px;
        }

        .stButton > button:hover {
            background: linear-gradient(to right,orange ,red 40%,purple);
            box-shadow: 0 0 20px rgba(255, 69, 0, 1), 0 0 20px rgba(255, 215, 0, 1), 0 0 20px rgba(255, 0, 0, 0.8);
            color: white;
        }

        .stButton > button img {
            width: 24px;
            height: 24px;
            vertical-align: middle;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar: Back to Homepage Button
with st.sidebar:
    if st.button("🏠 Back to Homepage", key="homepage_button"):
        st.write('<meta http-equiv="refresh" content="0; url=https://devking-kunal.github.io/Trend-Forge/" />', unsafe_allow_html=True)

# Sidebar Filters
st.sidebar.header("Filters")
start_date = min(df["Posting_Date"])
end_date = max(df["Posting_Date"])

# Date Input
col1, col2 = st.columns(2)
with col1:
    date1 = st.sidebar.date_input("Start Date", start_date)

with col2:
    date2 = st.sidebar.date_input("End Date", end_date)

df = df[(df["Posting_Date"] >= pd.to_datetime(date1).date()) & (df["Posting_Date"] <= pd.to_datetime(date2).date())]

content_type = st.sidebar.multiselect(
    "Content Type",
    options=["Is_Link", "Is_Photo", "Is_Status", "Is_Video", "Is_Carousel", "Is_Reel"],
    default=["Is_Photo", "Is_Video"],
)
if content_type:
    filters = [col for col in content_type if col in df.columns]
    df = df[df[filters].any(axis=1)]

# Calculate percentage changes
prev_reactions = df["Total_Reactions"].sum() * 0.9  # Example: Previous data approximation
prev_comments = df["Total_Comments"].sum() * 0.9
prev_shares = df["Total_Shares"].sum() * 0.9

reaction_change = (df["Total_Reactions"].sum() - prev_reactions) / prev_reactions * 100
comment_change = (df["Total_Comments"].sum() - prev_comments) / prev_comments * 100
share_change = (df["Total_Shares"].sum() - prev_shares) / prev_shares * 100

# Key Performance Indicators (KPIs)
st.subheader("Key Insights")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'''
        <div class="kpi">
            Total Reactions<br>
            {df["Total_Reactions"].sum():,} 
        </div>
    ''', unsafe_allow_html=True)
with col2:
    st.markdown(f'''
        <div class="kpi">
            Total Comments<br>
            {df["Total_Comments"].sum():,} 
        </div>
    ''', unsafe_allow_html=True)
with col3:
    st.markdown(f'''
        <div class="kpi">
            Total Shares<br>
            {df["Total_Shares"].sum():,} 
        </div>
    ''', unsafe_allow_html=True)

# Visualizations
st.subheader("Visualizations")

# Post Performance Over Time (Different Colors for Content Type)
content_types = ["Is_Link", "Is_Photo", "Is_Status", "Is_Video", "Is_Carousel", "Is_Reel"]
colors = ["#DB4437", "#4285F4", "#F4B400", "#0F9D58", "#A142F4", "#F4A142"]
fig1 = go.Figure()
for content, color in zip(content_types, colors):
    if content in df.columns:
        df_content = df[df[content] == 1]
        fig1.add_trace(go.Scatter(
            x=df_content["Posting_Date"],
            y=df_content["Total_Reactions"],
            mode='lines+markers',
            name=content,
            line=dict(color=color, width=2)
        ))
fig1.update_layout(
    title="Post Performance Over Time",
    xaxis_title="Posting Date",
    yaxis_title="Total Reactions",
    template="plotly_white",
    showlegend=True
)
st.plotly_chart(fig1, use_container_width=True)

# Reaction Types Distribution
reaction_sum = df[["Likes", "Loves", "Wows", "Hahas", "Sads", "Angrys"]].sum().reset_index()
reaction_sum.columns = ["Reaction Type", "Count"]

fig_reaction_types = px.bar(
    reaction_sum,
    x="Reaction Type",
    y="Count",
    title="Reaction Types Distribution",
    color="Reaction Type",
    color_discrete_sequence=px.colors.qualitative.Bold
)
fig_reaction_types.update_traces(marker_line_color="black", marker_line_width=1)
fig_reaction_types.update_layout(title_x=0.5, title_font_size=16)

# Content Types Distribution
content_counts = df[filters].sum().reset_index()
content_counts.columns = ["Content Type", "Count"]

fig_content_types = px.pie(
    content_counts,
    names="Content Type",
    values="Count",
    title="Content Type Distribution",
    color_discrete_sequence=["#4285F4", "#FF5733", "#FBBC05", "#34A853", "#EA4335", "#9B59B6"]  # Google colors
)
fig_content_types.update_layout(title_x=0.5, title_font_size=16)

# Display in one row
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig_reaction_types, use_container_width=True)

with col2:
    st.plotly_chart(fig_content_types, use_container_width=True)

#Positive and Negative reactions
# Define positive and negative reactions
positive_reactions = ["Likes", "Loves", "Wows", "Hahas"]
negative_reactions = ["Sads", "Angrys"]

# Calculate total positive and negative reactions
df["Positive_Reactions"] = df[positive_reactions].sum(axis=1)
df["Negative_Reactions"] = df[negative_reactions].sum(axis=1)

# Positive vs Negative Reactions 


# Customize the colors for positive and negative reactions
positive_color = "#34A853"  # Green for Positive Reactions
negative_color = "#EA4335"  # Red for Negative Reactions

# Create a stacked bar chart for Positive and Negative Reactions
fig_positive_negative_stacked = px.bar(
    df.groupby("Posting_Date")[["Positive_Reactions", "Negative_Reactions"]].sum().reset_index(),
    x="Posting_Date",
    y=["Positive_Reactions", "Negative_Reactions"],
    title="Positive vs Negative Reactions Over Time",
    color_discrete_sequence=[positive_color, negative_color],  # Apply custom colors
    barmode="stack"  # Stack the bars to show total values
)

# Display the chart
st.plotly_chart(fig_positive_negative_stacked, use_container_width=True)


# Pie chart for overall positive vs negative reactions
reaction_totals = {
    "Positive Reactions": df["Positive_Reactions"].sum(),
    "Negative Reactions": df["Negative_Reactions"].sum()
}
fig_pie_reactions = px.pie(
    names=list(reaction_totals.keys()),
    values=list(reaction_totals.values()),
    title="Overall Positive vs Negative Reactions",
    color_discrete_sequence=["#0F9D58", "#DB4437"]
)
st.plotly_chart(fig_pie_reactions, use_container_width=True)


# #Top Performing post analysis
#

# Top Performing post analysis
# Define performance metric (e.g., Total Engagement = Reactions + Comments + Shares)
df["Total_Engagement"] = df["Total_Reactions"] + df["Total_Comments"] + df["Total_Shares"]

# Top 5 performing posts based on Total Engagement
top_posts = df.nlargest(5, "Total_Engagement")[["Posting_Date", "Total_Engagement", "Total_Reactions", "Total_Comments", "Total_Shares"]]

# Bar chart for top-performing posts
# Bar chart for top-performing posts
fig_top_posts = px.bar(
    top_posts,
    x="Posting_Date",
    y="Total_Engagement",
    text="Total_Engagement",
    title="Top Performing Posts by Total Engagement",
    color="Total_Engagement",
    color_continuous_scale="viridis"
)

# Set the title font size once
fig_top_posts.update_layout(
    title_font_size=24  # Adjust the size of the title here (increase as needed)
)

fig_top_posts.update_traces(textfont_size=12, textposition="outside", marker_line_color="black", marker_line_width=1)

# Display bar chart and top posts details in one row with aligned headings
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig_top_posts, use_container_width=True)

with col2:
    st.markdown("<h3>Details of Top Performing Posts</h3>", unsafe_allow_html=True)
    st.dataframe(top_posts.style.highlight_max(axis=0, color="#F4B400", subset=["Total_Engagement"]))








 # Export Filtered Data
st.subheader("Export Data")
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("Download Filtered Data as CSV", data=csv, file_name="filtered_data.csv", mime="text/csv")

st.markdown("""
    <div style="
        position: fixed; 
        bottom: 0; 
        width: 100%; 
        text-align: left; 
        padding: 2px 0; 
        font-size: 20px; 
        font-weight: bold; 
        background: rgba(0, 0, 0, 0.5); 
        color: white; 
        text-shadow: 0 0 5px rgba(255, 69, 0, 0.8), 0 0 10px rgba(255, 215, 0, 0.7); 
        z-index: 999;
        backdrop-filter: blur(10px);
        border-top: 2px solid rgba(255, 215, 0, 0.7);
        background: none;
    ">
        © 2025 Trend-Forge. All rights reserved.  
    </div>
""", unsafe_allow_html=True)






























