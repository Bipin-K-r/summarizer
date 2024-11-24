import os
import pdfplumber
from transformers import pipeline
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

# summarizer = pipeline("summarization", model="t5-small")
summarizer = pipeline("summarization", model="EleutherAI/gpt-neo-125M")


class PaperListView(APIView):
    def get(self, request, *args, **kwargs):
        papers = []
        papers_folder = os.path.join(settings.BASE_DIR, "..", "papers/")
        if os.path.exists(papers_folder):
            for filename in os.listdir(papers_folder):
                if filename.endswith(".pdf"):
                    title = os.path.splitext(filename)[0]
                    papers.append({"title": title, "filename": filename})
        return Response(papers, status=status.HTTP_200_OK)


def split_text_into_chunks(text, max_token_length=1000):
    words = text.split()
    for i in range(0, len(words), max_token_length):
        yield " ".join(words[i : i + max_token_length])


class PaperDetailView(APIView):
    def get(self, request, filename, *args, **kwargs):
        try:
            papers_folder = os.path.join(settings.BASE_DIR, "..", "papers/")
            file_path = os.path.join(papers_folder, filename)

            if os.path.exists(file_path):
                text = ""
                table_data = []

                try:
                    with pdfplumber.open(file_path) as pdf:
                        for page in pdf.pages:
                            extracted_text = page.extract_text()
                            if extracted_text:
                                text += extracted_text + "\n"
                            tables = page.extract_tables()
                            for table in tables:
                                if table:
                                    table_data.append(table)

                except Exception as e:
                    return Response(
                        {"error": {str(e)}},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )

                if not text.strip():
                    return Response(
                        {"error": "no extractable text found in the doc"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                summaries = []
                for chunk in split_text_into_chunks(text, max_token_length=1000):
                    try:
                        summary_result = summarizer(
                            chunk, max_length=1000, min_length=25, do_sample=False
                        )
                        if isinstance(summary_result, list) and len(summary_result) > 0:
                            summaries.append(summary_result[0]["summary_text"])
                    except Exception as e:
                        print(f"error: {e}")
                        summaries.append("Error in summarization for this section")

                summary = " ".join(summaries)

                paper_data = {
                    "title": os.path.splitext(filename)[0],
                    "summary": summary,
                    "table_data": table_data,
                }
                return Response(paper_data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
