from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from models.models import CreateStringRequest, StringItem
from services import services
from utils.utils import parse_natural_language

router = APIRouter()


@router.post("/strings", response_model=StringItem, status_code=201)
def create_string(payload: CreateStringRequest):
    try:
        return services.create_string(payload.value)
    except ValueError:
        raise HTTPException(status_code=409, detail="String already exists")


@router.get("/strings/{string_value}", response_model=StringItem)
def get_string(string_value: str):
    result = services.get_string(string_value)
    if not result:
        raise HTTPException(status_code=404, detail="String not found")
    return result


@router.get("/strings")
def list_strings(
    is_palindrome: Optional[bool] = Query(None),
    min_length: Optional[int] = Query(None),
    max_length: Optional[int] = Query(None),
    word_count: Optional[int] = Query(None),
    contains_character: Optional[str] = Query(None, max_length=1),
):
    data = services.list_strings(
        is_palindrome, min_length, max_length, word_count, contains_character
    )
    return {
        "data": data,
        "count": len(data),
        "filters_applied": {
            "is_palindrome": is_palindrome,
            "min_length": min_length,
            "max_length": max_length,
            "word_count": word_count,
            "contains_character": contains_character,
        },
    }


@router.get("/strings/filter-by-natural-language")
def filter_by_nl(query: str = Query(...)):
    try:
        filters = parse_natural_language(query)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    data = services.list_strings(**filters)
    return {
        "data": data,
        "count": len(data),
        "interpreted_query": {
            "original": query,
            "parsed_filters": filters,
        },
    }


@router.delete("/strings/{string_value}", status_code=204)
def delete_string(string_value: str):
    ok = services.delete_string(string_value)
    if not ok:
        raise HTTPException(status_code=404, detail="String not found")
