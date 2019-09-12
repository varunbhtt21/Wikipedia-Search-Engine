import sys

from functools import reduce
from collections import defaultdict
from nltk.corpus import stopwords
from collections import defaultdict
from nltk.stem import PorterStemmer
from operator import itemgetter
import operator
import Stemmer
import os
import re
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import pairwise_kernels
import math
from functools import reduce
import timeit


# For Secondary Index File
Secondary_Body = {}
Secondary_Infobox = {}
Secondary_Links = {}
Secondary_Category = {}
Secondary_Title = {}
Secondary_Reference = {}


stop_words = ['all', 'just', "don't", 'being', 'over', 'both', 'through', 'yourselves', 'its', 'before', 'o', 'don', 'hadn', 'herself', 'll', 'had', 'should', 'to', 'only', 'won', 'under', 'ours', 'has', "should've", "haven't", 'do', 'them', 'his', 'very', "you've", 'they', 'not', 'during', 'now', 'him', 'nor', "wasn't", 'd', 'did', 'didn', 'this', 'she', 'each', 'further', "won't", 'where', "mustn't", "isn't", 'few', 'because', "you'd", 'doing', 'some', 'hasn', "hasn't", 'are', 'our', 'ourselves', 'out', 'what', 'for', "needn't", 'below', 're', 'does', "shouldn't", 'above', 'between', 'mustn', 't', 'be', 'we', 'who', "mightn't", "doesn't", 'were', 'here', 'shouldn', 'hers', "aren't", 'by', 'on', 'about', 'couldn', 'of', "wouldn't", 'against', 's', 'isn', 'or', 'own', 'into', 'yourself', 'down', "hadn't", 'mightn', "couldn't", 'wasn', 'your', "you're", 'from', 'her', 'their', 'aren', "it's", 'there', 'been', 'whom', 'too', 'wouldn', 'themselves', 'weren', 'was', 'until', 'more', 'himself', 'that', "didn't", 'but', "that'll", 'with', 'than', 'those', 'he', 'me', 'myself', 'ma', "weren't", 'these', 'up', 'will', 'while', 'ain', 'can', 'theirs', 'my', 'and', 've', 'then', 'is', 'am', 'it', 'doesn', 'an', 'as', 'itself', 'at', 'have', 'in', 'any', 'if', 'again', 'no', 'when', 'same', 'how', 'other', 'which', 'you', "shan't", 'shan', 'needn', 'haven', 'after', 'most', 'such', 'why', 'a', 'off', 'i', 'm', 'yours', "you'll", 'so', 'y', "she's", 'the', 'having', 'once']
Dict_Stop_Words = {}
ps = Stemmer.Stemmer('english')


# def set_list_intersection(set_list):
#     if not set_list:
#         print("haan")
#         return set()
    
#     result = set_list[0]
    
#     for s in set_list[1:]:
#         result &= s
    
#     return result



def field_query(search_query, outputs, path_to_index):

    start=timeit.default_timer()

    global Secondary_Body
    global Secondary_Infobox
    global Secondary_Links
    global Secondary_Title
    global Secondary_Reference
    global Secondary_Category

    Index_Title = {}


    search_query = search_query.split(" ")

    dict_val = {}
    search_quer = ""

    for value in search_query:
        if "title" in value or "infobox" in value or "body" in value or "category" in value or "ref" in value:
            flag = value.split(":")[0]
            value = value.split(":")[1]

            search_quer = search_quer + str(value) + " "

        if flag == "title":
            file_no = get_file_no(value, Secondary_Title)
            Loading_Data(value, Title_Posting_List, os.path.join(path_to_index, "Title_Final_Index/Title_Index_"+str(file_no)+".txt"))
            if Title_Posting_List[value]:
                dict_val[value] = Title_Posting_List[value]
            

        elif flag == "infobox":
            file_no = get_file_no(value, Secondary_Infobox)
            Loading_Data(value, Infobox_Posting_List, os.path.join(path_to_index, "Infobox_Final_Index/Infobox_Index_"+str(file_no)+".txt"))
            if Infobox_Posting_List[value]:
                dict_val[value] = Infobox_Posting_List[value]

        elif flag == "category":
            file_no = get_file_no(value, Secondary_Category)
            #print(file_no)
            Loading_Data(value, Category_Posting_List, os.path.join(path_to_index, "Category_Final_Index/Category_Index_"+str(file_no)+".txt"))
            if Category_Posting_List[value]:
                dict_val[value] = Category_Posting_List[value]

        elif flag == "body":
            file_no = get_file_no(value, Secondary_Body)
            #print("B",file_no)
            Loading_Data(value, Body_Posting_List, os.path.join(path_to_index, "Body_Final_Index/Body_Index_"+str(file_no)+".txt"))
            if Body_Posting_List[value]:
                dict_val[value] = Body_Posting_List[value]

        elif flag == "ref":
            file_no = get_file_no(value, Secondary_Reference)
            Loading_Data(value, Reference_Posting_List, os.path.join(path_to_index, "Reference_Final_Index/Reference_Index_"+str(file_no)+".txt"))
            if Reference_Posting_List[value]:
                dict_val[value] = Reference_Posting_List[value]


    union_list = []
    for keys, value in dict_val.items():
        union_list.append(set(value))

    if not union_list:
        print("Empty Information \n")
        return


    # ***********************************RANKING****************************************
    tmp = []
    # Finding Union and appending to list
    for val in reduce(lambda s1, s2: s1 & s2, union_list):
        tmp.append(val)

    if not tmp:
        for val in reduce(lambda s1, s2: s1 | s2, union_list):
            tmp.append(val)

    if not tmp:
        print("\n No Related Information Present \n")
        return
        

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

    temp = []
    for val in sorted_x:

        Loading_Index(Index_Title, val[0], os.path.join(path_to_index, "title/file"))

        li = []
        val1 = Index_Title[str(val[0])]
        li.append(val1)

        temp.append(val1.lower())

        # Check For No Duplicates
        if li in tmp_output:
            continue

        # outputs.append(li)
        tmp_output.append(li)
        count += 1

        if count == 200:
            break


    stop=timeit.default_timer()
    

    # APPLYING COSINE SIMILARITY

    v = []
    v.append(search_quer)

    # Scikit Learn
    from sklearn.feature_extraction.text import CountVectorizer
    import pandas as pd

    # Create the Document Term Matrix
    count_vectorizer = CountVectorizer(stop_words='english')
    count_vectorizer = CountVectorizer()
    sparse_matrix = count_vectorizer.fit_transform(temp)

    # OPTIONAL: Convert Sparse Matrix to Pandas Dataframe if you want to see the word frequencies.
    doc_term_matrix = sparse_matrix.todense()
    df = pd.DataFrame(doc_term_matrix, 
                      columns=count_vectorizer.get_feature_names(), 
                      index=temp)



    sparse_matrix1 = count_vectorizer.transform(v)
    doc_term_matrix1 = sparse_matrix1.todense()


    df1 = pd.DataFrame(doc_term_matrix1, 
                      columns=count_vectorizer.get_feature_names(), 
                      index=v)

    from sklearn.metrics.pairwise import cosine_similarity    
    cosine_values = cosine_similarity(df1, df)

    
    # Pairing title with the cosine values
    Pair_Title_Cosine_Value = []

    for cos_list in cosine_values:
        temp_list = []
        for value1, value2 in zip(cos_list, temp):
            temp_list.append((value1,value2))
        Pair_Title_Cosine_Value.append(temp_list)

    for val in range(0, len(Pair_Title_Cosine_Value)):
        Pair_Title_Cosine_Value[val] = sorted(Pair_Title_Cosine_Value[val], reverse=True, key=operator.itemgetter(0))
    
    Pair_Title_Cosine_Value = reduce(lambda x,y :x+y ,Pair_Title_Cosine_Value)


    count = 0
    for val in Pair_Title_Cosine_Value:
        count += 1
        li = []
        li.append(val[1])
        outputs.append(li)

        if count == 20:
            break

    print("\n\nTime Taken ",stop-start)
    print("------------------------------")

    count = 0
    for val in outputs:
        count += 1
        print(str(count)+" "+val[0])

    print("\n")
    print("*********************************************************************************************************************************")

    print("\n")
    li = []
    outputs.append(li)


def get_file_no(search_query, Secondary):

    for key, value in Secondary.items():
        if search_query <= key:
            file_no = Secondary[key]
            return file_no





#***************************************************************************************

def processing(search_quer, outputs, path_to_index):

    Index_Title = {}

    global Secondary_Body
    global Secondary_Infobox
    global Secondary_Links
    global Secondary_Title
    global Secondary_Reference
    global Secondary_Category




    if ":" in search_quer:
        field_query(search_quer, outputs, path_to_index)
        return 

    # TIMER STARTS
    start=timeit.default_timer()

    filter_query = []
    Dict_query = defaultdict(list)

    global Dict_Stop_Words
    search_query = search_quer.split(" ")
    
    for word in search_query:
        word = word.strip()
        #val = ps.stem(word)

        try:
            if Dict_Stop_Words[val] == 1:
                continue
        except:
            filter_query.append(word.lower())


 
    for word in filter_query:

        try:
            file_no = get_file_no(word, Secondary_Infobox)
            #print(file_no)
            Loading_Data(word, Infobox_Posting_List, os.path.join(path_to_index, "Infobox_Final_Index/Infobox_Index_"+str(file_no)+".txt"))
            if Infobox_Posting_List[word]:
                #print("I")
                Dict_query[word].append(Infobox_Posting_List[word])

        except:
            pass

       

        try:
            file_no = get_file_no(word, Secondary_Body)
            #print("B",file_no)
            Loading_Data(word, Body_Posting_List, os.path.join(path_to_index, "Body_Final_Index/Body_Index_"+str(file_no)+".txt"))
            if Body_Posting_List[word]:
                #print("B")
                Dict_query[word].append(Body_Posting_List[word])
            Body_Posting_List.clear()

        except:
            pass

        try:
            file_no = get_file_no(word, Secondary_Links)
            #print(file_no)
            Loading_Data(word, Links_Posting_List, os.path.join(path_to_index, "Links_Final_Index/Links_Index_"+str(file_no)+".txt"))
            if Links_Posting_List[word]:
                #print("L")
                Dict_query[word].append(Links_Posting_List[word])
            Links_Posting_List.clear()

        except:
            pass


        try:
            file_no = get_file_no(word, Secondary_Title)
            Loading_Data(word, Title_Posting_List, os.path.join(path_to_index, "Title_Final_Index/Title_Index_"+str(file_no)+".txt"))
            if Title_Posting_List[word]:
                #print("T")
                Dict_query[word].append(Title_Posting_List[word])
            Title_Posting_List.clear()

        except:
            pass


        try:
            file_no = get_file_no(word, Secondary_Category)
            #print(file_no)
            Loading_Data(word, Category_Posting_List, os.path.join(path_to_index, "Category_Final_Index/Category_Index_"+str(file_no)+".txt"))
            if Category_Posting_List[word]:
                #print("C")
                Dict_query[word].append(Category_Posting_List[word])
            Category_Posting_List.clear()

        except:
            pass


        try:
            file_no = get_file_no(word, Secondary_Reference)
            #print(file_no)
            Loading_Data(word, Reference_Posting_List, os.path.join(path_to_index, "Reference_Final_Index/Reference_Index_"+str(file_no)+".txt"))
            if Reference_Posting_List[word]:
                #print("R")
                Dict_query[word].append(Reference_Posting_List[word])
            Reference_Posting_List.clear()

        except:
            pass



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
        try:
            Intersect_List.append(Dict_for_intersect[word])
        except:
            print(word,"not found in Database !!!\n")
    
    if not Intersect_List:
        return


    #set_list_intersection(Intersect_List)
    # print(reduce(lambda s1, s2: s1 & s2, Intersect_List))


    
    tmp = []
    # Finding Union and appending to list
    for val in reduce(lambda s1, s2: s1 & s2, Intersect_List):
        tmp.append(val)

    if not tmp:
        for val in reduce(lambda s1, s2: s1 | s2, Intersect_List):
            tmp.append(val)
    
    if not tmp:
        print("\n No Related Information Present \n")
        return

    # Appending the sum of count value to each Doc ID
    Output = {} 
    for x, y in tmp: 
        if x in Output: 
            Output[x].append((y)) 
        else: 
            Output[x] = [(y)] 


    for i in Output:
        val = math.log(19567269/len(Output[i]))
        Output[i] = sum(Output[i])*val


    # Sort the Dictionary according to the keys
    sorted_x = sorted(Output.items(), key=operator.itemgetter(1), reverse=True)
    
    # Selecting Top 25 Values
    count = 0

    tmp_output = []
    temp = []
    for val in sorted_x:

        Loading_Index(Index_Title, val[0], os.path.join(path_to_index, "title/file"))

        li = []
        val1 = Index_Title[str(val[0])]
        li.append(val1)

        temp.append(val1.lower())

        # Check For No Duplicates
        if li in tmp_output:
            continue

        # outputs.append(li)
        tmp_output.append(li)
        count += 1

        if count == 200:
            break


    # TIMER STOPS
    stop=timeit.default_timer()

    # APPLYING COSINE SIMILARITY
    v = []
    v.append(search_quer)

    # Scikit Learn
    from sklearn.feature_extraction.text import CountVectorizer
    import pandas as pd

    # Create the Document Term Matrix
    count_vectorizer = CountVectorizer(stop_words='english')
    count_vectorizer = CountVectorizer()
    sparse_matrix = count_vectorizer.fit_transform(temp)

    # OPTIONAL: Convert Sparse Matrix to Pandas Dataframe if you want to see the word frequencies.
    doc_term_matrix = sparse_matrix.todense()
    df = pd.DataFrame(doc_term_matrix, 
                      columns=count_vectorizer.get_feature_names(), 
                      index=temp)



    sparse_matrix1 = count_vectorizer.transform(v)
    doc_term_matrix1 = sparse_matrix1.todense()


    df1 = pd.DataFrame(doc_term_matrix1, 
                      columns=count_vectorizer.get_feature_names(), 
                      index=v)

    from sklearn.metrics.pairwise import cosine_similarity    
    cosine_values = cosine_similarity(df1, df)

    
    # Pairing title with the cosine values
    Pair_Title_Cosine_Value = []

    for cos_list in cosine_values:
        temp_list = []
        for value1, value2 in zip(cos_list, temp):
            temp_list.append((value1,value2))
        Pair_Title_Cosine_Value.append(temp_list)

    for val in range(0, len(Pair_Title_Cosine_Value)):
        Pair_Title_Cosine_Value[val] = sorted(Pair_Title_Cosine_Value[val], reverse=True, key=operator.itemgetter(0))
    

    Pair_Title_Cosine_Value = reduce(lambda x,y :x+y ,Pair_Title_Cosine_Value)


    count = 0
    for val in Pair_Title_Cosine_Value:
        count += 1
        li = []
        li.append(val[1])
        outputs.append(li)

        if count == 20:
            break

    print("\n\nTime Taken ",stop-start)
    print("------------------------------")

    count = 0
    for val in outputs:
        count += 1
        print(str(count)+" "+val[0])

    print("\n")
    print("*********************************************************************************************************************************")


    print("\n")
    li = []
    outputs.append(li)


#*************************************************************************************************************************************************************



Infobox_Posting_List = defaultdict(list)
Category_Posting_List = defaultdict(list)
Body_Posting_List = defaultdict(list)
Links_Posting_List = defaultdict(list)
Title_Posting_List = defaultdict(list)
Reference_Posting_List = defaultdict(list)


def Loading_Data(word, Posting_List, catg):

    if Posting_List:
        Posting_List.clear()

    f=open(catg, "r")
    content = f.readlines()
    # content = content.split("\n")
    count = 0

    for i in content:
        if not i:
            continue

        key = i.split("~")[0].strip()
        value = i.split("~")[1]

        if key != word:
            continue
        
        value = value.replace("[", " ")
        value = value.replace("]"," ").split(",")

        for i in value:
            val = i.strip().split()
            if val:
                try:
                    Posting_List[key].append((int(val[0]), int(val[1])))
                except:
                    pass






def Loading_Index(Index_Title, val, catg):

    Secondary_Title = {}

    if Index_Title:
        Index_Title.clear()

    with open('Final_Index/title/Index_Title_Secondary_Index.pickle', 'rb') as handle:
        Secondary_Title = pickle.load(handle)

    for key, value in Secondary_Title.items():
        if int(val) <= int(key):
            file_no = Secondary_Title[key]
            break


    f=open(catg+str(file_no)+".txt", "r")
    content = f.read()
    content = content.split("\n")
    count = 0

    for i in content:
        if not i:
            continue

        key = i.split("~")[0].strip()
        value = i.split("~")[1]

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

    global Secondary_Body
    global Secondary_Infobox
    global Secondary_Links
    global Secondary_Category
    global Secondary_Title
    global Secondary_Reference

    with open('Final_Index/Body_Final_Index/Body_Secondary_Index.pickle', 'rb') as handle:
        Secondary_Body = pickle.load(handle)

    with open('Final_Index/Infobox_Final_Index/Infobox_Secondary_Index.pickle', 'rb') as handle:
        Secondary_Infobox = pickle.load(handle)

    with open('Final_Index/Links_Final_Index/Links_Secondary_Index.pickle', 'rb') as handle:
        Secondary_Links = pickle.load(handle)

    with open('Final_Index/Category_Final_Index/Category_Secondary_Index.pickle', 'rb') as handle:
        Secondary_Category = pickle.load(handle)

    with open('Final_Index/Title_Final_Index/Title_Secondary_Index.pickle', 'rb') as handle:
        Secondary_Title = pickle.load(handle)

    with open('Final_Index/Reference_Final_Index/Reference_Secondary_Index.pickle', 'rb') as handle:
        Secondary_Reference = pickle.load(handle)


    outputs = []

    # for search_query in queries:

    processing(queries, outputs, path_to_index)

    return outputs






def main():
    # path_to_index = sys.argv[1]
    # testfile = sys.argv[2]
    # path_to_output = sys.argv[3]

    path_to_index = "Final_Index/"
    testfile = "queryfile"
    path_to_output = "output.txt"

    print("\n")

    # queries = read_file(testfile)

    while(1):
        queries = input("Search : ")

        if " " in queries:
            queries = queries.split()
            for val in queries:
                val = ps.stemWord(val)

            query = ' '.join(queries)

        else:
            query = ps.stemWord(queries)

        if queries == "exit":
            break
        outputs = search(path_to_index, query)
        write_file(outputs, path_to_output)
        



if __name__ == '__main__':
    main()


