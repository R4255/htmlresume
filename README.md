# Resume Generator Project

## Project Overview

This project is a simple Flask web application that allows users to upload a PDF of their LinkedIn profile and convert it into a well-structured HTML resume. The application integrates the OpenAI API to transform the PDF content into HTML using AI-based text generation.


## Technologies Used

- **Flask**: A micro web framework in Python that provides the base for building the web application.
- **OpenAI API**: Used to generate HTML resumes from the extracted text in the LinkedIn PDF.
- **PyPDF2**: A Python library used to extract text from the uploaded PDF files.
- **HTML5/CSS3**: To structure and style the front-end of the resume generator page.

## How the Application Works

1. **Upload LinkedIn PDF**: The user uploads their LinkedIn profile saved as a PDF through the web interface.
2. **API Key Input**: Users are required to provide their OpenAI API key to interact with the GPT-3 model for generating the resume.
3. **PDF Text Extraction**: The PDF file is processed using `PyPDF2`, extracting all the text content from it.
4. **HTML Resume Generation**: The extracted content is passed to the OpenAI API, where a GPT-3 prompt generates a fully structured HTML5 resume based on the PDF content.
5. **Displaying the Resume**: The generated HTML is returned as a web page that the user can view or download.

## Key Components

### `main.py`

- **Upload and Process PDF**: 
  The Flask app accepts PDF uploads, checks file validity, and extracts the PDF's text using the `PdfReader` class from PyPDF2.
  
- **OpenAI API Call**: 
  Using the provided API key, the app interacts with OpenAI's GPT model to convert the extracted text into a structured HTML resume. A well-designed prompt is sent to the API to instruct the model on the expected output.

- **Error Handling**: 
  Error messages are displayed on the frontend in case of an invalid file or an API failure.

### `vercel.json`

- Configures Vercel to deploy the Flask app by specifying the Python handler (`@vercel/python`) and the routing.

### `start.sh`

- A script that starts the Flask application using Gunicorn in a production environment, binding to the specified port.

