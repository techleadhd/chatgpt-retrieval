---
runme:
  id: 01HK4NXTB4EC9T3SR79EKFFS1W
  version: v2.0
---

# chatgpt-retrieval

Simple script to use ChatGPT on your own files.

Here's the [YouTube Video](https://youtu.be/9AXP7tCI9PI).

## Installation

Install [Langchain](https://github.com/hwchase17/langchain) and other required packages. And, use python version 3.9 64bit.

```sh {"id":"01HK4NXTB4EC9T3SR797GCDYV7"}
pip install langchain openai chromadb==0.3.29 tiktoken unstructured unstructured[pdf]
```

Modify `constants.py.default` to use your own [OpenAI API key](https://platform.openai.com/account/api-keys), and rename it to `constants.py`.

Place your own data into `data/data.txt`.

## Example usage

Test reading `data/data.txt` file.

```sh {"id":"01HK4NXTB4EC9T3SR79A5R70JM"}
> python chatgpt.py "what is my dog's name"
Your dog's name is Sunny.

```

Test reading `data/cat.pdf` file.

```sh {"id":"01HK4NXTB4EC9T3SR79DCGAS5K"}
> python chatgpt.py "what is my cat's name"
Your cat's name is Muffy.

```
