# ========================================================================
# Copyright 2022 Emory University
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ========================================================================
import json
from typing import Dict, Any, List, Tuple
from collections import Counter
from src.vector_space_models import tf_idfs, most_similar, term_frequencies, document_frequencies, euclidean
import math

FM = {
    'antgrass2.ram': 'TheAntsandtheGrasshopper',
    'TheAssandhisPurchaser2': 'TheAssandHisPurchaser',
    'TheAssandtheLapdog2': 'TheAssandtheLapdog',
    'TheAssintheLionSkin': 'TheAssintheLionsSkin',
    'TheBellyandtheMembers2': 'TheBellyandtheMembers',
    'TheBuffoonandtheCountryman': 'TheBuffoonandtheCountryman2',
    'TheCrowandthePitcher2': 'crowpitc2.ram',
    'TheDogintheManger2': 'TheDogintheManger',
    'TheDogandtheShadow2': 'TheDogandtheShadow',
    'TheEagleandtheArrow2': 'TheEagleandtheArrow',
    'TheFoxandtheCrow2': 'TheFoxandtheCrow',
    'TheFoxandtheGoat2': 'TheFoxandtheGoat',
    'TheFoxandtheGrapes2': 'TheFoxandtheGrapes',
    'TheFoxandtheLion': 'TheFoxandtheLion2',
    'TheFoxandtheMask': 'foxmask2.ram',
    'haretort2.ram': 'TheHareandtheTortoise',
    'harefrog2.ram': 'TheHaresandtheFrogs',
    'TheHorseandtheAss2': 'TheHorseandtheAss',
    'TheLionandtheMouse2': 'lionmouse',
    'TheLioninLove2': 'TheLioninLove',
    'TheManandtheSatyr2': 'TheManandtheSatyr',
    'MercuryandtheWoodman': 'MercuryandtheWorkmen',
    'milkpail2.ram': 'milkmaidjug.jpg',
    'TheOldManandDeath2': 'TheOldManandDeath',
    'TheOldWomanandtheWine-Jar': 'womanjar2.ram',
    'TheOne-EyedDoe': 'TheOneEyedDoe',
    'ThePeacockandJuno': 'ThePeacockandJuno2',
    'TheRoseandtheAmaranth': 'TheRoseandtheAmaranth2',
    'TheSerpentandtheEagle': 'TheSerpentandtheEagle2',
    'shepherd2.ram': 'shepwolf2.ram',
    'TheSickLion2': 'TheSickLion',
    'TheTownMouseandtheCountryMouse': 'TheTownMouseandtheCountryMouse2',
    'TheTrumpeterTakenPrisoner2': 'TheTrumpeterTakenPrisoner',
    'TheTwoPots2': 'twopots2.ram',
    'TheVainJackdaw': 'TheVainJackdaw2',
    'TheWolfandtheCrane2': 'TheWolfandtheCrane',
    'TheWolfandtheLamb2': 'TheWolfandtheLamb',
    'TheWolfinSheepsClothing2': 'TheWolfinSheepsClothing'
}

#Method inputs:
    #B is altfable title, A is fable title.
    #X is Dict[altfable title, list of tokens in altfable], and Y is Dict[fable title, list of tokens in fable]
    #Z1 is Dict[title fable,Dict[term, tf_idfs]], Z2 = Dict[title altfable, Dict[term,tf_idfs]]
#Method function
    #num_same_word_pairs returns the number of same pairs of words in a fable and an altfable
    #where the words in the pair have relatively high tf_idfs and are not in a list of common words/punctuation
    #Unfortunately this method, though techincally functional, does not do well as an indiciation of overall document similarity
    #The fables are just too short for this method to be valuable
def num_same_word_pairs(fable: str, altfable: str, X: Dict[str,list], Y: Dict[str,list], Z1: Dict[str, Dict[str, float]], Z2: Dict[str, Dict[str, float]]) -> int:
    t=0
    A = X.get(fable)
    B = Y.get(altfable)
    BB = enumerate(B)
    P1 = [t for t, score in sorted(Z1[fable].items(), key=lambda x: x[1], reverse=True)[:int(len(A)/5)]]
    P2 = [t for t, score in sorted(Z2[altfable].items(), key=lambda x: x[1], reverse=True)[:int(len(B)/5)]]
    for j, word in BB:
        for i in range (0, len(A)-1):
            if word==A[i] and j<len(B)-1 and B[j+1]==A[i+1]:
                if A[i] in P1 or A[i+1] in P1 or word in P2 or B[j+1] in P2:
                    N = [".","!","?","\'", ":", ";","\"","and","the","or", ",", "he","she", "that", "I", "you", "him", "to", "in", "of", "his", "a", "had", "been", "did", "not", "they", "were", "was"]
                    if A[i] not in N and A[i+1] not in N: t += 1
    if t!=0: print("t: ", t, "fable: ", fable, " altfable: ", altfable)
    return t

#helper method for num_same_word_pairs
def get_list_tokens(fables) -> Dict[str,list]:
    def key(t): return t[t.rfind('&') + 1:]
    return {key(fable['source']): fable['tokens'].split() for fable in fables}



#Input: Dict[altfable title, fable title], output: an int representing the number of correct similar document matches
#The method checks with the correct matches list FM above to check how many correct matches the similar_documents method makes
#Prints the wrong matches with what the correct match should be
def number_right_matches(Z: Dict[str, str]) -> int:
    t = 0
    for Z1, Z2 in Z.items():
        if Z2 == FM.get(Z1,1): t += 1
        else:
            print("     Wrong:  ", '{} -> {} -> {}'.format(Z1, Z2, FM.get(Z1,1)))
    return t



#Method calculates the cosine similarity between two fables
def cosine(x1: Dict[str, float], x2: Dict[str, float]) -> float:
    t = sum((s1 * x2.get(term,0)) for term, s1 in x1.items())
        #if term is in x2 but not in x1 than we dont need to calculate anyway, since t+=0*s2 = t
    m1 = math.sqrt(sum(s1 ** 2 for term, s1 in x1.items()))
    m2 = math.sqrt(sum(s2 ** 2 for term, s2 in x2.items()))
    return t / (m1 * m2)



#Weighted term frequenct score, using the sublinear equation from the notes
#This work very badly! This is ecause our documents are small so this method doesn't make practical sense
#Each document does not have a relatively large number of terms, and the term frequency of each term is generally small
    #thus 1+math.log(tf)
def sublinear(fables) -> Dict[str,Dict[str,int]]:
    tfs = term_frequencies(fables)
    out = dict()
    for dkey, term_counts in tfs.items():
        out[dkey] = {t: 1+math.log(tf) for t,tf in term_counts.items()}
            #The sublinear function is if tf>0 then we do 1+math.log(tf). We always have tf>0, otherwise the term wouldn't be in the sparse vector
    return(out)

#Testing values of alpha
    #Using a for loop in the main method with variable i in range (0, 200), then alpha = 1/x, where x is any number and allows for get float values of alpha
    #I tested different value of alpha. The general range of correct matches of similar documents was 13 to 21 out of 37
    #For example, 0.85 yeilded 21 correct documents. Overall, this is better than using uclidean and tf_idfs, but worse than using cosine and tf_idfs
def normalize(fables) -> Dict[str,Dict[str,int]]:
    alpha = 0.2
    tfs = term_frequencies(fables)
    dfs = document_frequencies(fables)
    out = dict()
    for dkey, term_counts in tfs.items():
        max_tf = 0
        for t, tf in term_counts.items():
            if tf > max_tf: max_tf = tf
        out[dkey] = {t: alpha+(1-alpha)*(tf/max_tf) for t,tf in term_counts.items()}
    return out


#Input: all fables, Output: returns a Dict[fable title, Dict[term, calculated idfs of the term]]
#This method functions the same as the original tf_idfs method, except
    #if a term has first letter capitalized and is not in a list of common/non-important words/punctuation, then that term's tf_idfs score is increased
    #by 0.5. I experimented some and found that 0.2-0.5 seemed the best range.
    # This addition does not improve the accuracy the method/program, perhaps because of the short lengthes of the documents
def tf_idfs_with_capitals(fables) -> Dict[str, Dict[str, int]]:
    tfs = term_frequencies(fables)
    dfs = document_frequencies(fables)
    out = dict()
    D = len(tfs)
    #N is a list of common but un-important words/punctuation
    N = [".", "!", "?", "\'", ":", ";", "\"", "and", "the", "or", ",", "he", "she", "that", "i", "you", "him", "to",
         "in", "of", "his", "a", "had", "been", "did", "not", "they", "were", "was", "is", "of", "to", "in", "you", "have", "at", "by","her"
         "be", "will", "then", "but", "when", "now", "it", "as", "this", "so", "how", "on", "be", "once", "an","if", "what", "why", "ah",
         "yes", "do", "an", "yes", "for", "my", "one", "two", "three", "four", "we", "oh", "get", "no", "from", "0", "o", "good", "who", "among", "well"]
    for dkey, term_counts in tfs.items():
        dic = dict()
        for t, tf in term_counts.items():
            x = tf*math.log(D/dfs[t])
            if t[0].isupper() and t.lower() not in N:
                x=x+0.5
            dic[t] = x
        out[dkey] = dic
    return out


def vectorize(documents: List[Dict[str, Any]]) -> Dict[str, Dict[str, int]]:
    return tf_idfs_with_capitals(documents)



def similar_documents(X: Dict[str, Dict[str, float]], Y: Dict[str, Dict[str, float]]) -> Dict[str, str]:
            #X is Dict[titles altfables, Dict[terms in altfables, tf_idfs]]
            #Y is Dict[titles fables, Dict[terms in fables, tf_idfs]]
    return {k: most_similar1(Y, x) for k, x in X.items()} #use the method which compares cosine similarity
  #similar_documents takes the outputs of vectorize/tf_idfs of fables and altfables
  #Input to most_similar is Dict[titles fables, Dict[terms in fables, tf_idfs]], Dict[terms in altfables,tf_idfs]
  #returns the fable of all fables that is most similar to the alt fable


#Use cosine similarity instead of Euclidean distance
def most_similar1(Y: Dict[str, Dict[str, float]], x: Dict[str, float]) -> str:
    m, t = -1, None
    for title, y in Y.items():
        d = cosine(x,y)
        if m < 0 or d > m:
            m, t = d, title
    return t

#Uses Euclidean distance
def most_similar(Y: Dict[str, Dict[str, float]], x: Dict[str, float]) -> str:
    m, t = -1, None
    for title, y in Y.items(): #title is fable title
                               #y is Dict[terms in fables, tf_idfs]
                               # for all fables
        #print("title:", title)
        #print("y: ", y)
        d = euclidean(x, y)   #x is Dict[terms in in altfables, tf_idfs]
        if m < 0 or d < m:
            m, t = d, title
    return t
    #returns the title of the fable that is closest out of all fables to the given altfable


if __name__ == '__main__':
    fables = json.load(open('res/vsm/aesopfables.json'))
    fables_alt = json.load(open('res/vsm/aesopfables-alt.json'))

    v_fables = vectorize(fables)
    v_fables_alt = vectorize(fables_alt)

    for x, y in similar_documents(v_fables_alt, v_fables).items():
        print('{} -> {}'.format(x, y))

    #Check the correct number of matches and print all incorrect matches
    #My best: 33/37
    print(number_right_matches(similar_documents (v_fables_alt, v_fables)))
