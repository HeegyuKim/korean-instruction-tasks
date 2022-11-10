from pathlib import Path
import fire

from preprocessors import Preprocessors


def preprocess(dataset, save_dir="data/"):
    save_path = Path(save_dir, dataset)
    save_path.mkdir(exist_ok=True, parents=True)

    proc = Preprocessors.create(dataset)
    proc.setup()
    proc.preprocess(str(save_path))
    proc.cleanup()

if __name__ == "__main__":
    fire.Fire(preprocess)


