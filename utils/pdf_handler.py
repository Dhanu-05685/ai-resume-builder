from PyPDF2 import PdfReader
import io

def extract_text_from_pdf(file):
    """
    Extract text from PDF file
    Args:
        file: Flask file object or path to PDF
    Returns:
        Extracted text string
    """
    try:
        # If it's a file object from Flask request
        if hasattr(file, 'read'):
            pdf_reader = PdfReader(file)
        else:
            # If it's a file path
            with open(file, 'rb') as f:
                pdf_reader = PdfReader(f)
        
        text = ""
        total_pages = len(pdf_reader.pages)
        
        # Extract text from each page
        for page_num in range(total_pages):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
            text += f"\n--- Page {page_num + 1} ---\n"
        
        return text.strip() if text else None
    
    except Exception as e:
        print(f"Error extracting PDF text: {str(e)}")
        return None

def get_pdf_info(file):
    """
    Get information about PDF file
    Args:
        file: Flask file object or path to PDF
    Returns:
        Dictionary with PDF info
    """
    try:
        if hasattr(file, 'read'):
            pdf_reader = PdfReader(file)
        else:
            with open(file, 'rb') as f:
                pdf_reader = PdfReader(f)
        
        info = {
            'total_pages': len(pdf_reader.pages),
            'metadata': pdf_reader.metadata if pdf_reader.metadata else {},
        }
        
        return info
    
    except Exception as e:
        print(f"Error getting PDF info: {str(e)}")
        return None

def validate_pdf(file):
    """
    Validate if file is valid PDF
    Args:
        file: Flask file object
    Returns:
        Boolean
    """
    try:
        if hasattr(file, 'read'):
            pdf_reader = PdfReader(file)
            return len(pdf_reader.pages) > 0
        return False
    except:
        return False
