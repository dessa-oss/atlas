#!/usr/bin/env python3

import fileinput
import sys
import re
import os

rootdir = os.getcwd()
extensions = ('.py')

def replaceFile(filename, searchExp, replaceExp):
    with open(filename, 'r') as f:
        content = f.read()
        content_new = re.sub(searchExp, replaceExp, content, 0, re.DOTALL)
    
    with open(filename, "w") as f:
        f.write(content_new)

regex = r'\"\"\"\nCopyright \(C\) DeepLearning Financial.*\d\d\d\d\n\"\"\"\n'

for subdir, dirs, files in os.walk(rootdir):
    # Ignore hidden files and folders
    files = [f for f in files if not f[0] == '.']
    dirs[:] = [d for d in dirs if not d[0] == '.']
    
    for file in files:
        ext = os.path.splitext(file)[-1].lower()
        if ext in extensions:
            replaceFile(os.path.join(subdir, file), regex, '')