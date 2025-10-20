# from fastapi import APIRouter, HTTPException, Query
# from typing import Optional
# from models.models import CreateStringRequest, StringItem
# from services import services
# from utils.utils import parse_natural_language

# router = APIRouter()


# @router.post("/strings", response_model=StringItem, status_code=201)
# def create_string(payload: CreateStringRequest):
#     try:
#         return services.create_string(payload.value)
#     except ValueError:
#         raise HTTPException(status_code=409, detail="String already exists")


# @router.get("/strings/{string_value}", response_model=StringItem)
# def get_string(string_value: str):
#     result = services.get_string(string_value)
#     if not result:
#         raise HTTPException(status_code=404, detail="String not found")
#     return result


# @router.get("/strings")
# def list_strings(
#     is_palindrome: Optional[bool] = Query(None),
#     min_length: Optional[int] = Query(None),
#     max_length: Optional[int] = Query(None),
#     word_count: Optional[int] = Query(None),
#     contains_character: Optional[str] = Query(None, max_length=1),
# ):
#     data = services.list_strings(
#         is_palindrome, min_length, max_length, word_count, contains_character
#     )
#     return {
#         "data": data,
#         "count": len(data),
#         "filters_applied": {
#             "is_palindrome": is_palindrome,
#             "min_length": min_length,
#             "max_length": max_length,
#             "word_count": word_count,
#             "contains_character": contains_character,
#         },
#     }


# @router.get("/strings/filter-by-natural-language")
# def filter_by_nl(query: str = Query(...)):
#     try:
#         filters = parse_natural_language(query)
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))

#     data = services.list_strings(**filters)
#     return {
#         "data": data,
#         "count": len(data),
#         "interpreted_query": {
#             "original": query,
#             "parsed_filters": filters,
#         },
#     }


# @router.delete("/strings/{string_value}", status_code=204)
# def delete_string(string_value: str):
#     ok = services.delete_string(string_value)
#     if not ok:
#         raise HTTPException(status_code=404, detail="String not found")


from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from models.models import StringItem, CreateStringRequest
from services import services
from utils.utils import parse_natural_language

router = APIRouter()

# ---------------------------
# 1️⃣ Create / Analyze String
# ---------------------------
@router.post("/strings", response_model=StringItem, status_code=201)
def create_string(payload: CreateStringRequest):
    # ✅ Validate request body
    if not payload.value or not isinstance(payload.value, str):
        raise HTTPException(
            status_code=400,
            detail='Invalid request body or missing "value" field. Must provide a valid string.',
        )

    try:
        return services.create_string(payload.value)
    except ValueError as e:
        # ✅ String already exists
        if "exists" in str(e).lower():
            raise HTTPException(
                status_code=409,
                detail="String already exists in the system",
            )
        # ✅ Unexpected internal issue
        raise HTTPException(status_code=422, detail="Unprocessable entity")


# ---------------------------
# 2️⃣ Get Specific String
# ---------------------------
@router.get("/strings/{string_value}", response_model=StringItem)
def get_string(string_value: str):
    result = services.get_string(string_value)
    if not result:
        raise HTTPException(
            status_code=404, detail="String does not exist in the system"
        )
    return result


# ---------------------------
# 3️⃣ Get All Strings with Filtering
# ---------------------------
@router.get("/strings")
def list_strings(
    is_palindrome: Optional[bool] = Query(None),
    min_length: Optional[int] = Query(None),
    max_length: Optional[int] = Query(None),
    word_count: Optional[int] = Query(None),
    contains_character: Optional[str] = Query(None, max_length=1),
):
    try:
        # ✅ Validate query parameters
        if (
            min_length is not None and min_length < 0
        ) or (
            max_length is not None and max_length < 0
        ):
            raise HTTPException(
                status_code=400,
                detail="Invalid query parameter values. Lengths must be non-negative integers.",
            )

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

    except ValueError:
        raise HTTPException(
            status_code=400, detail="Invalid query parameter values or types"
        )


# ---------------------------
# 4️⃣ Natural Language Filtering
# ---------------------------
@router.get("/strings/filter-by-natural-language")
def filter_by_nl(query: str = Query(...)):
    try:
        filters = parse_natural_language(query)
        if not filters:
            raise HTTPException(
                status_code=400,
                detail="Unable to parse natural language query",
            )

        # Detect potential conflicting filters (e.g. min_length > max_length)
        if (
            "min_length" in filters
            and "max_length" in filters
            and filters["min_length"] > filters["max_length"]
        ):
            raise HTTPException(
                status_code=422,
                detail="Query parsed but resulted in conflicting filters",
            )

        data = services.list_strings(**filters)

        return {
            "data": data,
            "count": len(data),
            "interpreted_query": {
                "original": query,
                "parsed_filters": filters,
            },
        }

    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Unable to parse natural language query",
        )


# ---------------------------
# 5️⃣ Delete String
# ---------------------------
@router.delete("/strings/{string_value}", status_code=204)
def delete_string(string_value: str):
    ok = services.delete_string(string_value)
    if not ok:
        raise HTTPException(
            status_code=404,
            detail="String does not exist in the system",
        )
