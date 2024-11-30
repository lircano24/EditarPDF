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
    

@app.route('/reemplazar', methods=['POST'])
def reemplazar():
    try:
        # Guardar los archivos cargados
        main_file = request.files['main_pdf']
        replacement_file = request.files['replacement_pdf']
        page_to_replace = int(request.form['page']) - 1  # Página a reemplazar (indexada desde 0)

        main_path = os.path.join(UPLOAD_FOLDER, main_file.filename)
        replacement_path = os.path.join(UPLOAD_FOLDER, replacement_file.filename)
        main_file.save(main_path)
        replacement_file.save(replacement_path)

        # Leer los archivos PDF
        main_reader = PdfReader(main_path)
        replacement_reader = PdfReader(replacement_path)

        writer = PdfWriter()

        # Reemplazar la página en el archivo principal
        for i in range(len(main_reader.pages)):
            if i == page_to_replace:
                writer.add_page(replacement_reader.pages[0])  # Agrega la primera página del archivo de reemplazo
            else:
                writer.add_page(main_reader.pages[i])

        # Guardar el archivo modificado
        output_path = os.path.join(UPLOAD_FOLDER, f"modificado_{main_file.filename}")
        with open(output_path, "wb") as output_pdf:
            writer.write(output_pdf)

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        return f"Error: {e}"


if __name__ == '__main__':
    app.run(debug=True)
