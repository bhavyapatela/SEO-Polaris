import pandas as pd

file = "Data/whistle_data.xlsx"
xls = pd.ExcelFile(file)

for sheet in xls.sheet_names:
    print(f"\n--- Sheet: {sheet} ---")
    df = pd.read_excel(file, sheet_name=sheet)
    print("Columns:", list(df.columns))
    print("Shape:", df.shape)
    print("First row:")
    print(df.head(1).to_dict(orient='records'))