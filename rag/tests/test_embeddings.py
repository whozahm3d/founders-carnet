import pytest

from rag.compliance.embeddings import EmbeddingError, SentenceTransformerEncoder


class FakeSentenceTransformer:
    def __init__(self, vectors):
        self.vectors = vectors
        self.call = None

    def encode(self, texts, *, normalize_embeddings, convert_to_numpy):
        self.call = (texts, normalize_embeddings, convert_to_numpy)
        return self.vectors


def test_encoder_uses_normalized_batch_encoding_and_returns_python_floats():
    model = FakeSentenceTransformer([[1, 0], [0, 1]])
    encoder = SentenceTransformerEncoder("configured-model", model=model)

    vectors = encoder.encode(["first passage", "second passage"])

    assert vectors == ((1.0, 0.0), (0.0, 1.0))
    assert model.call == (["first passage", "second passage"], True, True)


def test_encoder_rejects_blank_input_and_inconsistent_output():
    encoder = SentenceTransformerEncoder("configured-model", model=FakeSentenceTransformer([]))

    with pytest.raises(EmbeddingError, match="must not be empty"):
        encoder.encode(["   "])

    encoder = SentenceTransformerEncoder(
        "configured-model",
        model=FakeSentenceTransformer([[1, 2], [3]]),
    )
    with pytest.raises(EmbeddingError, match="inconsistent dimensions"):
        encoder.encode(["first", "second"])


def test_encoder_requires_explicit_model_name():
    with pytest.raises(ValueError, match="must be configured"):
        SentenceTransformerEncoder(" ")
