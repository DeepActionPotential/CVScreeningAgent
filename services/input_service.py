import os
import PyPDF2, docx
from typing import Optional


class FileManager:
    
    def _read_txt(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def _read_pdf(self, file_path: str) -> str:
        text = ""
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
        return text

    def _read_docx(self, file_path: str) -> str:
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])


    def read_file(self, file_path: str) -> Optional[str]:

        """
        Reads the content of a file based on its extension.

        Supports .txt, .pdf, and .docx files. Returns the file's text content as a string.
        Raises a ValueError if the file type is unsupported.

        Args:
            file_path (str): The path to the file to be read.

        Returns:
            Optional[str]: The text content of the file, or None if the file cannot be read.
        """

        
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.txt':
            return self._read_txt(file_path)
        elif ext == '.pdf':
            return self._read_pdf(file_path)
        elif ext == '.docx':
            return self._read_docx(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")



