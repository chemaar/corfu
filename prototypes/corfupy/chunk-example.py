    
class Unifier:    
    def __init__(self,   list_most_used_words = []):
        #Init sets
        self.my_stop_words=read_words('stop-words.txt')
        self.acronyms=read_words('acronyms.txt')
        self.stop_words_wn = stopwords.words('english') #2-Stop words from Wordnet        
        self.company_stop_words_expanded = self.expand_list_wn( self.my_stop_words)
        self.company_most_used_stop_words_expanded = self.expand_list_wn( list_most_used_words)    
        self.company_most_10_used_stop_words_expanded=Set(list_most_used_words[0:10])
     
    #Given a list of words it returns an expanded list using wordnet
    def expand_list_wn(self,  list):    
        source = Set(list)
        expanded_set = Set()
        for word in   source:
            expanded_set = expanded_set | self.create_syns_from_wn(word)
        return expanded_set |  source
    
    #Given a set of words and a name returns the name without the set of words
    def remove_set(self, set,  name): 
        token_names= word_tokenize(name)       
        filtered_token_list = [w for w in  token_names if not w.lower() in set ]
        cleaned_name = 	" ".join(["".join(filtered_token) for filtered_token in filtered_token_list])
        return cleaned_name
        
    def stop_words(self,  name):
        return self.remove_set(self.company_stop_words_expanded ,  name)
        
    def unify(self,  rawname):
       #1-Stopwords and acronyms
       stop_unified_name = self.remove_set(self.company_stop_words_expanded ,  rawname).lower()
       stop_unified_name = self.remove_set(self.stop_words_wn, stop_unified_name).lower()       
       stop_unified_name = self.remove_set(self.company_most_used_stop_words_expanded,  stop_unified_name).lower()       
       stop_unified_name = self.remove_set(self.acronyms,  stop_unified_name).lower()       
       #2-Length words #FIXME: it can be optimized
       token_names= word_tokenize(stop_unified_name)     
       filtered_token_list = [w for w in  token_names if len(w) >2]
       len_cleaned_name = " ".join(["".join(filtered_token) for filtered_token in filtered_token_list])
       #3-If word exists then Spellchecker
       spelled_words = []
       for word  in word_tokenize(len_cleaned_name) :
        syns = wn.synsets(word) 
        spelled_words.append(word)
      #  if len(syns)>0:
      #      #spelled_words.append(correct(word))     
        #else:
            #spelled_words.append(word)
       spelled_name = " ".join(spelled_words)
       #4-Speech tagger
       #5-Remove non-nouns
       #6-Geonames
       unified_name = spelled_name.lower()
       return unified_name


