import xml.etree.cElementTree as ET
import mwparserfromhell
import re
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from collections import Counter
from collections import defaultdict



Infobox_Posting_List = defaultdict(list)
Category_Posting_List = defaultdict(list)
Body_Posting_List = defaultdict(list)
Links_Posting_List = defaultdict(list)

def posting_list(guest_list, catg):
    global DOC_NO

    global Infobox_Posting_List
    global Category_Posting_List
    global Body_Posting_List
    global Links_Posting_List
    
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







def print_PostingList():
    global Infobox_Posting_List
    global Category_Posting_List
    global Body_Posting_List
    global Links_Posting_List
    
    for i in Infobox_Posting_List:
        print(i, Infobox_Posting_List[i])

    for i in Category_Posting_List:
        print(i, Category_Posting_List[i])

    for i in Body_Posting_List:
        print(i, Body_Posting_List[i])

    for i in Links_Posting_List:
        print(i, Links_Posting_List[i])








#***************************************************************************************************************************************
stop_words = set(stopwords.words("english"))
#stop_words = ['all', 'just', "don't", 'being', 'over', 'both', 'through', 'yourselves', 'its', 'before', 'o', 'don', 'hadn', 'herself', 'll', 'had', 'should', 'to', 'only', 'won', 'under', 'ours', 'has', "should've", "haven't", 'do', 'them', 'his', 'very', "you've", 'they', 'not', 'during', 'now', 'him', 'nor', "wasn't", 'd', 'did', 'didn', 'this', 'she', 'each', 'further', "won't", 'where', "mustn't", "isn't", 'few', 'because', "you'd", 'doing', 'some', 'hasn', "hasn't", 'are', 'our', 'ourselves', 'out', 'what', 'for', "needn't", 'below', 're', 'does', "shouldn't", 'above', 'between', 'mustn', 't', 'be', 'we', 'who', "mightn't", "doesn't", 'were', 'here', 'shouldn', 'hers', "aren't", 'by', 'on', 'about', 'couldn', 'of', "wouldn't", 'against', 's', 'isn', 'or', 'own', 'into', 'yourself', 'down', "hadn't", 'mightn', "couldn't", 'wasn', 'your', "you're", 'from', 'her', 'their', 'aren', "it's", 'there', 'been', 'whom', 'too', 'wouldn', 'themselves', 'weren', 'was', 'until', 'more', 'himself', 'that', "didn't", 'but', "that'll", 'with', 'than', 'those', 'he', 'me', 'myself', 'ma', "weren't", 'these', 'up', 'will', 'while', 'ain', 'can', 'theirs', 'my', 'and', 've', 'then', 'is', 'am', 'it', 'doesn', 'an', 'as', 'itself', 'at', 'have', 'in', 'any', 'if', 'again', 'no', 'when', 'same', 'how', 'other', 'which', 'you', "shan't", 'shan', 'needn', 'haven', 'after', 'most', 'such', 'why', 'a', 'off', 'i', 'm', 'yours', "you'll", 'so', 'y', "she's", 'the', 'having', 'once']

ps = PorterStemmer()
Category_Final_List = []
final_list = []

def stemming(words, catg):
    global final_list 

    if final_list:
        del final_list[:]

    for w in words:
        val = ps.stem(w)

        if w == 'br':
            continue

        if w not in stop_words :
            final_list.append(w.lower())

    if catg == "infobox":
        posting_list(final_list, "infobox")

    if catg == "category":
        posting_list(final_list, "category")

    if catg == "links":
        posting_list(final_list, "links")


#****************************************************************************************************************************************
# String Processing Function [Use to clear the namespaces]
def processing(word):
    try:
        word = word.split('}')[1]
    except:
        pass
    return word



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
        words=re.findall(pattern, line)
        if "br" in words:
            words.remove("br")
        if "Infobox" in words:
            words.remove("Infobox")

        infobox_data.extend(words)

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
            words=re.findall(pattern, line)
            External_links.extend(words)

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
        if "Category" in i:
            Category = i.split(":")

            if len(Category)>1:
                Cat.append(Category[1].split("]]")[0])


    for line in Cat:
        words=re.findall(pattern, line)
        Category_data.extend(words)

    stemming(Category_data, "category")
    # print(Category_data)  

    



#**************************************************************************
# Get Body Tag Value

body_data = []
def body_tag(page):
    # text = mwparserfromhell.parse(page).splitlines()
    text = page.splitlines()

    # infobox_temp = mwparserfromhell.parse(page).filter_templates(matches='infobox .*')

    infobox_temp = page.filter_templates(matches='infobox .*')
    pattern=re.compile('[\d+\.]*[\d]+|[\w]+')

    global infobox_body
    body = []
    

    count = 0
    pos = -1

    for i in text:
        if i not in infobox_body:
            body.append(i)

            # if "References" in i:
            #     pos = count
            # count += 1

    

    for i in range(0,len(body)):
        if "References" in body[i] or "External links" in body[i] or "Category" in body[i] :
            pos = i
            break
    

    length = len(body)

    if pos != -1:
        del body[pos:length]

    for line in body:
        words=re.findall(pattern, line)
        body_data.extend(words)


    # Clear List
    del infobox_body[:]


    print(body_data)
    stemming(body_data, "body")

    
        

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

                print("page : ",DOC_NO)
                # f = open("Data/DOC "+str(count), 'w')

        #*********************************************************************
        # Getting Information of Title and Text

                for titl in elem:
                    page_tag = processing(str(titl.tag))

                    if page_tag == 'title':
                        pass
                        # print("title : ", titl.text)
                        
                        # if titl.text is not None:
                        #     f.write("Title : " + titl.text.encode('utf8') + "\n")

                    if page_tag == 'revision':
                        for tex in titl:
                            if processing(str(tex.tag)) == 'text':
                                # print("text : ", tex.text)

                                if tex.text is not None:
                                    code = mwparserfromhell.parse(tex.text)

                                    # Infobox_Extraction(code)
                                    # links(code)
                                    # get_Category(tex.text)
                                    body_tag(code)

                                    if DOC_NO == 20:
                                        print_PostingList()
                                        exit()

                                               
                                    # f.write("Text : " + tex.text.encode('utf8') + "\n")
                             
                elem.clear()

    




if __name__== "__main__":
    file_path = "wiki.xml"
    context = ET.iterparse(file_path)
    main()
    print_PostingList()
    print("Done")












