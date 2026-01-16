from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def root():
    return {"message":"Helloooo!!! If this works, the cloud's up!!"}

@app.get("/health")
def health():
    return {"status":"All good :)"}