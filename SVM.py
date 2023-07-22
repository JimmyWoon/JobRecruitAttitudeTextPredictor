from operator import contains
import nltk
from os import name
import ResumeParser as parser
from nltk.corpus import stopwords
import pandas as pd
import string
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors

from sklearn.utils import resample
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import scale
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import confusion_matrix, plot_confusion_matrix
from sklearn.metrics import plot_confusion_matrix
from sklearn.decomposition import PCA

from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from ResumeParser import ResumeParser
from scipy.sparse import csr_matrix

class SVM:
    
    def __init__(self) -> None:
        global X_res,y_res,clf_svm
        df = pd.read_csv('latest.csv').apply(lambda x: x.astype(str).str.lower())
        
        X = df.drop('Personality',axis=1).copy()
        y = df['Personality'].copy()
        ps = PorterStemmer()
        for w in X.index:
            X["Attribute"][w] = ps.stem(X["Attribute"][w])
        X_encoded = pd.get_dummies(X,columns=['Attribute'],dtype=int)
        X_res,y_res = self.oversampling(X_encoded,y)

        clf_svm = SVC(random_state=42,C=10,gamma=10,kernel='rbf')
        clf_svm.fit(X_res,y_res)
        pass

    def RetrieveTextFromResume(self,ResumeFile):
        rp = parser.ResumeParser()
        if ResumeFile != None and (".pdf" in ResumeFile or ".mp4" in ResumeFile or ".docx" in ResumeFile or ".doc" in ResumeFile or ".txt" in ResumeFile):
            text = rp.extract_text_from_file(ResumeFile)

        # else:
            # text = rp.doc_to_text_catdoc(ResumeFile)
        return text


    def remove_stops(self,textEntered,stops):
        words = textEntered.split()
        final = []
        for word in words:
            if word not in stops:
                final.append(word)
        final = " ".join(final) 
        # final = final.translate(str.maketrans("","",string.punctuation))
        # final = " ".join(final)
        # while "  " in final:
        #     final = final.replace("  "," ")
        return final

    def clean_text(self,docs):
        stops = stopwords.words("english")
        final = []
        clean_doc = self.remove_stops(docs,stops)  
        final.append(clean_doc)
        return(" ".join(final))

    def tokenization(self,textEntered):
        words = textEntered.split()
        return words

    def stemming(self, ArrayOfText):
        ps = PorterStemmer()

        for index in range(len(ArrayOfText)):
            ArrayOfText[index] = (ps.stem(ArrayOfText[index])).lower()

        return ArrayOfText

    def oversampling(self,X_encoded,y):
        from imblearn.combine import SMOTETomek
        smk = SMOTETomek(random_state=42)
        X_res,y_res= smk.fit_resample(X_encoded,y)#used to handle imbalanced data by generating new data for minor class
        print("X_res.shape")

        print(X_res.shape)
        return X_res,y_res

    def prediction(self,text):
        personality_predicted = []
        # ps = PorterStemmer()
        model = clf_svm
        for x in range(len(text)):
            singleAttributeDataFrame  = pd.DataFrame(columns=['Attribute']) 

            singleAttributeDataFrame.loc[len(singleAttributeDataFrame.index)] = text[x]

            # singleAttributeDataFrame["Attribute"][0] = ps.stem(singleAttributeDataFrame["Attribute"][0])
            dummifiedSingleAttribute = pd.get_dummies(singleAttributeDataFrame)

            single_train, single_test = X_res.align(dummifiedSingleAttribute, join='inner', axis=1)  # inner join align with the length of the trainning dataset

            single_train = single_train.reindex(columns = X_res.columns) #add all the attribute into the testing word
            single_test = single_test.reindex(columns = X_res.columns)

            single_test = single_test.fillna(0)
            
            result = clf_svm.predict(single_test)

            personality_predicted.append(result[0])
        return personality_predicted


if __name__ == '__main__':
    model = SVM()
    test= ['testData/1.pdf','testData/2.pdf','testData/3.pdf','testData/4.pdf','testData/5.pdf','testData/6.pdf','testData/7.pdf','testData/8.pdf','testData/9.pdf','testData/10.pdf','testData/18487300.pdf','testData/Cover Letter.pdf','testData/FIS RESUME LETTER.docx','testData/Organisation reply form - KPTM.pdf','testData/Resume Aidiel.pdf','testData/Resume_Woon Sin Yee.pdf','testData/RESUME.pdf','testData/Scanned Documents (5).pdf']
    rp = ResumeParser()
    # for x in test:
    #     text = rp.extract_text_from_file(x)
    #     print(rp.extract_field(text))
    #     Cleaned_text = model.clean_text(text)
    #     tokenized = model.tokenization(Cleaned_text)
    #     stemmed = model.stemming(tokenized)
    #     result = list(set(model.prediction(stemmed)))
    #     print(result , '\n')
        
    text = model.RetrieveTextFromResume("uploads/Chai_Ming_Xuan.pdf")
    print(text)
    Cleaned_text = model.clean_text(text)
    tokenized = model.tokenization(Cleaned_text)
    stemmed = model.stemming(tokenized)
    print(len(stemmed))

    result = list(set(model.prediction(stemmed)))
    print(result , '\n')

    # ValidationText = text.translate({ord(c): None for c in string.whitespace})
    # if len(ValidationText) <=20:
    #     print("No wordd detected")
    # else:
    #     Cleaned_text = model.clean_text(text)
    #     tokenized = model.tokenization(Cleaned_text)
    #     stemmed = model.stemming(tokenized)
    #     result = list(set(model.prediction(stemmed)))
    #     print(text)
    #     print(result)
