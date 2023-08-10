import email
from bs4 import BeautifulSoup, Tag

with open("input.eml") as f:
    msg = email.message_from_file(f)

for part in msg.get_payload():
    if part.get_content_type() == "text/html":
        html: bytes = part.get_payload(decode=True)
        break

soup = BeautifulSoup(html, "html.parser")
qna = []

# All the questions are in <h2> tags
for el in soup.find_all("h2"):
    el: Tag  # For better linting
    question = el.get_text().replace("\n", "")

    if not question.endswith("*"):
        continue

    # Remove the "*" at the end
    question = question[:-1].strip()

    if question in ("Class", "Index Number"):
        continue

    answer = el.parent.nextSibling.get_text().strip()
    qna.append(f"{question}\t{answer}")

with open("output.txt", "w") as f:
    f.write("\n".join(qna))

quiz_name = soup.find_all("h1")[1].get_text()
print(f'Extracted Q&As from "{quiz_name}" (written to "output.txt")')
