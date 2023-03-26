import pinecone
import streamlit as st
from sentence_transformers import SentenceTransformer
import pandas as pd
filename = "data/ENMAX_ESG.csv"

api_key=st.secrets["PINECONE_KEY"]
key = st.secrets["OPENAI_KEY"]



import os
import openai
openai.api_key = key

def create_prompt(context,query):
    header = "Answer the question as truthfully as possible using the provided context, and if the answer is not contained within the text and requires some latest information to be updated, print 'Sorry Not Sufficient context to answer query' \n"
    return header + context + "\n\n" + query + "\n"

def generate_answer(prompt):
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=0,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop = [' END']
    )
    return (response.choices[0].text).strip()

st.title("ENMAX ESG Question and Answering System")

user_input = st.text_area("Your Question",
"How do we prevent disturbance to nested birds?")
result = st.button("Make recommendations")

model = SentenceTransformer('all-MiniLM-L6-v2')


if result:
    pinecone.init(api_key=api_key, environment="us-east1-gcp")
    index = pinecone.Index("enmaxesg")
    q_new =user_input
    encoded_content = model.encode(q_new)
    query_result_content = index.query(vector=encoded_content.tolist(), 
                                       top_k=30,
                                       include_metadata=True)
    matches = query_result_content.matches
    ids = [res.id for res in matches]
    scores = [res.score for res in matches]
    metadata = [res.metadata["sentence"] for res in matches]
    df = pd.DataFrame({'id':ids, 
                        'score':scores,
                        'content': metadata
                        })
    context= "\n\n".join(df["content"])
    prompt = create_prompt(context,q_new)
    reply = generate_answer(prompt)
    st.write(reply)
