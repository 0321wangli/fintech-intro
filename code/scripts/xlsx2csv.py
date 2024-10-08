import pandas as pd

input_file = "../data/assignment_1_data.xlsx"
output_path = "../data/"

xls = pd.ExcelFile(input_file)
sheet_names = xls.sheet_names

for sheet in sheet_names:
    df = pd.read_excel(xls, sheet_name=sheet)

    output_file = f"{output_path}{sheet}.csv"

    df.to_csv(output_file, index=False)
    
    print(f"Sheet '{sheet}' has been saved as '{output_file}'")
