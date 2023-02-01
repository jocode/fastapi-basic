from fastapi import FastAPI

app = FastAPI()
app.title = "Mi aplicación con FastAPI"
app.version = "0.0.1"
app.description = "FastAPI documentation"

@app.get("/", tags=["home"], description="Hola")
def message():
    return "Hello world"