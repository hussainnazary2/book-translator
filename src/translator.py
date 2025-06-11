# book_translator_project/src/translator.py
from transformers import MT5ForConditionalGeneration, MT5Tokenizer


class Translator:
    def __init__(self, model_dir: str):
        self.model = MT5ForConditionalGeneration.from_pretrained(model_dir)
        self.tokenizer = MT5Tokenizer.from_pretrained(model_dir)

    def translate(self, text: str) -> str:
        inputs = self.tokenizer.encode(text, return_tensors="pt", max_length=512, truncation=True)
        outputs = self.model.generate(inputs, max_length=512)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)