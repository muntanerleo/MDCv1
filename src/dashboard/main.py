import streamlit as st
import pandas as pd

from src.db.database import DatabaseConnection
from src.db.preprocessing import preprocess_medication_data
from src.utils.viz_utils import (
    create_pie_chart, 
    create_bar_chart, 
    create_scatter_chart
)

class MedicationDashboard:
    def __init__(self):
        """
        Initialize the dashboard
        """
        # Load and preprocess data
        db_connection = DatabaseConnection()
        raw_df = db_connection.load_medications_data()
        self.df = preprocess_medication_data(raw_df)
    
    def overview_panel(self):
        """
        Create overview panel with key metrics and visualizations
        """
        st.header("Medication Overview")
        
        # KPI Columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Drugs", len(self.df))
        
        with col2:
            habit_forming_count = self.df[self.df['habit_forming'] == 'Yes'].shape[0]
            st.metric("Habit Forming Drugs", habit_forming_count)
        
        with col3:
            st.metric("Unique Therapeutic Types", 
                    self.df['therapeutic_type'].nunique())
        
        # Therapeutic Type Distribution
        st.subheader("Therapeutic Type Distribution")
        type_counts = self.df['therapeutic_type'].value_counts()
        fig = create_pie_chart(type_counts, "Drug Distribution by Therapeutic Type")
        st.plotly_chart(fig)
    
    def drug_comparison_panel(self):
        """
        Create drug comparison panel with interactive visualizations
        """
        st.header("Drug Comparison")
        
        # Filters
        col1, col2 = st.columns(2)
        with col1:
            therapeutic_type_filter = st.multiselect(
                "Select Therapeutic Types", 
                self.df['therapeutic_type'].unique()
            )
        with col2:
            use_case_filter = st.multiselect(
                "Select Use Cases", 
                self.df['usecase'].unique()
            )
        
        # Filter dataframe
        filtered_df = self.df.copy()
        if therapeutic_type_filter:
            filtered_df = filtered_df[filtered_df['therapeutic_type'].isin(therapeutic_type_filter)]
        if use_case_filter:
            filtered_df = filtered_df[filtered_df['usecase'].isin(use_case_filter)]
        
        # Side Effects Bar Chart
        st.subheader("Side Effects Comparison")
        side_effect_data = filtered_df.melt(
            id_vars=['drug_name'], 
            value_vars=[f'side_effect_{i}' for i in range(1, 6)],
            var_name='side_effect_column', 
            value_name='side_effect'
        )
        side_effect_counts = side_effect_data.dropna()['side_effect'].value_counts().head(10)
        
        fig_side_effects = create_bar_chart(
            side_effect_counts.index, 
            side_effect_counts.values,
            "Top 10 Side Effects",
            "Side Effect",
            "Frequency"
        )
        st.plotly_chart(fig_side_effects)
    
    def safety_risk_panel(self):
        """
        Create safety and risk analysis panel
        """
        st.header("Safety and Risk Analysis")
        
        # Risk Matrix
        st.subheader("Risk Matrix")
        risk_df = self.df.copy()
        risk_df['risk_score'] = (
            (risk_df['habit_forming'] == 'Yes').astype(int) * 2 + 
            risk_df['side_effects'].str.split(',').str.len()
        )
        
        fig_risk = create_scatter_chart(
            risk_df, 
            'therapeutic_type', 
            'risk_score', 
            'habit_forming', 
            "Risk Matrix: Therapeutic Type vs Risk Score"
        )
        st.plotly_chart(fig_risk)
    
    def administration_panel(self):
        """
        Create administration and patient suitability panel
        """
        st.header("Administration Methods")
        
        # Administration Method Distribution
        admin_counts = self.df['administration_method'].value_counts()
        fig_admin = create_pie_chart(
            admin_counts, 
            "Distribution of Administration Methods"
        )
        st.plotly_chart(fig_admin)
    
    def render(self):
        """
        Main dashboard layout and navigation
        """
        st.title("Medication Information Dashboard")
        
        # Sidebar for navigation
        page = st.sidebar.selectbox(
            "Select a Panel", 
            [
                "Overview", 
                "Drug Comparison", 
                "Safety Analysis", 
                "Administration Methods"
            ]
        )
        
        # Panel selection
        if page == "Overview":
            self.overview_panel()
        elif page == "Drug Comparison":
            self.drug_comparison_panel()
        elif page == "Safety Analysis":
            self.safety_risk_panel()
        elif page == "Administration Methods":
            self.administration_panel()