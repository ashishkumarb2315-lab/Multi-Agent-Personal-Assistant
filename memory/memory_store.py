import os
import sqlite3
import re
import math
from collections import Counter


class MemoryStore:
    """
    SQLite-based long-term memory store.

    Features:
    - Persistent memory
    - Fast storage
    - Keyword-based semantic-style search
    - Metadata support
    - No external model
    - No internet dependency
    """

    def __init__(self):

        # ------------------------------------------------
        # Project directory
        # ------------------------------------------------

        project_root = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

        # ------------------------------------------------
        # Database location
        # ------------------------------------------------

        self.database_path = os.path.join(
            project_root,
            "memory",
            "memory.db"
        )

        print("\nInitializing SQLite memory database...")

        # ------------------------------------------------
        # SQLite connection
        # ------------------------------------------------

        self.connection = sqlite3.connect(
            self.database_path
        )

        # ------------------------------------------------
        # Create memory table
        # ------------------------------------------------

        self._create_table()

        print("SQLite memory database ready.")

    # ====================================================
    # CREATE TABLE
    # ====================================================

    def _create_table(self):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS memories (

                id TEXT PRIMARY KEY,

                memory TEXT NOT NULL,

                category TEXT,

                source TEXT,

                created_at TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP

            )
            """
        )

        self.connection.commit()

    # ====================================================
    # TEXT TOKENIZATION
    # ====================================================

    def _tokenize(self, text: str) -> list[str]:

        words = re.findall(
            r"\b[a-zA-Z0-9]+\b",
            text.lower()
        )

        # Remove very common words
        stop_words = {
            "the",
            "is",
            "a",
            "an",
            "and",
            "or",
            "to",
            "of",
            "in",
            "on",
            "for",
            "with",
            "my",
            "i",
            "am",
            "using"
        }

        return [
            word
            for word in words
            if word not in stop_words
        ]

    # ====================================================
    # SIMILARITY
    # ====================================================

    def _calculate_similarity(
        self,
        query: str,
        document: str
    ) -> float:

        query_words = self._tokenize(
            query
        )

        document_words = self._tokenize(
            document
        )

        if not query_words or not document_words:

            return 0.0

        query_counter = Counter(
            query_words
        )

        document_counter = Counter(
            document_words
        )

        # ------------------------------------------------
        # Cosine similarity
        # ------------------------------------------------

        all_words = set(
            query_counter.keys()
        ).union(
            document_counter.keys()
        )

        query_vector = []
        document_vector = []

        for word in all_words:

            query_vector.append(
                query_counter[word]
            )

            document_vector.append(
                document_counter[word]
            )

        dot_product = sum(
            q * d
            for q, d in zip(
                query_vector,
                document_vector
            )
        )

        query_magnitude = math.sqrt(
            sum(
                q * q
                for q in query_vector
            )
        )

        document_magnitude = math.sqrt(
            sum(
                d * d
                for d in document_vector
            )
        )

        if (
            query_magnitude == 0
            or document_magnitude == 0
        ):

            return 0.0

        similarity = (
            dot_product
            /
            (
                query_magnitude
                *
                document_magnitude
            )
        )

        return similarity

    # ====================================================
    # SAVE MEMORY
    # ====================================================

    def save_memory(
        self,
        memory: str,
        memory_id: str,
        metadata: dict | None = None
    ):

        if not memory.strip():

            raise ValueError(
                "Memory cannot be empty."
            )

        metadata = metadata or {}

        category = metadata.get(
            "category",
            "general"
        )

        source = metadata.get(
            "source",
            "unknown"
        )

        print("\nSaving memory...")

        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT OR REPLACE INTO memories
            (
                id,
                memory,
                category,
                source
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                memory_id,
                memory,
                category,
                source
            )
        )

        self.connection.commit()

        print(
            "Memory saved successfully."
        )

    # ====================================================
    # SEARCH MEMORY
    # ====================================================

    def search_memory(
        self,
        query: str,
        number_of_results: int = 3
    ) -> list[str]:

        if not query.strip():

            return []

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                memory
            FROM memories
            """
        )

        rows = cursor.fetchall()

        if not rows:

            return []

        scored_results = []

        for memory_id, memory in rows:

            similarity = (
                self._calculate_similarity(
                    query,
                    memory
                )
            )

            scored_results.append(
                (
                    similarity,
                    memory
                )
            )

        # ------------------------------------------------
        # Sort highest similarity first
        # ------------------------------------------------

        scored_results.sort(
            key=lambda item: item[0],
            reverse=True
        )

        # ------------------------------------------------
        # Return only useful matches
        # ------------------------------------------------

        results = []

        for similarity, memory in scored_results:

            if similarity > 0:

                results.append(memory)

            if len(results) >= number_of_results:

                break

        return results

    # ====================================================
    # MEMORY COUNT
    # ====================================================

    def get_memory_count(self) -> int:

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM memories
            """
        )

        result = cursor.fetchone()

        return result[0]

    # ====================================================
    # CLOSE DATABASE
    # ====================================================

    def close(self):

        if self.connection:

            self.connection.close()


# ========================================================
# TEST PROGRAM
# ========================================================

def main():

    print()

    print("=" * 60)
    print("LONG-TERM MEMORY STORE TEST")
    print("=" * 60)

    memory = None

    try:

        # ------------------------------------------------
        # Initialize memory
        # ------------------------------------------------

        memory = MemoryStore()

        print(
            f"\nCurrent memories: "
            f"{memory.get_memory_count()}"
        )

        # ------------------------------------------------
        # Test memory
        # ------------------------------------------------

        test_memory = (
            "I am building a B.Tech final year "
            "Multi-Agent Personal Assistant Swarm "
            "using Python, Gemini and LangGraph."
        )

        # ------------------------------------------------
        # Save
        # ------------------------------------------------

        memory.save_memory(
            memory=test_memory,
            memory_id="test_memory_001",
            metadata={
                "category": "project",
                "source": "memory_test"
            }
        )

        # ------------------------------------------------
        # Count
        # ------------------------------------------------

        print(
            f"\nTotal memories now: "
            f"{memory.get_memory_count()}"
        )

        # ------------------------------------------------
        # Search
        # ------------------------------------------------

        query = input(
            "\nSearch memory:\n> "
        ).strip()

        if not query:

            print(
                "\nNo search query entered."
            )

            return

        print(
            "\nSearching memory..."
        )

        results = memory.search_memory(
            query=query,
            number_of_results=3
        )

        # ------------------------------------------------
        # Display results
        # ------------------------------------------------

        print()

        print("=" * 60)
        print("MEMORY SEARCH RESULTS")
        print("=" * 60)

        if results:

            for index, result in enumerate(
                results,
                start=1
            ):

                print()

                print(
                    f"{index}. {result}"
                )

        else:

            print(
                "\nNo relevant memories found."
            )

        # ------------------------------------------------
        # Final count
        # ------------------------------------------------

        print()

        print("=" * 60)

        print(
            f"Total stored memories: "
            f"{memory.get_memory_count()}"
        )

        print("=" * 60)

    except Exception as error:

        print()

        print("=" * 60)
        print("MEMORY ERROR")
        print("=" * 60)

        print(
            f"Error Type: "
            f"{type(error).__name__}"
        )

        print(
            f"Error Message: "
            f"{error}"
        )

    finally:

        if memory:

            memory.close()


# ========================================================
# RUN PROGRAM
# ========================================================

if __name__ == "__main__":

    main()