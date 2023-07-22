import datetime
from operator import contains
import string
from tkinter.font import names
from pdfminer.high_level import extract_text
import nltk
import docx2txt
import re
import subprocess
import requests
from nltk.corpus import stopwords
import re
import os

import aspose.words as aw
from win32com import client as wc
import spacy
from collections import Counter
#No doc files is allows
# PHONE_REG = re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]')
# EMAIL_REG = re.compile(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+')
EMAIL_REG = re.compile(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.{0,1}[a-z]+\.[a-z]+')

# you may read the database from a csv file or some other database
SKILLS_DB = [
    'machine learning',
    'data science',
    'python',
    'word',
    'excel',
    'english',
    'chinese',
    'cantonese',
    'bahasa melayu',
    'matlab',
    'mat lab',
    'ruby',
    'r',
    'angular',
    'c#',
    'c++',
    'vb.net',
    'css',
    'html',
    'java',
    '.net',
    'php',
    'database',
    'network configuration',
    'mysql',
    'flutter',
    'android studio',
    'sap',
    'rsa',
    'oracle',
    'quicken',
    'kronos',
    'inovisworks',
    'citrix',
    'peoplesoft',
    'onyx',
    'sas',
    'sql',
    'fortran',
    'vba',
    'jd edwards',
    'quickbooks',
    'microsoft dynamics ax',
    'rfms',
    'aws',
    'apache ignite',
    'autocad',
    'revit',
    'data analysis',
    'machine learning',
    'project management',
    'leadership'
]

RESERVED_WORDS = [
    'üniversity',
    'university',
    'college',
    'kolej',
    'academy',
    'faculty',
    'institute',
    'faculdades',
    'Schola',
    'schule',
    'lise',
    'lyceum',
    'lycee',
    'polytechnic',
    'okul',
    'school',
    'institute',
    'institut'
]
education_level = [
    'phd',
    'ph.d.',
    'doctor of philosophy',
    'master',
    'm.sc.',
    'bachelor',
    'bachelors',   
    'hons',
    'b.e.',
    'b.',
    'bsc',
    'b.sc.',
    'degree',
    'diploma',
    'foundation',
    'certificate',
    'spm'
]



class ResumeParser:
    def __init__(self) -> None:
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('maxent_ne_chunker')
        nltk.download('words')        
        nltk.download('stopwords')
        pass

    def extract_text_from_file(self,path):
        if '.pdf' in path:
            return extract_text(path)
        elif '.docx' in path:
            txt = docx2txt.process(path)
            if txt:
                return txt.replace('\t', ' ')
            return None
        elif '.txt' in path:
            myfile = open(path, "rt")
            contents = myfile.read()         # read the entire file to string
            myfile.close()                   # close the file
            return contents
        #already handle doc format by converting doc to docx in app.py when upload
        # elif '.doc' in path:
        #     doc = aw.Document(path)
        #     filename = path.split('/')[-1]
        #     filename = filename.split('.')[0]
        #     docx_path = 'uploads/'+filename+'.docx'
        #     doc.save(docx_path)

        #     txt = docx2txt.process(docx_path)
        #     if txt:
        #         return txt.replace('\t', ' ')
        #     return None
        
    def extract_names(self,txt):
        person_names=[]
        for sent in nltk.sent_tokenize(txt):
            for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
                if hasattr(chunk, 'label') and chunk.label() == 'PERSON':
                    person_names.append(
                        ' '.join(chunk_leave[0] for chunk_leave in chunk.leaves())
                    )
        return person_names

    def doc_to_text_catdoc(self,file_path):
        try:
            process = subprocess.Popen(  # noqa: S607,S603
                ['catdoc', '-w', file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )
        except (
            FileNotFoundError,
            ValueError,
            subprocess.TimeoutExpired,
            subprocess.SubprocessError,
        ) as err:
            return (None, str(err))
        else:
            stdout, stderr = process.communicate()
    
        return (stdout.strip(), stderr.strip())
    
 
    def extract_phone_number(self, resume_text):
        # regex = r'\b\+{0,1}\({0,1}\+{0,1}\d{2,3}[-.]?\d{3}[-.]?\d{4}\b'
        # phone = re.findall(regex,resume_text)


        phone = re.findall(r"\+{0,1}\({0,1}\+{0,1}[\d]{0,1}\s{0,1}[\d]{0,1}\s{0,1}[\d]{0,1}\s{0,1}[\d]{0,1}\s{0,1}[\d]{0,1}\s{0,1}[\d]{0,1}\s{0,1}[\d]{0,1}\s{0,1}[\d]{0,1}\s{0,1}[\d]{0,1}\s{0,1}[\d]{0,1}\s{0,1}\s{0,5}\t{0,4}-{0,1}\s{0,5}\t{0,4}[\d]{0,1}\s{0,1}[\d]{0,1}\s{0,1}[\d]{0,1}\s{0,1}[\d]{0,1}\s{0,1}[\d]{0,1}\s{0,1}[\d]{0,1}\s{0,1}[\d]{0,1}\s{0,1}[\d]{0,1}\s{0,1}[\d]{0,1}\s{0,1}[\d]{0,1}\s{0,1}-{0,1}\s{0,5}\t{0,4}[\d]{0,1}\s{0,1}[\d]{0,1}\s{0,1}[\d]{0,1}\s{0,1}[\d]{0,1}\s{0,1}[\d]{0,1}\s{0,1}[\d]{0,1}\s{0,1}[\d]{0,1}\s{0,1}[\d]{0,1}\s{0,1}[\d]{0,1}\s{0,1}[\d]{0,1}\s{0,1}", resume_text)
        # phone = re.findall(r"\+{0,1}\({0,1}\+{0,1}[\d]{2,4}\s{0,5}\t{0,4}-{0,1}\s{0,5}\t{0,4}[\d]{3,}\s{0,5}\t{0,4}[\d]{4,}", resume_text)

        # phone = re.findall(PHONE_REG, resume_text)
        # print(phone)


        if phone:
            # print('list of phone in function: ', phone)

            for phn in phone:
                number = ''.join(phn)
                number = number.replace("\n", "")
                if len(number) >= 9 and len(number) < 25:
                    if '+' in number or '(' in number or '-' in number:
                        return number
            # if resume_text.find(number) >= 0 and len(number) < 16:
            #     return (number)
        # return None
        else:
            return None
        return ''.join(phone[0])

    def extract_emails(self,resume_text):
        return re.findall(EMAIL_REG, resume_text)


    def extract_skills(self,input_text):
        stop_words = set(nltk.corpus.stopwords.words('english'))
        word_tokens = nltk.tokenize.word_tokenize(input_text)
    
        # remove the stop words
        filtered_tokens = [w for w in word_tokens if w not in stop_words]
    
        # remove the punctuation
        filtered_tokens = [w for w in word_tokens if w.isalpha()]
    
        # generate bigrams and trigrams (such as artificial intelligence)
        bigrams_trigrams = list(map(' '.join, nltk.everygrams(filtered_tokens, 2, 3)))
    
        # we create a set to keep the results in.
        found_skills = set()
    
        # we search for each token in our skills database
        for token in filtered_tokens:
            if token.lower() in SKILLS_DB:
                found_skills.add(token)
    
        # we search for each bigram and trigram in our skills database
        for ngram in bigrams_trigrams:
            if ngram.lower() in SKILLS_DB:
                found_skills.add(ngram)

        capitalized_set = {elem.capitalize() for elem in found_skills}
        return capitalized_set

    def extract_educationlevel(self,input_text):
        # stop_words = set(nltk.corpus.stopwords.words('english'))
        # word_tokens = nltk.tokenize.word_tokenize(input_text)
    
        # # remove the stop words
        # filtered_tokens = [w for w in word_tokens if w not in stop_words]
    
        # # remove the punctuation
        # filtered_tokens = [w for w in word_tokens if w.isalpha()]
    
        # # generate bigrams and trigrams (such as artificial intelligence)
        # bigrams_trigrams = list(map(' '.join, nltk.everygrams(filtered_tokens, 2, 3)))
    
        # # we create a set to keep the results in.
        found_educationlevel = set()
    
        # # we search for each token in our skills database
        # # for token in filtered_tokens:
        # #     if token.lower() in education_level:
        # #         found_educationlevel.add(token)
        # filtered_tokens_lower = []
        # for temp in filtered_tokens:
        #     filtered_tokens_lower.append(temp.lower())
        words = self.clean_text(input_text)
        words = words.lower() 
        # sorted_string = ' '.join(sorted(words.split(), key=lambda x: education_level.index(x)))
        
        # words = words.split()

        for x in education_level:

            if words.find(x) != -1:
                result = x
                if x == 'b.':
                    result = 'bachelor'
                elif x == 'm.sc.':
                    result = 'master'
                elif x == 'b.e.':
                    result = 'bachelor'
                elif x == 'bsc':
                    result = 'bachelor'
                elif x == 'b.sc.':
                    result = 'bachelor'
                found_educationlevel.add(result.title())
                break 

        # we search for each bigram and trigram in our skills database
        # for ngram in bigrams_trigrams:
        #     if ngram.lower() in education_level:
        #         found_educationlevel.add(ngram)
        #---------------------------------------------------------------------------------
        # bigrams_trigrams_lower = []
        # for temp in bigrams_trigrams:
        #     bigrams_trigrams_lower.append(temp.lower())

        # for x in education_level:
        #     # for ngram in bigrams_trigrams:
        #     if x in bigrams_trigrams_lower:
        #         found_educationlevel.add(x.capitalize())
        #         break 
        return found_educationlevel


    # def skill_exists(self, skill):
    #     url = f'https://api.apilayer.com/skills?q={skill}&amp;count=1'
    #     headers = {'apikey': 'YOUR API KEY'}
    #     response = requests.request('GET', url, headers=headers)
    #     result = response.json()
    
    #     if response.status_code == 200:
    #         return len(result) > 0 and result[0].lower() == skill.lower()
    #     raise Exception(result.get('message'))
    # #useless --------------------------------------------
    # def extract_skills2(self, input_text): 
    #     stop_words = set(nltk.corpus.stopwords.words('english'))
    #     word_tokens = nltk.tokenize.word_tokenize(input_text)
    
    #     # remove the stop words
    #     filtered_tokens = [w for w in word_tokens if w not in stop_words]
    
    #     # remove the punctuation
    #     filtered_tokens = [w for w in word_tokens if w.isalpha()]
    
    #     # generate bigrams and trigrams (such as artificial intelligence)
    #     bigrams_trigrams = list(map(' '.join, nltk.everygrams(filtered_tokens, 2, 3)))
    
    #     # we create a set to keep the results in.
    #     found_skills = set()
    
    #     # we search for each token in our skills database
    #     for token in filtered_tokens:
    #         if self.skill_exists(token.lower()):
    #             found_skills.add(token)
    
    #     # we search for each bigram and trigram in our skills database
    #     for ngram in bigrams_trigrams:
    #         if self.skill_exists(ngram.lower()):
    #             found_skills.add(ngram)
    
    #     return found_skills

    def extract_education(self,input_text):

        # organizations = []
    
        # # first get all the organization names using nltk
        # for sent in nltk.sent_tokenize(input_text):
        #     for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
        #         if hasattr(chunk, 'label') and chunk.label() == 'ORGANIZATION':
        #             organizations.append(' '.join(c[0] for c in chunk.leaves()))


        # # we search for each bigram and trigram for reserved words
        # # (college, university etc...)
        # # for org in organizations:
        # #     for word in RESERVED_WORDS:
        # #         if org.lower().find(word) >= 0:
        # #             education.add(org) 
        # # for word in RESERVED_WORDS:
        # #     if word in organizations.lower():
        # #         education.add()
        # # print('organizations in method: ')

        # # print(organizations)

        # education = set()

        # for org in organizations:
        #     for word in RESERVED_WORDS:
        #         if org.lower().find(word) >= 0:
        #             education.add(org) 
        #             break

        words = self.clean_text(input_text)
        words = words.lower() 
        # Regular expression pattern to match university names
        university_pattern = r'(university\s?\w+|\w+\suniversity)'

        # Search for university names in the text
        matches = re.findall(university_pattern, words)

        if bool(matches):

            # Count the occurrences of each element
            counted = Counter(matches)

            # Get the element(s) frequency which has the highest count 
            most_common = counted.most_common(1)[0][1]
            return (matches[0]).title()
            # if most_common == 1:
            #     return (matches[0]).title()
            # else:
            #     return (counted.most_common(1)[0][0]).title()
        else:
            return '-'




    def remove_stops(self,textEntered,stops):
        words = textEntered.split()
        final = []
        for word in words:
            if word not in stops:
                final.append(word)
        final = " ".join(final) 
        return final

    def clean_text(self,docs):
        stops = stopwords.words("english")
        final = []
        clean_doc = self.remove_stops(docs,stops)  
        final.append(clean_doc)
        return(" ".join(final))

    def temp_field(self,input_text):
        edu_keywords = ["university", "college", "school", "degree", "bachelor", "master", "phd"]

        # Extract named entities from resume text
        nlp = spacy.load("en_core_web_sm")

        doc = nlp(input_text)
        edu_entities = [ent.text for ent in doc.ents if ent.label_ in ["ORG", "EDU"] and any(keyword in ent.text.lower() for keyword in edu_keywords)]

        # Use dependency parsing to analyze relationships between named entities and other parts of the sentence
        education_field = None
        for token in doc:
            if token.dep_ == "nsubj" and any(entity in token.text.lower() for entity in edu_entities):
                for child in token.children:
                    if child.dep_ == "ROOT" and child.lemma_ in ["study", "graduate"]:
                        education_field = token.text

        print(education_field)

    def extract_field(self, input_text):
        words = self.clean_text(input_text)
        words = words.lower() 
        words = words.split() #--------
        for index, word in enumerate(words):
            for level in education_level:
                if level == word:
                    if word != 'spm':
                        # print(word)
                        # print(index)
                        result = (" ".join(words[index-5:index+5]))
                        if any(x in result for x in ['business','accounting','auditing','taxation','economic','finance','marketing','management','salesman','sales']):
                            return "Finance"
                        elif  any(x in result for x in ['property','estate','properties']):
                            return "Real Estate"
                        elif  any(x in result for x in ['carpentry','wood','woodworker']):
                            return "Carpenter"

                        elif  any(x in result for x in ['doctor','medical','science','surgeon','physiotherapy','dentist','nutritionist','scientist','biologist','chemist','pharmacy','biochemist','nursing','health','mental']):
                            if 'science' in result:
                                if 'computer' in result:
                                    return "Information Technology"
                                elif 'engineering' in result:
                                    return 'Engineering'
                            return "Medical"
                        elif  any(x in result for x in ['engineer','engineering','mechanical','electronic','electrical','maintenance']):
                            return "Engineering"
                        elif  any(x in result for x in ['human','clerk']):
                            return "Human Resource"
                        elif  any(x in result for x in ['teaching','lecturer']):
                            return "Education"
                        elif  any(x in result for x in ['culinary','baking','food','pastry']):
                            return "Culinary"
                        elif  any(x in result for x in ['public','relation','mass','communication','language','linguistics','linguistic','melayu','korean','english','japanese','spanish','chinese']):
                            return "Public Relation"
                        elif  any(x in result for x in ['hotel','cashier','waiter','customer', 'service']):
                            return "Service Industry"
                        elif  any(x in result for x in ['law']):
                            return "Law"
                        elif  any(x in result for x in ['fashion','designer','design','art']):
                            return "Art"
                        elif any(x in result for x in ['computer','computing','software','game','cybersecurity','data','technology','information','artificial intelligence','ai','it']):
                            return "Information Technology"
                        else:
                            continue

        words = " ".join(words)
        if 'information technology' in words or 'computing' in words or 'computer' in words:
            return "Information Technology"
        elif 'public relation' in words:
            return "Public Relation"
        elif 'finance' in words or 'banking' in words or 'business' in words or 'marketing' in words: 
            return "Finance"
        elif 'designer' in words:
            return "Art"
        elif 'chef' in words:
            return "Chef"
        elif 'agriculture' in words:
            return "Agriculture"
        elif 'accountant' in words:
            return "Accountant"
        elif 'medical' in words or 'health science' in words:
            return "Medical"
        elif 'human resource' in words:
            return "Human Resource"
        elif 'techer' in words:
            return "Teacher"
        return '-'

    def findCGPA(self, input_text):
        words = self.clean_text(input_text)
        words = words.lower()


        if (words.find('cgpa')) != -1:
            index = words.index('cgpa')
            # extract the text around the word
            start_index = index - 10  # 10 characters before the word
            end_index = index + len('cgpa') + 10  # len(word) characters after the word, plus 10 more
            text_around_word = words[start_index:end_index]

            temp = re.findall("\d+\.\d+", text_around_word)

            if len(temp) > 0 :
                for x in temp:
                    if float(x) <= 4.0 and float(x) > 0:
                        return x
                return "-"
            else:
                return '-'
        elif (words.find('gpa')) != -1 :

            index = words.index('gpa')
            # extract the text around the word
            start_index = index - 10  # 10 characters before the word
            end_index = index + len('gpa') + 10  # len(word) characters after the word, plus 10 more
            text_around_word = words[start_index:end_index]


            temp = re.findall("\d+\.\d+", text_around_word)

            if len(temp) > 0 :
                for x in temp:
                    if float(x) <= 4.0 and float(x) > 0:
                        return x
                return "-"
            else:
                return "-"
        else:
            temp = re.findall("\d+\.\d+", words)

            if len(temp) > 0 :
                for x in temp:
                    if float(x) <= 4.0 and float(x) > 0:
                        return x
                return "-"
            else:
                return "-"
        return "-"

    def findName(self,input_text,file_type):
        if file_type == '.mp4':
            # words = input_text.split()
            return (self.extract_names(input_text))[0]
        else:
            words = input_text.splitlines()
            for x in words:
                number_of_space = x.count(" ") #check number of space if the no. of space many meaning the person name got spacing between the alphabet so used other method
                if number_of_space > 5:
                    checkName = x.split()
                    if len(checkName) >= 6: # W o o n e n g c h u n 

                        x = re. split(r'\s{2,}', x)
                        x[:] = [i.replace(" ","") for i in x]

                        result = " ".join(x)

                        result = result.replace("\n", "")
                        return result.upper()
                else:
                    x = x.lower()
                    if 'curriculum' not in x and 'resume' not in x and 'bibography' not in x:
                        checkName = x.split()
                        if len(checkName) >= 2 and len(checkName) <=6:
                            return x.upper()        
            return words[0].upper()

    def findName_spacy(self, input_text,file_type):
        if file_type == '.mp4':
            # words = input_text.split()
            return (self.extract_names(input_text))[0]
        else:
            nlp = spacy.load("en_core_web_sm")
            doc = nlp(input_text)
            person_names = [ent.text for ent in doc.ents if ent.label_ == 'PERSON']
            # for x in person_names:
            #     print(x)
            remove_new_line = (person_names[0]).replace("\n", "")
            remove_additional_space = remove_new_line.rstrip()
            return (remove_additional_space.replace("  ",""))
            # words = input_text.splitlines()   
            # for x in words:
            #     number_of_space = x.count(" ") #check number of space if the no. of space many meaning the person name got spacing between the alphabet so used other method
            #     if number_of_space > 5:
            #         checkName = x.split()
            #         if len(checkName) >= 6: # W o o n e n g c h u n 

            #             x = re. split(r'\s{2,}', x)
            #             x[:] = [i.replace(" ","") for i in x]

            #             result = " ".join(x)

            #             result = result.replace("\n", "")
            #             return result.upper()
            #     else:
            #         x = x.lower()
            #         if 'curriculum' not in x and 'resume' not in x and 'bibography' not in x:
            #             checkName = x.split()
            #             if len(checkName) >= 2 and len(checkName) <=6:
            #                 return x.upper()        
            # return words[0].upper()
if __name__ == '__main__':

    # test= ['testData/1.pdf','testData/2.pdf','testData/3.pdf','testData/4.pdf','testData/5.pdf','testData/6.pdf','testData/7.pdf','testData/8.pdf','testData/9.pdf','testData/10.pdf','testData/18487300.pdf','testData/Cover Letter.pdf','testData/FIS RESUME LETTER.docx','testData/Organisation reply form - KPTM.pdf','testData/Resume Aidiel.pdf','testData/Resume_Woon Sin Yee.pdf','testData/RESUME.pdf','testData/Scanned Documents (5).pdf']
    rp = ResumeParser()
    # for x in test:
    #     text = rp.extract_text_from_file(x)
    #     print(rp.findCGPA(text))
    #     print(rp.findName(text))
    #     print("---------------------------")

    text = rp.extract_text_from_file("fullCV (18).pdf")
    # text = rp.extract_text_from_file('Challs hr resume.docx')

    ValidationText = text.translate({ord(c): None for c in string.whitespace})
    if len(ValidationText) <=20:
        print("No word detected")
    else:
        names = rp.extract_names(text)
        phone_number = rp.extract_phone_number(text)
        emails = rp.extract_emails(text)
        emails = [i for i in emails if '@gmail.com' or '@yahoo.com' or '@hotmail.com' or 'edu.my' or '.my' in i]
        skills = rp.extract_skills(text)
        education_information = rp.extract_education(text)
        educationle = rp.extract_educationlevel(text)

        # insituition = rp.extract_education2(text)
        # education_information = [x for x in education_information if len(x) > 10]
        # education_information = list(education_information)
        # for x in education_information:
        #     total.append(len(x))
        print(text)
        print("---------------------------")
        print(rp.findCGPA(text))
        print("findName: ")
        print(rp.findName(text,'.docx'))
        
        # print("findName with spacy: ")
        # print(rp.findName_spacy(text,'.docx'))

        if names:
            print(f'the list of extract_names: {names}')

        print(f'the list of phone: {phone_number}')

        print(f'the list of emails: {emails}')
        print(f'the list of skills: {",".join(skills)}')
        print(f'the list of education: {education_information}')
        # print(f'the len of education: {total}')

        print(f'the list of educationlevel: {educationle}')
        print(rp.extract_field(text) + '\n')
        print("---------------------------")

        # rp.temp_field(text)
