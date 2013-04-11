from nltk import pos_tag, word_tokenize
import nltk
#Read file
sentences = ["Oracle",  "Oracle corporation",  "Zurich Real Estate Netherlands BV"]
#Tokenize
token_names= [word_tokenize(sent) for sent in sentences]
print token_names
#Tag
tagged_names = [pos_tag(item)  for item in token_names]
#Chunk
grammar = r"""
NP: {<DT|PP\$>?<JJ>*<NN>} # chunk determiner/possessive,
# adjectives and nouns
{<NNP>+} # chunk sequences of proper nouns
"""
cp = nltk.RegexpParser(grammar)
for name in tagged_names:
    print cp.parse(name)
    #cp.parse(tagged_tokens[1]).draw()
