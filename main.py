import email
from bs4 import BeautifulSoup, Tag
from glob import glob
from os import makedirs


def extract_qna(soup: BeautifulSoup) -> str:
    qna = []

    # All the questions are in <h2> tags
    for el in soup.find_all("h2"):
        el: Tag  # For better linting
        question = el.get_text().replace("\n", "")

        # A "*" at the end indicates that it's a required question
        if not question.endswith("*"):
            continue

        # Remove the "*" at the end
        question = question[:-1].strip()

        # These aren't questions
        if question in ("Class", "Index Number"):
            continue

        answer = el.parent.nextSibling.get_text().strip()
        qna.append(f"{question}\t{answer}")

    return "\n".join(qna)


input_filenames = glob("input/*.eml")

if len(input_filenames) == 0:
    print("No .eml files found in input folder")
else:
    makedirs("output", exist_ok=True)

# Get all the .eml files in the input folder
for filename in input_filenames:
    # Read the email
    with open(filename) as f:
        msg = email.message_from_file(f)

    # Extract the HTML content of the email
    html: bytes = next(
        part.get_payload(decode=True)
        for part in msg.get_payload()
        if part.get_content_type() == "text/html"
    )

    # Parse the HTML
    soup = BeautifulSoup(html, "html.parser")

    # Extract the questions, answers and quiz name
    qna = extract_qna(soup)
    quiz_name: str = soup.find_all("h1")[1].get_text()

    # Save the extracted Q&A
    with open(f"output/{quiz_name}.txt", "w") as f:
        f.write(qna)

    print(f"{filename[6:]} => {quiz_name}.txt")
