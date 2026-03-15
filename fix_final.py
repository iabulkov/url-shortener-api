import re

def fix_links_file():
    filename = 'app/routers/links.py'
    
    with open(filename, 'r') as f:
        content = f.read()
    
    problem_functions = [
        'create_short_link',
        'redirect_to_original',
        'delete_link',
        'update_link',
        'get_link_stats',
        'search_links',
        'cleanup_unused_links',
        'get_expired_links_history',
        'get_popular_links',
        'refresh_link_expiration'
    ]
    
    new_content = content
    changes = 0
    
    for func_name in problem_functions:
        pattern = rf'(@router\.(get|post|put|delete)\("[^"]*"(?:, [^)]*)?)\n\s*async def {func_name}'
        
        def add_response_model(match):
            nonlocal changes
            decorator = match.group(1)
            if 'response_model=' not in decorator:
                if ', ' in decorator:
                    new_decorator = decorator.replace(', ', ', response_model=None, ')
                else:
                    new_decorator = decorator.replace('")', '", response_model=None)')
                
                print(f" Добавлен response_model=None для {func_name}")
                changes += 1
                return new_decorator + '\n    async def ' + func_name
            return match.group(0)
        
        new_content = re.sub(pattern, add_response_model, new_content, flags=re.MULTILINE)
    
    if changes > 0:
        backup = filename + '.final.backup'
        with open(backup, 'w') as f:
            f.write(content)
        print(f" Создана резервная копия: {backup}")
        
        with open(filename, 'w') as f:
            f.write(new_content)
        print(f"Внесено изменений: {changes}")
    else:
        print("Изменений не требуется")

if __name__ == "__main__":
    fix_links_file()