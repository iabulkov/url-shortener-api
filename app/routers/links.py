from fastapi import APIRouter, Depends, HTTPException, Request, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional

from app.database import get_db
from app import schemas

router = APIRouter(prefix='/links', tags=['Links'])

@router.get('/test', response_model=None)
async def test_endpoint(db: Session = Depends(get_db)) -> dict:
    result = db.execute(text('SELECT 1')).scalar()
    return {
        'message': 'Links router is working',
        'db_check': result == 1
    }

@router.post('/shorten', response_model=None)
async def create_short_link(
    request: Request,
    link: schemas.LinkCreate,
    db: Session = Depends(get_db)
) -> dict:
    return {
        'original_url': str(link.original_url),
        'short_code': 'test123',
        'short_url': f"{request.base_url}test123"
    }

@router.get('/{short_code}', response_model=None)
async def redirect_to_original(
    short_code: str,
    db: Session = Depends(get_db)
) -> RedirectResponse:
    return RedirectResponse(url='https://example.com')

@router.delete('/{short_code}', response_model=None)
async def delete_link(
    short_code: str,
    db: Session = Depends(get_db)
) -> dict:
    return {'message': f'Link {short_code} deleted'}

@router.put('/{short_code}', response_model=None)
async def update_link(
    request: Request,
    short_code: str,
    link_update: schemas.LinkUpdate,
    db: Session = Depends(get_db)
) -> dict:
    return {
        'short_code': short_code,
        'new_url': str(link_update.original_url)
    }

@router.get('/{short_code}/stats', response_model=None)
async def get_link_stats(
    short_code: str,
    db: Session = Depends(get_db)
) -> dict:
    return {
        'short_code': short_code,
        'clicks': 0,
        'created_at': '2024-01-01T00:00:00'
    }

@router.get('/search', response_model=None)
async def search_links(
    original_url: str = Query(...),
    db: Session = Depends(get_db)
) -> dict:
    return {
        'original_url': original_url,
        'links': []
    }

@router.get('/ping', response_model=None)
async def ping():
    return {'message': 'pong'}