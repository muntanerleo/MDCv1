import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import streamlit as st

def create_pie_chart(data: pd.Series, title: str):
    """
    Create a pie chart for categorical data
    
    Args:
        data (pd.Series): Categorical data to visualize
        title (str): Chart title
    
    Returns:
        plotly.graph_objs figure
    """
    return px.pie(
        data, 
        values=data.values, 
        names=data.index,
        title=title
    )

def create_bar_chart(x, y, title: str, x_label: str, y_label: str):
    """
    Create a bar chart
    
    Args:
        x: X-axis data
        y: Y-axis data
        title (str): Chart title
        x_label (str): X-axis label
        y_label (str): Y-axis label
    
    Returns:
        plotly.graph_objs figure
    """
    return px.bar(
        x=x, 
        y=y,
        title=title,
        labels={'x': x_label, 'y': y_label}
    )

def create_scatter_chart(df: pd.DataFrame, x: str, y: str, color: str, title: str):
    """
    Create a scatter chart
    
    Args:
        df (pd.DataFrame): Source DataFrame
        x (str): X-axis column
        y (str): Y-axis column
        color (str): Color column
        title (str): Chart title
    
    Returns:
        plotly.graph_objs figure
    """
    return px.scatter(
        df, 
        x=x, 
        y=y,
        color=color,
        hover_data=['drug_name', 'side_effects'],
        title=title
    )