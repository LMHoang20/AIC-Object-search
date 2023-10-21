from searcher import Searcher
from trie import Trie
import os

def main():
    trie = Trie()
    if os.path.exists('cache.json'):
        trie.load_from_cache('cache.json')
    else:
        trie.load_from_dir('data')
        trie.save_to_cache('cache.json')
        
    searcher = Searcher(trie)
    
    candidates = searcher.search([{'object': 'person', 'amount': 3}], 10)
    
    for candidate in candidates:
        print(candidate.frame.id, candidate.score)
        
    
if __name__ == '__main__':
    main()