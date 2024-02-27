import pandas as pd
from io import StringIO
from lobster_translator.helpers import get_interaction_from_line

def carfile_to_df(input_path: str, corresponding_structure: str) -> pd.DataFrame:
    # Read the file content
    with open(input_path, 'r') as file:
        lines = file.readlines()

    interactions = [get_interaction_from_line(line) for line in lines if line.startswith("No.")]
    integrated_interactions = ['i' + interaction for interaction in interactions]
    alternating = [element for pair in zip(interactions,integrated_interactions) for element in pair] # This looks very arcane

    # Data starts after interactions, join the remaining lines
    data = ''.join(lines[(3 + len(interactions)):])

    # Read the data into a DataFrame
    df = pd.read_csv(StringIO(data), delim_whitespace=True, header=None)

    # Rename columns
    df.columns = ['E', 'total', 'itotal'] + alternating

    df['structure'] = corresponding_structure

    return df