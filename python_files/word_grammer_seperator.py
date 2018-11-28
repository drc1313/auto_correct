import urllib.request
#Opens WebPage
def webRead(URL):
    try:
        h = urllib.request.urlopen(URL)
        print("Opened "+URL)
        response = h.read()
    except:
        print("Can't open "+URL)
        return 'error'
    return response
    
#Opens and returns current library of words in all_words.txt
def getCurrWords(length):
#trys to open file. If it does not extist, it will create the file
    try:
        file=open("../word_files/word_len"+str(length)+'.txt','r')
        file.close()
    except:
        file=open("../word_files/word_len"+str(length)+'.txt','w+')
        file.close()
        
    file=open("../word_files/word_len"+str(length)+'.txt','r')
    cur_words=[]
    for line in file:
        cur_words.append(line.strip())
    file.close()
  
    return cur_words
    
#Will use webRead and open dictionary.com with the desired word to look up at the end of URL
def wordLookUp(word):
    bighunk = webRead("https://www.dictionary.com/browse/"+word)
    if bighunk!='error':
        datatype = 'misspell'
        i = bighunk.find(datatype.encode())
        print(i)
        if i==-1:
            return True
        else:
            return False
        
    return False
 
#This will open the words_add.txt which searches for words within and returns all words found in a list
def getWord2Add():
    file=open('words_add.txt')
    sep_word_list=[]
 
    for line in file:
        cur_line=line
        line_list=cur_line.split()
        
        for line in line_list:
            if line.isalpha():
                sep_word_list.append(line.lower())
                
    return sep_word_list

def wordAppend(word):
    
    file=open("../word_files/all_words.txt",'a+')
    file.write(word.lower()+'\n')
    file.close()
    file=open("../word_files/word_len"+str(len(word))+'.txt','a+')
    file.write(word.lower()+'\n')
    file.close()

def main():
    word_list=getWord2Add()
    not_words=[]
    for word in word_list:
        curr_words=getCurrWords(len(word))
        match=False
        for curr_word in curr_words:
            if curr_word == word:
                match=True
                break
        for curr_word in not_words:
             if curr_word == word:
                match=True
                break
        if match==False:
            is_word=wordLookUp(word)
            if is_word==True:
                wordAppend(word)
                curr_words=getCurrWords(len(word))
            else:
                not_words.append(word)
main()
                