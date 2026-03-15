import re

with open('app/routers/links.py', 'r') as f:
    content = f.read()

pattern = r'(async def (\w+)\([^)]*\):\s*\n\s+""")'
matches = re.findall(pattern, content)

for match in matches:
    func_name = match[1]
    print(f"Найдена функция без возвращаемого типа: {func_name}")
    
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
    
    if func_name in return_types:
        old = f'async def {func_name}('
        new = f'async def {func_name}(' + return_types[func_name] + ':'
        content = content.replace(old, new)
        print(f"  Исправлено: {old} -> {new}")

with open('app/routers/links_fixed.py', 'w') as f:
    f.write(content)

print("\nФайл сохранен как app/routers/links_fixed.py")
print("Проверьте его и переименуйте в links.py если всё ок")