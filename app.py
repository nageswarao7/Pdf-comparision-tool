import streamlit as st
import tempfile
import os
from pdf_processor import extract_text_from_pdf
from llm_comparer import compare_texts
from visualizer import generate_diff_html

def main():
    st.set_page_config(page_title="PDF Comparison Tool", layout="wide")
    
    st.title("PDF Comparison Tool")
    st.write("Upload two PDF documents to compare them and visualize the differences.")
    
    # File upload section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Original Document")
        pdf1 = st.file_uploader("Upload the original PDF", type=['pdf'], key="pdf1")
    
    with col2:
        st.subheader("Modified Document")
        pdf2 = st.file_uploader("Upload the modified PDF", type=['pdf'], key="pdf2")
    
    if pdf1 and pdf2:
        # Create a button to trigger the comparison
        if st.button("Compare Documents"):
            with st.spinner("Processing PDFs..."):
                # Create temporary files
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp1:
                    tmp1.write(pdf1.getvalue())
                    tmp1_path = tmp1.name
                
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp2:
                    tmp2.write(pdf2.getvalue())
                    tmp2_path = tmp2.name
                
                # Extract text from PDFs
                st.info("Extracting text from PDFs...")
                text1 = extract_text_from_pdf(tmp1_path)
                text2 = extract_text_from_pdf(tmp2_path)
                
                # Clean up temporary files
                os.unlink(tmp1_path)
                os.unlink(tmp2_path)
                
                # Compare texts using LLM
                st.info("Analyzing differences with GPT-4o...")
                comparison_result = compare_texts(text1, text2)
                
                # Display results
                st.success("Comparison completed!")
                
                # Display summary
                st.subheader("Summary of Changes")
                st.write(f"Additions: {comparison_result['summary']['additions']}")
                st.write(f"Deletions: {comparison_result['summary']['deletions']}")
                st.write(f"Modifications: {comparison_result['summary']['modifications']}")
                
                # Display detailed summary provided by the LLM
                st.subheader("Change Analysis")
                st.write(comparison_result['detailed_summary'])
                
                # Display visualized differences
                st.subheader("Visualized Differences")
                diff_html = generate_diff_html(comparison_result['diff_sections'])
                st.components.v1.html(diff_html, height=800, scrolling=True)

if __name__ == "__main__":
    main()