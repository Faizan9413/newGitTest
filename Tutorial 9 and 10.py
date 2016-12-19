# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 08:32:58 2016

@author: 100518916
"""

import csv
import math
import operator

train = csv.reader(open('SchoolkidsTrain.csv'))
test = csv.reader(open('SchoolkidsTest.csv'))

#skip the header
train.__next__()
test.__next__()




# assign a value to the string atributes in the data
map = {
'boy':0,'girl':1,
'Rural':0, 'Suburban':0.5,  'Urban':1,
'Sports':0, 'Grades':0.45, 'Popular':1
}


#the training data
training = []
trainingMax = [0,0,0,0,0,0,0,0,0]
trainingMin = [9999,9999,9999,9999,9999,9999,9999,9999,9999]


# the data to be tested
testing = []
testingMax = [0,0,0,0,0,0,0,0,0]
testingMin = [9999,9999,9999,9999,9999,9999,9999,9999,9999]



#--------------------------------------------------------------------------------------------
#calculate the euclidean distance between the training data and the new data
def euclideanDistance(train,newData):
    eucDist = 0
    for i in range(len(train)-1):
        eucDist += pow((train[i] - newData[i]),2)
    eucDist = math.sqrt(eucDist)
    return (eucDist)
    
 # predict the goal   
def predict(newData,k):

    eucDistances = []
    
    #calculate the euclidean distance between the new data and everything in the training set
    for i in range(len(training)):
        eucDist = euclideanDistance(training[i],newData)
        eucDistances.append((training[i],eucDist))
    
    # sort the distances list based on the distance
    eucDistances.sort(key = operator.itemgetter(1))
    
    sports = 0
    grades = 0
    popular = 0
    
    #calculate prediction
    for i in range(k):
        if (eucDistances[i][0][8] == 0.0):
            sports += 1
        if (eucDistances[i][0][8] == 0.45):
            grades += 1
        if (eucDistances[i][0][8] == 1.0):
            popular += 1
    
    if((sports > grades) and (sports > popular)):
        return(0)
    if((grades > sports) and (grades > popular)):
        return(0.45)
    if((popular > grades) and (popular > sports)):
        return(1)
        
    #if all sports grades and popular the same then just pick sports    
    else:
        return(0)
    

#--------------------------------------------------------------------------------------------


for row in train:
    temp = []
    #access each cloumn in the row
    for i in range(len(row)):
        
        # if the current column is in the map
        if(row[i] in map):
            #add the integer value of it into the temp
            temp.append(map[row[i]])
            
            #else add the value in that column into temp as a float
        else:
            temp.append(float(row[i]))
            
         #find the max and min value for each column   
        if(temp[i] > trainingMax[i]):
            trainingMax[i] = temp[i]
            
        if(temp[i] < trainingMin[i]):
            trainingMin[i] = temp[i]
            
    #add the row to the training list        
    training.append(temp)
 
 
for row in test:
    temp = []
    #access each cloumn in the row
    for i in range(len(row)):
        
        # if the current column is in the map
        if(row[i] in map):
            #add the integer value of it into the temp
            temp.append(map[row[i]])
            
            #else add the value in that column into temp as a float
        else:
            temp.append(float(row[i]))
            
         #find the max and min value for each column   
        if(temp[i] > testingMax[i]):
            testingMax[i] = temp[i]
            
        if(temp[i] < testingMin[i]):
            testingMin[i] = temp[i]
            
    #add the row to the training list        
    testing.append(temp)   


#Normalize the training data - so everything is in the range 0-1 and no attribute dominates the other

for i in range(len(training)):
    for j in range(len(training[i])):
        training[i][j] = (training[i][j] - trainingMin[j])  / (trainingMax[j] - trainingMin[j])
      
        

#Normalize the testing data - so everything is in the range 0-1 and no attribute dominates the other

for i in range(len(testing)):
    for j in range(len(testing[i])):
        testing[i][j] = (testing[i][j] - testingMin[j])  / (testingMax[j] - testingMin[j])



k = 50


prediction = []
correctPrediction = 0

#predict the goal for all the data in testing
for i in range(len(testing)-1):
    # call the predict method and put the goal it predicted into prediction
    prediction.append(predict(testing[i],k))
    if (prediction[i] == testing[i][8]):
        correctPrediction +=1
    print("Actual Goal:",testing[i][8]," Predicted Goal:",prediction[i] )

#accuracy
accuracy = (correctPrediction/len(testing))*100
print("Accuracy: ", accuracy,"%")
    