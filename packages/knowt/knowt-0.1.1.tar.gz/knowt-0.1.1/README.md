# Self-hosted semantic search and QA

Have a conversation with your own private documents.
Want to know what your doctor said at your last exam?
What about the name of that cute person with the mishievious smile that you saw at San Diego Tech Coffee?
You probably have that info in a text file on your laptop somewhere, but you probably haven't ever used the word "mischievous" in the notes you jot down in a rush.
You may forget those details unless you have a tool like knowt to help you resurface them.
All you need to do is put your text notes into the "data/corpus" directory and knowt will take care of the rest.

Under the hood, Knowt implements a RAG (Retrieval Augmented Generative model).
So knowt first processes your private text files to create a searchable index of each passage of text you provide.
This gives it to perform "semantic search" on this indexed data blazingly fast, without using approximations.
See the project [final report](docs/Information Retrieval Systems.pdf) for more details.
To index a 10k documents should take less than a minute, and adding new documents takes seconds.
And answers to your questions take milliseconds.
Even if you wanted to ask some general question about some fact on Wikipedia, that would take less than a second (though indexing those 10M text stings took 3-4 hours on my two-yr-old laptop).

## Installation

#### Python virtual environment

To set up the project environment, follow these steps:

1. Clone the project repository or download the project files to your local machine.
2. Navigate to the project directory.
3. Create a Python virtual environment in the project directory:

```bash
pip install virtualenv
python -m virtualenv .venv
```

4. Activate the virtual environment (mac/linux):

```bash
source .venv/bin/activate
```

#### Install dependencies

Not that you have a virtual environment, you're ready to install some Python packages and download language models (spaCy and BERT).

1. Install the required packages using the `requirements.txt` file:

```bash
pip install -e .
```

2. Download the small BERT embedding model (you can use whichever open source model you like):

```bash
python -c 'from sentence_transformers import SentenceTransformer; sbert = SentenceTransformer("paraphrase-MiniLM-L6-v2")'
```

#### Quick start

You can search an example corpus of nutrition and health documents by running the `search_engine.py` script.

#### Search your personal docs

1. Replace the text files in `data/corpus` with your own.
2. Start the command-line search engine with:

```bash
python search_engine.py --refresh
```

The `--refresh` flag ensures that a fresh index is created based on your documents.
Otherwise it may ignore the `data/corpus` directory and reuse an existing index and corpus in the `data/cache` directory.

The `search_engine.py` script will first segement the text files into sentences.
Then it will create a "reverse index" by counting up words and character patterns in your documents.
It will also creat semantic embeddings to allow you to as questions about vague concepts without even knowing any the words you used in your documents.

## Contributing

Contributions to this project are welcome!

## License

This project is licensed under [MIT License](LICENSE).
