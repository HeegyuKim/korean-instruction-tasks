
from datasets import load_dataset
import jsonlines


class BasePreprocessor:

    def setup(self):
        pass

    def cleanup(self):
        pass

    def preprocess(self, save_dir: str):
        pass

    def save_jsonl(self, save_dir, split, items, max_items_per_file=1000000):
        index = 0
        fout = None
        
        for i, item in enumerate(items):
            if i % max_items_per_file == 0:
                index += 1
                if fout is not None:
                    fout.close()

                fout = jsonlines.open(f"{save_dir}/{split}_{index:04d}.jsonl", "w")
                
            fout.write(item)
        fout.close()

class HuggingfacePreprocessor(BasePreprocessor):

    @property
    def dataset_name(self):
        pass

    def setup(self):
        self.dataset = load_dataset(self.dataset_name)
    
    def cleanup(self):
        self.dataset = None

    def preprocess_item(self, item) -> any:
        pass

    def preprocess(self, save_dir):
        dataset = self.dataset.map(self.item)
        
        for split in dataset.keys():
            self.save_jsonl(save_dir, split, dataset[split])


class Preprocessors:
    registry = {}

    @classmethod
    def register(cls, name: str) -> callable:

        def inner_wrapper(wrapped_class: BasePreprocessor) -> callable:
            assert name not in cls.registry
            cls.registry[name] = wrapped_class
            return wrapped_class

        return inner_wrapper

    # end register()

    @classmethod
    def create(cls, name: str, **kwargs) -> BasePreprocessor:
        assert name in cls.registry
        exec_class = cls.registry[name]
        executor = exec_class(**kwargs)
        return executor