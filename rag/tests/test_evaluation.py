import json
from types import SimpleNamespace

from rag.evaluation.evaluate import (
    _chunk_token_limit,
    _numpy_dense,
    _tune_abstention_threshold,
    load_questions,
    split_dev_test,
)


def test_existing_questions_are_preserved_without_generated_answers():
    raw = open("rag/evaluation/gold_questions.jsonl", encoding="utf-8").read().splitlines()
    # Retain the repository's existing authored set; do not synthesize answers.
    assert len(raw) == 20
    assert all("gold_answer" not in line for line in raw)
    questions = load_questions()
    assert len(questions) == 20
    dev, test = split_dev_test(questions)
    assert (len(dev), len(test)) == (6, 14)
    raw_questions = {json.loads(line)["id"]: json.loads(line) for line in raw}
    for question_id in ("q009", "q010"):
        assert raw_questions[question_id]["answerable"] is False
        assert raw_questions[question_id]["out_of_scope_category"] == "outside indexed scope"
    assert all("supporting_chunk_ids" in item for item in raw_questions.values())


def test_numpy_dense_uses_cosine_over_normalized_vectors():
    chunks = (
        SimpleNamespace(id=1, chunk_id="aligned", text="aligned", embedding=(3.0, 0.0)),
        SimpleNamespace(id=2, chunk_id="orthogonal", text="orthogonal", embedding=(0.0, 4.0)),
    )
    ranked = _numpy_dense((2.0, 0.0), chunks, top_k=2)
    assert [row.chunk.chunk_id for row in ranked] == ["aligned", "orthogonal"]
    assert ranked[0].score == 1.0
    assert ranked[1].score == 0.0


def test_abstention_threshold_is_tuned_against_dev_labels():
    scores = {"yes-1": 0.91, "yes-2": 0.82, "no-1": 0.11, "no-2": 0.03}
    labels = {"yes-1": False, "yes-2": False, "no-1": True, "no-2": True}
    threshold = _tune_abstention_threshold(scores, labels)
    assert 0.11 < threshold <= 0.82


def test_e5_chunk_limit_reserves_tokens_for_passage_prefix():
    class Tokenizer:
        def __call__(self, text, *, add_special_tokens):
            return {"input_ids": [1, 2, 3] if text == "passage: " else [1]}

    model = SimpleNamespace(max_seq_length=512, tokenizer=Tokenizer())
    assert _chunk_token_limit("intfloat/multilingual-e5-base", model) == 509
    assert _chunk_token_limit("sentence-transformers/model", model) == 512
