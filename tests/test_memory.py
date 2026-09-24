import pytest

from memory.memory_store import MemoryStore
from agents.memory_agent import MemoryAgent


@pytest.fixture
def memory_store():
    store = MemoryStore()
    yield store
    store.close()


def test_memory_store_creation(memory_store):
    assert memory_store is not None


def test_save_memory(memory_store):
    result = memory_store.save_memory(
        "Python is a programming language.",
        "technical"
    )

    # Current implementation successfully saves the memory
    # but returns None.
    assert result is None
    assert memory_store.get_memory_count() >= 1


def test_search_memory(memory_store):
    memory_store.save_memory(
        "Python is used for artificial intelligence.",
        "technical"
    )

    results = memory_store.search_memory(
        "Python artificial intelligence"
    )

    assert isinstance(results, list)
    assert len(results) > 0


def test_search_no_match(memory_store):
    results = memory_store.search_memory(
        "completely unrelated xyz information"
    )

    assert isinstance(results, list)


def test_memory_count(memory_store):
    memory_store.save_memory(
        "First memory",
        "test"
    )

    count = memory_store.get_memory_count()

    assert count >= 1


def test_multiple_memories(memory_store):
    memory_store.save_memory(
        "Python programming",
        "technical"
    )

    memory_store.save_memory(
        "Machine learning",
        "technical"
    )

    memory_store.save_memory(
        "Data science",
        "technical"
    )

    count = memory_store.get_memory_count()

    assert count >= 3


def test_memory_similarity_search(memory_store):
    memory_store.save_memory(
        "I am building an AI project using Python.",
        "project"
    )

    results = memory_store.search_memory(
        "AI project Python"
    )

    assert isinstance(results, list)
    assert len(results) > 0


def test_memory_agent_creation():
    agent = MemoryAgent()

    assert agent is not None

    agent.close()


def test_memory_agent_remember():
    agent = MemoryAgent()

    result = agent.remember(
        "I am building a multi-agent AI project.",
        "project"
    )

    assert result is True

    agent.close()


def test_memory_agent_recall():
    agent = MemoryAgent()

    agent.remember(
        "I am building a multi-agent AI project using Python.",
        "project"
    )

    results = agent.recall(
        "multi-agent AI project"
    )

    assert isinstance(results, list)
    assert len(results) > 0

    agent.close()


def test_memory_agent_count():
    agent = MemoryAgent()

    agent.remember(
        "First project memory",
        "project"
    )

    count = agent.memory_count()

    assert count >= 1

    agent.close()