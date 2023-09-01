import pandas as pd

# Data obtained from https://www.kaggle.com/datasets/kendallgillies/nflstatistics
df = pd.read_csv('Basic_Stats.csv')

# Removes all inactive players and players with incomplete information
df.dropna(subset='Current Team', inplace=True)
df.dropna(subset='Number', inplace=True)
df.dropna(subset='Birth Place', inplace=True)

# Makes a dictionary with names that are easier to use in a object oriented way
newDF = {
    'playerName'  : df['Name'],
    'age'         : df['Age'],
    'hometown'    : df['Birth Place'],
    'college'     : df['College'],
    'team'        : df['Current Team'],
    'number'      : round(df['Number']).astype(int),
    'height'      : round(df['Height (inches)']*2.54,2),        # Converts inches to centimeters
    'weight'      : round(df['Weight (lbs)']*0.453592,2),   # Converts pounds into kilos
    'team'        : df['Current Team'],
    'experience'  : df['Experience'],
    'id'          : df['Player Id']
}

# Turns the dictionary into a new dataFrame
df2=pd.DataFrame(newDF) 

# Prints out the new dataFrame as a test
print(df2)

# Transcribes the dataFrame into a new csv file
df2.to_csv('processedData.csv',index = False)
