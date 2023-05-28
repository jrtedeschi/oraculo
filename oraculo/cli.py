import typer
import subprocess
import chromadb
from chromadb.config import Settings
from rich import print
from pathlib import Path
import yaml
from oraculo.functions.audio import audio_to_text
from oraculo.functions.data import create_embeddings, get_collections
from typing_extensions import Annotated
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)

APP_NAME = "oraculo"
app = typer.Typer()

app_dir = typer.get_app_dir(APP_NAME)
config_path: Path = Path(app_dir) / "config/config.yaml"

Collections = Enum("Collections", get_collections())


@app.command()
def transcribe(
    embeddings: Annotated[
        bool,
        typer.Option(
            help="Create embeddings from the segments of the transcription and persists them to a vector database."
        ),
    ] = False,
):
    path = typer.prompt("Path to audio file: ", default=None)
    language = typer.prompt("Input Audio Language: ", default="pt")
    model = typer.prompt("Model: ", default="base")
    output = typer.prompt("Output file: ", default=None)
    metadata = {}

    if embeddings:
        embeddings = typer.confirm("Create embeddings? ", default=True)
        if Collections == []:
            typer.echo("No collections found.")
            create = typer.confirm("Create new collection? ", default=True)
            if create:
                collection = typer.prompt("Set Collection: ", default=None)
                if collection not in Collections:
                    typer.echo("Collection does not exist. Creating new collection.")
                metadata = {"collection_name": collection}
            else:
                collection = typer.prompt("Set Collection: ", type=str)
                metadata = {"collection_name": collection}
        else:
            collection = typer.prompt("Set Collection: ", type=str)
            metadata = {"collection_name": collection}

    else:
        embeddings = False

    typer.echo("Transcribing... :floppy_disk:")
    audio_to_text(path, language, model, output, embeddings, metadata)


@app.command()
def webapp():
    subprocess.run(["streamlit", "run", "oraculo/webapp/hello_world.py"])


if __name__ == "__main__":
    app()
