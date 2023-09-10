from langchain.document_loaders import PyPDFLoader
from pathlib import Path
from oraculo.functions.data import get_collections, check_collection
import uuid
import logging

def read_pdf(path: Path, collection_name: str = None):
    """
    Read a PDF file and convert its pages to JSON format.

    Args:
        path (Path): The path to the PDF file.
        collection_name (str, optional): The name of the collection for metadata (default: None).

    Returns:
        list: A list of JSON representations of the PDF pages.
    """
    # Check if it's a PDF file
    if path.suffix != ".pdf":
        raise TypeError("File is not a pdf")

    path_str = str(path)
    logging.info("Reading pdf: " + path_str)
    
    # Load the PDF
    loader = PyPDFLoader(path_str)
    pages = loader.load_and_split()
    logging.info("Number of pages: " + str(len(pages)))
    
    # Convert pages to JSON
    json_pages = []
    for page in pages:
        page.json(ensure_ascii=False)
        if collection_name is not None:
            page['metadata']['collection_name'] = collection_name
        else: 
            page['metadata']['collection_name'] = path.stem
        json = page.json(ensure_ascii=False)
        json['metadata']['id'] = str(uuid.uuid4())
        json_pages.append(json)
    return json_pages

def read_batch_pdf(paths: list[Path], collection_name: str = None):
    """
    Read a batch of PDF files and convert them to JSON format.

    Args:
        paths (list[Path]): List of paths to PDF files.
        collection_name (str, optional): The name of the collection for metadata (default: None).

    Returns:
        list: A list of lists of JSON representations of PDF pages.
    """
    result = []
    for path in paths:
        result.append(read_pdf(path, collection_name))
    return result

def load_pdf(data: list[dict], client=None):
    """
    Load PDF data into a database collection.

    Args:
        data (list[dict]): List of dictionaries containing PDF data.
        client: A database client object (optional).

    Returns:
        None
    """
    # Split data into text and metadata
    for el in data:
        logging.info("Loading pdf: " + el['metadata']['collection_name'])

        text = el['page_content']
        metadata = el['metadata']
        
        # Create a collection if it does not exist
        logging.info("Creating collection: " + metadata['collection_name'])
        collections = get_collections(client)
        metadata, collection =  check_collection(metadata, client, collections)

        # Add the document to the collection
        logging.info("Adding document to collection: " + metadata['collection_name'])

        collection.add(
            ids=[metadata['id']],
            metadatas=[metadata],
            documents=[text]
        )
