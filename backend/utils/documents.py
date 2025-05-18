from PIL.PpmImagePlugin import PpmImageFile
from dotenv import load_dotenv
from pdf2image import convert_from_path
import os
from typing import List
import base64
from phi.agent import Agent
from pptx import Presentation
from PIL import Image
from tempfile import TemporaryDirectory
from phi.model.azure import AzureOpenAIChat
import io
from backend.settings import get_app_settings
from backend.utils.llm import get_model
from backend.agents.document_processing import DocumentProcessingEngine


# def extract_text_from_pdf(pdf_path: str) -> list[str]:
#     text_content = []
#     with open(pdf_path, 'rb') as file:
#         reader = PyPDF2.PdfReader(file)
#         # Convert all pages to images at high DPI
#         images = convert_from_path(pdf_path, dpi=300)
#         for i, page in enumerate(reader.pages):
#             # Extract text with PyPDF2
#             pdf_text = page.extract_text() or ""
#             # OCR the image
#             ocr_text = pytesseract.image_to_string(images[i])
#             # Combine both, prefer OCR if PyPDF2 is empty or very short
#             if len(pdf_text.strip()) < 50:
#                 combined = ocr_text
#             else:
#                 combined = pdf_text + "\n" + ocr_text
#             text_content.append(combined.strip())
#     all_text = "\n".join(text_content)
#     # Normalize line endings
#     all_text = all_text.replace('\r\n', '\n').replace('\r', '\n')
#     # Replace single newlines (not part of double newlines) with a space
#     all_text = re.sub(r'(?<!\n)\n(?!\n)', ' ', all_text)
#     # Now split on double newlines for paragraphs
#     paragraphs = [p.strip() for p in all_text.split('\n\n') if p.strip()]
#     return paragraphs

# Removed extract_text_from_file_with_llm and related logic. Use DocumentProcessingEngine instead.
# Example usage:
# engine = DocumentProcessingEngine(model)
# paragraphs = engine.extract_text(file_path)

if __name__ == "__main__":
    load_dotenv()
    app_settings = get_app_settings()
    model = get_model(app_settings.llm_config)
    engine = DocumentProcessingEngine(model)
    paragraphs = engine.extract_text("/Users/ashish_kumar/Downloads/LNRS - Auto Ratings Trevis Use Case (1).pdf")
    for i, para in enumerate(paragraphs, 1):
        print(f"Paragraph {i}:\n{para}\n")