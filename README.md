# Entropy Branching Functions
1. `python build_input.py [golden_result_file]` generates string with whitespace and newline characters to `input_str.utf8`. 
- `python build_entropy_dict.py [-f|-b]` generates forward and backward ngram entropy from `input_str.utf8` into `forward_entropy_dict.utf8` and `backward_entropy_dict.utf8`, respectively.
- `python seg.py [value_delta]` runs entropy branching on `input_str.utf8` with ngram entropy file and generates result in `seg_result.utf8`.
- `python compute_score.py [golden_result_file]` compares `seg_result.utf8` and `[golden_reuslt_file]`, and computes recall and precision.
- `python main.py [golden_result] [value_delta]` runs end-to-end script.
