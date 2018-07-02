import csv

cList=[0]*100
topI=[]

#read dataset
with open('data/largeData.csv', 'rb') as f:	
	dataSet = csv.reader(f,delimiter=',')
	#open a new file to redirect useful output
	with open('data/filteredLarge.csv', 'w+') as opf:		
		writer = csv.writer(opf)
		i=0
		j=0
		topCount=0
		bugs=[]
		for row in dataSet:
			#print subs[len(subs)-1]
			cList[len(row)]+=1
			if(i==0):
				writer.writerow(row)
			#check if row doesn't have all column values/ is not useful for parsing
			elif(len(row)<32):
				print (i," some ",len(row),"columns found out of 32\n")	
				j+=1
			else:
				subs = row[8].split(">")
				if(len(subs)>0 and subs[len(subs)-1] == 'Tops'):
					#filter and append row to output file if the product categoery is "tops"
					writer.writerow(row)
					topCount+=1
					topI.append(i)
			i+=1
			
print ("\n \n done reading file and found "+str(topCount)+" tops\tj=="+str(j)+"\n")
#print bug indexes which have less data/insufficient data
print bugs
print cList

