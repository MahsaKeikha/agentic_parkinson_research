from pathlib import Path


def test_reference_structure():
    required = ["AGENTS", "TOOLS", "SKILLS", "orchestration", "memory", "state", "schemas", "prompts", "config", "safety", "observability", "evals", "benchmarks", "examples", "docs"]
    for name in required:
        assert Path(name).exists()
    assert len(list(Path("AGENTS").glob("*.py"))) >= 6
    assert len(list(Path("TOOLS").glob("*.py"))) >= 5
    assert len(list(Path("SKILLS").glob("*.py"))) >= 5
