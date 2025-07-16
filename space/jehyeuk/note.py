import os


for key, attr in os.environ.items():
    print(f'{key}:: {attr}')