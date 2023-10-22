# AIC-Object-search

## API

### Health
`/health` (GET)

### Search:
`/search` (POST)

#### Request:

##### Body:
- `query_string`: list of objects to search for, separated by `,`, each object can have an optional `:number` suffix to specify the number of objects to search for, default is `any`.
- `topk`: return the top `k` results

#### Response:
- `status`: `int`, HTTP code
- `message`: `string`, Error message if error
- `data`: 
    - `video`: `string`, the name of the video
    - `frame_name`: `string`, the frame image name
    - `score`: `int`, the score of the keyframe

#### Example: 
Search for frames with any number of persons and exactly 2 cows:

Request: `http://localhost:8000/search`

Body: 
```json
{
    "query_text": "person, cow:2",
    "topk": 3
}   
```
Response: 
```json
{
    "data": 
    [
        {"video":"L01_V001","frame_name":"0006.jpg","score":12.87},
        {"video":"L01_V001","frame_name":"0211.jpg", "score":12.55},
        {"video":"L01_V001","frame_name":"0229.jpg","score":10.33}
    ],
    "message": "OK",
    "status": 200
}
```

#### Note:

- Downloading data from bucket takes around 1 minute.

- Loading the downloaded data into memory takes around 1 minute.

- Loading data from the cache to memory takes around 30 second.

- The number of objects should only be specified when searching for specific objects, e.g. `person:2, cow:3`, searching for generic objects should not have the number specified (you likely would not know the number of objects if you want to search for generic ones anyway), e.g. `animal, furniture`.