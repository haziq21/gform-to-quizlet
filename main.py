import email
from bs4 import BeautifulSoup, Tag

with open("input.eml") as f:
    msg = email.message_from_file(f)

for part in msg.get_payload():
    if part.get_content_type() == "text/html":
        html: bytes = part.get_payload(decode=True)
        break

soup = BeautifulSoup(html, "html.parser")
qna = ""

for el in soup.find_all("h2"):
    el: Tag

    if len(el.contents) != 2:
        continue

    question = el.contents[0].get_text().strip()

    if question == "Class" or question == "Index Number":
        continue

    answer = el.parent.nextSibling.get_text().strip()
    qna += f"{question}\t{answer}\n"

with open("output.txt", "w") as f:
    f.write(qna)
