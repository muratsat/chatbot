import asyncio
import os

from app.llm.vector_store import create_file


async def main():
    # loop through all files in "files" directory recursively

    file_paths = []

    # recursively find all .txt files in the directory
    for root, _, files in os.walk("files"):
        for file in files:
            if file.endswith(".txt") or file.endswith(".txt.bonuskana"):
                file_paths.append(os.path.join(root, file))

    await asyncio.gather(*[create_file(file_path) for file_path in file_paths])


if __name__ == "__main__":
    asyncio.run(main())
