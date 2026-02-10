import re

YEAR_RE = re.compile(r'^(19|20)\d{2}$')
QUESTION_RE = re.compile(r'^Q(\d{1,3})\.\s*(.*)')
OPTION_RE = re.compile(r'^\(([abcdABCD])\)\s*(.*)')

ANSWER_RE = re.compile(
    r'correct\s*answer|answer\s*:|option\s*[abcd]',
    re.IGNORECASE
)

def split_prelims_mcqs(pages, metadata, verbose=True):
    mcqs = []

    current_q = None
    current_opts = {}
    current_year = metadata.get("year")

    total_pages = len(pages)

    for p_idx, page in enumerate(pages, start=1):
        if verbose:
            print(f"[Splitter] Page {p_idx}/{total_pages}")

        for raw_line in page["text"].split("\n"):
            line = raw_line.strip()

            if not line:
                continue

            # 1️⃣ Year detection
            if YEAR_RE.match(line):
                if verbose:
                    print(f"[Splitter] Year detected: {line}")
                current_year = int(line)
                continue

            # 2️⃣ Skip answer lines
            if ANSWER_RE.search(line):
                continue

            # 3️⃣ Question start
            q_match = QUESTION_RE.match(line)
            if q_match:
                if current_q and len(current_opts) == 4:
                    mcqs.append({
                        **metadata,
                        "year": current_year,
                        "question_no": current_q["no"],
                        "question": current_q["text"].strip(),
                        "options": current_opts
                    })

                current_q = {
                    "no": int(q_match.group(1)),
                    "text": q_match.group(2)
                }
                current_opts = {}
                continue

            # 4️⃣ Option line
            opt_match = OPTION_RE.match(line)
            if opt_match and current_q:
                current_opts[opt_match.group(1).lower()] = opt_match.group(2)
                continue

            # 5️⃣ Continuation of question text
            if current_q and not current_opts:
                current_q["text"] += " " + line

    # Flush last question
    if current_q and len(current_opts) == 4:
        mcqs.append({
            **metadata,
            "year": current_year,
            "question_no": current_q["no"],
            "question": current_q["text"].strip(),
            "options": current_opts
        })

    if verbose:
        print(f"[Splitter] Total MCQs extracted: {len(mcqs)}")

    return mcqs
