from types import SimpleNamespace

from rag.compliance.retrieve import bm25, dense, hybrid


def _chunk(chunk_id: str, text: str, vector: list[float], row_id: int):
    return SimpleNamespace(id=row_id, chunk_id=chunk_id, text=text, embedding=vector)


def test_dense_bm25_and_hybrid_share_output_shape_and_hybrid_uses_rrf():
    chunks = [
        _chunk("a", "Company registration documents and procedure.", [1.0, 0.0], 1),
        _chunk("b", "Income tax rate and filing requirements.", [0.0, 1.0], 2),
    ]

    dense_rows = dense([1.0, 0.0], chunks)
    bm25_rows = bm25("company registration procedure", chunks)
    hybrid_rows = hybrid("company registration procedure", [1.0, 0.0], chunks)

    assert dense_rows[0].chunk.chunk_id == "a"
    assert bm25_rows[0].chunk.chunk_id == "a"
    assert hybrid_rows[0].chunk.chunk_id == "a"
    assert {row.method for row in dense_rows} == {"dense"}
    assert {row.method for row in bm25_rows} == {"bm25"}
    assert {row.method for row in hybrid_rows} == {"hybrid"}
    assert all(0 <= row.score <= 1 for row in hybrid_rows)


def test_bm25_returns_no_match_instead_of_arbitrary_top_chunk():
    chunks = [_chunk("a", "Company registration documents.", [1.0, 0.0], 1)]
    assert bm25("completely unrelated", chunks) == ()


def test_hybrid_caps_internal_candidate_count_to_retriever_limit():
    chunks = [
        _chunk(f"chunk-{index}", f"Company registration document {index}.", [1.0, 0.0], index)
        for index in range(25)
    ]
    ranked = hybrid("company registration", [1.0, 0.0], chunks, top_k=5)
    assert len(ranked) == 5
    assert all(row.method == "hybrid" for row in ranked)
