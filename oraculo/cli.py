import typer
import subprocess
import chromadb
from chromadb.config import Settings
from rich import print
from pathlib import Path
import yaml

APP_NAME = "oraculo"
app = typer.Typer()

app_dir = typer.get_app_dir(APP_NAME)
config_path: Path = Path(app_dir)/ "config/config.yaml"

@app.command()
def init():
    print(":crystal_ball: Hi there, this is [bold blue]Mana![/bold blue]")
    if not config_path.is_file():
        print("Config file doesn't exist yet")
        print("Creating config file... Just click [bold]Enter[/bold] if you want to use the default values")
        project_name = typer.prompt("Name of the project: ", default="My Project")
        db_folder = typer.prompt("Database folder: ", default=None)
        download_dummy_data = typer.confirm("Download dummy data? ", default=True)

        config = {
            "project_name": project_name,
            "download_dummy_data": download_dummy_data,
            "database" : {"folder": db_folder,},
            "webapp": {"port": 8501}
        }   
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, "w") as f:
            yaml.dump(config, f)
        print(f":sparkles: Config file created at {config_path}")
    else:
        print(f":check_mark_button: Config file already exists at {config_path}")

@app.command()
def webapp():
    subprocess.run(["streamlit", "run", "webapp/hello_world.py"])


@app.command()
def vectordb():
    # initialize the database
    with open(config_path, "r") as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)

    client = chromadb.Client(Settings(
        chroma_db_impl="duckdb+parquet",))
    

    
if __name__ == "__main__":
    app()