import library
import typer
from rich.console import Console
from rich.table import Table
from typing import Optional, Annotated




console = Console()

app = typer.Typer()
#app = typer.Typer(no_args_is_help=True, invoke_without_command=True)

@app.command("start")
def start():
    starter = library.start()
    typer.secho(starter, fg = typer.colors.BRIGHT_GREEN)

    # TODO: connect to database


# This is how you can get arguments, here username is a mandatory argument for this command.
@app.command("sign_up")
def sign_up(username: str):
    signuper = library.sign_up(username)
    typer.secho(signuper)
    # TODO: Add user with name {username} to database table


# This is how you can get arguments for login.
@app.command("sign_in")
def sign_in(username: str, password: str):
    signiner = library.sign_in(username, password)
    typer.secho(signiner)

# This is how you can get arguments for login.
@app.command("add_book")
def add_book():
    adder = library.add_book()
    typer.secho(adder, fg=typer.colors.GREEN)

@app.command("search_by_name")
def search_by_name(name: str):
    searcher = library.queries01(name)
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=10)
    table.add_column("ID", style="dim", width=10)
    table.add_column("Title", style="dim", min_width=10, justify=True)
    table.add_column("Author", style="dim", min_width=10, justify=True)
    table.add_column("Pages", style="dim", min_width=10, justify=True)
    table.add_column("Genre", style="dim", min_width=10, justify=True)
    table.add_column("Availability", style="dim", min_width=10, justify=True)
    i = 0
    for x in searcher.search_by_name():
        i += 1
        table.add_row(str(i), str(x[0]), x[1], x[2],str(x[3]), x[4], str(bool(x[5])))
    console.print(table)
    #typer.secho(searcher.search_by_name())

@app.command("search_by_author")
def search_by_author(name: str):
    searcher = library.queries01(name)
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=10)
    table.add_column("ID", style="dim", width=10)
    table.add_column("Title", style="dim", min_width=10, justify=True)
    table.add_column("Author", style="dim", min_width=10, justify=True)
    table.add_column("Pages", style="dim", min_width=10, justify=True)
    table.add_column("Genre", style="dim", min_width=10, justify=True)
    table.add_column("Availability", style="dim", min_width=10, justify=True)
    i = 0
    for x in searcher.search_by_author():
        i += 1
        table.add_row(str(i), str(x[0]), x[1], x[2],str(x[3]), x[4], str(bool(x[5])))
    console.print(table)
    #typer.secho(searcher.search_by_author())

@app.command("recently_added")
def recently_added(name: Annotated[Optional[str], typer.Argument()] = None):
    adder = library.queries01(name)
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=10)
    table.add_column("ID", style="dim", width=10)
    table.add_column("Title", style="dim", min_width=10, justify=True)
    table.add_column("Author", style="dim", min_width=10, justify=True)
    table.add_column("Pages", style="dim", min_width=10, justify=True)
    table.add_column("Genre", style="dim", min_width=10, justify=True)
    table.add_column("Availability", style="dim", min_width=10, justify=True)
    i = 0
    for x in adder.recently_added():
        i += 1
        table.add_row(str(i), str(x[0]), x[1], x[2],str(x[3]), x[4], str(bool(x[5])))
    console.print(table)
    #typer.secho(adder.recently_added())

@app.command("borrow_book")
def borrow_book(id_book: int, username: str):
    borrower = library.queries02(id_book, username)
    typer.secho(borrower.borrow_book())

@app.command("return_book")
def return_book(id_book: int, username: str):
    returner = library.queries02(id_book, username)
    typer.secho(returner.return_book())

@app.command("mark_read")
def mark_read(id_book: int, username: str):
    readmarker = library.queries02(id_book, username)
    typer.secho(readmarker.mark_read())

@app.command("fav_book")
def fav_book(id_book: int, username: str):
    favoriter = library.queries02(id_book, username)
    typer.secho(favoriter.fav_book(), color= True)


@app.command("most_read_books")
def most_read_books(genre: Annotated[Optional[str], typer.Argument()] = None):
    reader = library.queries01(genre)
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=10)
    table.add_column("ID", style="dim", width=10)
    table.add_column("Title", style="dim", min_width=10, justify=True)
    table.add_column("Author", style="dim", min_width=10, justify=True)
    table.add_column("Genre", style="dim", min_width=10, justify=True)
    table.add_column("Count", style="dim", min_width=10, justify=True)
    i = 0
    for x in reader.most_read_books():
        i += 1
        table.add_row(str(i), str(x[0]), x[1], x[2],str(x[3]), str(x[4]))
    console.print(table)

@app.command("most_favorite_books")
def most_read_books(genre: Annotated[Optional[str], typer.Argument()] = None):
    reader = library.queries01(genre)
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=10)
    table.add_column("ID", style="dim", width=10)
    table.add_column("Title", style="dim", min_width=10, justify=True)
    table.add_column("Author", style="dim", min_width=10, justify=True)
    table.add_column("Genre", style="dim", min_width=10, justify=True)
    table.add_column("Count", style="dim", min_width=10, justify=True)
    i = 0
    for x in reader.most_favorite_books():
        i += 1
        table.add_row(str(i), str(x[0]), x[1], x[2],str(x[3]), str(x[4]))
    console.print(table)

@app.command("most_read_genres")
def most_read_genres():
    reader = library.queries03()
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=10)
    table.add_column("Genre", style="dim", min_width=10, justify=True)
    table.add_column("Count", style="dim", min_width=10, justify=True)
    i = 0
    for x in reader.most_read_genres():
        i += 1
        table.add_row(str(i), str(x[0]), str(x[1]))
    console.print(table)

@app.command("most_read_authors")
def most_read_authors():
    reader = library.queries03()
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=10)
    table.add_column("Genre", style="dim", min_width=10, justify=True)
    table.add_column("Count", style="dim", min_width=10, justify=True)
    i = 0
    for x in reader.most_read_authors():
        i += 1
        table.add_row(str(i), str(x[0]), str(x[1]))
    console.print(table)

@app.command("my_books")
def my_books():
    reader = library.my_books()
    reader.returned()

@app.command("statistics")
def my_books():
    reader = library.my_books()
    reader.statistics()

@app.command("statistics")
def statistics():
    statis = library.my_books()
    statis.statistics()




if __name__ == "__main__":
    app()

