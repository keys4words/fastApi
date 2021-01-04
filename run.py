from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
async def hello_world():
    return {'Hello fastapi world'}




# tests api
# https://petstore.swagger.io/
# https://jsonplaceholder.typicode.com/

# running
# uvicorn run:app --reload --port 3000