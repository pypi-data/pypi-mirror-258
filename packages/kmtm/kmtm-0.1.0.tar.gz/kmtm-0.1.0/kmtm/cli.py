import click


@click.command()
@click.argument("number", nargs=1, type=float, required=True)
@click.option(
    "--kilos", "-k",
    is_flag=True,
    default=False,
    help="Kilometers is the desired output. Assumes miles is given."
    )
@click.option(
    "--miles", "-m",
    is_flag=True,
    default=False,
    help="Miles is the desired output. Assumes kilometers is given."
    )
def cli(number, kilos, miles):
    if kilos:
        converted_value = round(number * 1.60934, 2)
        click.echo(f"{number} miles is {converted_value} kilometers.")
    if miles:
        converted_value = round(number * 0.62137, 2)
        click.echo(f"{number} kilometers is {converted_value} miles.")
