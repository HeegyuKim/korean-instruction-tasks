
import jsonlines
import random



class BaseBuilder:
    
    def begin(self, save_dir: str, split: str, task):
        self.fout = jsonlines.open(f"{save_dir}/{split}.jsonl", "w")
        self.task = task

    def finish(self):
        self.fout.close()
        self.fout = None
        self.task = None

    def add_instance(self, item):
        template = random.choice(self.task["templates"])

        item = self.process_instance(item, template)
        item["task"] = self.task["name"]
        item["template-id"] = template["id"]
        self.fout.write(item)
    
    def process_instance(self, item, template):
        pass


class Builders:
    registry = {}


    @classmethod
    def register(cls, name: str) -> callable:

        def inner_wrapper(wrapped_class: BaseBuilder) -> callable:
            assert name not in cls.registry
            cls.registry[name] = wrapped_class
            return wrapped_class

        return inner_wrapper

    # end register()

    @classmethod
    def create(cls, name: str, **kwargs) -> BaseBuilder:
        assert name in cls.registry
        exec_class = cls.registry[name]
        executor = exec_class(**kwargs)
        return executor