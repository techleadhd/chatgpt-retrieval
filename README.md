# chatgpt-retrieval

Simple script to use ChatGPT on your own files.

Here's the [YouTube Video](https://youtu.be/9AXP7tCI9PI).

## Installation


```
git clone git@github.com:techleadhd/chatgpt-retrieval.git && cd chatgpt-retrieval
pip install -r requirements.txt
```

Create a `.env` file and add your own key to `OPENAI_API_KEY=""` [OpenAI API key](https://platform.openai.com/account/api-keys). 

Create two directories:
    0. `inputs`: This will hold your input files that are to be ingested (pdf's by default)
    1. `persist`:  This will hold indexed and ingested inputs in order to speed up subsequent queries.

## Example usage

### Create two directories:
    0. `inputs`: This will hold your input files that are to be ingested (pdf's by default)
    1. `persist`:  This will hold indexed and ingested inputs in order to speed up subsequent queries.

```shell
mkdir -p inputs, persist
```

### Add your to-be-indexed data to the input directory (i.e. your pdf's)

```shell
> cp ~/Downloads/*.pdf inputs/
```

### Index the documents and save
```shell
> ./localgpt.py --dir inputs --save_index --query "Your initial query here"
```

### Make use of the indexed documents

```shell
> ./localgpt.py --load_index ./persist -q "Your secondary query"
```

### Create a query file

```shell
> echo "My file query" > query.txt
> ./localgpt.py --load_index ./persist -qf query.txt
```

## CLI

```shell
> ./localgpt.py -h
usage: localgpt.py [-h] (-f FILE | -d DIR | -l LOAD_INDEX) [-s] [-t FILE_TYPES] (-qf QUERY_FILE | -q QUERY)

LocalGPT command line interface.

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Input path to a file to be ingested.
  -d DIR, --dir DIR     Input path to a directory of files to be ingested.
  -l LOAD_INDEX, --load_index LOAD_INDEX
                        Re-load indexed files
  -s, --save_index      Save inputs for further queries
  -t FILE_TYPES, --file_types FILE_TYPES
                        File types acceptable for ingestion.
  -qf QUERY_FILE, --query_file QUERY_FILE
                        Input path to the query file.
  -q QUERY, --query QUERY
                        Query in the command line.

```
