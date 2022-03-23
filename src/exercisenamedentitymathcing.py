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

    for i, (str, start, end, set) in enumerate(entities):
        if i>0 and entities[i-1][2] < entities[i][1]: tmp.update(entities[i-1][0], entities[i-1][1], entities[i-1][2], entities[i-1][3])
        if i=len(entities)-1 and entities[i - 1][2] < entities[i][1]: tmp.update(entities[i][0], entities[i][1], entities[i][2], entities[i][3])
    return tmp