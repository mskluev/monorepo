import os
import sys
import yaml
import json

def load_dependencies():
    with open("dependencies.yaml", "r") as f:
        data = yaml.safe_load(f)
    return data.get("dependencies", {})

def get_changed_files():
    # In actual CI, we would run `git diff --name-only ...`
    # Here we accept an argument or env var for testing.
    changed = os.environ.get("CHANGED_FILES", "").split()
    return changed

def get_affected_targets(changed_files, deps):
    affected = set()
    # Simple dependency resolution
    # Map component -> dependents
    # The dependencies.yaml is component -> dependents
    
    # Check direct hits
    for file in changed_files:
        for component, dependents in deps.items():
            if file.startswith(component):
                affected.add(component)
                # Add dependents (1 level deep for demo, ideally recursive)
                for dep in dependents:
                   affected.add(dep)
                   
    return list(affected)

def generate_pipeline(affected_targets):
    # Base structure
    pipeline = {
        "stages": ["build", "test"], 
        "jobs": {} # We will put jobs here but GitLab expects top-level keys
    }
    
    gitlab_jobs = {}
    
    for target in affected_targets:
        job_name = target.replace("/", "-")
        
        if target.startswith("go/"):
            gitlab_jobs[f"build-{job_name}"] = {
                "stage": "build",
                "image": "golang:1.21",
                "script": [
                    f"cd {target}",
                    "go build ./..."
                ]
            }
        elif target.startswith("python/"):
             gitlab_jobs[f"test-{job_name}"] = {
                "stage": "test",
                "image": "python:3.12",
                "script": [
                    "pip install uv", 
                    f"cd {target}",
                    "uv sync",
                    # Adjust command based on type
                    "uv run pytest" if "libs" in target else "uv run fanout" # simplified logic
                ]
            }
            
    # Return directly the jobs dict which is valid GitLab CI YAML
    # (plus stages if needed, but child pipelines often just have jobs)
    # Actually, child pipelines support full syntax.
    final_pipeline = {
        "stages": ["build", "test"],
        **gitlab_jobs
    }
        
    return final_pipeline

def main():
    deps = load_dependencies()
    changed_files = get_changed_files()
    if not changed_files:
        print("No changes detected.", file=sys.stderr)
        # Output empty pipeline or valid dummy
        print(yaml.dump({"stages": ["dummy"], "dummy": {"stage": "dummy", "script": ["echo no changes"]}}))
        return

    targets = get_affected_targets(changed_files, deps)
    print(f"Affected targets: {targets}", file=sys.stderr)
    
    pipeline = generate_pipeline(targets)
    print(yaml.dump(pipeline))

if __name__ == "__main__":
    main()
