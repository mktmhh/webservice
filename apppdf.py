from flask import Flask, request, jsonify
import pdfplumber
import tempfile

app = Flask(__name__)

@app.route('/extrair', methods=['POST'])
def extrair_pdf():
    if 'file' not in request.files:
        return jsonify({'erro': 'Arquivo não enviado'}), 400

    file = request.files['file']

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
        file.save(temp.name)
        with pdfplumber.open(temp.name) as pdf:
            try:
                pagina = pdf.pages[2]  # Página 3 (índice 2)
                texto = pagina.extract_text()
                linhas = texto.splitlines()

                dados = {}
                for linha in linhas:
                    if ':' in linha:
                        chave, valor = linha.split(':', 1)
                        dados[chave.strip()] = valor.strip()

                return jsonify(dados)
            except Exception as e:
                return jsonify({'erro': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
