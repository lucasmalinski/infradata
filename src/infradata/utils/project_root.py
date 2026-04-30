from pathlib import Path

def find_project_root(start: __file__, debug=False) -> Path: 
    start = Path(start)
    current = start.resolve()
    while current != current.parent:
        if (current / "pyproject.toml").exists() or (current / ".env").exists():
            if debug: 
                print(f"Found project root: {current}")
            return current
        current = current.parent    