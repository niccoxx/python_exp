from flask import Flask, request, jsonify
from confluent_kafka import Producer

# Configura il producer Kafka
kafka_config = {
    'bootstrap.servers': 'localhost:32777'  # Cambia con l'indirizzo del tuo broker
}
producer = Producer(kafka_config)

def send_to_kafka(topic, message):
    producer.produce(topic, value=message)
    producer.flush()  # assicura l'invio immediato


app = Flask(__name__)

# Memorizzazione dati ricevuti via API
data_store = {"data1": "", "data2": ""}

@app.route('/', methods=['GET', 'POST'])
def home():
    global data_store
    if request.method == 'POST':
        data_store["data1"] = request.form.get('data1', '')
        data_store["data2"] = request.form.get('data2', '')
                # Invia a Kafka
        message = f"{data_store['data1']}|{data_store['data2']}"
        send_to_kafka("python_test", message)
    return f'''
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Inserisci Dati</title>
                <style>
            body {{
                background-color: yellow;
            }}
        </style>
        <script>
            async function fetchData() {{
                const response = await fetch('/api/data');
                const data = await response.json();
                document.getElementById("liveData1").innerText = data.data.data1;
                document.getElementById("liveData2").innerText = data.data.data2;
            }}
            setInterval(fetchData, 2000);
        </script>
    </head>
    <body onload="fetchData()">
        <h2>Inserisci Dati</h2>
        <form method="POST">
            <label for="data1">Dato 1:</label>
            <input type="text" id="data1" name="data1" value="{data_store['data1']}"><br><br>
            <label for="data2">Dato 2:</label>
            <input type="text" id="data2" name="data2" value="{data_store['data2']}"><br><br>
            <input type="submit" value="Invia">
        </form>
        <h3>Dati inseriti:</h3>
        <p>Dato 1: <span id="liveData1">{data_store['data1']}</span></p>
        <p>Dato 2: <span id="liveData2">{data_store['data2']}</span></p>
    </body>
    </html>
    '''

@app.route('/api/data', methods=['GET', 'POST'])
def api_data():
    global data_store
    if request.method == 'POST':
        data = request.json
        data_store["data1"] = data.get("data1", "")
        data_store["data2"] = data.get("data2", "")
        #data_store["data1"] = request.form.get('data1', '')
        #data_store["data2"] = request.form.get('data2', '')

# Invia a Kafka
        message = f"{data_store['data1']}|{data_store['data2']}"
        send_to_kafka("python_test", message)
        return jsonify({"message": "Dati ricevuti", "data": data_store}), 200
    
    return jsonify({"data": data_store})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
