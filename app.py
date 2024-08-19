from flask import Flask, request, send_file, render_template
import PyPDF2
import os

app = Flask(__name__)

@app.route('/')
def upload_files():
    return render_template('upload.html')

@app.route('/merge', methods=['POST'])
def merge_pdfs():
    # Get the uploaded files
    file1 = request.files.get('file1')
    file2 = request.files.get('file2')

    # Check if both files are uploaded
    if not file1 or not file2:
        return "Both files must be uploaded", 400

    # Initialize PdfMerger
    merger = PyPDF2.PdfMerger()

    try:
        # Convert each uploaded file into a PdfReader object and append to merger
        for file in [file1, file2]:
            if file and file.filename.endswith('.pdf'):
                pdf_reader = PyPDF2.PdfReader(file)
                merger.append(pdf_reader)
            else:
                return "Invalid file format. Only PDF files are allowed.", 400

        # Define the name for the merged PDF
        merged_filename = 'merged.pdf'
        
        # Write the merged content to a new PDF file
        with open(merged_filename, 'wb') as merged_file:
            merger.write(merged_file)
        
        # Return the merged PDF as a downloadable file
        return send_file(merged_filename, as_attachment=True)
    
    except Exception as e:
        return f"Error processing files: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit
