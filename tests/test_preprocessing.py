import pandas as pd
import pytest
import numpy as np

from your_module import preprocess_medication_data  # Replace with actual import path

class TestMedicationDataPreprocessing:
    def test_generic_names_combination(self):
        """
        Test combining generic names across multiple columns
        """
        # Create a sample DataFrame with multiple generic name columns
        input_df = pd.DataFrame({
            'generic_name_1': ['Paracetamol', 'Ibuprofen'],
            'generic_name_2': ['Acetaminophen', np.nan],
            'generic_name_3': [np.nan, 'Advil'],
            'generic_name_4': ['Tylenol', np.nan],
            'generic_name_5': [np.nan, np.nan],
            'other_column': ['A', 'B']
        })
        
        # Expected output
        expected_generic_names = [
            'Paracetamol, Acetaminophen, Tylenol',
            'Ibuprofen, Advil'
        ]
        
        # Process the DataFrame
        processed_df = preprocess_medication_data(input_df)
        
        # Assertions
        assert 'generic_names' in processed_df.columns
        pd.testing.assert_series_equal(
            processed_df['generic_names'], 
            pd.Series(expected_generic_names, name='generic_names')
        )
    
    def test_side_effects_combination(self):
        """
        Test combining side effects across multiple columns
        """
        # Create a sample DataFrame with multiple side effect columns
        input_df = pd.DataFrame({
            'side_effect_1': ['Drowsiness', 'Headache'],
            'side_effect_2': ['Dizziness', np.nan],
            'side_effect_3': [np.nan, 'Nausea'],
            'side_effect_4': ['Fatigue', np.nan],
            'side_effect_5': [np.nan, np.nan],
            'other_column': ['A', 'B']
        })
        
        # Expected output
        expected_side_effects = [
            'Drowsiness, Dizziness, Fatigue',
            'Headache, Nausea'
        ]
        
        # Process the DataFrame
        processed_df = preprocess_medication_data(input_df)
        
        # Assertions
        assert 'side_effects' in processed_df.columns
        pd.testing.assert_series_equal(
            processed_df['side_effects'], 
            pd.Series(expected_side_effects, name='side_effects')
        )
    
    def test_empty_dataframe(self):
        """
        Test preprocessing with an empty DataFrame
        """
        # Create an empty DataFrame with expected columns
        input_df = pd.DataFrame(columns=[
            'generic_name_1', 'generic_name_2', 'generic_name_3', 
            'generic_name_4', 'generic_name_5',
            'side_effect_1', 'side_effect_2', 'side_effect_3', 
            'side_effect_4', 'side_effect_5'
        ])
        
        # Process the empty DataFrame
        processed_df = preprocess_medication_data(input_df)
        
        # Assertions
        assert processed_df.empty
        assert 'generic_names' in processed_df.columns
        assert 'side_effects' in processed_df.columns
    
    def test_dataframe_not_modified(self):
        """
        Test that the original DataFrame is not modified
        """
        # Create a sample DataFrame
        input_df = pd.DataFrame({
            'generic_name_1': ['Paracetamol'],
            'generic_name_2': ['Acetaminophen'],
            'side_effect_1': ['Drowsiness'],
            'side_effect_2': ['Dizziness']
        })
        
        # Keep a copy of the original DataFrame
        original_df = input_df.copy()
        
        # Process the DataFrame
        _ = preprocess_medication_data(input_df)
        
        # Verify original DataFrame remains unchanged
        pd.testing.assert_frame_equal(input_df, original_df)
    
    def test_no_combined_columns(self):
        """
        Test preprocessing a DataFrame without generic name or side effect columns
        """
        # Create a DataFrame without combined columns
        input_df = pd.DataFrame({
            'drug_name': ['Drug A', 'Drug B'],
            'description': ['Description 1', 'Description 2']
        })
        
        # Process the DataFrame
        processed_df = preprocess_medication_data(input_df)
        
        # Assertions
        assert 'generic_names' in processed_df.columns
        assert 'side_effects' in processed_df.columns
        assert processed_df['generic_names'].tolist() == ['', '']
        assert processed_df['side_effects'].tolist() == ['', '']
        assert processed_df.shape[1] == input_df.shape[1] + 2
    
    def test_mixed_data_types(self):
        """
        Test preprocessing with mixed data types
        """
        # Create a DataFrame with mixed data types
        input_df = pd.DataFrame({
            'generic_name_1': ['Paracetamol', 123],
            'generic_name_2': [np.nan, 'Ibuprofen'],
            'side_effect_1': ['Drowsiness', None],
            'side_effect_2': [456, 'Headache']
        })
        
        # Expected output (converted to strings)
        expected_generic_names = ['Paracetamol', '123, Ibuprofen']
        expected_side_effects = ['Drowsiness', 'Headache']
        
        # Process the DataFrame
        processed_df = preprocess_medication_data(input_df)
        
        # Assertions
        assert 'generic_names' in processed_df.columns
        assert 'side_effects' in processed_df.columns
        pd.testing.assert_series_equal(
            processed_df['generic_names'], 
            pd.Series(expected_generic_names, name='generic_names')
        )
        pd.testing.assert_series_equal(
            processed_df['side_effects'], 
            pd.Series(expected_side_effects, name='side_effects')
        )