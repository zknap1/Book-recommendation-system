from fastapi.responses import PlainTextResponse
from fastapi import FastAPI
import pickle
from pydantic import BaseModel, Field
from recommend_book import recommend_book_by_author, recommend_book_by_keyword, recommend_book_by_popularity, recommend_by_author_and_keyword
import uvicorn

# load data
data_rated = pickle.load(open('data_rated', 'rb'))
data_popular_books = pickle.load(open('data_popular_books', 'rb'))
n = 5


class Recommendation_request(BaseModel):
    author: str = Field(
        default=None,
        description='The app will recommend books written by author.'
    )
    title: str = Field(
        default=None,
        description='The app will recommend books which readers of this book also enjoyed.'
    )
    keyword: str = Field(
        default=None,
        description='The app will recommend books which have similar keywords in the title.'
    )

app = FastAPI()

@app.get("/", response_class=PlainTextResponse)
def home():
    return "Welcome"

@app.post("/request")
def recommend(request_body: Recommendation_request):
    author = request_body.author
    keyword = request_body.keyword
    title = request_body.title

    # title is inserted (in possible combination with author or keyword)
    if title and title != "string":
        response = recommend_book_by_popularity(
            data_rated, data_popular_books, title)
    # both author and keywords are inserted
    elif author and keyword and author != "string" and keyword != "string" and title in (None, "string"):
        response = recommend_by_author_and_keyword(
            data_rated, author, keyword, n)
    # only author is inserted
    elif author and author != "string" and keyword in (None, "string") and title in (None, "string"):
        response = recommend_book_by_author(data_rated, author)
    # only keyword is inserted
    elif keyword and keyword != "string" and author in (None, "string") and title in (None, "string"):
        response = recommend_book_by_keyword(data_rated, keyword, n)

    response_json = response.head().to_json(orient="records")

    return {"books": response_json}


if __name__=="__main__":
    uvicorn.run("app:app", host='127.0.0.1', port=8000, reload=True)
