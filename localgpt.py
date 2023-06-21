#!/usr/bin/env python

import argparse
import os

from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma
from langchain.indexes.vectorstore import VectorStoreIndexWrapper

load_dotenv()  # take environment variables from .env.

def setup_parser():
    # Set up the argument parser
    parser = argparse.ArgumentParser(description='LocalGPT command line interface.')

    # Define mutually exclusive group for file/dir ingestion
    ingestion_group = parser.add_mutually_exclusive_group(required=True)
    ingestion_group.add_argument('-f', '--file', type=str, help='Input path to a file to be ingested.')
    ingestion_group.add_argument('-d', '--dir', type=str, help='Input path to a directory of files to be ingested.')
    ingestion_group.add_argument('-l', '--load_index', type=str, help='Re-load indexed files')

    parser.add_argument('-s', '--save_index', action="store_true", help='Save inputs for further queries')   
    
    parser.add_argument('-t', '--file_types', type=str, help='File types acceptable for ingestion.', default="*.pdf")

    # Define mutually exclusive group for query/query_file
    query_group = parser.add_mutually_exclusive_group(required=True)
    query_group.add_argument('-qf', '--query_file', type=str, help='Input path to the query file.')
    query_group.add_argument('-q', '--query', type=str, help='Query in the command line.')

    # Parse the arguments
    return parser.parse_args()

def main():

    args = setup_parser()

    if args.query:
        query = args.query
    elif args.query_file:
        with open(args.query_file) as fid:
            query = fid.read()


    if args.load_index:
        print("Reusing index...\n")
        vectorstore = Chroma(persist_directory=args.load_index, embedding_function=OpenAIEmbeddings())
        index = VectorStoreIndexWrapper(vectorstore=vectorstore)

    else:
        if args.file is not None:
            loader = TextLoader(args.file)
        elif args.dir is not None:
            loader = DirectoryLoader(args.dir, glob=args.file_types)

        if args.save_index:
            index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory":"persist"}).from_loaders([loader])
        else:
            index = VectorstoreIndexCreator().from_loaders([loader])

    chain = RetrievalQA.from_chain_type(
      llm=ChatOpenAI(model="gpt-3.5-turbo"),
      retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
    )

    print(f"Query: {query}")
    print(chain.run(query))


if __name__ == "__main__":
    main()

