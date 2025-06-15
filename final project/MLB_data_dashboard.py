# MLB Historical Data Dashboard - Fixed Version
# Run with: streamlit run mlb_dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import re

# Configure Streamlit page
st.set_page_config(
    page_title="MLB Historical Data Dashboard",
    page_icon="⚾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .sidebar-content {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and cache the cleaned data"""
    try:
        df = pd.read_csv("mlb_cleaned_data.csv")
        return df
    except FileNotFoundError:
        st.error("Cleaned data file not found. Please run the data scraping and cleaning scripts first.")
        return None
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def create_timeline_chart(df):
    """Create an interactive timeline chart of MLB events"""
    try:
        # Aggregate data by year and category
        timeline_data = df.groupby(['year', 'category']).size().reset_index(name='count')
        
        # Ensure we have valid data
        if timeline_data.empty:
            st.warning("No data available for timeline chart.")
            return None
        
        fig = px.scatter(
            timeline_data, 
            x='year', 
            y='category',
            size='count',
            color='category',
            title="MLB Historical Events Timeline",
            labels={'year': 'Year', 'category': 'Category', 'count': 'Number of Events'},
            hover_data=['count']
        )
        
        fig.update_layout(
            height=400,
            xaxis_title="Year",
            yaxis_title="Category",
            showlegend=True
        )
        
        return fig
    except Exception as e:
        st.error(f"Error creating timeline chart: {e}")
        return None

def create_era_distribution_chart(df):
    """Create a chart showing distribution of events across baseball eras"""
    try:
        if 'era' not in df.columns:
            # Create era if not exists
            df['era'] = df['year'].apply(lambda x: classify_era(x))
        
        era_counts = df['era'].value_counts()
        
        if era_counts.empty:
            st.warning("No era data available.")
            return None
        
        fig = px.pie(
            values=era_counts.values,
            names=era_counts.index,
            title="Distribution of Historical Records by Baseball Era",
            hole=0.4
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label'
        )
        
        fig.update_layout(height=400)
        
        return fig
    except Exception as e:
        st.error(f"Error creating era distribution chart: {e}")
        return None

def create_category_trends_chart(df):
    """Create a line chart showing trends in different categories over time"""
    try:
        # Group by year and category
        trends_data = df.groupby(['year', 'category']).size().reset_index(name='count')
        
        if trends_data.empty:
            st.warning("No trend data available.")
            return None
        
        fig = px.line(
            trends_data,
            x='year',
            y='count',
            color='category',
            title="Trends in MLB Historical Records by Category",
            labels={'year': 'Year', 'count': 'Number of Records', 'category': 'Category'}
        )
        
        fig.update_layout(
            height=400,
            xaxis_title="Year",
            yaxis_title="Number of Records",
            hovermode='x unified'
        )
        
        return fig
    except Exception as e:
        st.error(f"Error creating category trends chart: {e}")
        return None

def create_word_frequency_chart(df):
    """Create a chart showing most common words in descriptions"""
    try:
        if 'description' not in df.columns:
            return None
        
        # Extract words from descriptions
        all_text = ' '.join(df['description'].fillna('').astype(str))
        words = re.findall(r'\b[a-zA-Z]{4,}\b', all_text.lower())
        
        if not words:
            st.warning("No text data available for word frequency analysis.")
            return None
        
        # Count word frequencies
        from collections import Counter
        word_counts = Counter(words)
        
        # Get top 20 words
        top_words = dict(word_counts.most_common(20))
        
        if not top_words:
            return None
        
        # Create DataFrame for plotting
        word_df = pd.DataFrame({
            'words': list(top_words.keys()),
            'frequency': list(top_words.values())
        })
        
        fig = px.bar(
            word_df,
            x='frequency',
            y='words',
            orientation='h',
            title="Most Frequent Words in MLB Historical Records",
            labels={'frequency': 'Frequency', 'words': 'Words'}
        )
        
        fig.update_layout(
            height=500,
            yaxis={'categoryorder': 'total ascending'}
        )
        
        return fig
    except Exception as e:
        st.error(f"Error creating word frequency chart: {e}")
        return None

def classify_era(year):
    """Classify baseball eras"""
    if year < 1920:
        return 'Dead Ball Era'
    elif year < 1945:
        return 'Live Ball Era'
    elif year < 1960:
        return 'Integration Era'
    elif year < 1976:
        return 'Expansion Era'
    elif year < 1994:
        return 'Free Agency Era'
    elif year < 2006:
        return 'Steroid Era'
    else:
        return 'Modern Era'

def create_interactive_heatmap(df):
    """Create an interactive heatmap of events by decade and category"""
    try:
        # Create decade column if not exists
        if 'decade' not in df.columns:
            df['decade'] = (df['year'] // 10) * 10
        
        # Create pivot table for heatmap
        heatmap_data = df.groupby(['decade', 'category']).size().reset_index(name='count')
        
        if heatmap_data.empty:
            st.warning("No data available for heatmap.")
            return None
        
        heatmap_pivot = heatmap_data.pivot(index='category', columns='decade', values='count').fillna(0)
        
        if heatmap_pivot.empty:
            st.warning("Unable to create heatmap with current data structure.")
            return None
        
        fig = px.imshow(
            heatmap_pivot,
            title="MLB Historical Events Heatmap (by Decade and Category)",
            labels={'x': 'Decade', 'y': 'Category', 'color': 'Number of Events'},
            aspect='auto'
        )
        
        fig.update_layout(height=400)
        
        return fig
    except Exception as e:
        st.error(f"Error creating heatmap: {e}")
        return None

def display_key_metrics(df):
    """Display key metrics in the sidebar"""
    try:
        st.sidebar.markdown("### 📊 Key Metrics")
        
        col1, col2 = st.sidebar.columns(2)
        
        with col1:
            st.metric("Total Records", len(df))
            year_span = df['year'].max() - df['year'].min()
            st.metric("Years Covered", f"{year_span}")
        
        with col2:
            st.metric("Categories", df['category'].nunique())
            st.metric("Latest Year", int(df['year'].max()))
    except Exception as e:
        st.sidebar.error(f"Error displaying metrics: {e}")

def create_detailed_view(df, selected_category, selected_years):
    """Create detailed view for selected filters"""
    try:
        # Filter data
        filtered_df = df[
            (df['category'] == selected_category) & 
            (df['year'].between(selected_years[0], selected_years[1]))
        ]
        
        if len(filtered_df) == 0:
            st.warning("No data found for the selected filters.")
            return
        
        # Display summary statistics
        st.subheader(f"📋 {selected_category} Details ({selected_years[0]}-{selected_years[1]})")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Records Found", len(filtered_df))
        with col2:
            avg_year = filtered_df['year'].mean()
            st.metric("Average Year", f"{avg_year:.0f}")
        with col3:
            if 'importance_score' in filtered_df.columns:
                avg_importance = filtered_df['importance_score'].mean()
                st.metric("Avg Importance", f"{avg_importance:.2f}")
            else:
                st.metric("Data Quality", "Good")
        
        # Show top records
        st.subheader("🏆 Top Records")
        
        if 'importance_score' in filtered_df.columns:
            top_records = filtered_df.nlargest(5, 'importance_score')
        else:
            top_records = filtered_df.head(5)
        
        for idx, record in top_records.iterrows():
            with st.expander(f"📅 {record['year']} - {record.get('player_name', 'Record')}"):
                st.write(f"**Category:** {record['category']}")
                if 'description' in record and pd.notna(record['description']):
                    description = str(record['description'])
                    if len(description) > 300:
                        description = description[:300] + "..."
                    st.write(f"**Description:** {description}")
                if 'statistic' in record and pd.notna(record['statistic']):
                    st.write(f"**Statistic:** {record['statistic']}")
                if 'value' in record and pd.notna(record['value']):
                    st.write(f"**Value:** {record['value']}")
    except Exception as e:
        st.error(f"Error creating detailed view: {e}")

def safe_plot_display(fig, error_message="Error displaying chart"):
    """Safely display a plotly figure with error handling"""
    if fig is not None:
        try:
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"{error_message}: {e}")
            # Show alternative simple chart or message
            st.info("Chart could not be displayed. This might be due to data formatting issues.")
    else:
        st.info("No chart data available.")

def main():
    """Main dashboard function"""
    # Header
    st.markdown('<h1 class="main-header">⚾ MLB Historical Data Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Load data
    df = load_data()
    if df is None:
        st.stop()
    
    # Data validation
    required_columns = ['year', 'category']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        st.error(f"Missing required columns: {missing_columns}")
        st.info("Available columns: " + ", ".join(df.columns.tolist()))
        st.stop()
    
    # Sidebar filters
    st.sidebar.title("🎛️ Dashboard Controls")
    
    # Display key metrics
    display_key_metrics(df)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔍 Filters")
    
    # Year range filter
    try:
        min_year = int(df['year'].min())
        max_year = int(df['year'].max())
        year_range = st.sidebar.slider(
            "Select Year Range",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year),
            step=1
        )
    except Exception as e:
        st.sidebar.error(f"Error with year filter: {e}")
        year_range = (1900, 2024)  # Default fallback
    
    # Category filter
    try:
        categories = ['All'] + sorted(list(df['category'].unique()))
        selected_category = st.sidebar.selectbox("Select Category", categories)
    except Exception as e:
        st.sidebar.error(f"Error with category filter: {e}")
        selected_category = 'All'
    
    # Era filter (if available)
    try:
        if 'era' not in df.columns:
            df['era'] = df['year'].apply(lambda x: classify_era(x))
        eras = ['All'] + sorted(list(df['era'].unique()))
        selected_era = st.sidebar.selectbox("Select Era", eras)
    except Exception as e:
        st.sidebar.error(f"Error with era filter: {e}")
        selected_era = 'All'
    
    # Filter data based on selections
    try:
        filtered_df = df[df['year'].between(year_range[0], year_range[1])].copy()
        
        if selected_category != 'All':
            filtered_df = filtered_df[filtered_df['category'] == selected_category]
        
        if selected_era != 'All' and 'era' in df.columns:
            filtered_df = filtered_df[filtered_df['era'] == selected_era]
    except Exception as e:
        st.error(f"Error filtering data: {e}")
        filtered_df = df.copy()
    
    # Main content area
    st.markdown(f"### 📈 Showing {len(filtered_df)} records from {year_range[0]} to {year_range[1]}")
    
    # Create tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Trends", "🔥 Heatmap", "📋 Details"])
    
    with tab1:
        st.markdown("#### 📊 Data Overview")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Timeline chart
            timeline_fig = create_timeline_chart(filtered_df)
            safe_plot_display(timeline_fig, "Error displaying timeline chart")
        
        with col2:
            # Era distribution
            era_fig = create_era_distribution_chart(filtered_df)
            safe_plot_display(era_fig, "Error displaying era distribution chart")
        
        # Summary statistics
        st.markdown("#### 📋 Summary Statistics")
        try:
            summary_stats = []
            for category in filtered_df['category'].unique():
                cat_data = filtered_df[filtered_df['category'] == category]
                summary_stats.append({
                    'Category': category,
                    'Count': len(cat_data),
                    'First Year': int(cat_data['year'].min()),
                    'Last Year': int(cat_data['year'].max()),
                    'Avg Year': round(cat_data['year'].mean(), 1)
                })
            
            summary_df = pd.DataFrame(summary_stats)
            st.dataframe(summary_df, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating summary statistics: {e}")
    
    with tab2:
        st.markdown("#### 📈 Historical Trends")
        
        # Category trends
        trends_fig = create_category_trends_chart(filtered_df)
        safe_plot_display(trends_fig, "Error displaying trends chart")
        
        # Word frequency analysis
        if 'description' in filtered_df.columns:
            st.markdown("#### 🔤 Most Common Words")
            word_freq_fig = create_word_frequency_chart(filtered_df)
            safe_plot_display(word_freq_fig, "Error displaying word frequency chart")
    
    with tab3:
        st.markdown("#### 🔥 Event Intensity Heatmap")
        
        # Interactive heatmap
        heatmap_fig = create_interactive_heatmap(filtered_df)
        safe_plot_display(heatmap_fig, "Error displaying heatmap")
        
        # Decade comparison
        try:
            if 'decade' not in filtered_df.columns:
                filtered_df['decade'] = (filtered_df['year'] // 10) * 10
            
            decade_stats = filtered_df.groupby('decade').size().reset_index(name='count')
            decade_fig = px.bar(
                decade_stats,
                x='decade',
                y='count',
                title="Events by Decade",
                labels={'decade': 'Decade', 'count': 'Number of Events'}
            )
            safe_plot_display(decade_fig, "Error displaying decade chart")
        except Exception as e:
            st.error(f"Error creating decade comparison: {e}")
    
    with tab4:
        st.markdown("#### 📋 Detailed Records")
        
        if selected_category != 'All':
            create_detailed_view(df, selected_category, year_range)
        else:
            st.info("Please select a specific category from the sidebar to view detailed records.")
        
        # Raw data table (with pagination)
        st.markdown("#### 📊 Raw Data Sample")
        
        # Display options
        col1, col2 = st.columns(2)
        with col1:
            rows_to_show = st.selectbox("Rows to display", [10, 25, 50, 100], index=0)
        with col2:
            if st.button("🔄 Refresh Data"):
                st.rerun()
        
        # Show filtered data
        try:
            display_df = filtered_df.head(rows_to_show)
            st.dataframe(display_df, use_container_width=True)
            
            # Download button
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Filtered Data as CSV",
                data=csv,
                file_name=f"mlb_filtered_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        except Exception as e:
            st.error(f"Error displaying data table: {e}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <p>MLB Historical Data Dashboard | Data scraped from baseball-almanac.com</p>
        <p>Built with Streamlit & Plotly | Last updated: {}</p>
    </div>
    """.format(datetime.now().strftime("%Y-%m-%d %H:%M")), unsafe_allow_html=True)

if __name__ == "__main__":
    main()