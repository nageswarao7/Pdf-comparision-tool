# PDF Comparison Tool

A web application that allows users to upload two PDF documents and visualize the differences between them, with changes highlighted in different colors. This tool uses GPT-4o to provide intelligent comparison of document content.

## Features

- Upload and compare two PDF documents
- Intelligent text extraction from PDFs
- LLM-powered comparison using GPT-4o
- Color-coded visualization of differences:
  - Added content: Green
  - Removed content: Red
  - Modified content: Yellow
- Summary report of changes

## Installation

1. Clone this repository:
```bash
git clone https://github.com/nageswarao7/Pdf-comparision-tool.git
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY=your-api-key-here
```

## Usage

1. Run the Streamlit application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the URL displayed in the terminal (typically http://localhost:8501)

3. Upload two PDF files using the interface

4. Click the "Compare Documents" button to start the comparison process

5. View the highlighted differences and summary report

## Technical Approach

### PDF Text Extraction
- Primary extraction using `pdfplumber` for layout preservation
- Fallback to `PyPDF2` for compatibility with different PDF formats
- Text chunking for handling large documents

### Text Comparison with GPT-4o
- LLM-based semantic comparison for better understanding of differences
- Structured JSON response format for consistent processing
- Identification of additions, deletions, and modifications

### Visualization
- HTML-based rendering with CSS styling for highlighting
- Tooltip functionality for viewing original text in modifications
- Responsive design for better user experience

## Limitations and Future Improvements

- **OCR Support**: Add OCR capabilities for scanned documents
- **Better Chunking**: Implement more sophisticated document chunking and alignment
- **Performance Optimization**: Improve handling of very large documents
- **Batch Processing**: Add support for comparing multiple documents at once
- **Export Functionality**: Allow exporting comparison results as PDF or HTML

