import xml.etree.cElementTree as ET
import mwparserfromhell



#**************************************************************************
# String Processing Function [Use to clear the namespaces]
def processing(word):
    try:
        word = word.split('}')[1]
    except:
        pass
    return word



#**************************************************************************
# Get Infobox Values
def Infobox_Extraction(page):
    """Parse out the first Infobox for the page as a dict."""
    templates = mwparserfromhell.parse(page).filter_templates()
    # filter_templates() : Make the list out of the text
    # strip()            : Remove left and right spaces

    infobox = {}
    for template in templates:
        if template.name.strip_code().startswith('Infobox'):
            infobox = {
                str(p.name).strip(): p.value.strip_code().strip()
                for p in template.params if p.value.strip_code().strip()
            }
    return infobox 



#**************************************************************************
# Get References
def References(page):
    templates = mwparserfromhell.parse(page).filter_external_links()
    # filter_templates() : Make the list out of the text
    # strip() : remove left and right spaces
    print(templates)



#**************************************************************************
# Get Category Values
def get_Category(page):

    for i in page.splitlines():
        if "Category" in i:
            Category = i.split(":")

            if len(Category)>1:
                print(Category[1].split("]]")[0])


#**************************************************************************
# Get Body Tag Value
def body_tag(page):
    


#**************************************************************************
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
                f = open("Data/DOC "+str(count), 'w')

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
                                    # Infobox_Extraction(tex.text)
                                    # References(tex.text)
                                    get_Category(tex.text)
                                    
                                    
                                    # f.write("Text : " + tex.text.encode('utf8') + "\n")
                             
                elem.clear()





if __name__== "__main__":
    file_path = "wiki.xml"
    context = ET.iterparse(file_path)
    main()
    print("Done")
