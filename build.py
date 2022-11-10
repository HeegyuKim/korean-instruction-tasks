from pathlib import Path
import fire, random
from tqdm import tqdm

from builders import Builders
from omegaconf import OmegaConf
from datasets import load_dataset


def get_dataset(dataset_name):
    if dataset_name.startswith("huggingface/"):
        prefix_len = len("huggingface/")
        return load_dataset(dataset_name[prefix_len:])
    else:
        raise Exception("으악")


def build(template, save_dir="tasks/"):
    template = OmegaConf.load("templates/" +  template + ".yml")
    dataset_name = template["dataset"]
    dataset_dict = get_dataset(dataset_name)
    tasks = template["tasks"]
    
    builders = []
    for task in tasks:
        builder = Builders.create(task["builder"])
        builders.append(builder)
        print(f"- Task {task['name']} ready")

    for split in dataset_dict.keys():
        print(f"start building tasks from {dataset_name} split {split}")
        dataset = dataset_dict[split]

        for builder, task in zip(builders, tasks):

            target_dir = Path(save_dir, task.name)
            target_dir.mkdir(exist_ok=True, parents=True)
            builder.begin(str(target_dir), split, task)
        
        for item in tqdm(dataset):
            builder = random.choice(builders)
            builder.add_instance(item)

        for builder in builders:
            builder.finish()
    


if __name__ == "__main__":
    fire.Fire(build)


