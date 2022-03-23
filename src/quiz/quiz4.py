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
import glob, os
from types import SimpleNamespace
from typing import Dict, List, Tuple, Set, Iterable, Any

import ahocorasick


def create_ac(data: Iterable[Tuple[str, Any]]) -> ahocorasick.Automaton:
    """
    Creates the Aho-Corasick automation and adds all (span, value) pairs in the data and finalizes this matcher.
    :param data: a collection of (span, value) pairs.
    """
    AC = ahocorasick.Automaton(ahocorasick.STORE_ANY)

    for span, value in data:
        if span in AC:
            t = AC.get(span)
        else:
            t = SimpleNamespace(span=span, values=set())
            AC.add_word(span, t)
        t.values.add(value)

    AC.make_automaton()
    return AC


def read_gazetteers(dirname: str) -> ahocorasick.Automaton:
    data = []
    for filename in glob.glob(os.path.join(dirname, '*.txt')):
        label = os.path.basename(filename)[:-4]
        for line in open(filename):
            data.append((line.strip(), label))
    return create_ac(data)


def match(AC: ahocorasick.Automaton, tokens: List[str]) -> List[Tuple[str, int, int, Set[str]]]:
    """
    :param AC: the finalized Aho-Corasick automation.
    :param tokens: the list of input tokens.
    :return: a list of tuples where each tuple consists of
             - span: str,
             - start token index (inclusive): int
             - end token index (exclusive): int
             - a set of values for the span: Set[str]
    """
    smap, emap, idx = dict(), dict(), 0
    for i, token in enumerate(tokens):
        smap[idx] = i
        idx += len(token)
        emap[idx] = i
        idx += 1

    # find matches
    text = ' '.join(tokens)
    spans = []
    for eidx, t in AC.iter(text):
        eidx += 1
        sidx = eidx - len(t.span)
        sidx = smap.get(sidx, None)
        eidx = emap.get(eidx, None)
        if sidx is None or eidx is None: continue
        spans.append((t.span, sidx, eidx + 1, t.values))

    return spans



def remove_subsets(entities: List[Tuple[str, int, int, Set[str]]]) -> List[Tuple[str, int, int, Set[str]]]:
    """
    :param entities: a list of tuples where each tuple consists of
             - span: str,
             - start token index (inclusive): int
             - end token index (exclusive): int
             - a set of values for the span: Set[str]
    :return: a list of entities where each entity is represented by a tuple of (span, start index, end index, value set)
    """
    tmp = []
    i = 0
    for k, (str, start, end, set) in enumerate(entities):
        if i>0 and i<len(entities) and entities[i-1][2] <= entities[i][1]:
            tmp.append((entities[i-1][0], entities[i-1][1], entities[i-1][2], entities[i-1][3]))
        elif i>0 and i<len(entities) and entities[i - 1][2] >= entities[i][1] and entities[i][2] >= entities[i-1][1]:
            range0 = entities[i-1][2]-entities[i-1][1]
            range1 = entities[i][2]-entities[i][1]
            if range1>range0:
                tmp.append((entities[i][0], entities[i][1], entities[i][2], entities[i][3]))
            if range0>=range1:
                tmp.append((entities[i-1][0], entities[i-1][1], entities[i-1][2], entities[i-1][3]))
            i = i + 1
        if i==len(entities)-1:
            tmp.append((entities[i][0], entities[i][1], entities[i][2], entities[i][3]))
        i = i + 1
    return tmp




def remove_overlaps_two(del_entities: List[Tuple[str, int, int, Set[str]]], tmp: List[Tuple[str,int,int,Set[str]]]) -> List[Tuple[str, int, int, Set[str]]]:
    if del_entities[0][2] <= del_entities[1][1]:
        tmp.append((del_entities[0][0], del_entities[0][1], del_entities[0][2], del_entities[0][3]))
        tmp.append((del_entities[1][0], del_entities[1][1], del_entities[1][2], del_entities[1][3]))
    elif del_entities[0][2] > del_entities[1][1]:
        range0 = del_entities[0][2] - del_entities[0][1]
        range1 = del_entities[1][2] - del_entities[1][1]
        if range1 > range0:
            tmp.append((del_entities[1][0], del_entities[1][1], del_entities[1][2], del_entities[1][3]))
        if range0 >= range1:
            tmp.append((del_entities[0][0], del_entities[0][1], del_entities[0][2], del_entities[0][3]))



def remove_overlaps(entities: List[Tuple[str, int, int, Set[str]]]) -> List[Tuple[str, int, int, Set[str]]]:
    """
    :param entities: a list of tuples where each tuple consists of
             - span: str,
             - start token index (inclusive): int
             - end token index (exclusive): int
             - a set of values for the span: Set[str]
    :return: a list of entities where each entity is represented by a tuple of (span, start index, end index, value set)
    """
    tmp = []
    del_entities = []
    for j, (str, start, end, set) in enumerate(entities):
        del_entities.append(entities[j])

    while len(del_entities) > 0:

        if len(del_entities) >= 3:
            if del_entities[0][2] <= del_entities[2][1] and del_entities[1][1] < del_entities[0][2] and del_entities[2][1] < del_entities[1][2]:
                tmp.append((del_entities[0][0], del_entities[0][1], del_entities[0][2], del_entities[0][3]))
                tmp.append((del_entities[2][0], del_entities[2][1], del_entities[2][2], del_entities[2][3]))
                del del_entities[2]
                del del_entities[1]
                del del_entities[0]

            elif del_entities[0][2] <= del_entities[1][1] and del_entities[1][2]>del_entities[2][1]:
                tmp.append((del_entities[0][0], del_entities[0][1], del_entities[0][2], del_entities[0][3]))
                del del_entities[0]

            elif del_entities[1][2] <= del_entities[2][1]:
                remove_overlaps_two(del_entities, tmp)
                del del_entities[1]
                del del_entities[0]

        elif len(del_entities) == 2:
            remove_overlaps_two(del_entities, tmp)
            del del_entities[1]
            del del_entities[0]

        elif len(del_entities) == 1:
            tmp.append((del_entities[0][0], del_entities[0][1], del_entities[0][2], del_entities[0][3]))
            del del_entities[0]

    return tmp


def to_bilou(tokens: List[str], entities: List[Tuple[str, int, int, str]]) -> List[str]:
    """
    :param tokens: a list of tokens.
    :param entities: a list of tuples where each tuple consists of
             - span: str,
             - start token index (inclusive): int
             - end token index (exclusive): int
             - a named entity tag
    :return: a list of named entity tags in the BILOU notation with respect to the tokens
    """
    result = []
    del_entities = []
    del_tokens = []
    for j, _ in enumerate(entities):
        del_entities.append(entities[j])
    del_tokens = []
    for i, _ in enumerate(tokens):
        del_tokens.append(tokens[i])

    while len(del_tokens) > 0 and len(del_entities) > 0:
        if del_tokens[0] == del_entities[0][0]:
            str_tag = ""
            multiple_NER_tags=0
            for x in del_entities[0][3]:
                if multiple_NER_tags != 0: str_tag += ", "
                str_tag += "U-" + x
                multiple_NER_tags += 1
            result.append(str_tag)
            del del_entities[0]
            del del_tokens[0]
        elif del_entities[0][0].startswith(del_tokens[0]):
            cur_entity = del_entities[0][0].split()
            check_if_same = 0
            for i in range(len(cur_entity)):
                if cur_entity[i] != del_tokens[i]: check_if_same+=1
            if check_if_same == 0:
                for i in range(len(cur_entity)):
                    str_char = ""
                    if i==0: str_char = "B-"
                    elif i==len(cur_entity)-1: str_char = "L-"
                    else: str_char = "I-"
                    str_tag = ""
                    multiple_NER_tags = 0
                    for x in del_entities[0][3]:
                        if multiple_NER_tags != 0: str_tag += ", "
                        str_tag += str_char + x
                        multiple_NER_tags+=1
                    result.append(str_tag)
                for i in range(len(cur_entity)):
                    del del_tokens[0]
                del del_entities[0]
            if check_if_same!=0:
                del del_tokens[0]
                result.append("0")
        else:
            del del_tokens[0]
            result.append("0")

    if len(del_entities) < 1 and len(del_tokens) > 0:
        for i, _ in enumerate(del_tokens):
            result.append("0")

    return result




if __name__ == '__main__':
    gaz_dir = 'res/ner'
    AC = read_gazetteers('res/ner')

    tokens = 'I went to Spain and South Korea United States today, it was nice, but not as nice as Atlantic City of Georgia'.split()
    entities = match(AC, tokens)
    entities = remove_overlaps(entities)
    #entities = remove_subsets(entities)
    #entities = remove_overlaps(entities)
    print(entities)
    tags = to_bilou(tokens, entities)
    for token, tag in zip(tokens, tags): print(token, tag)

