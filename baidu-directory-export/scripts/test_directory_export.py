import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import directory_export as exporter


class ExportTests(unittest.TestCase):
    def test_structure_and_names(self):
        nodes = exporter.parse_tree('├── 课程/\n│   ├── 10.pdf\n│   └── 2.mp4\n└── 空目录/\n')
        self.assertEqual(nodes[2]['path'], '课程/2.mp4')
        self.assertEqual(nodes[2]['parent'], 0)
        self.assertTrue(nodes[3]['directory'])

    def test_invalid_output(self):
        for text in ('', '请重新登录', '├── a.pdf\n未知行', '│   └── 孤立.pdf', '├── a\n└── a'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                exporter.parse_tree(text)

    def test_target_url(self):
        self.assertEqual(exporter.normalize_target('https://pan.baidu.com/disk/main#/index?category=all&path=%2Ftest'), '/test')
        for value in ('https://pan.baidu.com/s/test', 'relative', 'https://evil.example/disk/main?path=/'):
            with self.assertRaises(ValueError):
                exporter.normalize_target(value)

    def test_safe_html_and_roundtrip(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            tree = '└── <script>&.pdf'
            exporter.write_outputs(output, '/Test & <title>', '2026', tree, exporter.parse_tree(tree))
            rendered = (output / 'directory.html').read_text(encoding='utf-8')
            self.assertNotIn('<script>&.pdf', rendered)
            self.assertIn('Test &amp; &lt;title&gt;', rendered)
            self.assertEqual(exporter.read_source(output / 'directory.txt'), ('/Test & <title>', '2026', tree))
            with self.assertRaises(FileExistsError):
                exporter.write_outputs(output, '/test', '2026', tree, exporter.parse_tree(tree))

    def test_explicit_session_and_read_only_command(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            tool = root / 'client.exe'
            tool.touch()
            configuration = root / 'session'
            configuration.mkdir()
            output = root / 'export'
            def fake_run(command, **kwargs):
                self.assertEqual(command, [str(tool), 'tree', '/test'])
                self.assertEqual(kwargs['env']['BAIDUPCS_GO_CONFIG_DIR'], str(configuration))
                self.assertEqual(kwargs['env']['BAIDUPCS_GO_VERBOSE'], '0')
                kwargs['stdout'].write('└── file.pdf\n'.encode('utf-8'))
                return type('Result', (), {'returncode': 0})()
            arguments = ['directory_export.py', 'export', '--tool', str(tool), '--config-dir', str(configuration), '--target', '/test', '--output', str(output)]
            with patch('sys.argv', arguments), patch('subprocess.run', side_effect=fake_run), contextlib.redirect_stdout(io.StringIO()):
                exporter.main()
            self.assertTrue((output / 'directory.html').exists())


if __name__ == '__main__':
    unittest.main()
