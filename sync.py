import os
import hashlib
from constants import APIKEY, DATA_DIRECTORY,PERSIST
from langchain.indexes import VectorstoreIndexCreator
from langchain.embeddings.openai import OpenAIEmbeddings
from funcoms import get_loader_cls

def update_index_if_needed(data_directory, index_file_path, hash_file_path, openai_api_key):
    current_hash = get_data_hash(data_directory)
        # check if there is a saved hash, and if so, if it matches the current hash
    if os.path.exists(hash_file_path):
        with open(hash_file_path, "r") as f:
            stored_hash = f.read().strip()
    else:
        stored_hash = None

    if current_hash != stored_hash:
        print("Data has changed, updating index...")
        #index_creator = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory": index_file_path, "embedding_function": OpenAIEmbeddings(openai_api_key)} if PERSIST else {})
        os.environ["OPENAI_API_KEY"] = APIKEY
        index_creator = VectorstoreIndexCreator( vectorstore_kwargs={"persist_directory": index_file_path} if PERSIST else {})
        index_creator.from_loaders(get_loaders_from_directory(data_directory))
        #index_creator.create()
        # save the current hash
        with open(hash_file_path, "w") as f:
            f.write(current_hash)
    else:
        print("Data has not changed, not updating index.")

def get_data_hash(data_directory):
    hash_object = hashlib.md5()
    for filename in sorted(os.listdir(data_directory)):
        with open(os.path.join(data_directory, filename), 'rb') as f:
            hash_object.update(f.read())
    return hash_object.hexdigest()

def get_stored_hash(hash_file_path):
    stored_hash = None
    if os.path.exists(hash_file_path):
        with open(hash_file_path, 'r') as f:
            stored_hash = f.read().strip()
    return stored_hash

def get_loaders_from_directory(data_directory):
    loaders = []
    for filename in os.listdir(data_directory):
        file_extension = os.path.splitext(filename)[-1]
        loader_cls = get_loader_cls(file_extension)
        loader = loader_cls(os.path.join(data_directory, filename))
        loaders.append(loader)
    return loaders


# Call the function to update the index if needed
update_index_if_needed(DATA_DIRECTORY, "persist", "data_hash.txt",APIKEY)
