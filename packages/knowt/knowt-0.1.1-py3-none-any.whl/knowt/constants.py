# constants.py
import datetime
from pathlib import Path


try:
    BASE_DIR = Path(__file__).parent.parent.parent
except Exception:
    BASE_DIR = Path('./data')
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
GLOBS = ("**/*.txt", "**/*.md")  # add preprocessors for ReST and HTML

CORPUS_DIR = DATA_DIR / 'corpus'
CORPUS_DIR.mkdir(exist_ok=True)
TEXT_LABEL = 'sentence'
DF_PATH = CORPUS_DIR / f'{TEXT_LABEL}s.csv.bz2'
EMBEDDINGS_PATH = DF_PATH.with_suffix('.embeddings.joblib')
EXAMPLES_PATH = DF_PATH.with_suffix('.search_results.csv')

TODAY = datetime.date.today()
RAG_SEARCH_LIMIT = 8
RAG_MIN_RELEVANCE = .6
