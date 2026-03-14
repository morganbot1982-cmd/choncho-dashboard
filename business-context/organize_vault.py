import os
import shutil
from pathlib import Path

# --- CONFIGURATION ---
# Set this to the folder you want to clean up. "." means current folder.
SOURCE_DIR = Path(".") 
VAULT_NAME = "AI_VAULT"

# Define the "Logic Folders" for the AI Agent
MAP = {
    "FINANCE": [".csv", ".xlsx", ".json", "invoice", "receipt", "p&l", "tax"],
    "LEGAL": [".pdf", ".docx", "contract", "agreement", "terms", "policy"],
    "LOGISTICS": ["shipping", "manifest", "bol", "tracking", "supplier", "factory"],
    "CLIENT_DATA": ["project", "brief", "client", "booking", "feedback"],
    "STRATEGY": [".md", ".txt", "plan", "memo", "notes", "audit"]
}

def organize_vault():
    vault_path = SOURCE_DIR / VAULT_NAME
    vault_path.mkdir(exist_ok=True)

    # Create subdirectories
    for folder in MAP.keys():
        (vault_path / folder).mkdir(exist_ok=True)

    print(f"--- Starting AI Vault Organization in {SOURCE_DIR.absolute()} ---")

    for file_path in SOURCE_DIR.iterdir():
        # Skip directories and the script itself
        if file_path.is_dir() or file_path.name == __file__:
            continue

        filename_lower = file_path.name.lower()
        extension = file_path.suffix.lower()
        moved = False

        # Sort based on extension or keywords in the filename
        for folder, identifiers in MAP.items():
            if any(id_ in filename_lower for id_ in identifiers) or extension in identifiers:
                dest = vault_path / folder / file_path.name
                shutil.move(str(file_path), str(dest))
                print(f"[MOVED] {file_path.name} -> {folder}")
                moved = True
                break
        
        if not moved:
            # Move unknown files to an 'UNCATEGORIZED' folder for manual review
            un_dir = vault_path / "UNCATEGORIZED"
            un_dir.mkdir(exist_ok=True)
            shutil.move(str(file_path), un_dir / file_path.name)
            print(f"[?] {file_path.name} -> UNCATEGORIZED (Check keywords)")

    print("\n--- Organization Complete. Point OpenClaw to the 'AI_VAULT' folder. ---")

if __name__ == "__main__":
    organize_vault()
