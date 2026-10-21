import argparse
from datetime import datetime
import html
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import parse_qs, urlsplit


def normalize_target(value):
    if value.startswith(('http://', 'https://')):
        parsed = urlsplit(value)
        if parsed.hostname != 'pan.baidu.com' or not parsed.path.startswith('/disk/'):
            raise ValueError('Only personal pan.baidu.com /disk/ navigation URLs are supported.')
        parameters = parse_qs(parsed.fragment.partition('?')[2] or parsed.query)
        value = parameters.get('path', [''])[0]
    if not value.startswith('/') or any(character in value for character in '\r\n\x00'):
        raise ValueError('Provide an absolute Netdisk directory path or a URL containing path=.')
    return value.rstrip('/') or '/'


def parse_tree(text):
    nodes = []
    stack = []
    paths = set()
    for line in text.splitlines():
        if not line.strip():
            continue
        match = re.fullmatch(r'((?:│   |    )*)[├└]── (.*)', line)
        if not match:
            raise ValueError('Unexpected tree output; inspect tree-raw.log. Export was not verified.')
        depth = len(match[1]) // 4
        name = match[2]
        directory = name.endswith('/')
        name = name[:-1] if directory else name
        if not name or depth > len(stack):
            raise ValueError('Invalid name or missing parent in tree output.')
        stack = stack[:depth]
        path = '/'.join([nodes[index]['name'] for index in stack] + [name])
        if path in paths:
            raise ValueError('Duplicate path in tree output; completeness cannot be verified.')
        paths.add(path)
        node = dict(id=len(nodes), parent=stack[-1] if stack else None, name=name,
                    directory=directory, path=path,
                    ext='' if directory else Path(name).suffix.lower())
        nodes.append(node)
        if directory:
            stack.append(node['id'])
    if not nodes:
        raise ValueError('No tree entries: verify whether this is an empty directory or a failed listing.')
    return nodes


def read_source(source, target=None):
    text = source.read_text(encoding='utf-8-sig')
    lines = text.splitlines()
    if len(lines) >= 4 and lines[1].startswith('网盘路径：') and lines[2].startswith('导出时间：'):
        return normalize_target(lines[1].split('：', 1)[1]), lines[2].split('：', 1)[1], '\n'.join(lines[4:])
    if target is None:
        raise ValueError('Raw tree logs require --target.')
    return normalize_target(target), '未记录（由已有目录转换）', text


def write_outputs(output, target, timestamp, tree, nodes):
    title = (target.rsplit('/', 1)[-1] or '网盘根目录') + ' · 资料目录'
    metadata = f'网盘路径：{target} · 导出时间：{timestamp}'
    template = (Path(__file__).resolve().parent.parent / 'assets' / 'directory.html').read_text(encoding='utf-8')
    payload = json.dumps(dict(nodes=nodes, metadata=metadata), ensure_ascii=False).replace('<', '\\u003c')
    rendered = template.replace('__TITLE__', html.escape(title)).replace('__DATA__', payload)
    text = f'{title}\n网盘路径：{target}\n导出时间：{timestamp}\n\n{tree.rstrip()}\n'
    output.mkdir(parents=True, exist_ok=True)
    with (output / 'directory.txt').open('x', encoding='utf-8-sig') as handle:
        handle.write(text)
    with (output / 'directory.html').open('x', encoding='utf-8') as handle:
        handle.write(rendered)
    return dict(output=str(output), entries=len(nodes), folders=sum(node['directory'] for node in nodes),
                files=sum(not node['directory'] for node in nodes))


def main():
    parser = argparse.ArgumentParser(description='Read-only Baidu directory export and offline HTML conversion.')
    commands = parser.add_subparsers(dest='command', required=True)
    export = commands.add_parser('export')
    export.add_argument('--tool', type=Path, required=True)
    export.add_argument('--config-dir', type=Path, required=True)
    export.add_argument('--target', required=True)
    convert = commands.add_parser('convert')
    convert.add_argument('--input', type=Path, required=True)
    convert.add_argument('--target')
    for command in (export, convert):
        command.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    output = arguments.output.resolve()
    if any((output / name).exists() for name in ('directory.txt', 'directory.html', 'tree-raw.log', 'stderr.log')):
        raise ValueError('Output already contains export files. Choose a new output directory.')
    if arguments.command == 'export':
        target = normalize_target(arguments.target)
        tool = arguments.tool.resolve(strict=True)
        configuration = arguments.config_dir.resolve(strict=True)
        if not configuration.is_dir():
            raise ValueError('Configuration must be a directory used for this session login.')
        environment = os.environ.copy()
        environment['BAIDUPCS_GO_CONFIG_DIR'] = str(configuration)
        environment['BAIDUPCS_GO_VERBOSE'] = '0'
        output.mkdir(parents=True, exist_ok=True)
        print('Reading directory metadata only; large trees may take several minutes.', flush=True)
        with (output / 'tree-raw.log').open('wb') as stdout, (output / 'stderr.log').open('wb') as stderr:
            result = subprocess.run([str(tool), 'tree', target], env=environment, stdout=stdout, stderr=stderr)
        if result.returncode or (output / 'stderr.log').read_bytes().strip():
            raise ValueError('Client reported an error. Inspect the local logs; no final export generated.')
        tree = (output / 'tree-raw.log').read_text(encoding='utf-8-sig')
        timestamp = datetime.now().astimezone().isoformat(timespec='seconds')
    else:
        target, timestamp, tree = read_source(arguments.input, arguments.target)
    nodes = parse_tree(tree)
    print(json.dumps(write_outputs(output, target, timestamp, tree, nodes), ensure_ascii=False))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, UnicodeError) as error:
        print(f'Export failed: {error}', file=sys.stderr)
        sys.exit(1)
