import requests
import pandas as pd
import numpy as np

# web_2010 = requests.get("https://api.census.gov/data/2010/surname.html?get=NAME,COUNT&PCT2PRACE&PCTAIAN&PCTAPI&PCTBLACK&PCTHISPANIC&PCTWHITE")
# content_2010 = web_2010.json()
#
col_name = ["PCT2PRACE","PCTAIAN","PCTAPI","PCTBLACK","PCTHISPANIC","PCTWHITE"]
#
# total_2010_df = pd.DataFrame(content_2010[1:], columns=['Surname', 'Count', "PCT2PRACE","PCTAIAN","PCTAPI","PCTBLACK","PCTHISPANIC","PCTWHITE"])
# total_2010_df.insert(0, "Year", 2010)
# total_2010_df = total_2010_df.replace('(S)', np.nan)
# total_2010_df[['Count']] = total_2010_df['Count'].astype(int)
# total_2010_df[col_name] = total_2010_df[col_name].astype(float)
# total_2010_df.to_csv("./data/total_2010.csv", index=False)


web_2000 = requests.get("https://api.census.gov/data/2000/surname.html?get=NAME,COUNT&PCT2PRACE&PCTAIAN&PCTAPI&PCTBLACK&PCTHISPANIC&PCTWHITE")
content_2000 = web_2000.json()

total_2000_df = pd.DataFrame(content_2000[1:], columns=['Surname', 'Count', "PCT2PRACE","PCTAIAN","PCTAPI","PCTBLACK","PCTHISPANIC","PCTWHITE"])
total_2000_df.insert(0, "Year", 2000)
total_2000_df = total_2000_df.replace('(S)', np.nan)
total_2000_df[['Count']] = total_2000_df['Count'].astype(int)
total_2000_df[col_name] = total_2000_df[col_name].astype(float)
total_2000_df.to_csv("./data/total_2000.csv", index=False)

# total = pd.concat([total_2000_df, total_2010_df], ignore_index=True)
# total = total.replace('(S)', np.nan)
# col_name = ["PCT2PRACE","PCTAIAN","PCTAPI","PCTBLACK","PCTHISPANIC","PCTWHITE"]
# total[['Count']] = total['Count'].astype(int)
# total[col_name] = total[col_name].astype(float)
# total.to_csv("./data/total.csv", index=False)

