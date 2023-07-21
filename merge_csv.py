import pandas as pd
import os

directory = './dataset'
if not os.path.exists(directory):
    os.makedirs(directory)
    
# read the two CSV files
df1 = pd.read_csv('./export_logo_512/metadata.csv')
df2 = pd.read_csv('./export_logo2_512/metadata.csv')

# concatenate the two dataframes along the rows
merged_df = pd.concat([df1, df2])

# write the merged dataframe to a new CSV file
merged_df.to_csv('./dataset/metadata.csv', index=False)
