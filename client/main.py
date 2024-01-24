import click


@click.command()
@click.argument('color')
@click.option('--host', '-h')
@click.option('--port', '-p')
def main(color, host, port):
    URL = f'http://{host}:{port}/game'
    print(URL)
    print(color)


if __name__ == '__main__':
    main()
