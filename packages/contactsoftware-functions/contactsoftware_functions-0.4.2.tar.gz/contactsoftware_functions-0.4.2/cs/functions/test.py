import typer
from cs.functions.handler import execute

app = typer.Typer()


@app.command()
def test(source_path: str, function_name: str, payload_file: str) -> dict:
    with open(payload_file, "rb") as f:
        print(execute(function_name, f.read(), source_path))


if __name__ == "__main__":
    app()
