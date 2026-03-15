import re

def fix_links_file():
    filename = 'app/routers/links.py'
    
    print(f"Читаем файл: {filename}")
    
    with open(filename, 'r') as f:
        content = f.read()
    
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
    
    new_content = content
    changes = 0
    
    for func_name, return_type in return_types.items():
        pattern = rf'(async def {func_name}\([^)]*\):)'
        
        def replace_func(match):
            nonlocal changes
            changes += 1
            print(f"Исправлена функция: {func_name}")
            return match.group(1) + return_type + ':'
        
        new_content = re.sub(pattern, replace_func, new_content)
    
    if changes > 0:
        backup = filename + '.backup'
        with open(backup, 'w') as f:
            f.write(content)
        print(f"Создана резервная копия: {backup}")
        
        with open(filename, 'w') as f:
            f.write(new_content)
        print(f"✨ Внесено изменений: {changes}")
    else:
        print("Изменений не требуется")
    
    print("\n📋 Результат:")
    with open(filename, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines, 1):
            if 'async def' in line:
                has_return = '->' in line
                status = "yes" if has_return else "no"
                print(f"{status} Строка {i}: {line.strip()}")

if __name__ == "__main__":
    fix_links_file()