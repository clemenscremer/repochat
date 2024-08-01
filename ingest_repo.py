import os
import requests
import git
from urllib.parse import urlparse
import nbformat
import shutil

def build_overview(repo_path):
    """This function traverses the directory structure and builds a hierarchical overview of the files and folders."""
    overview = []
    for root, dirs, files in os.walk(repo_path):
        level = root.replace(repo_path, '').count(os.sep)
        indent = ' ' * 4 * level
        overview.append(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            overview.append(f"{subindent}{f}")
    return "\n".join(overview)

def ingest_repository(repo_url_or_path, output_string):
    if repo_url_or_path.startswith('http'):
        # Clone the GitHub repository
        repo = git.Repo.clone_from(repo_url_or_path, 'temp_repo')
        repo_path = repo.working_dir
    else:
        repo_path = repo_url_or_path

    # Build and append the overview to the output_string
    overview = build_overview(repo_path)
    output_string += "--- Repository Overview ---\n"
    output_string += overview + "\n\n"

    for root, dirs, files in os.walk(repo_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_name, file_ext = os.path.splitext(file)
            if file_ext == '.ipynb':
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    notebook = nbformat.read(f, nbformat.NO_CONVERT)
                    for cell in notebook.cells:
                        if cell.cell_type in ['code', 'markdown']:
                            output_string += f"--- {file_path} ---\n{cell.source}\n\n"
            elif file_ext in ['.py', '.md', '.yaml', '.txt']:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    file_content = f.read()
                    output_string += f"--- {file_path} ---\n{file_content}\n\n"

    if repo_url_or_path.startswith('http'):
        # Clean up the temporary repository
        shutil.rmtree(repo_path)

    return output_string