from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from modules.items.schemas import ItemCreate, ItemResponse, ItemUpdate
from core.database import get_db
from sqlalchemy.orm import Session
from modules.items.models import ItemModel

router = APIRouter(
    prefix="/items", tags=["Items Management"]
)

#In-memory mock database simulation



@router.get("/", response_model=List[ItemResponse], status_code=status.HTTP_200_OK)
def get_all_items(db: Session = Depends(get_db)):
    return db.query(ItemModel).all()


@router.get("/{item_id}", response_model=ItemResponse, status_code=status.HTTP_200_OK)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )
    return item



@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def update_item_complete( payload: ItemCreate, db: Session = Depends(get_db)):
    db_item = ItemModel(**payload.model_dump())
    db.add(db_item) #stage the change
    db.commit()  #write to disk
    db.refresh(db_item)
    return db_item


@router.put("/{item_id}", response_model=ItemResponse, status_code=status.HTTP_200_OK)
def update_item_complete(item_id: int, payload:ItemUpdate,  db: Session = Depends(get_db)):
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail=f"The  item with id {item_id} not found")
    item.name = payload.name
    item.description = payload.description
    item.price = payload.price
    item.buyer = payload.buyer
    
    db.commit()
    db.refresh(item)
    return item



@router.patch("/{item_id}", response_model=ItemResponse, status_code=status.HTTP_200_OK)
def update_item_partial(item_id: int, payload: ItemUpdate, db: Session = Depends(get_db)):
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if item is None:
        raise HTTPException(status_code= 404, detail=f"Item with if {item_id} not found")
    
    #Get  only the fields the client
    update_data = payload.model_dump(exclude_unset=True)
    
    #update the model instance
    for field, value in update_data.items():
        setattr(item, field, value)
        
    #save changes
    db.commit()
    
    # Refresh the instance with the latest data from the database
    db.refresh(item)
    return item
    



@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if item is None:
        raise HTTPException(status_code = 404, detail=f"item with id{item_id} not found")
    db.delete(item)
    db.commit
    return None


