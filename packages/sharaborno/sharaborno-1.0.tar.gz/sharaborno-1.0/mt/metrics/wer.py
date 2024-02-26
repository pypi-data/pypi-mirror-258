import numpy as np
from jiwer import wer


def word_error_rate(model, src_seqs, tar_seqs):
    pred_seqs = []
    for i, src_seq in enumerate(src_seqs):
        pred_seq = model.translate(src_seq)
        pred_seqs.append(pred_seq)

    src_seqs = np.array(src_seqs)
    tar_seqs = np.array(tar_seqs)

    return wer(src_seqs, tar_seqs)
