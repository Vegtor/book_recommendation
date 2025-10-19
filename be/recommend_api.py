import numpy as np
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from book_recommend_sql import recommendation_sql_v1
from book_recommend_goodreads import recommendation_sql_v2, recommendation_sql_v2_1
import os

app = FastAPI(title="Book Recommendation API")

FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:5173")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/recommend_v1")
def get_recommendations_v1(
    book_name: str = Query(..., description="Name of the book"),
    version: str = Query(..., description="Version of search"),
    author: Optional[str] = Query(None, description="Author of the book"),
    publisher: Optional[str] = Query(None, description="Publisher of the book"),
    year: Optional[int] = Query(None, description="Year of publication"),
    isbn: Optional[str] = Query(None, description="ISBN of the book")
):
    try:
        if version == "v1":
            searched_book, df = recommendation_sql_v1(book_name=book_name,author=author,book_publisher=publisher,
                                                      year_pb=year,isbn=isbn)
        else:
            searched_book, df = recommendation_sql_v1(book_name=book_name, author=author, book_publisher=publisher,
                                                      year_pb=year, isbn=isbn)

        result_book = searched_book.to_dict(orient="records")
        if df is not None and not df.empty:
            result = df.to_dict(orient="records")
        else:
            result = []
        return {
            "searched_book": result_book,
            "recommendations": result
        }

    except Exception as e:
        if hasattr(e, 'args') and len(e.args) == 2 and e.args[0] == -1:
            _, msg = e.args
            raise HTTPException(status_code=404, detail=msg)
        else:
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/recommend_v2")
def get_recommendations_v2(
    book_name: str = Query(..., description="Name of the book"),
    version: str = Query(..., description="Version of search"),
    author: Optional[str] = Query(None, description="Author of the book"),
    year: Optional[int] = Query(None, description="Year of publication"),
    isbn: Optional[str] = Query(None, description="ISBN of the book")
):
    def sanitize_df(df):
        return df.replace([np.nan, np.inf, -np.inf], None)

    try:
        if version == "v2":
            searched_book, df = recommendation_sql_v2(book_name=book_name,author=author,year_pb=year,isbn=isbn)
        else:
            searched_book, df = recommendation_sql_v2_1(book_name=book_name, author=author, year_pb=year, isbn=isbn)

        searched_book = sanitize_df(searched_book)
        result_book = searched_book.to_dict(orient="records")
        if df is not None and not df.empty:
            df = sanitize_df(df)
            result = df.to_dict(orient="records")
        else:
            result = []
        return {
            "searched_book": result_book,
            "recommendations": result
        }

    except Exception as e:
        if hasattr(e, 'args') and len(e.args) == 2 and e.args[0] == -1:
            _, msg = e.args
            raise HTTPException(status_code=404, detail=msg)
        else:
            raise HTTPException(status_code=500, detail=str(e))