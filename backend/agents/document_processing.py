from typing import List
import os
import base64
import io
from tempfile import TemporaryDirectory
from pptx import Presentation
from PIL import Image
from PIL.PpmImagePlugin import PpmImageFile
from pdf2image import convert_from_path
from phi.agent import Agent
from phi.model.azure import AzureOpenAIChat

class DocumentProcessingEngine:
    """
    Engine to extract text from PDF or PPTX files using an LLM with vision (e.g., GPT-4o via phidata).
    """
    def __init__(self, model: AzureOpenAIChat):
        self.model = model
        self.agent = Agent(model=model, markdown=True)

    def extract_text(self, file_path: str) -> List[str]:
        file_ext = os.path.splitext(file_path)[1].lower()
        images = []
        with TemporaryDirectory() as tmpdir:
            if file_ext == ".pdf":
                images = convert_from_path(file_path, dpi=300, output_folder=tmpdir)
            elif file_ext in [".ppt", ".pptx"]:
                prs = Presentation(file_path)
                for i, slide in enumerate(prs.slides):
                    width = prs.slide_width
                    height = prs.slide_height
                    img = Image.new("RGB", (width, height), "white")
                    img_path = os.path.join(tmpdir, f"slide_{i+1}.png")
                    img.save(img_path)
                    images.append(Image.open(img_path))
            else:
                raise ValueError("Unsupported file type. Only PDF and PPTX are supported.")

            paragraphs = []
            for i, img in enumerate(images):
                if isinstance(img, PpmImageFile):
                    img = img.convert("RGB")
                buffer = io.BytesIO()
                img.save(buffer, format="PNG")
                img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
                img_data_url = f"data:image/png;base64,{img_base64}"

                prompt = [
                    {"type": "text", "text": "Extract text from this slide."},
                    {"type": "image_url", "image_url": {"url": img_data_url}}
                ]
                response = self.agent.run(prompt)
                text = response.content if hasattr(response, "content") else str(response)
                for para in text.split("\n\n"):
                    para = para.strip()
                    if para:
                        paragraphs.append(para)
            return paragraphs 