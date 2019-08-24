import xml.etree.cElementTree as ET
import mwparserfromhell
import re
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

stop_words = set(stopwords.words("english"))
ps = PorterStemmer()

Infobox_Final_List = []
Category_Final_List = []

def stemming(words):
    global final_list 

    if final_list:
        del final_list[:]

    for w in words:
        val = ps.stem(w)
        if val not in final_list and val not in stop_words:
            final_list.append(val)

    print(final_list)



#**************************************************************************
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
def Infobox_Extraction(page):
    """Parse out the first Infobox for the page as a dict."""
    # templates = mwparserfromhell.parse(page).filter_templates(matches='infobox .*')
    # filter_templates() : Make the list out of the text
    # strip()            : Remove left and right spaces



    global infobox_body

    infobox = []
    code = mwparserfromhell.parse(page)

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
def links(page):
    External_links = []
    url_template = mwparserfromhell.parse(page)
    flag = 0
    pattern=re.compile('[\d+\.]*[\d]+|[\w]+')

    for line in url_template.encode('utf8').splitlines():
        if "External links" in line and flag == 0:
            flag = 1

        if flag == 1 and "*" in line:
            words=re.findall(pattern, line)
            External_links.extend(words)

    # print(External_links)
    print("\n\n\n\n")
    
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


    # print(Category_data)  

    



#**************************************************************************
# Get Body Tag Value

body_data = []
def body_tag(page):
    text = mwparserfromhell.parse(page).splitlines()
    infobox_temp = mwparserfromhell.parse(page).filter_templates(matches='infobox .*')
    pattern=re.compile('[\d+\.]*[\d]+|[\w]+')

    global infobox_body
    body = []
    
    for i in text:
        if i not in infobox_body:
            body.append(i)

    count = 0
    pos = -1
    for i in body:
        if "References" in i or "External links" in i or "Category" in i :
            pos = count
            break
        count += 1

    length = len(body)

    if pos != -1:
        del body[pos:length]


    for line in body:
        words=re.findall(pattern, line)
        body_data.extend(words)


    # Clear List
    del infobox_body[:]

    
        


#***********************************************************************************************************************************************
# Main Function
def main():
    count = 0
    for event, elem in context:
        tag = elem.tag

        if event == 'end':
            given_tag = processing(str(tag))

        #********************************************************************
        # Check for Page

            if given_tag == 'page':
                count += 1
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
                                    Infobox_Extraction(tex.text)
                                    links(tex.text)
                                    get_Category(tex.text)
                                    body_tag(tex.text)

                                    if count == 10:
                                        exit()

                                               
                                    # f.write("Text : " + tex.text.encode('utf8') + "\n")
                             
                elem.clear()





if __name__== "__main__":
    file_path = "wiki.xml"
    context = ET.iterparse(file_path)
    main()
    print("Done")












