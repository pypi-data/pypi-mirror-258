import tensorflow_text as tf_text
import tensorflow as tf
import mt
import random
import os
import numpy as np
import re
from mt.utils.const import *

bangla_numerals = [
    "শূন্য", "এক", "দুই", "তিন", "চার", "পাঁচ", "ছয়", "সাত", "আট", "নয়", "দশ",
    "এগার", "বার", "তের", "চৌদ্দ", "পনের", "ষোল", "সতের", "আঠার", "ঊনিশ", "বিশ",
    "একুশ", "বাইশ", "তেইশ", "চব্বিশ", "পঁচিশ", "ছাব্বিশ", "সাতাশ", "আটাশ", "ঊনত্রিশ", "ত্রিশ",
    "একত্রিশ", "বত্রিশ", "তেত্রিশ", "চৌত্রিশ", "পঁয়ত্রিশ", "ছত্রিশ", "সাঁইত্রিশ", "আটত্রিশ", "ঊনচল্লিশ", "চল্লিশ",
    "একচল্লিশ", "বিয়াল্লিশ", "তেতাল্লিশ", "চুয়াল্লিশ", "পঁয়তাল্লিশ", "ছেচল্লিশ", "সাতচল্লিশ", "আটচল্লিশ", "ঊনপঞ্চাশ",
    "পঞ্চাশ",
    "একান্ন", "বাহান্ন", "তেপান্ন", "চুয়ান্ন", "পঁঞ্চান্ন", "ছাপ্পান্ন", "সাতান্ন", "আটান্ন", "ঊনষাট", "ষাট",
    "একষট্টি", "বাষট্টি", "তেষট্টি", "চৌষট্টি", "পঁয়ষট্টি", "ছেষট্টি", "সাতাষট্টি", "আটষট্টি", "ঊনসত্তর", "সত্তর",
    "একাত্তর", "বাহাত্তর", "তিয়াত্তর", "চুয়াত্তর", "পঁচাত্তর", "ছিয়াত্তর", "সাতাত্তর", "আটাত্তর", "ঊনআশি", "আশি",
    "একাশি", "বিরাশি", "তিরাশি", "চুরাশি", "পঁচাশি", "ছিয়াশি", "সাতাশি", "আটাশি", "ঊননব্বই", "নব্বই",
    "একানব্বই", "বিরানব্বই", "তিরানব্বই", "চুরানব্বই", "পঁচানব্বই", "ছিয়ানব্বই", "সাতানব্বই", "আটানব্বই", "নিরানব্বই",
    "একশ"]


def num2bangla(input_number, context=False):
    if not str(input_number).isdigit():
        return str(input_number)
    # Context True Means if it is digit by digit
    if context:
        return ' '.join(bangla_numerals[int(digit)] for digit in str(input_number))

    input_number = int(input_number)

    if not 0 <= input_number <= 999999999:
        return "NotInRange"

    crore, input_number = divmod(input_number, 10000000)
    lakh, input_number = divmod(input_number, 100000)
    thousand, input_number = divmod(input_number, 1000)
    hundred, input_number = divmod(input_number, 100)
    tens, ones = divmod(input_number, 10)

    result = ""

    if crore:
        result += num2bangla(crore) + " কোটি "
    if lakh:
        result += num2bangla(lakh) + " লাখ"
    if thousand:
        result += " " + num2bangla(thousand) + " হাজার"
    if hundred:
        result += " " + num2bangla(hundred) + "শো"

    if (tens or ones) and 0 <= input_number <= 100:
        if result:
            result += " "
        result += bangla_numerals[int(input_number)]

    return result.lstrip() or "শূন্য"


def replace_numerals_with_words(text, context=False):
    words = text.split()
    modified_words = []
    for word in words:

        # handle phone number
        if word.startswith('০'):
            modified_words.append(num2bangla(word, context=True))
            continue

        comma = re.sub(re.escape(','), '', word)
        if comma.isnumeric() and int(comma) > 0:
            word = re.sub(re.escape(','), '', word);
            modified_words.append(num2bangla(word, context))
            continue

        # handled the "."
        decimal = re.sub(re.escape('.'), '', word)
        if '.' in word and decimal.isnumeric():
            parts = word.split('.')
            modified_words.append(num2bangla(parts[0], False))
            modified_words.append("দশমিক")
            if len(parts[1]) != 0:
                modified_words.append(num2bangla(parts[1], True))
            continue

        # handled if it is attached with a string
        else:
            temp_modified = []
            parts = re.split(r'(\d+)', word)
            for part in parts:
                if part.isnumeric():
                    part = num2bangla(part, context)
                elif part == '%':
                    part = 'শতাংশ'
                temp_modified.append(part)
            modified_words.append(''.join(temp_modified))

    updated_text = ' '.join(modified_words)
    return updated_text


def tf_bangla_text_processor(seq):
    seq = tf_text.normalize_utf8(seq, 'NFKD')
    # Replace special characters and punctuations with spaces
    cleaned_text = tf.strings.regex_replace(seq, '[^\w\s\u0980-\u09FF]', '')
    # Remove extra white spaces
    cleaned_text = tf.strings.regex_replace(cleaned_text, '\s+', ' ')
    # Return the cleaned text
    return cleaned_text


def tf_lower_and_split_punctuation(seq):
    # Split accented characters.
    seq = tf_text.normalize_utf8(seq, 'NFKD')
    # Convert seq to lower
    seq = tf.strings.lower(seq)
    # Keep space, a to z, and select punctuation.
    seq = tf.strings.regex_replace(seq, '[^ a-z.?!,¿]', '')
    # Add spaces around punctuation.
    seq = tf.strings.regex_replace(seq, '[.?!,¿]', r' \0 ')
    # Strip whitespace.
    seq = tf.strings.strip(seq)
    seq = tf.strings.join(['[START]', seq, '[END]'], separator=' ')
    return seq


class TextProcessor:
    def __init__(self, configs):
        self.src_tokenizer = self.get_tokenizer(configs["src_lang"])
        self.tar_tokenizer = self.get_tokenizer(configs["tar_lang"])

    def get_tokenizer(self, lang):
        if lang == "eng":
            return tf.keras.layers.TextVectorization(
                standardize=mt.data.processor.tf_lower_and_split_punctuation,
                max_tokens=mt.utils.const.configs["max_tokens"],
                ragged=True
            )
        elif lang == "spa":
            return tf.keras.layers.TextVectorization(
                standardize=mt.data.processor.tf_lower_and_split_punctuation,
                max_tokens=mt.utils.const.configs["max_tokens"],
                ragged=True
            )
        elif lang == "ban":
            return tf.keras.layers.TextVectorization(
                standardize=mt.data.processor.tf_bangla_text_processor,
                max_tokens=mt.utils.const.configs["max_tokens"],
                ragged=True
            )
        elif lang == "gar":
            return tf.keras.layers.TextVectorization(
                standardize=mt.data.processor.tf_lower_and_split_punctuation,
                max_tokens=mt.utils.const.configs["max_tokens"],
                ragged=True
            )
        else:
            raise Exception(f"Lang {self.lang}, text processor not found.")

    def get_tokenizers(self):
        return self.src_tokenizer, self.tar_tokenizer


class DataLoader:
    def __init__(self, configs, src_tokenizer, tar_tokenizer):
        self.dataset_name = configs["dataset_name"]
        self.src_lang = configs["src_lang"]
        self.tar_lang = configs["tar_lang"]
        self.data_dir = configs["data_dir"]
        self.buffer_size = configs["buffer_size"]
        self.batch_size = configs["batch_size"]
        self.src_tokenizer = src_tokenizer
        self.tar_tokenizer = tar_tokenizer

    def read_data(self):
        if self.dataset_name == "bd_multi_tribe":
            src_seqs = mt.utils.helpers.read_file(os.path.join(
                self.data_dir, self.dataset_name, self.src_lang + ".txt"))
            tar_seqs = mt.utils.helpers.read_file(os.path.join(
                self.data_dir, self.dataset_name, self.tar_lang + ".txt"))
            return np.array(src_seqs), np.array(tar_seqs)

        elif self.dataset_name == "spa-eng":
            lines = mt.utils.helpers.read_file(os.path.join(self.data_dir, dataset_name, "spa.txt"))
            pairs = [line.split('\t') for line in lines]
            context = np.array([context for target, context in pairs])
            target = np.array([target for target, context in pairs])
            return context, target
        elif self.dataset_name == "bn2ipa":
            df = pd.read_csv(os.path.join(self.data_dir, dataset_name, "bn2ipa.csv"))
            context = df["text"].to_list()
            target = df["ipa"].to_list()
            context = np.array(context)
            target = np.array(target)
            return context, target
        elif self.dataset_name == "hasan-etal-2020-low":
            src_seqs = mt.utils.helpers.read_file(os.path.join(
                self.data_dir, self.dataset_name, self.src_lang + ".txt"))
            tar_seqs = mt.utils.helpers.read_file(os.path.join(
                self.data_dir, self.dataset_name, self.tar_lang + ".txt"))
            return np.array(src_seqs), np.array(tar_seqs)
        else:
            raise Exception(f"MyError: Dataset name: {self.dataset_name} not found.")

    def load(self):
        context_raw, target_raw = self.read_data()

        is_train = np.random.uniform(size=(len(target_raw),)) < 0.8

        test_context_examples = context_raw[~is_train]
        test_target_examples = target_raw[~is_train]

        train_raw = (
            tf.data.Dataset
            .from_tensor_slices((context_raw[is_train], target_raw[is_train]))
            .shuffle(self.buffer_size)
            .batch(self.batch_size))

        val_raw = (
            tf.data.Dataset
            .from_tensor_slices((context_raw[~is_train], target_raw[~is_train]))
            .shuffle(self.buffer_size)
            .batch(self.batch_size))

        self.src_tokenizer.adapt(train_raw.map(lambda context, target: context))
        self.tar_tokenizer.adapt(train_raw.map(lambda context, target: target))

        train_ds = train_raw.map(self.process_text, tf.data.AUTOTUNE)
        val_ds = val_raw.map(self.process_text, tf.data.AUTOTUNE)
        return train_ds, val_ds, test_context_examples, test_target_examples

    def process_text(self, context, target):
        context = self.src_tokenizer(context).to_tensor()
        target = self.tar_tokenizer(target)
        targ_in = target[:, :-1].to_tensor()
        targ_out = target[:, 1:].to_tensor()
        return (context, targ_in), targ_out
