from nltk.corpus import wordnet as wn
from fastapi.responses import JSONResponse

OBJECT_MAP = {
    "stop_sign": "traffic_control",
    "sports_ball": "ball",
    "wine_glass": "glass",
    "potted_plant": "plant",   
}

MULTI_OBJECT_BONUS = 1.0

def get_hypernym_path(object):
    object = object.lower().replace(' ', '_')
    if object in OBJECT_MAP:
        object = OBJECT_MAP[object]
    synset = wn.synsets(object, 'n')
    if len(synset) == 0:
        hypernym_path = [object]
    else:
        hypernym_path = [s.name()[:-5] for s in synset[0].hypernym_paths()[0]]
    return hypernym_path

def parse_query(query: str) -> list[dict]:
    result = []
    query = query.split(',')
    for q in query:
        q = q.split(':')
        if len(q) == 2:
            result.append({'object': q[0], 'amount': int(q[1])})
        else:
            result.append({'object': q[0], 'amount': 'any'})
    return result

    
def make_response(status: int, message: str, data: dict|None = None) -> dict:
    return JSONResponse(content={
        'status': status,
        'message': message,
        'data': data,    
    })