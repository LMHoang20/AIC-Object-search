from candidate import Candidate
from frame import Frame
from helper import MULTI_OBJECT_BONUS, get_hypernym_path

from nltk.corpus import wordnet as wn


class Searcher:
    def __init__(self, trie):
        self.trie = trie
        
    def search(self, query: list[dict[str, str]], topk: int) -> list[Candidate]:
        candidates: dict[str, float] = {}
        for q in query:
            this_candidates: list[Candidate] = []
            object, amount = q['object'], q['amount']
            hypernym_path = get_hypernym_path(object)
            node_frames = self.trie.search(hypernym_path)
            if amount == 'any':
                this_candidates.extend([Candidate(node_frame.frame, node_frame.p_total) for node_frame in node_frames])
            elif amount == int(amount):
                this_candidates.extend([Candidate(node_frame.frame, node_frame.p_of(amount)) for node_frame in node_frames])
            else:
                raise ValueError('Amount must be an integer or "any"')
            for candidate in this_candidates:
                if candidate.frame.id not in candidates:
                    candidates[candidate.frame.id] = candidate.score
                else: 
                    candidates[candidate.frame.id] += candidate.score + MULTI_OBJECT_BONUS
                
        candidates = [Candidate(Frame(id=id), score) for id, score in candidates.items()]
        candidates = sorted(candidates, key=lambda candidate: candidate.score, reverse=True)
        if len(candidates) > topk:
            candidates = candidates[:topk]
        return candidates
        

            
        
                
            
        
        
        
        