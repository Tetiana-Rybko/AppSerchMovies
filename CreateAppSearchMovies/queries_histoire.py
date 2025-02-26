import sqlite3


class SearchHistory:
    def __init__(self, db_file="search_history.db"):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        # Создаем таблицу для хранения запросов, если её ещё нет
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS search_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query_text TEXT UNIQUE,
                search_count INTEGER DEFAULT 1
            )
        """)
        self.conn.commit()

    def save_query(self, query_text):
        # Если такой запрос уже есть, увеличиваем счётчик, иначе вставляем новый
        try:
            self.cursor.execute("""
                INSERT INTO search_history (query_text, search_count)
                VALUES (?, 1)
            """, (query_text,))
        except sqlite3.IntegrityError:
            # Запрос уже есть, обновляем счётчик
            self.cursor.execute("""
                UPDATE search_history
                SET search_count = search_count + 1
                WHERE query_text = ?
            """, (query_text,))
        self.conn.commit()

    def get_popular_queries(self, limit=10):
        self.cursor.execute("""
            SELECT query_text, search_count
            FROM search_history
            ORDER BY search_count DESC
            LIMIT ?
        """, (limit,))
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()
