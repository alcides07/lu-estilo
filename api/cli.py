import typer
from subprocess import run

app = typer.Typer()


@app.command()
def migrations(
    message: str = typer.Option(..., "-m", "--message", help="Mensagem da migração")
):
    """
    Cria uma nova migração automática com o Alembic.
    Exemplo: python cli.py migrations -m "add user table"
    """
    cmd = f"alembic revision --autogenerate -m '{message}'"
    run(cmd, shell=True, check=True, capture_output=True)


@app.command()
def migrate():
    """Aplica todas as migrações pendentes."""
    run("alembic upgrade head", shell=True, check=True, capture_output=True)


if __name__ == "__main__":
    app()
