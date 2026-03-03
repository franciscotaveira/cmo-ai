import json
import os
import shutil

# Caminhos
json_file = '/Users/franciscotaveira.ads/Downloads/pharma/antigravity-awesome-skills/skills_index.json'
target_base_dir = '/Users/franciscotaveira.ads/Documents/antigravity-kit/.agent/skills'

def run():
    print(f"Buscando bibliotecas de: {json_file}")
    with open(json_file, 'r', encoding='utf-8') as f:
        skills = json.load(f)

    # Filtrar para não criar pastas vazias/inúteis baseadas em jogos ou sem categoria, se a base for muito grande.
    # Como o usuário quis "tudo", faremos todos independentemente da categoria, mas ignoraremos erros de descrição vazia.
    count = 0
    
    for skill in skills:
        name = skill.get('name', '').strip()
        desc = skill.get('description', '').strip()
        
        if not name or not desc:
            continue
            
        # Ignorar skills muito extensas no nome ou inválidas
        if '/' in name or len(name) > 60:
            continue
            
        target_dir = os.path.join(target_base_dir, name)
        
        # Se o diretorio já existir (como clean-code que já temos), pulamos para não destruir a nossa base
        if os.path.exists(target_dir):
            continue

        os.makedirs(target_dir, exist_ok=True)
        
        skill_file = os.path.join(target_dir, 'SKILL.md')
        
        # Gerando Frontmatter YAML oficial da nossa HIVE
        content = f"---\nname: {name}\ndescription: {desc}\n---\n\n# {name.title()}\n\n{desc}\n"
        
        with open(skill_file, 'w', encoding='utf-8') as sf:
            sf.write(content)
            
        count += 1
        
    print(f"Sucesso. {count} novas Awesome Skills foram injetadas taticamente na mente colmeia.")

if __name__ == '__main__':
    run()
