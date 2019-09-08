from heapq import merge 
import itertools
from itertools import zip_longest
import heapq



def merge_files(final_index, no_of_files):

    print("Running...")

    k = no_of_files + 1
    run = 3
    first = 1

    heap = []
    disc_empty = []
    data_list = []

    f1 = open("Final.txt", 'w')

    while run != 1:

        file_names = []
        k = no_of_files

        for i in range(1, k):
            file_names.append("Data/Body/file"+str(i)+".txt")
            
        files = [open(i, "r") for i in file_names]

        for i, val in enumerate(files):
            val = val.readline().split(":")
            heapq.heappush(heap, (val[0], val[1], i))

        count = 0
       
        while heap:
            elem = heapq.heappop(heap)

            file_no = elem[2]
            val = files[file_no].readline().split(":")

            if not val[0]:
                # disc_empty.append(file_no)
                continue

            heapq.heappush(heap, (val[0], val[1], file_no))

            f1.write(elem[0]+":"+elem[1])


        run = 1
        f1.close()









    
        

    







merge_files("",29)
print("Done")

