import json
import os
import random
from mt.utils.const import configs
import re


def save_dict(file_path, data_dict, encoding='utf-8'):
    with open(file_path, "w", encoding=encoding) as f:
        json.dump(data_dict, f, ensure_ascii=False)


def load_dict(file_path):
    with open(file_path, "r", encoding='utf-8') as f:
        data_dict = json.load(f)
    return data_dict


def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        sentences = f.readlines()
    return sentences


def generate_report(model_configs, evaluation_results):
    model_config_md = "\n".join([f"| **{key}** | {value} |" for key, value in model_configs.items()])
    eval_results_md = "\n".join([f"| **{key}** | {value} |" for key, value in evaluation_results.items()])

    # Define the report content including model configuration
    report_content = (
            "# Evaluation Results\n"
            + "## Evaluation Metrics\n"
            + "| Metric       | Value    |\n"
            + "|--------------|----------|\n"
            + eval_results_md + "\n"
            + "## Model Configuration\n"
            + "| Hyperparameter | Value    |\n"
            + "|----------------|----------|\n"
            + model_config_md + "\n"
            + "## Model Summary\n"
    )

    # Write the report to the file
    report_file_path = os.path.join(model_configs["report_dir"], "evaluation_results.md")
    with open(report_file_path, "w") as report_file:
        report_file.write(report_content)

    print(f"Report saved at: {report_file_path}")


def filter_sentence_pairs(english_sentences, bangla_sentences, min_length):
    filtered_pairs = []
    for eng_sent, ban_sent in zip(english_sentences, bangla_sentences):
        if len(eng_sent.strip()) >= min_length and len(ban_sent.strip()) >= min_length:
            if not re.search(r'[a-zA-Z]', ban_sent):  # Check if Bangla sentence contains English alphabets
                filtered_pairs.append((eng_sent.strip(), ban_sent.strip()))
    return filtered_pairs


def take_ban_eng_random_samples():
    english_file = os.path.join(configs["data_dir"], 'hasan-etal-2020-low', "2.75M", "original_corpus.en")
    bangla_file = os.path.join(configs["data_dir"], 'hasan-etal-2020-low', "2.75M", "original_corpus.bn")

    english_sentences = read_file(english_file)
    bangla_sentences = read_file(bangla_file)

    assert len(english_sentences) == len(bangla_sentences), "Number of English and Bangla sentences don't match"

    sentence_pairs = filter_sentence_pairs(english_sentences, bangla_sentences, 20)

    selected_pairs = random.sample(sentence_pairs, 10000)

    print("Selected sentences count:", len(selected_pairs))

    eng_output_file = os.path.join(configs["data_dir"], 'hasan-etal-2020-low', 'eng.txt')
    ban_output_file = os.path.join(configs["data_dir"], 'hasan-etal-2020-low', 'ban.txt')
    with open(eng_output_file, 'w', encoding='utf-8') as eng_file, open(ban_output_file, 'w',
                                                                        encoding='utf-8') as ban_file:
        for pair in selected_pairs:
            eng_file.write(pair[0].strip() + '\n')
            ban_file.write(pair[1].strip() + '\n')


if __name__ == "__main__":
    print("Running helpers.py")
    # take_ban_eng_random_samples()
