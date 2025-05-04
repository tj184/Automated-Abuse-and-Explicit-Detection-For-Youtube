from detoxify import Detoxify
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import os

# Load models once globally for reuse
print("[INFO] Loading models...")
detoxify_model = Detoxify('original')

hatebert_model_name = "Hate-speech-CNERG/bert-base-uncased-hatexplain"
hatebert_tokenizer = AutoTokenizer.from_pretrained(hatebert_model_name)
hatebert_model = AutoModelForSequenceClassification.from_pretrained(hatebert_model_name)

def analyze_text_file(file_path: str):
    """
    Analyze the text in the given file for toxicity and hate speech using Detoxify and HateBERT.
    Returns a dictionary with all results.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read().strip()

    if not text:
        raise ValueError("Text file is empty.")

    print(f"\n[INPUT TEXT FROM: {file_path}]\n{text}\n")

    # Detoxify prediction
    print("[INFO] Running Detoxify...")
    detox_results = detoxify_model.predict(text)

    # HateBERT prediction
    print("[INFO] Running HateBERT...")
    inputs = hatebert_tokenizer(text, return_tensors="pt", truncation=True)
    outputs = hatebert_model(**inputs)
    hatebert_probs = torch.nn.functional.softmax(outputs.logits, dim=-1).detach().numpy()[0]
    hatebert_labels = ['normal', 'hateful', 'offensive']
    hatebert_results = dict(zip(hatebert_labels, hatebert_probs))

    # Final verdict logic
    toxicity_score = detox_results.get('toxicity', 0)
    hate_score = hatebert_results.get('hateful', 0) + hatebert_results.get('offensive', 0)

    if toxicity_score > 0.6 or hate_score > 0.6:
        verdict = "High likelihood of abusive or toxic content detected."
    elif toxicity_score > 0.3 or hate_score > 0.3:
        verdict = "Moderate risk of harmful language."
    else:
        verdict = "Text is likely safe and non-abusive."

    # Return results as dictionary
    return {
        "file_path": file_path,
        "text": text,
        "detoxify": detox_results,
        "hatebert": hatebert_results,
        "final_verdict": verdict
    }
