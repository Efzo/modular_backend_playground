from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from modules.items.schemas import ItemCreate, ItemResponse, ItemUpdate
from core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from modules.items.models import ItemModel

router = APIRouter(
    prefix="/items", tags=["Items Management"]
)

#In-memory mock database simulation



@router.get("/", response_model=List[ItemResponse], status_code=status.HTTP_200_OK)
async def get_all_items(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ItemModel))
    return result.scalars().all()  #extract rows into clean python objects


@router.get("/{item_id}", response_model=ItemResponse, status_code=status.HTTP_200_OK)
async def get_item(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ItemModel).filter(ItemModel.id == item_id))
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )
    return item



@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def update_item_complete( payload: ItemCreate, db: AsyncSession = Depends(get_db)):
    db_item = ItemModel(**payload.model_dump())
    db.add(db_item) #stage the change
    await db.commit()  #write to disk
    await db.refresh(db_item)
    return db_item


@router.put("/{item_id}", response_model=ItemResponse, status_code=status.HTTP_200_OK)
async def update_item_complete(item_id: int, payload:ItemUpdate,  db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ItemModel).filter(ItemModel.id == item_id))
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail=f"The  item with id {item_id} not found")
    item.name = payload.name
    item.description = payload.description
    item.price = payload.price
    item.buyer = payload.buyer
    
    await db.commit()
    await db.refresh(item)
    return item



@router.patch("/{item_id}", response_model=ItemResponse, status_code=status.HTTP_200_OK)
async def update_item_partial(item_id: int, payload: ItemUpdate, db: AsyncSession = Depends(get_db)):
    result =  await db.execute(select(ItemModel).filter(ItemModel.id == item_id))
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code= 404, detail=f"Item with if {item_id} not found")
    
    #Get  only the fields the client
    update_data = payload.model_dump(exclude_unset=True)
    
    #update the model instance
    for field, value in update_data.items():
        setattr(item, field, value)
        
    #save changes
    await db.commit()
    
    # Refresh the instance with the latest data from the database
    await db.refresh(item)
    return item
    



@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ItemModel).filter(ItemModel.id == item_id))
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code = 404, detail=f"item with id{item_id} not found")
    await db.delete(item)
    await db.commit()
    return None


