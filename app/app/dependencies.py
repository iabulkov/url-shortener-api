from fastapi import Request, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from app import models

def get_optional_user(request: Request, db: Session) -> Optional[models.User]:
    """Получение пользователя из токена, если он есть (для необязательной аутентификации)"""
    authorization = request.headers.get("Authorization")
    if not authorization or not authorization.startswith("Bearer "):
        return None
    
    from app.auth import get_current_user
    import asyncio
    
    try:
        token = authorization.replace("Bearer ", "")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        user = loop.run_until_complete(get_current_user(token, db))
        loop.close()
        return user
    except:
        return None

def check_link_ownership(link: models.Link, user: Optional[models.User]):
    """Проверка прав на изменение/удаление ссылки"""
    if link.owner_id and (not user or user.id != link.owner_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to modify this link"
        )
    return True