from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from book_recomend import recomendation_v1

app = FastAPI(title="Book Recommendation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/recommend")
def get_recommendations(book_name: str = Query(..., description="Name of the book")):
    df = recomendation_v1(book_name)

    result = df.to_dict(orient="records")
    return {"input_book": book_name, "recommendations": result}