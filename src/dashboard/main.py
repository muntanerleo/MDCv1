import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from src.db.database import DatabaseConnection
from src.db.preprocessing import preprocess_drug_details_1
from src.utils.viz_utils import (
    create_pie_chart, 
    create_bar_chart
)

class MedicationDashboard:
    def __init__(self):
        """
        Initialize the dashboard
        """
        # Load and preprocess data
        db_connection = DatabaseConnection()
        raw_df = db_connection.load_drug_details('drug_details_1')
        self.df = preprocess_drug_details_1(raw_df)
        self.raw_df = raw_df  # Store raw_df for later use
    
    
    def overview_panel(self):
        """
        Create overview panel with key metrics and visualizations
        """
        st.header("Medication Overview")
        
        # KPI Columns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Drugs", len(self.df))
        
        with col2:
            habit_forming_count = self.df[self.df['habit_forming'] == 'yes'].shape[0]
            st.metric("Habit Forming Drugs", habit_forming_count)
        
        with col3:
            st.metric("Unique Therapeutic Types", 
                    self.df['therapeutic_type'].nunique())
        
        with col4:
            st.write("Data Sourced From", 
                    self.df['data_source'][0])
        
        # Therapeutic Type Distribution
        st.subheader("Therapeutic Type Distribution")
        type_counts = self.df['therapeutic_type'].value_counts()
        fig = create_pie_chart(type_counts, "Drug Distribution by Therapeutic Type")
        st.plotly_chart(fig)
    
    
    def generics_panel(self):
        """
        Create panel showing generic drug availability
        """
        st.header("Generic Drug Availability")
        
        # Identify drugs with generic names
        generic_columns = ['generic_name_1', 'generic_name_2', 'generic_name_3', 'generic_name_4', 'generic_name_5']
        
        # Calculate percentage of drugs with actual generic names
        def has_valid_generic(row):
            return any(pd.notna(row[col]) and row[col] != 'NA' for col in generic_columns)
        
        drugs_with_generics = self.df.apply(has_valid_generic, axis=1)
        generic_percentage = (drugs_with_generics.sum() / len(self.df)) * 100
        
        # Display overall generics percentage
        st.metric("Percentage of Drugs with Generic Names", f"{generic_percentage:.2f}%")
        
        # Drug Search Section
        st.subheader("Drug Generic Search")
        search_drug = st.text_input("Enter a drug name to find its generics")
        
        if search_drug:
            # Case-insensitive partial matching
            matching_drugs = self.df[self.df['drug_name'].str.contains(search_drug, case=False)]
            
            if len(matching_drugs) > 0:
                for _, drug in matching_drugs.drop_duplicates(subset=['drug_name']).iterrows():
                    # Collect valid generic names, prioritizing first generic names
                    drug_generics = []
                    for col in generic_columns:
                        if pd.notna(drug[col]) and drug[col] != 'NA':
                            drug_generics.append(drug[col])
                    
                    # Display drug generic information
                    st.subheader(f"Generic Information for {drug['drug_name']}")
                    
                    if drug_generics:
                        st.write("Generic Names:")
                        for generic in drug_generics:
                            st.write(f"- {generic}")
                    else:
                        st.write("No generic names available for this drug.")
                    
                    # Optional: Show additional drug details
                    st.write(f"**Therapeutic Type:** {drug['therapeutic_type']}")
            else:
                st.write("No matching drugs found.")
        
        
        # Therapeutic type filter
        st.subheader("Generic Availability by Therapeutic Type")
        selected_type = st.selectbox(
            "Select Therapeutic Type", 
            self.df['therapeutic_type'].unique()
        )
        
        # Filter by therapeutic type
        type_df = self.df[self.df['therapeutic_type'] == selected_type]
        
        # Detailed generic information
        st.subheader("Drugs with Generic Names")
        
        # Prepare generic information
        generic_info = []
        for _, row in type_df.iterrows():
            drug_generics = [row[col] for col in generic_columns if pd.notna(row[col]) and row[col] != 'NA']
            if drug_generics:
                generic_info.append({
                    'Drug Name': row['drug_name'],
                    'Generic Names': ', '.join(drug_generics),
                    'Number of Generics': len(drug_generics)
                })
        
        # Display as DataFrame
        if generic_info:
            generic_df = pd.DataFrame(generic_info)
            st.dataframe(generic_df)
        else:
            st.write("No generic names found in the selected therapeutic type.")
    
    
    def drug_comparison_panel(self):
        """
        Create drug comparison panel with interactive visualizations
        """
        st.header("Drug Comparison")
        
        # Filters
        col2 = st.columns(2)[1]  # Use only col2
        with col2:
            use_case_filter = st.multiselect(
                "Select Use Cases", 
                options=self.df['usecase'].unique(),  # Ensure this column exists
                default=None
            )
        
        # Filter dataframe
        filtered_df = self.df.copy()
        if use_case_filter:
            filtered_df = filtered_df[filtered_df['usecase'].isin(use_case_filter)]
        
        # Debugging Outputs
        st.write("Use Case Filter Selected:", use_case_filter)
        st.write("Filtered DataFrame Preview:", filtered_df.head())
        
        # Side Effects Bar Chart
        st.subheader("Side Effects Comparison")
        side_effect_data = filtered_df.melt(
            id_vars=['drug_name'], 
            value_vars=['side_effect_1'],
            var_name='side_effect_column', 
            value_name='side_effect'
        )
        # side_effect_counts = side_effect_data[(side_effect_data['side_effect'] != 'NA')].dropna()['side_effect'].value_counts().head(10)
        side_effect_counts = side_effect_data[(side_effect_data['side_effect'] != 'NA')].dropna()['side_effect'].value_counts()
        
        # Debugging Outputs
        st.write("Side Effect Counts:", side_effect_counts)
        
        # Create Bar chart to display the side effects
        bar_chart = go.Figure(
            data=[
                go.Bar(
                    x=side_effect_counts.index,
                    y=side_effect_counts.values,
                    marker=dict(color='rgb(55, 83, 109)'),
                )
            ]
        )
        
        # Customize the layout of the bar chart
        bar_chart.update_layout(
            title='Top 10 Most Frequent Side Effects',
            xaxis=dict(title='Side Effects', tickangle=-45),
            yaxis=dict(title='Count'),
            template='plotly_white',
        )
        
        # Display the chart in Streamlit
        st.plotly_chart(bar_chart)
    
    
    def administration_needs_panel(self):
        """
        Create panel showing drug availability for specific administration needs
        """
        st.header("Drug Administration Availability")
        
        # Administration method filters
        st.subheader("Filter by Administration Method")
        admin_method = st.selectbox(
            "Select Administration Method", 
            self.df['administration_method'].unique()
        )
        
        # Filter dataframe by selected administration method
        filtered_df = self.df[self.df['administration_method'] == admin_method]
        
        # Key metrics
        st.metric(f"Drugs Available via {admin_method}", len(filtered_df))
        
        # Therapeutic type breakdown
        st.subheader(f"Therapeutic Types for {admin_method}")
        type_counts = filtered_df['therapeutic_type'].value_counts()
        
        # Pie chart of therapeutic types
        fig = create_pie_chart(
            type_counts, 
            f"Therapeutic Types for {admin_method} Administration"
        )
        st.plotly_chart(fig)
        
        # Detailed drug list
        st.subheader(f"Drugs with {admin_method} Administration")
        display_columns = ['drug_name', 'therapeutic_type', 'usecase']
        st.dataframe(filtered_df[display_columns])
    
    
    def habit_correlation_panel(self):
        """
        Analyze correlation between administration method and habit-forming properties
        """
        st.header("Administration Method & Habit Forming Analysis")
        
        # Specified administration methods
        allowed_methods = [
            'tablet', 'syrup', 'capsule', 'injection', 'suspension', 'iv', 
            'ointment', 'drop', 'cream', 'inhaler', 'kit', 'oral drops', 
            'nasal spray', 'lotion', 'spray', 'eye gel', 'oral gel', 
            'eye drop', 'eye/ear drops', 'flextouch', 'soap', 
            'oral solution', 'shampoo', 'expectorant'
        ]
        
        # Filter dataframe to include only specified methods
        filtered_df = self.df[self.df['administration_method'].isin(allowed_methods)]
        
        # Prepare data for analysis
        habit_data = filtered_df.groupby('administration_method')['habit_forming'].value_counts(normalize=True).unstack().fillna(0)
        
        # Plotting correlation
        st.subheader("Habit Forming Distribution by Administration Method")
        fig = create_bar_chart(
            habit_data.index, 
            habit_data['yes'] * 100,  # Percentage of habit-forming drugs
            "Percentage of Habit Forming Drugs by Administration Method",
            "Administration Method",
            "Percentage of Habit Forming Drugs"
        )
        st.plotly_chart(fig)
        
        # Side effects correlation
        st.subheader("Side Effects and Habit Forming Relationship")
        side_effect_columns = [f'side_effect_{i}' for i in range(1, 6)]
        
        # Count side effects for habit-forming drugs
        habit_forming_drugs = self.df[self.df['habit_forming'] == 'yes']
        non_habit_forming_drugs = self.df[self.df['habit_forming'] == 'no']
        
        def count_side_effects(df):
            side_effects = df[side_effect_columns].values.flatten()
            return pd.Series(side_effects).dropna().value_counts()
        
        habit_side_effects = count_side_effects(habit_forming_drugs)
        non_habit_side_effects = count_side_effects(non_habit_forming_drugs)
        
        # Side effects comparison
        st.subheader("Top Side Effects Comparison")
        comparison_df = pd.DataFrame({
            'Habit Forming Drugs': habit_side_effects.head(10),
            'Non-Habit Forming Drugs': non_habit_side_effects.head(10)
        })
        st.dataframe(comparison_df)
        
        # Heatmap Visualization
        st.header("Habit Forming Analysis Heatmap")
        
        # Create pivot table for heatmap
        heatmap_data = filtered_df.pivot_table(
            index='administration_method', 
            columns='habit_forming', 
            aggfunc='size', 
            fill_value=0
        )
        
        # Normalize to percentages
        heatmap_percentages = heatmap_data.div(heatmap_data.sum(axis=1), axis=0) * 100
        
        # Plotly heatmap
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_percentages.values,
            x=heatmap_percentages.columns,
            y=heatmap_percentages.index,
            hoverongaps = False,
            colorscale='Viridis'
        ))
        
        fig.update_layout(
            title='Habit Forming Distribution Across Administration Methods',
            xaxis_title='Habit Forming Status',
            yaxis_title='Administration Method'
        )
        
        st.plotly_chart(fig)
    
    
    def db_panel(self):
        """
        Create panel to display database table
        """
        st.header("Database Viewer")
        st.dataframe(self.raw_df)
    
    
    def raw_data_panel(self):
        """
        Panel to upload and view CSV data from the data folder.
        """
        st.header("Raw Data Viewer")
        
        # Allow the user to select a CSV file from the data folder
        data_folder = "../../data/medicine_dataset.csv"
        
        # Check if the file exists
        if not os.path.exists(data_folder):
            st.error(f"Raw data not found at `{data_folder}`. Please check again later.")
            return
        
        # Read and display the CSV file
        try:
            csv_df = pd.read_csv(data_folder)
            st.write(f"Displaying contents of: `{os.path.basename(data_folder)}`")
            st.dataframe(csv_df)
        except Exception as e:
            st.error(f"Error reading the file: {e}")
    
    
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
                "Generics",
                "Drug Comparison",
                "Administration Needs",
                "Habit Correlation",
                "Database Viewer",
                "Raw Data Viewer"
            ]
        )
        
        # Panel selection
        if page == "Overview":
            self.overview_panel()
        elif page == "Generics":
            self.generics_panel()
        elif page == "Drug Comparison":
            self.drug_comparison_panel()
        elif page == "Administration Needs":
            self.administration_needs_panel()
        elif page == "Habit Correlation":
            self.habit_correlation_panel()
        elif page == "Database Viewer":
            self.db_panel()
        elif page == "Raw Data Viewer":
            self.db_panel()