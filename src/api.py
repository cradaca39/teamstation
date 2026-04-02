from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class Item(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float


class ItemCreate(BaseModel):
    name: str
    description: str | None = None
    price: float


_items: list[Item] = [
    Item(id=1, name="Widget", description="A standard widget", price=9.99),
    Item(id=2, name="Gadget", description="A useful gadget", price=24.99),
    Item(id=3, name="Doohickey", description=None, price=4.49),
]


@router.get("/health")
def health():
    return {"status": "ok", "version": "1.0.0"}


@router.get("/items", response_model=list[Item])
def list_items():
    return _items


@router.post("/items", response_model=Item, status_code=201)
def create_item(item: ItemCreate):
    new_id = max((i.id for i in _items), default=0) + 1
    new_item = Item(id=new_id, **item.model_dump())
    _items.append(new_item)
    return new_item
