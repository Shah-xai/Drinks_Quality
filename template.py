import os
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S"
)
project_name="drinks_quality"
list_of_files=[
    ".github/workflows/main.yaml",
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/utils/common.py",
    f"src/{project_name}/config/__init__.py",
    f"src/{project_name}/config/configuration.py",
    f"src/{project_name}/pipeline/__init__.py",
    f"src/{project_name}/entity/__init__.py",
    f"src/{project_name}/entity/config_entity.py",
    f"src/{project_name}/constants/__init__.py",
    "config.yaml",
    "params.yaml",
    "schema.yaml",
    "main.py",
    "setup.py",
    "Dockerfile",
    "tests/test_workflow.py",
    "Research/EDA.ipynb"
]

for file in list_of_files:
    filepath=Path(file)
    filedir,filename=os.path.split(filepath)
    if file.endswith("/") or (not filepath.suffix):
        os.makedirs(filepath,exist_ok=True)
        logging.info(f"Creating directory: {filepath}")
    else:
        if filedir!="":
           os.makedirs(filedir,exist_ok=True)
           logging.info(f"Creating directory {filedir} for the file: {filename}")
        if ( not os.path.exists(filepath)) or (os.path.getsize(filepath)==0):
            with open(filepath,"w") as f:
                pass
                logging.info(f"Creating empty file: {filepath}")
        else:
            logging.info(f"{filename}  already exists")
          