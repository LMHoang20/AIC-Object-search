from frame import Frame 
from helper import OBJECT_MAP, get_hypernym_path

from numpy.polynomial import polynomial
from nltk.corpus import wordnet as wn
import json
import os

class NodeFrame:
    def __init__(self, frame: Frame, p_list: list[float]) -> None:
        self.frame = frame
        self.p_list = p_list
        self.p_total = self.calculate_p_total(p_list)
        self.p_exactly = self.calculate_p_exactly(p_list)
        
    def calculate_p_total(self, p_list: list[float]) -> float:
        return sum(p_list)

    def calculate_p_exactly(self, p_list: list[float]) -> list[float]:
        result = [1]
        p_list = [[1 - p, p] for p in p_list]
        for p in p_list:
            result = polynomial.polymul(result, p)
        return list(result) 
    
    def p_of(self, amount: int) -> float:
        if amount < len(self.p_exactly):
            return self.p_exactly[amount]
        else:
            return self.p_exactly[-1] * (0.1 ** (amount - len(self.p_exactly) + 1))
        
    def serialize(self) -> dict:
        return {
            'frame': self.frame.serialize(),
            'p_list': self.p_list,
        }

class Node:
    def __init__(self, node_frames: list[NodeFrame]) -> None:
        self.node_frames = node_frames
        self.children = {}

class Trie:
    def __init__(self) -> None:
        self.root = Node([])
        
    def insert(self, node_frame: NodeFrame, path: list[str]) -> None:
        node = self.root
        for word in path:
            if word not in node.children:
                node.children[word] = Node([])
            node = node.children[word]
        node.node_frames.append(node_frame)
        
    def search(self, path: list[str]) -> list[NodeFrame]:
        node = self.root
        for word in path:
            if word not in node.children:
                return []
            node = node.children[word]
        return self.search_all_children(node)
    
    def search_all_children(self, node: Node) -> list[NodeFrame]:
        result = []
        if len(node.node_frames) > 0:
            result.extend(node.node_frames)
        for child in node.children.values():
            result.extend(self.search_all_children(child))
        return result
            
    def load_from_dir(self, dir: str) -> None:
        for path, _, files in os.walk(dir):
            for file in files:
                if file.endswith('.json'):
                    data = json.load(open(os.path.join(path, file)))
                    video = file[:-5]
                    for frame_name, frame_data in data.items():
                        for object, p_list in frame_data.items():
                            hypernym_path = get_hypernym_path(object)
                            self.insert(NodeFrame(Frame(video=video, frame_name=frame_name), p_list), hypernym_path)
    
    def save_to_cache(self, cache_path: str) -> None:
        json.dump(self.serialize(), open(cache_path, 'w'))
        
    def load_from_cache(self, cache_path: str) -> None:
        self.deserialize(json.load(open(cache_path)))
        
    def serialize(self) -> dict:
        output = {}
        def dfs(node: Node, path: list[str]) -> None:
            if len(node.node_frames) > 0:
                output['/'.join(path)] = [node_frame.serialize() for node_frame in node.node_frames]
            for word, child in node.children.items():
                dfs(child, path + [word])
        dfs(self.root, [])
        return output
        
    def deserialize(self, input):
        for path, node_frames in input.items():
            path = path.split('/')
            for node_frame in node_frames:
                self.insert(NodeFrame(Frame(id=node_frame['frame']['id']), node_frame['p_list']), path)
        
            
        
    
            
        
        