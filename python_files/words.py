from random import randrange
import urllib.request

   
def fileOpen(file_name):
    file=open(file_name)
    word_list=[]
    for line in file:
        word_list+=line.split()
    return word_list
    
def wordClear(word):
    new_char_list=[]
    char_list=list(word)
    for char in char_list:
        if char.isalpha():
            new_char_list.append(char)
        else:
            break
    result=''.join(new_char_list)
    return result
    
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

def scatter_search(word,new_word,lib_word,trials,word_dict):
    curr_char=lib_word[trials]
    
    if curr_char==new_word[trials+1]:
        discard_char=new_word[trials]
        new_word=new_word[0:trials]+new_word[trials+1]+discard_char+new_word[trials+2:]
        
        if lib_word in word_dict:
            word_dict[lib_word]+=1
            
        else:
            word_dict[lib_word]=1
            
    return word_dict
    
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
                    if lib_word in word_dict:
                        word_dict[lib_word]+=1
                        
                    #else:
                        #word_dict[lib_word]=1
                        
                elif trials!=word_len-1:
                    word_dict=scatter_search(word,new_word,lib_word,trials,word_dict)
                    
                trials+=1
            if word_dict.get(lib_word) is not None:
                word_high_score=get_word_score(lib_word,word_dict,word,word_high_score)
                
        word_dict[lib_word]=word_high_score
        return word_dict
    
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
                    if lib_word in word_dict:
                        word_dict[lib_word]+=1
                    else:
                        word_dict[lib_word]=1
                elif trials!=word_len-1:
                    word_dict=scatter_search(word,new_word,lib_word,trials,word_dict)
                trials+=1 
            if word_dict.get(lib_word) is not None:
                word_high_score=get_word_score(lib_word,word_dict,word,word_high_score)
                    
        word_dict[lib_word]=word_high_score
        return word_dict
        
    if add_amt==2:
        
        word_len=len(word)+add_amt
        skip_one=0
        skip_two=0
        
        #for num in range(len(word)):
        while skip_one!=word_len:
            new_word=list(word)
            
            if skip_two==word_len:
                skip_one+=1
                skip_two=skip_one
            skip_two+=1
            new_word.insert(skip_one,'0')
            new_word.insert(skip_two,'0')
            #print(new_word)
            new_word=''.join(new_word)
            
            trials=0
            while trials!=word_len:
                if lib_word[trials]==new_word[trials]:
                    if lib_word in word_dict:
                        word_dict[lib_word]+=1
                        
                    else:
                        word_dict[lib_word]=1
                elif trials!=word_len-1:
                    word_dict=scatter_search(word,new_word,lib_word,trials,word_dict)
                trials+=1 
            if word_dict.get(lib_word) is not None:
                word_high_score=get_word_score(lib_word,word_dict,word,word_high_score)
                    
        word_dict[lib_word]=word_high_score
        return word_dict
                
def word_Suggest(word):
    word_len=len(word)-1
    word_end=word_len+4
    word_dict={}
    while word_len != word_end:
        word_lib_list=fileOpen("../word_files/word_len"+str(word_len)+'.txt')
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
                        if lib_word in word_dict:
                            word_dict[lib_word]+=1
                           
                        else:
                            word_dict[lib_word]=1
                           
                    elif trials!=word_len-1:
                        
                         word_dict=scatter_search(word,new_word,lib_word,trials,word_dict)    
                    trials+=1
                if word_dict.get(lib_word) is not None:
                        word_high_score=get_word_score(lib_word,word_dict,word,word_high_score)
                word_dict[lib_word]=word_high_score
            else:
                word_dict=search_down(1,word,lib_word,word_dict)
        word_len+=1
   
    top_list=sorted(word_dict, key=word_dict.get, reverse=True)
    return top_list[0:15]

def main():
    newList=[]
    set_text_list=fileOpen('set.txt')
    for word in set_text_list:
        d=wordClear(word)
        if len(d) >0:
            newList.append(d)
    print(newList)
    match=False
    for word in newList:
        match=False
        word_len=len(word)
        library_words_list=fileOpen("../word_files/word_len"+str(word_len)+'.txt')
        for lib_word in library_words_list:
            if word.lower()==lib_word:
                match=True
        print(word,match)
        if match==False:
            word_dict=word_Suggest(word)
            print(word_dict)
#main()


   