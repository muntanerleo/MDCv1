import streamlit as st
from src.dashboard.main import MedicationDashboard

def main():
    # Initialize and run dashboard
    dashboard = MedicationDashboard()
    dashboard.render()

if __name__ == "__main__":
    main()