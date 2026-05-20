import pandas as pd
from sqlalchemy import create_engine

# ─── EXTRACT ────────────────────────────────────────────────
def extract(filepath):
    df = pd.read_csv(filepath)
    print(f"[Extract] {len(df)} rows loaded")
    return df

# ─── TRANSFORM ──────────────────────────────────────────────
def transform(df):
    df.columns = df.columns.str.replace(" ", "_")
    df = df.drop_duplicates()

    df['Order_Date'] = pd.to_datetime(df['Order_Date'], errors='coerce', dayfirst=True)
    df['Ship_Date']  = pd.to_datetime(df['Ship_Date'],  errors='coerce', dayfirst=True)

    for col in df.select_dtypes(include=['object', 'str']).columns:
        df[col] = df[col].fillna("Unknown")

    df['Delivery_Days']       = (df['Ship_Date'] - df['Order_Date']).dt.days
    df['Is_Invalid_Delivery'] = df['Delivery_Days'] < 0

    print(f"[Transform] {df.shape[0]} rows, {df.shape[1]} columns")
    return df

# ─── LOAD ────────────────────────────────────────────────────
def load(df):
    from urllib.parse import quote_plus 

    # ── Fill these in ──────────────────────────────
    DB_USER     = "root"            # default MySQL username
    DB_PASSWORD = quote_plus("Keerthika@456")  # ← your real password here
    DB_HOST     = "localhost"
    DB_PORT     = "3306"            # default MySQL port
    DB_NAME     = "etl_project"
    # ───────────────────────────────────────────────

    connection_string = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    engine = create_engine(connection_string)

    # Load main cleaned data
    df.to_sql(
        name      = "orders",
        con       = engine,
        if_exists = "replace",
        index     = False
    )
    print(f"[Load] {len(df)} rows loaded into table: orders")

    # Load invalid records for auditing
    invalid_df = df[df['Is_Invalid_Delivery'] == True]
    if not invalid_df.empty:
        invalid_df.to_sql(
            name      = "invalid_orders",
            con       = engine,
            if_exists = "replace",
            index     = False
        )
        print(f"[Load] {len(invalid_df)} invalid rows → table: invalid_orders")

    print("[Load] All done!")

# ─── RUN ─────────────────────────────────────────────────────
if __name__ == "__main__":
    filepath = r"C:\Users\keert\OneDrive\ETL Project\Data\train.csv"

    raw_df   = extract(filepath)
    clean_df = transform(raw_df)
    load(clean_df)
