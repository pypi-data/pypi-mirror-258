import yaml

def load(specs_path):
    with open(specs_path, 'r') as file:
        specs = yaml.safe_load(file)
    return specs['datasets']
