from .types import CodeGeneration, DirectoryContext, FileGeneration
from .modules import import_file
from .conversions import get_pascal_name

from csv import DictReader
from fnmatch import fnmatch
from io import StringIO
from jinja2 import Template
from typing import Any, Dict, Iterable, List, IO, Optional
from pathlib import Path
import json
import shutil
import yaml

def _load_yaml_file(filename: str) -> Any:
    with open(filename, 'r') as fd:
        return yaml.safe_load(fd)

def _load_json_file(filename: str) -> Any:
    with open(filename, 'r') as fd:
        return json.load(fd)

def _load_csv_file(filename: str, header: Optional[List[str]] = None) -> Any:
    with open(filename, 'r') as fd:
        return list( DictReader(fd, fieldnames=header) )


class VarStorage:
    def __init__(self):
        self._vars : Dict[str, Any] = {}

    def clear_vars(self) -> None:
        self._vars.clear()

    def set_var(self, name: str, value: Any) -> None:
        self._vars[name] = value

    def all_vars(self) -> Dict[str, Any]:
        return self._vars


class CodeGenerator(VarStorage):
    def __init__(self):
        super().__init__()
        self._funcs : Dict[str, Any] = {}

    def load_module(self, py_file: str) -> None:
        module = import_file(py_file)
        for name in dir(module):
            if hasattr(getattr(module, name), '__call__'):
                self._funcs[name] = getattr(module, name)

    def _init_template_env(self, tpl: Template) -> None:
        tpl.environment.globals['pascal_name'] = get_pascal_name
        tpl.environment.globals['yaml'] = _load_yaml_file
        tpl.environment.globals['json'] = _load_json_file
        tpl.environment.globals['csv'] = _load_csv_file
        for name, func in self._funcs.items():
            tpl.environment.globals[name] = func

    def generate_string(self, input_template_file: str) -> str:
        tpl = Template( Path(input_template_file).read_text() )
        self._init_template_env(tpl)
        return tpl.render(**self._vars)

    def generate(self, input_template_file: str, output_file: str) -> None:
        Path(output_file).write_text( self.generate_string(input_template_file) )


class FileProcessorBase:
    def __init__(self, input_dir: str, output_dir: str):
        self._input_dir = Path(input_dir)
        self._output_dir = Path(output_dir)
        self._processors = {}

    def _on_unknown_file(self, input_file: Path, output_file: Path) -> None:
        self._copy_file(input_file, output_file)
    
    def _copy_file(self, input_file: Path, output_file: Path) -> None:
        if input_file.is_dir():
            output_file.mkdir(exist_ok=True)
        else:
            shutil.copyfile(str(input_file), str(output_file), follow_symlinks=False)
    
    def _process_files(self, input_dir: Path, output_dir: Path) -> None:
        output_dir.mkdir(parents=True, exist_ok=True)

        for item in input_dir.iterdir():
            self._process_item(input_dir, output_dir, item)

    def _process_item(self, input_dir: Path, output_dir: Path, item: Path) -> None:
        if item.is_dir():
            self._process_files(input_dir / item.name, output_dir / item.name)
        else:
            proc = self._processors.get(item.suffix, self._on_unknown_file)
            proc(input_dir / item.name, output_dir / item.name)


class TextReplacementFileProcessor(FileProcessorBase):
    def __init__(self, input_dir: str, output_dir: str):
        super().__init__(input_dir, output_dir)
        self._replacements = {}
        self._ignore_ptns = []

    def ignore_pattern(self, ptn: str) -> None:
        self._ignore_ptns.append(ptn)

    def _ignore_file(self, fn: str) -> bool:
        for ptn in self._ignore_ptns:
            if fnmatch(fn, ptn):
                return True

        return False

    def replace(self, key: bytes, value: bytes) -> None:
        self._replacements[key] = value

    def _replace_all(self, line: bytes) -> str:
        for from_bstr, to_bstr in self._replacements.items():
            line = line.replace(from_bstr, to_bstr)
        return line

    def _replace_text(self, input_file: Path, output_file: Path) -> None:
        with input_file.open('rb') as in_fd:
            with output_file.open('wb') as out_fd:
                for line in in_fd:
                    line = self._replace_all(line)
                    out_fd.write(line)

    def _on_unknown_file(self, input_file: Path, output_file: Path) -> None:
        self._replace_text(input_file, output_file)
    
    def _process_files(self, input_dir: Path, output_dir: Path) -> None:
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for item in input_dir.iterdir():
            if not item.is_dir() and self._ignore_file(item.name):
                self._copy_file(input_dir / item.name, output_dir / item.name)
            else:
                self._process_item(input_dir, output_dir, item)
    
    def process(self) -> None:
        self._process_files(self._input_dir, self._output_dir)


class FileProcessor(FileProcessorBase):
    def __init__(self, input_dir: str, output_dir: str, generator: CodeGenerator):
        super().__init__(input_dir, output_dir)
        self._code_gen = generator
        self._processors[".j2"] = self._process_jinja

    def _get_directory_context(self, input_dir: Path) -> DirectoryContext:
        codeify_template = input_dir / ".codeify"
        if codeify_template.is_file():
            return load_directory_context_yaml(self._code_gen, str(codeify_template))
        else:
            return DirectoryContext()
    
    def _process_jinja(self, input_file: Path, output_file: Path) -> None:
        # Drop last extension from file
        self._code_gen.generate(str(input_file), str(output_file.with_suffix("")))
    
    def _process_files(self, input_dir: Path, output_dir: Path) -> DirectoryContext:
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Check for ".codeify" file first
        ctx = self._get_directory_context(input_dir)

        for item in input_dir.iterdir():
            if ctx.ignore_file(item.name):
                continue
            self._process_item(input_dir, output_dir, item)

        return ctx

    def process(self) -> None:
        ctx = self._process_files(self._input_dir, self._output_dir)

        self._post_generation(self._input_dir, self._output_dir, ctx)
        
    def _post_generation(self, input_dir: Path, output_dir: Path, ctx: DirectoryContext) -> None:
        # Post-generation instructions
        generator = CodeGenerator()
        for file_gen in ctx.file_generators:
            generator.clear_vars()
            for key, value in file_gen.data.items():
                generator.set_var(key, value)
            
            inp, outp = input_dir / Path(file_gen.input_file), output_dir / Path(file_gen.output_file)
            generator.generate(str(inp), str(outp))


def load_code_generator_yaml(yaml_file: str) -> CodeGenerator:
    code_gen = CodeGenerator()
    data = yaml.safe_load(Path(yaml_file).read_text())
    for name, value in data.items():
        code_gen.set_var(name, value)
    return code_gen


def load_directory_context_yaml(code_gen: CodeGenerator, yaml_j2_file: str) -> DirectoryContext:
    file_gen : List[FileGeneration] = []

    ctx_data = yaml.safe_load( code_gen.generate_string(yaml_j2_file) )
    ignore = ctx_data.get('ignore', []) + ['.codeify']
    for output_file, input_data in ctx_data.get('generate', {}).items():
        file_gen.append( FileGeneration(input_data['input'], output_file, input_data.get('data', {})) )

    return DirectoryContext(ignore_files=ignore, file_generators=file_gen)


def run_generation(info: CodeGeneration) -> None:
    code_gen = load_code_generator_yaml(info.spec_file)

    for module_file in info.modules:
        code_gen.load_module(module_file)

    file_proc = FileProcessor(info.input_dir, info.output_dir, code_gen)
    file_proc.process()


def _parse_template_args(template_args: Iterable[str]) -> Dict[str, Any]:
    with StringIO() as yaml_buf:
        for arg in template_args:
            name, value = arg.split('=', 1)
            yaml_buf.write(f"\"{name.strip()}\": {value.strip()}\n")
        yaml_buf.seek(0)
        return yaml.safe_load(yaml_buf)


def _process_template_args(storage: VarStorage, template_args: Iterable[str]) -> None:
    for key, value in self._parse_template_args(template_args).items():
        storage.set_var(key, value)


def generate_output(template_file: str, template_args: Iterable[str], spec_file: Optional[str], output: IO, modules: Iterable[str]) -> None:
    code_gen = CodeGenerator()

    if spec_file:
        with open(spec_file, 'r') as fd:
            yaml_data = yaml.safe_load(fd)
        # Apply first to code generator
        for key, value in yaml_data.items():
            code_gen.set_var(key, value)
    
    if template_args:
        _process_template_args(code_gen, template_args)
    
    for module_file in modules:
        code_gen.load_module(module_file)

    output.write( code_gen.generate_string(template_file) )


def replace_text(input_dir: str, output_dir: str, spec_file: Optional[str], template_args: Iterable[str], ignore_patterns: Iterable[str]) -> None:
    fp = TextReplacementFileProcessor(Path(input_dir), Path(output_dir))

    for ptn in ignore_patterns:
        fp.ignore_pattern(ptn)

    if spec_file:
        with open(spec_file, 'r') as fd:
            yaml_data = yaml.safe_load(fd)
        # Apply first to file processor
        for key, value in yaml_data.items():
            fp.replace(str(key).encode('utf-8'), str(value).encode('utf-8'))
    
    if template_args:
        for key, value in _parse_template_args(template_args).items():
            fp.replace(key.encode('utf-8'), str(value).encode('utf-8'))

    fp.process()
