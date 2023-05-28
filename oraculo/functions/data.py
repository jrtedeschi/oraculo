import chromadb
from chromadb.config import Settings
import hashlib
import logging
from contextlib import closing
from tqdm.auto import tqdm

logging.basicConfig(level=logging.INFO)


def name_random_collection() -> str:
    import random
    import string

    return "".join(random.choices(string.ascii_uppercase + string.digits, k=10))


def add_metadata_to_segments(segments: list[dict], metadata: dict = {}):
    for segment in tqdm(segments):
        # generate id
        segment["id"] = hashlib.md5(segment["text"].encode("utf-8")).hexdigest()
        segment.update(metadata)
    return segments


def combine_segments(segments, metadata: dict = {}, window: int = 6, stride: int = 3):
    new_data = []
    for i in tqdm(range(0, len(segments), stride)):
        i_end = min(len(segments) - 1, i + window)
        if segments[i]["title"] != segments[i_end]["title"]:
            # in this case we skip this entry as we have start/end of two videos
            continue
        text = " ".join([t["text"] for t in segments[i:i_end]])

        new_data.append(
            {
                "start": segments[i]["start"],
                "end": segments[i_end]["end"],
                "text": text,
                "id": segments[i]["id"],
                **{k: segments[i][k] for k in metadata.keys()},
            }
        )
    return new_data


def create_embeddings(
    segments: list[dict],
    metadata: dict = {},
    client=None,
):
    if client is None:
        logging.info("Creating new Chroma client")
        client = chromadb.Client(
            Settings(persist_directory=".chromadb", chroma_db_impl="duckdb+parquet")
        )
    # if metadata in empty dict, generate random metadata
    if metadata == {}:
        metadata = {"title": name_random_collection()}
        if "collection_name" not in metadata:
            collection_name = name_random_collection()
            logging.info("Creating new Chroma collection: " + collection_name)
            collection = client.create_or_get_collection(collection_name)
        else:
            collection = client.create_or_get_collection(metadata["collection_name"])
    else:
        collection = client.create_or_get_collection(metadata["collection_name"])

    logging.info("Embedding documents...")
    segments = add_metadata_to_segments(segments, metadata)
    combined_segments = combine_segments(segments, metadata)

    logging.info("Adding documents to collection: " + collection_name)
    collection.add(
        ids=[doc["id"] for doc in combined_segments],
        metadatas=[
            {k: doc[k] for k in metadata.keys() + ["start", "end"]}
            for doc in combined_segments
        ],
        documents=[doc["text"] for doc in combined_segments],
    )

    del client
    del collection

    return segments


def get_collections(client=None):
    if client is None:
        client = chromadb.Client(
            Settings(persist_directory=".chromadb", chroma_db_impl="duckdb+parquet")
        )
        if client.list_collections() == []:
            return []

        collections = [col.name for col in client.list_collections()]
        del client
    return collections
