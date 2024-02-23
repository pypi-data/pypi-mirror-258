import pandas as pd

def run_remove_duplicates(input_file_path, output_file_path):

    file_path = input_file_path

    df = pd.read_excel(file_path)

    df = df.dropna(subset=['DOI'])

    df = df.drop_duplicates(subset=['DOI'])

    output_file = output_file_path

    df.to_csv(output_file, index=False, sep='\t', encoding='utf-8')

    # Made by Huilong Chen.

