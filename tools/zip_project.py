import os
import zipfile

EXCLUDE_DIRS = {"generated_images", "venv", "__pycache__", ".git", ".idea", ".tox", ".eggs", "build", "dist", "docs", "tests", "test", "examples", ".pytest_cache", ".mypy_cache"}
EXCLUDE_SUFFIXES = (".pyc", ".egg-info", ".log", ".jsonl")
EXCLUDE_FILES = (".DS_Store", "LICENSE", ".gitignore")

def should_exclude(path):
    parts = path.split(os.sep)
    return any(part in EXCLUDE_DIRS or part.endswith(EXCLUDE_SUFFIXES) for part in parts)

def zip_project_directory(source_dir: str, output_filename: str = "clipper.zip"):
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            # Remove excluded directories from the walk
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.endswith(EXCLUDE_SUFFIXES)]
            for file in files:
                if file in EXCLUDE_FILES or file.endswith(EXCLUDE_SUFFIXES):
                    continue
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, source_dir)
                if should_exclude(rel_path):
                    continue
                zipf.write(full_path, rel_path)
    print(f"✅ Project zipped to {output_filename}")

# Example usage
if __name__ == "__main__":
    zip_project_directory(".")
