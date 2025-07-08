import sys, os
import numpy as np

def readFiles(paths : list[str]):
    contents = []
    for filepath in paths:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            contents.append(f.read())
    return contents

def writeFiles(paths : list[str], contents):
    for path, content in zip(paths, contents):
        with open(path, 'w', encoding='utf-8', errors='ignore') as f:
            f.write(str(content)[1:-1])


def nvidiaData(contents: list[str]):
    for i, data in enumerate(contents):
        lines = data.strip().splitlines()[1:]
        results = [
            float(line.split(",")[1]) - float(line.split(",")[4])
            for line in lines
        ]
        contents[i] = results




if __name__ == "__main__":
    full_paths = [os.path.join(sys.argv[1], filename) for filename in os.listdir(sys.argv[1])]
    full_paths = [path for path in full_paths if os.path.isfile(path)]

    match int(sys.argv[2]):
        case 0:
            contents = readFiles(full_paths)
            nvidiaData(contents)
            writeFiles(full_paths, contents)
        case 1:
            pass
        case 2:
            pass
        case 3:
            pass