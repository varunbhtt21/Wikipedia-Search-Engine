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


tree = ET.parse('wiki.xml')
root = tree.getroot()
count = 0

for tag in root:
	
	page = str(tag)
	page = processing(page)

	# FOR PAGES
	if page == 'page':

		# FOR TITLES
		for tit in tag:
			title = str(tit)
			title = processing(title)

			if title == 'title':
				print("title : ",tit.text)
                                                           
                                                       
			# FOR TEXT
			if title == 'revision':
				for tex in tit:
					if processing(str(tex)) == 'text':
						Extract_Infobox(str(tex.text.encode('utf8')))
						count += 1
						if count == 3:
							exit()


			
		


				
			
















	


