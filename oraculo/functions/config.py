from pathlib import Path
import yaml
import typer



def create_config(config_path : Path):
    typer.echo("Initializing oraculo...")
    persist_directory = typer.prompt("Persist directory: ", default=".chromadb")
    persist_directory = Path(persist_directory)
    chroma_db_impl = typer.prompt(
        "Chroma DB Implementation: ", default="duckdb+parquet"
    )
    config = {
        "chromadb": {
            "persist_directory": persist_directory,
            "chroma_db_impl": chroma_db_impl,
        }
    }
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, "w") as f:
        yaml.dump(config, f)
    print(f"Config file created at {config_path}")
    return config_path