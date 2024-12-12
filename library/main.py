import uvicorn
from fastapi import FastAPI
from .database import Base, engine
from .routers import authors as AuthorRouter
from .routers import books as BookRouter
from .routers import borrow as BorrowRouter


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(AuthorRouter.router, prefix='/author')
app.include_router(BookRouter.router, prefix='/book')
app.include_router(BorrowRouter.router, prefix='/borrow')


if __name__=='__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000, reload=True)