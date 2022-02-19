# ========================================================================
# Copyright 2020 Emory University
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
import pickle
from collections import Counter
from typing import List, Tuple, Dict, Any

DUMMY = '!@#$'


def read_data(filename: str):
    data, sentence = [], []
    fin = open(filename)

    for line in fin:
        l = line.split()
        if l:
            sentence.append((l[0], l[1]))
        else:
            data.append(sentence)
            sentence = []

    return data


def word_count(data: List[List[Tuple[str, str]]]) -> int:
    """
    :param data: a list of tuple list where each inner list represents a sentence and every tuple is a (word, pos) pair.
    :return: the total number of words in the data
    """
    return sum([len(sentence) for sentence in data])


def to_probs(model: Dict[Any, Counter]) -> Dict[str, List[Tuple[str, float]]]:
    probs = dict()
    for feature, counter in model.items():
        ts = counter.most_common()
        total = sum([count for _, count in ts])
        probs[feature] = [(label, count/total) for label, count in ts]
    return probs



def create_cw_dict(data: List[List[Tuple[str, str]]]) -> Dict[str, List[Tuple[str, float]]]:
    """
    :param data: a list of tuple lists where each inner list represents a sentence and every tuple is a (word, pos) pair.
    :return: a dictionary where the key is a word and the value is the list of possible POS tags with probabilities in descending order.
    """
    model = dict()
    for sentence in data:
        for word, pos in sentence:
            model.setdefault(word, Counter()).update([pos])
    return to_probs(model)


def create_pp_dict(data: List[List[Tuple[str, str]]]) -> Dict[str, List[Tuple[str, float]]]:
    """
    :param data: a list of tuple lists where each inner list represents a sentence and every tuple is a (word, pos) pair.
    :return: a dictionary where the key is the previous POS tag and the value is the list of possible POS tags with probabilities in descending order.
    """
    model = dict()
    for sentence in data:
        for i, (_, curr_pos) in enumerate(sentence):
            prev_pos = sentence[i-1][1] if i > 0 else DUMMY
            model.setdefault(prev_pos, Counter()).update([curr_pos])
    return to_probs(model)


def create_pw_dict(data: List[List[Tuple[str, str]]]) -> Dict[str, List[Tuple[str, float]]]:
    """
    :param data: a list of tuple lists where each inner list represents a sentence and every tuple is a (word, pos) pair.
    :return: a dictionary where the key is the previous word and the value is the list of possible POS tags with probabilities in descending order.
    """
    model = dict()
    for sentence in data:
        for i, (_, curr_pos) in enumerate(sentence):
            prev_word = sentence[i-1][0] if i > 0 else DUMMY
            model.setdefault(prev_word, Counter()).update([curr_pos])
    return to_probs(model)


def create_nw_dict(data: List[List[Tuple[str, str]]]) -> Dict[str, List[Tuple[str, float]]]:
    """
    :param data: a list of tuple lists where each inner list represents a sentence and every tuple is a (word, pos) pair.
    :return: a dictionary where the key is the next word and the value is the list of possible POS tags with probabilities in descending order.
    """
    model = dict()
    for sentence in data:
        for i, (_, curr_pos) in enumerate(sentence):
            next_word = sentence[i+1][0] if i+1 < len(sentence) else DUMMY
            model.setdefault(next_word, Counter()).update([curr_pos])
    return to_probs(model)



def create_cw_pp_dict(data: List[List[Tuple[str, str]]]) -> Dict[Tuple[str,str], List[Tuple[str, float]]]:
    """
    :param data: a list of tuple lists where each inner list represents a sentence and every tuple is a (word, pos) pair.
    :return: a dictionary where the key is a tuple (current word, previous POS) and the value is the list of possible POS tags with probabilities in descending order.
    """
    model = dict()
    for sentence in data:
        for i, (word, curr_pos) in enumerate(sentence):
            prev_pos = sentence[i-1][1] if i > 0 else DUMMY
            model.setdefault((word, prev_pos), Counter()).update([curr_pos])
    return to_probs(model)


def create_cw_pw_dict(data: List[List[Tuple[str, str]]]) -> Dict[Tuple[str,str], List[Tuple[str, float]]]:
    """
    :param data: a list of tuple lists where each inner list represents a sentence and every tuple is a (word, pos) pair.
    :return: a dictionary where the key is a tuple of (current word, previous word) and the value is the list of possible POS tags with probabilities in descending order.
    """
    model = dict()
    for sentence in data:
        for i, (word, curr_pos) in enumerate(sentence):
            prev_word = sentence[i-1][0] if i > 0 else DUMMY
            model.setdefault((word, prev_word), Counter()).update([curr_pos])
    return to_probs(model)


def create_cw_nw_dict(data: List[List[Tuple[str, str]]]) -> Dict[Tuple[str,str], List[Tuple[str, float]]]:
    """
    :param data: a list of tuple lists where each inner list represents a sentence and every tuple is a (word, pos) pair.
    :return: a dictionary where the key is a tuple of the (current word, next word) and the value is the list of possible POS tags with probabilities in descending order.
    """
    model = dict()
    for sentence in data:
        for i, (word, curr_pos) in enumerate(sentence):
            next_word = sentence[i+1][0] if i+1 < len(sentence) else DUMMY
            model.setdefault((word,next_word), Counter()).update([curr_pos])
    return to_probs(model)


def create_pw_cw_nw_dict(data: List[List[Tuple[str, str]]]) -> Dict[Tuple[str,str,str], List[Tuple[str, float]]]:
    """
    :param data: a list of tuple lists where each inner list represents a sentence and every tuple is a (word, pos) pair.
    :return: a dictionary where the key is a tuple of the (previous word, current word, next word) and the value is the list of possible POS tags with probabilities in descending order.
    """
    model = dict()
    for sentence in data:
        for i, (word, curr_pos) in enumerate(sentence):
            prev_word = sentence[i - 1][0] if i > 0 else DUMMY
            next_word = sentence[i+1][0] if i+1 < len(sentence) else DUMMY
            model.setdefault((prev_word,word,next_word), Counter()).update([curr_pos])
    return to_probs(model)


def create_pp_cw_nw_dict(data: List[List[Tuple[str, str]]]) -> Dict[Tuple[str,str,str], List[Tuple[str, float]]]:
    """
    :param data: a list of tuple lists where each inner list represents a sentence and every tuple is a (word, pos) pair.
    :return: a dictionary where the key is a tuple of the (previous pos, current word, next word) and the value is the list of possible POS tags with probabilities in descending order.
    """
    model = dict()
    for sentence in data:
        for i, (word, curr_pos) in enumerate(sentence):
            prev_pos = sentence[i - 1][1] if i > 0 else DUMMY
            next_word = sentence[i+1][0] if i+1 < len(sentence) else DUMMY
            model.setdefault((prev_pos,word,next_word), Counter()).update([curr_pos])
    return to_probs(model)







def train(trn_data: List[List[Tuple[str, str]]], dev_data: List[List[Tuple[str, str]]]) -> Tuple:
    """
    :param trn_data: the training set
    :param dev_data: the development set
    :return: a tuple of all parameters necessary to perform part-of-speech tagging
    """
    cw_dict = create_cw_dict(trn_data)
    pp_dict = create_pp_dict(trn_data)
    pw_dict = create_pw_dict(trn_data)
    nw_dict = create_nw_dict(trn_data)
    cw_pw_dict = create_cw_pw_dict(trn_data)
    cw_nw_dict = create_cw_nw_dict(trn_data)
    cw_pp_dict = create_cw_pp_dict(trn_data)
    pw_cw_nw_dict = create_pw_cw_nw_dict(trn_data)
    pp_cw_nw_dict = create_pp_cw_nw_dict(trn_data)
    best_acc, best_args = -1, None

    cw_weight = 0.75
    pp_weight = 0.275
    pw_weight = 0.5
    nw_weight = 0.7
    cw_pw_weight = 1.0
    cw_nw_weight = 0.95
    cw_pp_weight = 0.65
    pw_cw_nw_weight = 0.55
    pp_cw_nw_weight = 0.800

    #After getting a general sense of the values whic should be associated with each weight from the sparse grid search,
    #I did a fine grain search of each inividual weight to extract the greatest values
    #My final highest training result score on the development data was 95.1% accuracy
    """
    grid = [0.0, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6 ,0.65, 0.7, 0.75, 0.8,0.85,0.9, 0.95,1.0, 1.05, 1.1, 1.2, 1.3, 1.4, 1.5, 2.0]
    for some_weight in grid:
         args = (cw_dict, pp_dict, pw_dict, nw_dict, cw_pw_dict, cw_nw_dict, cw_pp_dict, pw_cw_nw_dict, pp_cw_nw_dict, cw_weight,pp_weight, pw_weight, nw_weight, cw_pw_weight, cw_nw_weight, cw_pp_weight, pw_cw_nw_weight, pp_cw_nw_weight)
         acc = evaluate(dev_data, *args)
         print('{:5.6f}% - cw: {:3.3f}, pp: {:3.3f}, pw: {:3.3f}, nw: {:3.3f}, cw_pw: {:3.3f}, cw_nw: {:3.3f}, cw_pp: {:3.3f}, pw_cw_nw: {:3.3f}, pp_cw_nw: {:3.3f}'.format(acc, cw_weight, pp_weight, pw_weight, nw_weight, cw_pw_weight, cw_nw_weight,cw_pp_weight, pw_cw_nw_weight, pp_cw_nw_weight))
         if acc > best_acc: best_acc, best_args = acc, args
    """

    #Do a sparse grid search just like in class. I did it before adding the final/trigram dictionaries
    #Helped to find a general range for values
    #Obviously a more dense grid search with all dictionaries would have yeilded the highest result, but that would require too much time and memory
    """
    grid = [0.1, 0.5, 1.0]
    for cw_weight in grid:
        for pp_weight in grid:
            for pw_weight in grid:
                for nw_weight in grid:
                    for cw_pw_weight in grid:
                        for cw_nw_weight in grid:
                            for cw_pp_weight in grid:
                                args = (cw_dict, pp_dict, pw_dict, nw_dict, cw_pw_dict, cw_nw_dict, cw_pp_dict, cw_weight, pp_weight, pw_weight, nw_weight, cw_pw_weight, cw_nw_weight, cw_pp_weight)
                                acc = evaluate(dev_data, *args)
                                print('{:5.2f}% - cw: {:3.1f}, pp: {:3.1f}, pw: {:3.1f}, nw: {:3.1f}, cw_pw: {:3.1f}, cw_new: {:3.1f}, cw_pp: {:3.1f}'.format(acc, cw_weight, pp_weight, pw_weight, nw_weight, cw_pw_weight, cw_nw_weight, cw_pp_weight))
                                if acc > best_acc: best_acc, best_args = acc, args
                                """

    best_args = (cw_dict, pp_dict, pw_dict, nw_dict, cw_pw_dict, cw_nw_dict, cw_pp_dict, pw_cw_nw_dict, pp_cw_nw_dict, cw_weight, pp_weight, pw_weight, nw_weight, cw_pw_weight, cw_nw_weight, cw_pp_weight, pw_cw_nw_weight, pp_cw_nw_weight)
    best_acc = evaluate(dev_data, *best_args)
    print("  ")
    print('{:5.10f}% - cw: {:3.3f}, pp: {:3.3f}, pw: {:3.3f}, nw: {:3.3f}, cw_pw: {:3.3f}, cw_new: {:3.3f}, cw_pp: {:3.3f}, pw_cw_nw: {:3.3f}, pp_cw_nw: {:3.3f}'.format(best_acc, best_args[9], best_args[10], best_args[11], best_args[12], best_args[13], best_args[14], best_args[15], best_args[16], best_args[17]))
    return best_args


def evaluate(data: List[List[Tuple[str, str]]], *args):
    total, correct = 0, 0
    for sentence in data:
        tokens, gold = tuple(zip(*sentence))
        pred = [t[0] for t in predict(tokens, *args)]
        total += len(tokens)
        correct += len([1 for g, p in zip(gold, pred) if g == p])
    accuracy = 100.0 * correct / total
    return accuracy



def predict(tokens: List[str], *args) -> List[Tuple[str, float]]:
    """
        :param tokens: a list of tokens.
        :param args: a variable number of arguments
        :return: a list of tuple where each tuple represents a pair of (POS, score) of the corresponding token.
        """
    cw_dict, pp_dict, pw_dict, nw_dict, cw_pw_dict, cw_nw_dict, cw_pp_dict, pw_cw_nw_dict, pp_cw_nw_dict, cw_weight, pp_weight, pw_weight, nw_weight, cw_pw_weight, cw_nw_weight, cw_pp_weight, pw_cw_nw_weight, pp_cw_nw_weight = args
    output = []

    for i in range(len(tokens)):
        scores = dict()
        curr_word = tokens[i]
        prev_pos = output[i-1][0] if i > 0 else DUMMY
        prev_word = tokens[i-1] if i > 0 else DUMMY
        next_word = tokens[i+1] if i+1 < len(tokens) else DUMMY

        for pos, prob in cw_dict.get(curr_word, list()):
            scores[pos] = scores.get(pos, 0) + prob * cw_weight

        for pos, prob in pp_dict.get(prev_pos, list()):
            scores[pos] = scores.get(pos, 0) + prob * pp_weight

        for pos, prob in pw_dict.get(prev_word, list()):
            scores[pos] = scores.get(pos, 0) + prob * pw_weight

        for pos, prob in nw_dict.get(next_word, list()):
            scores[pos] = scores.get(pos, 0) + prob * nw_weight

        for pos, prob in cw_pw_dict.get((curr_word,prev_word), list()):
            scores[pos] = scores.get(pos, 0) + prob * cw_pw_weight

        for pos, prob in cw_nw_dict.get((curr_word,next_word), list()):
            scores[pos] = scores.get(pos, 0) + prob * cw_nw_weight

        for pos, prob in cw_pp_dict.get((curr_word,prev_pos), list()):
            scores[pos] = scores.get(pos, 0) + prob * cw_pp_weight

        for pos, prob in pw_cw_nw_dict.get((prev_word,curr_word,next_word), list()):
            scores[pos] = scores.get(pos, 0) + prob * pw_cw_nw_weight

        for pos, prob in pp_cw_nw_dict.get((prev_pos,curr_word,next_word), list()):
            scores[pos] = scores.get(pos, 0) + prob * pp_cw_nw_weight

        o = max(scores.items(), key=lambda t: t[1]) if scores else ('XX', 0.0)
        output.append(o)

    return output






if __name__ == '__main__':

    path = './'  # path to the cs329 directory
    trn_data = read_data(path + 'res/pos/wsj-pos.trn.gold.tsv')
    dev_data = read_data(path + 'res/pos/wsj-pos.dev.gold.tsv')
    #model_path = path + 'src/quiz/quiz3.pkl'
    model_path = path + 'quiz3.pkl'

    # save model
    args = train(trn_data, dev_data)
    pickle.dump(args, open(model_path, 'wb'))
    # load model
    args = pickle.load(open(model_path, 'rb'))
    print(evaluate(dev_data, *args))