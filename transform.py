import pandas as pd
def transform(df):
    df.columns = df.columns.str.replace(" ", "_")
    # duplicates
    df = df.drop_duplicates()
    #convert date to proper formats
    df['Order_Date'] = pd.to_datetime(df['Order_Date'],errors='coerce',  dayfirst=True)
    df['Ship_Date']  = pd.to_datetime(df['Ship_Date'],errors='coerce',  dayfirst=True)
    
     # handle missing values (only text columns)
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].fillna("Unknown")
        
    df['Delivery_Days'] = (df['Ship_Date'] - df['Order_Date']).dt.days
    # flag invalid deliveries
    df['Is_Invalid_Delivery'] = df['Delivery_Days'] < 0
    return df
df = pd.read_csv(r"C:\Users\keert\OneDrive\ETL Project\Data\train.csv")
result = transform(df)
print(result.head())
print(result[['Order_Date','Ship_Date']].head())
