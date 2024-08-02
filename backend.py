from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
candidate_labels = ['política', 'deporte', 'religión', 'cine']
historial = []

@app.route('/clasificar', methods=['POST'])
def clasificar():
    data = request.json
    codigo = data.get('codigo')
    texto = data.get('valor')

    if not texto:
        return jsonify({'error': 'No se proporcionó texto para clasificar'}), 400

    resultado = classifier(texto, candidate_labels)
    response = {
        'codigo': codigo,
        'labels': resultado['labels'],
        'scores': [round(score * 100, 2) for score in resultado['scores']],
        'highest': {
            'label': resultado['labels'][0],
            'score': round(resultado['scores'][0] * 100, 2)
        }
    }

    historial.append(response)
    return jsonify(response)

@app.route('/historial', methods=['GET'])
def obtener_historial():
    return jsonify(historial)

if __name__ == '__main__':
    app.run(port=8008)
