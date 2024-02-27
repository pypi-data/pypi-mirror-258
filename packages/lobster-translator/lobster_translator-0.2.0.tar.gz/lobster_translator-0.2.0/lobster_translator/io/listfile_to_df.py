import pandas as pd

def listfile_to_df(input_path, corresponding_structure):
    df = pd.read_csv(input_path, sep=r'\s+', engine='python', skiprows=1, header=None)
    df['structure'] = corresponding_structure
    df['interaction'] = df[1] + df[2]
    df['icobi'] = df[7]
    df['distance'] = df[3]
    return df[['structure','interaction','icobi', 'distance']]