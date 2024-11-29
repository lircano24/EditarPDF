from flask import Flask, render_template, request, send_file
from PyPDF2 import PdfReader, PdfWriter
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/eliminar', methods=['POST'])
def eliminar():
    try:
        # Guardar archivo cargado
        file = request.files['pdf_file']
        page_to_remove = int(request.form['page']) - 1
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # Eliminar la página
        reader = PdfReader(filepath)
        writer = PdfWriter()

        for i in range(len(reader.pages)):
            if i != page_to_remove:
                writer.add_page(reader.pages[i])

        output_path = os.path.join(UPLOAD_FOLDER, f"modificado_{file.filename}")
        with open(output_path, "wb") as output_pdf:
            writer.write(output_pdf)

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        return f"Error: {e}"

@app.route('/agregar', methods=['POST'])
def agregar():
    try:
        # Guardar archivos cargados
        main_file = request.files['main_pdf']
        additional_file = request.files['additional_pdf']
        main_path = os.path.join(UPLOAD_FOLDER, main_file.filename)
        additional_path = os.path.join(UPLOAD_FOLDER, additional_file.filename)
        main_file.save(main_path)
        additional_file.save(additional_path)

        # Agregar páginas
        main_reader = PdfReader(main_path)
        additional_reader = PdfReader(additional_path)
        writer = PdfWriter()

        for page in main_reader.pages:
            writer.add_page(page)

        writer.add_page(additional_reader.pages[0])  # Agregar la primera página del PDF adicional

        output_path = os.path.join(UPLOAD_FOLDER, f"modificado_{main_file.filename}")
        with open(output_path, "wb") as output_pdf:
            writer.write(output_pdf)

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)
