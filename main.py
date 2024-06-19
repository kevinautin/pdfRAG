from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    query = data['query']
    
    saved_response = get_saved_response(query)
    if saved_response:
        return jsonify({'response': saved_response.response})

    response = get_response(query)
    save_response(query, response)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
