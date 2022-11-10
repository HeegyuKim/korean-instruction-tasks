from .base import Builders, BaseBuilder
import random



DEFAULT_BINARY_ANSWER = ["아니오", "예"]


@Builders.register("binary-classification")
class BinaryClassificationBuider(BaseBuilder):

    def process_instance(self, item, template):
        inst = template["instruction"]
        input = template["input"].format(**item)
        output = DEFAULT_BINARY_ANSWER[item["label"]]

        return {
            "input": f"{inst}\n{input}",
            "output": output
        }


@Builders.register("multi-classification")
class MultiClassificationBuider(BaseBuilder):

    def join_labels(self, labels):
        return ",".join(labels)

    def process_instance(self, item, template):
        labelset = self.task["labelset"]
        labels = random.choice(labelset)

        inst = template["instruction"].format(labels=self.join_labels(labels))
        input = template["input"].format(**item)
        output = labels[item["label"]]

        return {
            "input": f"{inst}\n{input}",
            "output": output
        }