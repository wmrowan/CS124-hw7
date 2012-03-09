#!/usr/bin/python
import re
import pdb

## Simple representation of a tagged word
class Word:
    def __init__(self, w):
        match = re.match("(?P<ch>.+)_(?P=ch)", w)
        if match:
            self.word = match.group(1)
            self.tag = "PUNCT"
        else:
            (self.word, self.tag) = w.split("_")

    def pos(self,t):
        return self.tag == t

    def isNoun(self):
        return re.match("NN", self.tag) or re.match("PRP", self.tag)

    def isAdjective(self):
        return self.tag == "JJ"

    def isAdverb(self):
        return re.match("RB", self.tag)
        
    def isVerb(self):
        return re.match("VB", self.tag)

    def __repr__(self):
        return str(self)
    def __str__(self):
        return "{"+self.word+":"+self.tag+"}"


## Sentence reordering rules

def swap(s, i, j):
    tmp = s[i]
    s[i] = s[j]
    s[j] = tmp

# In English, adjectives come before the noun they modify
def AdjectiveBeforeNoun(s):
    for i in xrange(0, len(s)-1):
        if s[i].isNoun() and s[i+1].isAdjective():
            swap(s, i, i+1)

def AdverbAfterVerb(s):
    for i in xrange(0, len(s)-1):
        if s[i].isAdverb() and s[i+1].isVerb():
            swap(s, i, i+1)

def DOAferVerb(s):
    for i in xrange(0, len(s)-2):
        if s[i].isNoun() and s[i+1].isNoun() and s[i+2].isVerb():
            swap(s, i+1, i+2)

def InfinitiveVerbs(s):
    for i in xrange(0, len(s)-1):
        if s[i].pos("IN") and s[i+1].pos("VB"):
            s[i] = Word("to_TO")
    for i in xrange(0, len(s)-1):
        if s[i].isVerb() and s[i+1].pos("VB"):
            s.insert(i+1, Word("to_TO"))

def SwitchPluralNouns(s):
    for i in xrange(0, len(s)-1):
        if s[i].pos("NNS") and s[i+1].pos("NNS"):
            swap(s, i, i+1)

def reorder(s):
    AdjectiveBeforeNoun(s)
    AdverbAfterVerb(s)
    DOAferVerb(s)
    InfinitiveVerbs(s)
    SwitchPluralNouns(s)
    return s


## For producing final output

def collapseSentence(sentence):
    return " ".join(map(lambda x: x.word, sentence))

def collapse(sentences):
    return ".".join(map(collapseSentence, sentences))+"."


## For parsing input

def isValidWord(word):
    return not (word == "" )#or re.match("(?P<ch>.+)_(?P=ch)", word))

def transformSentence(sentence):
    words = sentence.split(" ")
    words = map(lambda x: x.strip(), words)
    words = filter(isValidWord, words)
    words = map(Word, words)
    return words

def transformText(txt):
    sentences = txt.split("._.")
    sentences = map(transformSentence, sentences)
    sentences = filter(lambda x: x != [], sentences)
    return sentences

def main():
    f = open("english-tagged.txt")
    txt = f.read()
    transformed = transformText(txt)
    reordered = map(reorder,transformed)
    result = collapse(reordered)
    print result

if __name__ == '__main__':
    main()
