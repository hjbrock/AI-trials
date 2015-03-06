# Author: Hannah Brock

import string
from decimal import *
import random

class FrequencyNode:
    def __init__(self):
        self.count = 0
        self.probability = 0.0
        self.prob_without_s_marker = 0.0
        self.next_words = { } 

    def __getitem__(self, i):
        try:
            return self.next_words[i]
        except KeyError:
            return FrequencyNode()

class NGramLangModel:
    SENTENCE = '<s>'

    def __init__(self, input_file):
        self.grams = { }
        self.PP = [ Decimal(1.0), Decimal(1.0), Decimal(1.0) ]
        self.counts = [ 0, 0, 0, 0 ]
        self.text = []
        self.words = []
        self.word_weight_total = Decimal(0.0)

        # read in words
        last_word1 = self.SENTENCE
        self.add_word(self.SENTENCE)
        last_word2 = ''
        with open(input_file, 'r') as text:
            for line in text:
                words = line.strip().split(' ')
                for word in words:
                    word, punct_break = self.clean_word(word)
                    if word != '':
                        self.add_word(word)
                        if last_word1 != '':
                            self.add_gram([last_word1, word])
                            if last_word2 != '':
                                self.add_gram([last_word2, last_word1, word])
                    if punct_break:
                        if word == '' and last_word1 != '':
                            word = last_word1
                            last_word1 = last_word2
                        if word != '':
                            self.add_gram([word, self.SENTENCE])
                        if last_word1 != '':
                            self.add_gram([last_word1, word, self.SENTENCE])
                        self.add_word(self.SENTENCE)
                        last_word1 = self.SENTENCE
                        last_word2 = word
                    elif word != '':
                        last_word2 = last_word1
                        last_word1 = word
        self.calc_probabilities()
        self.calc_perplexities()

    def calc_probabilities(self):
        """Calculate the probabilities for each word in the thre models.
           Build up a word->prob list for unigrams for use in text building
           while we do this
        """
        for w in self.grams:
            word = self.grams[w]
            word.probability = Decimal(word.count) / Decimal(self.counts[0])
            self.words.append( ( w, word.probability ) )
            self.word_weight_total += word.probability
            for w2 in word.next_words:
                word2 = word[w2]
                word2.probability = Decimal(word2.count) / Decimal(word.count)
                for w3 in word2.next_words:
                    word3 = word2[w3]
                    word3.probability = Decimal(word3.count) / Decimal(word2.count)

    def calc_perplexities(self):
        """Calculate the perplexities for the unigram, bigram, and trigram models"""
        last_word1 = ''
        last_word2 = ''
        for word in self.text:
            self.PP[0] = self.PP[0] * self.grams[word].probability
            if last_word1 != '':
                self.PP[1] = self.PP[1] * self.grams[last_word1][word].probability
                if last_word2 != '':
                    self.PP[2] = self.PP[2] * self.grams[last_word2][last_word1][word].probability
            else:
                self.PP[1] = self.PP[1] * self.grams[word].probability
                self.PP[2] = self.PP[2] * self.grams[word].probability
            last_word2 = last_word1
            last_word1 = word

        for i in range(3):
            self.PP[i] = self.PP[i]**(Decimal(-1.0/len(self.text)))

    def add_word(self, word):
        self.text.append(word)
        self.grams[word] = self.grams.get(word, FrequencyNode())
        self.grams[word].count += 1
        self.counts[0] += 1

    def add_gram(self, words):
        node = self.grams[words[0]]
        node.next_words[words[1]] = node.next_words.get(words[1], FrequencyNode())
        if len(words) == 2:
            node.next_words[words[1]].count += 1
            self.counts[1] += 1
            return
        node = node.next_words[words[1]]
        node.next_words[words[2]] = node.next_words.get(words[2], FrequencyNode())
        node.next_words[words[2]].count += 1
        self.counts[2] += 1

    @staticmethod
    def clean_word(word):
        if word == NGramLangModel.SENTENCE:
            return word
        punct_break = (word[-1:] == '.')
        word = word.translate(string.maketrans("",""), string.punctuation)
        return word.lower().strip(), punct_break

    def get_perplexity(self, N):
        return self.PP[N-1]

    def get_text_unigrams(self):
        """Create a 100-word text using the unigram model"""
        text = self.SENTENCE
        length = 0
        
        while length < 100:
            word = self.choose_word(self.words, self.word_weight_total)
            text, length = self.add_text(text, word, length)

        return text

    def get_text_bigrams(self):
        """Create a 100-word text using the bigram model"""
        text = self.SENTENCE
        word = text
        node = self.grams[word]
        length = 0
        # Now use bigrams
        while length < 100:
            words = [ ( w, node[w].probability ) for w in node.next_words ]
            if len(words) > 0:
                word = self.choose_word(words)
            else:
                word = self.choose_word(self.words, self.word_weight_total)
            node = self.grams[word]
            text, length = self.add_text(text, word, length)
        return text

    def get_text_trigrams(self):
        """Create a 100-word text using the trigram model"""
        text = self.SENTENCE
        word2 = text
        node = self.grams[word2]
        length = 0
        # Choose the second word based on bigram frequencies
        words = [ ( w, node[w].probability ) for w in node.next_words ]
        if len(words) > 0:
            word1 = self.choose_word(words)
        else:
            word1 = self.choose_word(self.words, self.word_weight_total)
        text, length = self.add_text(text, word1, length)
        # Now use trigrams
        while length < 100:
            words = [ ( w2, node[word1][w2].probability ) for w2 in node[word1].next_words ]
            word2 = word1
            node = self.grams[word2]
            if len(words) > 0:
                word1 = self.choose_word(words)
            else:
                word1 = self.choose_word(self.words, self.word_weight_total)
            text, length = self.add_text(text, word1, length)
        return text

    def add_text(self, text, word, length):
        if word == self.SENTENCE:
            text += '.'
            return text, length
        text += ' ' + word
        return text, length + 1

    def choose_word(self, words, total_weight = -1.0):
        """Choose a word from a list of words and probabilities
           words - list of tuples (word, probability)
        """
        random.shuffle(words)
        if total_weight == -1.0:
            total_weight = sum(weight for word, weight in words)
        choice = random.uniform(0, float(total_weight))
        upto = 0
        for word, weight in words:
            if upto + weight >= choice:
                return word
            upto += weight
        return words[0][0]

    def __str__(self):
        s = 'N-Grams:\n\tunigrams[' + str(self.counts[0]) + ']:'
        for n in self.grams:
            s += '\n\t\t' + n + ' - Count: ' + str(self.grams[n].count) + \
                 ' Probability: ' + str(self.grams[n].probability)
        s += '\n\tbigrams[' + str(self.counts[1]) + ']:'
        for n in self.grams:
            for w in self.grams[n].next_words:
                s += '\n\t\t' + n + ' ' + w + ' - Count: ' + str(self.grams[n][w].count) + \
                     ' Probability given w1: ' + str(self.grams[n][w].probability)
        s += '\n\ttrigrams[' + str(self.counts[2]) + ']:'
        for n in self.grams:
            for w in self.grams[n].next_words:
                for q in self.grams[n][w].next_words:
                    s += '\n\t\t' + n + ' ' + w + ' ' + q + ' - Count: ' + \
                         str(self.grams[n][w][q].count) + \
                         ' Probability given w1,w2: ' + str(self.grams[n][w][q].probability)
        return s

    def __repr__(self):
        return self.__str__()
