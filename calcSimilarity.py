#!/usr/bin/python
"""********************************************************************************************************

libraries and dependencies

*********************************************************************************************************"""

import json
import csv
import sys
import string
import numpy as np
import gensim
from scipy import spatial


"""*********************************************************************************************************

global variables

*********************************************************************************************************"""
data = {}
opDataJson = {}
headerNames = []
model = gensim.models.KeyedVectors.load_word2vec_format('packages/gensim.bin', binary=True)
index2word_set = set(model.wv.index2word)




"""*********************************************************************************************************

function to convert sentence to feature vector using gensim model

*********************************************************************************************************"""
def avg_feature_vector(sentence, model, num_features, index2word_set):
   
    words = sentence.split()
   
    feature_vec = np.zeros((num_features, ), dtype='float32')
   
    n_words = 0
   
    for word in words:
        if word in index2word_set:
            n_words += 1
            feature_vec = np.add(feature_vec, model[word])
   
    if (n_words > 0):
        feature_vec = np.divide(feature_vec, n_words)
   
    return feature_vec
    
    
"""*********************************************************************************************************

function to identify relative products and calculate similarity

*********************************************************************************************************"""
def calcDuplicates(data):
		
		#print ("\nFunction control in calDuplicates\n")
		
		#initialize a visited dictionary for all products with default value 0
		visited = {}
		for productId in data:
			visited[productId] = 0
		
		#iterate through all non-visited products and find similar products
		for productId, values1 in data.iteritems():
			
			if(visited[productId]==1):
				continue
			
			else:
				visited[productId] = 1
				
				#collect data from row----referencce product(p1)
				title1 =  values1[0]
				#imageUrlStr1 =  values1[1]
				mrp1 = values1[2]
				sellingPrice1 = values1[3]
				specialPrice1 = values1[4]
				productUrl1 =  values1[5]
				categories1 =  values1[6]
				productBrand1 = values1[7]
				productFamily1 = values1[8]
				discount1 = values1[9]
				shippingCharges1 = values1[10]
				size1 = values1[11]
				color1 = values1[12]
				keySpecsStr1 = values1[13]
				detailedSpecsStr1 =  values1[14]
				sellerName1 = values1[15]
				sleeve1 = values1[16]
				neck1 = values1[17]
				
				#split strings for further processing
				#imageUrlStr1 =  imageUrlStr1.split(";")
				categories1 =  categories1.split(">")
				productFamily1 = productFamily1.split(",") 
				keySpecsStr1 = keySpecsStr1.split(";")
				detailedSpecsStr1 =  detailedSpecsStr1.split(";")
				
				
				#imageStr1 = ""
				cate1 = ""

				"""for links in imageUrlStr1:
					imageStr1 += str(links)
				"""
				for cat in categories1:
					cate1 += str(cat)
					
					
				"""**********************************************************************
				Analyze specs and try to find product properties
				**********************************************************************"""
				if(len(keySpecsStr1)>1):
						
					fabric1 = keySpecsStr1[1]
					fabric1 = fabric1.split(":")
					if(fabric1[0]=="Fabric"):
						fabric1 = fabric1[len(fabric1)-1]
					else:
						fabric1 = "unknown"
				else:
					fabric1 = "unknown"

				if(len(detailedSpecsStr1)>1 and fabric1=="unknown"):
						
					fabric1 = detailedSpecsStr1[1]
					fabric1 = fabric1.split(":")
					if(fabric1[0]=="Fabric"):
						fabric1 = fabric1[len(fabric1)-1]
					else:
						fabric1 = "unknown"
						
						
				if(len(keySpecsStr1)>2):
						
					printPattern1 = keySpecsStr1[2]
					printPattern1 = printPattern1.split(":")
					if(printPattern1[0]=="Pattern"):
						printPattern1 = printPattern1[len(printPattern1)-1]
					else:
						printPattern1 = "unknown"
				else:
					printPattern1 = "unknown"

				if(len(detailedSpecsStr1)>2 and printPattern1 == "unknown"):
						
					printPattern1 = detailedSpecsStr1[2]
					printPattern1 = printPattern1.split(":")
					if(printPattern1[0]=="Pattern"):
						printPattern1 = printPattern1[len(printPattern1)-1]
					else:
						printPattern1 = "unknown"
				
				
				if(len(keySpecsStr1)>3):
						
					topType1 = keySpecsStr1[3]
					topType1 = topType1.split(":")
					if(topType1[0]=="Type"):
						topType1 = topType1[len(topType1)-1]
					else:
						topType1 = "unknown"
				else:
					topType1 = "unknown"

				if(len(detailedSpecsStr1)>3 and topType1 == "unknown"):
						
					topType1 = detailedSpecsStr1[3]
					topType1 = topType1.split(":")
					if(topType1[0]=="Type"):
						topType1 = topType1[len(topType1)-1]
					else:
						topType1 = "unknown"
				"""**********************************************************************
				End of specs analysis
				**********************************************************************"""
								
					
				
				
				#create product1 string
				p1str = title1+" "+mrp1+" "+str(sellingPrice1)+" "+str(specialPrice1)+" "+productUrl1+" "+cate1+" "+productBrand1+" "+str(discount1)+" "+str(shippingCharges1)+" "+sleeve1+" "+neck1+" "+fabric1+" "+printPattern1+" "+size1+" "+topType1
				#print ("\nString1 == "+p1str)
				p1StrV = avg_feature_vector(p1str, model=model, num_features=300, index2word_set=index2word_set)
				
				tempOutput = []
				#scan all product ids in product family0
				print ("number of family members = "+str(len(productFamily1)))
				for e in productFamily1:
						if(data.has_key(e)):
							print ("\nproduct family member found in dataset\n")
							visited[e]=1
							product2 = data[e]
							
							title2 =  product2[0]
							#imageUrlStr2 =  product2[1]
							mrp2 = product2[2]
							sellingPrice2 = product2[3]
							specialPrice2 = product2[4]
							productUrl2 =  product2[5]
							categories2 =  product2[6]
							productBrand2 = product2[7]
							productFamily2 = product2[8]
							discount2 = product2[9]
							shippingCharges2 = product2[10]
							size2 = product2[11]
							color2 = product2[12]
							keySpecsStr2 = product2[13]
							detailedSpecsStr2 =  product2[14]
							sellerName2 = product2[15]
							sleeve2 = product2[16]
							neck2 = product2[17]
							
							#split strings for further processing
							#imageUrlStr2 =  imageUrlStr2.split(";")
							categories2 =  categories2.split(">")
							productBrand2 = product2[7]
							productFamily2 = productFamily2.split(",") 
							keySpecsStr2 = keySpecsStr2.split(";")
							detailedSpecsStr2 =  detailedSpecsStr2.split(";")
							sellerName2 = product2[15]	
							
							"""*******************************************************
							specs analysis
							******************************************************"""
							if(len(keySpecsStr2)>1):
									
								fabric2 = keySpecsStr2[1]
								fabric2 = fabric2.split(":")
								if(fabric2[0]=="Fabric"):
									fabric2 = fabric2[len(fabric2)-1]
								else:
									fabric2 = "unknown"
							else:
									fabric2 = "unknown"
									
							if(len(detailedSpecsStr1)>1 and fabric2=="unknown"):
									
								fabric2 = detailedSpecsStr1[1]
								fabric2 = fabric2.split(":")
								if(fabric2[0]=="Fabric"):
									fabric2 = fabric2[len(fabric2)-1]
								else:
									fabric2 = "unknown"
									
									
							if(len(keySpecsStr2)>2):
									
								printPattern2 = keySpecsStr2[2]
								printPattern2 = printPattern2.split(":")
								if(printPattern2[0]=="Pattern"):
									printPattern2 = printPattern2[len(printPattern2)-1]
								else:
									printPattern2 = "unknown"
							else:
									printPattern2 = "unknown"

							if(len(detailedSpecsStr1)>2 and printPattern2 == "unknown"):
									
								printPattern2 = detailedSpecsStr1[2]
								printPattern2 = printPattern2.split(":")
								if(printPattern2[0]=="Pattern"):
									printPattern2 = printPattern2[len(printPattern2)-1]
								else:
									printPattern2 = "unknown"
							
							
							if(len(keySpecsStr2)>3):
									
								topType2 = keySpecsStr2[3]
								topType2 = topType2.split(":")
								if(topType2[0]=="Type"):
									topType2 = topType2[len(topType2)-1]
								else:
									topType2 = "unknown"
							else:
								topType2 = "unknown"

							if(len(detailedSpecsStr1)>3 and topType2 == "unknown"):
									
								topType2 = detailedSpecsStr1[3]
								topType2 = topType2.split(":")
								if(topType2[0]=="Type"):
									topType2 = topType2[len(topType2)-1]
								else:
									topType2 = "unknown"							


							"""*******************************************************
							end of specs analysis for product2
							******************************************************"""
							cate2 = ""
							for cat in categories2:
								cate2 += str(cat)
							
							#create product2 string
							p2str = title2+" "+mrp2+" "+str(sellingPrice2)+" "+str(specialPrice2)+" "+productUrl2+" "+cate2+" "+productBrand2+" "+str(discount2)+" "+str(shippingCharges2)+" "+sleeve2+" "+neck2+" "+fabric2+" "+printPattern2+" "+str(size2)+" "+topType2
							
							#create product2 vector
							p2StrV = avg_feature_vector(p2str, model=model, num_features=300, index2word_set=index2word_set) 
							
							print ("\np1-string-"+p1str+"\np2-string-"+p2str)
							
							#calculate similarity
							sim = 1 - spatial.distance.cosine(p1StrV, p2StrV)
							sim = sim *1000 / 1000
							sim = "%.8f" % sim

							print ("************************************\n")
							print ("\t\t"+str(sim)+"")
							print ("\n**********************************\n\n\n")
							
							if(sim>0.500000):
								result =[]
								result.append(e)
								result.append(str(sim))
								tempOutput.append(result)

				if(len(tempOutput)>0):
					opDataJson[productId] = tempOutput





"""***********************************************************************************************************

		function to read data and find similar items based on product family column 

***********************************************************************************************************"""


with open('dataCleanedLarge.csv', 'rb') as f:	

	dataSet = csv.reader(f,delimiter=',')
	print ("\ndata red sucessfully\n\n")
	loopCount=0;
	flag=0
	
	for row in dataSet:
		
		if(flag==0):
			flag=1
			continue
		elif(flag>0):
			print ("\n\ni am not stopping here\n\n\n")
			flag+=1
		else:
			break
		#initialize variables. Runs only for the first iteration
		if(loopCount==0):
			loopCount += 1
			currSeller = row[17]
		
		newSeller = row[17]
		print ("current seller="+currSeller+" and newSeller= "+newSeller)	
		if( newSeller != currSeller ):
			
			#search for duplicates with data stored till now
			calcDuplicates(data)
			flag=2
			print ("\n*************************************************\n")
			#print (data)
			print ("\n**************************************************\n")
			#clear contents of dictionary
			data.clear()
			#update seller details
			currSeller = row[17]	
			#add current row to dictionary
			colContents = [row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],row[18],row[19]]
			data[row[1]] = colContents
		
		else:
			colContents = [row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],row[18],row[19]]
			data[row[1]] = colContents
	#final call to the function, just for last seller.
	calcDuplicates(data)
	

	
"""**************************************************************************************************************
dump output data into json file
************************************************************************************************************"""

with open('output.json', 'w') as fp:
    json.dump(opDataJson, fp,sort_keys=True, indent=5)
    

print ("\n\ntesting done")		

