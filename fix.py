from heapq import merge 
import itertools
from itertools import zip_longest
import heapq
from collections import defaultdict
import pickle


Secondary_Index = {}
def merge_files(final_index, no_of_files):

    print("Running...")

    k = no_of_files + 1
    run = 3

    heap = []
    disc_empty = []
    Data_List = defaultdict(list)

    global Secondary_Index

    last_line = []
    file_count = 0
    while run != 1:

        file_names = []

        for i in range(1, k):
            file_names.append("Infobox_Final_Index/Infobox_Index_"+str(i)+".txt")
            
        # files = [open(i, "r") for i in file_names]

        for i in file_names:
            file_count += 1
            print(file_count)
            fp = open(i, "r")
            lines = fp.read().splitlines()
            last_line = lines[-1].split("~")[0]

            Secondary_Index[last_line] = file_count

            fp.close()


        # for i, val in enumerate(files):
        #     file_count += 1
        #     print(file_count)
        #     #val = val.readline().split("~")
        #     lines = val.read().splitlines()
        #     last_line = lines[-1].split("~")[0]

        #     Secondary_Index[last_line] = file_count


        run=1

      
      










merge_files("",1362)
print("Done")
# print(Secondary_Index)
with open('Infobox_Final_Index/Infobox_Secondary_Index.pickle', 'wb') as handle:
    pickle.dump(Secondary_Index, handle, protocol=pickle.HIGHEST_PROTOCOL)

print("Dumping Done")

# data = {}
# with open('Secondary_Index.pickle', 'rb') as handle:
#     data = pickle.load(handle)
# print(" yo ",data)


