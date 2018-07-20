import json
import os
from os.path import isfile
from os.path import join
import re

notebook_path = os.path.abspath("notebooks")
notebook_dir = os.listdir("notebooks")

filenames = [name for name in notebook_dir if re.match("^.*py$", name)]

for name in filenames:
    file_path = join(notebook_path, name)

    out_filepath = join(notebook_path, name[:-2] + "ipynb")

    out_file = open(test_filepath, "w")

    file_data = open(file_path, "r").read().split("\n")

    last_cell = 0

    cells = []
    cell_code = []
    curr_code = False

    for n in range(len(file_data)):
        if file_data[n] == "# Begin Markdown":
            if n!=0:
                cells += [file_data[last_cell + 1 : n-1]]
                cell_code += [curr_code]
            last_cell = n
            curr_code = False

        elif file_data[n] == "# Begin Code":
            if n!=0:
                cells += [file_data[last_cell + 1 : n-1]]
                cell_code += [curr_code]
            last_cell = n
            curr_code = True

    cells += [file_data[last_cell+1 : len(file_data)-1]]
    cell_code += [curr_code]

    out_cells = []

    for i in range(len(cells)):
        new_cell = dict()
        source = []
        raw_source = cells[i]

        if cell_code[i]:
            new_cell["cell_type"] = "code"
            new_cell["execution_count"] = None
            new_cell["outputs"] = []
        else:
            new_cell["cell_type"] = "markdown"

        new_cell["metadata"] = dict()

        for line in raw_source:

            if cell_code[i]:
                source += [line + "\n"]
            else:
                source += [line[2:] + "\n"]

        if source == []:
            continue

        source[-1] = source[-1][:-1]

        new_cell["source"] = source



        out_cells += [new_cell]


    kernelspec = dict()
    kernelspec["display_name"] = "Python Leabra7"
    kernelspec["language"] = "python"
    kernelspec["name"] = "leabra7"

    codemirror_mode = dict()
    codemirror_mode["name"] = "ipython"
    codemirror_mode["version"] = 3

    language_info = dict()
    language_info["codemirror_mode"] = codemirror_mode
    language_info["file_extension"] = ".py"
    language_info["mimetype"] = "text/x-python"
    language_info["name"] = "python"
    language_info["nbconvert_exporter"] = "python"
    language_info["pygments_lexer"] = "ipython3"
    language_info["version"] = "3.6.6"

    metadata = dict()
    metadata["kernelspec"] = kernelspec
    metadata["language_info"] = language_info

    out_data = dict()
    out_data["cells"] = out_cells
    out_data["metadata"] = metadata
    out_data["nbformat"] = 4
    out_data["nbformat_minor"] = 2

    json.dump(out_data, out_file, sort_keys = True, indent = 2)
