from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from modules.items.schemas import ItemCreate, ItemResponse, ItemUpdate
from core.database import get_db, MockDatabaseSession

router = APIRouter(
    prefix="/items", tags=["Items Management"]
)

#In-memory mock database simulation



@router.get("/", response_model=List[ItemResponse], status_code=status.HTTP_200_OK)
def get_all_items(db: MockDatabaseSession = Depends(get_db)):
    return list (db.data.values())


@router.get("/{item_id}", response_model=ItemResponse, status_code=status.HTTP_200_OK)
def get_item(item_id: int, db: MockDatabaseSession = Depends(get_db)):
    if item_id not in db.data:
        raise HTTPException(status_code=404, detail=f"item with {item_id} not found")
    return db.data[item_id]



@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def update_item_complete( payload: ItemCreate, db: MockDatabaseSession = Depends(get_db)):
    db.counter += 1
    new_item = {"id":db.counter, **payload.model_dump()}
    db.data[db.counter] = new_item
    return new_item


@router.put("/{item_id}", response_model=ItemResponse, status_code=status.HTTP_200_OK)
def update_item_complete(item_id: int, payload:ItemUpdate, db: MockDatabaseSession = Depends(get_db)):
    if item_id not in db.data:
        raise HTTPException(status_code=404, detail=f"The  item with id {item_id} not found")
    update_item = {"id": item_id, **payload.model_dump()}
    db.data[item_id] = update_item
    return update_item


@router.patch("/{item_id}", response_model=ItemResponse, status_code = status.HTTP_200_OK)
def update_item_partial(item_id: int, payload:ItemUpdate, db: MockDatabaseSession = Depends(get_db)):
    if item_id not in db.data:
        raise HTTPException(status_code=404, detail=f"Item with id {item_id} not found")
    
    stored_item_data = db.data[item_id]
    # Exclude_unset = True ignores field that the client didn't pass in the request body
    update_data =  payload.model_dump(exclude_unset = True)
    update_item = {**stored_item_data, **update_data}
    db.data[item_id] = update_item
    return update_item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: MockDatabaseSession = Depends(get_db)):
    if item_id not in db.data:
        raise HTTPException(status_code = 404, detail=f"item with id{item_id} not found")
    del db.data[item_id]
    return None


