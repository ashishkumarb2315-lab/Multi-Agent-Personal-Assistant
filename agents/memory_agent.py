import sys
import os

# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ============================================================
# IMPORT MEMORY STORE
# ============================================================

from memory.memory_store import MemoryStore


# ============================================================
# MEMORY AGENT
# ============================================================

class MemoryAgent:
    """
    Memory Agent

    Provides persistent long-term memory
    using SQLite.

    Responsibilities:
    - Store useful information
    - Retrieve relevant information
    - Track memory count
    """

    def __init__(self):

        self.mode = "sqlite"

        self.memory_store = MemoryStore()

        print("\nMemory Agent Mode: SQLITE")

    # ========================================================
    # STORE MEMORY
    # ========================================================

    def remember(
        self,
        information: str,
        category: str = "general"
    ):

        if not information.strip():
            return False

        self.memory_store.save_memory(
            information,
            category
        )

        print(
            f"\nMemory stored successfully."
        )

        return True

    # ========================================================
    # RECALL MEMORY
    # ========================================================

    def recall(
        self,
        query: str,
        number_of_results: int = 5
    ):

        if not query.strip():
            return []

        results = self.memory_store.search_memory(
            query,
            number_of_results
        )

        return results

    # ========================================================
    # MEMORY COUNT
    # ========================================================

    def memory_count(self):

        return self.memory_store.get_memory_count()

    # ========================================================
    # CLOSE MEMORY
    # ========================================================

    def close(self):

        self.memory_store.close()


# ============================================================
# INTERACTIVE TEST
# ============================================================

def main():

    print("\n")
    print("=" * 60)
    print("MEMORY AGENT TEST")
    print("=" * 60)

    memory_agent = MemoryAgent()

    # --------------------------------------------------------
    # STORE TEST MEMORY
    # --------------------------------------------------------

    memory_agent.remember(
        "The user is building a Multi-Agent "
        "Personal Assistant Swarm using Python, "
        "LangGraph and SQLite.",
        "project"
    )

    # --------------------------------------------------------
    # SEARCH MEMORY
    # --------------------------------------------------------

    print("\n")
    print("=" * 60)
    print("MEMORY SEARCH")
    print("=" * 60)

    results = memory_agent.recall(
        "Multi-Agent Personal Assistant"
    )

    for index, result in enumerate(
        results,
        start=1
    ):

        print(
            f"\n{index}. {result}"
        )

    # --------------------------------------------------------
    # COUNT
    # --------------------------------------------------------

    print("\n")
    print(
        "Total memories:",
        memory_agent.memory_count()
    )

    memory_agent.close()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()