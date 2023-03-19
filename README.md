# Introduction
Chat with your product catalog. Simple app to get you started creating a chatbot for your product catalog.

See full tutorial at [docs.geins.io](https://docs.geins.io/docs/guides/use-ai-on-your-product-catalog)

## Getting Started
1. Clone this repo

2. Run the following commands to get started:
```bash
pip install -r requirements.txt
```
On macOS and Linux, you may need to use `pip3` instead of `pip`.

3. Run the following command to start the app:
```bash
python app.py
```
On macOS and Linux, you may need to use `python3` instead of `python`.

4. Open the URL that is printed in the terminal. It will look something like this: `https://12345.gradio.app`

## How it works
This app downloads your product catalog from your Geins account and uses it to train a GPT-3 model. The model is then used to generate responses to user queries.

This app uses the [GPT-3 API](https://openai.com/blog/openai-api/) to generate responses to user queries.
