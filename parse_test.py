import xml.etree.ElementTree as ET 


def processing(word):
	word = word.split('}')[1].split("'")[0]
	return word


def Extract_Infobox(word):
	word = word.split("{{")
	flag = 1
	st = ""

	for i in word:
		if flag == 1:
			for j in i.split(" "):
				if j == 'Infobox':
					print("yes found")
					flag = 0
					break
		
		st += str(i)
	infobox = st.split("}}")[0]
	print(infobox)



tree = ET.iterparse('wiki.xml')
root = tree.getroot()
count = 0


for tag in root:
	page = str(tag)
	page = processing(page)

	# FOR PAGES
	if page == 'page':
		count += 1
		f = open("Data/DOC "+str(count), 'w')

		# FOR TITLES
		for tit in tag:
			title = str(tit)
			title = processing(title)

			if title == 'title':
				print("title : ",tit.text)
				if type(tit.text) is not None:
					f.write("Title : " + tit.text.encode('utf8') + "\n")
                        
                              
			# FOR TEXT
			if title == 'revision':
				for tex in tit:
					if processing(str(tex)) == 'text':

						# Extract_Infobox(str(tex.text.encode('utf8')))
						print("text : ", tex.text)

						if tex.text is not None:
							f.write("Text : " + tex.text.encode('utf8') + "\n")
                                                                               
		f.close()





			
		


				
			
















	


