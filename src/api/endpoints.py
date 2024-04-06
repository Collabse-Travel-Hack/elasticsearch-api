from fastapi import HTTPException, Query, APIRouter
from pydantic import BaseModel
from elasticsearch import Elasticsearch, NotFoundError

from src.config.settings import ELASTICSEARCH_HOST, ELASTICSEARCH_PORT

get_record = APIRouter()
get_index = APIRouter()

client = Elasticsearch(f'{ELASTICSEARCH_HOST}:{ELASTICSEARCH_PORT}')


class GetRecordRequest(BaseModel):
    index: str
    id: str


@get_record.post("/get_record")
async def get_record_handler(request: GetRecordRequest):
    try:
        # Поиск записи по id и index
        query = {
            'query': {
                'match': {
                    '_id': request.id
                }
            }
        }

        result = client.search(index=request.index, body=query)
        result = [hit['_source'] for hit in result['hits']['hits']]

        if not result:
            raise HTTPException(status_code=404, detail="Record not found")

        return result[0]
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Record not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class GetIndexRequest(BaseModel):
    index: str
    size: int = Query(default=10, ge=1, le=100, description="Page size")
    from_: int = Query(default=0, ge=0, alias="from", description="Starting offset")


@get_index.post("/get_index")
async def get_index_handler(request: GetIndexRequest):
    try:
        query = {
            'query': {
                'match_all': {}
            },
            'size': request.size,
            'from': request.from_
        }
        result = client.search(index=request.index, body=query)

        hits = result['hits']['hits']
        records = [hit['_source'] for hit in hits]

        return {
            'records': records,
            'total': result['hits']['total']['value']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
