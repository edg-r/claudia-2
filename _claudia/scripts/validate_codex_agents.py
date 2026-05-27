#!/usr/bin/env python3
import os
import tomllib

def main():
    workspace_root = "/Users/edgar/Documents/01 Projects/Claudia"
    codex_agents_dir = os.path.join(workspace_root, ".codex", "agents")
    
    if not os.path.exists(codex_agents_dir):
        print(f"Error: Target directory does not exist: {codex_agents_dir}")
        return
        
    files = [f for f in os.listdir(codex_agents_dir) if f.endswith(".toml")]
    print(f"Validating {len(files)} TOML files in {codex_agents_dir}...\n")
    
    errors = 0
    for filename in sorted(files):
        filepath = os.path.join(codex_agents_dir, filename)
        try:
            with open(filepath, "rb") as f:
                data = tomllib.load(f)
                
            # Verify required fields
            required = ["name", "description", "nickname_candidates", "developer_instructions"]
            missing = [field for field in required if field not in data]
            
            if missing:
                print(f"❌ {filename}: Missing required fields: {missing}")
                errors += 1
            else:
                print(f"✅ {filename}: Valid TOML (name: '{data['name']}', nickname: {data['nickname_candidates']})")
                
        except tomllib.TOMLDecodeError as e:
            print(f"❌ {filename}: TOML Decoding Error: {e}")
            errors += 1
        except Exception as e:
            print(f"❌ {filename}: Unexpected error: {e}")
            errors += 1
            
    print(f"\nValidation complete. Errors found: {errors}")

if __name__ == "__main__":
    main()
