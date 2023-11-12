import os

import openai
import pinecone
from datasets import load_dataset
from tqdm.auto import tqdm

EMBEDDING_MODEL = 'text-embedding-ada-002'

res = openai.Embedding.create(
    input=[
        "Sample document text goes here",
        'there will be several phrases in each batch'
    ], engine=EMBEDDING_MODEL
)

embeds = [record['embedding'] for record in res['data']]

pinecone.init(
    api_key=os.environ.get("PINECONE_API_KEY"),
    environment="gcp-starter"
)

if 'chatbot-vector' not in pinecone.list_indexes():
    pinecone.create_index('chatbot-vector', dimension=len(embeds[0]))

index = pinecone.Index('chatbot-vector')

trec = load_dataset('trec', split='train[:1000]')

batch_size = 32
for i in tqdm(range(0, len(trec['text']), batch_size)):
    i_end = min(i+batch_size, len(trec['text']))
    lines_batch = trec['text'][i: i+batch_size]
    ids_batch = [str(n) for n in range(i, i_end)]
    res = openai.Embedding.create(input=lines_batch, engine=EMBEDDING_MODEL)
    embeds = [record['embedding'] for record in res['data']]
    meta = [{'text': line} for line in lines_batch]
    to_upsert = zip(ids_batch, embeds, meta)
    index.upsert(vectors=list(to_upsert))

query = "What caused the 1929 Great Depression?"

xq = openai.Embedding.create(input=query, engine=EMBEDDING_MODEL)['data'][0]['embedding']

res = index.query([xq], top_k=5, include_metadata=True)

for match in res['matches']:
    print(f"{match['score']:.2f}: {match['metadata']['text']}")

query = "What was the cause of the major recession in the early 20th century?"

xq = openai.Embedding.create(input=query, engine=EMBEDDING_MODEL)['data'][0]['embedding']

res = index.query([xq], top_k=5, include_metadata=True)

for match in res['matches']:
    print(f"{match['score']:.2f}: {match['metadata']['text']}")

query = "Why was there a long-term economic downturn in the early 20th century?"

xq = openai.Embedding.create(input=query, engine=EMBEDDING_MODEL)['data'][0]['embedding']

res = index.query([xq], top_k=5, include_metadata=True)

for match in res['matches']:
    print(f"{match['score']:.2f}: {match['metadata']['text']}")
