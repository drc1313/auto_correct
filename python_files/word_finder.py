'''
File that holds all functions used by the program
In short, functions work together to take misspelled word and compare 
them to correct ones giving points to matches
word_finder.py
Dillon/Scott
12/3/18
'''
#Opens files given and returns list of words inside 
def file_open(file_name):
    file=open(file_name)
    word_list=[]
    for line in file:
        word_list+=line.split()
    return word_list

#Clears word of things that are not letters
def word_clear(word):
    new_char_list=[]
    char_list=list(word)
    for char in char_list:
        if char.isalpha():
            new_char_list.append(char)
        else:
            break
    result=''.join(new_char_list)
    return result

#Gives a point to a word in the dictionary
def give_points(word_dict,lib_word):
    if lib_word in word_dict:
        word_dict[lib_word]+=1
    else:
        word_dict[lib_word]=1
    return word_dict

#Tallys up the score of word given in parameter
#Adds points to words with similar starts/ends
#Removes point to longer words that may skew results
#Returns the high score certain construction of word 
#EX. word compared to world. (wor0d) replaces (wo0rd) as highscore to (world) because (wor0d) gets 4 pts and (wo0rd) gets 3pts
def get_word_score(lib_word,word_dict,word,word_high_score):
    if word_dict.get(lib_word) is not None:
        if lib_word[0]==word[0]:
            word_dict[lib_word]+=1
            if lib_word[-1]==word[-1]:
                word_dict[lib_word]+=1
        if len(lib_word)-1>len(word):
            word_dict[lib_word]-=1
        word_score=word_dict.get(lib_word)
        word_dict[lib_word]=0
        if word_score>word_high_score:
            word_high_score=word_score
        return word_high_score

#Moves letters around and reconstructs misspelled word to match correct spelled word 
#returns dictionary containing newly gained points and newly constructed word
def scatter_search(word,new_word,lib_word,trials,word_dict):
    curr_char=lib_word[trials]
    if curr_char==new_word[trials+1]:
        discard_char=new_word[trials]
        new_word=new_word[0:trials]+new_word[trials+1]+discard_char+new_word[trials+2:]
        word_dict=give_points(word_dict,lib_word)
    return word_dict,new_word

#Searches files under the length of misspelled for correct word depending on subt_amt value
#Removes a letter from misspelled word at every index one at a time and compares to correct words
#Calls for scatter_search if no match is found at same indexes to broaden search
#This will only search in the file that contains words one letter less then the misspelled word
#returns dictionary containing newly gained points
def search_down(subt_amt,word,lib_word,word_dict):
    word_high_score=0
    word_score=0
    if subt_amt==1:
        word_len=len(word)-subt_amt
        for num in range(len(word)):
            new_word=list(word)
            del new_word[num]
            new_word=''.join(new_word)
            trials=0
            while trials!=word_len:
                if lib_word[trials]==new_word[trials]:
                    word_dict=give_points(word_dict,lib_word)
                elif trials!=word_len-1:
                    word_dict,new_word=scatter_search(word,new_word,lib_word,trials,word_dict)
                trials+=1
            if word_dict.get(lib_word) is not None:
                word_high_score=get_word_score(lib_word,word_dict,word,word_high_score)
        word_dict[lib_word]=word_high_score
        return word_dict

#similar to search_down but will instead add zeros to misspelled words to match correct word length
#Zeros will shuffle around indexes to get a better match 
#This will search files that are one or two letters more then the misspelled word
#returns dictionary containing newly gained points
def search_up(add_amt,word,lib_word,word_dict):
    word_high_score=0
    word_score=0
    if add_amt==1:
        word_len=len(word)+add_amt
        for num in range(len(word)):
            new_word=list(word)
            new_word.insert(num,'0')
            new_word=''.join(new_word)
            trials=0
            while trials!=word_len:
                if lib_word[trials]==new_word[trials]:
                    word_dict=give_points(word_dict,lib_word)
                elif trials!=word_len-1:
                    word_dict,new_word=scatter_search(word,new_word,lib_word,trials,word_dict)
                trials+=1 
            if word_dict.get(lib_word) is not None:
                word_high_score=get_word_score(lib_word,word_dict,word,word_high_score)
        word_dict[lib_word]=word_high_score
        return word_dict
        
    if add_amt==2:
        word_len=len(word)+add_amt
        skip_one=0
        skip_two=0
        while skip_one!=word_len:
            new_word=list(word)
            if skip_two==word_len:
                skip_one+=1
                skip_two=skip_one
            skip_two+=1
            new_word.insert(skip_one,'0')
            new_word.insert(skip_two,'0')
            new_word=''.join(new_word)
            trials=0
            while trials!=word_len:
                if lib_word[trials]==new_word[trials]:
                    word_dict=give_points(word_dict,lib_word)
                elif trials!=word_len-1:
                    word_dict,new_word=scatter_search(word,new_word,lib_word,trials,word_dict)
                trials+=1 
            if word_dict.get(lib_word) is not None:
                word_high_score=get_word_score(lib_word,word_dict,word,word_high_score)
        word_dict[lib_word]=word_high_score
        return word_dict

#Creates the dictionary and opens files the are close length to misspelled word
#Returns a list containing 15 word suggestions 
def word_suggest(word):
    word_len=len(word)-1
    word_end=word_len+4
    word_dict={}
    while word_len != word_end:
        word_lib_list=file_open("../word_files/word_len"+str(word_len)+'.txt')
        for lib_word in word_lib_list:
            word_high_score=0
            word_score=0
            if (len(word)+1)==word_len:
                word_dict=search_up(1,word,lib_word,word_dict)
            elif (len(word)+2)==word_len:
                word_dict=search_up(2,word,lib_word,word_dict)
            elif len(word)==word_len:
                new_word=word
                trials=0
                while trials!=word_len:
                    if lib_word[trials]==new_word[trials]:
                        word_dict=give_points(word_dict,lib_word)
                    elif trials!=word_len-1:
                         word_dict,new_word=scatter_search(word,new_word,lib_word,trials,word_dict)    
                    trials+=1
                if word_dict.get(lib_word) is not None:
                        word_high_score=get_word_score(lib_word,word_dict,word,word_high_score)
                word_dict[lib_word]=word_high_score
            else:
                word_dict=search_down(1,word,lib_word,word_dict)
        word_len+=1
    top_list=sorted(word_dict, key=word_dict.get, reverse=True)
    return top_list[0:15]



   