import argparse
import json
import os
import glob
from jinja2 import Environment, FileSystemLoader
from simple_term_menu import TerminalMenu

# Set up Jinja2 environment
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def prompt_user(prompt, choices=None, default=None):
    if choices:
        menu = TerminalMenu(choices, title=f"#### {prompt} ####")
        selected_index = menu.show()
        return choices[selected_index]
    else:
        user_input = input(f"#### {prompt} [{default}] ####: ")
        return user_input.strip() or default

def update_program_file(program_path, context):
    with open(program_path, 'r') as f:
        lines = f.readlines()

    new_service_line = f"builder.Services.AddScoped<I{context['prefix']}{context['module']}{context['suffix']}Service, {context['prefix']}{context['module']}{context['suffix']}Service>();\n"
    new_repository_line = f"builder.Services.AddScoped<I{context['prefix']}{context['module']}{context['suffix']}Repository, {context['prefix']}{context['module']}{context['suffix']}Repository>();\n"

    # Check if service and repository already exist
    if new_service_line in lines or new_repository_line in lines:
        return  # Prevent duplicates

    # Find the correct location to insert dependencies
    insert_index = None
    for i, line in enumerate(lines):
        if "// Register dependencies" in line:
            insert_index = i + 1
            break

    # If "// Register dependencies" not found, add it before the app.Build()
    if insert_index is None:
        for i, line in enumerate(lines):
            if "var app = builder.Build();" in line:
                insert_index = i
                lines.insert(i, "\n// Register dependencies\n")
                break

    # Insert new dependencies
    lines.insert(insert_index, new_service_line)
    lines.insert(insert_index + 1, new_repository_line)

    # Write updated content back
    with open(program_path, 'w') as f:
        f.writelines(lines)

    print(f"Updated {program_path} with new dependencies.")

def get_template_env(tech_stack):
    template_folder = os.path.join(BASE_DIR, 'templates', tech_stack)
    return Environment(loader=FileSystemLoader(template_folder))

# Function to generate code from template
def generate_code(template_env, template_name, output_path, context):
    template = template_env.get_template(template_name)
    content = template.render(context)

    # Ensure Program.cs is placed at the root output directory
    if "Program" in output_path:
        program_path = os.path.join(os.path.dirname(output_path), "Program.cs")
        if os.path.exists(program_path):
            print(f"Updating existing Program.cs instead of overwriting: {program_path}")
            update_program_file(program_path, context)
        else:
            with open(program_path, 'w') as f:
                f.write(content)
            print(f"Generated: {program_path}")
    else:
        with open(output_path, 'w') as f:
            f.write(content)
        print(f"Generated: {output_path}")

# Parse JSON schema with error handling
def parse_json_schema(schema_path):
    try:
        with open(schema_path, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error loading schema: {e}")
        exit(1)

# Interactive CLI setup
def main():
    print("""
    \n
           M E T L I F E
           E \         E \ \r
           T   \       T   \ \r
           L     M E T L I F E
           I     E     I     E
           F     T     F     T
           M E T L I F E     L
             \   I       \   I
               \ F         \ F
                 M E T L I F E \n

    \r ###########################################
    \r ### [Internal Tool Code Generator v0.1] ###
    \r ###########################################
    \n
    """)
    tech_stack = prompt_user("Select tech stack", ["netcore", "nestjs", "nano"], "netcore")
    
    module_name = input("Enter module name [Customer]: ") or "Customer"
    
    # Detect and list all .json files for entity selection
    json_files = glob.glob("*.json")
    if json_files:
        entity_path = prompt_user("Select a JSON schema file", json_files)
    else:
        entity_path = prompt_user("Enter path to JSON schema", default="entity.json")

    file_ext = "cs" if tech_stack == "netcore" else "ts"
    output_dir = input(f"Enter output directory [{os.path.join(BASE_DIR, 'output')}]: ") or os.path.join(BASE_DIR, 'output')
    
    schema = parse_json_schema(entity_path)
    module_output_dir = os.path.join(output_dir, module_name)
    os.makedirs(module_output_dir, exist_ok=True)
    
    prefix = input("Enter class prefix (leave blank for none): ") or ""
    suffix = input("Enter class suffix (leave blank for none): ") or ""
    
    template_env = get_template_env(tech_stack)
    
    context = {
        'module': module_name,
        'fields': schema['fields'],
        'prefix': prefix,
        'suffix': suffix
    }
    
    template_mappings = {
        'netcore': {
            'program.cs.j2': '../Program',
            'controller.cs.j2': 'Controllers/controller',
            'service.cs.j2': 'Services/service',
            'repository.cs.j2': 'Repositories/repository',
            'entity.cs.j2': 'Models/entity',
            'test_controller.cs.j2': 'Tests/test_controller',
            'test_service.cs.j2': 'Tests/test_service',
            'test_repository.cs.j2': 'Tests/test_repository',
            'test_entity.cs.j2': 'Tests/test_entity'
        },
        'nestjs': {
            'controller.ts.j2': 'controllers/controller',
            'service.ts.j2': 'services/service',
            'repository.ts.j2': 'repositories/repository',
            'entity.ts.j2': 'models/entity',
            'test_controller.ts.j2': 'tests/test_controller',
            'test_service.ts.j2': 'tests/test_service',
            'test_repository.ts.j2': 'tests/test_repository',
            'test_entity.ts.j2': 'tests/test_entity'
        },
        'nano': {
            'controller.ts.j2': 'controllers/controller',
            'service.ts.j2': 'services/service',
            'repository.ts.j2': 'repositories/repository',
            'entity.ts.j2': 'models/entity',
            'test_controller.ts.j2': 'tests/test_controller',
            'test_service.ts.j2': 'tests/test_service',
            'test_repository.ts.j2': 'tests/test_repository',
            'test_entity.ts.j2': 'tests/test_entity'
        }
    }

    templates = template_mappings.get(tech_stack, {})
    
    for template_file, output_name in templates.items():
        output_path = os.path.join(module_output_dir, output_name + f'.{file_ext}')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        generate_code(template_env, template_file, output_path, context)

if __name__ == '__main__':
    main()
