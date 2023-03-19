from gpt_index import SimpleDirectoryReader, GPTListIndex, GPTSimpleVectorIndex, LLMPredictor, PromptHelper
from langchain import OpenAI
import gradio as gr
import pandas as pd
import requests
import sys
import os

# Set environment variables
os.environ["GEINS_API_KEY"] = 'YOUR-GEINS-API-KEY'
os.environ["OPENAI_API_KEY"] = 'sk-YOUR-OPENAI-API-KEY'
os.environ["INDEX_FILENAME"] = 'index.json'
os.environ["DIRECTORY_PATH"] = 'docs'

def query_and_save_to_csv(api_url, query, csv_path, api_key):
    # Set the request headers to include the API key
    headers = {'X-APIKEY': api_key}

    # Send the GraphQL query to the API with the headers
    response = requests.post(api_url, json={'query': query}, headers=headers)

    # Check response
    response.raise_for_status()

    # Convert the response JSON to a pandas DataFrame
    data = pd.json_normalize(response.json()['data']['products'])

    # Save the DataFrame to a CSV file
    with open(csv_path, 'w') as f:
        data.to_csv(f, index=False)

def construct_index(directory_path):
    # Set the parameters for the prompt helper according to the model
    max_input_size = 4096
    num_outputs = 512
    max_chunk_overlap = 20
    chunk_size_limit = 600
    
    # Create a prompt helper to help with chunking
    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

    # Create a LLM predictor from OpenAI with a temperature of 0.7
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.7, model_name="gpt-3.5-turbo", max_tokens=num_outputs))
    
    # Load the documents from the directory
    documents = SimpleDirectoryReader(directory_path).load_data()

    # Create the index
    index = GPTSimpleVectorIndex(documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)

    # Save the index to disk
    index.save_to_disk(os.environ["INDEX_FILENAME"])

    return index

def chatbot(input_text):
    index = GPTSimpleVectorIndex.load_from_disk('index.json')
    response = index.query(input_text, response_mode="compact")
    return response.response

iface = gr.Interface(fn=chatbot,
                     inputs=gr.inputs.Textbox(lines=7, label="Enter your text"),
                     outputs="text",
                     title="Chat with your Product catalog")
# Download the data
api_url = 'https://shopapi.carismar.io/graphql'
query = '''
query products(
  $take: Int = 1000
) {
  products(
    take: $take
  ) {
    products {
      productId
      name
      articleNumber
      brand {
    	    name
  		}
      primaryCategory {
    		name
  		}
      texts {
      	text1
      	text2
      	text3
    	}
      parameterGroups {
      	name
      	parameters {
        	name
        	value
      }
    	}
    }
  }
}
'''
csv_path = os.environ["DIRECTORY_PATH"] + '/' +'product_catalog.csv'
query_and_save_to_csv(api_url, query, csv_path, os.environ["GEINS_API_KEY"])

# Construct the index form the directory specified in the environment variable
index = construct_index(os.environ["DIRECTORY_PATH"])

# Launch the interface
iface.launch(share=True)