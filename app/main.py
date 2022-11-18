from fastapi import FastAPI

app = FastAPI(docs_url="/api/docs")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/names")
async def root():
    return {"message": "Uri & Noam"}


