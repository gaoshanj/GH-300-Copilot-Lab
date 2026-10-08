from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.service import calculate_checksum, find_order, summarize_order

app = FastAPI(title="GH-300 Applied Lab API", version="1.0.0")


class TextRequest(BaseModel):
    text: str = Field(min_length=1, max_length=10_000)


class OrderSummaryRequest(BaseModel):
    order_id: str = Field(min_length=1, max_length=32)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/checksum")
def checksum(request: TextRequest) -> dict[str, int]:
    return {"checksum": calculate_checksum(request.text)}


@app.get("/orders/{order_id}")
def order_summary(order_id: str) -> dict:
    order = find_order(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="order not found")
    return summarize_order(order)

