import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. Page Configuration
st.set_page_config(
    page_title="Biodiversity Hotspot Detection Engine",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Title & Description
st.title("🌿 Biodiversity Hotspot Detection Engine")
st.markdown("""
This intelligent engine processes ecological data, species distributions, and environmental stressors 
to pinpoint and prioritize critical biodiversity hotspots requiring conservation attention.
""")

# 3. Cached Data Loading 
@st.cache_data
def load_data():
    # Broken provinces list is fixed here safely
    provinces = [
        'Western Province', 
        'Central Province', 
        'Southern Province', 
        'Northern Province'
    ]
    
    data = pd.DataFrame({
        'latitude': np.random.uniform(5.9, 9.9, size=100),   
        'longitude': np.random.uniform(79.6, 81.9, size=100),
        'species_richness': np.random.randint(10, 150, size=100),
        'threat_index': np.random.uniform(0.1, 1.0, size=100),
        'region': np.random.choice(provinces, size=100)
    })
    data['hotspot_score'] = data['species_richness'] * data['threat_index']
    return data

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    df = pd.DataFrame()

# 4. Sidebar Controls & Filters
st.sidebar.header("🕹️ Engine Controls")

if not df.empty:
    all_regions = ["All Regions"] + list(df['region'].unique())
    selected_region = st.sidebar.selectbox("Select Target Region", all_regions)
    
    threat_threshold = st.sidebar.slider(
        "Minimum Threat Index Trigger", 
        min_value=0.0, 
        max_value=1.0, 
        value=0.4, 
        step=0.05
    )
    
    filtered_df = df[df['threat_index'] >= threat_threshold]
    if selected_region != "All Regions":
        filtered_df = filtered_df[filtered_df['region'] == selected_region]

    # 5. Top-Level High-Value Metrics
    st.markdown("### 📊 Engine Status Overview")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Total Ecosystem Grid Points Analyzed", value=len(df))
    with col2:
        active_hotspots = len(filtered_df[filtered_df['hotspot_score'] > 50])
        st.metric(label="Active Hotspots Detected", value=active_hotspots, delta=f"{active_hotspots - len(df)//4} from baseline")
    with col3:
        avg_threat = filtered_df['threat_index'].mean() if not filtered_df.empty else 0
        st.metric(label="Average Threat Level", value=f"{avg_threat:.2f}")

    st.markdown("---")

    # 6. Geospatial Mapping & Visualization Layout
    left_col, right_col = st.columns([2, 1])

    with left_col:
        st.subheader("🗺️ Hotspot Geographic Mapping")
        if not filtered_df.empty:
            fig = px.scatter_mapbox(
                filtered_df, 
                lat="latitude", 
                lon="longitude", 
                size="species_richness", 
                color="hotspot_score",
                color_continuous_scale=px.colors.sequential.YlOrRd, 
                zoom=6.5, 
                height=500,
                hover_name="region",
                hover_data=["species_richness", "threat_index", "hotspot_score"]
            )
            fig.update_layout(mapbox_style="carto-positron")
            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No data points match your current filter criteria.")

    with right_col:
        st.subheader("📈 Threat Distribution Analysis")
        if not filtered_df.empty:
            fig_hist = px.histogram(
                filtered_df, 
                x="hotspot_score", 
                nbins=15, 
                title="Density of Hotspot Severity Scores",
                labels={'hotspot_score': 'Severity Score'},
                color_discrete_sequence=['#2ecc71']
            )
            fig_hist.update_layout(margin={"r":10,"t":40,"l":10,"b":10})
            st.plotly_chart(fig_hist, use_container_width=True)
        else:
            st.info("Adjust the sliders to view distribution dynamics.")

    # 7. Raw Engine Output Data Inspection
    st.markdown("---")
    st.subheader("📋 Engine Core Data Log")
    with st.expander("Expand to audit raw processed environmental telemetry"):
        st.dataframe(filtered_df, use_container_width=True)

else:
    st.info("Please connect your backend data loader to populate the engine telemetry.")
