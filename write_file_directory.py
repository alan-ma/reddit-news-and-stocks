# write file directory for front end use

from os import listdir

with open("visualization/fileDirectory.js", 'w') as output:
  file_directory = [ file.strip(".json") for file in sorted(listdir("new_parsed_dates"), reverse=True)]
  output.write("var fileDirectory = ")
  output.write(str(file_directory))
  output.write(";\n")

print("done")
