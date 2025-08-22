from fastapi import FastAPI, Response, status
from mangum import Mangum

app = FastAPI()

@app.get("/")
def root():
    return {"message": "OK"}

@app.get("/fail")
def fail(response: Response):
    response.status_code = status.HTTP_400_BAD_REQUEST
    return {"message": "Failure"}

# Lambda handler
handler = Mangum(app)
