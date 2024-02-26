"""
Create RAG to answer questions using a VectorDB(globs=['data/corpus/**/*.txt']) of text files

>>> from .constants import DATA_DIR
>>> rag = RAG(db=DATA_DIR / 'corpus_nutrition')
>>> q = 'What is the healthiest fruit?'
>>> rag.ask(q)[:69]
'The healthiest fruits recommended for people with diabetes and glycem'
>>> q = 'How much exercise is healthiest?'
>>> rag.ask(q)rag.ask(q)[:69]
'The amount of exercise that is healthy for an individual is not speci'
"""

import sys
import dotenv
import logging
from pathlib import Path
from openai import OpenAI
from .search import VectorDB
from .constants import RAG_SEARCH_LIMIT, RAG_MIN_RELEVANCE

try:
    log = logging.getLogger(__name__)
except NameError:
    log = logging.getLogger('llm.__main__')


dotenv.dotenv_values()
env = dotenv.dotenv_values()
OPENROUTER_API_KEY = env['OPENROUTER_API_KEY']
CLIENT = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

# globals().update(env)
LLM_MODELS = (
    'meta-llama/llama-2-13b-chat',  # expensive
    "openai/gpt-3.5-turbo",  # free?
    'auto',  # unknown?
    'open-orca/mistral-7b-openorca',  # cheaper/better than Llama-2-13
    "mistralai/mistral-7b-instruct",  # free
)
LLM_MODEL_DICT = {s.split('/')[0].lower().split('-')[-1].lower(): s for s in LLM_MODELS}
LLM_MODEL_DICT.update({s.split('/')[-1].lower().split('-')[0].lower(): s for s in LLM_MODELS})
LLM_MODEL = LLM_MODELS[-1]

PROMPT_EXAMPLES = []
PROMPT_EXAMPLES.append([
    "PUG meetup", "2024-01-27",
    "You are an elementary school student answering questions on a reading comprehension test. "
    "Your answers must only contain information from the passage of TEXT provided. "
    "Read the following TEXT and answer the QUESTION below the text as succintly as possible. "
    "Do not add any information or embelish your answer. "
    "You will be penalized if you include information not contained in the TEXT passage. \n\n"
    "TEXT: {context}\n\n"
    "QUESTION: {question}\n\n"])
PROMPT_EXAMPLES.append([
    "Vish benchmark", "2024-02-01",
    "You are an elementary school student answering questions on a reading comprehension test. "
    "Your answers must only contain information from the passage of TEXT provided. "
    "Read the following TEXT and answer the QUESTION below the text as succinctly as possible. "
    "Do not add any information or embelish your answer. "
    "You will be penalized if your ANSWER includes any information not contained in the passage of TEXT provided above the QUESTION. \n\n"
    "TEXT: {context}\n\n"
    "QUESTION: {question}\n\n"
    "ANSWER: "])
PROMPT_EXAMPLES.append([
    "reading comprehension exam", "2024-02-12",
    "You are an elementary school student answering questions on a reading comprehension exam. \n"
    "To answer the exam QUESTION, first read the TEXT provided to see if it contains enough information to answer the QUESTION. \n"
    "Read the TEXT provided below and answer the QUESTION as succinctly as possible. \n"
    "Your ANSWER should only contain the facts within the TEXT. \n"
    "If the TEXT provided does not contain enough information to answer the QUESTION you should ANSWER with \n "
    "'I do not have enough information to answer your question.'. \n"
    "You will be penalized if your ANSWER includes any information not contained in the TEXT provided. \n\n"
    "TEXT: {context}\n\n"
    "QUESTION: {question}\n\n"
    "ANSWER: "])
PROMPT_EXAMPLES.append([
    "search results comprehension exam", "2024-02-24",
    "You are an elementary school student answering questions on a reading comprehension exam. \n"
    "To answer the exam QUESTION, first read the SEARCH_RESULTS to see if it contains enough information to answer the QUESTION. \n"
    "Read the TEXT provided below and answer the QUESTION as succinctly as possible. \n"
    "Your ANSWER should only contain facts from found in the SEARCH_RESULTS. \n"
    "If SEARCH_RESULTS text does not contain enough information to answer the QUESTION you should ANSWER with \n "
    "'The quetion cannot be answered based on the document database search results provided.'. \n"
    "You will be penalized if your ANSWER includes any information not contained in SEARCH_RESULTS. \n\n"
    "TEXT: {context}\n\n"
    "QUESTION: {question}\n\n"
    "ANSWER: "])


RAG_PROMPT_TEMPLATE = PROMPT_EXAMPLES[-1][-1]


def get_model(model):
    return LLM_MODEL_DICT.get(model, model)


class RAG:

    def __init__(
            self, prompt_template=RAG_PROMPT_TEMPLATE, llm_model=LLM_MODEL,
            search_limit=RAG_SEARCH_LIMIT, min_relevance=RAG_MIN_RELEVANCE,
            client=None, db=None):
        global CLIENT
        client = client or CLIENT
        self.client = client
        self.prompt_template = prompt_template
        self.llm_model_name = llm_model
        self.hist = []
        self.search_limit = search_limit or RAG_SEARCH_LIMIT
        self.min_relevance = min_relevance or RAG_MIN_RELEVANCE
        if not isinstance(db, VectorDB):
            db = Path(db)
            self.db = VectorDB(db, search_limit=self.search_limit, min_relevance=self.min_relevance)

    def setattrs(self, *args, **kwargs):
        if len(args) and isinstance(args[0], dict):
            kwargs.update(args[0])
        for k, v in kwargs.items():
            # TODO: try/except better here
            if not hasattr(self, k):
                log.error(f'No such attribute "{k}" in a {self.__class__.__name__} class!')
                raise AttributeError(f'No such attribute in a {self.__class__.__name__} class!')
            setattr(self, k, v)

    def ask(self, question, context=0, search_limit=None, min_relevance=None, prompt_template=None, **kwargs):
        """ Ask the RAG a question, optionally reusing previously retrieved context strings

        Args:
          context (int|str): A str will be used directly in the LLM prompt.
            -1 => last context from history of chat queries
             0 => refresh the context using the VectorDB for semantic search
             1 => use the first context retrieved this session
             2 => use the 2nd context retrieved this session
        """
        self.question = question
        self.search_limit = search_limit = search_limit or self.search_limit
        self.min_relevance = min_relevance = min_relevance or self.min_relevance
        self.prompt_template = prompt_template = prompt_template or self.prompt_template
        self.setattrs(kwargs)
        if (not context or context in [0, 'refresh', '', None]) or not len(self.hist):
            topdocs = self.db.search(question, limit=search_limit)
            topdocs = topdocs[topdocs['relevance'] > min_relevance]
            context = '\n'.join(list(topdocs[self.db.text_label]))
        if isinstance(context, int):
            try:
                context = self.hist[context]['context']
            except IndexError:
                context = self.hist[-1]['context']
        self.context = context = context or 'Search returned 0 results.'
        self.hist.append({k: getattr(self, k) for k in 'question context prompt_template'.split()})
        prompt = self.prompt_template.format(**self.hist[-1])  # **vars(self))
        self.completion = self.client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://qary.ai",  # Optional, for including your app on openrouter.ai rankings.
                "X-Title": "https://qary.ai",  # Optional. Shows in rankings on openrouter.ai.
            },
            model=self.llm_model_name,
            messages=[{"role": "user", "content": prompt}, ],)
        # TODO: function to flatten an openAI Completion object into a more open-standard interoperable format
        self.answers = [
            (cc.message.content, cc.logprobs)
            for cc in self.completion.choices]
        self.answer, self.answer_logprob = self.answers[0]
        self.answer_id = self.completion.id
        # FIXME: .hist rows should each be temporarily stored in a .turn dict with well-defined schema accepted by all functions
        self.hist[-1].update({k: getattr(self, k) for k in 'answer answer_id answer_logprob'.split()})  # answer=completion['content']
        return self.answer


if __name__ == '__main__':
    question = ' '.join(sys.argv[1:])
    rag = RAG()
    answers = [rag.ask(question)]
    # answers = ask_llm(
    #     question=question,
    #     model='auto',
    #     context='',
    #     prompt_template=PROMPT_NO_CONTEXT)
    print(answers + '\n')
