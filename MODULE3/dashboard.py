"""
AI-Driven Secure Quant & IoT Terminal - Module 3 (Web Dashboard)
Applies User-Centered Design (UCD) principles to visualize financial data and AI sentiment.
"""
import streamlit as st
import pandas as pd
import altair as alt

# --- UCD Configuration: Accessibility and Cognitive Load ---
# Set page configuration to utilize screen space effectively but cleanly
st.set_page_config(
    page_title="Quant Terminal Dashboard", 
    page_icon="📈", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- UCD Principle: Colorblind-friendly Palette ---
# Avoid relying solely on red/green. We use distinct colors for positive/negative 
# and add clear text indicators.
COLOR_PROFIT = "#2ECC71" # Accessible Green
COLOR_LOSS = "#E74C3C"   # Accessible Red
COLOR_NEUTRAL = "#95A5A6" # Neutral Gray

def load_mock_data():
    """
    Simulates loading data from Module 1 (ETL & AI) and Module 2 (Risk Math).
    TODO: Integrate with main.py or database once all modules are connected.
    """
    # Mock portfolio data
    assets = ['AAPL', 'MSFT', 'GOOGL', 'GOLD', 'URA']
    return pd.DataFrame({
        'Asset': assets,
        'Price': [150.2, 310.5, 2750.1, 1850.0, 22.5],
        'Daily Change (%)': [1.2, -0.5, 2.1, -1.5, 3.4],
        'AI Sentiment': ['Positive', 'Neutral', 'Positive', 'Negative', 'Positive'],
        'Risk Level': ['Low', 'Low', 'Medium', 'High', 'Medium']
    })

def render_dashboard():
    """
    Renders the UI components applying visual hierarchy.
    """
    # --- UCD Principle: Clear Visual Hierarchy (Title & Main KPIs first) ---
    st.title("🛡️ AI-Driven Secure Quant Terminal")
    st.markdown("### Portfolio Overview & Risk Analysis")
    
    # Load data
    df = load_mock_data()
    
    # --- UCD Principle: Minimize Cognitive Load (Glanceable KPIs) ---
    # Displaying high-level metrics in columns so the user gets context instantly
    col1, col2, col3 = st.columns(3)
    
    total_assets = len(df)
    avg_change = df['Daily Change (%)'].mean()
    
    with col1:
        st.metric(label="Total Tracked Assets", value=total_assets)
    with col2:
        st.metric(label="Average Daily Change", value=f"{avg_change:.2f}%")
    with col3:
        st.metric(label="System Status", value="Active / Secure")

    st.divider()

    # --- UCD Principle: Accessible Data Visualization ---
    # We use Altair for native, lightweight, interactive charts
    st.markdown("#### Asset Performance & AI Sentiment")
    
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('Asset', title='Ticker Symbol', sort=None),
        y=alt.Y('Daily Change (%)', title='Change (%)'),
        color=alt.Color('AI Sentiment', scale=alt.Scale(
            domain=['Positive', 'Negative', 'Neutral'],
            range=[COLOR_PROFIT, COLOR_LOSS, COLOR_NEUTRAL]
        )),
        tooltip=['Asset', 'Price', 'Daily Change (%)', 'AI Sentiment', 'Risk Level']
    ).properties(
        title="Daily Change by Asset (Color-coded by NLP Analysis)",
        height=400
    ).interactive()
    
    st.altair_chart(chart, use_container_width=True)

    # --- UCD Principle: Detailed Data on Demand ---
    # Don't overwhelm the user with tables initially, but make them available
    st.markdown("#### Raw Data & Risk Assessment")
    
    # Using Streamlit's dataframe to display tabular data cleanly
    st.dataframe(
        df, 
        use_container_width=True,
        hide_index=True
    )

if __name__ == "__main__":
    render_dashboard()
