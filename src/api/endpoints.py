from fastapi import HTTPException, Query, APIRouter, Path
from pydantic import BaseModel
from elasticsearch import Elasticsearch, NotFoundError

from src.config.settings import ELASTICSEARCH_HOST, ELASTICSEARCH_PORT

get_record = APIRouter()
get_index = APIRouter()

client = Elasticsearch(f'{ELASTICSEARCH_HOST}:{ELASTICSEARCH_PORT}')


@get_record.get("/places/{id}")
async def get_record_handler(id: str = Path(..., description="Record ID")):
    try:
        # Поиск записи по id и index
        query = {
            'query': {
                'match': {
                    'id': id
                }
            }
        }

        result = client.search(index="places", body=query)
        result = [hit['_source'] for hit in result['hits']['hits']]

        if not result:
            raise HTTPException(status_code=404, detail="Record not found")

        return result[0]
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Record not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@get_index.get("/places")
async def get_index_handler(size: int = Query(..., ge=1, le=100), offset: int = Query(..., ge=0)):
    try:
        query = {
            'query': {
                'match_all': {}
            },
            'size': size,
            'from': offset
        }
        result = client.search(index="places", body=query)

        hits = result['hits']['hits']
        records = [hit['_source'] for hit in hits]

        return {
            'records': records,
            'total': result['hits']['total']['value']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
