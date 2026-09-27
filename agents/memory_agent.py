from memory.memory_store import MemoryStore


class MemoryAgent:
    """
    Memory Agent

    Provides an interface between the agent workflow
    and the persistent MemoryStore.

    Responsibilities:
    - Save information into memory
    - Recall relevant memories
    - Count stored memories
    - Close the memory database
    """

    def __init__(self, database_path=None):
        """
        Initialize the Memory Agent.

        Parameters
        ----------
        database_path : str or None
            Optional path to the SQLite memory database.

            If no path is supplied, MemoryStore will use
            its default database location.
        """

        if database_path is None:
            self.memory_store = MemoryStore()
        else:
            self.memory_store = MemoryStore(
                database_path
            )

    # ============================================================
    # REMEMBER
    # ============================================================

    def remember(
        self,
        content,
        category="general"
    ):
        """
        Save information into memory.

        Parameters
        ----------
        content : str
            Information to remember.

        category : str
            Category of the memory.

        Returns
        -------
        bool
            True if the operation completes successfully.
        """

        try:

            self.memory_store.save_memory(
                content,
                category
            )

            return True

        except Exception:
            return False

    # ============================================================
    # SAVE MEMORY
    # ============================================================

    def save_memory(
        self,
        content,
        category="general"
    ):
        """
        Save memory.

        This is an alias for remember() and is used
        by the workflow for compatibility.
        """

        return self.remember(
            content,
            category
        )

    # ============================================================
    # RECALL
    # ============================================================

    def recall(
        self,
        query,
        number_of_results=5
    ):
        """
        Recall memories relevant to a query.

        Parameters
        ----------
        query : str
            Search query.

        number_of_results : int
            Maximum number of memories to return.

        Returns
        -------
        list
            Relevant memories.
        """

        try:

            return self.memory_store.search_memory(
                query,
                number_of_results
            )

        except Exception:
            return []

    # ============================================================
    # RECALL MEMORY
    # ============================================================

    def recall_memory(
        self,
        query,
        number_of_results=5
    ):
        """
        Recall relevant memories.

        This is an alias for recall() and is used
        by the workflow for compatibility.
        """

        return self.recall(
            query,
            number_of_results
        )

    # ============================================================
    # MEMORY COUNT
    # ============================================================

    def memory_count(self):
        """
        Return the total number of stored memories.

        Returns
        -------
        int
            Number of stored memories.
        """

        try:

            return self.memory_store.get_memory_count()

        except Exception:
            return 0

    # ============================================================
    # GET MEMORY COUNT
    # ============================================================

    def get_memory_count(self):
        """
        Alias for memory_count().
        """

        return self.memory_count()

    # ============================================================
    # CLOSE
    # ============================================================

    def close(self):
        """
        Close the memory database safely.
        """

        try:

            self.memory_store.close()

        except Exception:
            pass


# ================================================================
# DIRECT TEST
# ================================================================

if __name__ == "__main__":

    print("=" * 60)
    print("MEMORY AGENT TEST")
    print("=" * 60)

    agent = MemoryAgent()

    # ------------------------------------------------------------
    # Save memory
    # ------------------------------------------------------------

    print("\nSaving memory...")

    result = agent.remember(
        "I am building a multi-agent AI project using Python.",
        "project"
    )

    print(
        "Memory saved:",
        result
    )

    # ------------------------------------------------------------
    # Recall memory
    # ------------------------------------------------------------

    print("\nRecalling memory...")

    memories = agent.recall(
        "multi-agent AI project Python"
    )

    if memories:

        for index, memory in enumerate(
            memories,
            start=1
        ):

            print(
                f"{index}. {memory}"
            )

    else:

        print("No memories found.")

    # ------------------------------------------------------------
    # Memory count
    # ------------------------------------------------------------

    print(
        "\nMemory count:",
        agent.memory_count()
    )

    # ------------------------------------------------------------
    # Close
    # ------------------------------------------------------------

    agent.close()

    print(
        "\nMemory Agent test completed."
    )