"""THIS FILE IS NOT PART OF THE APP, BUT STORED HERE
TO BE USED WHEN NEEDED
"""

from fastapi import FastAPI, Request
import logging

app = FastAPI()

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(message)s", 
    handlers=[logging.StreamHandler()]
)

@app.middleware("http")
async def log_request_response(request: Request, call_next):

    # Collect request details
    method = request.method
    url = request.url
    headers = dict(request.headers)
    body = await request.body()
    body_str = body.decode("utf-8") if body else "No Body"

    logging.info(f"Request: {method} {url} | Headers: {headers} | Body: {body_str}")

    response = await call_next(request)
    logging.info(f"Response: Status {response.status_code} for {method} {url}")

    return response
