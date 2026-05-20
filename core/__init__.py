from .assembler import (
    CPUCore,
    MemoryFilter,
    InvalidInstructionException,
    ParameterOutOfRangeException,
    CodeOutOfRangeException,
    InstructionLoadControlSignals,
    ControlSignals,
    assemble,
    disassemble,
    instructions,
    bintoint,
    getint,
    hexstr,
    sanitize,
)

try:
    from .compiler import (
        CompilerError,
        FunctionPrototype,
        GlobalVariable,
        Sections,
        CompilerSettings,
        builtin_forward_refs,
        parse_forward_refs,
        parse_and_compile_module,
        compile_module,
        set_working_directory,
        set_file_loader,
        add_library_directory,
        clear_library,
    )
    COMPILER_AVAILABLE = True
except ImportError:
    COMPILER_AVAILABLE = False

__all__ = [
    "CPUCore",
    "MemoryFilter",
    "InvalidInstructionException",
    "ParameterOutOfRangeException",
    "CodeOutOfRangeException",
    "InstructionLoadControlSignals",
    "ControlSignals",
    "assemble",
    "disassemble",
    "instructions",
    "bintoint",
    "getint",
    "hexstr",
    "sanitize",
]

if COMPILER_AVAILABLE:
    __all__ += [
        "CompilerError",
        "FunctionPrototype",
        "GlobalVariable",
        "Sections",
        "CompilerSettings",
        "builtin_forward_refs",
        "parse_forward_refs",
        "parse_and_compile_module",
        "compile_module",
        "set_working_directory",
        "set_file_loader",
        "add_library_directory",
        "clear_library",
    ]
