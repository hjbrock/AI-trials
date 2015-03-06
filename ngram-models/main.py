# Author: Hannah Brock

import sys
from ngram_model import NGramLangModel

if len(sys.argv) < 2:
    print('Input file is required')
    exit(1)

infile = sys.argv[1]
gramfile = 'grams.txt'
text_postfix = '_texts.txt'

print('Creating model...')
model = NGramLangModel(infile)
with open(gramfile, 'w') as out:
    out.write(str(model))
for i in range(3):
    print('Perplexity of ' + str(i+1) + ' grams: ' + str(model.get_perplexity(i+1)))

print('Creating trigram texts...')
with open('trigram' + text_postfix, 'w') as out:
    for i in range(20):
        out.write(model.get_text_trigrams())
        out.write('\n\n')

print('Creating bigram texts...')
with open('bigram' + text_postfix, 'w') as out:
    for i in range(20):
        out.write(model.get_text_bigrams())
        out.write('\n\n')

print('Creating unigram texts...')
with open('unigram' + text_postfix, 'w') as out:
    for i in range(20):
        out.write(model.get_text_unigrams())
        out.write('\n\n')
