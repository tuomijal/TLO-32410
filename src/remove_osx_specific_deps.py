'''
To make Binder work by default some OSX specific dependencies must be removed
from environment.yml. This script takes care of that by following instructions
provided here: https://github.com/binder-examples/conda
'''

from pyprojroot import here
import os

to_remove = ['libcxxabi', 'appnope', 'libgfortran', 'libcxx']
old_path = here() / "environment.yml"
new_path = here() / 'temp_env.yml'
with open(old_path, "r") as old_f, open(new_path, 'w') as new_f:
     for line in old_f:
        if not any(bad_word in line for bad_word in to_remove):
            new_f.write(line)

os.remove(path)
os.rename(new_path, old_path)
