"""Template for creating standard widgets in a Databricks notebook.

This module provides a reusable framework for generating a set of dropdown
widgets commonly used for filtering reports. It is designed to be easily
customizable and depends on the `dbutils` object provided by the Databricks
environment.

Key Programmatic Features:
  - MONTH_NBRS: Programmatically generates a list of month numbers ('1' to '12').
  - YEARS_MINUS_3: Programmatically generates a list containing the current
    year plus the three preceding years (e.g., ['2024', '2023', '2022', '2021']).

How to Use:
  1. In your Databricks notebook, import and call the function like this:
     ```python
     from cfuncs.display_widgets import display_widgets
     display_widgets(dbutils)
     ```
  2. Access the selected widget values in subsequent cells using:
     `dbutils.widgets.get("WidgetName")`.
"""

from datetime import datetime, timezone
import logging  # Import the logging module

# --- Date Values ---
DATETIMESTAMP_UTC: datetime = datetime.now(timezone.utc)
DATETIMESTAMP_LOCAL: datetime = DATETIMESTAMP_UTC.astimezone()

# --- Widget Choices ---
COCOMS: list = ['AFRICOM', 'EUCOM', 'CENTCOM', 'NORTHCOM', 'SOUTHCOM', 'INDOPACOM']
REPORT_TYPES: list = ['Monthly', 'Quarterly']
MONTH_NBRS: list[str] = [str(i) for i in range(1, 13)]
YEARS_MINUS_3: list[str] = [str(DATETIMESTAMP_LOCAL.year - i) for i in range(4)]

def display_widgets(_dbutils):
    
    widgets_to_create = [

        {'name': 'COCOM', 
         'defaultValue': 'AFRICOM', 
         'choices': COCOMS, 
         'label': "Identify your COCOM"},
        
        {'name': 'Report Type', 
         'defaultValue': 'Quarterly', 
         'choices': REPORT_TYPES, 
         'label': "Monthly or Quarterly"},
        
        {'name': 'Report Year', 
         'defaultValue': str(DATETIMESTAMP_LOCAL.year), 
         'choices': YEARS_MINUS_3, 
         'label': "Report Year"},
        
        {'name': 'Report Month', 
         'defaultValue': str(DATETIMESTAMP_LOCAL.month), 
         'choices': MONTH_NBRS, 
         'label': "Report Month"}
    
    ]

    for widget_params in widgets_to_create:
        
        try:
            _dbutils.widgets.dropdown(**widget_params)

        except Exception as e:
            logging.warning(f"Failed to create widget '{widget_params['name']}': {e}")
