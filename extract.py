import pandas as pd 
df = pd.read_csv(r"C:\Users\keert\OneDrive\ETL Project\Data\train.csv")
"""
print(df.head())
print(df.columns)
print(df.info())
"""
df.columns = df.columns.str.replace(" ", "_")
print(df.columns)
