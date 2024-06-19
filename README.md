# Installation

pip install -r requirements.txt

Copy or rename `.env.default` as `.env`.

If you plan to use OpenAI, add your OpenAI secret key in `.env`.

If you plan to use Llama2 rather than OpenAI, in `.env`, set `USE_OPENAI` as `False`, and follow section "Install Llama2". If not, you can skip it.

# Install Llama2

git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
make

Download llama-2-7b-chat.Q4_K_M.gguf from https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/tree/main
Save it into llama.cpp/models/

# Text segmentation

First, add the pdf document you want to query to `data/books`.

To segment the text and create the vector embeddings, run
`python create_database.py`

# Query the LLM about the paper

Run `python app.py`
Then, make calls to the REST API.

Ask a question:
`curl -X POST -H "Content-Type: application/json" -d '{"question": "What this Llama thing about?"}' http://127.0.0.1:5000/query`

Check the history of questions asked:
`curl -X GET http://127.0.0.1:5000/history`

Reset the history:
`curl -X DELETE http://127.0.0.1:5000/history`
