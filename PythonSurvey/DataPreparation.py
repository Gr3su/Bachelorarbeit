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

def nvidiaData(contents: list[str], full_paths : list[str]):
    data = contents[0]
    lines = data.strip().splitlines()[1:]
    results = [
        float(line.split(",")[1]) - float(line.split(",")[4])
        for line in lines
    ]
    contents[:] = [str(results[max(i-50, 0):i])[1:-1] for i in range(len(results), 0, -50)]

    if contents[-1].count(",") < 49:
        contents.pop()
    contents.reverse()

    dirName = os.path.dirname(full_paths[0])
    full_paths.clear()
    for i in range(1,len(contents) + 1):
        full_paths.append(os.path.join(dirName, str(i * 50)))


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
        if len(temps) < 1000:
            continue
        
        temps = temps[-1000:]
        valid_contents.append(", ".join(temps))
        valid_paths.append(path)

    contents[:] = valid_contents
    full_paths[:] = valid_paths

def ecg500(contents: list[str], full_paths: list[str]):
    data = [float(x) for x in contents[0].split()]
    data = [str(data[i:i+140 if i <= len(data) else len(data)])[1:-1] for i in range(0, len(data), 140)]
    if len(data[-1]) != 140:
        data.pop()

    contents[:] = data
    
    dirName = os.path.dirname(full_paths[0])
    full_paths.clear()
    for i in range(1,len(contents) + 1):
        full_paths.append(os.path.join(dirName, str(i * 140)))
    

if __name__ == "__main__":
    full_paths = [os.path.join(sys.argv[1], filename) for filename in os.listdir(sys.argv[1])]
    full_paths = [path for path in full_paths if os.path.isfile(path)]

    contents = readFiles(full_paths)
    match int(sys.argv[2]):
        case 0:
            nvidiaData(contents, full_paths)
        case 1:
            euWeatherData(contents, full_paths)
        case 2:
            ecg500(contents, full_paths)
    writeFiles(full_paths, contents)