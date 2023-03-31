import numpy as np
import cv2
import base64
from fastapi import FastAPI
from starlette.requests import Request
from models.model import model, processor, device

from config import TITLE, VERSION


app = FastAPI(
    title=TITLE,
    version=VERSION
)

@app.get("/")
def read_root():
    return VERSION

@app.post("/")
async def post_root(req: Request):
    src = await req.body()
    src = np.fromstring(base64.b64decode(src[23:]), dtype=np.uint8)
    img = cv2.imdecode(src, cv2.IMREAD_COLOR)
    pixel_values = processor([img], return_tensors="pt").pixel_values
    generated_ids = model.generate(pixel_values)
    model_output = processor.tokenizer.batch_decode(generated_ids, skip_special_tokens=True, device=device)[0]
    return model_output
