import numpy as np
from . import utilities
from . import constants

target_vectorization = utilities.read_pickle_tv(constants.target_tv_path)
source_vectorization = utilities.read_pickle_tv(constants.source_tv_path)
seq2seq_rnn = utilities.reconstruct_model_from_h5(constants.seq2seq_rnn_path)
spa_vocab = target_vectorization.get_vocabulary()
spa_index_lookup = dict(zip(range(len(spa_vocab)), spa_vocab))
max_decoded_sentence_length = 20


def decode_sequence_rnn(input_sentence):
    tokenized_input_sentence = source_vectorization([input_sentence])
    decoded_sentence = "start"
    for i in range(max_decoded_sentence_length):
        tokenized_target_sentence = target_vectorization([decoded_sentence])
        next_token_predictions = seq2seq_rnn.predict(
            [tokenized_input_sentence, tokenized_target_sentence])
        sampled_token_index = np.argmax(next_token_predictions[0, i, :])
        sampled_token = spa_index_lookup[sampled_token_index]
        decoded_sentence += " " + sampled_token
        if sampled_token == "end":
            break

    return " ".join(decoded_sentence.split()[1:-1])
