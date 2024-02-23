import os
import sys

lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'lib'))
sys.path.insert(0, lib_path)

import pandas as pd
from clause import Learner, Options

def train(dataset_paths):
    all_rules = []  # This will store all the rules from every dataset
    
    for dataset in dataset_paths:
        options = Options()
        options.set("learner.mode", "amie")

        # Extract the dataset path from the dictionary
        dataset_path = dataset["path"]
        
        # Define the path for the output rules file
        path_rules_output = dataset_path.replace("train.txt", "learned_rules.txt")
        
        # Setup and run the learner
        learner = Learner(options=options.get("learner"))
        learner.learn_rules(path_data=dataset_path, path_output=path_rules_output)
        
        # Load the output file and append its rules to the all_rules list
        df = pd.read_csv(path_rules_output, sep='\t', header=None, names=['Support', 'BodySize', 'Confidence', 'Rule'])
        all_rules.extend(df['Rule'].tolist())
    
    return all_rules
