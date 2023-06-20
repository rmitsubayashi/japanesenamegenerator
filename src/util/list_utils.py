from itertools import chain, combinations
from typing import List

class ListUtils:

    """
    Example: powerset([1,2,3]) --> (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    """
    def powerset(self, iterable: List[object]) -> List[List[object]]:
        s = list(iterable)
        return list(chain.from_iterable(combinations(s, r) for r in range(1, len(s)+1)))

    """
    Example: combination([1],[1,2],[3,4]) --> [[1,1,3],[1,1,4],[1,2,3],[1,2,4]]
    """
    def combination(self, iterable: List[List[object]]) -> List[List[object]]:
        return self._combination(iterable, 0, None)

    # probably can do this cleaner :(
    def _combination(self, iterable: List[List[object]], index: int, prev_object: object) -> List[List[object]]:
        # edge leaf
        if index == len(iterable):
            return [[prev_object]]

        result = []
        for currentObject in iterable[index]:
            next_leaves = self._combination(iterable, index+1, currentObject)
            
            for leaf in next_leaves:
                # starting node
                if prev_object == None:
                    result.append(leaf)
                else:
                    added_parent_leaf = [prev_object] + leaf
                    result.append(added_parent_leaf)
        
        return result

