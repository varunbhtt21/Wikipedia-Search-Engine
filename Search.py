from collections import defaultdict
import re

Infobox_Posting_List = defaultdict(list)
Category_Posting_List = defaultdict(list)
Body_Posting_List = defaultdict(list)
Links_Posting_List = defaultdict(list)
Title_Posting_List = defaultdict(list)




def Loading_Data(Posting_List, catg):

	f=open(catg, "r")

	content = f.read()

	content = content.split("\n")
	count = 0

	for i in content:

		if not i:
			continue

		key = i.split(":")[0].strip()
		value = i.split(":")[1]
		
		value = value.replace("[", " ")
		value = value.replace("]"," ").split(",")

		for i in value:
			val = i.strip().split()
			if val:
				try:
					Posting_List[key].append((int(val[0]), int(val[1])))
				except:
					pass

		




def main():

	print("\nProcessing...\n")
	
	global Infobox_Posting_List
	global Title_Posting_List
	global Links_Posting_List
	global Category_Posting_List
	global Body_Posting_List


	Loading_Data(Infobox_Posting_List, "Infobox.txt")
	Loading_Data(Title_Posting_List, "Title.txt")
	Loading_Data(Links_Posting_List, "Links.txt")
	Loading_Data(Category_Posting_List, "Category.txt")
	Loading_Data(Body_Posting_List, "Body.txt")
	
	# print(Infobox_Posting_List)
	# print(Title_Posting_List)
	# print(Links_Posting_List)
	# print(Category_Posting_List)
	# print(Body_Posting_List)












if __name__== "__main__":
    main()
    print("Done")

