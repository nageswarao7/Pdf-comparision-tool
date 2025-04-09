import json
import os
import logging
from typing import Dict, List, Any
import time
from openai import OpenAI
from pdf_processor import chunk_text
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# You would need to set up your OpenAI API key
# For a real implementation, use environment variables or a secure config
# os.environ["OPENAI_API_KEY"] = "your-api-key"  # You'd set this in a secure way

def call_openai_api(prompt: str, model: str = "gpt-4o") -> Dict[str, Any]:
    """
    Call the OpenAI API with the given prompt using the openai package
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
    
    client = OpenAI(api_key=api_key)
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2  # Lower temperature for more deterministic results
        )
        return response
    except Exception as e:
        logger.error(f"Error calling OpenAI API: {str(e)}")
        raise

def compare_chunk(text1: str, text2: str) -> Dict[str, Any]:
    """
    Compare two text chunks using GPT-4o
    """
    prompt = f"""
You are a document comparison expert. Your task is to analyze two versions of a document and identify differences.

Original document text:
```
{text1}
```

Modified document text:
```
{text2}
```

First, analyze the two texts to identify:
1. Additions (text present in the modified version but not in the original)
2. Deletions (text present in the original but not in the modified version)
3. Modifications (text changed from the original to the modified version)

Then, provide a JSON response in the following format:
{{
    "diff_sections": [
        {{
            "type": "unchanged", 
            "text": "Text that appears in both versions unchanged"
        }},
        {{
            "type": "added",
            "text": "Text that was added in the modified version"
        }},
        {{
            "type": "deleted",
            "text": "Text that was deleted from the original"
        }},
        {{
            "type": "modified",
            "text": "Text that was modified",
            "original": "How it appeared in the original"
        }}
    ],
    "summary": {{
        "additions": 5,
        "deletions": 3,
        "modifications": 2
    }},
    "detailed_summary": "A brief human-readable summary of the key changes"
}}

Be precise in your analysis. Only identify true differences, not just variations in whitespace or formatting.
Ensure that the diff_sections array, when combined in order, represents the full modified document with proper highlighting.
"""

    try:
        response = call_openai_api(prompt)
        response_text = response.choices[0].message.content
        
        # Extract the JSON part from the response
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        if json_start >= 0 and json_end > json_start:
            json_str = response_text[json_start:json_end]
            return json.loads(json_str)
        else:
            logger.error("Could not extract JSON from response")
            return {"error": "Invalid response format"}
    except Exception as e:
        logger.error(f"Error in compare_chunk: {str(e)}")
        return {"error": str(e)}

def compare_texts(text1: str, text2: str) -> Dict[str, Any]:
    """
    Compare two full texts by potentially breaking them into chunks
    and then combining the results
    """
    # For simplicity in this implementation, we'll treat the entire text as one chunk
    # In a production system, you would chunk larger documents and process them separately
    
    # If texts are too large, chunk them
    if len(text1) > 10000 or len(text2) > 10000:
        logger.info("Texts are large, chunking for comparison...")
        # This is a simplified approach - in a real implementation, you would need a more
        # sophisticated chunking strategy that aligns the chunks between documents
        chunks1 = chunk_text(text1)
        chunks2 = chunk_text(text2)
        
        # For this demonstration, just compare the first chunks
        # Real implementation would compare corresponding chunks or use a smarter alignment
        if chunks1 and chunks2:
            return compare_chunk(chunks1[0], chunks2[0])
        else:
            return {"error": "Failed to chunk the documents properly"}
    else:
        return compare_chunk(text1, text2)