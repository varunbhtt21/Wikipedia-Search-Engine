import xml.etree.cElementTree as ET
import mwparserfromhell
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
        f5.write(i.encode('utf8') + " : ")
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
        gc.disable()
        val = ps.stem(w)

        if val == 'br':
            continue

        final_list.append(val)

    gc.enable()

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
def Infobox_Extraction(code):
    """Parse out the first Infobox for the page as a dict."""
    # templates = mwparserfromhell.parse(page).filter_templates(matches='infobox .*')
    # filter_templates() : Make the list out of the text
    # strip()            : Remove left and right spaces



    global infobox_body
    infobox = []

    # code = mwparserfromhell.parse(page)

    for template in code.filter_templates():
        if 'Infobox' in template.name:
            infobox_body = template.encode('utf8').splitlines()
            infobox = template.encode('utf8').split("|")
    
    pattern=re.compile('[\d+\.]*[\d]+|[\w]+')

    infobox_data = []
    for line in infobox:

        gc.disable()
        words=re.findall(pattern, line)
        if "br" in words:
            words.remove("br")
        if "Infobox" in words:
            words.remove("Infobox")

        infobox_data.extend(words)

    gc.enable()

    # print(infobox_data)
    stemming(infobox_data, "infobox")




#***********************************************************************************************************************************************
# Get References
def links(url_template):
    External_links = []

    # url_template = mwparserfromhell.parse(page)
    
    flag = 0
    pattern=re.compile('[\d+\.]*[\d]+|[\w]+')

    for line in url_template.encode('utf8').splitlines():
        if "External links" in line and flag == 0:
            flag = 1

        if flag == 1 and "*" in line:
            gc.disable()
            words=re.findall(pattern, line)
            External_links.extend(words)

    gc.enable()

    # print(External_links)
    stemming(External_links, "links")
    
    # filter_templates() : Make the list out of the text
    # strip() : remove left and right spaces
    


#***********************************************************************************************************************************************
# Get Category Values

def get_Category(page):

    Cat = []
    Category_data = []

    pattern=re.compile('[\d+\.]*[\d]+|[\w]+')


    for i in page.splitlines():
        gc.disable()
        if "Category" in i:
            Category = i.split(":")

            if len(Category)>1:
                Cat.append(Category[1].split("]]")[0])

    gc.enable()


    for line in Cat:
        gc.disable()
        words=re.findall(pattern, line)
        Category_data.extend(words)
    gc.enable()

    stemming(Category_data, "category")
    # print(Category_data)  

    



#**************************************************************************
# Get Body Tag Value


def body_tag(page):

    body_data = []
    text = page.splitlines()
    pattern=re.compile('[\d+\.]*[\d]+|[\w]+')

    global infobox_body
    body = []

    count = 0
    pos = -1
    flag = 0


    for i in text:
        if i not in infobox_body:
            gc.disable()
            body.append(i)

            if flag == 0:
                if "References" in i or "External links" in i or "Category" in i :
                    pos = count
                    flag = 1
            count += 1
    gc.enable()
 

    for line in body:
        gc.disable()
        words=re.findall(pattern, line)
        body_data.extend(words)
    gc.enable()

    dl = []
    stop_words = set(stopwords.words("english"))

    for i in range(0, len(body_data)):
        body_data[i] = body_data[i].lower()

    
    Refined_data = []
    for i in body_data:
        gc.disable()
        if i not in stop_words:
            Refined_data.append(i)

    gc.enable()

    # Clear List
    del infobox_body[:]

    #print(Refined_data)
    
    # print(len(body_data))
    stemming(Refined_data, "body")
    # del body_data[:]

    
        

DOC_NO = 0
#***********************************************************************************************************************************************
# Main Function
def main():
    
    global DOC_NO

    for event, elem in context:
        tag = elem.tag

        if event == 'end':
            given_tag = processing(str(tag))

        #********************************************************************
        # Check for Page

            if given_tag == 'page':
                DOC_NO += 1

                print("DOCUMENT : " + str(DOC_NO))
        #*********************************************************************
        # Getting Information of Title and Text

                for titl in elem:
                    page_tag = processing(str(titl.tag))

                    if page_tag == 'title':
                        Title_Extraction(titl.text)
                        # print("title : ", titl.text)
                        
                        # if titl.text is not None:
                        #     f.write("Title : " + titl.text.encode('utf8') + "\n")

                    if page_tag == 'revision':
                        for tex in titl:
                            if processing(str(tex.tag)) == 'text':
                                # print("text : ", tex.text)

                                if tex.text is not None:
                                    code = mwparserfromhell.parse(tex.text)

                                    Infobox_Extraction(code)
                                    links(code)
                                    get_Category(tex.text)
                                    body_tag(code)

                                    # if DOC_NO == 500:
                                    #     print_PostingList()
                                    #     index_file()
                                    #     exit()

                             
                elem.clear()

    




if __name__== "__main__":
    file_path = "wiki.xml"
    context = ET.iterparse(file_path)
    start=timeit.default_timer()

    main()
    print_PostingList()
    index_file()
    stop=timeit.default_timer()
    print(stop-start)

    print("Done")












