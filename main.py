from flask import Flask, request, render_template, send_file
from openai import OpenAI
from PyPDF2 import PdfReader
import io
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the user uploaded a file
        if 'file' not in request.files:
            return render_template('upload.html', error='No file part found.')
        
        file = request.files['file']
        api_key = request.form['api_key']  # Only rely on user-provided API key
        
        if file.filename == '':
            return render_template('upload.html', error='No selected file.')
        
        if file and allowed_file(file.filename):
            try:
                # Extract text from the PDF
                pdf_content = extract_text_from_pdf(file)
                
                # Generate HTML resume using OpenAI API
                html_resume = generate_html_resume(pdf_content, api_key)
                
                resume_filename = 'resume.html'
                with open(resume_filename, 'w') as f:
                    f.write(html_resume)
                
                # Return the generated HTML file to the user
                return send_file(resume_filename, as_attachment=True)
            except Exception as e:
                return render_template('upload.html', error=f'Error processing file: {str(e)}')
    
    return render_template('upload.html')

def allowed_file(filename):
    # Allow only PDF files
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'

def extract_text_from_pdf(file):
    # Extract text from the uploaded PDF file
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def generate_html_resume(pdf_content, api_key):
    # Set up OpenAI client with the provided API key
    client = OpenAI(api_key=api_key)
    
    # Define prompt for the OpenAI API
    prompt = f"""Convert the following LinkedIn profile information into a well-structured HTML resume. 
    Use appropriate HTML5 tags and include inline CSS for styling:

    {pdf_content}

    The HTML should be fully formed, including <!DOCTYPE html>, <html>, <head>, and <body> tags.
    Add a meta viewport tag for responsiveness.
    Use a clean, professional design with a color scheme.
    """
    
    try:
        # Make the API request
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates HTML resumes from LinkedIn profile information."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            n=1,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        # Return error if the API call fails
        return f"Error interacting with OpenAI API: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
