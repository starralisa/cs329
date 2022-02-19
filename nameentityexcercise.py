



def recognize_ngram(tokens: List[str], gazetteer: Dict[str, Set[str]]) -> List[Tuple[int, int, str, Set[str]]]:
    elements = []


    for a in range(len(tokens)):
        for b in range(a+1, len(tokens)+1):
            keyvalue = ' '.join(tokens[a:b])
            value = gazetteer.get(keyvalue, None)
            if value != None: elements.append(a,b,keyvalue,value);

    return elements;
