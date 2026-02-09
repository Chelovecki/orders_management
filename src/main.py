from  fastapi import FastAPI

app = FastAPI()

@app.get('/')
def get_():
    return 'hello world'