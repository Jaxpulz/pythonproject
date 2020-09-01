import yaml

with open('directors.yaml') as directors_file:
    directors = yaml.safe_load(directors_file)

print(directors)