from fastapi import APIRouter, HTTPException, status
from typing import List
from modules.items.schemas import ItemCreate, ItemResponse, ItemUpdate

router = APIRouter(
    prefix="/items", tags=["Items Management"]
)

#In-memory mock database simulation

DATABASE_MOCK = {
    1: {"id": 1, "name": "Production Blueprint", "description": "Architecture plans", "price": 49.99},
    2: {"id": 2, "name": "Debugger Mug", "description": "Holds liquid sanity", "price":14.95} # type: ignore
}

current_id_counter = 2

@router.get("/", response_model=List[ItemResponse], status_code=status.HTTP_200_OK)
def get_all_items():
    return DATABASE_MOCK.values()


@router.get("/{item_id}", response_model=ItemResponse, status_code=status.HTTP_200_OK)
def get_item(item_id: int):
    if item_id not in DATABASE_MOCK:
        raise HTTPException(status_code=404, detail=f"item with {item_id} not found")
    return DATABASE_MOCK[item_id]



@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def update_item_complete( payload: ItemCreate):
    global current_id_counter
    current_id_counter += 1
    new_item = {"id":current_id_counter, **payload.model_dump()}
    DATABASE_MOCK[current_id_counter] = new_item
    return new_item


@router.put("/{item_id}", response_model=ItemResponse, status_code=status.HTTP_200_OK)
def update_item_complete(item_id: int, payload:ItemUpdate):
    if item_id not in DATABASE_MOCK:
        raise HTTPException(status_code=404, detail=f"The  item with id {item_id} not found")
    update_item = {"id": item_id, **payload.model_dump()}
    DATABASE_MOCK[item_id] = update_item
    return update_item


@router.patch("/{item_id}", response_model=ItemResponse, status_code = status.HTTP_200_OK)
def update_item_partial(item_id: int, payload:ItemUpdate):
    if item_id not in DATABASE_MOCK:
        raise HTTPException(status_code=404, detail=f"Item with id {item_id} not found")
    
    stored_item_data = DATABASE_MOCK[item_id]
    # Exclude_unset = True ignores field that the client didn't pass in the request body
    update_data =  payload.model_dump(exclude_unset = True)
    update_item = {**stored_item_data, **update_data}
    DATABASE_MOCK[item_id] = update_item
    return update_item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    if item_id not in DATABASE_MOCK:
        raise HTTPException(status_code = 404, detail=f"item with id{item_id} not found")
    del DATABASE_MOCK[item_id]
    return None


