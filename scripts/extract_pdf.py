from pathlib import Path
import json
import sys

from pypdf import PdfReader


def extract_pdf(pdf_path: Path) -> dict:
    reader = PdfReader(str(pdf_path))

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        text = text.strip()

        if not text:
            continue

        pages.append(
            {
                "page": page_number,
                "text": text,
            }
        )

    full_text = "\n\n".join(
        page["text"]
        for page in pages
    )

    return {
        "document_id": pdf_path.stem,
        "filename": pdf_path.name,
        "page_count": len(reader.pages),
        "pages_with_text": len(pages),
        "text": full_text,
        "pages": pages,
    }


def main():
    if len(sys.argv) != 2:
        print(
            "Usage: python scripts/extract_pdf.py <pdf_path>"
        )
        sys.exit(1)

    pdf_path = Path(sys.argv[1])

    if not pdf_path.exists():
        print(f"PDF not found: {pdf_path}")
        sys.exit(1)

    if pdf_path.suffix.lower() != ".pdf":
        print("Input file must be a PDF.")
        sys.exit(1)

    output_dir = Path("data/processed/documents")
    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    result = extract_pdf(pdf_path)

    output_path = (
        output_dir
        / f"{pdf_path.stem}.json"
    )

    with output_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            result,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print()
    print("=" * 70)
    print("PDF EXTRACTION COMPLETE")
    print("=" * 70)
    print(f"Document       : {pdf_path.name}")
    print(f"Total pages    : {result['page_count']}")
    print(
        f"Pages with text: "
        f"{result['pages_with_text']}"
    )
    print(
        f"Characters     : "
        f"{len(result['text']):,}"
    )
    print()
    print(f"Output:")
    print(output_path)
    print("=" * 70)


if __name__ == "__main__":
    main()