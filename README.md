# ChatGPT Retrieval Script 🤖
 [![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/release/python-370/) [![ChatGPT Badge](https://img.shields.io/badge/ChatGPT-Ready-orange.svg)](https://openai.com/) [![YouTube Tutorial](https://img.shields.io/badge/YouTube-Tutorial-red.svg)](https://youtu.be/9AXP7tCI9PI)

Use ChatGPT to interact with your own files seamlessly.



## Overview 🌐

This script allows you to leverage the power of ChatGPT on your local text files. Perfect for searching, Q&A, or any interaction that requires a conversational touch.

Check out the [YouTube Video](https://youtu.be/9AXP7tCI9PI) tutorial for a comprehensive walkthrough!

## Installation 📦

Before using the script, ensure you've installed the necessary libraries:

```bash
pip install langchain openai chromadb tiktoken unstructured
```

## Usage 🚀

To use the script:

1. Ensure your API key is correctly set in `constants.py`.
2. For text files, place them in the `data/` directory.
3. Run the script and provide a query argument or use interactive mode to input queries.

```bash
python your_script_name.py "Your question here"
```

Or, use the interactive mode:

```bash
python your_script_name.py
```

To exit, type `quit`, `q`, or `exit`.

## Features 🌟

- **Persistence:** Toggle the `PERSIST` flag to save the model's index to disk and reuse for faster subsequent searches.
- **Modular Code:** Easily switch between different loaders or models by changing just a few lines.
- **Interactive Mode:** Chat with ChatGPT in real-time and get your answers instantly.

## Contributing 🤝

Feel free to fork, improve, make pull requests or fill issues. I'm always happy to get feedback or help out with questions!


⭐️ If you found this useful, please star the repo to show your support!
