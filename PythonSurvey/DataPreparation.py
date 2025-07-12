import sys, os
import numpy as np

def readFiles(paths : list[str]):
    contents = []
    for filepath in paths:
        with open(filepath, 'r', encoding='utf-8') as f:
            contents.append(f.read())
    return contents

def writeFiles(paths : list[str], contents):
    for path, content in zip(paths, contents):
        newFileName = os.path.splitext(os.path.basename(path))[0] + ".csv"
        newPath = os.path.join(os.path.dirname(path), "../prepared", newFileName)

        os.makedirs(os.path.dirname(newPath), exist_ok=True)
        with open(newPath, 'w', encoding='utf-8') as f:
            f.write(str(content))

def nvidiaData(contents: list[str]):
    for i, data in enumerate(contents):
        lines = data.strip().splitlines()[1:]
        results = [
            float(line.split(",")[1]) - float(line.split(",")[4])
            for line in lines
        ]
        contents[i] = str(results)[1:-1]

def euWeatherData(contents: list[str], full_paths: list[str]):
    valid_contents = []
    valid_paths = []

    for data, path in zip(contents, full_paths):
        lines = data.strip().splitlines()
        temp_idx = qual_idx = None

        for i, line in enumerate(lines):
            if "TG   : Mean temperature in" in line:
                start, end = map(int, line.split()[0].split("-"))
                temp_idx = (start, end)
            elif "Q_TG : quality code for TG" in line:
                start, end = map(int, line.split()[0].split("-"))
                qual_idx = (start, end)
            elif line.startswith("STAID"):
                lines = lines[i+1:]
                break

        if temp_idx is None or qual_idx is None:
            continue

        if any(int(line[qual_idx[0]:qual_idx[1]]) != 0 for line in lines):
            continue

        temps = [line[temp_idx[0]:temp_idx[1]].strip() for line in lines]
        valid_contents.append(", ".join(temps))
        valid_paths.append(path)

    contents[:] = valid_contents
    full_paths[:] = valid_paths


if __name__ == "__main__":
    full_paths = [os.path.join(sys.argv[1], filename) for filename in os.listdir(sys.argv[1])]
    full_paths = [path for path in full_paths if os.path.isfile(path)]

    match int(sys.argv[2]):
        case 0:
            contents = readFiles(full_paths)
            nvidiaData(contents)
            writeFiles(full_paths, contents)
        case 1:
            contents = readFiles(full_paths)
            euWeatherData(contents, full_paths)
            writeFiles(full_paths, contents)
        case 2:
            pass
        case 3:
            pass