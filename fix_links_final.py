# fix_links_final.py
import re

def fix_file(filename):
    with open(filename, 'r') as f:
        content = f.read()
    
    # Словарь функций и их возвращаемых типов
    return_types = {
        'create_short_link': ' -> schemas.LinkResponse',
        'redirect_to_original': ' -> RedirectResponse',
        'delete_link': ' -> dict',
        'update_link': ' -> schemas.LinkResponse',
        'get_link_stats': ' -> schemas.LinkStats',
        'search_links': ' -> schemas.LinkSearchResponse',
        'cleanup_unused_links': ' -> dict',
        'get_expired_links_history': ' -> list[schemas.LinkStats]',
        'get_popular_links': ' -> list',
        'refresh_link_expiration': ' -> dict',
    }
    
    changes = 0
    for func_name, return_type in return_types.items():
        # Ищем объявление функции без возвращаемого типа
        pattern = rf'(async def {func_name}\([^)]*\):)'
        replacement = rf'\1{return_type}:'
        
        new_content, count = re.subn(pattern, replacement, content)
        if count > 0:
            changes += count
            content = new_content
            print(f"✅ Исправлена функция: {func_name}")
    
    if changes > 0:
        with open(filename, 'w') as f:
            f.write(content)
        print(f"\n✨ Внесено изменений: {changes}")
    else:
        print("❌ Ничего не изменено")
    
    return changes

if __name__ == "__main__":
    fix_file('app/routers/links_fixed.py')