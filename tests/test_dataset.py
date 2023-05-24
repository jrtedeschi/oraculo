from oraculo.functions.data import get_dummy_dataset, embed_documents, split_text, embed_text
from tqdm import tqdm
import chromadb
from chromadb.config import Settings
import hashlib
import logging
from contextlib import closing

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# data = get_dummy_dataset()        

# new_data = []

# window = 6  # number of sentences to combine
# stride = 3  # number of sentences to 'stride' over, used to create overlap

# print("Combining documents...")
# for i in tqdm(range(0, len(data), stride)):
#     i_end = min(len(data)-1, i+window)
#     if data[i]['title'] != data[i_end]['title']:
#         # in this case we skip this entry as we have start/end of two videos
#         continue
#     text = ' '.join(data[i:i_end]['text'])
#     new_data.append({
#         'start': data[i]['start'],
#         'end': data[i_end]['end'],
#         'title': data[i]['title'],
#         'text': text,  
#         'id': hashlib.md5(data[i]['id'].encode("utf-8")).hexdigest(),
#         'source_url': data[i]['url'],
#         'published': data[i]['published']
#     })


client = chromadb.Client(Settings(persist_directory=".chromadb", chroma_db_impl="duckdb+parquet"))
# collection = client.create_collection("youtube-transcriptions")
# client.create_collection("youtube-transcriptions")

# client.delete_collection("youtube-transcriptions")

# print("Embedding documents...")
# for i in tqdm(range(0, 30)):
#     new_data[i].update({'embeddings': embed_text(new_data[i]['text'])})

# update new_data to range 200

collection = client.get_collection("youtube-transcriptions")

# collection.add(
#     ids=[doc['id'] for doc in new_data],
#     metadatas=[{'start': doc['start'], 'end': doc['end'], 'title': doc['title'], 'source_url': doc['source_url'], 'published': doc['published']} for doc in new_data],
#     documents=[doc['text'] for doc in new_data],
# )

print(collection.query(query_texts=["what is Openai CLIP?"], n_results=5))


# del client
# del collection
