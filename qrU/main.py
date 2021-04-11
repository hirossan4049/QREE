from uuid import uuid4
import io

from starlette.responses import StreamingResponse
from fastapi import FastAPI
import qrcode


app = FastAPI()
qr_img = bytes()
qr_hex = bytes()


def updateImg():
    global qr_img
    global qr_hex
    qr_hex = uuid4().hex
    print("qrhex", qr_hex)
    img = qrcode.make(qr_hex)
    output = io.BytesIO()
    img.save(output, format="png")
    qr_img = output
    #qr_img = io.BytesIO(output.getvalue())

@app.on_event("startup")
def startup_event():
    print("startup", qr_hex)
    updateImg()
    print("startup end", qr_hex)

@app.get("/")
def index():
    print(qr_hex)
    print(qr_img)
    return StreamingResponse(io.BytesIO(qr_img.getvalue()), media_type="image/png")


@app.get("/join/{id}/{name}")
def join(id: str, name: str):
    if id == str(qr_hex):
        print("join:", name)
        updateImg()
        return f"join: {name}"

    return "error"

