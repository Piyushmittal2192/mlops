import os
import argparse
import pandas as pd
from get_data import  read_params
from load_data import load_and_save
from sklearn.model_selection import train_test_split

def split_and_saved_data(config_path):
    config = read_params(config_path)
    raw_data_path = config['load_data']['raw_dataset_csv']
    train_data_path = config['split_data']['train_path']
    test_data_path = config['split_data']['test_path']
    test_size = config['split_data']['test_size']
    random_state = config['base']['random_state']
    df = pd.read_csv(raw_data_path, sep = ',', encoding='utf-8')

    train_data, test_data = train_test_split(df, test_size= test_size, random_state=random_state)

    train_data.to_csv(train_data_path, sep=",", index=False, encoding="utf-8")
    test_data.to_csv(test_data_path, sep=",", index=False, encoding="utf-8")

if __name__ == '__main__':
    args = argparse.ArgumentParser()

    args.add_argument('--config', default='params.yaml')
    parsed_args = args.parse_args()
    split_and_saved_data(config_path=parsed_args.config)



