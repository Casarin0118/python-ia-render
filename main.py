from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()

GEMINI_API_KEY = 'AIzaSyCKsjQuEb2LlIv6IdVMXvt01rnp9lIK-hU'


if not GEMINI_API_KEY:
    raise ValueError("A chave de API do Gemini não foi configurada no arquivo .env")


genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    prompt = request.args.get('prompt')

    if not prompt:
        return jsonify({'error': 'Nenhum prompt fornecido'}), 400

    context = 'Responda como se fosse uma inteligência artificial chamada Pedro'
    input_ia = f'{context}: {prompt}'
    try:
        print(f"Enviando prompt para a API: {input_ia}")
        response = model.generate_content(input_ia)
        print(f"Resposta completa da API: {response}")
        print(f"Texto da resposta da API: {response.text}")
        return jsonify({'message': response.text})
    except Exception as e:
        print(f"Erro ao gerar resposta: {e}")
        return jsonify({'error': f'Ocorreu um erro na geração da resposta: {e}'}), 500

if __name__ == '__main__':
    app.run(debug=True)