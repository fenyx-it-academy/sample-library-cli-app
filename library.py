import sqlite3
import datetime
from colorama import Fore, Back, Style
from rich.console import Console
from rich.table import Table
from main import console



class start:
    def create_connection(self, file):
        conn = None
        try:
            conn = sqlite3.connect(file)
        except:
            print('The system can not connect to the database')

        return conn
    def create_database(self):
        self.cur.execute(f"""CREATE TABLE books (
            book_id integer primary key AUTOINCREMENT,
            title text NOT NULL,
            author_id integer,
            pages integer NOT NULL,
            genre_id integer NOT NULL,
            added_by integer,
            added_date datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
            num_readed integer ,
            votes integer ,
            rating integer,
            tally integer,
            FOREIGN KEY (genre_id) REFERENCES genre (genre_id),
            FOREIGN KEY (author_id) REFERENCES author (author_id),
            FOREIGN KEY (added_by) REFERENCES users (user_id),
            FOREIGN KEY (book_id) REFERENCES borrow_books (book_id));""")
        self.cur.execute("""CREATE TABLE genre (
            genre_id integer primary key AUTOINCREMENT,
            name text NOT NULL,
            emoji text NOT NULL);""")
        self.cur.execute("""CREATE TABLE author (
            author_id integer primary key AUTOINCREMENT,
            name text NOT NULL);""")
        self.cur.execute("""CREATE TABLE orders (
            order_id integer primary key AUTOINCREMENT,
            user_id integer NOT NULL,
            book_id integer NOT NULL,
            borrowed boolean DEFAULT False,
            borrow_date datetime,
            returned boolean DEFAULT False,
            readed boolean DEFAULT False,
            favorite boolean DEFAULT False,
            FOREIGN KEY (user_id) REFERENCES user (user_id),
            FOREIGN KEY (book_id) REFERENCES books (book_id));""")
        self.cur.execute("""CREATE TABLE users (
            user_id integer primary key AUTOINCREMENT,
            username text NOT NULL,
            name text NOT NULL,
            password text NOT NULL,
            birthyear varchar NOT NULL,
            address text ,
            login_state boolean DEFAULT False,
            type varchar NOT NULL,
            FOREIGN KEY (type) REFERENCES person_type (type));""")
        self.cur.execute("""CREATE TABLE person_type (
            type varchar  primary key,
            name text NOT NULL);""")

    def insert_default_values(self):
        #Genre default values
        self.cur.execute("""INSERT INTO genre (name, emoji) VALUES ('Classics', '🏛️');""")
        self.cur.execute("""INSERT INTO genre (name, emoji) VALUES ('Comedy', '🤡');""")
        self.cur.execute("""INSERT INTO genre (name, emoji) VALUES ('Graphic Novels', '🦇');""")
        self.cur.execute("""INSERT INTO genre (name, emoji) VALUES ('Adventure', '⛯');""")
        self.cur.execute("""INSERT INTO genre (name, emoji) VALUES ('Science fiction', '👽');""")
        self.cur.execute("""INSERT INTO genre (name, emoji) VALUES ('Dystopian', '🧟‍♀️');""")
        self.cur.execute("""INSERT INTO genre (name, emoji) VALUES ('Realistic', '📕');""")
        self.cur.execute("""INSERT INTO genre (name, emoji) VALUES ('Movies', '🎞️');""")
        self.cur.execute("""INSERT INTO genre (name, emoji) VALUES ('Thriller', '😨');""")
        self.cur.execute("""INSERT INTO genre (name, emoji) VALUES ('Horror', '💀');""")
        self.cur.execute("""INSERT INTO genre (name, emoji) VALUES ('Animals', '🐘');""")
        self.cur.execute("""INSERT INTO genre (name, emoji) VALUES ('Fantasy', '🦄');""")
        self.cur.execute("""INSERT INTO genre (name, emoji) VALUES ('Sport', '🤼');""")
        self.cur.execute("""INSERT INTO genre (name, emoji) VALUES ('Mystery', '⁉️');""")
        self.cur.execute("""INSERT INTO genre (name, emoji) VALUES ('Romance', '💘');""")
        self.cur.execute("""INSERT INTO genre (name, emoji) VALUES ('Historical fiction', '🏺');""")
        self.cur.execute("""INSERT INTO genre (name, emoji) VALUES ('Short stories', '📜');""")

        #Default value of person_type
        self.cur.execute("""INSERT INTO person_type (type, name) VALUES ('u', 'user');""")
        self.cur.execute("""INSERT INTO person_type (type, name) VALUES ('p', 'personnel');""")



    def __str__(self):
        msg = f'''Welcome to Library CLI!📚 \n\nYou can execute command '--help' to see the possible commands'''
        con = self.create_connection("library.db")
        self.cur = con.cursor()
        x = self.cur.execute("""SELECT count(*) FROM sqlite_master WHERE type='table' """).fetchall()

        if x == [(0,)]:
            self.create_database()
            self.insert_default_values()


        con.commit()
        con.close()

        return msg
#End of the Start class

class sign_up(start):
    def __init__(self, username):
        self.un = username

    def __str__(self):
        con = self.create_connection("library.db")
        self.cur = con.cursor()

        while True:

            com = self.cur.execute(
                """SELECT username FROM users WHERE username = ?""", (self.un,)).fetchall()

            if [tuple([self.un])] == com:
                msg = Fore.RED + f"""This username already exists!\nPlease enter another username!🙁 """
                print(msg)
                self.un = input("Please enter your Username: ")
                continue
            else:
                break

        self.nm = input("Please enter your name: ")

        self.paas = input("Please enter your password: ")

        while True:
            try:
                self.b_d = int(input("Please enter your birth year: "))
            except:
                print("Your birth year must be a four digit number!")
                continue
            else:
                self.bd = str(self.b_d)
                if not(len(self.bd) == 4):
                    print("Your birth year must be a four digit number!")
                    continue
                else:
                    break

        self.add = input("Please enter your address: ")
        while True:
            self.tp = input("Please enter your user's type (p as personnel) or (u as user):").lower()
            if not(self.tp == 'p' or self.tp == 'u'):
                print("You have entered a wrong letter!")
                continue
            else:
                break

        self.cur.execute(
            """INSERT INTO users (username, name, password, birthyear, address, type) VALUES (?,?,?,?,?,?);
            """, (self.un, self.nm, self.paas, self.bd, self.add, self.tp))


        con.commit()
        con.close()

        return f"""Nice that you are signing up!👍 """
#End of the sign_up class


class sign_in(start):

    def __init__(self,username: str, password: str):
        self.uname = username
        self.pw = password

    def __str__(self):
        con = self.create_connection("library.db")
        cur = con.cursor()

        x1 = cur.execute("""SELECT user_id FROM users WHERE username = ? ; """, (self.uname,)).fetchall()
        x2 = cur.execute("""SELECT user_id FROM users WHERE username = ? And 
        password = ?""", (self.uname, self.pw)).fetchall()
        if len(x1) == 0:
            msg = Fore.RED + """⭕ Your username is wrong!⭕ """
        elif len(x2) == 0:
            msg = Fore.RED + """⭕ Your password is wrong!⭕ """
        else:
            msg = f"Let's sign you in!\n" + Fore.GREEN + f"User {x1[0][0]} successfully signed in!😄 "
            previous_id = cur.execute("""SELECT user_id FROM users WHERE login_state = ? """,
                                      (True,)).fetchall()

            if len(previous_id) == 0:
                cur.execute("""UPDATE users SET login_state = ? WHERE user_id = ? ;""",(True, x1[0][0]))
            else:
                cur.execute("""UPDATE users SET login_state = ? WHERE user_id = ?""",
                            (0, previous_id[0][0]))
                cur.execute("""UPDATE users SET login_state = ? WHERE user_id = ?""", (True, x1[0][0]))

        con.commit()
        con.close()

        return msg
#End of the sign_in class

class add_book(start):
    def __init__(self):
        self.con = self.create_connection("library.db")
        self.cur = self.con.cursor()
        x = self.cur.execute("""SELECT user_id FROM users WHERE login_state = True""").fetchall()

        if len(x) == 0:
            print(""" 🚨 For adding a book, you must log in first 🚨 """)
        else:
            print(""" ℹ️ Please enter the required book information to add ℹ️ """)
            self.title = input("Please enter the title of the book 📘 : ")
            author = input("Please enter the name of the author ✍️ : ")
            id_author = self.cur.execute("""SELECT author_id FROM author WHERE name = ? ;""",
                                         (author,)).fetchall()
            if len(id_author) == 0:
                self.cur.execute("""INSERT INTO author (name) VALUES (?);""",(author,))
                id_author = self.cur.execute("""SELECT author_id FROM author WHERE name = ? ;""",
                                             (author,)).fetchall()

            y = self.cur.execute("SELECT * FROM genre").fetchall()
            for i in y:
                print(i)
            c = True
            while c:
                genre = int(input("Please enter id of the genre from above table 👁️‍🗨️ :"))
                for f in y:
                    if f[0] == genre:
                        c = False
                        break

            pages = int(input("Please enter the numbers of pages 🗐 :"))
            tally = int(input("Please enter the number of the book #️⃣ :"))
            self.cur.execute("""INSERT INTO books (title, author_id, pages, genre_id, added_by, tally) 
            VALUES (?, ?, ?, ?, ?, ?);""",(self.title, id_author[0][0], pages, genre, x[0][0], tally))

            self.con.commit()

    def __str__(self):
        id1 = self.cur.execute("""SELECT book_id FROM books WHERE title = ? ;""",
                               (self.title,)).fetchall()
        msg = f""" 👌 The book with id {id1[0][0]} has been successfully added 👌 """

        self.con.commit()
        self.con.close()

        return msg
#END OF THE add_book CLASS

class queries01:
    def __init__(self, username):
        self.tag = username
        self.console = Console()

        self.con = sqlite3.connect("library.db")
        self.cur = self.con.cursor()


    def search_by_name(self):
        sql = '''SELECT books.book_id, books.title, author.name, books.pages, genre.name, books.tally
        FROM books INNER JOIN author ON author.author_id = books.author_id INNER JOIN 
        genre on genre.genre_id = books.genre_id WHERE books.title LIKE ?;'''
        my_pattern = f"%{self.tag}%"
        books = self.cur.execute(sql, (my_pattern,)).fetchall()
        return books

        self.con.close

    def search_by_author(self):
        sql = '''SELECT books.book_id, books.title, author.name, books.pages, genre.name, books.tally
        FROM books INNER JOIN author ON author.author_id = books.author_id INNER JOIN 
        genre on genre.genre_id = books.genre_id WHERE author.name LIKE ?;'''
        my_pattern = f"%{self.tag}%"
        books = self.cur.execute(sql, (my_pattern, )).fetchall()
        return books

        #self.con.commit()
        self.con.close

    def recently_added(self):
        if self.tag == None:
            sql = '''SELECT books.book_id, books.title, author.name, books.pages, genre.name, books.tally
                                FROM books INNER JOIN author ON author.author_id = books.author_id INNER JOIN 
                                genre on genre.genre_id = books.genre_id ORDER BY books.added_date LIMIT 5;'''
            books = self.cur.execute(sql).fetchall()
            return books
        else:
            genre = str(self.tag)
            genre = genre.lower()
            genre = genre.capitalize()
            txt = "ssss"
            t = txt.lower()
            x = self.cur.execute("""SELECT genre_id FROM genre WHERE name = ?""",
                                 (genre,)).fetchall()
            id_genre = x[0]
            sql = '''SELECT books.book_id, books.title, author.name, books.pages, genre.name, books.tally FROM 
            books INNER JOIN author ON author.author_id = books.author_id INNER JOIN 
            genre on genre.genre_id = books.genre_id WHERE genre.genre_id = ? 
            ORDER BY books.added_date LIMIT 5;'''
            books = self.cur.execute(sql, (id_genre)).fetchall()

            self.con.close()

            return books
        #END OF THE RECENTLY_ADDED

    def most_read_books(self):
        if self.tag == None:
            sql = """SELECT books.book_id, books.title, author.name, genre.name, COUNT(*) FROM
                    books INNER JOIN author ON author.author_id = books.author_id INNER 
                    JOIN genre ON genre.genre_id = books.genre_id 
                    INNER JOIN orders ON books.book_id = orders.book_id WHERE orders.readed = TRUE LIMIT 10;"""

            books = self.cur.execute(sql).fetchall()
            return books
        else:
            genre = str(self.tag)
            genre = genre.lower()
            genre = genre.capitalize()

            x = self.cur.execute("""SELECT genre_id FROM genre WHERE name = ?""",
                                 (genre,)).fetchall()
            id_genre = x[0]
            sql = """SELECT books.book_id, books.title, author.name, genre.name, COUNT(*) FROM
                                books INNER JOIN author ON author.author_id = books.author_id INNER 
                                JOIN genre ON genre.genre_id = books.genre_id 
                                INNER JOIN orders ON books.book_id = orders.book_id 
                                WHERE orders.readed = TRUE
                                AND genre.genre_id = ? LIMIT 10;"""
            books = self.cur.execute(sql, (id_genre)).fetchall()

        return books
    #End of the most_read_books

    def most_favorite_books(self):
        if self.tag == None:
            sql = """SELECT books.book_id, books.title, author.name, genre.name, COUNT(*) FROM
                    books INNER JOIN author ON author.author_id = books.author_id INNER 
                    JOIN genre ON genre.genre_id = books.genre_id 
                    INNER JOIN orders ON books.book_id = orders.book_id WHERE orders.favorite = TRUE LIMIT 10;"""

            books = self.cur.execute(sql).fetchall()
            return books
        else:
            genre = str(self.tag)
            genre = genre.lower()
            genre = genre.capitalize()

            x = self.cur.execute("""SELECT genre_id FROM genre WHERE name = ?""",
                                 (genre,)).fetchall()
            id_genre = x[0]
            sql = """SELECT books.book_id, books.title, author.name, genre.name, COUNT(*) FROM
                                books INNER JOIN author ON author.author_id = books.author_id INNER 
                                JOIN genre ON genre.genre_id = books.genre_id 
                                INNER JOIN orders ON books.book_id = orders.book_id 
                                WHERE orders.favorite = TRUE
                                AND genre.genre_id = ? LIMIT 10;"""
            books = self.cur.execute(sql, (id_genre)).fetchall()

        return books
    #End_of most_favorite_books

class queries02():
    def __init__(self, id_book, username):
        self.tag = id_book
        self.uname = username


        self.console = Console()
        self.con = sqlite3.connect("library.db")
        self.cur = self.con.cursor()

    def borrow_book(self):
        x = self.cur.execute("""SELECT user_id FROM users WHERE login_state = True""").fetchall()
        w = self.cur.execute("""SELECT user_id FROM users WHERE username = ?""",
                             (self.uname,)).fetchall()
        if x == w:
            if len(x) == 0:
                print(""" 🚨 For adding a book, you must log in first 🚨 """)
            else:
                sql = """SELECT tally FROM books WHERE book_id = ?;"""
                count = self.cur.execute(sql, (self.tag,)).fetchall()
                self.number = count[0][0]
                if self.number == 0:
                    self.msg = f"""Sorry, book {self.tag} is not available! Try again later 🏁 ."""
                else:
                    self.number -= 1
                    self.cur.execute("""UPDATE books SET tally = ? WHERE book_id = ?;""",
                                     (self.number, self.tag))
                    y = self.cur.execute("""SELECT borrowed FROM orders WHERE user_id = ? AND book_id = ?;""",
                                         (x[0][0], self.tag)).fetchall()
                    if len(y) == 0:
                        self.cur.execute("""INSERT INTO orders (user_id, book_id, borrowed, borrow_date) VALUES
                                    (?, ?, ?, ?)""", (x[0][0], self.tag, True, datetime.datetime.now()))
                    elif y[0][0] == False:
                        self.cur.execute("""INSERT INTO orders (borrowed, borrow_date) VALUES
                                                            (?, ?)""", (True, datetime.datetime.now()))
                    else:
                        self.cur.execute("""INSERT INTO orders (user_id, book_id, borrowed, borrow_date) VALUES
                                                            (?, ?, ?, ?)""",
                                         (x[0][0], self.tag, True, datetime.datetime.now()))
        else:
            print(""" 🚨 For adding a book, you must log in first 🚨 """)


        self.con.commit()
        self.con.close()
        msg = f"""YOU borrowed book {self.tag}"""
        return msg

    #End of borrowed_book

    def return_book(self):

        x = self.cur.execute("""SELECT user_id FROM users WHERE login_state = True""").fetchall()
        w = self.cur.execute("""SELECT user_id FROM users WHERE username = ?""",
                             (self.uname,)).fetchall()
        if x == w:
            if len(x) == 0:
                print(""" 🚨 For adding a book, you must log in first 🚨 """)
            else:
                bw_tag = self.cur.execute("""SELECT borrowed FROM orders WHERE book_id = ? AND user_id = ?;""",
                                          (self.tag, x[0][0])).fetchall()

                if len(bw_tag) == 0:
                    msg = f"""Sorry, you did not borrow book {self.tag} ☹️ ."""
                elif bw_tag[0][0] == True:
                    self.cur.execute("""UPDATE orders SET returned = ? WHERE book_id = ? AND user_id = ?;""",
                                     (True, self.tag, x[0][0])).fetchall()
                    y = self.cur.execute("""SELECT tally FROM books WHERE book_id = ?;""",
                                         (self.tag,)).fetchall()
                    number = y[0][0]
                    number += 1
                    self.cur.execute("""UPDATE books SET tally = ? WHERE book_id = ?;""",
                                     (number, self.tag)).fetchall()
                    msg = f"""You returned book {self.tag} 🙂 """
        else:
            print(""" 🚨 For adding a book, you must log in first 🚨 """)


        self.con.commit()
        self.con.close()
        return msg

    #END of the return_book

    def mark_read(self):
        x = self.cur.execute("""SELECT user_id FROM users WHERE login_state = True""").fetchall()
        w = self.cur.execute("""SELECT user_id FROM users WHERE username = ?""",
                             (self.uname,)).fetchall()
        if x == w:
            if len(x) == 0:
                print(""" 🚨 For set to reading a book, you must log in first 🚨 """)
            else:
                sbook = self.cur.execute("""SELECT book_id FROM orders WHERE book_id = ? AND user_id = ?""",
                                         (self.tag, self.uname)).fetchall()
                if len(sbook) == 0:
                    sbook = self.cur.execute("""SELECT book_id FROM books WHERE book_id = ?""",
                                            (self.tag,)).fetchall()
                    if len(sbook) ==0:
                        msg = f"""There is not the book with ID = {self.tag}"""
                    else:
                        self.cur.execute("""INSERT INTO orders (user_id , book_id, readed) VALUES (?, ?, ?)""",
                                         (x[0][0], self.tag, True))
                        msg = f""" 📖 You markt book {self.tag} as read 📖 """
                else:
                    self.cur.execute("""UPDATE orders SET readed = ? WHERE user_id = ? AND book_id = ?; """,
                                     (True, x[0][0], self.tag))
                    msg = f""" 📖 You markt book {self.tag} as read 📖 """
        else:
            print(""" 🚨 For set to reading a book, you must log in first 🚨 """)

        self.con.commit()
        self.con.close()
        return msg
    #End of the read mark

    def fav_book(self):
        x = self.cur.execute("""SELECT user_id FROM users WHERE login_state = True""").fetchall()
        w = self.cur.execute("""SELECT user_id FROM users WHERE username = ?""",
                             (self.uname,)).fetchall()
        if x == w:
            if len(x) == 0:
                msg = """ 🚨 For set a book to favorite, you must log in first 🚨 """
            else:
                sbook = self.cur.execute("""SELECT book_id FROM orders WHERE book_id = ? AND user_id = ?""",
                                         (self.tag, x[0][0])).fetchall()
                if len(sbook) == 0:
                    sbook2 = self.cur.execute("""SELECT book_id FROM books WHERE book_id = ?""",
                                             (self.tag,)).fetchall()
                    if len(sbook2) == 0:
                        msg = f""" 🚨 There is not a book with ID = {self.tag} 🚨 """
                    else:
                        self.cur.execute("""INSERT INTO orders (user_id , book_id, favorite) VALUES (?, ?, ?);""",
                                         (x[0][0], self.tag, True))
                        msg = f""" 📖 You added book {self.tag} to your favorites 📖 """
                else:
                    self.cur.execute("""UPDATE orders SET favorite = ? WHERE user_id = ? AND book_id = ?;""",
                                     (True, x[0][0], self.tag))
                    msg = f""" 📖 You added book {self.tag} to your favorites 📖 """
        else:
            msg = """ 🚨 For set a book to favorite, you must log in first 🚨 """

        self.con.commit()
        self.con.close()

        return msg
    #End of the fav_book

class queries03():
    def __init__(self):
        self.console = Console()
        self.con = sqlite3.connect("library.db")
        self.cur = self.con.cursor()


    def most_read_genres(self):
        sql = """SELECT genre.name, COUNT(*) FROM genre INNER JOIN books ON genre.genre_id = books.genre_id INNER JOIN
        orders ON books.book_id = orders.book_id WHERE orders.readed = TRUE LIMIT 5;"""

        x = self.cur.execute(sql).fetchall()

        return x
    #End of the most_read_genres

    def most_read_authors(self):
        sql = """SELECT author.name, COUNT(*) FROM author INNER JOIN books ON author.author_id = books.author_id INNER 
        JOIN orders ON books.book_id = orders.book_id WHERE orders.readed = TRUE LIMIT 3;"""

        x = self.cur.execute(sql).fetchall()

        return x

class my_books():
    console = Console()
    con = sqlite3.connect("library.db")
    cur = con.cursor()

    def statistics(self):
        x = self.cur.execute("""SELECT user_id FROM users WHERE login_state = TRUE;""").fetchall()

        sql_books = '''SELECT COUNT(*) FROM books INNER JOIN orders ON books.book_id = orders.book_id INNER JOIN
        users ON users.user_id = orders.user_id WHERE orders.readed = TRUE AND orders.user_id = ?;'''
        u_id = str(x[0][0])
        books = self.cur.execute(sql_books, u_id).fetchall()

        sql_authors = '''SELECT COUNT(*) FROM books INNER JOIN orders ON books.book_id = orders.book_id INNER JOIN
                users ON users.user_id = orders.user_id INNER JOIN author on author.author_id = books.author_id WHERE
                 orders.readed = TRUE AND orders.user_id = ?;'''
        u_id = str(x[0][0])
        authors = self.cur.execute(sql_authors, u_id).fetchall()

        sql_genre = '''SELECT COUNT(*) FROM books INNER JOIN orders ON books.book_id = orders.book_id INNER JOIN
                users ON users.user_id = orders.user_id INNER JOIN genre on genre.genre_id = books.genre_id WHERE
             orders.readed = TRUE AND orders.user_id = ?;'''
        u_id = str(x[0][0])
        genre = self.cur.execute(sql_genre, u_id).fetchall()

        table = Table(show_header=True, header_style="bold blue")
        table.add_column("statistics", style="dim", min_width=10, justify=True)
        table.add_column("Number", style="dim", min_width=10, justify=True)
        a = books[0][0]
        b = authors[0][0]
        c = genre[0][0]
        sum = a + b + c

        table.add_row("Books you read", str(a))
        table.add_row("Authors you read", str(b))
        table.add_row("Genre you read", str(c))
        table.add_row("Total pages you read", str(sum))
        console.print(table)

    def returned(self):
        x = self.cur.execute("""SELECT user_id FROM users WHERE login_state = TRUE;""").fetchall()
        sql = '''SELECT books.book_id, books.title, author.name, books.pages, genre.name, books.tally
                            FROM books INNER JOIN author ON author.author_id = books.author_id INNER JOIN
                            genre on genre.genre_id = books.genre_id INNER JOIN orders ON
                            books.book_id = orders.book_id INNER JOIN users ON users.user_id = orders.user_id
                            WHERE orders.returned = TRUE AND users.user_id = ?;'''
        u_id = str(x[0][0])
        books = self.cur.execute(sql, (u_id,)).fetchall()

        table1 = Table(show_header=True, header_style="bold blue")
        table1.add_column("#", style="dim", width=10)
        table1.add_column("ID", style="dim", width=10)
        table1.add_column("Title", style="dim", min_width=10, justify=True)
        table1.add_column("Author", style="dim", min_width=10, justify=True)
        table1.add_column("Pages", style="dim", min_width=10, justify=True)
        table1.add_column("Genre", style="dim", min_width=10, justify=True)
        table1.add_column("Availability", style="dim", min_width=10, justify=True)
        i = 0
        for x in books:
            i += 1
            s = str(i)
            table1.add_row(s, str(x[0]), x[1], x[2], str(x[3]), x[4], str(bool(x[5])))
        print("The books you read 📕 📕 📕 ")
        console.print(table1)
        print('\n')

        x = self.cur.execute("""SELECT user_id FROM users WHERE login_state = TRUE;""").fetchall()
        sql = '''SELECT books.book_id, books.title, author.name, books.pages, genre.name, books.tally
                                            FROM books INNER JOIN author ON author.author_id = books.author_id INNER JOIN
                                            genre on genre.genre_id = books.genre_id INNER JOIN orders ON
                                            books.book_id = orders.book_id INNER JOIN users ON users.user_id = orders.user_id
                                            WHERE orders.borrowed = TRUE AND users.user_id = ?;'''
        uid = str(x[0][0])
        books = self.cur.execute(sql, (uid,)).fetchall()

        table2 = Table(show_header=True, header_style="bold blue")
        table2.add_column("#", style="dim", width=10)
        table2.add_column("ID", style="dim", width=10)
        table2.add_column("Title", style="dim", min_width=10, justify=True)
        table2.add_column("Author", style="dim", min_width=10, justify=True)
        table2.add_column("Pages", style="dim", min_width=10, justify=True)
        table2.add_column("Genre", style="dim", min_width=10, justify=True)
        table2.add_column("Availability", style="dim", min_width=10, justify=True)
        i = 0
        for x in books:
            i += 1
            table2.add_row(str(i), str(x[0]), x[1], x[2], str(x[3]), x[4], str(bool(x[5])))

        print("The books you are reading 📖 📖 📖 ")
        console.print(table2)
        print('\n')

        x = self.cur.execute("""SELECT user_id FROM users WHERE login_state = TRUE;""").fetchall()
        sql = '''SELECT books.book_id, books.title, author.name, books.pages, genre.name, books.tally
                                                    FROM books INNER JOIN author ON author.author_id = books.author_id INNER JOIN
                                                    genre on genre.genre_id = books.genre_id INNER JOIN orders ON
                                                    books.book_id = orders.book_id INNER JOIN users ON users.user_id = orders.user_id
                                                    WHERE orders.readed = TRUE AND users.user_id = ?;'''
        u_id = str(x[0][0])

        books = self.cur.execute(sql, (u_id,)).fetchall()

        table3 = Table(show_header=True, header_style="bold blue")
        table3.add_column("#", style="dim", width=10)
        table3.add_column("ID", style="dim", width=10)
        table3.add_column("Title", style="dim", min_width=10, justify=True)
        table3.add_column("Author", style="dim", min_width=10, justify=True)
        table3.add_column("Pages", style="dim", min_width=10, justify=True)
        table3.add_column("Genre", style="dim", min_width=10, justify=True)
        table3.add_column("Availability", style="dim", min_width=10, justify=True)
        i = 0
        for x in books:
            i += 1
            table3.add_row(str(i), str(x[0]), x[1], x[2], str(x[3]), x[4], str(bool(x[5])))

        print("The books you will read 📘 📘 📘 ")
        console.print(table3)
        print('\n')

        x = self.cur.execute("""SELECT user_id FROM users WHERE login_state = TRUE;""").fetchall()
        sql = '''SELECT books.book_id, books.title, author.name, books.pages, genre.name, books.tally
                                                FROM books INNER JOIN author ON author.author_id = books.author_id INNER JOIN
                                                genre on genre.genre_id = books.genre_id INNER JOIN orders ON
                                                books.book_id = orders.book_id INNER JOIN users ON users.user_id = orders.user_id
                                                WHERE orders.favorite = TRUE AND users.user_id = ?;'''
        u_id = str(x[0][0])

        books = self.cur.execute(sql, (u_id,)).fetchall()

        table4 = Table(show_header=True, header_style="bold blue")
        table4.add_column("#", style="dim", width=10)
        table4.add_column("ID", style="dim", width=10)
        table4.add_column("Title", style="dim", min_width=10, justify=True)
        table4.add_column("Author", style="dim", min_width=10, justify=True)
        table4.add_column("Pages", style="dim", min_width=10, justify=True)
        table4.add_column("Genre", style="dim", min_width=10, justify=True)
        table4.add_column("Availability", style="dim", min_width=10, justify=True)
        i = 0
        for x in books:
            i += 1
            table4.add_row(str(i), str(x[0]), x[1], x[2], str(x[3]), x[4], str(bool(x[5])))

        print("Your favorite books 📚 📚 📚 ")
        console.print(table4)

        #con.close



