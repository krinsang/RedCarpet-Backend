import csv
import os
import sys
import copy

for file in os.listdir(os.getcwd()):
	buff = []
	if file.endswith("list_attr_cloth.txt"):
		with open(file, "r+") as f:
			lines = f.readlines()
			for line in lines:
				line = line.split(' ')
				line = [x for x in line if x != '']
				number = line[-1]
				del line[-1]
				if len(line) > 0:
					line.append('\t')
					length = len(line) - 1
					for i in range(length):
						line.insert(1 + 2*i, ' ')
				line.append(number)
				line = str().join(line)
				buff.append(copy.deepcopy(line))
				# if line is not '\n':
				# 	print(line)					
			# f.writelines(buff)
			f.close()
		with open("list_attr_cloth_mod.txt", "w+") as f:
			print(buff)
			f.writelines(buff)
			f.close()

txt_file = "list_attr_cloth_mod.txt"
csv_file = "list_attr_cloth.csv"

in_txt = csv.reader(open(txt_file, "+r"), delimiter = '\t')
out_csv = csv.writer(open(csv_file, "+w"))

out_csv.writerows(in_txt)