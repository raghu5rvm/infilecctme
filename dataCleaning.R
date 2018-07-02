#include library files
library("dplyr")
library("tidyr")

#load data
oldData <- read.csv("/home/raghu/Desktop/assign/data/filteredLarge.csv",stringsAsFactors = TRUE,header = TRUE)
View(head(oldData))

#replace blanks with NAs
oldData[oldData==""] <- NA

data.spacesFilled <- oldData
View(data.spacesFilled)

#list column indexes which are not useful
notUsefulIndex <- c(3,12,13,14,17,20,21,22,25,27,28,29,32)#("inStock","codAvailable","offers","deliveryTime","sizeUnit","storage","displaySize","sellerAverageRating","sellerNoOfRatings"
                    #,"sellerNoOfReviews","idealFor","specificationList")
#delete useless columns
data.usefulColsOnly <- data.spacesFilled[,-notUsefulIndex]

#From further analysis of data, these are found as invalid data and so removed
data.usefulColsOnly$sleeve[data.usefulColsOnly$sleeve=="Apparels>Women>Western Wear>Shirts, Tops & Tunics>Tops"] <- NA
data.usefulColsOnly$sleeve[data.usefulColsOnly$sleeve=="false"] <- NA
data.usefulColsOnly$sleeve[data.usefulColsOnly$sleeve=="http://dl.flipkart.com/dl/jaipur-kurti-casual-sleeveless-printed-women-s-grey-top/p/itmephsazrymfavw?pid=TOPEPB2PKZEHHMFQ"] <- NA
data.usefulColsOnly$sleeve[data.usefulColsOnly$sleeve=="http://dl.flipkart.com/dl/miss-chase-casual-3-4th-sleeve-solid-women-s-maroon-top/p/itmerquwfwhtrzna?pid=TOPE3HGFSZPUZFGG"] <- NA
data.usefulColsOnly$sleeve[data.usefulColsOnly$sleeve=="70"] <- NA
data.usefulColsOnly$sleeve[data.usefulColsOnly$sleeve=="57"] <- NA
data.usefulColsOnly$sleeve[data.usefulColsOnly$sleeve=="0"] <- NA


#drop all rows with incomplete data
dropIncomplete <- function(data, variables){
  completeIndexes <- complete.cases(data[,variables])
  return(data[completeIndexes, ])
}

data.nasDropped <- dropIncomplete(data.usefulColsOnly,c("productId","mrp","sellingPrice","specialPrice","categories","productBrand","color"
                                                        ,"size","sleeve","neck","sellerName","keySpecsStr","detailedSpecsStr"))

#check for more incomplete data if still exists
for(i in head){
  print (i)
  print (sum(is.na(data.nasDropped$i)))
}


View(data.nasDropped)

data.correctDataTypes <- data.nasDropped

#format and correct data types of columns
data.correctDataTypes$mrp <- as.numeric(data.correctDataTypes$mrp)

data.correctDataTypes$sellingPrice <- as.numeric(data.correctDataTypes$sellingPrice)

data.correctDataTypes$specialPrice <- as.numeric(data.correctDataTypes$specialPrice)

data.correctDataTypes$discount<- as.numeric(data.correctDataTypes$discount)

data.correctDataTypes$shippingCharges<- as.numeric(data.correctDataTypes$shippingCharges)

data.correctDataTypes$shippingCharges<- as.numeric(data.correctDataTypes$shippingCharges)


#summarize data
summary(data.correctDataTypes)

#sort by sellerName,productBrand,mrp
data.sorted <- data.correctDataTypes[with(data.correctDataTypes, order(sellerName,productBrand,mrp)),]

#export to csv
write.csv(data.sorted,file="/home/raghu/Desktop/assign/dataCleanedLarge.csv",sep=",",col.names=TRUE)
