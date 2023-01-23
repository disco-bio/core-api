import json
import pprint

INPUT_FILEPATH = "static/data/v1/mim2gene.txt"
OUTPUT_FILEPATH = "output.json"


file = open(INPUT_FILEPATH)

file_lines = file.readlines()

return_dict = {}

print(len(file_lines))
for i in range(len(file_lines)):
    curr_line_list = file_lines[i].split("\t")
    if len(curr_line_list)>2 and curr_line_list[1] in ["gene", "gene/phenotype"]:
        return_dict[curr_line_list[2]] = curr_line_list[3]


with open(OUTPUT_FILEPATH, 'w') as outputfile:
    json.dump(return_dict, outputfile)
