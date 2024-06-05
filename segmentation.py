def segment_text(text, strategy="simple"):
    if strategy == "simple":
        return text.split(".")
    elif strategy == "length":
        return [text[i : i + 1000] for i in range(0, len(text), 1000)]
    else:
        raise ValueError("Unknown strategy")


def load_paper(filepath="Llama2.pdf"):
    with open(filepath, "r") as f:
        return f.read()
