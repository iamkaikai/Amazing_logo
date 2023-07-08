from datasets import load_dataset
import pandas as pd
from datasets import load_dataset

dataset = load_dataset("imagefolder", data_dir="./amazing_logos/data", split="train")
dataset.push_to_hub("iamkaikai/amazing_logos")