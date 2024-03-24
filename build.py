from asyncio import gather, run
from asyncio.subprocess import create_subprocess_exec
from pathlib import Path


async def build_file(target_file, binary_filename, client = False):
    print(f'Start building {binary_filename}')
    build_cmd = [
        'pyinstaller',
        str(target_file),
        '--name', binary_filename,
        '--onefile',
    ]
    if client:
        build_cmd += [
            '--add-data', r'static:static',
        ]
    else:
        build_cmd += [
            '--hidden-import', 'server.main'
        ]
    process = await create_subprocess_exec(*build_cmd)
    await process.wait()
    print(f'Build {binary_filename}')


async def build():
    client_target_file = Path.cwd() / 'client' / 'main.py'
    client_binary_filename = 'MillClient'
    server_target_file = Path.cwd() / 'server' / 'main.py'
    server_binary_filename = 'MillServer'
    await gather(
        build_file(client_target_file, client_binary_filename, client=True),
        build_file(server_target_file, server_binary_filename),
    )

if __name__ == '__main__':
    run(build())