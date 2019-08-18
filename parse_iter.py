import xml.etree.cElementTree as ET


def processing(word):
    try:
        word = word.split('}')[1]
    except:
        pass
    return word



def main():
    count = 0
    for event, elem in context:
        tag = elem.tag

        if event == 'end':
            given_tag = processing(str(tag))

            if given_tag == 'page':
                count += 1
                f = open("Data/DOC "+str(count), 'w')

                # Getting Information of Title and Text
                for titl in elem:
                    page_tag = processing(str(titl.tag))

                    if page_tag == 'title':
                        # print("title : ", titl.text)
                        
                        if type(titl.text) is not None:
                            f.write("Title : " + titl.text.encode('utf8') + "\n")

                    if page_tag == 'revision':
                        for tex in titl:
                            if processing(str(tex.tag)) == 'text':
                                # print("text : ", tex.text)

                                if tex.text is not None:
                                    f.write("Text : " + tex.text.encode('utf8') + "\n")
                             
                elem.clear()





if __name__== "__main__":
    file_path = "wiki.xml"
    context = ET.iterparse(file_path)
    main()
    print("Done")
