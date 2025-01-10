from fastapi import FastAPI, Request
import logging
import json

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

@app.middleware("http")
async def log_request_response(request: Request, call_next):
    # Log request details
    logging.info(f"Incoming request: {request.method} {request.url}")
    logging.info(f"Headers: {dict(request.headers)}")
    
    # Read and log the body (need to clone it as the body stream can be read only once)
    body = await request.body()
    if body:
        logging.info(f"Body: {body.decode('utf-8')}")
    
    # Process the request and get the response
    response = await call_next(request)
    
    # Log response details
    logging.info(f"Response status: {response.status_code}")
    
    return response
