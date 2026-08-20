import json
from pathlib import Path


def main():
    data_dir = Path(r"C:\Users\Kartik Saini\Documents\589\LLMs_work\compare_x\data\raw\amazon")
    

    files = list(data_dir.glob("*.jsonl"))

    if not files:
        raise FileNotFoundError(
            f"No .jsonl file found in {data_dir}"
        )

    if len(files) > 1:
        print("Found multiple JSONL files:")
        for file in files:
            print(f" - {file.name}")

        raise RuntimeError(
            "Keep only the Amazon metadata JSONL file "
            "in data/raw/amazon for this inspection."
        )

    file_path = files[0]

    print(f"File: {file_path.name}")
    print(f"Size: {file_path.stat().st_size / (1024 ** 3):.2f} GB")
    print()

    records = []

    with file_path.open(
        "r",
        encoding="utf-8",
    ) as file:

        for index, line in enumerate(file):
            if index >= 5:
                break

            line = line.strip()

            if not line:
                continue

            record = json.loads(line)
            records.append(record)

    print(f"Records inspected: {len(records)}")
    print()

    for index, record in enumerate(records, start=1):
        print("=" * 70)
        print(f"RECORD {index}")
        print("=" * 70)

        print("Fields:")
        print(sorted(record.keys()))
        print()

        for key, value in record.items():
            if isinstance(value, str):
                preview = value[:200]
            elif isinstance(value, list):
                preview = (
                    f"list[{len(value)}] "
                    f"{value[:2]}"
                )
            elif isinstance(value, dict):
                preview = (
                    f"dict[{len(value)}] "
                    f"{dict(list(value.items())[:5])}"
                )
            else:
                preview = value

            print(f"{key}: {preview}")

        print()


if __name__ == "__main__":
    main()