def index():
    print(""" 

1) Design a simple machine learning model to train the training instances and test the same. 
          
2) Find-s algorithm for finding the most specific.
          
3) Support Vector Machine Algorithm for Multiclass classification using Iris.CSV & wine dataset from sklearn.
                
4)	For a given set of training data examples stored in a .csv file, 
    implement and demonstrate the candidate-elimination algorithm 
    to output a description of the set of all hypotheses consistent with the training examples.     

5) Write a program to implement the Naïve Bayesian classifier 
    for a sample training data set stored as a .csv file. 
    Compute the accuracy of the classifier, considering few test data sets.
          
6) Decision Tree classifier & Random Forest Classifier. 
          
7) Data loading, feature scoring and ranking, feature selection 
    (Principal Component Analysis)
          
8a) Least Square Regression Algorithm. 
8b) Logistic Regression algorithm.
             
9a) Build an Artificial Neural Network by implementing the Backpropagation algorithm and 
    test the same using appropriate data sets. 
9b) Perform Text pre-processing, Text clustering, classification with Prediction, Test Score and Confusion Matrix  
          
10a) Implement the different Distance methods (Euclidean) with Prediction, Test Score and Confusion Matrix.
10b) Implement the classification model using K means clustering with Prediction, Test Score and Confusion Matrix.

""")
    

def prog(num):
    if num =="1":
        print(""" 
        --- Pract 1 ---
              
import matplotlib.pyplot as plt
numpy.random.seed(2)
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

x = numpy.random.normal(3,1,100)
y = numpy.random.normal(156,40,100) /x
plt.scatter(x,y)
plt.xlabel("X")
plt.ylabel("Y")
plt.show()

train_x = x[:80]
train_y = y[:80]
test_x = x[:20]
test_y = y[:20]

plt.scatter(train_x,train_y)
plt.xlabel("train_x")
plt.ylabel("train_y")
plt.show()

train_x, test_x, train_y, test_y = train_test_split(x,y,test_size=0.3)
plt.scatter(test_x,test_y)
plt.xlabel("test_x")
plt.ylabel("test_y")
plt.show()

# Draw a Polynomial Regression line through the data points with training data
mymodel = numpy.poly1d(numpy.polyfit(train_x, train_y, 4))
myline = numpy.linspace(0,6,100)
plt.scatter(train_x, train_y)
plt.plot(myline, mymodel(myline))
plt.xlabel("train_x")
plt.ylabel("train_y")
plt.show()

# Draw a Polynomial Regression line through the data points with test data
mymodel = numpy.poly1d(numpy.polyfit(test_x, test_y, 4))
myline = numpy.linspace(0,6,100)
plt.scatter(test_x, test_y)
plt.plot(myline, mymodel(myline))
plt.xlabel("test_x")
plt.ylabel("test_y")
plt.show()

r2 = r2_score(train_y, mymodel(train_x))
print("\n\nr2 Score: ",r2)
print("\nPrediction: ",mymodel(5)) 

              

        """)

    elif num =="2":
        print(""" 
        --- Pract 2  ---

import csv
a = []
with open('data.csv', 'r') as csvfile:
    next(csvfile)
    for row in csv.reader(csvfile):
        a.append(row)
    print(a)

print("\nThe total number of training instances are : ",len(a))

num_attribute = len(a[0])-1

print("\nThe initial hypothesis is : ")
hypothesis = ['0']*num_attribute
print(hypothesis)

for i in range(0, len(a)):
    if a[i][num_attribute] == 'yes':
        print ("\nInstance ", i+1, "is", a[i], " and is Positive Instance")
        for j in range(0, num_attribute):
            if hypothesis[j] == '0' or hypothesis[j] == a[i][j]:
                hypothesis[j] = a[i][j]
            else:
                hypothesis[j] = '?'
        print("The hypothesis for the training instance", i+1, " is: " , hypothesis, "\n")

    if a[i][num_attribute] == 'no':
        print ("\nInstance ", i+1, "is", a[i], " and is Negative Instance Hence Ignored")
        print("The hypothesis for the training instance", i+1, " is: " , hypothesis, "\n")

print("\nThe Maximally specific hypothesis for the training instance is ", hypothesis) 


                            
        """)

    elif num =="3":
        print(""" 
        --- Pract 3  ---

from sklearn import svm, datasets
import sklearn.model_selection as model_selection
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns 

iris = datasets.load_iris()
#iris = datasets.load_wine()

X = iris.data[:, :2]
y = iris.target
X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, train_size=0.80, test_size=0.20, random_state=101)

rbf = svm.SVC(kernel='rbf', gamma=0.5, C=0.1).fit(X_train, y_train)
poly = svm.SVC(kernel='poly', degree=3, C=1).fit(X_train, y_train)

poly_pred = poly.predict(X_test)
rbf_pred = rbf.predict(X_test)

poly_accuracy = accuracy_score(y_test, poly_pred)
poly_f1 = f1_score(y_test, poly_pred, average='weighted')
print('Accuracy (Polynomial Kernel): ', "%.2f" % (poly_accuracy*100))
print('F1 (Polynomial Kernel): ', "%.2f" % (poly_f1*100))

rbf_accuracy = accuracy_score(y_test, rbf_pred)
rbf_f1 = f1_score(y_test, rbf_pred, average='weighted')
print('Accuracy (RBF Kernel): ', "%.2f" % (rbf_accuracy*100))
print('F1 (RBF Kernel): ', "%.2f" % (rbf_f1*100)) 

# Calculate the confusion matrix for the Polynomial Kernel model
poly_confusion_matrix = confusion_matrix(y_test, poly_pred)
print('Confusion Matrix (Polynomial Kernel):\n', poly_confusion_matrix)

# Create a heatmap of the confusion matrix for Polynomial Kernel
plt.figure(figsize=(8, 6))
sns.heatmap(poly_confusion_matrix, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix (Polynomial Kernel)')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()

# Calculate the confusion matrix for the RBF Kernel model
rbf_confusion_matrix = confusion_matrix(y_test, rbf_pred)
print('Confusion Matrix (RBF Kernel):\n', rbf_confusion_matrix)

# Create a heatmap of the confusion matrix for RBF Kernel
plt.figure(figsize=(8, 6))
sns.heatmap(rbf_confusion_matrix, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix (RBF Kernel)')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show() 

                            
        """)

    
    elif num =="4":
        print(""" 
        --- Pract 4  ---
import numpy as np
import pandas as pd

#Loading data from a csv file.
data = pd.DataFrame(data=pd.read_csv('/content/drive/MyDrive/Colab Notebooks/ML Pract/Datasets/data.csv'))
print(data)

              
#########################################################

#Separating concept features from Target
concepts = np.array(data.iloc[:,0:6])
print(concepts)

#########################################################

#Isolating target into a separate DataFrame
#Copying last column to target  array
target = np.array(data.iloc[:,6])
print(target) 

#########################################################

def learn(concepts, target): 
#Initialise S0 with the first instance from concepts.
#.copy()makes sure a new list is created instead of just pointing to the same memory location.
    specific_h = concepts[0].copy()
    print()
    print("Initialization of specific_h and genearal_h")
    print()
    print("Specific Boundary: ", specific_h)
    general_h = [["?" for i in range(len(specific_h))] for i in range(len(specific_h))]
    print()
    print("Generic Boundary: ",general_h)  
# The learning iterations.
    for i, h in enumerate(concepts):
        print()
        print("Instance", i+1 , "is ", h)
# Checking if the hypothesis has a positive target.
        if target[i] == "yes":
            print("Instance is Positive ")
            for x in range(len(specific_h)): 
# Change values in S & G only if values change.
                if h[x]!= specific_h[x]:                    
                    specific_h[x] ='?'                     
                    general_h[x][x] ='?'
# Checking if the hypothesis has a positive target.                  
        if target[i] == "no":            
            print("Instance is Negative ")
            for x in range(len(specific_h)): 
# For negative hypothesis change values only in G.
                if h[x]!= specific_h[x]:                    
                    general_h[x][x] = specific_h[x]                
                else:                    
                    general_h[x][x] = '?'        
        
        print("Specific Bundary after ", i+1, "Instance is ", specific_h)         
        print("Generic Boundary after ", i+1, "Instance is ", general_h)
        print()
# find indices where we have empty rows, meaning those that are unchanged.
    indices = [i for i, val in enumerate(general_h) if val == ['?', '?', '?', '?', '?', '?']]    
    for i in indices:   
# remove those rows from general_h
        general_h.remove(['?', '?', '?', '?', '?', '?']) 
# Return final values
    return specific_h, general_h 

s_final, g_final = learn(concepts, target)
print("Final Specific_h: ", s_final, sep="\ n") <---
print("Final General_h: ", g_final, sep="\ n")  <---

                                
        """)

    elif num =="5":
        print(""" 
        --- Pract 5  ---

        """)

    elif num =="6":
        print(""" 
        --- Pract 6  ---

        """)

    elif num =="7":
        print(""" 
        --- Pract 7  ---

        """)

    elif num =="8a":
        print(""" 
        --- Pract 8a  ---

        """)

    elif num =="8b":
        print(""" 
        --- Pract 8b  ---

        """)

    elif num =="9a":
        print(""" 
        --- Pract 9a  ---

        """)

    elif num =="9b":
        print(""" 
        --- Pract 9b  ---

        """)

    elif num =="10a":
        print(""" 
        --- Pract 10a  ---

        """)

    elif num =="10b":
        print(""" 
        --- Pract 10b  ---

        """)

    else:
        print("Invalid input")
        
        