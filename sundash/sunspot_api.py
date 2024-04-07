"""
File: sunspot_api.py
Description: API for accessing data from the sunspot.db
"""

import pandas as pd
import sqlite3

class SunspotAPI:
    con = None

    @staticmethod
    def connect(dbfile):
        """ make a connection """
        SunspotAPI.con = sqlite3.connect(dbfile, check_same_thread=False)


    @staticmethod
    def execute(query):
        """ executes query """
        return pd.read_sql_query(query, SunspotAPI.con)


    @staticmethod
    def get_sunspot_amt():
        """ gets data for amount of sunspots """
        query = "SELECT * FROM sunspot WHERE Daily_Sunspot_Total > -1"
        df = SunspotAPI.execute(query)
        return df


    @staticmethod
    def get_sunspot_amt_range(start_date, end_date):
        """ gets data for amount of sunspots over specified range """
        query = f"SELECT * FROM sunspot WHERE Date_Fraction > {start_date} AND Date_Fraction < {end_date} and Daily_Sunspot_Total > -1"
        df = SunspotAPI.execute(query)
        return df
    
