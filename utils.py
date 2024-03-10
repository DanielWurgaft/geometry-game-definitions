import os
from tqdm import tqdm
import json
import random
random.seed(10)

def create_concept_dictionary(base_path, custom_definitions = None, randomize = False):
    concept_dict = {}
    test_img_paths = []
    train_pos_img_paths = []
    train_neg_img_paths = []
    for dataset_section in ["elements", "constraints"]:
        concepts_path = os.path.join(base_path, dataset_section)
        for index, concept in enumerate(os.listdir(concepts_path)):
            concept_path = os.path.join(concepts_path, concept)
            if os.path.isdir(concept_path):
                concept_subdict = {}

                if custom_definitions:
                    concept_subdict["definition"] = custom_definitions[index]
                else:
                    concept_subdict["definition"] = open(os.path.join(concept_path, 'definition.txt'), 'r').readlines()[0].strip()

                concept_subdict["definition_code"] = open(os.path.join(concept_path, 'concept.txt'), 'r').read()

                # Adding full file paths for train images
                train_path = os.path.join(concept_path, 'train')
                if os.path.exists(train_path):
                    concept_subdict["train"] = [os.path.join(train_path, file) for file in os.listdir(train_path) if "neg" not in file]
                    if randomize:
                        random.shuffle(concept_subdict["train"])
                    train_pos_img_paths += concept_subdict["train"]
                    concept_subdict["train_neg"] = [os.path.join(train_path, file) for file in os.listdir(train_path) if "neg" in file]
                    if randomize:
                        random.shuffle(concept_subdict["train_neg"])
                    train_neg_img_paths += concept_subdict["train_neg"]
                # Adding full file paths for test images
                test_path = os.path.join(concept_path, 'test')
                if os.path.exists(test_path):
                    concept_subdict["test"] = [os.path.join(test_path, file) for file in os.listdir(test_path)]
                    if randomize:
                        random.shuffle(concept_subdict["test"])
                    test_img_paths += concept_subdict["test"]

                concept_dict[concept] = concept_subdict
    
    # write test image paths to javascript file
    with open(os.path.join("img_paths.js"), "w") as js_file:
        test_img_paths_dict = json.dumps({"test": test_img_paths, "train_pos": train_pos_img_paths, "train_neg": train_neg_img_paths})
        js_file.write(f"var img_paths = {test_img_paths_dict};")
    # write concept dict to javascript file
    with open(os.path.join("concept_dict.js"), "w") as js_file:
        concept_dict = json.dumps(concept_dict)
        js_file.write(f"var concept_dict = {concept_dict};")


if __name__ == "__main__":
    base_path = "geoclidean"
    create_concept_dictionary(base_path, randomize=True)
