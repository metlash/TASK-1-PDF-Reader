#required imports
from flask import Flask, render_template, request, send_file
import PyPDF2

app = Flask(__name__)

#localhost:5000/upload_page
@app.route('/upload_page')
def upload_file():
   return render_template('upload.html')

#method to upload and conver a json file to excel file
@app.route('/download_page', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']
        f.save(f.filename)
        
        pdfFileObject = open(f.filename,'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObject)
        
        out=f.filename[0:f.filename.index('.')]+'.txt'
        
        number_of_pages = pdfReader.numPages
        text_data=""
        for i in range(number_of_pages):
           pageObject = pdfReader.getPage(i)
           text_data+=pageObject.extractText()

        WriteTxtFile = open(out,'w')
        WriteTxtFile.write(text_data)
        
        return  render_template("download.html", value = out)  

#code to download the file
@app.route('/download_file/<filename>')
def return_files(filename):
    file_path = filename
    return send_file(file_path, as_attachment=True, attachment_filename=filename)

if __name__ == '__main__':
    app.run()
