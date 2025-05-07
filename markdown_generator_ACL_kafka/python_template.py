import re
import argparse
from jinja2 import Environment, FileSystemLoader

# Incolla qui la tua lista di topic manualmente
topics = [
  
]

# Incolla qui l'output ACL direttamente come stringa
acl_output = """ 
Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=xxxx, patternType=LITERAL)`:
        (principal=User:yyy, host=*, operation=READ, permissionType=ALLOW)


"""

def parse_acl(acl_output):
    """Parsa l'output ACL"""
    acls = []
    current_resource = None

    # Parsea l'output ACL
    for line in acl_output.splitlines():
        resource_match = re.match(r"Current ACLs for resource `ResourcePattern\(resourceType=(.*?), name=(.*?), patternType=(.*?)\)`:", line)
        if resource_match:
            resource_type, name, pattern_type = resource_match.groups()
            current_resource = {
                "resource_type": resource_type,
                "name": name,
                "pattern_type": pattern_type,
                "permissions": []
            }
            acls.append(current_resource)
        else:
            perm_match = re.match(r"\s*\(principal=(.*?), host=(.*?), operation=(.*?), permissionType=(.*?)\)", line)
            if perm_match and current_resource:
                principal, host, operation, permission_type = perm_match.groups()
                current_resource["permissions"].append({
                    "principal": principal,
                    "host": host,
                    "operation": operation,
                    "permission_type": permission_type
                })

    return acls

def generate_markdown(topics, acls, principal, output_filename):
    """Genera un file Markdown con i topic e le ACL"""
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("template.md.j2")
    output = template.render(topics=topics, acls=acls, principal=principal)

    with open(output_filename, "w", encoding="utf-8") as file:
        file.write(output)

    print(f"✔ File Markdown generato: {output_filename}")

def main():
    # Configurazione degli argomenti da linea di comando
    parser = argparse.ArgumentParser(description="Genera un report Markdown con ACL e Topic.")
    parser.add_argument('--output', type=str, required=True, help="Nome del file di output Markdown (es. output.md)")
    parser.add_argument('--principal', type=str, required=True, help="Nome del principal (es. DCC)")
    args = parser.parse_args()

    # Esegui il parsing delle ACL
    acls = parse_acl(acl_output)

    # Genera il Markdown con il nome del file passato come argomento
    generate_markdown(topics, acls, args.principal, args.output)

if __name__ == "__main__":
    main()
