import sqlite3


class db:
    def __init__(self, db_file):
        '''Инициализация соединения с бд'''
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        '''Создание таблиц'''
        self.cursor.executescript(
            '''
            CREATE TABLE IF NOT EXISTS users (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            bread   INTEGER NOT NULL,
            cat     INTEGER NOT NULL
            );

            
            CREATE TABLE IF NOT EXISTS messages (
            id         INTEGER  PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER  REFERENCES users (user_id) ON DELETE CASCADE NOT NULL,
            chat_id    INTEGER  NOT NULL,
            message_id DOUBLE   NOT NULL,
            content    VARCHAR  NOT NULL,
            date_time  DATETIME NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS statistic (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER REFERENCES users (id) ON DELETE CASCADE
                            NOT NULL,
            bread   INTEGER NOT NULL,
            cat     INTEGER NOT NULL
            );
            '''
        )
        return self.conn.commit()

    def user_exists(self, user_id):
        """Проверяем, есть ли юзер в БД"""
        result = self.cursor.execute("SELECT id FROM users WHERE user_id = ?", (user_id,))
        return bool(len(result.fetchall()))

    def add_user(self, user_id):
        '''Добавлям юзера в бд'''
        self.cursor.execute("INSERT INTO users (user_id, bread, cat) VALUES (?, 0, 0)", (user_id,))
        return self.conn.commit()

    def update_bread(self, user_id):
        '''Добавляем в статистику +1 к хлебу'''
        self.cursor.execute("UPDATE users set bread = bread + 1 WHERE user_id = ?", (user_id,))
        return self.conn.commit()

    def update_cat(self, user_id):
        '''Добавляем в статистику +1 к коту'''
        self.cursor.execute("UPDATE users set cat = cat + 1 WHERE user_id = ?", (user_id,))
        return self.conn.commit()

    def add_statistics(self, user_id):
        '''Добавлям статистику для каждого пользователя'''
        self.cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        return self.conn.commit()

    def add_message(self, user_id, chat_id, message_id, content, date_time):
        '''Добавляем сообщение в бд'''
        self.cursor.execute("INSERT INTO messages (user_id, chat_id, message_id, content, date_time) VALUES (?, ?, ?, ?, ?)",
                            (user_id, chat_id, message_id, content, date_time,))
        return self.conn.commit()