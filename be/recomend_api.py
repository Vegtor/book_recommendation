from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from book_recomend_sql import recomendation_sql_v3

app = FastAPI(title="Book Recommendation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/recommend_v3")
def get_recommendations(
    book_name: str = Query(..., description="Name of the book"),
    author: Optional[str] = Query(None, description="Author of the book"),
    publisher: Optional[str] = Query(None, description="Publisher of the book"),
    year: Optional[int] = Query(None, description="Year of publication"),
    isbn: Optional[str] = Query(None, description="ISBN of the book")
):
    try:
        df = recomendation_sql_v3(
            book_name=book_name,
            author=author,
            book_publisher=publisher,
            year_pb=year,
            isbn=isbn
        )

        result = df.to_dict(orient="records")
        return {
            "input": {
                "book_name": book_name,
                "author": author,
                "publisher": publisher,
                "year": year,
                "isbn": isbn
            },
            "recommendations": result
        }

    except Exception as e:
        if hasattr(e, 'args') and len(e.args) == 2 and e.args[0] == -1:
            _, msg = e.args
            raise HTTPException(status_code=404, detail=msg)
        else:
            raise HTTPException(status_code=500, detail=str(e))