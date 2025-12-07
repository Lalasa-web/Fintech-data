import os
import json

BASE_FOLDER = "Fintech-data"

CHUNK_LENGTH = 350
CHUNK_OVERLAP = 50

CHUNKS_OUTPUT_PATH = os.path.join(BASE_FOLDER, "all_chunks.json")
METADATA_OUTPUT_PATH = os.path.join(BASE_FOLDER, "all_metadata.json")


ROLE_MAP = {
    "engineering": [
        "Engineering Lead", "Backend Developer", "Frontend Developer",
        "DevOps Engineer", "System Architect", "Security Team", "C-Level Executive"
    ],
    "finance": [
        "Finance Manager", "Accounts Team", "Auditor",
        "Risk Analyst", "CFO", "C-Level Executive"
    ],
    "marketing": [
        "Marketing Manager", "SEO Team", "Content Strategist",
        "Growth Lead", "CMO", "C-Level Executive"
    ],
    "hr": [
        "HR Manager", "Talent Acquisition", "Compliance Officer",
        "Payroll Team", "C-Level Executive"
    ],
    "general": [
        "Employees", "Department Heads", "C-Level Executive"
    ]
}


def split_into_chunks(words, size, overlap):
    chunks = []
    position = 0

    while position < len(words):
        chunk_words = words[position:position + size]
        chunks.append(chunk_words)
        position = position + size - overlap

    return chunks


all_chunks = []
all_metadata = []
chunk_number = 1


for department_name in os.listdir(BASE_FOLDER):
    department_path = os.path.join(BASE_FOLDER, department_name)

    if not os.path.isdir(department_path):
        continue

    department_key = department_name.lower()

    print(f"\n Scanning Department: {department_name}")

    for filename in os.listdir(department_path):
        if not (filename.endswith(".txt") or filename.endswith(".md")):
            continue

        file_path = os.path.join(department_path, filename)

        print(f"    Processing: {filename}")

        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        tokens = content.split()
        chunk_list = split_into_chunks(tokens, CHUNK_LENGTH, CHUNK_OVERLAP)

        local_chunk_index = 1

        for chunk_tokens in chunk_list:
            chunk_text = " ".join(chunk_tokens)
            chunk_id = f"{department_key.upper()}_CHUNK_{chunk_number}"

            all_chunks.append({
                "chunk_id": chunk_id,
                "content": chunk_text
            })

            all_metadata.append({
                "chunk_id": chunk_id,
                "source_document": filename,
                "department": department_name,
                "chunk_index": local_chunk_index,
                "approx_token_count": len(chunk_tokens),
                "security_level": "Confidential",
                "allowed_roles": ROLE_MAP.get(department_key, ["C-Level Executive"])
            })

            local_chunk_index += 1
            chunk_number += 1


with open(CHUNKS_OUTPUT_PATH, "w", encoding="utf-8") as chunk_file:
    json.dump(all_chunks, chunk_file, indent=4)

with open(METADATA_OUTPUT_PATH, "w", encoding="utf-8") as metadata_file:
    json.dump(all_metadata, metadata_file, indent=4)


print("\n RAG DATA GENERATION COMPLETED SUCCESSFULLY")
print(" all_chunks.json created")
print(" all_metadata.json created")
print(" Total chunks generated:", len(all_chunks))
