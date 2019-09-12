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

    while run != 1:

        file_names = []

        for i in range(1, k):
            file_names.append("Infobox/file"+str(i)+".txt")
            
        files = [open(i, "r") for i in file_names]

        for i, val in enumerate(files):
            val = val.readline().split("~")
            heapq.heappush(heap, (val[0], val[1], i))

        count = 0
        file_count = 0
        flag = 0
       
        while heap:

            flag = 0
            count += 1

            elem = heapq.heappop(heap)

            file_no = elem[2]
            val = files[file_no].readline().split("~")

            if not val[0]:
                # disc_empty.append(file_no)
                continue



            heapq.heappush(heap, (val[0], val[1], file_no))
            Data_List[elem[0]].append(elem[1])

            if count == 50000:
                flag = 1

                file_count += 1
                print("File : ",file_count)

                f2 = open("Final_Index/Infobox_Final_Index/Infobox_Index_"+str(file_count)+".txt", 'w')

                for key, value in Data_List.items():
                    f2.write(key+"~")

                    for val in value :
                        f2.write(str(val).rstrip("\n"))

                    f2.write("\n")

                count = 0
                Data_List.clear()

                Secondary_Index[key] = file_count
                f2.close()

        run = 1

        if flag == 0:
            file_count += 1
            print("Last File : ",file_count)
            f2 = open("Final_Index/Infobox_Final_Index/Infobox_Index_"+str(file_count)+".txt", 'w')
            for key, value in Data_List.items():
                f2.write(key+"~")
                
                for val in value :
                    f2.write(str(val).rstrip("\n"))

                f2.write("\n")

            Secondary_Index[key] = file_count
            f2.close()
    










merge_files("",979)
print("Done")
# print(Secondary_Index)
with open('Final_Index/Infobox_Final_Index/Infobox_Secondary_Index.pickle', 'wb') as handle:
    pickle.dump(Secondary_Index, handle, protocol=pickle.HIGHEST_PROTOCOL)

print("Dumping Done")

# data = {}
# with open('Secondary_Index.pickle', 'rb') as handle:
#     data = pickle.load(handle)
# print(" yo ",data)


