import zipfile
import os
from bs4 import BeautifulSoup
from datetime import date

# Config
epub_file = "book.epub"
output_file = "book_custom.adoc"
publishing_level = 3  # adjust as needed

# Extract EPUB
with zipfile.ZipFile(epub_file, 'r') as zip_ref:
    zip_ref.extractall("epub_content")

# Find all XHTML files (chapters)
xhtml_files = []
for root, dirs, files in os.walk("epub_content"):
    for file in files:
        if file.endswith(".xhtml") or file.endswith(".html"):
            xhtml_files.append(os.path.join(root, file))

# Helper: map HTML heading level to custom event
def map_heading(tag, publishing_level):
    level = int(tag[1])  # h1 -> 1, h2 -> 2, etc.
    if publishing_level == 2:
        if level >= 2:
            return "content"
    elif publishing_level == 3:
        if level == 2:
            return "index"
        elif level == 3:
            return "content"
    elif publishing_level == 4:
        if level == 3:
            return "index"
        elif level == 4:
            return "content"
    elif publishing_level == 5:
        if level == 4:
            return "index"
        elif level == 5:
            return "content"
    return None

# Convert one chapter
def convert_chapter(file_path):
    soup = BeautifulSoup(open(file_path, encoding="utf-8"), "html.parser")
    output = []

    # Optional: root article title
    title_tag = soup.find("h1")
    if title_tag:
        output.append(f"= {title_tag.get_text().strip()}")
        output.append(f":published: {date.today()}")
        output.append(f":tags: auto-generated\n")
    
    # Process all headings and paragraphs
    for elem in soup.find_all(["h1","h2","h3","h4","h5","h6","p","img"]):
        if elem.name.startswith("h"):
            event_type = map_heading(elem.name, publishing_level)
            if event_type == "index":
                output.append(f"\n== {elem.get_text().strip()}\n")
            elif event_type == "content":
                output.append(f"\n=== {elem.get_text().strip()}\n")
        elif elem.name == "p":
            output.append(elem.get_text().strip() + "\n")
        elif elem.name == "img":
            src = elem.get("src")
            output.append(f":image: {src}\n")

    return "\n".join(output)

# Combine all chapters
with open(output_file, "w", encoding="utf-8") as f_out:
    for chapter in sorted(xhtml_files):
        f_out.write(convert_chapter(chapter))
        f_out.write("\n\n")

print(f"Conversion complete! Output written to {output_file}")

