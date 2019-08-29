import xml.etree.cElementTree as ET
import re
# from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from collections import Counter
from collections import defaultdict
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import SnowballStemmer
import timeit
import gc



# ************************************************************************************************************************************

def index_file():

    f1 = open("Data/Infobox.txt", 'w')
    f2 = open("Data/Category.txt", 'w')
    f3 = open("Data/Links.txt", 'w')
    f4 = open("Data/Body.txt", 'w')
    f5 = open("Data/Title.txt", 'w')


    global Infobox_Posting_List
    global Category_Posting_List
    global Body_Posting_List
    global Links_Posting_List
    global Title_Posting_List

    for i in Infobox_Posting_List:
        f1.write(i + " : ")
        for j in Infobox_Posting_List[i]:
            f1.write("[ ")
            for k in j:
                f1.write(str(k)+" ")
            f1.write("] ,")
        f1.write("\n")

    for i in Category_Posting_List:
        f2.write(i + " : ")
        for j in Category_Posting_List[i]:
            f2.write("[ ")
            for k in j:
                f2.write(str(k)+" ")
            f2.write("] ,")
        f2.write("\n")



    for i in Body_Posting_List:
        f4.write(i + " : ")
        for j in Body_Posting_List[i]:
            f4.write("[ ")
            for k in j:
                f4.write(str(k)+" ")
            f4.write("] ,")
        f4.write("\n")



    for i in Links_Posting_List:
        f3.write(i + " : ")
        for j in Links_Posting_List[i]:
            f3.write("[ ")
            for k in j:
                f3.write(str(k)+" ")
            f3.write("] ,")
        f3.write("\n")


    for i in Title_Posting_List:
        f5.write(i + " : ")
        for j in Title_Posting_List[i]:
            f5.write("[ ")
            for k in j:
                f5.write(str(k)+" ")
            f5.write("] ,")
        f5.write("\n")

       

    f1.close()
    f2.close()
    f3.close()
    f4.close()
    f5.close()




#*******************************************************************************************************************************************

Infobox_Posting_List = defaultdict(list)
Category_Posting_List = defaultdict(list)
Body_Posting_List = defaultdict(list)
Links_Posting_List = defaultdict(list)
Title_Posting_List = defaultdict(list)

def posting_list(guest_list, catg):
    global DOC_NO

    global Infobox_Posting_List
    global Category_Posting_List
    global Body_Posting_List
    global Links_Posting_List
    global Title_Posting_List
    
    counter_list = Counter(guest_list)
    temp = set(guest_list)


    if catg == "infobox":
        for i in temp:
            Infobox_Posting_List[i].append((DOC_NO, counter_list[i]))

    if catg == "category":
        for i in temp:
            Category_Posting_List[i].append((DOC_NO, counter_list[i]))

    if catg == "body":
        for i in temp:
            Body_Posting_List[i].append((DOC_NO, counter_list[i]))

    if catg == "links":
        for i in temp:
            Links_Posting_List[i].append((DOC_NO, counter_list[i]))

    if catg == "title":
        for i in temp:
            Title_Posting_List[i].append((DOC_NO, counter_list[i]))




#****************************************************************************************************************************************

def print_PostingList():
    global Infobox_Posting_List
    global Category_Posting_List
    global Body_Posting_List
    global Links_Posting_List
    global Title_Posting_List
    
    for i in Infobox_Posting_List:
        print(i, Infobox_Posting_List[i])

    for i in Category_Posting_List:
        print(i, Category_Posting_List[i])

    for i in Body_Posting_List:
        print(i, Body_Posting_List[i])

    for i in Links_Posting_List:
        print(i, Links_Posting_List[i])

    for i in Title_Posting_List:
        print(i, Title_Posting_List[i])





#***************************************************************************************************************************************
stop_words = set(stopwords.words("english"))
#stop_words = ['all', 'just', "don't", 'being', 'over', 'both', 'through', 'yourselves', 'its', 'before', 'o', 'don', 'hadn', 'herself', 'll', 'had', 'should', 'to', 'only', 'won', 'under', 'ours', 'has', "should've", "haven't", 'do', 'them', 'his', 'very', "you've", 'they', 'not', 'during', 'now', 'him', 'nor', "wasn't", 'd', 'did', 'didn', 'this', 'she', 'each', 'further', "won't", 'where', "mustn't", "isn't", 'few', 'because', "you'd", 'doing', 'some', 'hasn', "hasn't", 'are', 'our', 'ourselves', 'out', 'what', 'for', "needn't", 'below', 're', 'does', "shouldn't", 'above', 'between', 'mustn', 't', 'be', 'we', 'who', "mightn't", "doesn't", 'were', 'here', 'shouldn', 'hers', "aren't", 'by', 'on', 'about', 'couldn', 'of', "wouldn't", 'against', 's', 'isn', 'or', 'own', 'into', 'yourself', 'down', "hadn't", 'mightn', "couldn't", 'wasn', 'your', "you're", 'from', 'her', 'their', 'aren', "it's", 'there', 'been', 'whom', 'too', 'wouldn', 'themselves', 'weren', 'was', 'until', 'more', 'himself', 'that', "didn't", 'but', "that'll", 'with', 'than', 'those', 'he', 'me', 'myself', 'ma', "weren't", 'these', 'up', 'will', 'while', 'ain', 'can', 'theirs', 'my', 'and', 've', 'then', 'is', 'am', 'it', 'doesn', 'an', 'as', 'itself', 'at', 'have', 'in', 'any', 'if', 'again', 'no', 'when', 'same', 'how', 'other', 'which', 'you', "shan't", 'shan', 'needn', 'haven', 'after', 'most', 'such', 'why', 'a', 'off', 'i', 'm', 'yours', "you'll", 'so', 'y', "she's", 'the', 'having', 'once']

# ps = PorterStemmer()
ps = SnowballStemmer('english')
Category_Final_List = []
final_list = []

def stemming(words, catg):
    global final_list 

    if final_list:
        del final_list[:]

    for w in words:
        #gc.disable()
        val = ps.stem(w)

        if val == 'br':
            continue

        if val == 'redirect':
            continue

        final_list.append(val)

    #gc.enable()

    if catg == "infobox":
        posting_list(final_list, "infobox")

    if catg == "category":
        posting_list(final_list, "category")

    if catg == "links":
        posting_list(final_list, "links")

    if catg == "body":
        posting_list(final_list, "body")

    if catg == "title":
        posting_list(final_list, "title")


#****************************************************************************************************************************************
# String Processing Function [Use to clear the namespaces]
def processing(word):
    try:
        word = word.split('}')[1]
    except:
        pass
    return word


#******************************************************************************************************************************************

def Title_Extraction(word):

    title = word.split()
    stemming(title, "title")


#************************************************************************************************************************************************
# Get Infobox Values

infobox_body = []
pos_1 = -1
pos_2 = -1
def Infobox_Extraction(code):
    text = code.split("\n")
    infobox = []

    flag = 0 
    count = 1 
    
    global pos_1
    global pos_2

    pos_1 = -1
    pos_2 = -1

    for val in range(0, len(text)):
        if flag == 0 and ("Infobox" in text[val] or "information" in text[val]):
            flag = 1
            pos_1 = val
            continue

        if flag == 1:
            if "{{" in text[val]:
                count += 1
            if "}}" in text[val]:
                count -= 1

            if count != 0:
                infobox.append(text[val])

            if count==0:
                pos_2 = val
                break

   
    pattern=re.compile('[\d+\.]*[\d]+|[\w]+')

    infobox_data = []
    for line in infobox:

        words=re.findall(pattern, line)
        if "br" in words:
            words.remove("br")
        if "Infobox" in words:
            words.remove("Infobox")

        infobox_data.extend(words)

    stemming(infobox_data, "infobox")



posn_links = -1
#***********************************************************************************************************************************************
# Get References
def links(text):
    External_links = []

    # url_template = mwparserfromhell.parse(page)
    
    
    pattern=re.compile('[\d+\.]*[\d]+|[\w]+')
    text = text.split("\n")
    global posn_links

    flag = 0
    posn_links = -1
    for line in range(0, len(text)):
        if "External links" in text[line] and flag == 0:
            posn_links = line
            flag = 1

        if flag == 1 and "*" in text[line]:
            words=re.findall(pattern, text[line])
            External_links.extend(words)


    stemming(External_links, "links")
    

#***********************************************************************************************************************************************
# Get Category Values

posn_Category = -1
def get_Category(text):

    Cat = []
    Category_data = []

    pattern=re.compile('[\d+\.]*[\d]+|[\w]+')

    global posn_Category
    posn_Category = -1

    flag = 0
    text = text.split("\n")

    for i in range(0, len(text)):
        if "Category" in text[i]:
            Category = text[i].split(":")
            flag += 1

            if flag == 1:
                posn_Category = i
                flag += 1

            if len(Category)>1:
                Cat.append(Category[1].split("]]")[0])



    for line in Cat:
        words=re.findall(pattern, line)
        Category_data.extend(words)

    stemming(Category_data, "category")
    


#**************************************************************************
# Get Body Tag Value


def body_tag(text):

    global posn_Category
    global posn_links
    global pos_1
    global pos_2

    text = text.split("\n")
    length = len(text)

    if posn_links == -1:
        if posn_Category == -1:
            pass
        else:
            del text[posn_Category:length]
    else:
        if posn_Category != -1:
            min_ele = min(posn_links, posn_Category)
            del text[min_ele:length]

        else:
            del text[posn_links:length]


    if pos_1 != -1:
        pos_2 += 1
        del text[pos_1:pos_2]


    body_data = []
    pattern=re.compile('[\d+\.]*[\d]+|[\w]+')

    for line in text:
        words=re.findall(pattern, line)
        body_data.extend(words)



    for i in range(0, len(body_data)):
        body_data[i] = body_data[i].lower()

    
    Refined_data = []
    for i in body_data:
        if i not in stop_words:
            Refined_data.append(i)

    
    stemming(Refined_data, "body")








DOC_NO = 0

#***********************************************************************************************************************************************
# Main Function
def main():
    
    global DOC_NO
    global title_doc

    

    for event, elem in context:
        tag = elem.tag

        if event == 'end':
            given_tag = processing(str(tag))

        #********************************************************************
        # Check for Page

            if given_tag == 'title':
                Title_Extraction(elem.text)
                DOC_NO += 1

                # print(elem.text)

                if DOC_NO % 1000 == 0:
                    print("DOCUMENT : " + str(DOC_NO))

                title_doc.append((DOC_NO, elem.text))
                # f6.write(str(DOC_NO) + ":"+elem.text+"\n")
        #*********************************************************************
        # Getting Information of Title and Text

                   
            if given_tag == 'text':

                # print("\n\ntext :", elem.text)
                            
                if elem.text is not None:
                    Infobox_Extraction(elem.text)
                    links(elem.text)
                    get_Category(elem.text)
                    body_tag(elem.text)

                # if DOC_NO == 5:
                #     # print_PostingList()
                #     # index_file()
                #     exit()

                             
            elem.clear()



    


title_doc = []

if __name__== "__main__":


    f6 = open("Data/Index_Title.txt", 'w')
    file_path = "wiki.xml"
    context = ET.iterparse(file_path)
    start=timeit.default_timer()

    main()
    # print_PostingList()
    index_file()
    stop=timeit.default_timer()
    print(stop-start)

    for i in title_doc:
        f6.write(str(i[0]) + ":" + i[1] + "\n")
    f6.close()

    print("Done")







