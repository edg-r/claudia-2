#!/usr/bin/env python3
import json
import os
import tomllib

def main():
    workspace_root = "/Users/edgar/Documents/000 Files"
    codex_agents_dir = os.path.join(workspace_root, ".codex", "agents")
    manifest_path = os.path.join(workspace_root, "_claudia", "system", "manifest.json")
    
    if not os.path.exists(codex_agents_dir):
        print(f"Error: Target directory does not exist: {codex_agents_dir}")
        return

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    manifest_agents = {agent["name"].lower(): agent for agent in manifest.get("agents", [])}
        
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
                continue

            name = data["name"]
            agent = manifest_agents.get(name)
            if not agent:
                print(f"❌ {filename}: No matching manifest agent for name '{name}'")
                errors += 1
                continue

            memory = agent.get("memory", "")
            memory_path = os.path.join(workspace_root, memory)
            required_memory = ["AGENT_CONTEXT.md", "FEEDBACK.md", "TASK_LOG.md"]
            missing_memory = [
                item for item in required_memory
                if not os.path.exists(os.path.join(memory_path, item))
            ]
            if missing_memory:
                print(f"❌ {filename}: Missing memory files in {memory}: {missing_memory}")
                errors += 1
                continue

            instructions = data["developer_instructions"]
            if memory and f"Your memory at `{memory}`" not in instructions:
                print(f"❌ {filename}: Runtime context override does not reference manifest memory path {memory}")
                errors += 1
                continue

            print(f"✅ {filename}: Valid TOML and memory path (name: '{name}', memory: '{memory}')")
                
        except tomllib.TOMLDecodeError as e:
            print(f"❌ {filename}: TOML Decoding Error: {e}")
            errors += 1
        except Exception as e:
            print(f"❌ {filename}: Unexpected error: {e}")
            errors += 1
            
    print(f"\nValidation complete. Errors found: {errors}")
    if errors:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
