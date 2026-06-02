#!/usr/bin/env python3
import os
import re
import json

def parse_frontmatter_and_body(content):
    # Match frontmatter at the very beginning of the file
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
    if not match:
        raise ValueError("Could not find valid frontmatter delimiters at the start of the file.")
    
    frontmatter_text = match.group(1).strip()
    body_text = match.group(2).strip()
    
    # Parse frontmatter line by line to handle multiline description
    frontmatter = {}
    current_key = None
    description_lines = []
    
    for line in frontmatter_text.splitlines():
        # Check if line is indented, indicating continuation of the description
        if current_key == "description" and (line.startswith("  ") or line.startswith("\t")):
            description_lines.append(line.strip())
        else:
            match = re.match(r'^([^:]+):\s*(.*)$', line)
            if match:
                key = match.group(1).strip()
                val = match.group(2).strip()
                frontmatter[key] = val
                current_key = key
                if key == "description":
                    description_lines = [val]
            else:
                current_key = None
                
    if "description" in frontmatter:
        # Join multiline description with a space
        frontmatter["description"] = " ".join(description_lines).replace('"', '\\"')
        
    return frontmatter, body_text

def main():
    workspace_root = "/Users/edgar/Documents/000 Files"
    definitions_dir = os.path.join(workspace_root, "_claudia", "agent_definitions")
    codex_agents_dir = os.path.join(workspace_root, ".codex", "agents")
    manifest_path = os.path.join(workspace_root, "_claudia", "system", "manifest.json")
    
    # Create target directory if it doesn't exist
    os.makedirs(codex_agents_dir, exist_ok=True)
    print(f"Ensured directory exists: {codex_agents_dir}")
    
    # Load manifest to get exact memory paths
    agent_memory_map = {}
    if os.path.exists(manifest_path):
        try:
            with open(manifest_path, "r", encoding="utf-8") as f_manifest:
                manifest_data = json.load(f_manifest)
                for agent in manifest_data.get("agents", []):
                    agent_memory_map[agent["name"].lower()] = agent.get("memory", "")
            print(f"Successfully loaded {len(agent_memory_map)} agent memory paths from manifest.")
        except Exception as e:
            print(f"Warning: Failed to load manifest memory paths: {e}")
    else:
        print(f"Warning: Manifest not found at {manifest_path}")
    
    if not os.path.exists(definitions_dir):
        print(f"Error: Agent definitions directory not found at {definitions_dir}")
        return
        
    files = [f for f in os.listdir(definitions_dir) if f.endswith(".md")]
    print(f"Found {len(files)} agent definition files.")
    
    for filename in sorted(files):
        filepath = os.path.join(definitions_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        try:
            frontmatter, body = parse_frontmatter_and_body(content)
            
            # Use name from frontmatter or fall back to file basename
            proper_name = frontmatter.get("name", os.path.splitext(filename)[0].capitalize())
            lowercase_name = proper_name.lower()
            description = frontmatter.get("description", "")
            
            # Look up memory path from manifest map
            memory_path = agent_memory_map.get(lowercase_name, f"_claudia/agents/{lowercase_name}/")
            
            # Format custom context loading constraints. This appended block is
            # intentionally later than the source definition so Codex runtime
            # context loading stays narrow even when older definitions contain
            # broad SOP-loading language.
            context_loading_directive = f"""
## Codex Runtime Context Override

When operating as this custom Claudia subagent in Codex, hyperfocus on your own agent context. This section controls Codex runtime context loading and overrides broader source-definition language such as "read and comply with all SOPs" when deciding what to load by default.

Default loading order:
1. This custom subagent configuration, which is already loaded as your agent definition.
2. Your memory at `{memory_path}`: load `AGENT_CONTEXT.md` and `FEEDBACK.md` first.
3. `TASK_LOG.md` only selectively by tail, search, or relevance unless the task requires full history.
4. Task-specific files, folders, connectors, and constraints supplied in Claudia's dispatch packet.
5. Task-specific SOP or workflow excerpts only as needed to act safely.

Do not load by default:
- `_claudia/system/CLAUDIA.md`.
- `_claudia/system/CLAUDIA_SOUL.md`.
- Legacy `CLAUDE.md`.
- The full `_claudia/system/manifest.json`.
- The full `_claudia/system/CODEX_WORKFLOW.md`.
- All SOPs in `_claudia/sop/`.
- Memory folders, logs, or context files belonging to other agents.
- The full `_claudia/memory/preferences.md`; parent Claudia should supply relevant preferences, and you should load preferences only when needed for the scoped task.

If earlier source-definition text says to read all SOPs, follow all SOPs, or load broad preferences, interpret that in Codex runtime as: load only the task-specific SOP, workflow, or preference excerpt required for this dispatch.
"""
            # Append context directive to instructions body
            body_with_directive = body + "\n" + context_loading_directive
            
            # Format the TOML content
            escaped_body = body_with_directive.replace('"""', '\\"\\"\\"')
            
            toml_content = f"""# Codex Custom Subagent Configuration for {proper_name}
# Automatically generated from {os.path.relpath(filepath, workspace_root)}

name = "{lowercase_name}"
description = "{description}"
nickname_candidates = ["{proper_name}"]

developer_instructions = \"\"\"
{escaped_body}
\"\"\"
"""
            # Write TOML file
            toml_filename = f"{lowercase_name}.toml"
            toml_filepath = os.path.join(codex_agents_dir, toml_filename)
            with open(toml_filepath, "w", encoding="utf-8") as f_out:
                f_out.write(toml_content)
                
            print(f"Generated {os.path.relpath(toml_filepath, workspace_root)}")
            
        except Exception as e:
            print(f"Failed to process {filename}: {e}")

if __name__ == "__main__":
    main()
