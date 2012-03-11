#!/usr/bin/python
import re
import pdb

NEGATIVE_WORDS = ['not', 'never', 'nothing']

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

    def isGerund(self):
        return self.tag == "VBG"

    def startsWithVowel(self):
        letter = self.word[0].lower()
        return any([ letter == l for l in ["a","e","i","o","u"]])

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

def DOAfterVerb(s):
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

def OrOf(s):
    orofs = []
    for i in range(0, len(s)-1):
      Word = s[i]
      if Word.word.lower() == "or":
          if s[i+1].word.lower() == "of":
              orofs.append(i)

    if len(orofs) == 0:
        return

    firstOrOf = orofs.pop(0)
    s.pop(firstOrOf) # delete "or"

    numdeleted = 1

    for orof in orofs:
        s.pop(orof + 1 - numdeleted)
        numdeleted += 1

# distinguish whether or not there's a verb in front of 'to the'
def ToThe(s):
    tothes = []

    for i in range(1, len(s)-1):
      Word = s[i]
      if Word.word.lower() == "to":
          if s[i+1].word.lower() == "the":
              if not s[i-1].isVerb():
                  tothes.append(i)

    if len(tothes) == 0:
        return

    firstToThe = tothes.pop(0)
    s.pop(firstToThe + 1)

    numdeleted = 1

    for tothe in tothes:
        ind = tothe+1 - numdeleted
        s.pop(tothe - numdeleted)
        s.pop(tothe - numdeleted)
        numdeleted += 2 

def AAn(s):
    Ans = []
    As = []

    for i in range(0, len(s)-1):
        Word = s[i]
        word = Word.word
        if word == "a" and s[i+1].startsWithVowel():
            Ans.append(i)
        if word == "an" and not s[i+1].startsWithVowel():
            As.append(i)

    for A in As:
        s[A].word = "a"

    for An in Ans:
        s[An].word = "an"

def OfStrip(s):
    ofs = []

    for i in range(1, len(s) - 1):
        if s[i].word != "of":
            continue
        if s[i-1].isVerb() and not s[i-1].isGerund() and s[i+1].isNoun():
            ofs.append(i)

    if len(ofs) == 0:
        return

    numdeleted = 0
    for of in ofs:
        s.pop(of - numdeleted)
        numdeleted += 1

def NotSwap(s):
    for i in range(0, len(s)-2):
        if s[i].word != "not":
            continue
        swap(s, i+1, i+2)

def DoubleNeg(s):
    doublenegs = []

    for i in range(0, len(s)-1):
        if s[i].word != "not":
            continue
        if s[i+1].word in NEGATIVE_WORDS:
            doublenegs.append(i)

    numdeleted = 0
    for doubleneg in doublenegs:
        s.pop(doubleneg - numdeleted)
        numdeleted += 1
            

def reorder(s):
    print " ".join([S.word for S in s])
    AdjectiveBeforeNoun(s)
    AdverbAfterVerb(s)
    DOAfterVerb(s)
    InfinitiveVerbs(s)
    OrOf(s)
    ToThe(s)
    AAn(s)
    OfStrip(s)
    NotSwap(s)
    DoubleNeg(s)
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
    print txt + "\n"
    transformed = transformText(txt)
    reordered = map(reorder,transformed)
    result = collapse(reordered)
    print ".\n".join(result.split("."))

if __name__ == '__main__':
    main()
