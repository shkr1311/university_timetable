import pandas as pd
import zipfile

# Read dataset
df = pd.read_csv("nep2020_courses.csv")

# Programmes
programmes = ["FYUP", "B.Ed", "M.Ed", "ITEP"]

files = []
for prog in programmes:
    prog_df = df[df['programme'] == prog].reset_index(drop=True)  # reset index
    prog_df["course_id"] = prog_df.index + 1  # ID 1 se start
    file_name = f"{prog.replace('.', '').upper()}.csv"
    prog_df.to_csv(file_name, index=False)
    files.append(file_name)

# ZIP create
with zipfile.ZipFile("NEP2020_Programmes.zip", "w") as zipf:
    for file in files:
        zipf.write(file)
