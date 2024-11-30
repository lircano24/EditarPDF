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
        replacement_pages = request.form['replacement_pages']  # Páginas seleccionadas

        main_path = os.path.join(UPLOAD_FOLDER, main_file.filename)
        replacement_path = os.path.join(UPLOAD_FOLDER, replacement_file.filename)
        main_file.save(main_path)
        replacement_file.save(replacement_path)

        # Leer los archivos PDF
        main_reader = PdfReader(main_path)
        replacement_reader = PdfReader(replacement_path)

        writer = PdfWriter()

        # Procesar las páginas seleccionadas
        selected_pages = [int(p) - 1 for p in replacement_pages.split(",") if p.isdigit()]

        # Reemplazar la página en el archivo principal con las páginas seleccionadas
        for i in range(len(main_reader.pages)):
            if i == page_to_replace:
                for page_index in selected_pages:
                    if 0 <= page_index < len(replacement_reader.pages):
                        writer.add_page(replacement_reader.pages[page_index])
            else:
                writer.add_page(main_reader.pages[i])

        # Guardar el archivo modificado
        output_path = os.path.join(UPLOAD_FOLDER, f"modificado_{main_file.filename}")
        with open(output_path, "wb") as output_pdf:
            writer.write(output_pdf)

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        return f"Error: {e}"

''' 
@app.route('/detalles_pdf', methods=['POST'])
def detalles_pdf():
    try:
        # Guardar el archivo subido temporalmente
        pdf_file = request.files['pdf_file']
        temp_path = os.path.join(UPLOAD_FOLDER, pdf_file.filename)
        pdf_file.save(temp_path)

        # Leer el PDF y contar las páginas
        reader = PdfReader(temp_path)
        num_pages = len(reader.pages)

        # Devolver la cantidad de páginas
        return {"num_pages": num_pages}, 200

    except Exception as e:
        return {"error": str(e)}, 500
    
'''

@app.route('/detalles_pdf', methods=['POST'])
def detalles_pdf():
    try:
        file = request.files['pdf_file']
        reader = PdfReader(file)
        num_pages = len(reader.pages)
        return {'num_pages': num_pages}
    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    app.run(debug=True)
