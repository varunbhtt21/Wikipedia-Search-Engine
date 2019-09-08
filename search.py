import sys

from functools import reduce
from collections import defaultdict
from nltk.corpus import stopwords
from collections import defaultdict
from nltk.stem import PorterStemmer
from operator import itemgetter
import operator
import os
import re


stop_words = ['all', 'just', "don't", 'being', 'over', 'both', 'through', 'yourselves', 'its', 'before', 'o', 'don', 'hadn', 'herself', 'll', 'had', 'should', 'to', 'only', 'won', 'under', 'ours', 'has', "should've", "haven't", 'do', 'them', 'his', 'very', "you've", 'they', 'not', 'during', 'now', 'him', 'nor', "wasn't", 'd', 'did', 'didn', 'this', 'she', 'each', 'further', "won't", 'where', "mustn't", "isn't", 'few', 'because', "you'd", 'doing', 'some', 'hasn', "hasn't", 'are', 'our', 'ourselves', 'out', 'what', 'for', "needn't", 'below', 're', 'does', "shouldn't", 'above', 'between', 'mustn', 't', 'be', 'we', 'who', "mightn't", "doesn't", 'were', 'here', 'shouldn', 'hers', "aren't", 'by', 'on', 'about', 'couldn', 'of', "wouldn't", 'against', 's', 'isn', 'or', 'own', 'into', 'yourself', 'down', "hadn't", 'mightn', "couldn't", 'wasn', 'your', "you're", 'from', 'her', 'their', 'aren', "it's", 'there', 'been', 'whom', 'too', 'wouldn', 'themselves', 'weren', 'was', 'until', 'more', 'himself', 'that', "didn't", 'but', "that'll", 'with', 'than', 'those', 'he', 'me', 'myself', 'ma', "weren't", 'these', 'up', 'will', 'while', 'ain', 'can', 'theirs', 'my', 'and', 've', 'then', 'is', 'am', 'it', 'doesn', 'an', 'as', 'itself', 'at', 'have', 'in', 'any', 'if', 'again', 'no', 'when', 'same', 'how', 'other', 'which', 'you', "shan't", 'shan', 'needn', 'haven', 'after', 'most', 'such', 'why', 'a', 'off', 'i', 'm', 'yours', "you'll", 'so', 'y', "she's", 'the', 'having', 'once']
Dict_Stop_Words = {}
ps = PorterStemmer()


# def set_list_intersection(set_list):
#     if not set_list:
#         print("haan")
#         return set()
    
#     result = set_list[0]
    
#     for s in set_list[1:]:
#         result &= s
    
#     return result



def field_query(search_query, outputs):

    search_query = search_query.split(" ")

    dict_val = {}
    for value in search_query:
        if "title" in value or "infobox" in value or "body" in value or "category" in value or "ref" in value:
            flag = value.split(":")[0]
            value = value.split(":")[1]

        if flag == "title":
            dict_val[value] = Title_Posting_List[value]

        elif flag == "infobox":
            dict_val[value] = Infobox_Posting_List[value]

        elif flag == "category":
            dict_val[value] = Infobox_Posting_List[value]

        elif flag == "body":
            dict_val[value] = Body_Posting_List[value]

        elif flag == "ref":
            dict_val[value] = Reference_Posting_List[value]


    union_list = []
    for keys, value in dict_val.items():
        union_list.append(set(value))


    # ***********************************RANKING****************************************
    tmp = []
    # Finding Union and appending to list
    for val in reduce(lambda s1, s2: s1 | s2, union_list):
        tmp.append(val)
        

    # Appending the sum of count value to each Doc ID
    Output = {} 
    for x, y in tmp: 
        if x in Output: 
            Output[x].append((y)) 
        else: 
            Output[x] = [(y)] 

    for i in Output:
        Output[i] = sum(Output[i])


    # Sort the Dictionary according to the keys
    sorted_x = sorted(Output.items(), key=operator.itemgetter(1), reverse=True)

    # Selecting Top 25 Values
    count = 0
    tmp_output = []

    for val in sorted_x:
        li = []
        val1 = Index_Title[str(val[0])]
        li.append(val1)

        # Check for no Duplicates
        if li in tmp_output:
            continue

        outputs.append(li)
        tmp_output.append(li)
        count += 1

        if count == 20:
            break

    li = []
    outputs.append(li)

    return outputs

    









#***************************************************************************************

def processing(search_query, outputs):

    if ":" in search_query:
        field_query(search_query, outputs)
        return 

    filter_query = []
    Dict_query = defaultdict(list)

    global Dict_Stop_Words
    search_query = search_query.split(" ")
    
    for word in search_query:
        word = word.strip()
        val = ps.stem(word)

        try:
            if Dict_Stop_Words[val] == 1:
                continue
        except:
            filter_query.append(word.lower())



    for word in filter_query:
        try:
            if Infobox_Posting_List[word]:
                # for val in Infobox_Posting_List[word]:
                Dict_query[word].append(Infobox_Posting_List[word])

        except:
            pass

        try:
            if Body_Posting_List[word]:
                # for val in Body_Posting_List[word]:
                Dict_query[word].append(Body_Posting_List[word])

        except:
            pass

        try:
            if Links_Posting_List[word]:
                # for val in Body_Posting_List[word]:
                Dict_query[word].append(Links_Posting_List[word])

        except:
            pass


        try:
            if Title_Posting_List[word]:
                # for val in Body_Posting_List[word]:
                Dict_query[word].append(Title_Posting_List[word])

        except:
            pass


        try:
            if Category_Posting_List[word]:
                # for val in Body_Posting_List[word]:
                Dict_query[word].append(Category_Posting_List[word])

        except:
            pass


        # try:
        #     if Reference_Posting_List[word]:
        #         # for val in Body_Posting_List[word]:
        #         Dict_query[word].append(Reference_Posting_List[word])

        # except:
        #     pass



    for key in filter_query:
        try:
            find_inter.append(sorted(Dict_query[key], key=itemgetter(0)))
        except:
            pass

        
    # Forming Dictionary of set for words
    Dict_for_intersect = {}
    for word in filter_query:
        temp_set = set()
        for wor in Dict_query[word]:
            for w in wor:
                temp_set.add((w[0],w[1]))
        
            Dict_for_intersect[word] = set(temp_set)



    # Forming Intersection List
    Intersect_List = []
    for word in filter_query:
        Intersect_List.append(Dict_for_intersect[word])


    #set_list_intersection(Intersect_List)
    # print(reduce(lambda s1, s2: s1 & s2, Intersect_List))


    
    tmp = []
    # Finding Union and appending to list
    for val in reduce(lambda s1, s2: s1 | s2, Intersect_List):
        tmp.append(val)
        

    # Appending the sum of count value to each Doc ID
    Output = {} 
    for x, y in tmp: 
        if x in Output: 
            Output[x].append((y)) 
        else: 
            Output[x] = [(y)] 

    for i in Output:
        Output[i] = sum(Output[i])


    # Sort the Dictionary according to the keys
    sorted_x = sorted(Output.items(), key=operator.itemgetter(1), reverse=True)

    # Selecting Top 25 Values
    count = 0
    tmp_output = []
    for val in sorted_x:
        li = []
        val1 = Index_Title[str(val[0])]
        li.append(val1)

        # Check For No Duplicates
        if li in tmp_output:
            continue

        outputs.append(li)
        tmp_output.append(li)
        count += 1

        if count == 20:
            break


    li = []
    outputs.append(li)



    





#*************************************************************************************************************************************************************



Infobox_Posting_List = defaultdict(list)
Category_Posting_List = defaultdict(list)
Body_Posting_List = defaultdict(list)
Links_Posting_List = defaultdict(list)
Title_Posting_List = defaultdict(list)
Reference_Posting_List = defaultdict(list)


def Loading_Data(Posting_List, catg):

    f=open(catg, "r")
    content = f.read()
    content = content.split("\n")
    count = 0

    for i in content:
        if not i:
            continue

        key = i.split(":")[0].strip()
        value = i.split(":")[1]
        
        value = value.replace("[", " ")
        value = value.replace("]"," ").split(",")

        for i in value:
            val = i.strip().split()
            if val:
                try:
                    Posting_List[key].append((int(val[0]), int(val[1])))
                except:
                    pass




Index_Title = {}
def Loading_Index(Index_Title, catg):

    f=open(catg, "r")
    content = f.read()
    content = content.split("\n")
    count = 0

    for i in content:
        if not i:
            continue

        key = i.split(":")[0].strip()
        value = i.split(":")[1]

        Index_Title[key] = value
        







def read_file(testfile):
    with open(testfile, 'r') as file:
        queries = file.readlines()
    return queries


def write_file(outputs, path_to_output):
    '''outputs should be a list of lists.
        len(outputs) = number of queries
        Each element in outputs should be a list of titles corresponding to a particular query.'''
    
    

    with open(path_to_output, 'w') as file:
        for output in outputs:

            if not output:
                file.write('\n')
            for line in output:
                file.write(line.strip())
            file.write('\n')



def search(path_to_index, queries):
    '''Write your code here'''

    global Dict_Stop_Words
    for key in stop_words:
        Dict_Stop_Words[key] = 1


    print("\nProcessing...\n")
    
    global Infobox_Posting_List
    global Title_Posting_List
    global Links_Posting_List
    global Category_Posting_List
    global Body_Posting_List
    global Reference_Posting_List
    global Index_Title

    Loading_Data(Infobox_Posting_List, os.path.join(path_to_index, "Infobox.txt"))
    Loading_Data(Title_Posting_List, os.path.join(path_to_index, "Title.txt"))
    Loading_Data(Links_Posting_List, os.path.join(path_to_index, "Links.txt"))
    Loading_Data(Category_Posting_List, os.path.join(path_to_index, "Category.txt"))
    Loading_Data(Body_Posting_List, os.path.join(path_to_index, "Body.txt"))
    Loading_Index(Reference_Posting_List, os.path.join(path_to_index, "Reference.txt"))
    Loading_Index(Index_Title, os.path.join(path_to_index, "Index_Title.txt"))

    outputs = []

    #search_query = "title:gandhi body:arjun infobox:gandhi category:gandhi"
    #processing(search_query)
    for search_query in queries:
        processing(search_query, outputs)

    return outputs






def main():
    path_to_index = sys.argv[1]
    testfile = sys.argv[2]
    path_to_output = sys.argv[3]

    queries = read_file(testfile)
    outputs = search(path_to_index, queries)
    write_file(outputs, path_to_output)
    print("Done")


if __name__ == '__main__':
    main()


