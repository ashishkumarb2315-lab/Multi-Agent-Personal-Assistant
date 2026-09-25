import sqlite3
import re
import math
from collections import Counter


class MemoryStore:
    """
    SQLite-based persistent memory store.

    Stores memories and provides lightweight
    keyword/cosine-similarity search.
    """

    def __init__(self):
        print("\nInitializing SQLite memory database...")

        self.database_path = "memory/memory.db"

        # check_same_thread=False allows the SQLite connection
        # to be safely used by Streamlit's execution thread.
        self.connection = sqlite3.connect(
            self.database_path,
            check_same_thread=False
        )

        self.cursor = self.connection.cursor()

        self._create_table()

        print("SQLite memory database ready.")

    def _create_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                category TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        self.connection.commit()

    def _tokenize(self, text):
        """
        Convert text into lowercase word tokens.
        """

        return re.findall(
            r"\b[a-zA-Z0-9]+\b",
            text.lower()
        )

    def _calculate_similarity(self, text1, text2):
        """
        Calculate cosine similarity between two texts
        using simple word-frequency vectors.
        """

        tokens1 = self._tokenize(text1)
        tokens2 = self._tokenize(text2)

        if not tokens1 or not tokens2:
            return 0.0

        counter1 = Counter(tokens1)
        counter2 = Counter(tokens2)

        all_words = set(counter1) | set(counter2)

        vector1 = [
            counter1.get(word, 0)
            for word in all_words
        ]

        vector2 = [
            counter2.get(word, 0)
            for word in all_words
        ]

        dot_product = sum(
            a * b
            for a, b in zip(vector1, vector2)
        )

        magnitude1 = math.sqrt(
            sum(a * a for a in vector1)
        )

        magnitude2 = math.sqrt(
            sum(b * b for b in vector2)
        )

        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0

        return dot_product / (
            magnitude1 * magnitude2
        )

    def save_memory(self, content, category="general"):
        """
        Save a memory into SQLite.
        """

        print("\nSaving memory...")

        try:

            self.cursor.execute(
                """
                SELECT id
                FROM memories
                WHERE content = ?
                """,
                (content,)
            )

            existing = self.cursor.fetchone()

            if existing:

                print("Memory already exists.")

                return None

            self.cursor.execute(
                """
                INSERT INTO memories
                (content, category)
                VALUES (?, ?)
                """,
                (
                    content,
                    category
                )
            )

            self.connection.commit()

            print("Memory saved successfully.")

            return None

        except sqlite3.Error as error:

            print(
                f"Memory save error: {error}"
            )

            return None

    def search_memory(
        self,
        query,
        number_of_results=5
    ):
        """
        Search stored memories using
        cosine similarity.
        """

        print("\nSearching memory...")

        self.cursor.execute(
            """
            SELECT
                id,
                content,
                category,
                created_at
            FROM memories
            """
        )

        rows = self.cursor.fetchall()

        scored_results = []

        for row in rows:

            memory_id = row[0]
            content = row[1]
            category = row[2]
            created_at = row[3]

            similarity = self._calculate_similarity(
                query,
                content
            )

            if similarity > 0:

                scored_results.append(
                    (
                        similarity,
                        memory_id,
                        content,
                        category,
                        created_at
                    )
                )

        scored_results.sort(
            key=lambda item: item[0],
            reverse=True
        )

        results = []

        for item in scored_results[:number_of_results]:

            results.append(item[2])

        return results

    def get_memory_count(self):
        """
        Return total number of stored memories.
        """

        self.cursor.execute(
            """
            SELECT COUNT(*)
            FROM memories
            """
        )

        result = self.cursor.fetchone()

        return result[0]

    def close(self):
        """
        Close SQLite connection safely.
        """

        try:

            if self.connection:

                self.connection.close()

        except sqlite3.Error:
            pass


if __name__ == "__main__":

    store = MemoryStore()

    store.save_memory(
        "I am building a multi-agent AI project.",
        "project"
    )

    results = store.search_memory(
        "multi-agent AI project"
    )

    print("\n" + "=" * 60)
    print("MEMORY SEARCH RESULTS")
    print("=" * 60)

    for index, result in enumerate(
        results,
        start=1
    ):

        print(
            f"\n{index}. {result}"
        )

    print(
        f"\nTotal stored memories: "
        f"{store.get_memory_count()}"
    )

    store.close()