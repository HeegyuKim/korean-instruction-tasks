from .base import BasePreprocessor, Preprocessors, HuggingfacePreprocessor

from datasets import load_dataset, DatasetDict


@Preprocessors.register("nsmc")
class NSMCPreprocessor(BasePreprocessor):

    def setup(self):
        dataset = load_dataset("nsmc")
        self.dataset = dataset.rename_column("document", "text")

    def cleanup(self):
        self.dataset = None

    def preprocess(self, save_dir: str):
        for split in self.dataset.keys():
            self.save_jsonl(save_dir, split, self.dataset[split])