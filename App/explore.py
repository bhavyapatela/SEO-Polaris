import pandas as pd

file = "Data/whistle_data.xlsx"

xls = pd.ExcelFile(file)

print(xls.sheet_names)