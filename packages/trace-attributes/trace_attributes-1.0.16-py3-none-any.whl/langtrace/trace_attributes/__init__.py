# __init__.py
from enum import Enum

from .models.database_span_attributes import DatabaseSpanAttributes
from .models.openai_span_attributes import OpenAISpanAttributes


class Event(Enum):
    STREAM_START = "stream.start"
    STREAM_OUTPUT = "stream.output"
    STREAM_END = "stream.end"


class LlamaIndexMethods(Enum):
    BASEEXTRACTOR_EXTRACT = "llamaindex.BaseExtractor.extract"
    SIMPLEPROMPT_CALL = "llamaindex.SimplePrompt.call"
    CHATENGINE_EXTRACT = "llamaindex.ChatEngine.chat"
    RETRIEVER_RETRIEVE = "llamaindex.Retriever.retrieve"
    QUERYENGINE_QUERY = "llamaindex.QueryEngine.query"
    BASEREADER_LOADDATA = "llamaindex.BaseReader.loadData"


class OpenAIMethods(Enum):
    CHAT_COMPLETION = "openai.chat.completion.create"
    IMAGES_GENERATION = "openai.images.generation.create"
    EMBEDDINGS_CREATE = "openai.embeddings.create"


class ChromaDBMethods(Enum):
    ADD = "chromadb.collection.add"
    QUERY = "chromadb.collection.query"
    DELETE = "chromadb.collection.delete"
    PEEK = "chromadb.collection.peek"
    UPDATE = "chromadb.collection.update"
    MODIFY = "chromadb.collection.modify"
    COUNT = "chromadb.collection.count"


class PineconeMethods(Enum):
    UPSERT = "pinecone.Index.upsert"
    QUERY = "pinecone.Index.query"
    DELETE_ONE = "pinecone.Index.deleteOne"
    DELETE_MANY = "pinecone.Index.deleteMany"
    DELETE_ALL = "pinecone.Index.deleteAll"


# Export only what you want to be accessible directly through `import my_package`
__all__ = ['OpenAISpanAttributes', 'DatabaseSpanAttributes', 'Event',
           'LlamaIndexMethods', 'OpenAIMethods', 'ChromaDBMethods', 'PineconeMethods']
