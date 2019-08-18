import xml.etree.cElementTree as ET
file_path = "wiki.xml"
context = ET.iterparse(file_path, events=("start", "end"))


def processing(word):

    try:
        word = word.split('}')[1]
    except:
        pass

    return word


count = 0
# turn it into an iterator
context = iter(context)
on_members_tag = False

for event, elem in context:
    tag = elem.tag
    value = elem.text
    
    if value :
        value = value.encode('utf-8').strip()

    if event == 'start' :
        pass




    if event == 'end':

        # FOR PAGES
        page = str(tag)
        page = processing(page)
        if page == 'page':
            count += 1
            # f = open("Data/DOC "+str(count), 'w')

            # FOR TITLES
            for tit in elem:

                title = tit.tag
                value = tit.text
                
               
                title = str(title)
                title = processing(title)

                if title == 'title':
                    print("title : ",tit.text)
                    break
                    if type(tit.text) is not None:
                        print("yes")
                        # f.write("Title : " + tit.text.encode('utf8') + "\n")
                        
                              
                # FOR TEXT
                if title == 'revision':
                    for tex in tit:
                        if processing(str(tex)) == 'text':

                            # Extract_Infobox(str(tex.text.encode('utf8')))
                            print("text : ", tex.text)

                            if tex.text is not None:
                                print("No")
                                # f.write("Text : " + tex.text.encode('utf8') + "\n")
                                                                               
            # f.close()
    elem.clear()