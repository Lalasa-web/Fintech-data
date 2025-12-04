import re
from pathlib import Path
from typing import List, Dict

def split_by_headings(text: str) -> List[str]:
    sections = re.split(r"\n## ", text)
    cleaned_sections = []

    for sec in sections:
        sec = sec.strip()
        if sec:
            cleaned_sections.append("## " + sec if not sec.startswith("#") else sec)

    return cleaned_sections

def select_meaningful_chunks(sections: List[str], keywords: List[str], max_chunks: int = 3):
    selected = []

    for section in sections:
        for key in keywords:
            if key.lower() in section.lower():
                selected.append(section)
                break

        if len(selected) == max_chunks:
            break

    return selected

def generate_metadata(chunk: str, file_name: str, department: str, role: str, chunk_id: int) -> Dict:
    return {
        "chunk_id": chunk_id,
        "file_name": file_name,
        "department": department,
        "role": role,
        "source_type": "md",
        "text_preview": chunk[:120] + "..."
    }

def process_document(file_path: str, department: str, role: str, keywords: List[str]):
    text = Path(file_path).read_text(encoding="utf-8")

    sections = split_by_headings(text)
    selected_chunks = select_meaningful_chunks(sections, keywords, max_chunks=3)

    metadata_records = []
    for i, chunk in enumerate(selected_chunks, start=1):
        meta = generate_metadata(
            chunk=chunk,
            file_name=Path(file_path).name,
            department=department,
            role=role,
            chunk_id=i
        )
        metadata_records.append(meta)

    return selected_chunks, metadata_records

if __name__ == "__main__":

    base_path = Path(__file__).parent
    doc1 = base_path / "quarterly_financial_report.md"

    keywords_qfr = ["summary", "q3", "2024"]

    chunks, metadata = process_document(
        file_path=doc1,
        department="finance",
        role="c-level",
        keywords=keywords_qfr
    )

    print("\n--- SELECTED CHUNKS FROM quarterly_financial_report.md ---\n")
    for i, c in enumerate(chunks, start=1):
        print(f"\n--- CHUNK {i} ---\n")
        print(c)

    print("\n\n--- GENERATED METADATA ---\n")
    for m in metadata:
        print(m)
