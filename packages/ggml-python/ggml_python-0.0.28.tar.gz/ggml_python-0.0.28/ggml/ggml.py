"""This module is the core of the ggml-python library, it exposes a low-level [ctypes](https://docs.python.org/3/library/ctypes.html)-based interface for ggml.

Structures and functions in the `ggml.ggml` module map directly to the original ggml C library and
they operate at a fairly low level.
No additional runtime checks checks are performed nor is memory management handled automatically.
You've been warned :).

With that in mind here are some useful things to keep in mind

- While runtime checks are avoided for performance reasons, this module attempts to provide a type-safe interface by using Python's type annotations. Please report any issues you find.
- Functions accept both ctypes types (c_int, c_bool, c_float, etc.) and Python types (int, bool, float, etc.) as parameters.
- Functions return Python types for simple values (int, bool, float, etc.) and ctypes types for complex values ([ggml_context_p][ggml.ggml_context_p], [ggml_tensor_p][ggml.ggml_tensor_p], etc.).
- Memory management is the responsibility of the user. The user must call [ggml.ggml_free][] on the context after calling [ggml.ggml_init][].
- Opaque pointers that are returned by ggml functions (e.g. [ggml.ggml_init][ggml.ggml_init]) are returned as int's or None in Python. For some additional static type safety these pointers are wrapped in [NewType](https://docs.python.org/3/library/typing.html#typing.NewType) definitions (e.g. [ggml.ggml_context_p][ggml.ggml_context_p]).

Example

```python
import ggml
import ctypes

# Allocate a new context with 16 MB of memory
params = ggml.ggml_init_params(mem_size=16 * 1024 * 1024, mem_buffer=None)
ctx = ggml.ggml_init(params)

# Instantiate tensors
x = ggml.ggml_new_tensor_1d(ctx, ggml.GGML_TYPE_F32, 1)
a = ggml.ggml_new_tensor_1d(ctx, ggml.GGML_TYPE_F32, 1)
b = ggml.ggml_new_tensor_1d(ctx, ggml.GGML_TYPE_F32, 1)

# Use ggml operations to build a computational graph
x2 = ggml.ggml_mul(ctx, x, x)
f = ggml.ggml_add(ctx, ggml.ggml_mul(ctx, a, x2), b)

gf = ggml.ggml_new_graph(ctx)
ggml.ggml_build_forward_expand(gf, f)

# Set the input values
ggml.ggml_set_f32(x, 2.0)
ggml.ggml_set_f32(a, 3.0)
ggml.ggml_set_f32(b, 4.0)

# Compute the graph
ggml.ggml_graph_compute_with_ctx(ctx, gf, 1)

# Get the output value
output = ggml.ggml_get_f32_1d(f, 0)
assert output == 16.0

# Free the context
ggml.ggml_free(ctx)
```

"""
from __future__ import annotations

import os
import sys
import ctypes
import pathlib
import importlib.resources
from typing import (
    List,
    Optional,
    Sequence,
    Union,
    NewType,
    TYPE_CHECKING,
    TypeVar,
    Generic,
)
from typing_extensions import TypeAlias


# Load the library
def load_shared_library(module_name: str, lib_base_name: str):
    # Construct the paths to the possible shared library names
    base_path = pathlib.Path(__file__).parent.resolve()
    # Searching for the library in the current directory under the name "libggml" (default name
    # for ggml) and "ggml" (default name for this repo)
    lib_names: List[str] = [
        f"lib{lib_base_name}.so",
        f"lib{lib_base_name}.dylib",
        f"{lib_base_name}.dll",
    ]

    path: Optional[pathlib.Path] = None

    for lib_name in lib_names:
        try:
            with importlib.resources.path(module_name, lib_name) as p:
                if os.path.exists(p):
                    path = p
                    break
        except FileNotFoundError:
            pass

    if path is None:
        raise FileNotFoundError(
            f"Shared library with base name '{lib_base_name}' not found"
        )

    cdll_args = dict()  # type: ignore
    # Add the library directory to the DLL search path on Windows (if needed)
    if sys.platform == "win32" and sys.version_info >= (3, 8):
        os.add_dll_directory(str(base_path))
        cdll_args["winmode"] = 0

    # Try to load the shared library, handling potential errors
    try:
        return ctypes.CDLL(str(path), **cdll_args)  # type: ignore
    except Exception as e:
        raise RuntimeError(f"Failed to load shared library '{path}': {e}")


module_name = "ggml"
lib_base_name = "ggml"
lib = load_shared_library(module_name, lib_base_name)


#####################################################
# GGML Utility Types
#####################################################


if TYPE_CHECKING:
    CtypesCData = TypeVar("CtypesCData", bound=ctypes._CData)  # type: ignore

    CtypesArray: TypeAlias = ctypes.Array[CtypesCData]  # type: ignore

    CtypesPointer: TypeAlias = ctypes._Pointer[CtypesCData]  # type: ignore

    CtypesVoidPointer: TypeAlias = ctypes.c_void_p

    class CtypesRef(Generic[CtypesCData]):
        pass

    CtypesPointerOrRef: TypeAlias = Union[
        CtypesPointer[CtypesCData], CtypesRef[CtypesCData]
    ]

    CtypesFuncPointer: TypeAlias = ctypes._FuncPointer  # type: ignore


def byref(obj: CtypesCData, offset: Optional[int] = None) -> CtypesRef[CtypesCData]:
    """Type-annotated version of ctypes.byref"""
    return ctypes.byref(obj, offset) if offset is not None else ctypes.byref(obj)  # type: ignore


#####################################################
# GGML API
# source: include/ggml/ggml.h
#####################################################


# define GGML_FILE_MAGIC   0x67676d6c // "ggml"
# define GGML_FILE_VERSION 1
GGML_FILE_MAGIC = 0x67676D6C
GGML_FILE_VERSION = 1

# define GGML_QNT_VERSION        2    // bump this on quantization format changes
# define GGML_QNT_VERSION_FACTOR 1000 // do not change this
GGML_QNT_VERSION = 2
GGML_QNT_VERSION_FACTOR = 1000

# define GGML_MAX_DIMS           4
# define GGML_MAX_PARAMS         2048
# define GGML_MAX_CONTEXTS       64
# define GGML_MAX_SRC            10
# define GGML_MAX_NAME           64
# define GGML_MAX_OP_PARAMS      64
# define GGML_DEFAULT_N_THREADS  4
# define GGML_DEFAULT_GRAPH_SIZE 2048
GGML_MAX_DIMS = 4
GGML_MAX_PARAMS = 2048
GGML_MAX_CONTEXTS = 64
GGML_MAX_SRC = 10
GGML_MAX_NAME = 64
GGML_MAX_OP_PARAMS = 64
GGML_DEFAULT_N_THREADS = 4
GGML_DEFAULT_GRAPH_SIZE = 2048

# #if UINTPTR_MAX == 0XFFFFFFFF
#     #define GGML_MEMALIGN 4
# #else
#     # define GGML_MEMALIGN 16
# #endif
GGML_MEMALIGN = (
    16 if ctypes.sizeof(ctypes.c_void_p) == 4 else 32
)  # FIXME: Check if this is correct

# #define GGML_EXIT_SUCCESS 0
GGML_EXIT_SUCCESS = 0
# #define GGML_EXIT_ABORTED 1
GGML_EXIT_ABORTED = 1

# define GGUF_MAGIC "GGUF"
GGUF_MAGIC = "GGUF"

# define GGUF_VERSION 3
GGUF_VERSION = 3

# #define GGUF_DEFAULT_ALIGNMENT 32
GGUF_DEFAULT_ALIGNMENT = 32

# TODO: Check if this is correct
# typedef uint16_t ggml_fp16_t;
ggml_fp16_t = ctypes.c_uint16


# GGML_API float       ggml_fp16_to_fp32(ggml_fp16_t x);
def ggml_fp16_to_fp32(x: ggml_fp16_t, /) -> float:
    ...


ggml_fp16_to_fp32 = lib.ggml_fp16_to_fp32
ggml_fp16_to_fp32.argtypes = [ggml_fp16_t]
ggml_fp16_to_fp32.restype = ctypes.c_float


# GGML_API ggml_fp16_t ggml_fp32_to_fp16(float x);
def ggml_fp32_to_fp16(x: ctypes.c_float, /) -> int:
    ...


ggml_fp32_to_fp16 = lib.ggml_fp32_to_fp16
ggml_fp32_to_fp16.argtypes = [ctypes.c_float]
ggml_fp32_to_fp16.restype = ggml_fp16_t


# GGML_API void ggml_fp16_to_fp32_row(const ggml_fp16_t * x, float * y, size_t n);
def ggml_fp16_to_fp32_row(
    x: CtypesArray[ggml_fp16_t], y: CtypesArray[ctypes.c_float], n: Union[ctypes.c_int, int], /
) -> None:
    ...


ggml_fp16_to_fp32_row = lib.ggml_fp16_to_fp32_row
ggml_fp16_to_fp32_row.argtypes = [
    ctypes.POINTER(ggml_fp16_t),
    ctypes.POINTER(ctypes.c_float),
    ctypes.c_int,
]
ggml_fp16_to_fp32_row.restype = None


# GGML_API void ggml_fp32_to_fp16_row(const float * x, ggml_fp16_t * y, size_t n);
def ggml_fp32_to_fp16_row(
    x: CtypesArray[ctypes.c_float], y: CtypesArray[ggml_fp16_t], n: Union[ctypes.c_int, int], /
) -> None:
    ...


ggml_fp32_to_fp16_row = lib.ggml_fp32_to_fp16_row
ggml_fp32_to_fp16_row = lib.ggml_fp32_to_fp16_row
ggml_fp32_to_fp16_row.argtypes = [
    ctypes.POINTER(ctypes.c_float),
    ctypes.POINTER(ggml_fp16_t),
    ctypes.c_int,
]
ggml_fp32_to_fp16_row.restype = None


# struct ggml_context;
ggml_context_p = NewType("ggml_context_p", int)
"""Opaque pointer to a ggml_context.

ggml_context structs are not accessed directly instead they must be created using [ggml_init](ggml.ggml_init) and freed using [ggml_free](ggml.ggml_free)."""

ggml_context_p_ctypes = ctypes.c_void_p  # type: ignore

# enum ggml_type {
#     GGML_TYPE_F32  = 0,
#     GGML_TYPE_F16  = 1,
#     GGML_TYPE_Q4_0 = 2,
#     GGML_TYPE_Q4_1 = 3,
#     // GGML_TYPE_Q4_2 = 4, support has been removed
#     // GGML_TYPE_Q4_3 (5) support has been removed
#     GGML_TYPE_Q5_0 = 6,
#     GGML_TYPE_Q5_1 = 7,
#     GGML_TYPE_Q8_0 = 8,
#     GGML_TYPE_Q8_1 = 9,
#     GGML_TYPE_Q2_K = 10,
#     GGML_TYPE_Q3_K = 11,
#     GGML_TYPE_Q4_K = 12,
#     GGML_TYPE_Q5_K = 13,
#     GGML_TYPE_Q6_K = 14,
#     GGML_TYPE_Q8_K = 15,
#     GGML_TYPE_IQ2_XXS = 16,
#     GGML_TYPE_IQ2_XS  = 17,
#     GGML_TYPE_IQ3_XXS = 18,
#     GGML_TYPE_IQ1_S   = 19,
#     GGML_TYPE_IQ4_NL  = 20,
#     GGML_TYPE_I8,
#     GGML_TYPE_I16,
#     GGML_TYPE_I32,
#     GGML_TYPE_COUNT,
# };
GGML_TYPE_F32 = 0
GGML_TYPE_F16 = 1
GGML_TYPE_Q4_0 = 2
GGML_TYPE_Q4_1 = 3
GGML_TYPE_Q5_0 = 6
GGML_TYPE_Q5_1 = 7
GGML_TYPE_Q8_0 = 8
GGML_TYPE_Q8_1 = 9
GGML_TYPE_Q2_K = 10
GGML_TYPE_Q3_K = 11
GGML_TYPE_Q4_K = 12
GGML_TYPE_Q5_K = 13
GGML_TYPE_Q6_K = 14
GGML_TYPE_Q8_K = 15
GGML_TYPE_IQ2_XXS = 16
GGML_TYPE_IQ2_XS = 17
GGML_TYPE_IQ3_XXS = 18
GGML_TYPE_IQ1_S = 19
GGML_TYPE_IQ4_NL = 20
GGML_TYPE_I8 = 21
GGML_TYPE_I16 = 22
GGML_TYPE_I32 = 23
GGML_TYPE_COUNT = 24

# // precision
# enum ggml_prec {
#     GGML_PREC_DEFAULT,
#     GGML_PREC_F32,
# };
GGML_PREC_DEFAULT = 0
GGML_PREC_F32 = 1

# enum ggml_backend_type {
#     GGML_BACKEND_CPU = 0,
#     GGML_BACKEND_GPU = 10,
#     GGML_BACKEND_GPU_SPLIT = 20,
# };
GGML_BACKEND_CPU = 0
GGML_BACKEND_GPU = 10
GGML_BACKEND_GPU_SPLIT = 20


# // model file types
# enum ggml_ftype {
#     GGML_FTYPE_UNKNOWN     = -1,
#     GGML_FTYPE_ALL_F32     = 0,
#     GGML_FTYPE_MOSTLY_F16  = 1,  // except 1d tensors
#     GGML_FTYPE_MOSTLY_Q4_0 = 2,  // except 1d tensors
#     GGML_FTYPE_MOSTLY_Q4_1 = 3,  // except 1d tensors
#     GGML_FTYPE_MOSTLY_Q4_1_SOME_F16 = 4, // tok_embeddings.weight and output.weight are F16
#     GGML_FTYPE_MOSTLY_Q8_0 = 7,  // except 1d tensors
#     GGML_FTYPE_MOSTLY_Q5_0 = 8,  // except 1d tensors
#     GGML_FTYPE_MOSTLY_Q5_1 = 9,  // except 1d tensors
#     GGML_FTYPE_MOSTLY_Q2_K = 10, // except 1d tensors
#     GGML_FTYPE_MOSTLY_Q3_K = 11, // except 1d tensors
#     GGML_FTYPE_MOSTLY_Q4_K = 12, // except 1d tensors
#     GGML_FTYPE_MOSTLY_Q5_K = 13, // except 1d tensors
#     GGML_FTYPE_MOSTLY_Q6_K = 14, // except 1d tensors
#     GGML_FTYPE_MOSTLY_IQ2_XXS = 15, // except 1d tensors
#     GGML_FTYPE_MOSTLY_IQ2_XS  = 16, // except 1d tensors
#     GGML_FTYPE_MOSTLY_IQ3_XXS = 17, // except 1d tensors
#     GGML_FTYPE_MOSTLY_IQ1_S   = 18, // except 1d tensors
#     GGML_FTYPE_MOSTLY_IQ4_NL  = 19, // except 1d tensors
# };
GGML_FTYPE_UNKNOWN = -1
GGML_FTYPE_ALL_F32 = 0
GGML_FTYPE_MOSTLY_F16 = 1
GGML_FTYPE_MOSTLY_Q4_0 = 2
GGML_FTYPE_MOSTLY_Q4_1 = 3
GGML_FTYPE_MOSTLY_Q4_1_SOME_F16 = 4
GGML_FTYPE_MOSTLY_Q8_0 = 7
GGML_FTYPE_MOSTLY_Q5_0 = 8
GGML_FTYPE_MOSTLY_Q5_1 = 9
GGML_FTYPE_MOSTLY_Q2_K = 10
GGML_FTYPE_MOSTLY_Q3_K = 11
GGML_FTYPE_MOSTLY_Q4_K = 12
GGML_FTYPE_MOSTLY_Q5_K = 13
GGML_FTYPE_MOSTLY_Q6_K = 14
GGML_FTYPE_MOSTLY_IQ2_XXS = 15
GGML_FTYPE_MOSTLY_IQ2_XS = 16
GGML_FTYPE_MOSTLY_IQ3_XXS = 17
GGML_FTYPE_MOSTLY_IQ1_S = 18
GGML_FTYPE_MOSTLY_IQ4_NL = 19


# // available tensor operations:
# enum ggml_op {
#     GGML_OP_NONE = 0,

#     GGML_OP_DUP,
#     GGML_OP_ADD,
#     GGML_OP_ADD1,
#     GGML_OP_ACC,
#     GGML_OP_SUB,
#     GGML_OP_MUL,
#     GGML_OP_DIV,
#     GGML_OP_SQR,
#     GGML_OP_SQRT,
#     GGML_OP_LOG,
#     GGML_OP_SUM,
#     GGML_OP_SUM_ROWS,
#     GGML_OP_MEAN,
#     GGML_OP_ARGMAX,
#     GGML_OP_REPEAT,
#     GGML_OP_REPEAT_BACK,
#     GGML_OP_CONCAT,
#     GGML_OP_SILU_BACK,
#     GGML_OP_NORM, // normalize
#     GGML_OP_RMS_NORM,
#     GGML_OP_RMS_NORM_BACK,
#     GGML_OP_GROUP_NORM,

#     GGML_OP_MUL_MAT,
#     GGML_OP_MUL_MAT_ID,
#     GGML_OP_OUT_PROD,

#     GGML_OP_SCALE,
#     GGML_OP_SET,
#     GGML_OP_CPY,
#     GGML_OP_CONT,
#     GGML_OP_RESHAPE,
#     GGML_OP_VIEW,
#     GGML_OP_PERMUTE,
#     GGML_OP_TRANSPOSE,
#     GGML_OP_GET_ROWS,
#     GGML_OP_GET_ROWS_BACK,
#     GGML_OP_DIAG,
#     GGML_OP_DIAG_MASK_INF,
#     GGML_OP_DIAG_MASK_ZERO,
#     GGML_OP_SOFT_MAX,
#     GGML_OP_SOFT_MAX_BACK,
#     GGML_OP_ROPE,
#     GGML_OP_ROPE_BACK,
#     GGML_OP_ALIBI,
#     GGML_OP_CLAMP,
#     GGML_OP_CONV_TRANSPOSE_1D,
#     GGML_OP_IM2COL,
#     GGML_OP_CONV_TRANSPOSE_2D,
#     GGML_OP_POOL_1D,
#     GGML_OP_POOL_2D,
#     GGML_OP_UPSCALE, // nearest interpolate
#     GGML_OP_PAD,
#     GGML_OP_ARGSORT,
#     GGML_OP_LEAKY_RELU,

#     GGML_OP_FLASH_ATTN,
#     GGML_OP_FLASH_FF,
#     GGML_OP_FLASH_ATTN_BACK,
#     GGML_OP_WIN_PART,
#     GGML_OP_WIN_UNPART,
#     GGML_OP_GET_REL_POS,
#     GGML_OP_ADD_REL_POS,

#     GGML_OP_UNARY,

#     GGML_OP_MAP_UNARY,
#     GGML_OP_MAP_BINARY,

#     GGML_OP_MAP_CUSTOM1_F32,
#     GGML_OP_MAP_CUSTOM2_F32,
#     GGML_OP_MAP_CUSTOM3_F32,

#     GGML_OP_MAP_CUSTOM1,
#     GGML_OP_MAP_CUSTOM2,
#     GGML_OP_MAP_CUSTOM3,

#     GGML_OP_CROSS_ENTROPY_LOSS,
#     GGML_OP_CROSS_ENTROPY_LOSS_BACK,

#     GGML_OP_COUNT,
# };
GGML_OP_NONE = 0
GGML_OP_DUP = 1
GGML_OP_ADD = 2
GGML_OP_ADD1 = 3
GGML_OP_ACC = 4
GGML_OP_SUB = 5
GGML_OP_MUL = 6
GGML_OP_DIV = 7
GGML_OP_SQR = 8
GGML_OP_SQRT = 9
GGML_OP_LOG = 10
GGML_OP_SUM = 11
GGML_OP_SUM_ROWS = 12
GGML_OP_MEAN = 13
GGML_OP_ARGMAX = 14
GGML_OP_REPEAT = 15
GGML_OP_REPEAT_BACK = 16
GGML_OP_CONCAT = 17
GGML_OP_SILU_BACK = 18
GGML_OP_NORM = 19
GGML_OP_RMS_NORM = 20
GGML_OP_RMS_NORM_BACK = 21
GGML_OP_GROUP_NORM = 22
GGML_OP_MUL_MAT = 23
GGML_OP_MUL_MAT_ID = 24
GGML_OP_OUT_PROD = 25
GGML_OP_SCALE = 26
GGML_OP_SET = 27
GGML_OP_CPY = 28
GGML_OP_CONT = 29
GGML_OP_RESHAPE = 30
GGML_OP_VIEW = 31
GGML_OP_PERMUTE = 32
GGML_OP_TRANSPOSE = 33
GGML_OP_GET_ROWS = 34
GGML_OP_GET_ROWS_BACK = 35
GGML_OP_DIAG = 36
GGML_OP_DIAG_MASK_INF = 37
GGML_OP_DIAG_MASK_ZERO = 38
GGML_OP_SOFT_MAX = 39
GGML_OP_SOFT_MAX_BACK = 40
GGML_OP_ROPE = 41
GGML_OP_ROPE_BACK = 42
GGML_OP_ALIBI = 43
GGML_OP_CLAMP = 44
GGML_OP_CONV_TRANSPOSE_1D = 45
GGML_OP_IM2COL = 46
GGML_OP_CONV_TRANSPOSE_2D = 47
GGML_OP_POOL_1D = 48
GGML_OP_POOL_2D = 49
GGML_OP_UPSCALE = 50
GGML_OP_PAD = 51
GGML_OP_ARGSORT = 52
GGML_OP_LEAKY_RELU = 53
GGML_OP_FLASH_ATTN = 54
GGML_OP_FLASH_FF = 55
GGML_OP_FLASH_ATTN_BACK = 56
GGML_OP_WIN_PART = 57
GGML_OP_WIN_UNPART = 58
GGML_OP_GET_REL_POS = 59
GGML_OP_ADD_REL_POS = 60
GGML_OP_UNARY = 61
GGML_OP_MAP_UNARY = 62
GGML_OP_MAP_BINARY = 63
GGML_OP_MAP_CUSTOM1_F32 = 64
GGML_OP_MAP_CUSTOM2_F32 = 65
GGML_OP_MAP_CUSTOM3_F32 = 66
GGML_OP_MAP_CUSTOM1 = 67
GGML_OP_MAP_CUSTOM2 = 68
GGML_OP_MAP_CUSTOM3 = 69
GGML_OP_CROSS_ENTROPY_LOSS = 70
GGML_OP_CROSS_ENTROPY_LOSS_BACK = 71
GGML_OP_COUNT = 72

# enum ggml_unary_op {
#     GGML_UNARY_OP_ABS,
#     GGML_UNARY_OP_SGN,
#     GGML_UNARY_OP_NEG,
#     GGML_UNARY_OP_STEP,
#     GGML_UNARY_OP_TANH,
#     GGML_UNARY_OP_ELU,
#     GGML_UNARY_OP_RELU,
#     GGML_UNARY_OP_GELU,
#     GGML_UNARY_OP_GELU_QUICK,
#     GGML_UNARY_OP_SILU,
#     GGML_UNARY_OP_HARDSWISH,
#     GGML_UNARY_OP_HARDSIGMOID,

#     GGML_UNARY_OP_COUNT,
# };
GGML_UNARY_OP_ABS = 0
GGML_UNARY_OP_SGN = 1
GGML_UNARY_OP_NEG = 2
GGML_UNARY_OP_STEP = 3
GGML_UNARY_OP_TANH = 4
GGML_UNARY_OP_ELU = 5
GGML_UNARY_OP_RELU = 6
GGML_UNARY_OP_GELU = 7
GGML_UNARY_OP_GELU_QUICK = 8
GGML_UNARY_OP_SILU = 9
GGML_UNARY_OP_HARDSWISH = 10
GGML_UNARY_OP_HARDSIGMOID = 11
GGML_UNARY_OP_COUNT = 12

# enum ggml_object_type {
#     GGML_OBJECT_TENSOR,
#     GGML_OBJECT_GRAPH,
#     GGML_OBJECT_WORK_BUFFER
# };
GGML_OBJECT_TENSOR = 0
GGML_OBJECT_GRAPH = 1
GGML_OBJECT_WORK_BUFFER = 2

# enum ggml_log_level {
#     GGML_LOG_LEVEL_ERROR = 2,
#     GGML_LOG_LEVEL_WARN  = 3,
#     GGML_LOG_LEVEL_INFO  = 4,
#     GGML_LOG_LEVEL_DEBUG = 5
# };
GGML_LOG_LEVEL_ERROR = 2
GGML_LOG_LEVEL_WARN = 3
GGML_LOG_LEVEL_INFO = 4
GGML_LOG_LEVEL_DEBUG = 5


# enum ggml_tensor_flag {
#     GGML_TENSOR_FLAG_INPUT  = 1,
#     GGML_TENSOR_FLAG_OUTPUT = 2,
#     GGML_TENSOR_FLAG_PARAM  = 4,
# };
GGML_TENSOR_FLAG_INPUT = 1
GGML_TENSOR_FLAG_OUTPUT = 2
GGML_TENSOR_FLAG_PARAM = 4


# // ggml object
# struct ggml_object {
#     size_t offs;
#     size_t size;

#     struct ggml_object * next;

#     enum ggml_object_type type;


#     char padding[4];
# };
class ggml_object(ctypes.Structure):
    pass


ggml_object._fields_ = [
    ("offs", ctypes.c_size_t),
    ("size", ctypes.c_size_t),
    ("next", ctypes.POINTER(ggml_object)),
    ("type", ctypes.c_int),
    ("padding", ctypes.c_char * 4),
]

ggml_object_p: TypeAlias = "ctypes._Pointer[ggml_object]"  # type: ignore

GGML_OBJECT_SIZE = ctypes.sizeof(ggml_object)


# // n-dimensional tensor
# struct ggml_tensor {
#     enum ggml_type         type;
#     enum ggml_backend_type backend;

#     struct ggml_backend_buffer * buffer;

#     int64_t ne[GGML_MAX_DIMS]; // number of elements
#     size_t  nb[GGML_MAX_DIMS]; // stride in bytes:
#                                // nb[0] = ggml_type_size(type)
#                                // nb[1] = nb[0]   * (ne[0] / ggml_blck_size(type)) + padding
#                                // nb[i] = nb[i-1] * ne[i-1]

#     // compute data
#     enum ggml_op op;

#     // op params - allocated as int32_t for alignment
#     int32_t op_params[GGML_MAX_OP_PARAMS / sizeof(int32_t)];

#     int32_t flags;

#     struct ggml_tensor * grad;
#     struct ggml_tensor * src[GGML_MAX_SRC];

#     // performance
#     int     perf_runs;
#     int64_t perf_cycles;
#     int64_t perf_time_us;

#     struct ggml_tensor * view_src;
#     size_t               view_offs;

#     void * data;

#     char name[GGML_MAX_NAME];

#     void * extra; // extra things e.g. for ggml-cuda.cu


#     char padding[8];
# };
class ggml_tensor(ctypes.Structure):
    """n-dimensional tensor

    Attributes:
        type (int): ggml_type
        backend (int): ggml_backend
        buffer (ctypes.pointer[ggml_backend_buffer]): pointer to backend buffer
        ne (ctypes.Array[ctypes.c_int64]): number of elements in each dimension
        nb (ctypes.Array[ctypes.c_size_t]): stride in bytes for each dimension
        op (int): ggml operation
        op_params (ctypes.Array[ctypes.c_int32]): `GGML_MAX_OP_PARAMS`-length array of operation parameters
        flags (int): tensor flags
        grad (ggml_tensor_p): reference to gradient tensor
        src (ctypes.Array[ggml_tensor_p]): `GGML_MAX_SRC`-length array of source tensors
        perf_runs (int): number of performance runs
        perf_cycles (int): number of cycles
        perf_time_us (int): time in microseconds
        view_src (ggml_tensor_p): pointer to tensor if this tensor is a view, None if the tensor is not a view
        view_offs (ctypes.c_size_t): offset into the data pointer of the view tensor
        data (ctypes.c_void_p): reference to raw tensor data
        name (bytes): name of tensor
        extra (ctypes.c_void_p): extra data (e.g. for CUDA)
    """

    pass


ggml_tensor._fields_ = [
    ("type", ctypes.c_int),
    ("backend", ctypes.c_int),
    ("buffer", ctypes.c_void_p),
    ("ne", ctypes.c_int64 * GGML_MAX_DIMS),
    ("nb", ctypes.c_size_t * GGML_MAX_DIMS),
    ("op", ctypes.c_int),
    (
        "op_params",
        ctypes.c_int32 * (GGML_MAX_OP_PARAMS // ctypes.sizeof(ctypes.c_int32)),
    ),
    ("flags", ctypes.c_int),
    ("grad", ctypes.POINTER(ggml_tensor)),
    ("src", ctypes.POINTER(ggml_tensor) * GGML_MAX_SRC),
    ("perf_runs", ctypes.c_int),
    ("perf_cycles", ctypes.c_int64),
    ("perf_time_us", ctypes.c_int64),
    ("view_src", ctypes.POINTER(ggml_tensor)),
    ("view_offs", ctypes.c_size_t),
    ("data", ctypes.c_void_p),
    ("name", ctypes.c_char * GGML_MAX_NAME),
    ("extra", ctypes.c_void_p),
    ("padding", ctypes.c_char * 8),
]

GGML_TENSOR_SIZE = ctypes.sizeof(ggml_tensor)

ggml_tensor_p: TypeAlias = "ctypes._Pointer[ggml_tensor]"  # type: ignore
"""ctypes pointer to a [ggml_tensor][ggml.ggml_tensor]

Can be dereferenced to a [ggml_tensor][ggml.ggml_tensor] object using
the `.contents` attribute."""


# // Abort callback
# // If not NULL, called before ggml computation
# // If it returns true, the computation is aborted
# typedef bool (*ggml_abort_callback)(void * data);
ggml_abort_callback = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_void_p)


# // the compute plan that needs to be prepared for ggml_graph_compute()
# // since https://github.com/ggerganov/ggml/issues/287
# struct ggml_cplan {
#     size_t    work_size; // size of work buffer, calculated by `ggml_graph_plan()`
#     uint8_t * work_data; // work buffer, to be allocated by caller before calling to `ggml_graph_compute()`

#     int n_threads;


#     // abort ggml_graph_compute when true
#     ggml_abort_callback abort_callback;
#     void *              abort_callback_data;
# };
class ggml_cplan(ctypes.Structure):
    """Compute plan for a ggml computation graph

    Attributes:
        work_size (int): size of work buffer
        work_data (ctypes.pointer[ctypes.c_uint8]): work buffer
        n_threads (int): number of threads
        abort_callback (ggml_abort_callback): abort callback
        abort_callback_data (ctypes.c_void_p): abort callback data
    """

    _fields_ = [
        ("work_size", ctypes.c_size_t),
        ("work_data", ctypes.POINTER(ctypes.c_uint8)),
        ("n_threads", ctypes.c_int),
        (
            "abort_callback",
            ggml_abort_callback,
        ),
        ("abort_callback_data", ctypes.c_void_p),
    ]


GGML_CPLAN_SIZE = ctypes.sizeof(ggml_cplan)

ggml_cplan_p: TypeAlias = "ctypes._Pointer[ggml_cplan]"  # type: ignore
"""ctypes pointer to a [ggml_cplan][ggml.ggml_cplan]

Can be dereferenced to a [ggml_cplan][ggml.ggml_cplan] object using
the `.contents` attribute."""

# enum ggml_cgraph_eval_order {
#     GGML_CGRAPH_EVAL_ORDER_LEFT_TO_RIGHT = 0,
#     GGML_CGRAPH_EVAL_ORDER_RIGHT_TO_LEFT,
#     GGML_CGRAPH_EVAL_ORDER_COUNT
# };
GGML_CGRAPH_EVAL_ORDER_LEFT_TO_RIGHT = 0
GGML_CGRAPH_EVAL_ORDER_RIGHT_TO_LEFT = 1
GGML_CGRAPH_EVAL_ORDER_COUNT = 2


# struct ggml_hash_set {
#     size_t size;
#     struct ggml_tensor ** keys;
# };
class ggml_hash_set(ctypes.Structure):
    _fields_ = [
        ("size", ctypes.c_size_t),
        ("keys", ctypes.POINTER(ctypes.POINTER(ggml_tensor))),
    ]


# // computation graph
# struct ggml_cgraph {
#     int size;
#     int n_nodes;
#     int n_leafs;

#     struct ggml_tensor ** nodes;
#     struct ggml_tensor ** grads;
#     struct ggml_tensor ** leafs;

#     struct ggml_hash_set visited_hash_table;

#     enum ggml_cgraph_eval_order order;


#     // performance
#     int     perf_runs;
#     int64_t perf_cycles;
#     int64_t perf_time_us;
# };
class ggml_cgraph(ctypes.Structure):
    """ggml computation graph

    Attributes:
        n_nodes (int): number of nodes
        n_leafs (int): number of leafs
        nodes (ctypes.Array[ggml_tensor_p]): `n_nodes`-length array of compute tensors
        grads (ctypes.Array[ggml_tensor_p]): `n_nodes`-length array of gradient tensors
        leafs (ctypes.Array[ggml_tensor_p]): `n_leafs`-length array of parameter tensors
        visited_hash_table (ctypes.Array[ctypes.POINTER(ggml_tensor)]): hash table of visited tensors
        order (int): evaluation order
        perf_runs (int): number of runs
        perf_cycles (int): number of cycles
        perf_time_us (int): computation time in microseconds"""

    _fields_ = [
        ("size", ctypes.c_int),
        ("n_nodes", ctypes.c_int),
        ("n_leafs", ctypes.c_int),
        ("nodes", ctypes.POINTER(ctypes.POINTER(ggml_tensor))),
        ("grads", ctypes.POINTER(ctypes.POINTER(ggml_tensor))),
        ("leafs", ctypes.POINTER(ctypes.POINTER(ggml_tensor))),
        ("visited_hash_table", ggml_hash_set),
        ("order", ctypes.c_int),
        ("perf_runs", ctypes.c_int),
        ("perf_cycles", ctypes.c_int64),
        ("perf_time_us", ctypes.c_int64),
    ]


ggml_cgraph_p: TypeAlias = "ctypes._Pointer[ggml_cgraph]"  # type: ignore
"""ctypes pointer to a [ggml_cgraph][ggml.ggml_cgraph]

Can be dereferenced to a [ggml_cgraph][ggml.ggml_cgraph] object using
the `.contents` attribute."""


# struct ggml_scratch {
#     size_t offs;
#     size_t size;
#     void * data;
# };
class ggml_scratch(ctypes.Structure):
    _fields_ = [
        ("offs", ctypes.c_size_t),
        ("size", ctypes.c_size_t),
        ("data", ctypes.c_void_p),
    ]


# struct ggml_init_params {
#     // memory pool
#     size_t mem_size;   // bytes
#     void * mem_buffer; // if NULL, memory will be allocated internally
#     bool   no_alloc;   // don't allocate memory for the tensor data
# };
class ggml_init_params(ctypes.Structure):
    """Initialization parameters for a ggml context

    **NOTE**: Reference counting does not cross into ggml, if you allocate a memory buffer
    in python using ctypes Arrays or a numpy array, you must keep a reference to it until
    you free the ggml context otherwise you will encounter a segmentation fault.

    Attributes:
        mem_size (int): size of memory pool in bytes
        mem_buffer (ctypes.c_void_p): pointer to memory pool, if None, memory will be allocated internally
        no_alloc (bool): don't allocate memory for tensor data
    """

    _fields_ = [
        ("mem_size", ctypes.c_size_t),
        ("mem_buffer", ctypes.c_void_p),
        ("no_alloc", ctypes.c_bool),
    ]


# // compute types

# // NOTE: the INIT or FINALIZE pass is not scheduled unless explicitly enabled.
# // This behavior was changed since https://github.com/ggerganov/llama.cpp/pull/1995.
# enum ggml_task_type {
#     GGML_TASK_INIT = 0,
#     GGML_TASK_COMPUTE,
#     GGML_TASK_FINALIZE,
# };
GGML_TASK_INIT = 0
GGML_TASK_COMPUTE = 1
GGML_TASK_FINALIZE = 2

# struct ggml_compute_params {
#     enum ggml_task_type type;

#     // ith = thread index, nth = number of threads
#     int ith, nth;


#     // work buffer for all threads
#     size_t wsize;
#     void * wdata;
# };
class ggml_compute_params(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_int),
        ("ith", ctypes.c_int),
        ("nth", ctypes.c_int),
        ("wsize", ctypes.c_size_t),
        ("wdata", ctypes.c_void_p),
    ]


ggml_compute_params_p: TypeAlias = "ctypes._Pointer[ggml_compute_params]"  # type: ignore


# // numa strategies
# enum ggml_numa_strategy {
#     GGML_NUMA_STRATEGY_DISABLED   = 0,
#     GGML_NUMA_STRATEGY_DISTRIBUTE = 1,
#     GGML_NUMA_STRATEGY_ISOLATE    = 2,
#     GGML_NUMA_STRATEGY_NUMACTL    = 3,
#     GGML_NUMA_STRATEGY_MIRROR     = 4,
#     GGML_NUMA_STRATEGY_COUNT
# };
GGML_NUMA_STRATEGY_DISABLED = 0
GGML_NUMA_STRATEGY_DISTRIBUTE = 1
GGML_NUMA_STRATEGY_ISOLATE = 2
GGML_NUMA_STRATEGY_NUMACTL = 3
GGML_NUMA_STRATEGY_MIRROR = 4
GGML_NUMA_STRATEGY_COUNT = 5


# // misc


# GGML_API void    ggml_time_init(void); // call this once at the beginning of the program
def ggml_time_init():
    ...


ggml_time_init = lib.ggml_time_init
ggml_time_init.argtypes = []
ggml_time_init.restype = None


# GGML_API int64_t ggml_time_ms(void);
def ggml_time_ms() -> int:
    ...


ggml_time_ms = lib.ggml_time_ms
ggml_time_ms.argtypes = []
ggml_time_ms.restype = ctypes.c_int64


# GGML_API int64_t ggml_time_us(void);
def ggml_time_us() -> int:
    ...


ggml_time_us = lib.ggml_time_us
ggml_time_us.argtypes = []
ggml_time_us.restype = ctypes.c_int64


# GGML_API int64_t ggml_cycles(void);
def ggml_cycles() -> int:
    ...


ggml_cycles = lib.ggml_cycles
ggml_cycles.argtypes = []
ggml_cycles.restype = ctypes.c_int64


# GGML_API int64_t ggml_cycles_per_ms(void);
def ggml_cycles_per_ms() -> int:
    ...


ggml_cycles_per_ms = lib.ggml_cycles_per_ms
ggml_cycles_per_ms.argtypes = []
ggml_cycles_per_ms.restype = ctypes.c_int64


# GGML_API void    ggml_print_backtrace(void);
def ggml_print_backtrace():
    ...


ggml_print_backtrace = lib.ggml_print_backtrace
ggml_print_backtrace.argtypes = []
ggml_print_backtrace.restype = None


# GGML_API void    ggml_numa_init(enum ggml_numa_strategy numa); // call once for better performance on NUMA systems
def ggml_numa_init(numa: Union[ctypes.c_int, int], /):
    ...


ggml_numa_init = lib.ggml_numa_init
ggml_numa_init.argtypes = [ctypes.c_int]
ggml_numa_init.restype = None


# GGML_API bool    ggml_is_numa(void); // true if init detected that system has >1 NUMA node
def ggml_is_numa() -> bool:
    ...


ggml_is_numa = lib.ggml_is_numa
ggml_is_numa.argtypes = []
ggml_is_numa.restype = ctypes.c_bool


# GGML_API void    ggml_print_object (const struct ggml_object * obj);
def ggml_print_object(obj: ggml_object_p, /):
    ...


ggml_print_object = lib.ggml_print_object
ggml_print_object.argtypes = [ctypes.POINTER(ggml_object)]
ggml_print_object.restype = None


# GGML_API void    ggml_print_objects(const struct ggml_context * ctx);
def ggml_print_objects(ctx: ggml_context_p, /):
    ...


ggml_print_objects = lib.ggml_print_objects
ggml_print_objects.argtypes = [ggml_context_p_ctypes]
ggml_print_objects.restype = None


# GGML_API GGML_CALL int64_t ggml_nelements   (const struct ggml_tensor * tensor);
def ggml_nelements(tensor: ggml_tensor_p, /) -> int:
    """Get the number of elements in a tensor

    Parameters:
        tensor: tensor

    Returns:
        number of elements"""
    ...


ggml_nelements = lib.ggml_nelements
ggml_nelements.argtypes = [ctypes.POINTER(ggml_tensor)]
ggml_nelements.restype = ctypes.c_int64


# GGML_API GGML_CALL int64_t ggml_nrows       (const struct ggml_tensor * tensor);
def ggml_nrows(tensor: ggml_tensor_p, /) -> int:
    """Get the number of rows in a tensor

    Parameters:
        tensor: tensor

    Returns:
        number of rows"""
    ...


ggml_nrows = lib.ggml_nrows
ggml_nrows.argtypes = [ctypes.POINTER(ggml_tensor)]
ggml_nrows.restype = ctypes.c_int64


# GGML_API GGML_CALL size_t  ggml_nbytes      (const struct ggml_tensor * tensor);
def ggml_nbytes(tensor: ggml_tensor_p, /) -> int:
    """Get the number of bytes required to store tensor data

    Parameters:
        tensor: tensor

    Returns:
        number of bytes"""
    ...


ggml_nbytes = lib.ggml_nbytes
ggml_nbytes.argtypes = [ctypes.POINTER(ggml_tensor)]
ggml_nbytes.restype = ctypes.c_size_t


# GGML_API           size_t  ggml_nbytes_pad  (const struct ggml_tensor * tensor); // same as ggml_nbytes() but padded to GGML_MEM_ALIGN
def ggml_nbytes_pad(tensor: ggml_tensor_p, /) -> int:
    """Get the number of bytes required to store tensor data, padded to GGML_MEM_ALIGN

    Parameters:
        tensor: tensor

    Returns:
        number of bytes"""
    ...


ggml_nbytes_pad = lib.ggml_nbytes_pad
ggml_nbytes_pad.argtypes = [ctypes.POINTER(ggml_tensor)]
ggml_nbytes_pad.restype = ctypes.c_size_t


# GGML_API GGML_CALL int    ggml_blck_size(enum ggml_type type);
def ggml_blck_size(type: Union[ctypes.c_int, int], /) -> int:
    ...


ggml_blck_size = lib.ggml_blck_size
ggml_blck_size.argtypes = [ctypes.c_int]
ggml_blck_size.restype = ctypes.c_int


# GGML_API GGML_CALL size_t ggml_type_size(enum ggml_type type);             // size in bytes for all elements in a block
def ggml_type_size(type: Union[ctypes.c_int, int], /) -> int:
    ...


ggml_type_size = lib.ggml_type_size
ggml_type_size.argtypes = [ctypes.c_int]
ggml_type_size.restype = ctypes.c_size_t


# GGML_API GGML_CALL size_t ggml_row_size (enum ggml_type type, int64_t ne); // size in bytes for all elements in a row
def ggml_row_size(type: Union[ctypes.c_int, int], ne: int, /) -> int:
    ...


ggml_row_size = lib.ggml_row_size
ggml_row_size.argtypes = [ctypes.c_int, ctypes.c_int64]
ggml_row_size.restype = ctypes.c_size_t


# GGML_DEPRECATED(
# GGML_API double ggml_type_sizef(enum ggml_type type), // ggml_type_size()/ggml_blck_size() as float
# "use ggml_row_size() instead");
def ggml_type_sizef(type: Union[ctypes.c_int, int], /) -> float:
    ...


ggml_type_sizef = lib.ggml_type_sizef
ggml_type_sizef.argtypes = [ctypes.c_int]
ggml_type_sizef.restype = ctypes.c_double


# GGML_API GGML_CALL const char * ggml_type_name(enum ggml_type type);
def ggml_type_name(type: Union[ctypes.c_int, int], /) -> bytes:
    ...


ggml_type_name = lib.ggml_type_name
ggml_type_name.argtypes = [ctypes.c_int]
ggml_type_name.restype = ctypes.c_char_p


# GGML_API GGML_CALL const char * ggml_op_name  (enum ggml_op   op);
def ggml_op_name(op: Union[ctypes.c_int, int], /) -> bytes:
    ...


ggml_op_name = lib.ggml_op_name
ggml_op_name.argtypes = [ctypes.c_int]
ggml_op_name.restype = ctypes.c_char_p


# GGML_API           const char * ggml_op_symbol(enum ggml_op   op);
def ggml_op_symbol(op: Union[ctypes.c_int, int], /) -> bytes:
    ...


ggml_op_symbol = lib.ggml_op_symbol
ggml_op_symbol.argtypes = [ctypes.c_int]
ggml_op_symbol.restype = ctypes.c_char_p


# GGML_API           const char * ggml_unary_op_name(enum ggml_unary_op op);
def ggml_unary_op_name(op: Union[ctypes.c_int, int], /) -> bytes:
    ...


ggml_unary_op_name = lib.ggml_unary_op_name
ggml_unary_op_name.argtypes = [ctypes.c_int]
ggml_unary_op_name.restype = ctypes.c_char_p


# GGML_API GGML_CALL const char * ggml_op_desc(const struct ggml_tensor * t); // unary or op name
def ggml_op_desc(t: ggml_tensor_p, /) -> bytes:
    ...


ggml_op_desc = lib.ggml_op_desc
ggml_op_desc.argtypes = [ctypes.POINTER(ggml_tensor)]
ggml_op_desc.restype = ctypes.c_char_p


# GGML_API GGML_CALL size_t  ggml_element_size(const struct ggml_tensor * tensor);
def ggml_element_size(tensor: ggml_tensor_p, /) -> int:
    ...


ggml_element_size = lib.ggml_element_size
ggml_element_size.argtypes = [ctypes.POINTER(ggml_tensor)]
ggml_element_size.restype = ctypes.c_size_t


# GGML_API GGML_CALL bool    ggml_is_quantized(enum ggml_type type);
def ggml_is_quantized(type: Union[ctypes.c_int, int], /) -> bool:
    ...


ggml_is_quantized = lib.ggml_is_quantized
ggml_is_quantized.argtypes = [ctypes.c_int]
ggml_is_quantized.restype = ctypes.c_bool


# // TODO: temporary until model loading of ggml examples is refactored
# GGML_API enum ggml_type ggml_ftype_to_ggml_type(enum ggml_ftype ftype);
def ggml_ftype_to_ggml_type(ftype: Union[ctypes.c_int, int], /) -> int:
    ...


ggml_ftype_to_ggml_type = lib.ggml_ftype_to_ggml_type
ggml_ftype_to_ggml_type.argtypes = [ctypes.c_int]
ggml_ftype_to_ggml_type.restype = ctypes.c_int


# GGML_API GGML_CALL bool ggml_is_transposed(const struct ggml_tensor * tensor);
def ggml_is_transposed(tensor: ggml_tensor_p, /) -> bool:
    """Check if a tensor is transposed

    Parameters:
        tensor: tensor

    Returns:
        True if tensor is transposed else False"""
    ...


ggml_is_transposed = lib.ggml_is_transposed
ggml_is_transposed.argtypes = [ctypes.POINTER(ggml_tensor)]
ggml_is_transposed.restype = ctypes.c_bool


# GGML_API GGML_CALL bool ggml_is_contiguous(const struct ggml_tensor * tensor);
def ggml_is_contiguous(tensor: ggml_tensor_p, /) -> bool:
    """Check if a tensor is contiguous

    Parameters:
        tensor: tensor

    Returns:
        True if tensor is contiguous else False"""
    ...


ggml_is_contiguous = lib.ggml_is_contiguous
ggml_is_contiguous.argtypes = [ctypes.POINTER(ggml_tensor)]
ggml_is_contiguous.restype = ctypes.c_bool


# GGML_API GGML_CALL bool ggml_is_permuted  (const struct ggml_tensor * tensor);
def ggml_is_permuted(tensor: ggml_tensor_p, /) -> bool:
    """Check if a tensor is permuted

    Parameters:
        tensor: tensor

    Returns:
        True if tensor is permuted else False"""
    ...


ggml_is_permuted = lib.ggml_is_permuted
ggml_is_permuted.argtypes = [ctypes.POINTER(ggml_tensor)]
ggml_is_permuted.restype = ctypes.c_bool


# GGML_API           bool ggml_is_scalar    (const struct ggml_tensor * tensor);
def ggml_is_scalar(tensor: ggml_tensor_p, /) -> bool:
    """Check if a tensor is a scalar"""
    ...


ggml_is_scalar = lib.ggml_is_scalar
ggml_is_scalar.argtypes = [ctypes.POINTER(ggml_tensor)]
ggml_is_scalar.restype = ctypes.c_bool


# GGML_API           bool ggml_is_vector    (const struct ggml_tensor * tensor);
def ggml_is_vector(tensor: ggml_tensor_p, /) -> bool:
    """Check if a tensor is a vector"""
    ...


ggml_is_vector = lib.ggml_is_vector
ggml_is_vector.argtypes = [ctypes.POINTER(ggml_tensor)]
ggml_is_vector.restype = ctypes.c_bool


# GGML_API           bool ggml_is_matrix    (const struct ggml_tensor * tensor);
def ggml_is_matrix(tensor: ggml_tensor_p, /) -> bool:
    """Check if a tensor is a matrix"""
    ...


ggml_is_matrix = lib.ggml_is_matrix
ggml_is_matrix.argtypes = [ctypes.POINTER(ggml_tensor)]
ggml_is_matrix.restype = ctypes.c_bool


# GGML_API           bool ggml_is_3d        (const struct ggml_tensor * tensor);
def ggml_is_3d(tensor: ggml_tensor_p, /) -> bool:
    """Check if a tensor is 3d"""
    ...


ggml_is_3d = lib.ggml_is_3d
ggml_is_3d.argtypes = [ctypes.POINTER(ggml_tensor)]
ggml_is_3d.restype = ctypes.c_bool


# GGML_API           int  ggml_n_dims       (const struct ggml_tensor * tensor); // returns 1 for scalars
def ggml_n_dims(tensor: ggml_tensor_p, /) -> int:
    """Get the number of dimensions in a tensor"""
    ...


ggml_n_dims = lib.ggml_n_dims
ggml_n_dims.argtypes = [ctypes.POINTER(ggml_tensor)]
ggml_n_dims.restype = ctypes.c_int


# GGML_API bool ggml_are_same_shape(const struct ggml_tensor * t0, const struct ggml_tensor * t1);
def ggml_are_same_shape(t0: ggml_tensor_p, t1: ggml_tensor_p, /) -> bool:
    """Check if two tensors have the same shape

    Parameters:
        t0: tensor 0
        t1: tensor 1

    Returns:
        True if tensors have the same shape else False"""
    ...


ggml_are_same_shape = lib.ggml_are_same_shape
ggml_are_same_shape.argtypes = [
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
]
ggml_are_same_shape.restype = ctypes.c_bool


# // use this to compute the memory overhead of a tensor
# GGML_API size_t ggml_tensor_overhead(void);
def ggml_tensor_overhead() -> int:
    """Overhead required for a tensor struct in bytes

    Returns:
        size of tensor struct in bytes"""
    ...


ggml_tensor_overhead = lib.ggml_tensor_overhead
ggml_tensor_overhead.argtypes = []
ggml_tensor_overhead.restype = ctypes.c_size_t

# // main


# GGML_API struct ggml_context * ggml_init(struct ggml_init_params params);
def ggml_init(params: ggml_init_params, /) -> Optional[ggml_context_p]:
    """Instantiate a new ggml context with params.

    You must call `ggml_free()` to free the context.

    Parameters:
        params: ggml init params

    Returns:
        Pointer to ggml_context or None if failed to initialize context."""
    ...


ggml_init = lib.ggml_init
ggml_init.argtypes = [ggml_init_params]
ggml_init.restype = ggml_context_p_ctypes


# GGML_API void                  ggml_free(struct ggml_context * ctx);
def ggml_free(ctx: ggml_context_p, /):
    """Free the ggml context.

    Parameters:
        ctx: ggml context"""
    ...


ggml_free = lib.ggml_free
ggml_free.argtypes = [ggml_context_p_ctypes]
ggml_free.restype = None


# GGML_API size_t  ggml_used_mem(const struct ggml_context * ctx);
def ggml_used_mem(ctx: ggml_context_p, /) -> int:
    """Return the amount of memory used by the ggml context in bytes.

    Parameters:
        ctx: ggml context

    Returns:
        amount of memory used in bytes"""
    ...


ggml_used_mem = lib.ggml_used_mem
ggml_used_mem.argtypes = [ggml_context_p_ctypes]
ggml_used_mem.restype = ctypes.c_size_t


# GGML_API size_t  ggml_set_scratch(struct ggml_context * ctx, struct ggml_scratch scratch);
def ggml_set_scratch(ctx: ggml_context_p, scratch: ggml_scratch, /) -> int:
    """Set the scratch buffer for the ggml context."""
    ...


ggml_set_scratch = lib.ggml_set_scratch
ggml_set_scratch.argtypes = [ggml_context_p_ctypes, ggml_scratch]
ggml_set_scratch.restype = ctypes.c_size_t


# GGML_API bool    ggml_get_no_alloc(struct ggml_context * ctx);
def ggml_get_no_alloc(ctx: ggml_context_p, /) -> bool:
    """Return the no_alloc flag for the ggml context."""
    ...


ggml_get_no_alloc = lib.ggml_get_no_alloc
ggml_get_no_alloc.argtypes = [ggml_context_p_ctypes]
ggml_get_no_alloc.restype = ctypes.c_bool


# GGML_API void    ggml_set_no_alloc(struct ggml_context * ctx, bool no_alloc);
def ggml_set_no_alloc(ctx: ggml_context_p, no_alloc: Union[ctypes.c_bool, bool], /):
    """Set the no_alloc flag for the ggml context."""
    ...


ggml_set_no_alloc = lib.ggml_set_no_alloc
ggml_set_no_alloc.argtypes = [ggml_context_p_ctypes, ctypes.c_bool]
ggml_set_no_alloc.restype = None


# GGML_API void *  ggml_get_mem_buffer     (struct ggml_context * ctx);
def ggml_get_mem_buffer(ctx: ggml_context_p, /) -> Optional[int]:
    """Return the memory buffer for the ggml context."""
    ...


ggml_get_mem_buffer = lib.ggml_get_mem_buffer
ggml_get_mem_buffer.argtypes = [ggml_context_p_ctypes]
ggml_get_mem_buffer.restype = ctypes.c_void_p


# GGML_API size_t  ggml_get_mem_size       (struct ggml_context * ctx);
def ggml_get_mem_size(ctx: ggml_context_p, /) -> int:
    """Return the size of the memory buffer for the ggml context in bytes."""
    ...


ggml_get_mem_size = lib.ggml_get_mem_size
ggml_get_mem_size.argtypes = [ggml_context_p_ctypes]
ggml_get_mem_size.restype = ctypes.c_size_t


# GGML_API size_t  ggml_get_max_tensor_size(const struct ggml_context * ctx);
def ggml_get_max_tensor_size(ctx: ggml_context_p, /) -> int:
    """Return the maximum size of a tensor in bytes."""
    ...


ggml_get_max_tensor_size = lib.ggml_get_max_tensor_size
ggml_get_max_tensor_size.argtypes = [ggml_context_p_ctypes]
ggml_get_max_tensor_size.restype = ctypes.c_size_t


# GGML_API struct ggml_tensor * ggml_new_tensor(
#         struct ggml_context * ctx,
#         enum   ggml_type type,
#         int    n_dims,
#         const int64_t *ne);
def ggml_new_tensor(
    ctx: ggml_context_p,
    type: Union[ctypes.c_int, int],
    n_dims: Union[ctypes.c_int, int],
    ne: CtypesArray[ctypes.c_int64],
    /,
) -> ggml_tensor_p:
    """Create a new tensor with the given type, number of dimensions, and number of elements in each dimension.

    Parameters:
        ctx: ggml context
        type: ggml type
        n_dims: number of dimensions
        ne (ctypes.Array[ctypes.c_int64]): number of elements in each dimension (array of length n_dims)

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_new_tensor = lib.ggml_new_tensor
ggml_new_tensor.argtypes = [
    ggml_context_p_ctypes,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_int64),
]
ggml_new_tensor.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_new_tensor_1d(
#         struct ggml_context * ctx,
#         enum   ggml_type type,
#         int64_t ne0);
def ggml_new_tensor_1d(
    ctx: ggml_context_p,
    type: Union[ctypes.c_int, int],
    ne0: Union[ctypes.c_int64, int],
    /,
) -> ggml_tensor_p:
    """Create a new 1-dimensional tensor with the given type and number of elements.

    Parameters:
        ctx: ggml context
        type: ggml type
        ne0: number of elements in dimension 0

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_new_tensor_1d = lib.ggml_new_tensor_1d
ggml_new_tensor_1d.argtypes = [ggml_context_p_ctypes, ctypes.c_int, ctypes.c_int64]
ggml_new_tensor_1d.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_new_tensor_2d(
#         struct ggml_context * ctx,
#         enum   ggml_type type,
#         int64_t ne0,
#         int64_t ne1);
def ggml_new_tensor_2d(
    ctx: ggml_context_p,
    type: Union[ctypes.c_int, int],
    ne0: Union[ctypes.c_int64, int],
    ne1: Union[ctypes.c_int64, int],
    /,
) -> ggml_tensor_p:
    """Create a new 2-dimensional tensor with the given type and number of elements in each dimension.

    Parameters:
        ctx: ggml context
        type: ggml type
        ne0: number of elements in dimension 0
        ne1: number of elements in dimension 1

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_new_tensor_2d = lib.ggml_new_tensor_2d
ggml_new_tensor_2d.argtypes = [
    ggml_context_p_ctypes,
    ctypes.c_int,
    ctypes.c_int64,
    ctypes.c_int64,
]
ggml_new_tensor_2d.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_new_tensor_3d(
#         struct ggml_context * ctx,
#         enum   ggml_type type,
#         int64_t ne0,
#         int64_t ne1,
#         int64_t ne2);
def ggml_new_tensor_3d(
    ctx: ggml_context_p,
    type: Union[ctypes.c_int, int],
    ne0: Union[ctypes.c_int64, int],
    ne1: Union[ctypes.c_int64, int],
    ne2: Union[ctypes.c_int64, int],
    /,
) -> ggml_tensor_p:
    """Create a new 3-dimensional tensor with the given type and number of elements in each dimension.

    Parameters:
        ctx: ggml context
        type: ggml type
        ne0: number of elements in dimension 0
        ne1: number of elements in dimension 1
        ne2: number of elements in dimension 2

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_new_tensor_3d = lib.ggml_new_tensor_3d
ggml_new_tensor_3d.argtypes = [
    ggml_context_p_ctypes,
    ctypes.c_int,
    ctypes.c_int64,
    ctypes.c_int64,
    ctypes.c_int64,
]
ggml_new_tensor_3d.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_new_tensor_4d(
#         struct ggml_context * ctx,
#         enum   ggml_type type,
#         int64_t ne0,
#         int64_t ne1,
#         int64_t ne2,
#         int64_t ne3);
def ggml_new_tensor_4d(
    ctx: ggml_context_p,
    type: Union[ctypes.c_int, int],
    ne0: Union[ctypes.c_int64, int],
    ne1: Union[ctypes.c_int64, int],
    ne2: Union[ctypes.c_int64, int],
    ne3: Union[ctypes.c_int64, int],
    /,
) -> ggml_tensor_p:
    """Create a new 4-dimensional tensor with the given type and number of elements in each dimension.

    Parameters:
        ctx: ggml context
        type: ggml type
        ne0: number of elements in dimension 0
        ne1: number of elements in dimension 1
        ne2: number of elements in dimension 2

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_new_tensor_4d = lib.ggml_new_tensor_4d
ggml_new_tensor_4d.argtypes = [
    ggml_context_p_ctypes,
    ctypes.c_int,
    ctypes.c_int64,
    ctypes.c_int64,
    ctypes.c_int64,
    ctypes.c_int64,
]
ggml_new_tensor_4d.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_new_i32(struct ggml_context * ctx, int32_t value);
def ggml_new_i32(
    ctx: ggml_context_p, value: Union[ctypes.c_int32, int], /
) -> ggml_tensor_p:
    """Create a 1 element tensor with the given integer value.

    Parameters:
        ctx: ggml context
        value: integer value

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_new_i32 = lib.ggml_new_i32
ggml_new_i32.argtypes = [ggml_context_p_ctypes, ctypes.c_int32]
ggml_new_i32.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_new_f32(struct ggml_context * ctx, float value);
def ggml_new_f32(
    ctx: ggml_context_p, value: Union[ctypes.c_float, float], /
) -> ggml_tensor_p:
    """Create a 1 element tensor with the given float value.

    Parameters:
        ctx: ggml context
        value: float value

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_new_f32 = lib.ggml_new_f32
ggml_new_f32.argtypes = [ggml_context_p_ctypes, ctypes.c_float]
ggml_new_f32.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_dup_tensor (struct ggml_context * ctx, const struct ggml_tensor * src);
def ggml_dup_tensor(ctx: ggml_context_p, src: ggml_tensor_p, /) -> ggml_tensor_p:
    """Create a new tensor with the same type and dimensions as the source tensor.

    Parameters:
        ctx: ggml context
        src: source tensor

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_dup_tensor = lib.ggml_dup_tensor
ggml_dup_tensor.argtypes = [ggml_context_p_ctypes, ctypes.POINTER(ggml_tensor)]
ggml_dup_tensor.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_view_tensor(struct ggml_context * ctx, struct ggml_tensor * src);
def ggml_view_tensor(ctx: ggml_context_p, src: ggml_tensor_p, /) -> ggml_tensor_p:
    """Create a new tensor with the same type, dimensions and data as the source tensor.

    Parameters:
        ctx: ggml context
        src: source tensor

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_view_tensor = lib.ggml_view_tensor
ggml_view_tensor.argtypes = [ggml_context_p_ctypes, ctypes.POINTER(ggml_tensor)]
ggml_view_tensor.restype = ctypes.POINTER(ggml_tensor)


# // Context tensor enumeration and lookup
# GGML_API struct ggml_tensor * ggml_get_first_tensor(const struct ggml_context * ctx);
def ggml_get_first_tensor(ctx: ggml_context_p, /) -> ggml_tensor_p:
    """Get the first tensor from the ggml context.

    Parameters:
        ctx: ggml context

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_get_first_tensor = lib.ggml_get_first_tensor
ggml_get_first_tensor.argtypes = [ggml_context_p_ctypes]
ggml_get_first_tensor.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_get_next_tensor (const struct ggml_context * ctx, struct ggml_tensor * tensor);
def ggml_get_next_tensor(
    ctx: ggml_context_p, tensor: ggml_tensor_p, /
) -> ggml_tensor_p:
    """Get the next tensor from the ggml context.

    Parameters:
        ctx: ggml context
        tensor: tensor

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_get_next_tensor = lib.ggml_get_next_tensor
ggml_get_next_tensor.argtypes = [ggml_context_p_ctypes, ctypes.POINTER(ggml_tensor)]
ggml_get_next_tensor.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_get_tensor(struct ggml_context * ctx, const char * name);
def ggml_get_tensor(ctx: ggml_context_p, name: bytes, /) -> ggml_tensor_p:
    """Get a tensor from the ggml context by name.

    Parameters:
        ctx: ggml context
        name: name of tensor

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_get_tensor = lib.ggml_get_tensor
ggml_get_tensor.argtypes = [ggml_context_p_ctypes, ctypes.c_char_p]
ggml_get_tensor.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_set_zero(struct ggml_tensor * tensor);
def ggml_set_zero(tensor: ggml_tensor_p, /) -> ggml_tensor_p:
    """Zero all elements in a tensor.

    Parameters:
        tensor: tensor

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_set_zero = lib.ggml_set_zero
ggml_set_zero.argtypes = [ctypes.POINTER(ggml_tensor)]
ggml_set_zero.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_set_i32 (struct ggml_tensor * tensor, int32_t value);
def ggml_set_i32(
    tensor: ggml_tensor_p, value: Union[ctypes.c_int32, int], /
) -> ggml_tensor_p:
    """Set all elements in a tensor to the given integer value.

    Parameters:
        tensor: tensor
        value: integer value

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_set_i32 = lib.ggml_set_i32
ggml_set_i32.argtypes = [ctypes.POINTER(ggml_tensor), ctypes.c_int32]
ggml_set_i32.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_set_f32 (struct ggml_tensor * tensor, float value);
def ggml_set_f32(
    tensor: ggml_tensor_p, value: Union[ctypes.c_float, float], /
) -> ggml_tensor_p:
    """Set all elements in a tensor to the given float value.

    Parameters:
        tensor: tensor
        value: float value

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_set_f32 = lib.ggml_set_f32
ggml_set_f32.argtypes = [ctypes.POINTER(ggml_tensor), ctypes.c_float]
ggml_set_f32.restype = ctypes.POINTER(ggml_tensor)


# // Converts a flat index into coordinates
# GGML_API void    ggml_unravel_index(const struct ggml_tensor * tensor, int64_t i, int64_t * i0, int64_t * i1, int64_t * i2, int64_t * i3);
def ggml_unravel_index(
    tensor: ggml_tensor_p,
    i: Union[ctypes.c_int64, int],
    i0,  # type: "ctypes._Pointer(ctypes.c_int64)" # type: ignore
    i1,  # type: "ctypes._Pointer(ctypes.c_int64)" # type: ignore
    i2,  # type: "ctypes._Pointer(ctypes.c_int64)" # type: ignore
    i3,  # type: "ctypes._Pointer(ctypes.c_int64)" # type: ignore
    /,
):
    """Convert a flat index into coordinates.

    Parameters:
        tensor: tensor
        i: flat index
        i0: pointer to index 0
        i1: pointer to index 1
        i2: pointer to index 2
        i3: pointer to index 3"""
    ...


ggml_unravel_index = lib.ggml_unravel_index
ggml_unravel_index.argtypes = [
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int64,
    ctypes.POINTER(ctypes.c_int64),
    ctypes.POINTER(ctypes.c_int64),
    ctypes.POINTER(ctypes.c_int64),
    ctypes.POINTER(ctypes.c_int64),
]
ggml_unravel_index.restype = None


# GGML_API int32_t ggml_get_i32_1d(const struct ggml_tensor * tensor, int i);
def ggml_get_i32_1d(tensor: ggml_tensor_p, i: Union[ctypes.c_int, int], /) -> int:
    """Get the integer value of the i-th element in a 1-dimensional tensor.

    Parameters:
        tensor: tensor
        i: index of element

    Returns:
        integer value of element at index i"""
    ...


ggml_get_i32_1d = lib.ggml_get_i32_1d
ggml_get_i32_1d.argtypes = [ctypes.POINTER(ggml_tensor), ctypes.c_int]
ggml_get_i32_1d.restype = ctypes.c_int32


# GGML_API void    ggml_set_i32_1d(const struct ggml_tensor * tensor, int i, int32_t value);
def ggml_set_i32_1d(
    tensor: ggml_tensor_p,
    i: Union[ctypes.c_int, int],
    value: Union[ctypes.c_int32, int],
    /,
):
    """Set the integer value of the i-th element in a 1-dimensional tensor.

    Parameters:
        tensor: tensor
        i: index of element
        value: integer value to set element to"""
    ...


ggml_set_i32_1d = lib.ggml_set_i32_1d
ggml_set_i32_1d.argtypes = [
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int,
    ctypes.c_int32,
]
ggml_set_i32_1d.restype = None


# GGML_API int32_t ggml_get_i32_nd(const struct ggml_tensor * tensor, int i0, int i1, int i2, int i3);
def ggml_get_i32_nd(
    tensor: ggml_tensor_p,
    i0: Union[ctypes.c_int, int],
    i1: Union[ctypes.c_int, int],
    i2: Union[ctypes.c_int, int],
    i3: Union[ctypes.c_int, int],
    /,
) -> int:
    """Get the integer value of the element at the given coordinates in a 4-dimensional tensor.

    Parameters:
        tensor: tensor
        i0: index of element in dimension 0
        i1: index of element in dimension 1
        i2: index of element in dimension 2
        i3: index of element in dimension 3

    Returns:
        integer value of element at coordinates"""
    ...


ggml_get_i32_nd = lib.ggml_get_i32_nd
ggml_get_i32_nd.argtypes = [
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
]
ggml_get_i32_nd.restype = ctypes.c_int32


# GGML_API void    ggml_set_i32_nd(const struct ggml_tensor * tensor, int i0, int i1, int i2, int i3, int32_t value);
def ggml_set_i32_nd(
    tensor: ggml_tensor_p,
    i0: Union[ctypes.c_int, int],
    i1: Union[ctypes.c_int, int],
    i2: Union[ctypes.c_int, int],
    i3: Union[ctypes.c_int, int],
    value: Union[ctypes.c_int32, int],
    /,
):
    """Set the integer value of the element at the given coordinates in a 4-dimensional tensor.

    Parameters:
        tensor: tensor
        i0: index of element in dimension 0
        i1: index of element in dimension 1
        i2: index of element in dimension 2
        i3: index of element in dimension 3
        value: integer value to set element to"""
    ...


ggml_set_i32_nd = lib.ggml_set_i32_nd
ggml_set_i32_nd.argtypes = [
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int32,
]
ggml_set_i32_nd.restype = None


# GGML_API float   ggml_get_f32_1d(const struct ggml_tensor * tensor, int i);
def ggml_get_f32_1d(tensor: ggml_tensor_p, i: Union[ctypes.c_int, int], /) -> float:
    """Get the float value of the i-th element in a 1-dimensional tensor.

    Parameters:
        tensor: tensor

    Returns:
        float value of element at index i"""
    ...


ggml_get_f32_1d = lib.ggml_get_f32_1d
ggml_get_f32_1d.argtypes = [ctypes.POINTER(ggml_tensor), ctypes.c_int]
ggml_get_f32_1d.restype = ctypes.c_float


# GGML_API void    ggml_set_f32_1d(const struct ggml_tensor * tensor, int i, float value);
def ggml_set_f32_1d(
    tensor: ggml_tensor_p,
    i: Union[ctypes.c_int, int],
    value: Union[ctypes.c_float, float],
    /,
):
    """Set the float value of the i-th element in a 1-dimensional tensor.

    Parameters:
        tensor: tensor
        i: index of element
        value: float value to set element to"""
    ...


ggml_set_f32_1d = lib.ggml_set_f32_1d
ggml_set_f32_1d.argtypes = [
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int,
    ctypes.c_float,
]
ggml_set_f32_1d.restype = None


# GGML_API float   ggml_get_f32_nd(const struct ggml_tensor * tensor, int i0, int i1, int i2, int i3);
def ggml_get_f32_nd(
    tensor: ggml_tensor_p,
    i0: Union[ctypes.c_int, int],
    i1: Union[ctypes.c_int, int],
    i2: Union[ctypes.c_int, int],
    i3: Union[ctypes.c_int, int],
    /,
) -> float:
    """Get the float value of the element at the given coordinates in a 4-dimensional tensor.

    Parameters:
        tensor: tensor
        i0: index of element in dimension 0
        i1: index of element in dimension 1
        i2: index of element in dimension 2
        i3: index of element in dimension 3

    Returns:
        float value of element at coordinates"""
    ...


ggml_get_f32_nd = lib.ggml_get_f32_nd
ggml_get_f32_nd.argtypes = [
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
]
ggml_get_f32_nd.restype = ctypes.c_float


# GGML_API void    ggml_set_f32_nd(const struct ggml_tensor * tensor, int i0, int i1, int i2, int i3, float value);
def ggml_set_f32_nd(
    tensor: ggml_tensor_p,
    i0: Union[ctypes.c_int, int],
    i1: Union[ctypes.c_int, int],
    i2: Union[ctypes.c_int, int],
    i3: Union[ctypes.c_int, int],
    value: Union[ctypes.c_float, float],
    /,
):
    """Set the float value of the element at the given coordinates in a 4-dimensional tensor.

    Parameters:
        tensor: tensor
        i0: index of element in dimension 0
        i1: index of element in dimension 1
        i2: index of element in dimension 2
        i3: index of element in dimension 3
        value: float value to set element to"""
    ...


ggml_set_f32_nd = lib.ggml_set_f32_nd
ggml_set_f32_nd.argtypes = [
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_float,
]
ggml_set_f32_nd.restype = None


# GGML_API void *  ggml_get_data    (const struct ggml_tensor * tensor);
def ggml_get_data(tensor: ggml_tensor_p, /) -> Optional[int]:
    """Get the data pointer of a tensor.

    Parameters:
        tensor: tensor

    Returns:
        Pointer to data, or None if tensor has no data"""
    ...


ggml_get_data = lib.ggml_get_data
ggml_get_data.argtypes = [ctypes.POINTER(ggml_tensor)]
ggml_get_data.restype = ctypes.c_void_p


# GGML_API float * ggml_get_data_f32(const struct ggml_tensor * tensor);
def ggml_get_data_f32(
    tensor: ggml_tensor_p, /
) -> Optional[CtypesArray[ctypes.c_float]]:
    """Get the data pointer of a tensor as a float array.

    Parameters:
        tensor: tensor

    Returns:
        (Optional[ctypes.Array[ctypes.c_float]]): array of float to data, or None if tensor has no data
    """
    ...


ggml_get_data_f32 = lib.ggml_get_data_f32
ggml_get_data_f32.argtypes = [ctypes.POINTER(ggml_tensor)]
ggml_get_data_f32.restype = ctypes.POINTER(ctypes.c_float)


# GGML_API GGML_CALL enum ggml_unary_op ggml_get_unary_op(const struct ggml_tensor * tensor);
def ggml_get_unary_op(tensor: ggml_tensor_p, /) -> int:
    """Get the unary operation of a tensor.

    Parameters:
        tensor: tensor

    Returns:
        unary operation"""
    ...


ggml_get_unary_op = lib.ggml_get_unary_op
ggml_get_unary_op.argtypes = [ctypes.POINTER(ggml_tensor)]
ggml_get_unary_op.restype = ctypes.c_int


# GGML_API const char *         ggml_get_name(const struct ggml_tensor * tensor);
def ggml_get_name(tensor: ggml_tensor_p, /) -> bytes:
    """Get the name of a tensor.

    Parameters:
        tensor: tensor

    Returns:
        name of tensor"""
    ...


ggml_get_name = lib.ggml_get_name
ggml_get_name.argtypes = [ctypes.POINTER(ggml_tensor)]
ggml_get_name.restype = ctypes.c_char_p


# GGML_API struct ggml_tensor * ggml_set_name(struct ggml_tensor * tensor, const char * name);
def ggml_set_name(tensor: ggml_tensor_p, name: bytes, /) -> ggml_tensor_p:
    """Set the name of a tensor.

    Parameters:
        tensor: tensor
        name: name to set tensor to

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_set_name = lib.ggml_set_name
ggml_set_name.argtypes = [ctypes.POINTER(ggml_tensor), ctypes.c_char_p]
ggml_set_name.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_format_name(struct ggml_tensor * tensor, const char * fmt, ...);
def ggml_format_name(
    tensor: ggml_tensor_p,
    fmt: bytes,
    /,
    *args: Sequence[Union[bool, int, float, str]],
) -> ggml_tensor_p:
    """Format the name of a tensor using the given format c string and arguments.

    Parameters:
        tensor: tensor
        fmt: format c string
        args: arguments to format string

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_format_name = lib.ggml_format_name
ggml_format_name.argtypes = [ctypes.POINTER(ggml_tensor), ctypes.c_char_p]
ggml_format_name.restype = ctypes.POINTER(ggml_tensor)

# //
# // operations on tensors with backpropagation
# //


# GGML_API struct ggml_tensor * ggml_dup(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a);
def ggml_dup(ctx: ggml_context_p, a: ggml_tensor_p, /) -> ggml_tensor_p:
    ...


ggml_dup = lib.ggml_dup
ggml_dup.argtypes = [ggml_context_p_ctypes, ctypes.POINTER(ggml_tensor)]
ggml_dup.restype = ctypes.POINTER(ggml_tensor)


# // in-place, returns view(a)
# GGML_API struct ggml_tensor * ggml_dup_inplace(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a);
def ggml_dup_inplace(ctx: ggml_context_p, a: ggml_tensor_p, /) -> ggml_tensor_p:
    ...


ggml_dup_inplace = lib.ggml_dup_inplace
ggml_dup_inplace.argtypes = [ggml_context_p_ctypes, ctypes.POINTER(ggml_tensor)]
ggml_dup_inplace.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_add(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * b);
def ggml_add(
    ctx: ggml_context_p, a: ggml_tensor_p, b: ggml_tensor_p, /
) -> ggml_tensor_p:
    """Add two tensors together and return the result.

    Parameters:
        ctx: ggml context
        a: first tensor
        b: second tensor

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_add = lib.ggml_add
ggml_add.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
]
ggml_add.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_add_inplace(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * b);
def ggml_add_inplace(
    ctx: ggml_context_p, a: ggml_tensor_p, b: ggml_tensor_p, /
) -> ggml_tensor_p:
    """Add two tensors together and store the result in the first tensor.

    Parameters:
        ctx: ggml context
        a: first tensor
        b: second tensor

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_add_inplace = lib.ggml_add_inplace
ggml_add_inplace.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
]
ggml_add_inplace.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_add_cast(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * b,
#         enum   ggml_type      type);
def ggml_add_cast(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    b: ggml_tensor_p,
    type: Union[ctypes.c_int, int],
    /,
) -> ggml_tensor_p:
    """Add two tensors together and cast the result to the given type.

    Parameters:
        ctx: ggml context
        a: first tensor
        b: second tensor
        type: type to cast result to

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_add_cast = lib.ggml_add_cast
ggml_add_cast.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int,
]
ggml_add_cast.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_add1(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * b);
def ggml_add1(
    ctx: ggml_context_p, a: ggml_tensor_p, b: ggml_tensor_p, /
) -> ggml_tensor_p:
    ...


ggml_add1 = lib.ggml_add1
ggml_add1.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
]
ggml_add1.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_add1_inplace(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * b);
def ggml_add1_inplace(
    ctx: ggml_context_p, a: ggml_tensor_p, b: ggml_tensor_p, /
) -> ggml_tensor_p:
    ...


ggml_add1_inplace = lib.ggml_add1_inplace
ggml_add1_inplace.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
]
ggml_add1_inplace.restype = ctypes.POINTER(ggml_tensor)


# // dst = a
# // view(dst, nb1, nb2, nb3, offset) += b
# // return dst
# GGML_API struct ggml_tensor * ggml_acc(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * b,
#         size_t                nb1,
#         size_t                nb2,
#         size_t                nb3,
#         size_t                offset);
def ggml_acc(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    b: ggml_tensor_p,
    nb1: Union[ctypes.c_size_t, int],
    nb2: Union[ctypes.c_size_t, int],
    nb3: Union[ctypes.c_size_t, int],
    offset: Union[ctypes.c_size_t, int],
    /,
) -> ggml_tensor_p:
    ...


ggml_acc = lib.ggml_acc
ggml_acc.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.c_size_t,
    ctypes.c_size_t,
    ctypes.c_size_t,
    ctypes.c_size_t,
]
ggml_acc.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_acc_inplace(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * b,
#         size_t                nb1,
#         size_t                nb2,
#         size_t                nb3,
#         size_t                offset);
def ggml_acc_inplace(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    b: ggml_tensor_p,
    nb1: Union[ctypes.c_size_t, int],
    nb2: Union[ctypes.c_size_t, int],
    nb3: Union[ctypes.c_size_t, int],
    offset: Union[ctypes.c_size_t, int],
    /,
) -> ggml_tensor_p:
    ...


ggml_acc_inplace = lib.ggml_acc_inplace
ggml_acc_inplace.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.c_size_t,
    ctypes.c_size_t,
    ctypes.c_size_t,
    ctypes.c_size_t,
]
ggml_acc_inplace.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_sub(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * b);
def ggml_sub(
    ctx: ggml_context_p, a: ggml_tensor_p, b: ggml_tensor_p, /
) -> ggml_tensor_p:
    """Subtract two tensors and return the result.

    Parameters:
        ctx: ggml context
        a: first tensor
        b: second tensor

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_sub = lib.ggml_sub
ggml_sub.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
]
ggml_sub.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_sub_inplace(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * b);
def ggml_sub_inplace(
    ctx: ggml_context_p, a: ggml_tensor_p, b: ggml_tensor_p, /
) -> ggml_tensor_p:
    """Subtract two tensors and store the result in the first tensor.

    Parameters:
        ctx: ggml context
        a: first tensor
        b: second tensor

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_sub_inplace = lib.ggml_sub_inplace
ggml_sub_inplace.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
]
ggml_sub_inplace.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_mul(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * b);
def ggml_mul(
    ctx: ggml_context_p, a: ggml_tensor_p, b: ggml_tensor_p, /
) -> ggml_tensor_p:
    """Element-wise multiply two tensors and return the result.

    Parameters:
        ctx: ggml context
        a: first tensor
        b: second tensor

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_mul = lib.ggml_mul
ggml_mul.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
]
ggml_mul.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_mul_inplace(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * b);
def ggml_mul_inplace(
    ctx: ggml_context_p, a: ggml_tensor_p, b: ggml_tensor_p, /
) -> ggml_tensor_p:
    """Element-wise multiply two tensors and store the result in the first tensor.

    Parameters:
        ctx: ggml context
        a: first tensor
        b: second tensor

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_mul_inplace = lib.ggml_mul_inplace
ggml_mul_inplace.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
]
ggml_mul_inplace.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_div(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * b);
def ggml_div(
    ctx: ggml_context_p, a: ggml_tensor_p, b: ggml_tensor_p, /
) -> ggml_tensor_p:
    """Element-wise divide two tensors and return the result.

    Parameters:
        ctx: ggml context
        a: first tensor
        b: second tensor

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_div = lib.ggml_div
ggml_div.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
]
ggml_div.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_div_inplace(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * b);
def ggml_div_inplace(
    ctx: ggml_context_p, a: ggml_tensor_p, b: ggml_tensor_p, /
) -> ggml_tensor_p:
    """Element-wise divide two tensors and store the result in the first tensor.

    Parameters:
        ctx: ggml context
        a: first tensor
        b: second tensor

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_div_inplace = lib.ggml_div_inplace
ggml_div_inplace.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
]
ggml_div_inplace.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_sqr(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a);
def ggml_sqr(ctx: ggml_context_p, a: ggml_tensor_p, /) -> ggml_tensor_p:
    """Square all elements in a tensor and return the result.

    Parameters:
        ctx: ggml context
        a: tensor

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_sqr = lib.ggml_sqr
ggml_sqr.argtypes = [ggml_context_p_ctypes, ctypes.POINTER(ggml_tensor)]
ggml_sqr.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_sqr_inplace(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a);
def ggml_sqr_inplace(ctx: ggml_context_p, a: ggml_tensor_p, /) -> ggml_tensor_p:
    """Square all elements in a tensor and store the result in the first tensor.

    Parameters:
        ctx: ggml context
        a: tensor

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_sqr_inplace = lib.ggml_sqr_inplace
ggml_sqr_inplace.argtypes = [ggml_context_p_ctypes, ctypes.POINTER(ggml_tensor)]
ggml_sqr_inplace.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_sqrt(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a);
def ggml_sqrt(ctx: ggml_context_p, a: ggml_tensor_p, /) -> ggml_tensor_p:
    """Square root all elements in a tensor and return the result.

    Parameters:
        ctx: ggml context
        a: tensor

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_sqrt = lib.ggml_sqrt
ggml_sqrt.argtypes = [ggml_context_p_ctypes, ctypes.POINTER(ggml_tensor)]
ggml_sqrt.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_sqrt_inplace(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a);
def ggml_sqrt_inplace(ctx: ggml_context_p, a: ggml_tensor_p, /) -> ggml_tensor_p:
    """Square root all elements in a tensor and store the result in the first tensor.

    Parameters:
        ctx: ggml context

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_sqrt_inplace = lib.ggml_sqrt_inplace
ggml_sqrt_inplace.argtypes = [ggml_context_p_ctypes, ctypes.POINTER(ggml_tensor)]
ggml_sqrt_inplace.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_log(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a);
def ggml_log(ctx: ggml_context_p, a: ggml_tensor_p, /) -> ggml_tensor_p:
    """Take the natural logarithm of all elements in a tensor and return the result.

    Parameters:
        ctx: ggml context
        a: tensor

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_log = lib.ggml_log
ggml_log.argtypes = [ggml_context_p_ctypes, ctypes.POINTER(ggml_tensor)]
ggml_log.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_log_inplace(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a);
def ggml_log_inplace(ctx: ggml_context_p, a: ggml_tensor_p, /) -> ggml_tensor_p:
    """Take the natural logarithm of all elements in a tensor and store the result in the first tensor.

    Parameters:
        ctx: ggml context
        a: tensor

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_log_inplace = lib.ggml_log_inplace
ggml_log_inplace.argtypes = [ggml_context_p_ctypes, ctypes.POINTER(ggml_tensor)]
ggml_log_inplace.restype = ctypes.POINTER(ggml_tensor)


# // return scalar
# GGML_API struct ggml_tensor * ggml_sum(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a);
def ggml_sum(ctx: ggml_context_p, a: ggml_tensor_p, /) -> ggml_tensor_p:
    """Sum all elements in a tensor and return the result.

    Parameters:
        ctx: ggml context
        a: tensor

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_sum = lib.ggml_sum
ggml_sum.argtypes = [ggml_context_p_ctypes, ctypes.POINTER(ggml_tensor)]
ggml_sum.restype = ctypes.POINTER(ggml_tensor)


# // sums along rows, with input shape [a,b,c,d] return shape [1,b,c,d]
# GGML_API struct ggml_tensor * ggml_sum_rows(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a);
def ggml_sum_rows(ctx: ggml_context_p, a: ggml_tensor_p, /) -> ggml_tensor_p:
    """Sum all elements in a tensor along the first axis and return the result.

    sums along rows, with input shape [a,b,c,d] return shape [1,b,c,d]

    Parameters:
        ctx: ggml context
        a: tensor

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_sum_rows = lib.ggml_sum_rows
ggml_sum_rows.argtypes = [ggml_context_p_ctypes, ctypes.POINTER(ggml_tensor)]
ggml_sum_rows.restype = ctypes.POINTER(ggml_tensor)


# // mean along rows
# GGML_API struct ggml_tensor * ggml_mean(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a);
def ggml_mean(ctx: ggml_context_p, a: ggml_tensor_p, /) -> ggml_tensor_p:
    """Take the mean of all elements in a tensor and return the result.

    Parameters:
        ctx: ggml context
        a: tensor

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_mean = lib.ggml_mean
ggml_mean.argtypes = [ggml_context_p_ctypes, ctypes.POINTER(ggml_tensor)]
ggml_mean.restype = ctypes.POINTER(ggml_tensor)


# // argmax along rows
# GGML_API struct ggml_tensor * ggml_argmax(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a);
def ggml_argmax(ctx: ggml_context_p, a: ggml_tensor_p, /) -> ggml_tensor_p:
    """Take the argmax of all elements in a tensor and return the result.

    argmax along rows

    Parameters:
        ctx: ggml context
        a: tensor

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_argmax = lib.ggml_argmax
ggml_argmax.argtypes = [ggml_context_p_ctypes, ctypes.POINTER(ggml_tensor)]
ggml_argmax.restype = ctypes.POINTER(ggml_tensor)


# // if a is the same shape as b, and a is not parameter, return a
# // otherwise, return a new tensor: repeat(a) to fit in b
# GGML_API struct ggml_tensor * ggml_repeat(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * b);
def ggml_repeat(
    ctx: ggml_context_p, a: ggml_tensor_p, b: ggml_tensor_p, /
) -> ggml_tensor_p:
    """Repeat a tensor to fit the shape of another tensor.

    If a is the same shape as b, and a is not parameter, return a

    Parameters:
        ctx: ggml context
        a: tensor to repeat
        b: tensor to fit

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_repeat = lib.ggml_repeat
ggml_repeat.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
]
ggml_repeat.restype = ctypes.POINTER(ggml_tensor)


# // sums repetitions in a into shape of b
# GGML_API struct ggml_tensor * ggml_repeat_back(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * b);
def ggml_repeat_back(
    ctx: ggml_context_p, a: ggml_tensor_p, b: ggml_tensor_p, /
) -> ggml_tensor_p:
    ...


ggml_repeat_back = lib.ggml_repeat_back
ggml_repeat_back.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
]
ggml_repeat_back.restype = ctypes.POINTER(ggml_tensor)


# // concat a and b on dim 2
# // used in stable-diffusion
# GGML_API struct ggml_tensor * ggml_concat(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * b);
def ggml_concat(
    ctx: ggml_context_p, a: ggml_tensor_p, b: ggml_tensor_p, /
) -> ggml_tensor_p:
    """Concatenate two tensors along the second axis and return the result.

    Parameters:
        ctx: ggml context
        a: first tensor
        b: second tensor

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_concat = lib.ggml_concat
ggml_concat.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
]
ggml_concat.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_abs(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a);
def ggml_abs(ctx: ggml_context_p, a: ggml_tensor_p, /) -> ggml_tensor_p:
    """Take the absolute value of all elements in a tensor and return the result.

    Parameters:
        ctx: ggml context
        a: tensor

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_abs = lib.ggml_abs
ggml_abs.argtypes = [ggml_context_p_ctypes, ctypes.POINTER(ggml_tensor)]
ggml_abs.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_abs_inplace(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a);
def ggml_abs_inplace(ctx: ggml_context_p, a: ggml_tensor_p, /) -> ggml_tensor_p:
    """Take the absolute value of all elements in a tensor and store the result in the first tensor.

    Parameters:
        ctx: ggml context
        a: tensor

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_abs_inplace = lib.ggml_abs_inplace
ggml_abs_inplace.argtypes = [ggml_context_p_ctypes, ctypes.POINTER(ggml_tensor)]
ggml_abs_inplace.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_sgn(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a);
def ggml_sgn(ctx: ggml_context_p, a: ggml_tensor_p, /) -> ggml_tensor_p:
    """Get the sign of all elements in a tensor and return the result.

    Parameters:
        ctx: ggml context
        a: tensor

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_sgn = lib.ggml_sgn
ggml_sgn.argtypes = [ggml_context_p_ctypes, ctypes.POINTER(ggml_tensor)]
ggml_sgn.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_sgn_inplace(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a);
def ggml_sgn_inplace(ctx: ggml_context_p, a: ggml_tensor_p, /) -> ggml_tensor_p:
    """Get the sign of all elements in a tensor and store the result in the first tensor.

    Parameters:
        ctx: ggml context
        a: tensor

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_sgn_inplace = lib.ggml_sgn_inplace
ggml_sgn_inplace.argtypes = [ggml_context_p_ctypes, ctypes.POINTER(ggml_tensor)]
ggml_sgn_inplace.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_neg(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a);
def ggml_neg(ctx: ggml_context_p, a: ggml_tensor_p, /) -> ggml_tensor_p:
    """Negate all elements in a tensor and return the result.

    Parameters:
        ctx: ggml context
        a: tensor

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_neg = lib.ggml_neg
ggml_neg.argtypes = [ggml_context_p_ctypes, ctypes.POINTER(ggml_tensor)]
ggml_neg.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_neg_inplace(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a);
def ggml_neg_inplace(ctx: ggml_context_p, a: ggml_tensor_p, /) -> ggml_tensor_p:
    """Negate all elements in a tensor and store the result in the first tensor.

    Parameters:
        ctx: ggml context
        a: tensor

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_neg_inplace = lib.ggml_neg_inplace
ggml_neg_inplace.argtypes = [ggml_context_p_ctypes, ctypes.POINTER(ggml_tensor)]
ggml_neg_inplace.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_step(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a);
def ggml_step(ctx: ggml_context_p, a: ggml_tensor_p, /) -> ggml_tensor_p:
    ...


ggml_step = lib.ggml_step
ggml_step.argtypes = [ggml_context_p_ctypes, ctypes.POINTER(ggml_tensor)]
ggml_step.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_tanh(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a);
def ggml_tanh(ctx: ggml_context_p, a: ggml_tensor_p, /) -> ggml_tensor_p:
    """Apply the tanh activation function to all elements in a tensor and return the result.

    Parameters:
        ctx: ggml context
        a: tensor

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_tanh = lib.ggml_tanh
ggml_tanh.argtypes = [ggml_context_p_ctypes, ctypes.POINTER(ggml_tensor)]
ggml_tanh.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_tanh_inplace(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a);
def ggml_tanh_inplace(ctx: ggml_context_p, a: ggml_tensor_p, /) -> ggml_tensor_p:
    """Apply the tanh activation function to all elements in a tensor and store the result in the first tensor.

    Parameters:
        ctx: ggml context
        a: tensor

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_tanh_inplace = lib.ggml_tanh_inplace
ggml_tanh_inplace.argtypes = [ggml_context_p_ctypes, ctypes.POINTER(ggml_tensor)]
ggml_tanh_inplace.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_elu(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a);
def ggml_elu(ctx: ggml_context_p, a: ggml_tensor_p, /) -> ggml_tensor_p:
    """Apply the ELU activation function to all elements in a tensor and return the result.

    Parameters:
        ctx: ggml context
        a: tensor

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_elu = lib.ggml_elu
ggml_elu.argtypes = [ggml_context_p_ctypes, ctypes.POINTER(ggml_tensor)]
ggml_elu.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_elu_inplace(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a);
def ggml_elu_inplace(ctx: ggml_context_p, a: ggml_tensor_p, /) -> ggml_tensor_p:
    """Apply the ELU activation function to all elements in a tensor and store the result in the first tensor.

    Parameters:
        ctx: ggml context
        a: tensor

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_elu_inplace = lib.ggml_elu_inplace
ggml_elu_inplace.argtypes = [ggml_context_p_ctypes, ctypes.POINTER(ggml_tensor)]
ggml_elu_inplace.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_relu(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a);
def ggml_relu(ctx: ggml_context_p, a: ggml_tensor_p, /) -> ggml_tensor_p:
    """Apply the ReLU activation function to all elements in a tensor and return the result.

    Parameters:
        ctx: ggml context
        a: tensor

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_relu = lib.ggml_relu
ggml_relu.argtypes = [ggml_context_p_ctypes, ctypes.POINTER(ggml_tensor)]
ggml_relu.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_leaky_relu(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a, float negative_slope, bool inplace);
def ggml_leaky_relu(
    ctx: ggml_context_p, a: ggml_tensor_p, negative_slope: float, inplace: bool, /
) -> ggml_tensor_p:
    """Apply the Leaky ReLU activation function to all elements in a tensor and return the result.

    Parameters:
        ctx: ggml context
        a: tensor
        negative_slope: negative slope
        inplace: whether to store the result in the first tensor

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_leaky_relu = lib.ggml_leaky_relu
ggml_leaky_relu.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.c_float,
    ctypes.c_bool,
]
ggml_leaky_relu.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_relu_inplace(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a);
def ggml_relu_inplace(ctx: ggml_context_p, a: ggml_tensor_p, /) -> ggml_tensor_p:
    """Apply the ReLU activation function to all elements in a tensor and store the result in the first tensor.

    Parameters:
        ctx: ggml context
        a: tensor

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_relu_inplace = lib.ggml_relu_inplace
ggml_relu_inplace.argtypes = [ggml_context_p_ctypes, ctypes.POINTER(ggml_tensor)]
ggml_relu_inplace.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_gelu(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a);
def ggml_gelu(ctx: ggml_context_p, a: ggml_tensor_p, /) -> ggml_tensor_p:
    """Apply the Gaussian Error Linear Unit activation function to all elements in a tensor and return the result.

    Parameters:
        ctx: ggml context
        a: tensor

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_gelu = lib.ggml_gelu
ggml_gelu.argtypes = [ggml_context_p_ctypes, ctypes.POINTER(ggml_tensor)]
ggml_gelu.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_gelu_inplace(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a);
def ggml_gelu_inplace(ctx: ggml_context_p, a: ggml_tensor_p, /) -> ggml_tensor_p:
    """Apply the Gaussian Error Linear Unit activation function to all elements in a tensor and store the result in the first tensor.

    Parameters:
        ctx: ggml context
        a: tensor

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_gelu_inplace = lib.ggml_gelu_inplace
ggml_gelu_inplace.argtypes = [ggml_context_p_ctypes, ctypes.POINTER(ggml_tensor)]
ggml_gelu_inplace.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_gelu_quick(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a);
def ggml_gelu_quick(ctx: ggml_context_p, a: ggml_tensor_p, /) -> ggml_tensor_p:
    """Apply the Gaussian Error Linear Unit activation function to all elements in a tensor and return the result.

    Parameters:
        ctx: ggml context
        a: tensor

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_gelu_quick = lib.ggml_gelu_quick
ggml_gelu_quick.argtypes = [ggml_context_p_ctypes, ctypes.POINTER(ggml_tensor)]
ggml_gelu_quick.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_gelu_quick_inplace(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a);
def ggml_gelu_quick_inplace(ctx: ggml_context_p, a: ggml_tensor_p, /) -> ggml_tensor_p:
    """Apply the Gaussian Error Linear Unit activation function to all elements in a tensor and store the result in the first tensor.

    Parameters:
        ctx: ggml context
        a: tensor

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_gelu_quick_inplace = lib.ggml_gelu_quick_inplace
ggml_gelu_quick_inplace.argtypes = [ggml_context_p_ctypes, ctypes.POINTER(ggml_tensor)]
ggml_gelu_quick_inplace.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_silu(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a);
def ggml_silu(ctx: ggml_context_p, a: ggml_tensor_p, /) -> ggml_tensor_p:
    """Apply the Sigmoid Linear Unit activation function to all elements in a tensor and return the result.

    Parameters:
        ctx: ggml context
        a: tensor

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_silu = lib.ggml_silu
ggml_silu.argtypes = [ggml_context_p_ctypes, ctypes.POINTER(ggml_tensor)]
ggml_silu.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_silu_inplace(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a);
def ggml_silu_inplace(ctx: ggml_context_p, a: ggml_tensor_p, /) -> ggml_tensor_p:
    """Apply the Sigmoid Linear Unit activation function to all elements in a tensor and store the result in the first tensor.

    Parameters:
        ctx: ggml context
        a: tensor

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_silu_inplace = lib.ggml_silu_inplace
ggml_silu_inplace.argtypes = [ggml_context_p_ctypes, ctypes.POINTER(ggml_tensor)]
ggml_silu_inplace.restype = ctypes.POINTER(ggml_tensor)


# // a - x
# // b - dy
# GGML_API struct ggml_tensor * ggml_silu_back(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * b);
def ggml_silu_back(
    ctx: ggml_context_p, a: ggml_tensor_p, b: ggml_tensor_p, /
) -> ggml_tensor_p:
    ...


ggml_silu_back = lib.ggml_silu_back
ggml_silu_back.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
]
ggml_silu_back.restype = ctypes.POINTER(ggml_tensor)


# // hardswish(x) = x * relu6(x + 3) / 6
# GGML_API struct ggml_tensor * ggml_hardswish(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a);
def ggml_hardswish(ctx: ggml_context_p, a: ggml_tensor_p, /) -> ggml_tensor_p:
    """Apply the Hardswish activation function to all elements in a tensor and return the result.

    Parameters:
        ctx: ggml context
        a: tensor

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_hardswish = lib.ggml_hardswish
ggml_hardswish.argtypes = [ggml_context_p_ctypes, ctypes.POINTER(ggml_tensor)]
ggml_hardswish.restype = ctypes.POINTER(ggml_tensor)


# // hardsigmoid(x) = relu6(x + 3) / 6
# GGML_API struct ggml_tensor * ggml_hardsigmoid(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a);
def ggml_hardsigmoid(ctx: ggml_context_p, a: ggml_tensor_p, /) -> ggml_tensor_p:
    """Apply the Hardsigmoid activation function to all elements in a tensor and return the result.

    Parameters:
        ctx: ggml context
        a: tensor

    Returns:
        Pointer to ggml_tensor"""

    ...


ggml_hardsigmoid = lib.ggml_hardsigmoid
ggml_hardsigmoid.argtypes = [ggml_context_p_ctypes, ctypes.POINTER(ggml_tensor)]
ggml_hardsigmoid.restype = ctypes.POINTER(ggml_tensor)


# // normalize along rows
# GGML_API struct ggml_tensor * ggml_norm(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a
#         float                eps);
def ggml_norm(
    ctx: ggml_context_p, a: ggml_tensor_p, eps: Union[ctypes.c_float, float], /
) -> ggml_tensor_p:
    """Normalize all elements in a tensor along the first axis and return the result.

    normalize along rows.

    Parameters:
        ctx: ggml context
        a: tensor
        eps: minimum value to avoid division by zero

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_norm = lib.ggml_norm
ggml_norm.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.c_float,
]
ggml_norm.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_norm_inplace(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a
#         float                eps);
def ggml_norm_inplace(
    ctx: ggml_context_p, a: ggml_tensor_p, eps: Union[ctypes.c_float, float], /
) -> ggml_tensor_p:
    """Normalize all elements in a tensor along the first axis and store the result in the first tensor.

    normalize along rows.

    Parameters:
        ctx: ggml context
        a: tensor
        eps: minimum value to avoid division by zero

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_norm_inplace = lib.ggml_norm_inplace
ggml_norm_inplace.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.c_float,
]
ggml_norm_inplace.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_rms_norm(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         float                 eps);
def ggml_rms_norm(
    ctx: ggml_context_p, a: ggml_tensor_p, eps: Union[ctypes.c_float, float], /
) -> ggml_tensor_p:
    """Compute the RMS norm of a tensor and return the result.

    Parameters:
        ctx: ggml context
        a: tensor
        eps: float

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_rms_norm = lib.ggml_rms_norm
ggml_rms_norm.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.c_float,
]
ggml_rms_norm.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_rms_norm_inplace(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         float                 eps);
def ggml_rms_norm_inplace(
    ctx: ggml_context_p, a: ggml_tensor_p, eps: Union[ctypes.c_float, float], /
) -> ggml_tensor_p:
    ...


ggml_rms_norm_inplace = lib.ggml_rms_norm_inplace
ggml_rms_norm_inplace.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.c_float,
]
ggml_rms_norm_inplace.restype = ctypes.POINTER(ggml_tensor)


# // group normalize along ne0*ne1*n_groups
# // used in stable-diffusion
# // TODO: eps is hardcoded to 1e-6 for now
# GGML_API struct ggml_tensor * ggml_group_norm(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         int                   n_groups);
def ggml_group_norm(
    ctx: ggml_context_p, a: ggml_tensor_p, n_groups: int, /
) -> ggml_tensor_p:
    """Group normalize a tensor and return the result.

    Parameters:
        ctx: ggml context
        a: tensor
        n_groups: int

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_group_norm = lib.ggml_group_norm
ggml_group_norm.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int,
]
ggml_group_norm.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_group_norm_inplace(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         int                   n_groups);
def ggml_group_norm_inplace(
    ctx: ggml_context_p, a: ggml_tensor_p, n_groups: int, /
) -> ggml_tensor_p:
    """Group normalize a tensor and store the result in the first tensor.

    Parameters:
        ctx: ggml context
        a: tensor
        n_groups: int

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_group_norm_inplace = lib.ggml_group_norm_inplace
ggml_group_norm_inplace.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int,
]
ggml_group_norm_inplace.restype = ctypes.POINTER(ggml_tensor)


# // a - x
# // b - dy
# GGML_API struct ggml_tensor * ggml_rms_norm_back(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * b
#         float                 eps);
def ggml_rms_norm_back(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    b: ggml_tensor_p,
    eps: Union[ctypes.c_float, float],
    /,
) -> ggml_tensor_p:
    ...


ggml_rms_norm_back = lib.ggml_rms_norm_back
ggml_rms_norm_back.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.c_float,
]
ggml_rms_norm_back.restype = ctypes.POINTER(ggml_tensor)


# // A: k columns, n rows => [ne03, ne02, n, k]
# // B: k columns, m rows  (i.e. we transpose it internally) => [ne03 * x, ne02 * y, m, k]
# // result is n columns, m rows => [ne03 * x, ne02 * y, m, n]
# GGML_API struct ggml_tensor * ggml_mul_mat(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * b);
def ggml_mul_mat(
    ctx: ggml_context_p, a: ggml_tensor_p, b: ggml_tensor_p, /
) -> ggml_tensor_p:
    """Multiply two matrices and return the result.

    A: k columns, n rows => [ne03, ne02, n, k]
    B: k columns, m rows  (i.e. we transpose it internally) => [ne03 * x, ne02 * y, m, k]
    result is n columns, m rows => [ne03 * x, ne02 * y, m, n]

    Parameters:
        ctx: ggml context
        a: tensor
        b: tensor

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_mul_mat = lib.ggml_mul_mat
ggml_mul_mat.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
]
ggml_mul_mat.restype = ctypes.POINTER(ggml_tensor)


# // change the precision of a matrix multiplication
# // set to GGML_PREC_F32 for higher precision (useful for phi-2)
# GGML_API void ggml_mul_mat_set_prec(
#         struct ggml_tensor * a,
#         enum ggml_prec       prec);
def ggml_mul_mat_set_prec(a: ggml_tensor_p, prec: Union[ctypes.c_int, int], /) -> None:
    """Change the precision of a matrix multiplication.

    set to GGML_PREC_F32 for higher precision (useful for phi-2)

    Parameters:
        a: tensor
        prec: precision"""
    ...


ggml_mul_mat_set_prec = lib.ggml_mul_mat_set_prec
ggml_mul_mat_set_prec.argtypes = [ctypes.POINTER(ggml_tensor), ctypes.c_int]
ggml_mul_mat_set_prec.restype = None


# // indirect matrix multiplication
# //  ggml_mul_mat_id(ctx, as, ids, id, b) ~= ggml_mul_mat(as[ids[id]], b)
# GGML_API struct ggml_tensor * ggml_mul_mat_id(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * const as[],
#         int                   n_as,
#         struct ggml_tensor  * ids,
#         int                   id,
#         struct ggml_tensor  * b);
def ggml_mul_mat_id(
    ctx: ggml_context_p,
    as_,  # type: ctypes.POINTER(ctypes.POINTER(ggml_tensor)) # type: ignore
    n_as: int,
    ids: ggml_tensor_p,
    id_: int,
    b: ggml_tensor_p,
    /,
) -> ggml_tensor_p:
    """Multiply two matrices and return the result.

    indirect matrix multiplication

    ggml_mul_mat_id(ctx, as, ids, id, b) ~= ggml_mul_mat(as[ids[id]], b)

    Parameters:
        ctx: ggml context
        as_: array of tensor pointers
        n_as: int
        ids: tensor
        id_: int
        b: tensor

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_mul_mat_id = lib.ggml_mul_mat_id
ggml_mul_mat_id.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ctypes.POINTER(ggml_tensor)),
    ctypes.c_int,
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int,
    ctypes.POINTER(ggml_tensor),
]
ggml_mul_mat_id.restype = ctypes.POINTER(ggml_tensor)


# // A: m columns, n rows,
# // B: p columns, n rows,
# // result is m columns, p rows
# GGML_API struct ggml_tensor * ggml_out_prod(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * b);
def ggml_out_prod(
    ctx: ggml_context_p, a: ggml_tensor_p, b: ggml_tensor_p, /
) -> ggml_tensor_p:
    """Compute the outer product of two matrices and return the result.

    A: m columns, n rows,
    B: p columns, n rows,
    result is m columns, p rows

    Parameters:
        ctx: ggml context
        a: tensor
        b: tensor

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_out_prod = lib.ggml_out_prod
ggml_out_prod.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
]
ggml_out_prod.restype = ctypes.POINTER(ggml_tensor)

# //
# // operations on tensors without backpropagation
# //


# GGML_API struct ggml_tensor * ggml_scale(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         float                 s);
def ggml_scale(
    ctx: ggml_context_p, a: ggml_tensor_p, s: Union[ctypes.c_float, float], /
) -> ggml_tensor_p:
    """Scale a tensor by another tensor and return the result.

    Parameters:
        ctx: ggml context
        a: tensor
        s: float

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_scale = lib.ggml_scale
ggml_scale.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.c_float,
]
ggml_scale.restype = ctypes.POINTER(ggml_tensor)


# // in-place, returns view(a)
# GGML_API struct ggml_tensor * ggml_scale_inplace(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         float                 s);
def ggml_scale_inplace(
    ctx: ggml_context_p, a: ggml_tensor_p, s: Union[ctypes.c_float, float], /
) -> ggml_tensor_p:
    """Scale a tensor by another tensor and store the result in the first tensor.

    Parameters:
        ctx: ggml context
        a: tensor
        s: float

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_scale_inplace = lib.ggml_scale_inplace
ggml_scale_inplace.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.c_float,
]
ggml_scale_inplace.restype = ctypes.POINTER(ggml_tensor)


# // b -> view(a,offset,nb1,nb2,3), return modified a
# GGML_API struct ggml_tensor * ggml_set(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * b,
#         size_t                nb1,
#         size_t                nb2,
#         size_t                nb3,
#         size_t                offset);
def ggml_set(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    b: ggml_tensor_p,
    nb1: Union[ctypes.c_size_t, int],
    nb2: Union[ctypes.c_size_t, int],
    nb3: Union[ctypes.c_size_t, int],
    offset: Union[ctypes.c_size_t, int],
    /,
) -> ggml_tensor_p:
    ...


ggml_set = lib.ggml_set
ggml_set.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.c_size_t,
    ctypes.c_size_t,
    ctypes.c_size_t,
    ctypes.c_size_t,
]
ggml_set.restype = ctypes.POINTER(ggml_tensor)


# // b -> view(a,offset,nb1,nb2,3), return view(a)
# GGML_API struct ggml_tensor * ggml_set_inplace(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * b,
#         size_t                nb1,
#         size_t                nb2,
#         size_t                nb3,
#         size_t                offset);
def ggml_set_inplace(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    b: ggml_tensor_p,
    nb1: Union[ctypes.c_size_t, int],
    nb2: Union[ctypes.c_size_t, int],
    nb3: Union[ctypes.c_size_t, int],
    offset: Union[ctypes.c_size_t, int],
    /,
) -> ggml_tensor_p:
    ...


ggml_set_inplace = lib.ggml_set_inplace
ggml_set_inplace.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.c_size_t,
    ctypes.c_size_t,
    ctypes.c_size_t,
    ctypes.c_size_t,
]
ggml_set_inplace.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_set_1d(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * b,
#         size_t                offset);
def ggml_set_1d(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    b: ggml_tensor_p,
    offset: Union[ctypes.c_size_t, int],
    /,
) -> ggml_tensor_p:
    ...


ggml_set_1d = lib.ggml_set_1d
ggml_set_1d.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.c_size_t,
]
ggml_set_1d.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_set_1d_inplace(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * b,
#         size_t                offset);
def ggml_set_1d_inplace(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    b: ggml_tensor_p,
    offset: Union[ctypes.c_size_t, int],
    /,
) -> ggml_tensor_p:
    ...


ggml_set_1d_inplace = lib.ggml_set_1d_inplace
ggml_set_1d_inplace.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.c_size_t,
]
ggml_set_1d_inplace.restype = ctypes.POINTER(ggml_tensor)


# // b -> view(a,offset,nb1,nb2,3), return modified a
# GGML_API struct ggml_tensor * ggml_set_2d(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * b,
#         size_t                nb1,
#         size_t                offset);
def ggml_set_2d(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    b: ggml_tensor_p,
    nb1: Union[ctypes.c_size_t, int],
    offset: Union[ctypes.c_size_t, int],
    /,
) -> ggml_tensor_p:
    ...


ggml_set_2d = lib.ggml_set_2d
ggml_set_2d.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.c_size_t,
    ctypes.c_size_t,
]
ggml_set_2d.restype = ctypes.POINTER(ggml_tensor)


# // b -> view(a,offset,nb1,nb2,3), return view(a)
# GGML_API struct ggml_tensor * ggml_set_2d_inplace(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * b,
#         size_t                nb1,
#         size_t                offset);
def ggml_set_2d_inplace(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    b: ggml_tensor_p,
    nb1: Union[ctypes.c_size_t, int],
    offset: Union[ctypes.c_size_t, int],
    /,
) -> ggml_tensor_p:
    ...


ggml_set_2d_inplace = lib.ggml_set_2d_inplace
ggml_set_2d_inplace.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.c_size_t,
    ctypes.c_size_t,
]
ggml_set_2d_inplace.restype = ctypes.POINTER(ggml_tensor)


# // a -> b, return view(b)
# GGML_API struct ggml_tensor * ggml_cpy(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * b);
def ggml_cpy(
    ctx: ggml_context_p, a: ggml_tensor_p, b: ggml_tensor_p, /
) -> ggml_tensor_p:
    ...


ggml_cpy = lib.ggml_cpy
ggml_cpy.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
]
ggml_cpy.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_cast(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         enum   ggml_type      type);
def ggml_cast(
    ctx: ggml_context_p, a: ggml_tensor_p, type_: Union[ctypes.c_int, int], /
) -> ggml_tensor_p:
    ...


ggml_cast = lib.ggml_cast
ggml_cast.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int,
]
ggml_cast.restype = ctypes.POINTER(ggml_tensor)


# // make contiguous
# GGML_API struct ggml_tensor * ggml_cont(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a);
def ggml_cont(ctx: ggml_context_p, a: ggml_tensor_p, /) -> ggml_tensor_p:
    """Make a tensor contiguous and return the result.

    Parameters:
        ctx: ggml context
        a: tensor

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_cont = lib.ggml_cont
ggml_cont.argtypes = [ggml_context_p_ctypes, ctypes.POINTER(ggml_tensor)]
ggml_cont.restype = ctypes.POINTER(ggml_tensor)


# // make contiguous, with new shape
# GGML_API struct ggml_tensor * ggml_cont_1d(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         int64_t               ne0);
def ggml_cont_1d(
    ctx: ggml_context_p, a: ggml_tensor_p, ne0: Union[ctypes.c_int64, int], /
) -> ggml_tensor_p:
    ...


ggml_cont_1d = lib.ggml_cont_1d
ggml_cont_1d.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int64,
]
ggml_cont_1d.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_cont_2d(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         int64_t               ne0,
#         int64_t               ne1);
def ggml_cont_2d(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    ne0: Union[ctypes.c_int64, int],
    ne1: Union[ctypes.c_int64, int],
    /,
) -> ggml_tensor_p:
    ...


ggml_cont_2d = lib.ggml_cont_2d
ggml_cont_2d.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int64,
    ctypes.c_int64,
]
ggml_cont_2d.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_cont_3d(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         int64_t               ne0,
#         int64_t               ne1,
#         int64_t               ne2);
def ggml_cont_3d(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    ne0: Union[ctypes.c_int64, int],
    ne1: Union[ctypes.c_int64, int],
    ne2: Union[ctypes.c_int64, int],
    /,
) -> ggml_tensor_p:
    ...


ggml_cont_3d = lib.ggml_cont_3d
ggml_cont_3d.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int64,
    ctypes.c_int64,
    ctypes.c_int64,
]
ggml_cont_3d.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_cont_4d(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         int64_t               ne0,
#         int64_t               ne1,
#         int64_t               ne2,
#         int64_t               ne3);
def ggml_cont_4d(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    ne0: Union[ctypes.c_int64, int],
    ne1: Union[ctypes.c_int64, int],
    ne2: Union[ctypes.c_int64, int],
    ne3: Union[ctypes.c_int64, int],
    /,
) -> ggml_tensor_p:
    ...


ggml_cont_4d = lib.ggml_cont_4d
ggml_cont_4d.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int64,
    ctypes.c_int64,
    ctypes.c_int64,
    ctypes.c_int64,
]
ggml_cont_4d.restype = ctypes.POINTER(ggml_tensor)


# // return view(a), b specifies the new shape
# // TODO: when we start computing gradient, make a copy instead of view
# GGML_API struct ggml_tensor * ggml_reshape(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * b);
def ggml_reshape(
    ctx: ggml_context_p, a: ggml_tensor_p, b: ggml_tensor_p, /
) -> ggml_tensor_p:
    ...


ggml_reshape = lib.ggml_reshape
ggml_reshape.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
]
ggml_reshape.restype = ctypes.POINTER(ggml_tensor)


# // return view(a)
# // TODO: when we start computing gradient, make a copy instead of view
# GGML_API struct ggml_tensor * ggml_reshape_1d(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         int64_t               ne0);
def ggml_reshape_1d(
    ctx: ggml_context_p, a: ggml_tensor_p, ne0: Union[ctypes.c_int64, int], /
) -> ggml_tensor_p:
    ...


ggml_reshape_1d = lib.ggml_reshape_1d
ggml_reshape_1d.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int64,
]
ggml_reshape_1d.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_reshape_2d(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         int64_t               ne0,
#         int64_t               ne1);
def ggml_reshape_2d(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    ne0: Union[ctypes.c_int64, int],
    ne1: Union[ctypes.c_int64, int],
    /,
) -> ggml_tensor_p:
    ...


ggml_reshape_2d = lib.ggml_reshape_2d
ggml_reshape_2d.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int64,
    ctypes.c_int64,
]
ggml_reshape_2d.restype = ctypes.POINTER(ggml_tensor)


# // return view(a)
# // TODO: when we start computing gradient, make a copy instead of view
# GGML_API struct ggml_tensor * ggml_reshape_3d(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         int64_t               ne0,
#         int64_t               ne1,
#         int64_t               ne2);
def ggml_reshape_3d(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    ne0: Union[ctypes.c_int64, int],
    ne1: Union[ctypes.c_int64, int],
    ne2: Union[ctypes.c_int64, int],
    /,
) -> ggml_tensor_p:
    ...


ggml_reshape_3d = lib.ggml_reshape_3d
ggml_reshape_3d.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int64,
    ctypes.c_int64,
    ctypes.c_int64,
]
ggml_reshape_3d.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_reshape_4d(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         int64_t               ne0,
#         int64_t               ne1,
#         int64_t               ne2,
#         int64_t               ne3);
def ggml_reshape_4d(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    ne0: Union[ctypes.c_int64, int],
    ne1: Union[ctypes.c_int64, int],
    ne2: Union[ctypes.c_int64, int],
    ne3: Union[ctypes.c_int64, int],
    /,
) -> ggml_tensor_p:
    ...


ggml_reshape_4d = lib.ggml_reshape_4d
ggml_reshape_4d.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int64,
    ctypes.c_int64,
    ctypes.c_int64,
    ctypes.c_int64,
]
ggml_reshape_4d.restype = ctypes.POINTER(ggml_tensor)


# // offset in bytes
# GGML_API struct ggml_tensor * ggml_view_1d(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         int64_t               ne0,
#         size_t                offset);
def ggml_view_1d(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    ne0: Union[ctypes.c_int64, int],
    offset: Union[ctypes.c_size_t, int],
    /,
) -> ggml_tensor_p:
    ...


ggml_view_1d = lib.ggml_view_1d
ggml_view_1d.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int64,
    ctypes.c_size_t,
]
ggml_view_1d.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_view_2d(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         int64_t               ne0,
#         int64_t               ne1,
#         size_t                nb1, // row stride in bytes
#         size_t                offset);
def ggml_view_2d(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    ne0: Union[ctypes.c_int64, int],
    ne1: Union[ctypes.c_int64, int],
    nb1: Union[ctypes.c_size_t, int],
    offset: Union[ctypes.c_size_t, int],
    /,
) -> ggml_tensor_p:
    ...


ggml_view_2d = lib.ggml_view_2d
ggml_view_2d.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int64,
    ctypes.c_int64,
    ctypes.c_size_t,
    ctypes.c_size_t,
]
ggml_view_2d.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_view_3d(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         int64_t               ne0,
#         int64_t               ne1,
#         int64_t               ne2,
#         size_t                nb1, // row   stride in bytes
#         size_t                nb2, // slice stride in bytes
#         size_t                offset);
def ggml_view_3d(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    ne0: Union[ctypes.c_int64, int],
    ne1: Union[ctypes.c_int64, int],
    ne2: Union[ctypes.c_int64, int],
    nb1: Union[ctypes.c_size_t, int],
    nb2: Union[ctypes.c_size_t, int],
    offset: Union[ctypes.c_size_t, int],
    /,
) -> ggml_tensor_p:
    ...


ggml_view_3d = lib.ggml_view_3d
ggml_view_3d.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int64,
    ctypes.c_int64,
    ctypes.c_int64,
    ctypes.c_size_t,
    ctypes.c_size_t,
    ctypes.c_size_t,
]
ggml_view_3d.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_view_4d(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         int64_t               ne0,
#         int64_t               ne1,
#         int64_t               ne2,
#         int64_t               ne3,
#         size_t                nb1, // row   stride in bytes
#         size_t                nb2, // slice stride in bytes
#         size_t                nb3,
#         size_t                offset);
def ggml_view_4d(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    ne0: Union[ctypes.c_int64, int],
    ne1: Union[ctypes.c_int64, int],
    ne2: Union[ctypes.c_int64, int],
    ne3: Union[ctypes.c_int64, int],
    nb1: Union[ctypes.c_size_t, int],
    nb2: Union[ctypes.c_size_t, int],
    nb3: Union[ctypes.c_size_t, int],
    offset: Union[ctypes.c_size_t, int],
    /,
) -> ggml_tensor_p:
    ...


ggml_view_4d = lib.ggml_view_4d
ggml_view_4d.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int64,
    ctypes.c_int64,
    ctypes.c_int64,
    ctypes.c_int64,
    ctypes.c_size_t,
    ctypes.c_size_t,
    ctypes.c_size_t,
    ctypes.c_size_t,
]
ggml_view_4d.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_permute(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         int                   axis0,
#         int                   axis1,
#         int                   axis2,
#         int                   axis3);
def ggml_permute(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    axis0: Union[ctypes.c_int, int],
    axis1: Union[ctypes.c_int, int],
    axis2: Union[ctypes.c_int, int],
    axis3: Union[ctypes.c_int, int],
    /,
) -> ggml_tensor_p:
    ...


ggml_permute = lib.ggml_permute
ggml_permute.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
]
ggml_permute.restype = ctypes.POINTER(ggml_tensor)


# // alias for ggml_permute(ctx, a, 1, 0, 2, 3)
# GGML_API struct ggml_tensor * ggml_transpose(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a);
def ggml_transpose(ctx: ggml_context_p, a: ggml_tensor_p, /) -> ggml_tensor_p:
    """Transpose *the first two dimensions* of a tensor and return the result.

    alias for `ggml_permute(ctx, a, 1, 0, 2, 3)`

    Parameters:
        ctx: ggml context
        a: tensor

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_transpose = lib.ggml_transpose
ggml_transpose.argtypes = [ggml_context_p_ctypes, ctypes.POINTER(ggml_tensor)]
ggml_transpose.restype = ctypes.POINTER(ggml_tensor)


# // supports 3D: a->ne[2] == b->ne[1]
# GGML_API struct ggml_tensor * ggml_get_rows(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * b);
def ggml_get_rows(
    ctx: ggml_context_p, a: ggml_tensor_p, b: ggml_tensor_p, /
) -> ggml_tensor_p:
    ...


ggml_get_rows = lib.ggml_get_rows
ggml_get_rows.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
]
ggml_get_rows.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_get_rows_back(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * b,
#         struct ggml_tensor  * c);
def ggml_get_rows_back(
    ctx: ggml_context_p, a: ggml_tensor_p, b: ggml_tensor_p, c: ggml_tensor_p, /
) -> ggml_tensor_p:
    ...


ggml_get_rows_back = lib.ggml_get_rows_back
ggml_get_rows_back.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
]
ggml_get_rows_back.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_diag(
#     struct ggml_context     * ctx,
#     struct ggml_tensor      * a);
def ggml_diag(ctx: ggml_context_p, a: ggml_tensor_p, /) -> ggml_tensor_p:
    ...


ggml_diag = lib.ggml_diag
ggml_diag.argtypes = [ggml_context_p_ctypes, ctypes.POINTER(ggml_tensor)]
ggml_diag.restype = ctypes.POINTER(ggml_tensor)


# // set elements above the diagonal to -INF
# GGML_API struct ggml_tensor * ggml_diag_mask_inf(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         int                   n_past);
def ggml_diag_mask_inf(
    ctx: ggml_context_p, a: ggml_tensor_p, n_past: Union[ctypes.c_int, int], /
) -> ggml_tensor_p:
    ...


ggml_diag_mask_inf = lib.ggml_diag_mask_inf
ggml_diag_mask_inf.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int,
]
ggml_diag_mask_inf.restype = ctypes.POINTER(ggml_tensor)


# // in-place, returns view(a)
# GGML_API struct ggml_tensor * ggml_diag_mask_inf_inplace(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         int                   n_past);
def ggml_diag_mask_inf_inplace(
    ctx: ggml_context_p, a: ggml_tensor_p, n_past: Union[ctypes.c_int, int], /
) -> ggml_tensor_p:
    ...


ggml_diag_mask_inf_inplace = lib.ggml_diag_mask_inf_inplace
ggml_diag_mask_inf_inplace.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int,
]
ggml_diag_mask_inf_inplace.restype = ctypes.POINTER(ggml_tensor)


# // set elements above the diagonal to 0
# GGML_API struct ggml_tensor * ggml_diag_mask_zero(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         int                   n_past);
def ggml_diag_mask_zero(
    ctx: ggml_context_p, a: ggml_tensor_p, n_past: Union[ctypes.c_int, int], /
) -> ggml_tensor_p:
    ...


ggml_diag_mask_zero = lib.ggml_diag_mask_zero
ggml_diag_mask_zero.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int,
]
ggml_diag_mask_zero.restype = ctypes.POINTER(ggml_tensor)


# // in-place, returns view(a)
# GGML_API struct ggml_tensor * ggml_diag_mask_zero_inplace(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         int                   n_past);
def ggml_diag_mask_zero_inplace(
    ctx: ggml_context_p, a: ggml_tensor_p, n_past: Union[ctypes.c_int, int], /
) -> ggml_tensor_p:
    ...


ggml_diag_mask_zero_inplace = lib.ggml_diag_mask_zero_inplace
ggml_diag_mask_zero_inplace.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int,
]
ggml_diag_mask_zero_inplace.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_soft_max(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a);
def ggml_soft_max(ctx: ggml_context_p, a: ggml_tensor_p, /) -> ggml_tensor_p:
    ...


ggml_soft_max = lib.ggml_soft_max
ggml_soft_max.argtypes = [ggml_context_p_ctypes, ctypes.POINTER(ggml_tensor)]
ggml_soft_max.restype = ctypes.POINTER(ggml_tensor)


# // in-place, returns view(a)
# GGML_API struct ggml_tensor * ggml_soft_max_inplace(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a);
def ggml_soft_max_inplace(ctx: ggml_context_p, a: ggml_tensor_p, /) -> ggml_tensor_p:
    ...


ggml_soft_max_inplace = lib.ggml_soft_max_inplace
ggml_soft_max_inplace.argtypes = [ggml_context_p_ctypes, ctypes.POINTER(ggml_tensor)]
ggml_soft_max_inplace.restype = ctypes.POINTER(ggml_tensor)


# // fused soft_max(a*scale + mask + pos[i]*(ALiBi slope))
# // mask is optional
# // pos is required when max_bias > 0.0f
# // max_bias = 0.0f for no ALiBi
# GGML_API struct ggml_tensor * ggml_soft_max_ext(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * mask,
#         struct ggml_tensor  * pos,
#         float                 scale,
#         float                 max_bias);
def ggml_soft_max_ext(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    mask: ggml_tensor_p,
    pos: ggml_tensor_p,
    scale: Union[ctypes.c_float, float],
    max_bias: Union[ctypes.c_float, float],
    /,
) -> ggml_tensor_p:
    ...


ggml_soft_max_ext = lib.ggml_soft_max_ext
ggml_soft_max_ext.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.c_float,
    ctypes.c_float,
]
ggml_soft_max_ext.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_soft_max_back(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * b);
def ggml_soft_max_back(
    ctx: ggml_context_p, a: ggml_tensor_p, b: ggml_tensor_p, /
) -> ggml_tensor_p:
    ...


ggml_soft_max_back = lib.ggml_soft_max_back
ggml_soft_max_back.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
]
ggml_soft_max_back.restype = ctypes.POINTER(ggml_tensor)


# // in-place, returns view(a)
# GGML_API struct ggml_tensor * ggml_soft_max_back_inplace(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * b);
def ggml_soft_max_back_inplace(
    ctx: ggml_context_p, a: ggml_tensor_p, b: ggml_tensor_p, /
) -> ggml_tensor_p:
    ...


ggml_soft_max_back_inplace = lib.ggml_soft_max_back_inplace
ggml_soft_max_back_inplace.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
]
ggml_soft_max_back_inplace.restype = ctypes.POINTER(ggml_tensor)


# // rotary position embedding
# // if mode & 1 == 1, skip n_past elements (DEPRECATED)
# // if mode & 2 == 1, GPT-NeoX style
# // if mode & 4 == 1, ChatGLM style
# //
# // b is an int32 vector with size a->ne[2], it contains the positions
# GGML_API struct ggml_tensor * ggml_rope(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * b,
#         int                   n_dims,
#         int                   mode,
#         int                   n_ctx);
def ggml_rope(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    b: ggml_tensor_p,
    n_dims: Union[ctypes.c_int, int],
    mode: Union[ctypes.c_int, int],
    n_ctx: Union[ctypes.c_int, int],
    /,
) -> ggml_tensor_p:
    """Rotary position embedding

    Parameters:
        ctx: ggml context
        a: tensor
        b: int32 vector with size a->ne[2], it contains the positions
        n_dims: number of dimensions
        mode: if mode & 1 == 1, skip n_past elements (DEPRECATED)
                if mode & 2 == 1, GPT-NeoX style
                if mode & 4 == 1, ChatGLM style
        n_ctx: context size

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_rope = lib.ggml_rope
ggml_rope.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
]
ggml_rope.restype = ctypes.POINTER(ggml_tensor)


# // in-place, returns view(a)
# GGML_API struct ggml_tensor * ggml_rope_inplace(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * b,
#         int                   n_dims,
#         int                   mode,
#         int                   n_ctx);
def ggml_rope_inplace(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    b: ggml_tensor_p,
    n_dims: Union[ctypes.c_int, int],
    mode: Union[ctypes.c_int, int],
    n_ctx: Union[ctypes.c_int, int],
    /,
) -> ggml_tensor_p:
    """Rotary position embedding inplace

    Parameters:
        ctx: ggml context
        a: tensor
        b: int32 vector with size a->ne[2], it contains the positions
        n_dims: number of dimensions
        mode: if mode & 1 == 1, skip n_past elements (DEPRECATED)
                if mode & 2 == 1, GPT-NeoX style
                if mode & 4 == 1, ChatGLM style
        n_ctx: context size

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_rope_inplace = lib.ggml_rope_inplace
ggml_rope_inplace.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
]
ggml_rope_inplace.restype = ctypes.POINTER(ggml_tensor)


# // custom RoPE
# GGML_API struct ggml_tensor * ggml_rope_custom(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * b,
#         int                   n_dims,
#         int                   mode,
#         int                   n_ctx,
#         int                   n_orig_ctx,
#         float                 freq_base,
#         float                 freq_scale,
#         float                 ext_factor,
#         float                 attn_factor,
#         float                 beta_fast,
#         float                 beta_slow);
def ggml_rope_custom(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    b: ggml_tensor_p,
    n_dims: Union[ctypes.c_int, int],
    mode: Union[ctypes.c_int, int],
    n_ctx: Union[ctypes.c_int, int],
    n_orig_ctx: Union[ctypes.c_int, int],
    freq_base: Union[ctypes.c_float, float],
    freq_scale: Union[ctypes.c_float, float],
    ext_factor: Union[ctypes.c_float, float],
    attn_factor: Union[ctypes.c_float, float],
    beta_fast: Union[ctypes.c_float, float],
    beta_slow: Union[ctypes.c_float, float],
    /,
) -> ggml_tensor_p:
    """Custom rotary position embedding"""
    ...


ggml_rope_custom = lib.ggml_rope_custom
ggml_rope_custom.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_float,
    ctypes.c_float,
    ctypes.c_float,
    ctypes.c_float,
    ctypes.c_float,
    ctypes.c_float,
]
ggml_rope_custom.restype = ctypes.POINTER(ggml_tensor)


# // in-place, returns view(a)
# GGML_API struct ggml_tensor * ggml_rope_custom_inplace(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * b,
#         int                   n_dims,
#         int                   mode,
#         int                   n_ctx,
#         int                   n_orig_ctx,
#         float                 freq_base,
#         float                 freq_scale,
#         float                 ext_factor,
#         float                 attn_factor,
#         float                 beta_fast,
#         float                 beta_slow);
def ggml_rope_custom_inplace(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    b: ggml_tensor_p,
    n_dims: Union[ctypes.c_int, int],
    mode: Union[ctypes.c_int, int],
    n_ctx: Union[ctypes.c_int, int],
    n_orig_ctx: Union[ctypes.c_int, int],
    freq_base: Union[ctypes.c_float, float],
    freq_scale: Union[ctypes.c_float, float],
    ext_factor: Union[ctypes.c_float, float],
    attn_factor: Union[ctypes.c_float, float],
    beta_fast: Union[ctypes.c_float, float],
    beta_slow: Union[ctypes.c_float, float],
    /,
) -> ggml_tensor_p:
    """Custom rotary position embedding inplace"""
    ...


ggml_rope_custom_inplace = lib.ggml_rope_custom_inplace
ggml_rope_custom_inplace.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_float,
    ctypes.c_float,
    ctypes.c_float,
    ctypes.c_float,
    ctypes.c_float,
    ctypes.c_float,
]
ggml_rope_custom_inplace.restype = ctypes.POINTER(ggml_tensor)


# // compute correction dims for YaRN RoPE scaling
# GGML_CALL void ggml_rope_yarn_corr_dims(
#     int n_dims, int n_orig_ctx, float freq_base, float beta_fast, float beta_slow, float dims[2]);
def ggml_rope_yarn_corr_dims(
    n_dims: Union[ctypes.c_int, int],
    n_orig_ctx: Union[ctypes.c_int, int],
    freq_base: Union[ctypes.c_float, float],
    beta_fast: Union[ctypes.c_float, float],
    beta_slow: Union[ctypes.c_float, float],
    dims: CtypesArray[ctypes.c_float],
    /,
) -> None:
    """Compute correction dims for YaRN RoPE scaling"""
    ...


ggml_rope_yarn_corr_dims = lib.ggml_rope_yarn_corr_dims
ggml_rope_yarn_corr_dims.argtypes = [
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_float,
    ctypes.c_float,
    ctypes.c_float,
    ctypes.POINTER(ctypes.c_float),
]
ggml_rope_yarn_corr_dims.restype = None


# // xPos RoPE, in-place, returns view(a)
# GGML_API struct ggml_tensor * ggml_rope_xpos_inplace(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * b,
#         int                   n_dims,
#         float                 base,
#         bool                  down);
def ggml_rope_xpos_inplace(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    b: ggml_tensor_p,
    n_dims: Union[ctypes.c_int, int],
    base: Union[ctypes.c_float, float],
    down: Union[ctypes.c_bool, bool],
    /,
) -> ggml_tensor_p:
    """xPos RoPE, in-place, returns view(a)"""
    ...


ggml_rope_xpos_inplace = lib.ggml_rope_xpos_inplace
ggml_rope_xpos_inplace.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int,
    ctypes.c_float,
    ctypes.c_bool,
]
ggml_rope_xpos_inplace.restype = ctypes.POINTER(ggml_tensor)


# // rotary position embedding backward, i.e compute dx from dy
# // a - dy
# GGML_API struct ggml_tensor * ggml_rope_back(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * b,
#         int                   n_dims,
#         int                   mode,
#         int                   n_ctx,
#         int                   n_orig_ctx,
#         float                 freq_base,
#         float                 freq_scale,
#         float                 ext_factor,
#         float                 attn_factor,
#         float                 beta_fast,
#         float                 beta_slow,
#         float                 xpos_base,
#         bool                  xpos_down);
def ggml_rope_back(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    b: ggml_tensor_p,
    n_dims: Union[ctypes.c_int, int],
    mode: Union[ctypes.c_int, int],
    n_ctx: Union[ctypes.c_int, int],
    n_orig_ctx: Union[ctypes.c_int, int],
    freq_base: Union[ctypes.c_float, float],
    freq_scale: Union[ctypes.c_float, float],
    ext_factor: Union[ctypes.c_float, float],
    attn_factor: Union[ctypes.c_float, float],
    beta_fast: Union[ctypes.c_float, float],
    beta_slow: Union[ctypes.c_float, float],
    xpos_base: Union[ctypes.c_float, float],
    xpos_down: Union[ctypes.c_bool, bool],
    /,
) -> ggml_tensor_p:
    """Rotary position embedding backward pass"""
    ...


ggml_rope_back = lib.ggml_rope_back
ggml_rope_back.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_float,
    ctypes.c_float,
    ctypes.c_float,
    ctypes.c_float,
    ctypes.c_float,
    ctypes.c_float,
    ctypes.c_float,
    ctypes.c_bool,
]
ggml_rope_back.restype = ctypes.POINTER(ggml_tensor)


# // alibi position embedding
# // in-place, returns view(a)
# GGML_API struct ggml_tensor * ggml_alibi(
# GGML_DEPRECATED(GGML_API struct ggml_tensor * ggml_alibi(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         int                   n_past,
#         int                   n_head,
#         float                 bias_max),
#     "use ggml_soft_max_ext instead (will be removed in Mar 2024)");
def ggml_alibi(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    n_past: Union[ctypes.c_int, int],
    n_head: Union[ctypes.c_int, int],
    bias_max: Union[ctypes.c_float, float],
    /,
) -> ggml_tensor_p:
    ...


ggml_alibi = lib.ggml_alibi
ggml_alibi.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_float,
]
ggml_alibi.restype = ctypes.POINTER(ggml_tensor)


# // clamp
# // in-place, returns view(a)
# GGML_API struct ggml_tensor * ggml_clamp(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         float                 min,
#         float                 max);
def ggml_clamp(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    min: Union[ctypes.c_float, float],
    max: Union[ctypes.c_float, float],
    /,
) -> ggml_tensor_p:
    """Clamp tensor values between min and max

    Parameters:
        ctx: ggml context
        a: tensor
        min: minimum value
        max: maximum value

    Returns:
        Pointer to ggml_tensor"""
    ...


ggml_clamp = lib.ggml_clamp
ggml_clamp.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.c_float,
    ctypes.c_float,
]
ggml_clamp.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_im2col(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * b,
#         int                  s0,
#         int                  s1,
#         int                  p0,
#         int                  p1,
#         int                  d0,
#         int                  d1,
#         bool                 is_2D,
#         enum ggml_type       dst_type);
def ggml_im2col(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    b: ggml_tensor_p,
    s0: Union[ctypes.c_int, int],
    s1: Union[ctypes.c_int, int],
    p0: Union[ctypes.c_int, int],
    p1: Union[ctypes.c_int, int],
    d0: Union[ctypes.c_int, int],
    d1: Union[ctypes.c_int, int],
    is_2D: Union[ctypes.c_bool, bool],
    dst_type: Union[ctypes.c_int, int],
    /,
) -> ggml_tensor_p:
    ...


ggml_im2col = lib.ggml_im2col
ggml_im2col.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_bool,
    ctypes.c_int,
]
ggml_im2col.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_conv_depthwise_2d(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * b,
#         int                  s0,
#         int                  s1,
#         int                  p0,
#         int                  p1,
#         int                  d0,
#         int                  d1);
def ggml_conv_depthwise_2d(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    b: ggml_tensor_p,
    s0: Union[ctypes.c_int, int],
    s1: Union[ctypes.c_int, int],
    p0: Union[ctypes.c_int, int],
    p1: Union[ctypes.c_int, int],
    d0: Union[ctypes.c_int, int],
    d1: Union[ctypes.c_int, int],
    /,
) -> ggml_tensor_p:
    ...


ggml_conv_depthwise_2d = lib.ggml_conv_depthwise_2d
ggml_conv_depthwise_2d.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
]
ggml_conv_depthwise_2d.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_conv_1d(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * b,
#         int                   s0,  // stride
#         int                   p0,  // padding
#         int                   d0); // dilation
def ggml_conv_1d(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    b: ggml_tensor_p,
    s0: Union[ctypes.c_int, int],
    p0: Union[ctypes.c_int, int],
    d0: Union[ctypes.c_int, int],
    /,
) -> ggml_tensor_p:
    """Convolution 1D

    Parameters:
        a: input tensor
        b: filter tensor
        s0: stride
        p0: padding
        d0: dilation

    Returns:
        output tensor"""
    ...


ggml_conv_1d = lib.ggml_conv_1d
ggml_conv_1d.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
]
ggml_conv_1d.restype = ctypes.POINTER(ggml_tensor)


# // conv_1d with padding = half
# // alias for ggml_conv_1d(a, b, s, a->ne[0]/2, d)
# GGML_API struct ggml_tensor* ggml_conv_1d_ph(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * b,
#         int                   s,
#         int                   d);
def ggml_conv_1d_ph(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    b: ggml_tensor_p,
    s: Union[ctypes.c_int, int],
    d: Union[ctypes.c_int, int],
    /,
) -> ggml_tensor_p:
    """Convolution 1D with padding = half

    Parameters:
        a: input tensor
        b: filter tensor
        s: stride
        d: dilation

    Returns:
        output tensor"""
    ...


ggml_conv_1d_ph = lib.ggml_conv_1d_ph
ggml_conv_1d_ph.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int,
    ctypes.c_int,
]
ggml_conv_1d_ph.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_conv_transpose_1d(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * b,
#         int                   s0,
#         int                   p0,
#         int                   d0);
def ggml_conv_transpose_1d(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    b: ggml_tensor_p,
    s0: Union[ctypes.c_int, int],
    p0: Union[ctypes.c_int, int],
    d0: Union[ctypes.c_int, int],
    /,
) -> ggml_tensor_p:
    """Convolution transpose 1D

    Parameters:
        a: input tensor
        b: filter tensor
        s0: stride
        p0: padding
        d0: dilation

    Returns:
        output tensor"""
    ...


ggml_conv_transpose_1d = lib.ggml_conv_transpose_1d
ggml_conv_transpose_1d.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
]
ggml_conv_transpose_1d.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_conv_2d(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * b,
#         int                   s0,
#         int                   s1,
#         int                   p0,
#         int                   p1,
#         int                   d0,
#         int                   d1);
def ggml_conv_2d(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    b: ggml_tensor_p,
    s0: Union[ctypes.c_int, int],
    s1: Union[ctypes.c_int, int],
    p0: Union[ctypes.c_int, int],
    p1: Union[ctypes.c_int, int],
    d0: Union[ctypes.c_int, int],
    d1: Union[ctypes.c_int, int],
    /,
) -> ggml_tensor_p:
    """Convolution 2D

    Parameters:
        a: input tensor
        b: filter tensor
        s0: stride
        s1: stride
        p0: padding
        p1: padding
        d0: dilation
        d1: dilation

    Returns:
        output tensor"""
    ...


ggml_conv_2d = lib.ggml_conv_2d
ggml_conv_2d.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
]
ggml_conv_2d.restype = ctypes.POINTER(ggml_tensor)


# // kernel size is a->ne[0] x a->ne[1]
# // stride is equal to kernel size
# // padding is zero
# // example:
# // a:     16   16    3  768
# // b:   1024 1024    3    1
# // res:   64   64  768    1
# // used in sam
# GGML_API struct ggml_tensor * ggml_conv_2d_sk_p0(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * b);
def ggml_conv_2d_sk_p0(
    ctx: ggml_context_p, a: ggml_tensor_p, b: ggml_tensor_p, /
) -> ggml_tensor_p:
    """Convolution 2D

    Parameters:
        a: input tensor
        b: filter tensor

    Returns:
        output tensor"""
    ...


ggml_conv_2d_sk_p0 = lib.ggml_conv_2d_sk_p0
ggml_conv_2d_sk_p0.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
]
ggml_conv_2d_sk_p0.restype = ctypes.POINTER(ggml_tensor)


# // kernel size is a->ne[0] x a->ne[1]
# // stride is 1
# // padding is half
# // example:
# // a:      3    3    256  256
# // b:     64   64    256    1
# // res:   64   64    256    1
# // used in sam
# GGML_API struct ggml_tensor * ggml_conv_2d_s1_ph(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * b);
def ggml_conv_2d_s1_ph(
    ctx: ggml_context_p, a: ggml_tensor_p, b: ggml_tensor_p, /
) -> ggml_tensor_p:
    """Convolution 2D with stride = 1 and padding = half

    Parameters:
        a: input tensor
        b: filter tensor

    Returns:
        output tensor"""
    ...


ggml_conv_2d_s1_ph = lib.ggml_conv_2d_s1_ph
ggml_conv_2d_s1_ph.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
]
ggml_conv_2d_s1_ph.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_conv_transpose_2d_p0(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * b,
#         int                   stride);
def ggml_conv_transpose_2d_p0(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    b: ggml_tensor_p,
    stride: Union[ctypes.c_int, int],
    /,
) -> ggml_tensor_p:
    """Convolution Transpose 2D with padding = zero

    Parameters:
        a: input tensor
        b: filter tensor
        stride: stride

    Returns:
        output tensor"""
    ...


ggml_conv_transpose_2d_p0 = lib.ggml_conv_transpose_2d_p0
ggml_conv_transpose_2d_p0.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int,
]
ggml_conv_transpose_2d_p0.restype = ctypes.POINTER(ggml_tensor)

# enum ggml_op_pool {
#     GGML_OP_POOL_MAX,
#     GGML_OP_POOL_AVG,
#     GGML_OP_POOL_COUNT,
# };
GGML_OP_POOL_MAX = 0
GGML_OP_POOL_AVG = 1
GGML_OP_POOL_COUNT = 2


# GGML_API struct ggml_tensor * ggml_pool_1d(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         enum ggml_op_pool     op,
#         int                   k0, // kernel size
#         int                   s0, // stride
#         int                   p0); // padding
def ggml_pool_1d(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    op: Union[ctypes.c_int, int],
    k0: Union[ctypes.c_int, int],
    s0: Union[ctypes.c_int, int],
    p0: Union[ctypes.c_int, int],
    /,
) -> ggml_tensor_p:
    """1D Pooling

    Parameters:
        a: input tensor
        op: pooling operation
        k0: kernel size
        s0: stride
        p0: padding

    Returns:
        output tensor"""
    ...


ggml_pool_1d = lib.ggml_pool_1d
ggml_pool_1d.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
]
ggml_pool_1d.restype = ctypes.POINTER(ggml_tensor)


# // the result will have 2*p0 padding for the first dimension
# // and 2*p1 padding for the second dimension
# GGML_API struct ggml_tensor * ggml_pool_2d(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         enum ggml_op_pool     op,
#         int                   k0,
#         int                   k1,
#         int                   s0,
#         int                   s1,
#         float                 p0,
#         float                 p1);
def ggml_pool_2d(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    op: Union[ctypes.c_int, int],
    k0: Union[ctypes.c_int, int],
    k1: Union[ctypes.c_int, int],
    s0: Union[ctypes.c_int, int],
    s1: Union[ctypes.c_int, int],
    p0: Union[ctypes.c_float, float],
    p1: Union[ctypes.c_float, float],
    /,
) -> ggml_tensor_p:
    """2D Pooling

    Parameters:
        a: input tensor
        op: pooling operation
        k0: kernel size
        k1: kernel size
        s0: stride
        s1: stride
        p0: padding
        p1: padding

    Returns:
        output tensor"""
    ...


ggml_pool_2d = lib.ggml_pool_2d
ggml_pool_2d.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_float,
    ctypes.c_float,
]
ggml_pool_2d.restype = ctypes.POINTER(ggml_tensor)


# // nearest interpolate
# // used in stable-diffusion
# GGML_API struct ggml_tensor * ggml_upscale(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         int                   scale_factor);
def ggml_upscale(
    ctx: ggml_context_p, a: ggml_tensor_p, scale_factor: Union[ctypes.c_int, int], /
) -> ggml_tensor_p:
    """Upscale

    Parameters:
        a: input tensor
        scale_factor: scale factor

    Returns:
        output tensor"""
    ...


ggml_upscale = lib.ggml_upscale
ggml_upscale.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int,
]
ggml_upscale.restype = ctypes.POINTER(ggml_tensor)


# // pad each dimension with zeros: [x, ..., x] -> [x, ..., x, 0, ..., 0]
# GGML_API struct ggml_tensor * ggml_pad(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         int                  p0,
#         int                  p1,
#         int                  p2,
#         int                  p3);
def ggml_pad(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    p0: Union[ctypes.c_int, int],
    p1: Union[ctypes.c_int, int],
    p2: Union[ctypes.c_int, int],
    p3: Union[ctypes.c_int, int],
    /,
) -> ggml_tensor_p:
    """Pad tensor with zeros

    Parameters:
        a: input tensor
        p0: padding
        p1: padding
        p2: padding
        p3: padding

    Returns:
        output tensor"""
    ...


ggml_pad = lib.ggml_pad
ggml_pad.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
]
ggml_pad.restype = ctypes.POINTER(ggml_tensor)

# // sort rows
# enum ggml_sort_order {
#     GGML_SORT_ASC,
#     GGML_SORT_DESC,
# };
GGML_SORT_ASC = 0
GGML_SORT_DESC = 1


# GGML_API struct ggml_tensor * ggml_argsort(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         enum ggml_sort_order  order);
def ggml_argsort(
    ctx: ggml_context_p, a: ggml_tensor_p, order: Union[ctypes.c_int, int], /
) -> ggml_tensor_p:
    """Argsort

    Parameters:
        a: input tensor
        order: sort order

    Returns:
        output tensor"""
    ...


ggml_argsort = lib.ggml_argsort
ggml_argsort.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int,
]
ggml_argsort.restype = ctypes.POINTER(ggml_tensor)


# // top k elements per row
# GGML_API struct ggml_tensor * ggml_top_k(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         int                   k);
def ggml_top_k(
    ctx: ggml_context_p, a: ggml_tensor_p, k: Union[ctypes.c_int, int], /
) -> ggml_tensor_p:
    """Top k elements per row

    Parameters:
        a: input tensor
        k: number of elements

    Returns:
        output tensor"""
    ...


# GGML_API struct ggml_tensor * ggml_flash_attn(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * q,
#         struct ggml_tensor  * k,
#         struct ggml_tensor  * v,
#         bool                  masked);
def ggml_flash_attn(
    ctx: ggml_context_p,
    q: ggml_tensor_p,
    k: ggml_tensor_p,
    v: ggml_tensor_p,
    masked: Union[ctypes.c_bool, bool],
    /,
) -> ggml_tensor_p:
    ...


ggml_flash_attn = lib.ggml_flash_attn
ggml_flash_attn.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.c_bool,
]
ggml_flash_attn.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_flash_attn_back(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * q,
#         struct ggml_tensor  * k,
#         struct ggml_tensor  * v,
#         struct ggml_tensor  * d,
#         bool                  masked);
def ggml_flash_attn_back(
    ctx: ggml_context_p,
    q: ggml_tensor_p,
    k: ggml_tensor_p,
    v: ggml_tensor_p,
    d: ggml_tensor_p,
    masked: Union[ctypes.c_bool, bool],
    /,
) -> ggml_tensor_p:
    ...


ggml_flash_attn_back = lib.ggml_flash_attn_back
ggml_flash_attn_back.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.c_bool,
]
ggml_flash_attn_back.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_flash_ff(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * b0,
#         struct ggml_tensor  * b1,
#         struct ggml_tensor  * c0,
#         struct ggml_tensor  * c1);
def ggml_flash_ff(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    b0: ggml_tensor_p,
    b1: ggml_tensor_p,
    c0: ggml_tensor_p,
    c1: ggml_tensor_p,
    /,
) -> ggml_tensor_p:
    ...


ggml_flash_ff = lib.ggml_flash_ff
ggml_flash_ff.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
]
ggml_flash_ff.restype = ctypes.POINTER(ggml_tensor)


# // partition into non-overlapping windows with padding if needed
# // example:
# // a:   768   64   64    1
# // w:    14
# // res: 768   14   14    25
# // used in sam
# GGML_API struct ggml_tensor * ggml_win_part(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         int                   w);
def ggml_win_part(
    ctx: ggml_context_p, a: ggml_tensor_p, w: Union[ctypes.c_int, int], /
) -> ggml_tensor_p:
    ...


ggml_win_part = lib.ggml_win_part
ggml_win_part.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int,
]
ggml_win_part.restype = ctypes.POINTER(ggml_tensor)


# // reverse of ggml_win_part
# // used in sam
# GGML_API struct ggml_tensor * ggml_win_unpart(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         int                   w0,
#         int                   h0,
#         int                   w);
def ggml_win_unpart(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    w0: Union[ctypes.c_int, int],
    h0: Union[ctypes.c_int, int],
    w: Union[ctypes.c_int, int],
    /,
) -> ggml_tensor_p:
    ...


ggml_win_unpart = lib.ggml_win_unpart
ggml_win_unpart.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
]
ggml_win_unpart.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_unary(
#         struct ggml_context * ctx,
#             struct ggml_tensor * a,
#             enum ggml_unary_op op);
def ggml_unary(
    ctx: ggml_context_p, a: ggml_tensor_p, op: Union[ctypes.c_int, int], /
) -> ggml_tensor_p:
    ...


ggml_unary = lib.ggml_unary
ggml_unary.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int,
]
ggml_unary.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_unary_inplace(
#     struct ggml_context * ctx,
#     struct ggml_tensor  * a,
#     enum ggml_unary_op op);
def ggml_unary_inplace(
    ctx: ggml_context_p, a: ggml_tensor_p, op: Union[ctypes.c_int, int], /
) -> ggml_tensor_p:
    ...


ggml_unary_inplace = lib.ggml_unary_inplace
ggml_unary_inplace.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int,
]
ggml_unary_inplace.restype = ctypes.POINTER(ggml_tensor)


# // used in sam
# GGML_API struct ggml_tensor * ggml_get_rel_pos(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         int                   qh,
#         int                   kh);
def ggml_get_rel_pos(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    qh: Union[ctypes.c_int, int],
    kh: Union[ctypes.c_int, int],
    /,
) -> ggml_tensor_p:
    ...


ggml_get_rel_pos = lib.ggml_get_rel_pos
ggml_get_rel_pos.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int,
    ctypes.c_int,
]
ggml_get_rel_pos.restype = ctypes.POINTER(ggml_tensor)


# // used in sam
# GGML_API struct ggml_tensor * ggml_add_rel_pos(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * pw,
#         struct ggml_tensor  * ph);
def ggml_add_rel_pos(
    ctx: ggml_context_p, a: ggml_tensor_p, pw: ggml_tensor_p, ph: ggml_tensor_p, /
) -> ggml_tensor_p:
    ...


ggml_add_rel_pos = lib.ggml_add_rel_pos
ggml_add_rel_pos.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
]
ggml_add_rel_pos.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_add_rel_pos_inplace(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * a,
#         struct ggml_tensor  * pw,
#         struct ggml_tensor  * ph);
def ggml_add_rel_pos_inplace(
    ctx: ggml_context_p, a: ggml_tensor_p, pw: ggml_tensor_p, ph: ggml_tensor_p, /
) -> ggml_tensor_p:
    ...


ggml_add_rel_pos_inplace = lib.ggml_add_rel_pos_inplace
ggml_add_rel_pos_inplace.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
]
ggml_add_rel_pos_inplace.restype = ctypes.POINTER(ggml_tensor)

# // custom operators (DEPRECATED)

# typedef void (*ggml_unary_op_f32_t)(const int, float *, const float *);
ggml_unary_op_f32_t = ctypes.CFUNCTYPE(
    None, ctypes.c_int, ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float)
)

# typedef void (*ggml_binary_op_f32_t)(const int, float *, const float *, const float *);
ggml_binary_op_f32_t = ctypes.CFUNCTYPE(
    None,
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_float),
    ctypes.POINTER(ctypes.c_float),
    ctypes.POINTER(ctypes.c_float),
)

# typedef void (*ggml_custom1_op_f32_t)(struct ggml_tensor *, const struct ggml_tensor *);
ggml_custom1_op_f32_t = ctypes.CFUNCTYPE(
    None, ctypes.POINTER(ggml_tensor), ctypes.POINTER(ggml_tensor)
)
"""Unary operator function type"""

# typedef void (*ggml_custom2_op_f32_t)(struct ggml_tensor *, const struct ggml_tensor *, const struct ggml_tensor *);
ggml_custom2_op_f32_t = ctypes.CFUNCTYPE(
    None,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
)
"""Binary operator function type"""

# typedef void (*ggml_custom3_op_f32_t)(struct ggml_tensor *, const struct ggml_tensor *, const struct ggml_tensor *, const struct ggml_tensor *);
ggml_custom3_op_f32_t = ctypes.CFUNCTYPE(
    None,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
)
"""Ternary operator function type"""


# GGML_API struct ggml_tensor * ggml_map_unary_f32(
#         struct ggml_context        * ctx,
#         struct ggml_tensor         * a,
#                ggml_unary_op_f32_t   fun);
def ggml_map_unary_f32(
    ctx: ggml_context_p, a: ggml_tensor_p, fun: CtypesFuncPointer, /  # type: ignore
) -> ggml_tensor_p:
    ...


ggml_map_unary_f32 = lib.ggml_map_unary_f32
ggml_map_unary_f32.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ggml_unary_op_f32_t,
]
ggml_map_unary_f32.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_map_unary_inplace_f32(
#         struct ggml_context        * ctx,
#         struct ggml_tensor         * a,
#                 ggml_unary_op_f32_t   fun);
def ggml_map_unary_inplace_f32(
    ctx: ggml_context_p, a: ggml_tensor_p, fun: CtypesFuncPointer, /  # type: ignore
) -> ggml_tensor_p:
    ...


ggml_map_unary_inplace_f32 = lib.ggml_map_unary_inplace_f32
ggml_map_unary_inplace_f32.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ggml_unary_op_f32_t,
]
ggml_map_unary_inplace_f32.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_map_binary_f32(
#         struct ggml_context         * ctx,
#         struct ggml_tensor          * a,
#         struct ggml_tensor          * b,
#                ggml_binary_op_f32_t   fun);
def ggml_map_binary_f32(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    b: ggml_tensor_p,
    fun: CtypesFuncPointer,  # type: ignore
    /,
) -> ggml_tensor_p:
    ...


ggml_map_binary_f32 = lib.ggml_map_binary_f32
ggml_map_binary_f32.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ggml_binary_op_f32_t,
]
ggml_map_binary_f32.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_map_binary_inplace_f32(
#         struct ggml_context         * ctx,
#         struct ggml_tensor          * a,
#         struct ggml_tensor          * b,
#                 ggml_binary_op_f32_t   fun);
def ggml_map_binary_inplace_f32(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    b: ggml_tensor_p,
    fun: CtypesFuncPointer,  # type: ignore
    /,
) -> ggml_tensor_p:
    ...


ggml_map_binary_inplace_f32 = lib.ggml_map_binary_inplace_f32
ggml_map_binary_inplace_f32.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ggml_binary_op_f32_t,
]
ggml_map_binary_inplace_f32.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_map_custom1_f32(
#         struct ggml_context          * ctx,
#         struct ggml_tensor           * a,
#                 ggml_custom1_op_f32_t   fun);
def ggml_map_custom1_f32(
    ctx: ggml_context_p, a: ggml_tensor_p, fun: CtypesFuncPointer, /  # type: ignore
) -> ggml_tensor_p:
    """Custom unary operator on a tensor.

    Example:
        ```python
        import ggml

        @ggml.ggml_custom1_op_f32_t
        def custom_op(b: ggml.tensor_p, a: ggml.tensor_p):
            # do something with a and copy to b
            return

        ...

        b = ggml.ggml_map_custom1_f32(ctx, a, custom_op)
        ```

    Parameters:
        a: input tensor
        fun (ggml.ggml_custom1_op_f32_t): function to apply to each element

    Returns:
        output tensor"""
    ...


ggml_map_custom1_f32 = lib.ggml_map_custom1_f32
ggml_map_custom1_f32.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ggml_custom1_op_f32_t,
]
ggml_map_custom1_f32.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_map_custom1_inplace_f32(
#         struct ggml_context          * ctx,
#         struct ggml_tensor           * a,
#                 ggml_custom1_op_f32_t   fun);
def ggml_map_custom1_inplace_f32(
    ctx: ggml_context_p, a: ggml_tensor_p, fun: "ctypes._CFuncPtr", /  # type: ignore
) -> ggml_tensor_p:
    """Custom unary operator on a tensor inplace.

    Parameters:
        a: input tensor
        fun (ggml.ggml_custom1_op_f32_t): function to apply to each element

    Returns:
        output tensor"""
    ...


ggml_map_custom1_inplace_f32 = lib.ggml_map_custom1_inplace_f32
ggml_map_custom1_inplace_f32.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ggml_custom1_op_f32_t,
]
ggml_map_custom1_inplace_f32.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_map_custom2_f32(
#         struct ggml_context          * ctx,
#         struct ggml_tensor           * a,
#         struct ggml_tensor           * b,
#                 ggml_custom2_op_f32_t   fun);
def ggml_map_custom2_f32(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    b: ggml_tensor_p,
    fun: CtypesFuncPointer,  # type: ignore
    /,
) -> ggml_tensor_p:
    """Custom binary operator on two tensors.

    Parameters:
        a: input tensor
        b: input tensor
        fun (ggml.ggml_custom2_op_f32_t): function to apply to each element

    Returns:
        output tensor"""
    ...


ggml_map_custom2_f32 = lib.ggml_map_custom2_f32
ggml_map_custom2_f32.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ggml_custom2_op_f32_t,
]
ggml_map_custom2_f32.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_map_custom2_inplace_f32(
#         struct ggml_context          * ctx,
#         struct ggml_tensor           * a,
#         struct ggml_tensor           * b,
#                 ggml_custom2_op_f32_t   fun);
def ggml_map_custom2_inplace_f32(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    b: ggml_tensor_p,
    fun: CtypesFuncPointer,  # type: ignore
) -> ggml_tensor_p:
    """Custom binary operator on two tensors inplace.

    Parameters:
        a: input tensor
        b: input tensor
        fun (ggml.ggml_custom2_op_f32_t): function to apply to each element

    Returns:
        output tensor"""
    ...


ggml_map_custom2_inplace_f32 = lib.ggml_map_custom2_inplace_f32
ggml_map_custom2_inplace_f32.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ggml_custom2_op_f32_t,
]
ggml_map_custom2_inplace_f32.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_map_custom3_f32(
#         struct ggml_context          * ctx,
#         struct ggml_tensor           * a,
#         struct ggml_tensor           * b,
#         struct ggml_tensor           * c,
#                 ggml_custom3_op_f32_t   fun);
def ggml_map_custom3_f32(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    b: ggml_tensor_p,
    c: ggml_tensor_p,
    fun: CtypesFuncPointer,  # type: ignore
) -> ggml_tensor_p:
    """Custom ternary operator on three tensors.

    Parameters:
        a: input tensor
        b: input tensor
        c: input tensor
        fun (ggml.ggml_custom3_op_f32_t): function to apply to each element

    Returns:
        output tensor"""
    ...


ggml_map_custom3_f32 = lib.ggml_map_custom3_f32
ggml_map_custom3_f32.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ggml_custom3_op_f32_t,
]
ggml_map_custom3_f32.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_map_custom3_inplace_f32(
#         struct ggml_context          * ctx,
#         struct ggml_tensor           * a,
#         struct ggml_tensor           * b,
#         struct ggml_tensor           * c,
#                 ggml_custom3_op_f32_t   fun);
def ggml_map_custom3_inplace_f32(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    b: ggml_tensor_p,
    c: ggml_tensor_p,
    fun: CtypesFuncPointer,  # type: ignore
) -> ggml_tensor_p:
    """Custom ternary operator on three tensors inplace.

    Parameters:
        a: input tensor
        b: input tensor
        c: input tensor
        fun (ggml.ggml_custom3_op_f32_t): function to apply to each element

    Returns:
        output tensor"""
    ...


ggml_map_custom3_inplace_f32 = lib.ggml_map_custom3_inplace_f32
ggml_map_custom3_inplace_f32.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ggml_custom3_op_f32_t,
]
ggml_map_custom3_inplace_f32.restype = ctypes.POINTER(ggml_tensor)

# // custom operators v2

# typedef void (*ggml_custom1_op_t)(struct ggml_tensor * dst , const struct ggml_tensor * a, int ith, int nth, void * userdata);
ggml_custom1_op_t = ctypes.CFUNCTYPE(
    None,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_void_p,
)
"""Custom unary operator on a tensor."""

# typedef void (*ggml_custom2_op_t)(struct ggml_tensor * dst , const struct ggml_tensor * a, const struct ggml_tensor * b, int ith, int nth, void * userdata);
ggml_custom2_op_t = ctypes.CFUNCTYPE(
    None,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_void_p,
)
"""Custom binary operator on two tensors."""

# typedef void (*ggml_custom3_op_t)(struct ggml_tensor * dst , const struct ggml_tensor * a, const struct ggml_tensor * b, const struct ggml_tensor * c, int ith, int nth, void * userdata);
ggml_custom3_op_t = ctypes.CFUNCTYPE(
    None,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_void_p,
)
"""Custom ternary operator on three tensors."""

# #define GGML_N_TASKS_MAX -1
GGML_N_TASKS_MAX = -1


# GGML_API struct ggml_tensor * ggml_map_custom1(
#         struct ggml_context   * ctx,
#         struct ggml_tensor    * a,
#         ggml_custom1_op_t       fun,
#         int                     n_tasks,
#         void                  * userdata);
def ggml_map_custom1(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    fun: CtypesFuncPointer,  # type: ignore
    n_tasks: Union[ctypes.c_int, int],
    userdata: Union[ctypes.c_void_p, int, None],
) -> ggml_tensor_p:
    ...


ggml_map_custom1 = lib.ggml_map_custom1
ggml_map_custom1.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ggml_custom1_op_t,
    ctypes.c_int,
    ctypes.c_void_p,
]
ggml_map_custom1.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_map_custom1_inplace(
#         struct ggml_context   * ctx,
#         struct ggml_tensor    * a,
#         ggml_custom1_op_t       fun,
#         int                     n_tasks,
#         void                  * userdata);
def ggml_map_custom1_inplace(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    fun: CtypesFuncPointer,  # type: ignore
    n_tasks: Union[ctypes.c_int, int],
    userdata: Union[ctypes.c_void_p, int, None],
) -> ggml_tensor_p:
    ...


ggml_map_custom1_inplace = lib.ggml_map_custom1_inplace
ggml_map_custom1_inplace.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ggml_custom1_op_t,
    ctypes.c_int,
    ctypes.c_void_p,
]
ggml_map_custom1_inplace.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_map_custom2(
#         struct ggml_context   * ctx,
#         struct ggml_tensor    * a,
#         struct ggml_tensor    * b,
#         ggml_custom2_op_t       fun,
#         int                     n_tasks,
#         void                  * userdata);
def ggml_map_custom2(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    b: ggml_tensor_p,
    fun: CtypesFuncPointer,  # type: ignore
    n_tasks: Union[ctypes.c_int, int],
    userdata: Union[ctypes.c_void_p, int, None],
) -> ggml_tensor_p:
    ...


ggml_map_custom2 = lib.ggml_map_custom2
ggml_map_custom2.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ggml_custom2_op_t,
    ctypes.c_int,
    ctypes.c_void_p,
]
ggml_map_custom2.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_map_custom2_inplace(
#         struct ggml_context   * ctx,
#         struct ggml_tensor    * a,
#         struct ggml_tensor    * b,
#         ggml_custom2_op_t       fun,
#         int                     n_tasks,
#         void                  * userdata);
def ggml_map_custom2_inplace(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    b: ggml_tensor_p,
    fun: CtypesFuncPointer,  # type: ignore
    n_tasks: Union[ctypes.c_int, int],
    userdata: Union[ctypes.c_void_p, int, None],
) -> ggml_tensor_p:
    ...


ggml_map_custom2_inplace = lib.ggml_map_custom2_inplace
ggml_map_custom2_inplace.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ggml_custom2_op_t,
    ctypes.c_int,
    ctypes.c_void_p,
]
ggml_map_custom2_inplace.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_map_custom3(
#         struct ggml_context   * ctx,
#         struct ggml_tensor    * a,
#         struct ggml_tensor    * b,
#         struct ggml_tensor    * c,
#         ggml_custom3_op_t       fun,
#         int                     n_tasks,
#         void                  * userdata);
def ggml_map_custom3(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    b: ggml_tensor_p,
    c: ggml_tensor_p,
    fun: CtypesFuncPointer,  # type: ignore
    n_tasks: Union[ctypes.c_int, int],
    userdata: Union[ctypes.c_void_p, int, None],
) -> ggml_tensor_p:
    ...


ggml_map_custom3 = lib.ggml_map_custom3
ggml_map_custom3.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ggml_custom3_op_t,
    ctypes.c_int,
    ctypes.c_void_p,
]
ggml_map_custom3.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_map_custom3_inplace(
#         struct ggml_context   * ctx,
#         struct ggml_tensor    * a,
#         struct ggml_tensor    * b,
#         struct ggml_tensor    * c,
#         ggml_custom3_op_t       fun,
#         int                     n_tasks,
#         void                  * userdata);
def ggml_map_custom3_inplace(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    b: ggml_tensor_p,
    c: ggml_tensor_p,
    fun: CtypesFuncPointer,  # type: ignore
    n_tasks: Union[ctypes.c_int, int],
    userdata: Union[ctypes.c_void_p, int, None],
) -> ggml_tensor_p:
    ...


ggml_map_custom3_inplace = lib.ggml_map_custom3_inplace
ggml_map_custom3_inplace.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ggml_custom3_op_t,
    ctypes.c_int,
    ctypes.c_void_p,
]
ggml_map_custom3_inplace.restype = ctypes.POINTER(ggml_tensor)

# // loss function


# GGML_API struct ggml_tensor * ggml_cross_entropy_loss(
#         struct ggml_context         * ctx,
#         struct ggml_tensor          * a,
#         struct ggml_tensor          * b);
def ggml_cross_entropy_loss(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    b: ggml_tensor_p,
) -> ggml_tensor_p:
    ...


ggml_cross_entropy_loss = lib.ggml_cross_entropy_loss
ggml_cross_entropy_loss.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
]
ggml_cross_entropy_loss.restype = ctypes.POINTER(ggml_tensor)


# GGML_API struct ggml_tensor * ggml_cross_entropy_loss_back(
#         struct ggml_context         * ctx,
#         struct ggml_tensor          * a,
#         struct ggml_tensor          * b,
#         struct ggml_tensor          * c);
def ggml_cross_entropy_loss_back(
    ctx: ggml_context_p,
    a: ggml_tensor_p,
    b: ggml_tensor_p,
    c: ggml_tensor_p,
) -> ggml_tensor_p:
    ...


ggml_cross_entropy_loss_back = lib.ggml_cross_entropy_loss_back
ggml_cross_entropy_loss_back.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
]
ggml_cross_entropy_loss_back.restype = ctypes.POINTER(ggml_tensor)

# //
# // automatic differentiation
# //


# GGML_API void ggml_set_param(
#         struct ggml_context * ctx,
#         struct ggml_tensor  * tensor);
def ggml_set_param(ctx: ggml_context_p, tensor: ggml_tensor_p):
    ...


ggml_set_param = lib.ggml_set_param
ggml_set_param.argtypes = [ggml_context_p_ctypes, ctypes.POINTER(ggml_tensor)]
ggml_set_param.restype = None


# GGML_API void ggml_build_forward_expand (struct ggml_cgraph * cgraph, struct ggml_tensor * tensor);
def ggml_build_forward_expand(
    cgraph: ggml_cgraph_p,
    tensor: ggml_tensor_p,
):
    """Add a tensor to the forward computation graph. This is used to
    compute and save the value of the tensor.

    Parameters:
        cgraph: The graph.
        tensor: The tensor."""
    ...


ggml_build_forward_expand = lib.ggml_build_forward_expand
ggml_build_forward_expand.argtypes = [
    ctypes.POINTER(ggml_cgraph),
    ctypes.POINTER(ggml_tensor),
]
ggml_build_forward_expand.restype = None


# GGML_API void ggml_build_backward_expand(struct ggml_context * ctx, struct ggml_cgraph * gf, struct ggml_cgraph * gb, bool keep);
def ggml_build_backward_expand(
    ctx: ggml_context_p,
    gf: ggml_cgraph_p,
    gb: ggml_cgraph_p,
    keep: Union[ctypes.c_bool, bool],
):
    """Add a tensor to the backward computation graph. This is used to
    compute the gradient of the tensor.

    Parameters:
        ctx: The context.
        gf: The forward graph.
        gb: The backward graph.
        keep: Whether to keep the tensor."""
    ...


ggml_build_backward_expand = lib.ggml_build_backward_expand
ggml_build_backward_expand.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_cgraph),
    ctypes.POINTER(ggml_cgraph),
    ctypes.c_bool,
]
ggml_build_backward_expand.restype = None


# // graph allocation in a context
# GGML_API struct ggml_cgraph * ggml_new_graph         (struct ggml_context * ctx); // size = GGML_DEFAULT_GRAPH_SIZE, grads = false
def ggml_new_graph(ctx: ggml_context_p) -> ggml_cgraph_p:
    """Create a new graph.

    Parameters:
        ctx: The context.

    Returns:
        The graph."""
    ...


ggml_new_graph = lib.ggml_new_graph
ggml_new_graph.argtypes = [ggml_context_p_ctypes]
ggml_new_graph.restype = ctypes.POINTER(ggml_cgraph)


# GGML_API struct ggml_cgraph * ggml_new_graph_custom  (struct ggml_context * ctx, size_t size, bool grads);
def ggml_new_graph_custom(
    ctx: ggml_context_p,
    size: Union[ctypes.c_size_t, int],
    grads: Union[ctypes.c_bool, bool],
) -> ggml_cgraph_p:
    """Create a new graph with custom size and grads.

    Parameters:
        ctx: The context.
        size: The size of the graph.
        grads: Whether to keep the gradients.

    Returns:
        The graph."""
    ...


ggml_new_graph_custom = lib.ggml_new_graph_custom
ggml_new_graph_custom.argtypes = [ggml_context_p_ctypes, ctypes.c_size_t, ctypes.c_bool]
ggml_new_graph_custom.restype = ctypes.POINTER(ggml_cgraph)


# GGML_API struct ggml_cgraph * ggml_graph_dup         (struct ggml_context * ctx, struct ggml_cgraph * cgraph);
def ggml_graph_dup(
    ctx: ggml_context_p,
    cgraph: ggml_cgraph_p,
) -> ggml_cgraph_p:
    """Duplicate a graph.

    Parameters:
        ctx: The context.
        cgraph: The graph.

    Returns:
        The graph."""
    ...


ggml_graph_dup = lib.ggml_graph_dup
ggml_graph_dup.argtypes = [ggml_context_p_ctypes, ctypes.POINTER(ggml_cgraph)]
ggml_graph_dup.restype = ctypes.POINTER(ggml_cgraph)


# GGML_API struct ggml_cgraph   ggml_graph_view        (struct ggml_cgraph * cgraph, int i0, int i1);
def ggml_graph_view(
    cgraph: ggml_cgraph_p,
    i0: Union[ctypes.c_int, int],
    i1: Union[ctypes.c_int, int],
) -> ggml_cgraph:
    """View a graph.

    Parameters:
        cgraph: The graph.
        i0: The start index.
        i1: The end index.

    Returns:
        The graph."""
    ...


ggml_graph_view = lib.ggml_graph_view
ggml_graph_view.argtypes = [ctypes.POINTER(ggml_cgraph), ctypes.c_int, ctypes.c_int]
ggml_graph_view.restype = ggml_cgraph


# GGML_API void                 ggml_graph_cpy         (struct ggml_cgraph * src, struct ggml_cgraph * dst);
def ggml_graph_cpy(
    src: ggml_cgraph_p,
    dst: ggml_cgraph_p,
):
    """Copy a graph.

    Parameters:
        src: The source graph.
        dst: The destination graph."""
    ...


ggml_graph_cpy = lib.ggml_graph_cpy
ggml_graph_cpy.argtypes = [ctypes.POINTER(ggml_cgraph), ctypes.POINTER(ggml_cgraph)]
ggml_graph_cpy.restype = None


# GGML_API void                 ggml_graph_reset       (struct ggml_cgraph * cgraph);  // zero grads
def ggml_graph_reset(
    cgraph: ggml_cgraph_p,
):
    """Reset a graph.

    Parameters:
        cgraph: The graph."""
    ...


ggml_graph_reset = lib.ggml_graph_reset
ggml_graph_reset.argtypes = [ctypes.POINTER(ggml_cgraph)]
ggml_graph_reset.restype = None


# GGML_API void                 ggml_graph_clear       (struct ggml_cgraph * cgraph);
def ggml_graph_clear(
    cgraph: ggml_cgraph_p,
):
    """Clear a graph.

    Parameters:
        cgraph: The graph."""
    ...


ggml_graph_clear = lib.ggml_graph_clear
ggml_graph_clear.argtypes = [ctypes.POINTER(ggml_cgraph)]
ggml_graph_clear.restype = None


# GGML_API size_t ggml_graph_overhead(void);
def ggml_graph_overhead() -> int:
    """Get the overhead of the graph."""
    ...


ggml_graph_overhead = lib.ggml_graph_overhead
ggml_graph_overhead.argtypes = []
ggml_graph_overhead.restype = ctypes.c_size_t


# GGML_API size_t ggml_graph_overhead_custom(size_t size, bool grads);
def ggml_graph_overhead_custom(
    size: Union[ctypes.c_size_t, int],
    grads: Union[ctypes.c_bool, bool],
) -> int:
    ...


ggml_graph_overhead_custom = lib.ggml_graph_overhead_custom
ggml_graph_overhead_custom.argtypes = [ctypes.c_size_t, ctypes.c_bool]
ggml_graph_overhead_custom.restype = ctypes.c_size_t


# // ggml_graph_plan() has to be called before ggml_graph_compute()
# // when plan.work_size > 0, caller must allocate memory for plan.work_data
# GGML_API struct ggml_cplan ggml_graph_plan   (const struct ggml_cgraph * cgraph, int n_threads /*= GGML_DEFAULT_N_THREADS*/);
def ggml_graph_plan(
    cgraph: ggml_cgraph_p,
    n_threads: Union[ctypes.c_int, int] = GGML_DEFAULT_N_THREADS,
) -> ggml_cplan:
    """Plan the computation graph.

    Parameters:
        cgraph: The graph.
        n_threads: The number of threads to use.

    Returns:
        The plan."""
    ...


ggml_graph_plan = lib.ggml_graph_plan
ggml_graph_plan.argtypes = [
    ctypes.POINTER(ggml_cgraph),
    ctypes.c_int,
]
ggml_graph_plan.restype = ggml_cplan


# GGML_API int               ggml_graph_compute(      struct ggml_cgraph * cgraph, struct ggml_cplan * cplan);
def ggml_graph_compute(
    cgraph: ggml_cgraph_p,
    cplan: ggml_cplan_p,
) -> int:
    ...


ggml_graph_compute = lib.ggml_graph_compute
ggml_graph_compute.argtypes = [
    ctypes.POINTER(ggml_cgraph),
    ctypes.POINTER(ggml_cplan),
]
ggml_graph_compute.restype = ctypes.c_int


# // same as ggml_graph_compute() but the work data is allocated as a part of the context
# // note: the drawback of this API is that you must have ensured that the context has enough memory for the work data
# GGML_API void ggml_graph_compute_with_ctx(struct ggml_context * ctx, struct ggml_cgraph * cgraph, int n_threads);
def ggml_graph_compute_with_ctx(
    ctx: ggml_context_p,
    cgraph: ggml_cgraph_p,
    n_threads: Union[ctypes.c_int, int],
):
    """Compute the graph with a context.

    Parameters:
        ctx: The context.
        cgraph: The graph.
        n_threads: The number of threads to use."""
    ...


ggml_graph_compute_with_ctx = lib.ggml_graph_compute_with_ctx
ggml_graph_compute_with_ctx.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_cgraph),
    ctypes.c_int,
]
ggml_graph_compute_with_ctx.restype = None


# GGML_API struct ggml_tensor * ggml_graph_get_tensor(struct ggml_cgraph * cgraph, const char * name);
def ggml_graph_get_tensor(
    cgraph: ggml_cgraph_p,
    name: bytes,
) -> ggml_tensor_p:
    """Get a tensor from the graph by name.

    Parameters:
        cgraph: The graph.
        name: The name of the tensor.

    Returns:
        The tensor."""
    ...


ggml_graph_get_tensor = lib.ggml_graph_get_tensor
ggml_graph_get_tensor.argtypes = [
    ctypes.POINTER(ggml_cgraph),
    ctypes.c_char_p,
]
ggml_graph_get_tensor.restype = ctypes.POINTER(ggml_tensor)


# GGML_API void                 ggml_graph_export(const struct ggml_cgraph * cgraph, const char * fname);
def ggml_graph_export(
    cgraph: ggml_cgraph_p,
    fname: bytes,
):
    ...


ggml_graph_export = lib.ggml_graph_export
ggml_graph_export.argtypes = [
    ctypes.POINTER(ggml_cgraph),
    ctypes.c_char_p,
]
ggml_graph_export.restype = None


# GGML_API struct ggml_cgraph * ggml_graph_import(const char * fname, struct ggml_context ** ctx_data, struct ggml_context ** ctx_eval);
def ggml_graph_import(
    fname: bytes,
    ctx_data: "ctypes._Pointer[ggml_context_p]",  # type: ignore
    ctx_eval: "ctypes._Pointer[ggml_context_p]",  # type: ignore
) -> ggml_cgraph_p:
    ...


ggml_graph_import = lib.ggml_graph_import
ggml_graph_import.argtypes = [
    ctypes.c_char_p,
    ctypes.POINTER(ggml_context_p_ctypes),
    ctypes.POINTER(ggml_context_p_ctypes),
]
ggml_graph_import.restype = ctypes.POINTER(ggml_cgraph)


# // print info and performance information for the graph
# GGML_API void ggml_graph_print(const struct ggml_cgraph * cgraph);
def ggml_graph_print(
    cgraph: ggml_cgraph_p,
):
    ...


ggml_graph_print = lib.ggml_graph_print
ggml_graph_print.argtypes = [ctypes.POINTER(ggml_cgraph)]
ggml_graph_print.restype = None


# // dump the graph into a file using the dot format
# GGML_API void ggml_graph_dump_dot(const struct ggml_cgraph * gb, const struct ggml_cgraph * gf, const char * filename);
def ggml_graph_dump_dot(
    gb: ggml_cgraph_p,
    gf: ggml_cgraph_p,
    filename: bytes,
):
    ...


ggml_graph_dump_dot = lib.ggml_graph_dump_dot
ggml_graph_dump_dot.argtypes = [
    ctypes.POINTER(ggml_cgraph),
    ctypes.POINTER(ggml_cgraph),
    ctypes.c_char_p,
]
ggml_graph_dump_dot.restype = None


# // build gradient checkpointing backward graph gb for gf using provided checkpoints
# // gb_tmp will contain original backward graph with rewritten backward process nodes,
# // but without the second forward pass nodes.
# GGML_API void ggml_build_backward_gradient_checkpointing(
#         struct ggml_context   * ctx,
#         struct ggml_cgraph    * gf,
#         struct ggml_cgraph    * gb,
#         struct ggml_cgraph    * gb_tmp,
#         struct ggml_tensor  * * checkpoints,
#         int                     n_checkpoints);
def ggml_build_backward_gradient_checkpointing(
    ctx: ggml_context_p,
    gf: ggml_cgraph_p,
    gb: ggml_cgraph_p,
    gb_tmp: ggml_cgraph_p,
    checkpoints: "ctypes._Pointer[ggml_tensor_p]",  # type: ignore
    n_checkpoints: Union[ctypes.c_int, int],
):
    ...


ggml_build_backward_gradient_checkpointing = (
    lib.ggml_build_backward_gradient_checkpointing
)
ggml_build_backward_gradient_checkpointing.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_cgraph),
    ctypes.POINTER(ggml_cgraph),
    ctypes.POINTER(ggml_cgraph),
    ctypes.POINTER(ctypes.POINTER(ggml_tensor)),
    ctypes.c_int,
]
ggml_build_backward_gradient_checkpointing.restype = None


# //
# // optimization
# //

# // optimization methods
# enum ggml_opt_type {
#     GGML_OPT_ADAM,
#     GGML_OPT_LBFGS,
# };
GGML_OPT_ADAM = 0
GGML_OPT_LBFGS = 1

# // linesearch methods
# enum ggml_linesearch {
#     GGML_LINESEARCH_DEFAULT = 1,

#     GGML_LINESEARCH_BACKTRACKING_ARMIJO       = 0,
#     GGML_LINESEARCH_BACKTRACKING_WOLFE        = 1,
#     GGML_LINESEARCH_BACKTRACKING_STRONG_WOLFE = 2,
# };
GGML_LINESEARCH_DEFAULT = 1
GGML_LINESEARCH_BACKTRACKING_ARMIJO = 0
GGML_LINESEARCH_BACKTRACKING_WOLFE = 1
GGML_LINESEARCH_BACKTRACKING_STRONG_WOLFE = 2

# // optimization return values
# enum ggml_opt_result {
#     GGML_OPT_OK = 0,
#     GGML_OPT_DID_NOT_CONVERGE,
#     GGML_OPT_NO_CONTEXT,
#     GGML_OPT_INVALID_WOLFE,
#     GGML_OPT_FAIL,
#     GGML_OPT_CANCEL,

#     GGML_LINESEARCH_FAIL = -128,
#     GGML_LINESEARCH_MINIMUM_STEP,
#     GGML_LINESEARCH_MAXIMUM_STEP,
#     GGML_LINESEARCH_MAXIMUM_ITERATIONS,
#     GGML_LINESEARCH_INVALID_PARAMETERS,
# };
GGML_OPT_OK = 0
GGML_OPT_DID_NOT_CONVERGE = 1
GGML_OPT_NO_CONTEXT = 2
GGML_OPT_INVALID_WOLFE = 3
GGML_OPT_FAIL = 4
GGML_OPT_CANCEL = 5
GGML_LINESEARCH_FAIL = -128
GGML_LINESEARCH_MINIMUM_STEP = -127
GGML_LINESEARCH_MAXIMUM_STEP = -126
GGML_LINESEARCH_MAXIMUM_ITERATIONS = -125
GGML_LINESEARCH_INVALID_PARAMETERS = -124

# typedef void (*ggml_opt_callback)(void * data, int accum_step, float * sched, bool * cancel);
ggml_opt_callback = ctypes.CFUNCTYPE(
    None,
    ctypes.c_void_p,
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_float),
    ctypes.POINTER(ctypes.c_bool),
)

# typedef void (*ggml_log_callback)(enum ggml_log_level level, const char * text, void * user_data);
ggml_log_callback = ctypes.CFUNCTYPE(
    None, ctypes.c_int, ctypes.c_char_p, ctypes.c_void_p
)

# // optimization parameters
# //
# //   see ggml.c (ggml_opt_default_params) for default values
# //
# struct ggml_opt_params {
#     enum ggml_opt_type type;

#     size_t graph_size;

#     int n_threads;

#     // delta-based convergence test
#     //
#     //   if past == 0 - disabled
#     //   if past > 0:
#     //     stop if |f(x) - f(x_past)| < delta * max(1, |f(x)|)
#     //
#     int past;
#     float delta;

#     // maximum number of iterations without improvement
#     //
#     //   if 0 - disabled
#     //   if > 0:
#     //     assume convergence if no cost improvement in this number of iterations
#     //
#     int max_no_improvement;

#     bool print_forward_graph;
#     bool print_backward_graph;

#     int n_gradient_accumulation;

#     // ADAM parameters
#     struct {
#         int n_iter;

#         float sched; // schedule multiplier (fixed, decay or warmup)
#         float decay; // weight decay for AdamW, use 0.0f to disable
#         int   decay_min_ndim; // minimum number of tensor dimension to apply weight decay
#         float alpha; // learning rate
#         float beta1;
#         float beta2;
#         float eps;   // epsilon for numerical stability
#         float eps_f; // epsilon for convergence test
#         float eps_g; // epsilon for convergence test
#         float gclip; // gradient clipping
#     } adam;

#     // LBFGS parameters
#     struct {
#         int m; // number of corrections to approximate the inv. Hessian
#         int n_iter;
#         int max_linesearch;

#         float eps;      // convergence tolerance
#         float ftol;     // line search tolerance
#         float wolfe;
#         float min_step;
#         float max_step;

#         enum ggml_linesearch linesearch;
#     } lbfgs;
# };


class ggml_opt_params_adam(ctypes.Structure):
    _fields_ = [
        ("n_iter", ctypes.c_int),
        ("sched", ctypes.c_float),
        ("decay", ctypes.c_float),
        ("decay_min_ndim", ctypes.c_int),
        ("alpha", ctypes.c_float),
        ("beta1", ctypes.c_float),
        ("beta2", ctypes.c_float),
        ("eps", ctypes.c_float),
        ("eps_f", ctypes.c_float),
        ("eps_g", ctypes.c_float),
        ("gclip", ctypes.c_float),
    ]


class ggml_opt_params_lbfgs(ctypes.Structure):
    _fields_ = [
        ("m", ctypes.c_int),
        ("n_iter", ctypes.c_int),
        ("max_linesearch", ctypes.c_int),
        ("eps", ctypes.c_float),
        ("ftol", ctypes.c_float),
        ("wolfe", ctypes.c_float),
        ("min_step", ctypes.c_float),
        ("max_step", ctypes.c_float),
        ("linesearch", ctypes.c_int),
    ]


class ggml_opt_params(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_int),
        ("graph_size", ctypes.c_size_t),
        ("n_threads", ctypes.c_int),
        ("past", ctypes.c_int),
        ("delta", ctypes.c_float),
        ("max_no_improvement", ctypes.c_int),
        ("print_forward_graph", ctypes.c_bool),
        ("print_backward_graph", ctypes.c_bool),
        ("n_gradient_accumulation", ctypes.c_int),
        ("adam", ggml_opt_params_adam),
        ("lbfgs", ggml_opt_params_lbfgs),
    ]


# struct ggml_opt_context {
#     struct ggml_context * ctx;
#     struct ggml_opt_params params;

#     int iter;
#     int64_t nx; // number of parameter elements

#     bool just_initialized;

#     float loss_before;
#     float loss_after;

#     struct {
#         struct ggml_tensor * g;  // current gradient
#         struct ggml_tensor * m;  // first moment
#         struct ggml_tensor * v;  // second moment
#         struct ggml_tensor * pf; // past function values
#         float fx_best;
#         float fx_prev;
#         int n_no_improvement;
#     } adam;

#     struct {
#         struct ggml_tensor * x;    // current parameters
#         struct ggml_tensor * xp;   // previous parameters
#         struct ggml_tensor * g;    // current gradient
#         struct ggml_tensor * gp;   // previous gradient
#         struct ggml_tensor * d;    // search direction
#         struct ggml_tensor * pf;   // past function values
#         struct ggml_tensor * lmal; // the L-BFGS memory alpha
#         struct ggml_tensor * lmys; // the L-BFGS memory ys
#         struct ggml_tensor * lms;  // the L-BFGS memory s
#         struct ggml_tensor * lmy;  // the L-BFGS memory y
#         float fx_best;
#         float step;
#         int j;
#         int k;
#         int end;
#         int n_no_improvement;
#     } lbfgs;
# };


class ggml_opt_context_adam(ctypes.Structure):
    _fields_ = [
        ("g", ctypes.POINTER(ggml_tensor)),
        ("m", ctypes.POINTER(ggml_tensor)),
        ("v", ctypes.POINTER(ggml_tensor)),
        ("pf", ctypes.POINTER(ggml_tensor)),
        ("fx_best", ctypes.c_float),
        ("fx_prev", ctypes.c_float),
        ("n_no_improvement", ctypes.c_int),
    ]


class ggml_opt_context_lbfgs(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.POINTER(ggml_tensor)),
        ("xp", ctypes.POINTER(ggml_tensor)),
        ("g", ctypes.POINTER(ggml_tensor)),
        ("gp", ctypes.POINTER(ggml_tensor)),
        ("d", ctypes.POINTER(ggml_tensor)),
        ("pf", ctypes.POINTER(ggml_tensor)),
        ("lmal", ctypes.POINTER(ggml_tensor)),
        ("lmys", ctypes.POINTER(ggml_tensor)),
        ("lms", ctypes.POINTER(ggml_tensor)),
        ("lmy", ctypes.POINTER(ggml_tensor)),
        ("fx_best", ctypes.c_float),
        ("step", ctypes.c_float),
        ("j", ctypes.c_int),
        ("k", ctypes.c_int),
        ("end", ctypes.c_int),
        ("n_no_improvement", ctypes.c_int),
    ]


class ggml_opt_context(ctypes.Structure):
    _fields_ = [
        ("ctx", ggml_context_p_ctypes),
        ("params", ggml_opt_params),
        ("iter", ctypes.c_int),
        ("nx", ctypes.c_int64),
        ("just_initialized", ctypes.c_bool),
        ("loss_before", ctypes.c_float),
        ("loss_after", ctypes.c_float),
        ("adam", ggml_opt_context_adam),
        ("lbfgs", ggml_opt_context_lbfgs),
    ]


ggml_opt_context_p = ctypes.POINTER(ggml_opt_context)


# GGML_API struct ggml_opt_params ggml_opt_default_params(enum ggml_opt_type type);
def ggml_opt_default_params(type: Union[ctypes.c_int, bool]) -> ggml_opt_params:
    ...


ggml_opt_default_params = lib.ggml_opt_default_params
ggml_opt_default_params.argtypes = [ctypes.c_int]
ggml_opt_default_params.restype = ggml_opt_params


# // optimize the function defined by the tensor f
# GGML_API enum ggml_opt_result ggml_opt(
#         struct ggml_context * ctx,
#         struct ggml_opt_params params,
#         struct ggml_tensor * f);
def ggml_opt(
    ctx: ggml_context_p,
    params: ggml_opt_params,
    f: ggml_tensor_p,
) -> int:
    ...


ggml_opt = lib.ggml_opt
ggml_opt.argtypes = [
    ggml_context_p_ctypes,
    ggml_opt_params,
    ctypes.POINTER(ggml_tensor),
]
ggml_opt.restype = ctypes.c_int


# // initialize optimizer context
# GGML_API void ggml_opt_init(
#         struct ggml_context     * ctx,
#         struct ggml_opt_context * opt,
#         struct ggml_opt_params    params,
#         int64_t                   nx);
def ggml_opt_init(
    ctx: ggml_context_p,
    opt: "ctypes._Pointer[ggml_opt_context]",  # type: ignore
    params: ggml_opt_params,
    nx: Union[ctypes.c_int64, int],
):
    ...


ggml_opt_init = lib.ggml_opt_init
ggml_opt_init.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_opt_context),
    ggml_opt_params,
    ctypes.c_int64,
]
ggml_opt_init.restype = None


# // continue optimizing the function defined by the tensor f
# GGML_API enum ggml_opt_result ggml_opt_resume(
#         struct ggml_context * ctx,
#         struct ggml_opt_context * opt,
#         struct ggml_tensor * f);
def ggml_opt_resume(
    ctx: ggml_context_p,
    opt: "ctypes._Pointer[ggml_opt_context]",  # type: ignore
    f: ggml_tensor_p,
) -> int:
    ...


ggml_opt_resume = lib.ggml_opt_resume
ggml_opt_resume.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_opt_context),
    ctypes.POINTER(ggml_tensor),
]
ggml_opt_resume.restype = ctypes.c_int


# // continue optimizing the function defined by the tensor f
# GGML_API enum ggml_opt_result ggml_opt_resume_g(
#         struct ggml_context * ctx,
#         struct ggml_opt_context * opt,
#         struct ggml_tensor * f,
#         struct ggml_cgraph * gf,
#         struct ggml_cgraph * gb,
#         ggml_opt_callback callback,
#         void * callback_data);
def ggml_opt_resume_g(
    ctx: ggml_context_p,
    opt: "ctypes._Pointer[ggml_opt_context]",  # type: ignore
    f: ggml_tensor_p,
    gf: ggml_cgraph_p,
    gb: ggml_cgraph_p,
    callback: "ctypes._CFuncPtr[None, ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_bool)]",  # type: ignore
    callback_data: Union[ctypes.c_void_p, int, None],
) -> int:
    ...


ggml_opt_resume_g = lib.ggml_opt_resume_g
ggml_opt_resume_g.argtypes = [
    ggml_context_p_ctypes,
    ctypes.POINTER(ggml_opt_context),
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_cgraph),
    ctypes.POINTER(ggml_cgraph),
    ggml_opt_callback,
    ctypes.c_void_p,
]
ggml_opt_resume_g.restype = ctypes.c_int


# //
# // tensor flags
# //
# GGML_API void ggml_set_input(struct ggml_tensor * tensor);
def ggml_set_input(tensor: ggml_tensor_p):
    ...


ggml_set_input = lib.ggml_set_input
ggml_set_input.argtypes = [ctypes.POINTER(ggml_tensor)]
ggml_set_input.restype = None


# GGML_API void ggml_set_output(struct ggml_tensor * tensor);
def ggml_set_output(tensor: ggml_tensor_p):
    ...


ggml_set_output = lib.ggml_set_output
ggml_set_output.argtypes = [ctypes.POINTER(ggml_tensor)]
ggml_set_output.restype = None


# //
# // quantization
# //


# // - ggml_quantize_init can be called multiple times with the same type
# //   it will only initialize the quantization tables for the first call or after ggml_quantize_free
# //   automatically called by ggml_quantize_chunk for convenience
# //
# // - ggml_quantize_free will free any memory allocated by ggml_quantize_init
# //   call this at the end of the program to avoid memory leaks
# //
# // note: these are thread-safe
# //
# GGML_API void ggml_quantize_init(enum ggml_type type);
def ggml_quantize_init(type: Union[ctypes.c_int, int]):
    ...


ggml_quantize_init = lib.ggml_quantize_init
ggml_quantize_init.argtypes = [ctypes.c_int]
ggml_quantize_init.restype = None


# GGML_API void ggml_quantize_free(void);
def ggml_quantize_free():
    ...


ggml_quantize_free = lib.ggml_quantize_free
ggml_quantize_free.argtypes = []
ggml_quantize_free.restype = None


# // TODO: these would probably get removed in favor of the more general ggml_quantize_chunk
# GGML_API size_t ggml_quantize_q4_0(const float * src, void * dst, int n, int k, int64_t * hist);
def ggml_quantize_q4_0(
    src: CtypesArray[ctypes.c_float],
    dst: Union[ctypes.c_void_p, int, None],
    n: Union[ctypes.c_int, int],
    k: Union[ctypes.c_int, int],
    hist: CtypesArray[ctypes.c_int64],
) -> int:
    ...


ggml_quantize_q4_0 = lib.ggml_quantize_q4_0
ggml_quantize_q4_0.argtypes = [
    ctypes.POINTER(ctypes.c_float),
    ctypes.c_void_p,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_int64),
]
ggml_quantize_q4_0.restype = ctypes.c_size_t


# GGML_API size_t ggml_quantize_q4_1(const float * src, void * dst, int n, int k, int64_t * hist);
def ggml_quantize_q4_1(
    src: CtypesArray[ctypes.c_float],
    dst: Union[ctypes.c_void_p, int, None],
    n: Union[ctypes.c_int, int],
    k: Union[ctypes.c_int, int],
    hist: CtypesArray[ctypes.c_int64],
) -> int:
    ...


ggml_quantize_q4_1 = lib.ggml_quantize_q4_1
ggml_quantize_q4_1.argtypes = [
    ctypes.POINTER(ctypes.c_float),
    ctypes.c_void_p,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_int64),
]
ggml_quantize_q4_1.restype = ctypes.c_size_t


# GGML_API size_t ggml_quantize_q5_0(const float * src, void * dst, int n, int k, int64_t * hist);
def ggml_quantize_q5_0(
    src: CtypesArray[ctypes.c_float],
    dst: Union[ctypes.c_void_p, int, None],
    n: Union[ctypes.c_int, int],
    k: Union[ctypes.c_int, int],
    hist: CtypesArray[ctypes.c_int64],
) -> int:
    ...


ggml_quantize_q5_0 = lib.ggml_quantize_q5_0
ggml_quantize_q5_0.argtypes = [
    ctypes.POINTER(ctypes.c_float),
    ctypes.c_void_p,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_int64),
]
ggml_quantize_q5_0.restype = ctypes.c_size_t


# GGML_API size_t ggml_quantize_q5_1(const float * src, void * dst, int n, int k, int64_t * hist);
def ggml_quantize_q5_1(
    src: CtypesArray[ctypes.c_float],
    dst: Union[ctypes.c_void_p, int, None],
    n: Union[ctypes.c_int, int],
    k: Union[ctypes.c_int, int],
    hist: CtypesArray[ctypes.c_int64],
) -> int:
    ...


ggml_quantize_q5_1 = lib.ggml_quantize_q5_1
ggml_quantize_q5_1.argtypes = [
    ctypes.POINTER(ctypes.c_float),
    ctypes.c_void_p,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_int64),
]
ggml_quantize_q5_1.restype = ctypes.c_size_t


# GGML_API size_t ggml_quantize_q8_0(const float * src, void * dst, int n, int k, int64_t * hist);
def ggml_quantize_q8_0(
    src: CtypesArray[ctypes.c_float],
    dst: Union[ctypes.c_void_p, int, None],
    n: Union[ctypes.c_int, int],
    k: Union[ctypes.c_int, int],
    hist: CtypesArray[ctypes.c_int64],
) -> int:
    ...


ggml_quantize_q8_0 = lib.ggml_quantize_q8_0
ggml_quantize_q8_0.argtypes = [
    ctypes.POINTER(ctypes.c_float),
    ctypes.c_void_p,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_int64),
]
ggml_quantize_q8_0.restype = ctypes.c_size_t


# GGML_API size_t ggml_quantize_q2_K(const float * src, void * dst, int n, int k, int64_t * hist);
def ggml_quantize_q2_K(
    src: CtypesArray[ctypes.c_float],
    dst: Union[ctypes.c_void_p, int, None],
    n: Union[ctypes.c_int, int],
    k: Union[ctypes.c_int, int],
    hist: CtypesArray[ctypes.c_int64],
) -> int:
    ...


ggml_quantize_q2_K = lib.ggml_quantize_q2_K
ggml_quantize_q2_K.argtypes = [
    ctypes.POINTER(ctypes.c_float),
    ctypes.c_void_p,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_int64),
]
ggml_quantize_q2_K.restype = ctypes.c_size_t


# GGML_API size_t ggml_quantize_q3_K(const float * src, void * dst, int n, int k, int64_t * hist);
def ggml_quantize_q3_K(
    src: CtypesArray[ctypes.c_float],
    dst: Union[ctypes.c_void_p, int, None],
    n: Union[ctypes.c_int, int],
    k: Union[ctypes.c_int, int],
    hist: CtypesArray[ctypes.c_int64],
) -> int:
    ...


ggml_quantize_q3_K = lib.ggml_quantize_q3_K
ggml_quantize_q3_K.argtypes = [
    ctypes.POINTER(ctypes.c_float),
    ctypes.c_void_p,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_int64),
]
ggml_quantize_q3_K.restype = ctypes.c_size_t


# GGML_API size_t ggml_quantize_q4_K(const float * src, void * dst, int n, int k, int64_t * hist);
def ggml_quantize_q4_K(
    src: CtypesArray[ctypes.c_float],
    dst: Union[ctypes.c_void_p, int, None],
    n: Union[ctypes.c_int, int],
    k: Union[ctypes.c_int, int],
    hist: CtypesArray[ctypes.c_int64],
) -> int:
    ...


ggml_quantize_q4_K = lib.ggml_quantize_q4_K
ggml_quantize_q4_K.argtypes = [
    ctypes.POINTER(ctypes.c_float),
    ctypes.c_void_p,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_int64),
]
ggml_quantize_q4_K.restype = ctypes.c_size_t


# GGML_API size_t ggml_quantize_q5_K(const float * src, void * dst, int n, int k, int64_t * hist);
def ggml_quantize_q5_K(
    src: CtypesArray[ctypes.c_float],
    dst: Union[ctypes.c_void_p, int, None],
    n: Union[ctypes.c_int, int],
    k: Union[ctypes.c_int, int],
    hist: CtypesArray[ctypes.c_int64],
) -> int:
    ...


ggml_quantize_q5_K = lib.ggml_quantize_q5_K
ggml_quantize_q5_K.argtypes = [
    ctypes.POINTER(ctypes.c_float),
    ctypes.c_void_p,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_int64),
]
ggml_quantize_q5_K.restype = ctypes.c_size_t


# GGML_API size_t ggml_quantize_q6_K(const float * src, void * dst, int n, int k, int64_t * hist);
def ggml_quantize_q6_K(
    src: CtypesArray[ctypes.c_float],
    dst: Union[ctypes.c_void_p, int, None],
    n: Union[ctypes.c_int, int],
    k: Union[ctypes.c_int, int],
    hist: CtypesArray[ctypes.c_int64],
) -> int:
    ...


ggml_quantize_q6_K = lib.ggml_quantize_q6_K
ggml_quantize_q6_K.argtypes = [
    ctypes.POINTER(ctypes.c_float),
    ctypes.c_void_p,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_int64),
]
ggml_quantize_q6_K.restype = ctypes.c_size_t


# // some quantization type cannot be used without an importance matrix
# GGML_API bool ggml_quantize_requires_imatrix(enum ggml_type type);
def ggml_quantize_requires_imatrix(
    type: Union[ctypes.c_int, int],
) -> bool:
    ...


ggml_quantize_requires_imatrix = lib.ggml_quantize_requires_imatrix
ggml_quantize_requires_imatrix.argtypes = [
    ctypes.c_int,
]
ggml_quantize_requires_imatrix.restype = ctypes.c_bool


# // calls ggml_quantize_init internally (i.e. can allocate memory)
# GGML_API size_t ggml_quantize_chunk(enum ggml_type type, const float * src, void * dst,
#         int start, int nrows, int n_per_row, int64_t * hist, const float * imatrix);
def ggml_quantize_chunk(
    type: Union[ctypes.c_int, int],
    src: CtypesArray[ctypes.c_float],
    dst: Union[ctypes.c_void_p, int, None],
    start: Union[ctypes.c_int, int],
    nrows: Union[ctypes.c_int, int],
    n_per_row: Union[ctypes.c_int, int],
    hist: CtypesArray[ctypes.c_int64],
    imatrix: CtypesArray[ctypes.c_float],
) -> int:
    ...


ggml_quantize_chunk = lib.ggml_quantize_chunk
ggml_quantize_chunk.argtypes = [
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_float),
    ctypes.c_void_p,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_int64),
    ctypes.POINTER(ctypes.c_float),
]
ggml_quantize_chunk.restype = ctypes.c_size_t


# //
# // gguf
# //

# enum gguf_type {
#     GGUF_TYPE_UINT8   = 0,
#     GGUF_TYPE_INT8    = 1,
#     GGUF_TYPE_UINT16  = 2,
#     GGUF_TYPE_INT16   = 3,
#     GGUF_TYPE_UINT32  = 4,
#     GGUF_TYPE_INT32   = 5,
#     GGUF_TYPE_FLOAT32 = 6,
#     GGUF_TYPE_BOOL    = 7,
#     GGUF_TYPE_STRING  = 8,
#     GGUF_TYPE_ARRAY   = 9,
#     GGUF_TYPE_UINT64  = 10,
#     GGUF_TYPE_INT64   = 11,
#     GGUF_TYPE_FLOAT64 = 12,
#     GGUF_TYPE_COUNT,       // marks the end of the enum
# };
GGUF_TYPE_UINT8 = 0
GGUF_TYPE_INT8 = 1
GGUF_TYPE_UINT16 = 2
GGUF_TYPE_INT16 = 3
GGUF_TYPE_UINT32 = 4
GGUF_TYPE_INT32 = 5
GGUF_TYPE_FLOAT32 = 6
GGUF_TYPE_BOOL = 7
GGUF_TYPE_STRING = 8
GGUF_TYPE_ARRAY = 9
GGUF_TYPE_COUNT = 10

# struct gguf_context;
gguf_context_p = NewType("gguf_context_p", int)
gguf_context_p_ctypes = ctypes.c_void_p

# struct gguf_init_params {
#     bool no_alloc;


#     // if not NULL, create a ggml_context and allocate the tensor data in it
#     struct ggml_context ** ctx;
# };
class gguf_init_params(ctypes.Structure):
    _fields_ = [
        ("no_alloc", ctypes.c_bool),
        ("ctx", ctypes.POINTER(ggml_context_p_ctypes)),
    ]


# GGML_API struct gguf_context * gguf_init_empty(void);
def gguf_init_empty() -> Optional[gguf_context_p]:
    ...


gguf_init_empty = lib.gguf_init_empty
gguf_init_empty.argtypes = []
gguf_init_empty.restype = gguf_context_p_ctypes


# GGML_API struct gguf_context * gguf_init_from_file(const char * fname, struct gguf_init_params params);
def gguf_init_from_file(
    fname: bytes,
    params: gguf_init_params,
) -> Optional[gguf_context_p]:
    ...


gguf_init_from_file = lib.gguf_init_from_file
gguf_init_from_file.argtypes = [
    ctypes.c_char_p,
    gguf_init_params,
]
gguf_init_from_file.restype = gguf_context_p_ctypes

# //GGML_API struct gguf_context * gguf_init_from_buffer(..);


# GGML_API void gguf_free(struct gguf_context * ctx);
def gguf_free(
    ctx: gguf_context_p,
):
    ...


gguf_free = lib.gguf_free
gguf_free.argtypes = [
    gguf_context_p_ctypes,
]
gguf_free.restype = None


# GGML_API const char * gguf_type_name(enum gguf_type type);
def gguf_type_name(
    type: Union[ctypes.c_int, int],
) -> bytes:
    ...


gguf_type_name = lib.gguf_type_name
gguf_type_name.argtypes = [
    ctypes.c_int,
]
gguf_type_name.restype = ctypes.c_char_p


# GGML_API int    gguf_get_version    (const struct gguf_context * ctx);
def gguf_get_version(
    ctx: gguf_context_p,
) -> int:
    ...


gguf_get_version = lib.gguf_get_version
gguf_get_version.argtypes = [
    gguf_context_p_ctypes,
]
gguf_get_version.restype = ctypes.c_int


# GGML_API size_t gguf_get_alignment  (const struct gguf_context * ctx);
def gguf_get_alignment(
    ctx: gguf_context_p,
) -> int:
    ...


gguf_get_alignment = lib.gguf_get_alignment
gguf_get_alignment.argtypes = [
    gguf_context_p_ctypes,
]
gguf_get_alignment.restype = ctypes.c_size_t


# GGML_API size_t gguf_get_data_offset(const struct gguf_context * ctx);
def gguf_get_data_offset(
    ctx: gguf_context_p,
) -> int:
    ...


gguf_get_data_offset = lib.gguf_get_data_offset
gguf_get_data_offset.argtypes = [
    gguf_context_p_ctypes,
]
gguf_get_data_offset.restype = ctypes.c_size_t


# GGML_API void * gguf_get_data       (const struct gguf_context * ctx);
def gguf_get_data(
    ctx: gguf_context_p,
) -> Optional[int]:
    ...


gguf_get_data = lib.gguf_get_data
gguf_get_data.argtypes = [
    gguf_context_p_ctypes,
]
gguf_get_data.restype = ctypes.c_void_p


# GGML_API int          gguf_get_n_kv(const struct gguf_context * ctx);
def gguf_get_n_kv(
    ctx: gguf_context_p,
) -> int:
    ...


gguf_get_n_kv = lib.gguf_get_n_kv
gguf_get_n_kv.argtypes = [
    gguf_context_p_ctypes,
]
gguf_get_n_kv.restype = ctypes.c_int


# GGML_API int          gguf_find_key(const struct gguf_context * ctx, const char * key);
def gguf_find_key(
    ctx: gguf_context_p,
    key: bytes,
) -> int:
    ...


gguf_find_key = lib.gguf_find_key
gguf_find_key.argtypes = [
    gguf_context_p_ctypes,
    ctypes.c_char_p,
]
gguf_find_key.restype = ctypes.c_int


# GGML_API const char * gguf_get_key (const struct gguf_context * ctx, int key_id);
def gguf_get_key(
    ctx: gguf_context_p,
    key_id: Union[ctypes.c_int, int],
) -> bytes:
    ...


gguf_get_key = lib.gguf_get_key
gguf_get_key.argtypes = [
    gguf_context_p_ctypes,
    ctypes.c_int,
]
gguf_get_key.restype = ctypes.c_char_p


# GGML_API enum gguf_type gguf_get_kv_type (const struct gguf_context * ctx, int key_id);
def gguf_get_kv_type(
    ctx: gguf_context_p,
    key_id: Union[ctypes.c_int, int],
) -> int:
    ...


gguf_get_kv_type = lib.gguf_get_kv_type
gguf_get_kv_type.argtypes = [
    gguf_context_p_ctypes,
    ctypes.c_int,
]
gguf_get_kv_type.restype = ctypes.c_int


# GGML_API enum gguf_type gguf_get_arr_type(const struct gguf_context * ctx, int key_id);
def gguf_get_arr_type(
    ctx: gguf_context_p,
    key_id: Union[ctypes.c_int, int],
) -> int:
    ...


gguf_get_arr_type = lib.gguf_get_arr_type
gguf_get_arr_type.argtypes = [
    gguf_context_p_ctypes,
    ctypes.c_int,
]
gguf_get_arr_type.restype = ctypes.c_int


# // results are undefined if the wrong type is used for the key
# GGML_API uint8_t      gguf_get_val_u8  (const struct gguf_context * ctx, int key_id);
def gguf_get_val_u8(
    ctx: gguf_context_p,
    key_id: Union[ctypes.c_int, int],
) -> int:
    ...


gguf_get_val_u8 = lib.gguf_get_val_u8
gguf_get_val_u8.argtypes = [
    gguf_context_p_ctypes,
    ctypes.c_int,
]
gguf_get_val_u8.restype = ctypes.c_uint8


# GGML_API int8_t       gguf_get_val_i8  (const struct gguf_context * ctx, int key_id);
def gguf_get_val_i8(
    ctx: gguf_context_p,
    key_id: Union[ctypes.c_int, int],
) -> int:
    ...


gguf_get_val_i8 = lib.gguf_get_val_i8
gguf_get_val_i8.argtypes = [
    gguf_context_p_ctypes,
    ctypes.c_int,
]
gguf_get_val_i8.restype = ctypes.c_int8


# GGML_API uint16_t     gguf_get_val_u16 (const struct gguf_context * ctx, int key_id);
def gguf_get_val_u16(
    ctx: gguf_context_p,
    key_id: Union[ctypes.c_int, int],
) -> int:
    ...


gguf_get_val_u16 = lib.gguf_get_val_u16
gguf_get_val_u16.argtypes = [
    gguf_context_p_ctypes,
    ctypes.c_int,
]
gguf_get_val_u16.restype = ctypes.c_uint16


# GGML_API int16_t      gguf_get_val_i16 (const struct gguf_context * ctx, int key_id);
def gguf_get_val_i16(
    ctx: gguf_context_p,
    key_id: Union[ctypes.c_int, int],
) -> int:
    ...


gguf_get_val_i16 = lib.gguf_get_val_i16
gguf_get_val_i16.argtypes = [
    gguf_context_p_ctypes,
    ctypes.c_int,
]
gguf_get_val_i16.restype = ctypes.c_int16


# GGML_API uint32_t     gguf_get_val_u32 (const struct gguf_context * ctx, int key_id);
def gguf_get_val_u32(
    ctx: gguf_context_p,
    key_id: Union[ctypes.c_int, int],
) -> int:
    ...


gguf_get_val_u32 = lib.gguf_get_val_u32
gguf_get_val_u32.argtypes = [
    gguf_context_p_ctypes,
    ctypes.c_int,
]
gguf_get_val_u32.restype = ctypes.c_uint32


# GGML_API int32_t      gguf_get_val_i32 (const struct gguf_context * ctx, int key_id);
def gguf_get_val_i32(
    ctx: gguf_context_p,
    key_id: Union[ctypes.c_int, int],
) -> int:
    ...


gguf_get_val_i32 = lib.gguf_get_val_i32
gguf_get_val_i32.argtypes = [
    gguf_context_p_ctypes,
    ctypes.c_int,
]
gguf_get_val_i32.restype = ctypes.c_int32


# GGML_API float        gguf_get_val_f32 (const struct gguf_context * ctx, int key_id);
def gguf_get_val_f32(
    ctx: gguf_context_p,
    key_id: Union[ctypes.c_int, int],
) -> float:
    ...


gguf_get_val_f32 = lib.gguf_get_val_f32
gguf_get_val_f32.argtypes = [
    gguf_context_p_ctypes,
    ctypes.c_int,
]
gguf_get_val_f32.restype = ctypes.c_float


# GGML_API uint64_t     gguf_get_val_u64 (const struct gguf_context * ctx, int key_id);
def gguf_get_val_u64(
    ctx: gguf_context_p,
    key_id: Union[ctypes.c_int, int],
) -> int:
    ...


gguf_get_val_u64 = lib.gguf_get_val_u64
gguf_get_val_u64.argtypes = [
    gguf_context_p_ctypes,
    ctypes.c_int,
]
gguf_get_val_u64.restype = ctypes.c_uint64


# GGML_API int64_t      gguf_get_val_i64 (const struct gguf_context * ctx, int key_id);
def gguf_get_val_i64(
    ctx: gguf_context_p,
    key_id: Union[ctypes.c_int, int],
) -> int:
    ...


gguf_get_val_i64 = lib.gguf_get_val_i64
gguf_get_val_i64.argtypes = [
    gguf_context_p_ctypes,
    ctypes.c_int,
]
gguf_get_val_i64.restype = ctypes.c_int64


# GGML_API double       gguf_get_val_f64 (const struct gguf_context * ctx, int key_id);
def gguf_get_val_f64(
    ctx: gguf_context_p,
    key_id: Union[ctypes.c_int, int],
) -> float:
    ...


gguf_get_val_f64 = lib.gguf_get_val_f64
gguf_get_val_f64.argtypes = [
    gguf_context_p_ctypes,
    ctypes.c_int,
]
gguf_get_val_f64.restype = ctypes.c_double


# GGML_API bool         gguf_get_val_bool(const struct gguf_context * ctx, int key_id);
def gguf_get_val_bool(
    ctx: gguf_context_p,
    key_id: Union[ctypes.c_int, int],
) -> bool:
    ...


gguf_get_val_bool = lib.gguf_get_val_bool
gguf_get_val_bool.argtypes = [
    gguf_context_p_ctypes,
    ctypes.c_int,
]
gguf_get_val_bool.restype = ctypes.c_bool


# GGML_API const char * gguf_get_val_str (const struct gguf_context * ctx, int key_id);
def gguf_get_val_str(
    ctx: gguf_context_p,
    key_id: Union[ctypes.c_int, int],
) -> bytes:
    ...


gguf_get_val_str = lib.gguf_get_val_str
gguf_get_val_str.argtypes = [
    gguf_context_p_ctypes,
    ctypes.c_int,
]
gguf_get_val_str.restype = ctypes.c_char_p


# GGML_API const void * gguf_get_val_data(const struct gguf_context * ctx, int key_id);
def gguf_get_val_data(
    ctx: gguf_context_p,
    key_id: Union[ctypes.c_int, int],
) -> Optional[int]:
    ...


gguf_get_val_data = lib.gguf_get_val_data
gguf_get_val_data.argtypes = [
    gguf_context_p_ctypes,
    ctypes.c_int,
]
gguf_get_val_data.restype = ctypes.c_void_p


# GGML_API int          gguf_get_arr_n   (const struct gguf_context * ctx, int key_id);
def gguf_get_arr_n(
    ctx: gguf_context_p,
    key_id: Union[ctypes.c_int, int],
) -> int:
    ...


gguf_get_arr_n = lib.gguf_get_arr_n
gguf_get_arr_n.argtypes = [
    gguf_context_p_ctypes,
    ctypes.c_int,
]
gguf_get_arr_n.restype = ctypes.c_int


# GGML_API const void * gguf_get_arr_data(const struct gguf_context * ctx, int key_id);
def gguf_get_arr_data(
    ctx: gguf_context_p,
    key_id: Union[ctypes.c_int, int],
) -> Optional[int]:
    ...


gguf_get_arr_data = lib.gguf_get_arr_data
gguf_get_arr_data.argtypes = [
    gguf_context_p_ctypes,
    ctypes.c_int,
]
gguf_get_arr_data.restype = ctypes.c_void_p


# GGML_API const char * gguf_get_arr_str (const struct gguf_context * ctx, int key_id, int i);
def gguf_get_arr_str(
    ctx: gguf_context_p,
    key_id: Union[ctypes.c_int, int],
    i: Union[ctypes.c_int, int],
) -> bytes:
    ...


gguf_get_arr_str = lib.gguf_get_arr_str
gguf_get_arr_str.argtypes = [
    gguf_context_p_ctypes,
    ctypes.c_int,
    ctypes.c_int,
]
gguf_get_arr_str.restype = ctypes.c_char_p


# GGML_API int            gguf_get_n_tensors    (const struct gguf_context * ctx);
def gguf_get_n_tensors(
    ctx: gguf_context_p,
) -> int:
    ...


gguf_get_n_tensors = lib.gguf_get_n_tensors
gguf_get_n_tensors.argtypes = [
    gguf_context_p_ctypes,
]
gguf_get_n_tensors.restype = ctypes.c_int


# GGML_API int            gguf_find_tensor      (const struct gguf_context * ctx, const char * name);
def gguf_find_tensor(
    ctx: gguf_context_p,
    name: bytes,
) -> int:
    ...


gguf_find_tensor = lib.gguf_find_tensor
gguf_find_tensor.argtypes = [
    gguf_context_p_ctypes,
    ctypes.c_char_p,
]
gguf_find_tensor.restype = ctypes.c_int


# GGML_API size_t         gguf_get_tensor_offset(const struct gguf_context * ctx, int i);
def gguf_get_tensor_offset(
    ctx: gguf_context_p,
    i: Union[ctypes.c_int, int],
) -> int:
    ...


gguf_get_tensor_offset = lib.gguf_get_tensor_offset
gguf_get_tensor_offset.argtypes = [
    gguf_context_p_ctypes,
    ctypes.c_int,
]
gguf_get_tensor_offset.restype = ctypes.c_size_t


# GGML_API char *         gguf_get_tensor_name  (const struct gguf_context * ctx, int i);
def gguf_get_tensor_name(
    ctx: gguf_context_p,
    i: Union[ctypes.c_int, int],
) -> bytes:
    ...


gguf_get_tensor_name = lib.gguf_get_tensor_name
gguf_get_tensor_name.argtypes = [
    gguf_context_p_ctypes,
    ctypes.c_int,
]
gguf_get_tensor_name.restype = ctypes.c_char_p


# GGML_API enum ggml_type gguf_get_tensor_type  (const struct gguf_context * ctx, int i);
def gguf_get_tensor_type(
    ctx: gguf_context_p,
    i: Union[ctypes.c_int, int],
) -> int:
    ...


gguf_get_tensor_type = lib.gguf_get_tensor_type
gguf_get_tensor_type.argtypes = [
    gguf_context_p_ctypes,
    ctypes.c_int,
]
gguf_get_tensor_type.restype = ctypes.c_int


# // overrides existing values or adds a new one
# GGML_API void gguf_set_val_u8  (struct gguf_context * ctx, const char * key, uint8_t  val);
def gguf_set_val_u8(
    ctx: gguf_context_p,
    key: bytes,
    val: Union[ctypes.c_uint8, int],
):
    ...


gguf_set_val_u8 = lib.gguf_set_val_u8
gguf_set_val_u8.argtypes = [
    gguf_context_p_ctypes,
    ctypes.c_char_p,
    ctypes.c_uint8,
]
gguf_set_val_u8.restype = None


# GGML_API void gguf_set_val_i8  (struct gguf_context * ctx, const char * key, int8_t   val);
def gguf_set_val_i8(
    ctx: gguf_context_p,
    key: bytes,
    val: Union[ctypes.c_int8, int],
):
    ...


gguf_set_val_i8 = lib.gguf_set_val_i8
gguf_set_val_i8.argtypes = [
    gguf_context_p_ctypes,
    ctypes.c_char_p,
    ctypes.c_int8,
]
gguf_set_val_i8.restype = None


# GGML_API void gguf_set_val_u16 (struct gguf_context * ctx, const char * key, uint16_t val);
def gguf_set_val_u16(
    ctx: gguf_context_p,
    key: bytes,
    val: Union[ctypes.c_uint16, int],
):
    ...


gguf_set_val_u16 = lib.gguf_set_val_u16
gguf_set_val_u16.argtypes = [
    gguf_context_p_ctypes,
    ctypes.c_char_p,
    ctypes.c_uint16,
]
gguf_set_val_u16.restype = None


# GGML_API void gguf_set_val_i16 (struct gguf_context * ctx, const char * key, int16_t  val);
def gguf_set_val_i16(
    ctx: gguf_context_p,
    key: bytes,
    val: Union[ctypes.c_int16, int],
):
    ...


gguf_set_val_i16 = lib.gguf_set_val_i16
gguf_set_val_i16.argtypes = [
    gguf_context_p_ctypes,
    ctypes.c_char_p,
    ctypes.c_int16,
]
gguf_set_val_i16.restype = None


# GGML_API void gguf_set_val_u32 (struct gguf_context * ctx, const char * key, uint32_t val);
def gguf_set_val_u32(
    ctx: gguf_context_p,
    key: bytes,
    val: Union[ctypes.c_uint32, int],
):
    ...


gguf_set_val_u32 = lib.gguf_set_val_u32
gguf_set_val_u32.argtypes = [
    gguf_context_p_ctypes,
    ctypes.c_char_p,
    ctypes.c_uint32,
]
gguf_set_val_u32.restype = None


# GGML_API void gguf_set_val_i32 (struct gguf_context * ctx, const char * key, int32_t  val);
def gguf_set_val_i32(
    ctx: gguf_context_p,
    key: bytes,
    val: Union[ctypes.c_int32, int],
):
    ...


gguf_set_val_i32 = lib.gguf_set_val_i32
gguf_set_val_i32.argtypes = [
    gguf_context_p_ctypes,
    ctypes.c_char_p,
    ctypes.c_int32,
]
gguf_set_val_i32.restype = None


# GGML_API void gguf_set_val_f32 (struct gguf_context * ctx, const char * key, float    val);
def gguf_set_val_f32(
    ctx: gguf_context_p,
    key: bytes,
    val: Union[ctypes.c_float, float],
):
    ...


gguf_set_val_f32 = lib.gguf_set_val_f32
gguf_set_val_f32.argtypes = [
    gguf_context_p_ctypes,
    ctypes.c_char_p,
    ctypes.c_float,
]
gguf_set_val_f32.restype = None


# GGML_API void gguf_set_val_u64 (struct gguf_context * ctx, const char * key, uint64_t val);
def gguf_set_val_u64(
    ctx: gguf_context_p,
    key: bytes,
    val: Union[ctypes.c_uint64, int],
):
    ...


gguf_set_val_u64 = lib.gguf_set_val_u64
gguf_set_val_u64.argtypes = [
    gguf_context_p_ctypes,
    ctypes.c_char_p,
    ctypes.c_uint64,
]
gguf_set_val_u64.restype = None


# GGML_API void gguf_set_val_i64 (struct gguf_context * ctx, const char * key, int64_t  val);
def gguf_set_val_i64(
    ctx: gguf_context_p,
    key: bytes,
    val: Union[ctypes.c_int64, int],
):
    ...


gguf_set_val_i64 = lib.gguf_set_val_i64
gguf_set_val_i64.argtypes = [
    gguf_context_p_ctypes,
    ctypes.c_char_p,
    ctypes.c_int64,
]
gguf_set_val_i64.restype = None


# GGML_API void gguf_set_val_f64 (struct gguf_context * ctx, const char * key, double   val);
def gguf_set_val_f64(
    ctx: gguf_context_p,
    key: bytes,
    val: Union[ctypes.c_double, float],
):
    ...


gguf_set_val_f64 = lib.gguf_set_val_f64
gguf_set_val_f64.argtypes = [
    gguf_context_p_ctypes,
    ctypes.c_char_p,
    ctypes.c_double,
]
gguf_set_val_f64.restype = None


# GGML_API void gguf_set_val_bool(struct gguf_context * ctx, const char * key, bool     val);
def gguf_set_val_bool(
    ctx: gguf_context_p,
    key: bytes,
    val: Union[ctypes.c_bool, bool],
):
    ...


gguf_set_val_bool = lib.gguf_set_val_bool
gguf_set_val_bool.argtypes = [
    gguf_context_p_ctypes,
    ctypes.c_char_p,
    ctypes.c_bool,
]
gguf_set_val_bool.restype = None


# GGML_API void gguf_set_val_str (struct gguf_context * ctx, const char * key, const char * val);
def gguf_set_val_str(
    ctx: gguf_context_p,
    key: bytes,
    val: bytes,
):
    ...


gguf_set_val_str = lib.gguf_set_val_str
gguf_set_val_str.argtypes = [
    gguf_context_p_ctypes,
    ctypes.c_char_p,
    ctypes.c_char_p,
]
gguf_set_val_str.restype = None


# GGML_API void gguf_set_arr_data(struct gguf_context * ctx, const char * key, enum gguf_type type, const void * data, int n);
def gguf_set_arr_data(
    ctx: gguf_context_p,
    key: bytes,
    type: Union[ctypes.c_int, int],
    data: Union[ctypes.c_void_p, int, None],
    n: Union[ctypes.c_int, int],
):
    ...


gguf_set_arr_data = lib.gguf_set_arr_data
gguf_set_arr_data.argtypes = [
    gguf_context_p_ctypes,
    ctypes.c_char_p,
    ctypes.c_int,
    ctypes.c_void_p,
    ctypes.c_int,
]
gguf_set_arr_data.restype = None


# GGML_API void gguf_set_arr_str (struct gguf_context * ctx, const char * key, const char ** data, int n);
def gguf_set_arr_str(
    ctx: gguf_context_p,
    key: bytes,
    data: CtypesPointer[ctypes.c_char_p],
    n: Union[ctypes.c_int, int],
):
    ...


gguf_set_arr_str = lib.gguf_set_arr_str
gguf_set_arr_str.argtypes = [
    gguf_context_p_ctypes,
    ctypes.c_char_p,
    ctypes.POINTER(ctypes.c_char_p),
    ctypes.c_int,
]
gguf_set_arr_str.restype = None


# // set or add KV pairs from another context
# GGML_API void gguf_set_kv(struct gguf_context * ctx, struct gguf_context * src);
def gguf_set_kv(
    ctx: gguf_context_p,
    src: gguf_context_p,
):
    ...


gguf_set_kv = lib.gguf_set_kv
gguf_set_kv.argtypes = [
    gguf_context_p_ctypes,
    gguf_context_p_ctypes,
]
gguf_set_kv.restype = None


# // manage tensor info
# GGML_API void gguf_add_tensor(struct gguf_context * ctx, const struct ggml_tensor * tensor);
def gguf_add_tensor(
    ctx: gguf_context_p,
    tensor: ggml_tensor_p,
):
    ...


gguf_add_tensor = lib.gguf_add_tensor
gguf_add_tensor.argtypes = [
    gguf_context_p_ctypes,
    ctypes.POINTER(ggml_tensor),
]
gguf_add_tensor.restype = None


# GGML_API void gguf_set_tensor_type(struct gguf_context * ctx, const char * name, enum ggml_type type);
def gguf_set_tensor_type(
    ctx: gguf_context_p, name: bytes, type: Union[ctypes.c_int, int], /
):
    ...


gguf_set_tensor_type = lib.gguf_set_tensor_type
gguf_set_tensor_type.argtypes = [
    gguf_context_p_ctypes,
    ctypes.c_char_p,
    ctypes.c_int,
]
gguf_set_tensor_type.restype = None


# GGML_API void gguf_set_tensor_data(struct gguf_context * ctx, const char * name, const void * data, size_t size);
def gguf_set_tensor_data(
    ctx: gguf_context_p,
    name: bytes,
    data: Union[ctypes.c_void_p, int, None],
    size: Union[ctypes.c_size_t, int],
    /,
):
    ...


gguf_set_tensor_data = lib.gguf_set_tensor_data
gguf_set_tensor_data.argtypes = [
    gguf_context_p_ctypes,
    ctypes.c_char_p,
    ctypes.c_void_p,
    ctypes.c_size_t,
]
gguf_set_tensor_data.restype = None

# // writing gguf files can be done in 2 ways:
# //
# // - write the entire gguf_context to a binary file in a single pass:
# //
# //   gguf_write_to_file(ctx, fname);
# //
# // - first prepare a file with a placeholder for the meta data, write the tensor data, then write the meta data:
# //
# //   FILE * f = fopen(fname, "wb");
# //   fseek(f, gguf_get_meta_size(ctx), SEEK_SET);
# //   fwrite(f, ...);
# //   void * data = gguf_meta_get_meta_data(ctx);
# //   fseek(f, 0, SEEK_SET);
# //   fwrite(f, data, gguf_get_meta_size(ctx));
# //   free(data);
# //   fclose(f);
# //


# // write the entire context to a binary file
# GGML_API void gguf_write_to_file(const struct gguf_context * ctx, const char * fname, bool only_meta);
def gguf_write_to_file(
    ctx: gguf_context_p, fname: bytes, only_meta: Union[ctypes.c_bool, bool], /
):
    ...


gguf_write_to_file = lib.gguf_write_to_file
gguf_write_to_file.argtypes = [
    gguf_context_p_ctypes,
    ctypes.c_char_p,
    ctypes.c_bool,
]
gguf_write_to_file.restype = None


# // get the size in bytes of the meta data (header, kv pairs, tensor info) including padding
# GGML_API size_t gguf_get_meta_size(const struct gguf_context * ctx);
def gguf_get_meta_size(ctx: gguf_context_p, /) -> int:
    ...


gguf_get_meta_size = lib.gguf_get_meta_size
gguf_get_meta_size.argtypes = [
    gguf_context_p_ctypes,
]
gguf_get_meta_size.restype = ctypes.c_size_t


# GGML_API void   gguf_get_meta_data(const struct gguf_context * ctx, void * data);
def gguf_get_meta_data(ctx: gguf_context_p, data: Union[ctypes.c_void_p, int, None], /):
    ...


gguf_get_meta_data = lib.gguf_get_meta_data
gguf_get_meta_data.argtypes = [
    gguf_context_p_ctypes,
    ctypes.c_void_p,
]
gguf_get_meta_data.restype = None


# //
# // system info
# //


# GGML_API int ggml_cpu_has_avx        (void);
def ggml_cpu_has_avx() -> int:
    ...


ggml_cpu_has_avx = lib.ggml_cpu_has_avx
ggml_cpu_has_avx.argtypes = []
ggml_cpu_has_avx.restype = ctypes.c_int


# GGML_API int ggml_cpu_has_avx_vnni   (void);
def ggml_cpu_has_avx_vnni() -> int:
    ...


ggml_cpu_has_avx_vnni = lib.ggml_cpu_has_avx_vnni
ggml_cpu_has_avx_vnni.argtypes = []
ggml_cpu_has_avx_vnni.restype = ctypes.c_int


# GGML_API int ggml_cpu_has_avx2       (void);
def ggml_cpu_has_avx2() -> int:
    ...


ggml_cpu_has_avx2 = lib.ggml_cpu_has_avx2
ggml_cpu_has_avx2.argtypes = []
ggml_cpu_has_avx2.restype = ctypes.c_int


# GGML_API int ggml_cpu_has_avx512     (void);
def ggml_cpu_has_avx512() -> int:
    ...


ggml_cpu_has_avx512 = lib.ggml_cpu_has_avx512
ggml_cpu_has_avx512.argtypes = []
ggml_cpu_has_avx512.restype = ctypes.c_int


# GGML_API int ggml_cpu_has_avx512_vbmi(void);
def ggml_cpu_has_avx512_vbmi() -> int:
    ...


ggml_cpu_has_avx512_vbmi = lib.ggml_cpu_has_avx512_vbmi
ggml_cpu_has_avx512_vbmi.argtypes = []
ggml_cpu_has_avx512_vbmi.restype = ctypes.c_int


# GGML_API int ggml_cpu_has_avx512_vnni(void);
def ggml_cpu_has_avx512_vnni() -> int:
    ...


ggml_cpu_has_avx512_vnni = lib.ggml_cpu_has_avx512_vnni
ggml_cpu_has_avx512_vnni.argtypes = []
ggml_cpu_has_avx512_vnni.restype = ctypes.c_int


# GGML_API int ggml_cpu_has_fma        (void);
def ggml_cpu_has_fma() -> int:
    ...


ggml_cpu_has_fma = lib.ggml_cpu_has_fma
ggml_cpu_has_fma.argtypes = []
ggml_cpu_has_fma.restype = ctypes.c_int


# GGML_API int ggml_cpu_has_neon       (void);
def ggml_cpu_has_neon() -> int:
    ...


ggml_cpu_has_neon = lib.ggml_cpu_has_neon
ggml_cpu_has_neon.argtypes = []
ggml_cpu_has_neon.restype = ctypes.c_int


# GGML_API int ggml_cpu_has_arm_fma    (void);
def ggml_cpu_has_arm_fma() -> int:
    ...


ggml_cpu_has_arm_fma = lib.ggml_cpu_has_arm_fma
ggml_cpu_has_arm_fma.argtypes = []
ggml_cpu_has_arm_fma.restype = ctypes.c_int


# GGML_API int ggml_cpu_has_metal      (void);
def ggml_cpu_has_metal() -> int:
    ...


ggml_cpu_has_metal = lib.ggml_cpu_has_metal
ggml_cpu_has_metal.argtypes = []
ggml_cpu_has_metal.restype = ctypes.c_int


# GGML_API int ggml_cpu_has_f16c       (void);
def ggml_cpu_has_f16c() -> int:
    ...


ggml_cpu_has_f16c = lib.ggml_cpu_has_f16c
ggml_cpu_has_f16c.argtypes = []
ggml_cpu_has_f16c.restype = ctypes.c_int


# GGML_API int ggml_cpu_has_fp16_va    (void);
def ggml_cpu_has_fp16_va() -> int:
    ...


ggml_cpu_has_fp16_va = lib.ggml_cpu_has_fp16_va
ggml_cpu_has_fp16_va.argtypes = []
ggml_cpu_has_fp16_va.restype = ctypes.c_int


# GGML_API int ggml_cpu_has_wasm_simd  (void);
def ggml_cpu_has_wasm_simd() -> int:
    ...


ggml_cpu_has_wasm_simd = lib.ggml_cpu_has_wasm_simd
ggml_cpu_has_wasm_simd.argtypes = []
ggml_cpu_has_wasm_simd.restype = ctypes.c_int


# GGML_API int ggml_cpu_has_blas       (void);
def ggml_cpu_has_blas() -> int:
    ...


ggml_cpu_has_blas = lib.ggml_cpu_has_blas
ggml_cpu_has_blas.argtypes = []
ggml_cpu_has_blas.restype = ctypes.c_int


# GGML_API int ggml_cpu_has_cublas     (void);
def ggml_cpu_has_cublas() -> int:
    ...


ggml_cpu_has_cublas = lib.ggml_cpu_has_cublas
ggml_cpu_has_cublas.argtypes = []
ggml_cpu_has_cublas.restype = ctypes.c_int


# GGML_API int ggml_cpu_has_clblast    (void);
def ggml_cpu_has_clblast() -> int:
    ...


ggml_cpu_has_clblast = lib.ggml_cpu_has_clblast
ggml_cpu_has_clblast.argtypes = []
ggml_cpu_has_clblast.restype = ctypes.c_int


# GGML_API int ggml_cpu_has_vulkan     (void);
def ggml_cpu_has_vulkan() -> int:
    ...


ggml_cpu_has_vulkan = lib.ggml_cpu_has_vulkan
ggml_cpu_has_vulkan.argtypes = []
ggml_cpu_has_vulkan.restype = ctypes.c_int


# GGML_API int ggml_cpu_has_kompute    (void);
def ggml_cpu_has_kompute() -> int:
    ...


ggml_cpu_has_kompute = lib.ggml_cpu_has_kompute
ggml_cpu_has_kompute.argtypes = []
ggml_cpu_has_kompute.restype = ctypes.c_int


# GGML_API int ggml_cpu_has_gpublas    (void);
def ggml_cpu_has_gpublas() -> int:
    ...


ggml_cpu_has_gpublas = lib.ggml_cpu_has_gpublas
ggml_cpu_has_gpublas.argtypes = []
ggml_cpu_has_gpublas.restype = ctypes.c_int


# GGML_API int ggml_cpu_has_sse3       (void);
def ggml_cpu_has_sse3() -> int:
    ...


ggml_cpu_has_sse3 = lib.ggml_cpu_has_sse3
ggml_cpu_has_sse3.argtypes = []
ggml_cpu_has_sse3.restype = ctypes.c_int


# GGML_API int ggml_cpu_has_ssse3      (void);
def ggml_cpu_has_ssse3() -> int:
    ...


ggml_cpu_has_ssse3 = lib.ggml_cpu_has_ssse3
ggml_cpu_has_ssse3.argtypes = []
ggml_cpu_has_ssse3.restype = ctypes.c_int


# GGML_API int ggml_cpu_has_sycl       (void);
def ggml_cpu_has_sycl() -> int:
    ...


ggml_cpu_has_sycl = lib.ggml_cpu_has_sycl
ggml_cpu_has_sycl.argtypes = []
ggml_cpu_has_sycl.restype = ctypes.c_int


# GGML_API int ggml_cpu_has_vsx        (void);
def ggml_cpu_has_vsx() -> int:
    ...


ggml_cpu_has_vsx = lib.ggml_cpu_has_vsx
ggml_cpu_has_vsx.argtypes = []
ggml_cpu_has_vsx.restype = ctypes.c_int


# GGML_API int ggml_cpu_has_matmul_int8(void);
def ggml_cpu_has_matmul_int8() -> int:
    ...


ggml_cpu_has_matmul_int8 = lib.ggml_cpu_has_matmul_int8
ggml_cpu_has_matmul_int8.argtypes = []
ggml_cpu_has_matmul_int8.restype = ctypes.c_int


# //
# // Internal types and functions exposed for tests and benchmarks
# //

# typedef void (*ggml_to_float_t)(const void * x, float * y, int k);
ggml_to_float_t = ctypes.CFUNCTYPE(
    None, ctypes.c_void_p, ctypes.POINTER(ctypes.c_float), ctypes.c_int
)

# typedef void (*ggml_from_float_t)(const float * x, void * y, int k);
ggml_from_float_t = ctypes.CFUNCTYPE(
    None, ctypes.POINTER(ctypes.c_float), ctypes.c_void_p, ctypes.c_int
)

# typedef void (*ggml_vec_dot_t)   (int n, float * GGML_RESTRICT s, size_t bs, const void * GGML_RESTRICT x, size_t bx,
#                                   const void * GGML_RESTRICT y, size_t by, int nrc);
ggml_vec_dot_t = ctypes.CFUNCTYPE(
    None,
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_float),
    ctypes.c_size_t,
    ctypes.c_void_p,
    ctypes.c_size_t,
    ctypes.c_void_p,
    ctypes.c_size_t,
    ctypes.c_int,
)


# typedef struct {
#     const char      * type_name;
#     int               blck_size;
#     size_t            type_size;
#     bool              is_quantized;
#     ggml_to_float_t   to_float;
#     ggml_from_float_t from_float;
#     ggml_from_float_t from_float_reference;
#     ggml_vec_dot_t    vec_dot;
#     enum ggml_type    vec_dot_type;
#     int64_t           nrows; // number of rows to process simultaneously;
# } ggml_type_traits_t;
class ggml_type_traits_t(ctypes.Structure):
    _fields_ = [
        ("type_name", ctypes.c_char_p),
        ("blck_size", ctypes.c_int),
        ("type_size", ctypes.c_size_t),
        ("is_quantized", ctypes.c_bool),
        ("to_float", ggml_to_float_t),
        ("from_float", ggml_from_float_t),
        ("from_float_reference", ggml_from_float_t),
        ("vec_dot", ggml_vec_dot_t),
        ("vec_dot_type", ctypes.c_int),
        ("nrows", ctypes.c_int64),
    ]


# GGML_API ggml_type_traits_t ggml_internal_get_type_traits(enum ggml_type type);
def ggml_internal_get_type_traits(
    type: Union[ctypes.c_int, int], /
) -> ggml_type_traits_t:
    ...


ggml_internal_get_type_traits = lib.ggml_internal_get_type_traits
ggml_internal_get_type_traits.argtypes = [ctypes.c_int]
ggml_internal_get_type_traits.restype = ggml_type_traits_t

#####################################################
# GGML ALLOC API
# source: include/ggml/ggml-alloc.h
#####################################################


# typedef struct ggml_backend_buffer_type * ggml_backend_buffer_type_t;
# typedef struct ggml_backend_buffer * ggml_backend_buffer_t;
# typedef struct ggml_backend * ggml_backend_t;
ggml_backend_buffer_type_t = NewType("ggml_backend_buffer_type_t", int)
ggml_backend_buffer_type_t_ctypes: TypeAlias = ctypes.c_void_p

ggml_backend_buffer_t = NewType("ggml_backend_buffer_t", int)
ggml_backend_buffer_t_ctypes: TypeAlias = ctypes.c_void_p

ggml_backend_t = NewType("ggml_backend_t", int)
ggml_backend_t_ctypes: TypeAlias = ctypes.c_void_p


# // Tensor allocator
# typedef struct ggml_tallocr * ggml_tallocr_t;
ggml_tallocr = NewType("ggml_tallocr", int)
ggml_tallocr_ctypes: TypeAlias = ctypes.c_void_p


# GGML_API ggml_tallocr_t ggml_tallocr_new(ggml_backend_buffer_t buffer);
def ggml_tallocr_new(
    buffer: Union[ggml_backend_buffer_t, int], /
) -> Optional[ggml_tallocr]:
    ...


ggml_tallocr_new = lib.ggml_tallocr_new
ggml_tallocr_new.argtypes = [ggml_backend_buffer_t_ctypes]
ggml_tallocr_new.restype = ggml_tallocr


# GGML_API void           ggml_tallocr_free(ggml_tallocr_t talloc);
def ggml_tallocr_free(talloc: Union[ggml_tallocr, int], /) -> None:
    ...


ggml_tallocr_free = lib.ggml_tallocr_free
ggml_tallocr_free.argtypes = [ggml_tallocr_ctypes]
ggml_tallocr_free.restype = None


# GGML_API void           ggml_tallocr_alloc(ggml_tallocr_t talloc, struct ggml_tensor * tensor);
def ggml_tallocr_alloc(
    talloc: Union[ggml_tallocr, int], tensor: ggml_tensor_p, /
) -> None:
    ...


ggml_tallocr_alloc = lib.ggml_tallocr_alloc
ggml_tallocr_alloc.argtypes = [ggml_tallocr_ctypes, ctypes.POINTER(ggml_tensor)]
ggml_tallocr_alloc.restype = None


# // Graph allocator
# /*
#   Example usage:
#     ggml_gallocr_t galloc = ggml_gallocr_new(ggml_bacckend_cpu_buffer_type());

#     // optional: create a worst-case graph and reserve the buffers to avoid reallocations
#     ggml_gallocr_reserve(galloc, build_graph(max_batch));

#     // allocate the graph
#     struct ggml_cgraph * graph = build_graph(batch);
#     ggml_gallocr_alloc_graph(galloc, graph);

#     printf("compute buffer size: %zu bytes\n", ggml_gallocr_get_buffer_size(galloc, 0));

#     // evaluate the graph
#     ggml_backend_graph_compute(backend, graph);
# */

# // special tensor flags for use with the graph allocator:
# //   ggml_set_input(): all input tensors are allocated at the beginning of the graph in non-overlapping addresses
# //   ggml_set_output(): output tensors are never freed and never overwritten


# typedef struct ggml_gallocr * ggml_gallocr_t;
ggml_gallocr = NewType("ggml_gallocr", int)
ggml_gallocr_ctypes: TypeAlias = ctypes.c_void_p


# GGML_API ggml_gallocr_t ggml_gallocr_new(ggml_backend_buffer_type_t buft);
def ggml_gallocr_new(
    buft: Union[ggml_backend_buffer_type_t, int], /
) -> Optional[ggml_gallocr]:
    ...


ggml_gallocr_new = lib.ggml_gallocr_new
ggml_gallocr_new.argtypes = [ggml_backend_buffer_type_t_ctypes]
ggml_gallocr_new.restype = ggml_gallocr_ctypes


# GGML_API ggml_gallocr_t ggml_gallocr_new_n(ggml_backend_buffer_type_t * bufts, int n_bufs);
def ggml_gallocr_new_n(
    bufts: Union[ggml_backend_buffer_type_t, int], n_bufs: int, /
) -> Optional[ggml_gallocr]:
    ...


ggml_gallocr_new_n = lib.ggml_gallocr_new_n
ggml_gallocr_new_n.argtypes = [ggml_backend_buffer_type_t_ctypes, ctypes.c_int]
ggml_gallocr_new_n.restype = ggml_gallocr_ctypes


# GGML_API void           ggml_gallocr_free(ggml_gallocr_t galloc);
def ggml_gallocr_free(galloc: Union[ggml_gallocr, int], /) -> None:
    ...


ggml_gallocr_free = lib.ggml_gallocr_free
ggml_gallocr_free.argtypes = [ggml_gallocr_ctypes]
ggml_gallocr_free.restype = None


# // pre-allocate buffers from a measure graph - does not allocate or modify the graph
# // call with a worst-case graph to avoid buffer reallocations
# // not strictly required for single buffer usage: ggml_gallocr_alloc_graph will reallocate the buffers automatically if needed
# // returns false if the buffer allocation failed
# GGML_API bool ggml_gallocr_reserve(ggml_gallocr_t galloc, struct ggml_cgraph * graph);
def ggml_gallocr_reserve(
    galloc: Union[ggml_gallocr, int], graph: ggml_cgraph_p, /
) -> bool:
    """pre-allocate buffers from a measure graph - does not allocate or modify the graph
    call with a worst-case graph to avoid buffer reallocations
    not strictly required for single buffer usage: ggml_gallocr_alloc_graph will reallocate the buffers automatically if needed
    returns false if the buffer allocation failed"""
    ...


ggml_gallocr_reserve = lib.ggml_gallocr_reserve
ggml_gallocr_reserve.argtypes = [ggml_gallocr_ctypes, ctypes.POINTER(ggml_cgraph)]
ggml_gallocr_reserve.restype = ctypes.c_bool


# GGML_API bool ggml_gallocr_reserve_n(ggml_gallocr_t galloc, struct ggml_cgraph * graph, const int * node_buffer_ids);
def ggml_gallocr_reserve_n(
    galloc: Union[ggml_gallocr, int],
    graph: ggml_cgraph_p,
    node_buffer_ids: "ctypes._Pointer[ctypes.c_int]",  # type: ignore
    /,
) -> bool:
    ...


ggml_gallocr_reserve_n = lib.ggml_gallocr_reserve_n
ggml_gallocr_reserve_n.argtypes = [
    ggml_gallocr_ctypes,
    ctypes.POINTER(ggml_cgraph),
    ctypes.POINTER(ctypes.c_int),
]
ggml_gallocr_reserve_n.restype = ctypes.c_bool


# // automatic reallocation if the topology changes when using a single buffer
# // returns false if using multiple buffers and a re-allocation is needed (call ggml_gallocr_reserve_n first to set the node buffers)
# GGML_API bool ggml_gallocr_alloc_graph(ggml_gallocr_t galloc, struct ggml_cgraph * graph);
def ggml_gallocr_alloc_graph(
    galloc: Union[ggml_gallocr, int], graph: ggml_cgraph_p, /
) -> bool:
    """automatic reallocation if the topology changes when using a single buffer
    returns false if using multiple buffers and a re-allocation is needed (call ggml_gallocr_reserve_n first to set the node buffers)
    """
    ...


ggml_gallocr_alloc_graph = lib.ggml_gallocr_alloc_graph
ggml_gallocr_alloc_graph.argtypes = [ggml_gallocr_ctypes, ctypes.POINTER(ggml_cgraph)]
ggml_gallocr_alloc_graph.restype = ctypes.c_bool


# GGML_API size_t ggml_gallocr_get_buffer_size(ggml_gallocr_t galloc, int buffer_id);
def ggml_gallocr_get_buffer_size(
    galloc: Union[ggml_gallocr, int], buffer_id: Union[ctypes.c_int, int], /
) -> int:
    ...


ggml_gallocr_get_buffer_size = lib.ggml_gallocr_get_buffer_size
ggml_gallocr_get_buffer_size.argtypes = [ggml_gallocr_ctypes, ctypes.c_int]
ggml_gallocr_get_buffer_size.restype = ctypes.c_size_t


# // Utils
# // Create a buffer and allocate all the tensors in a ggml_context
# GGML_API struct ggml_backend_buffer * ggml_backend_alloc_ctx_tensors_from_buft(struct ggml_context * ctx, ggml_backend_buffer_type_t buft);
def ggml_backend_alloc_ctx_tensors_from_buft(
    ctx: ggml_context_p, buft: Union[ggml_backend_buffer_type_t, int], /
) -> Optional[ggml_backend_buffer_t]:
    """Create a buffer and allocate all the tensors in a ggml_context"""
    ...


ggml_backend_alloc_ctx_tensors_from_buft = lib.ggml_backend_alloc_ctx_tensors_from_buft
ggml_backend_alloc_ctx_tensors_from_buft.argtypes = [
    ggml_context_p_ctypes,
    ggml_backend_buffer_type_t_ctypes,
]
ggml_backend_alloc_ctx_tensors_from_buft.restype = ggml_backend_buffer_t_ctypes


# GGML_API struct ggml_backend_buffer * ggml_backend_alloc_ctx_tensors(struct ggml_context * ctx, ggml_backend_t backend);
def ggml_backend_alloc_ctx_tensors(
    ctx: ggml_context_p, backend: Union[ggml_backend_t, int], /
) -> Optional[ggml_backend_buffer_t]:
    ...


ggml_backend_alloc_ctx_tensors = lib.ggml_backend_alloc_ctx_tensors
ggml_backend_alloc_ctx_tensors.argtypes = [ggml_context_p_ctypes, ggml_backend_t_ctypes]
ggml_backend_alloc_ctx_tensors.restype = ggml_backend_buffer_t_ctypes


#####################################################
# GGML Backend API
# source: include/ggml/ggml-backend.h
#####################################################

# typedef struct ggml_backend_buffer_type * ggml_backend_buffer_type_t;
# typedef struct ggml_backend_buffer * ggml_backend_buffer_t;
# typedef struct ggml_backend * ggml_backend_t;
# typedef void * ggml_backend_graph_plan_t;
ggml_backend_graph_plan_t = NewType("ggml_backend_graph_plan_t", int)
ggml_backend_graph_plan_t_ctypes: TypeAlias = ctypes.c_void_p

# //
# // Backend buffer
# //


# // buffer type
# GGML_API           const char *          ggml_backend_buft_name            (ggml_backend_buffer_type_t buft);
def ggml_backend_buft_name(buft: Union[ggml_backend_buffer_type_t, int], /) -> bytes:
    ...


ggml_backend_buft_name = lib.ggml_backend_buft_name
ggml_backend_buft_name.argtypes = [ggml_backend_buffer_type_t_ctypes]
ggml_backend_buft_name.restype = ctypes.c_char_p


# GGML_API GGML_CALL ggml_backend_buffer_t ggml_backend_buft_alloc_buffer    (ggml_backend_buffer_type_t buft, size_t size);
def ggml_backend_buft_alloc_buffer(
    buft: Union[ggml_backend_buffer_type_t, int], size: Union[ctypes.c_size_t, int], /
) -> Optional[ggml_backend_buffer_t]:
    ...


ggml_backend_buft_alloc_buffer = lib.ggml_backend_buft_alloc_buffer
ggml_backend_buft_alloc_buffer.argtypes = [
    ggml_backend_buffer_type_t_ctypes,
    ctypes.c_size_t,
]
ggml_backend_buft_alloc_buffer.restype = ggml_backend_buffer_t_ctypes


# GGML_API           size_t                ggml_backend_buft_get_alignment   (ggml_backend_buffer_type_t buft);
def ggml_backend_buft_get_alignment(
    buft: Union[ggml_backend_buffer_type_t, int], /
) -> int:
    ...


ggml_backend_buft_get_alignment = lib.ggml_backend_buft_get_alignment
ggml_backend_buft_get_alignment.argtypes = [ggml_backend_buffer_type_t_ctypes]
ggml_backend_buft_get_alignment.restype = ctypes.c_size_t


# GGML_API           size_t                ggml_backend_buft_get_max_size    (ggml_backend_buffer_type_t buft);
def ggml_backend_buft_get_max_size(
    buft: Union[ggml_backend_buffer_type_t, int], /
) -> int:
    ...


ggml_backend_buft_get_max_size = lib.ggml_backend_buft_get_max_size
ggml_backend_buft_get_max_size.argtypes = [ggml_backend_buffer_type_t_ctypes]
ggml_backend_buft_get_max_size.restype = ctypes.c_size_t


# GGML_API GGML_CALL size_t                ggml_backend_buft_get_alloc_size  (ggml_backend_buffer_type_t buft, struct ggml_tensor * tensor);
def ggml_backend_buft_get_alloc_size(
    buft: Union[ggml_backend_buffer_type_t, int], tensor: ggml_tensor_p, /
) -> int:
    ...


ggml_backend_buft_get_alloc_size = lib.ggml_backend_buft_get_alloc_size
ggml_backend_buft_get_alloc_size.argtypes = [
    ggml_backend_buffer_type_t_ctypes,
    ctypes.POINTER(ggml_tensor),
]
ggml_backend_buft_get_alloc_size.restype = ctypes.c_size_t


# GGML_API           bool                  ggml_backend_buft_supports_backend(ggml_backend_buffer_type_t buft, ggml_backend_t backend);
def ggml_backend_buft_supports_backend(
    buft: Union[ggml_backend_buffer_type_t, int], backend: Union[ggml_backend_t, int], /
) -> bool:
    ...


ggml_backend_buft_supports_backend = lib.ggml_backend_buft_supports_backend
ggml_backend_buft_supports_backend.argtypes = [
    ggml_backend_buffer_type_t_ctypes,
    ggml_backend_t_ctypes,
]
ggml_backend_buft_supports_backend.restype = ctypes.c_bool


# GGML_API           bool                  ggml_backend_buft_is_host         (ggml_backend_buffer_type_t buft);
def ggml_backend_buft_is_host(buft: Union[ggml_backend_buffer_type_t, int], /) -> bool:
    ...


ggml_backend_buft_is_host = lib.ggml_backend_buft_is_host
ggml_backend_buft_is_host.argtypes = [ggml_backend_buffer_type_t_ctypes]
ggml_backend_buft_is_host.restype = ctypes.c_bool


# // buffer
# enum ggml_backend_buffer_usage {
#     GGML_BACKEND_BUFFER_USAGE_ANY = 0,
#     GGML_BACKEND_BUFFER_USAGE_WEIGHTS = 1,
# };
GGML_BACKEND_BUFFER_USAGE_ANY = 0
GGML_BACKEND_BUFFER_USAGE_WEIGHTS = 1


# GGML_API           const char *               ggml_backend_buffer_name          (ggml_backend_buffer_t buffer);
def ggml_backend_buffer_name(buffer: Union[ggml_backend_buffer_t, int], /) -> bytes:
    ...


ggml_backend_buffer_name = lib.ggml_backend_buffer_name
ggml_backend_buffer_name.argtypes = [ggml_backend_buffer_t_ctypes]
ggml_backend_buffer_name.restype = ctypes.c_char_p


# GGML_API           void                       ggml_backend_buffer_free          (ggml_backend_buffer_t buffer);
def ggml_backend_buffer_free(buffer: Union[ggml_backend_buffer_t, int], /):
    ...


ggml_backend_buffer_free = lib.ggml_backend_buffer_free
ggml_backend_buffer_free.argtypes = [ggml_backend_buffer_t_ctypes]
ggml_backend_buffer_free.restype = None


# GGML_API           void *                     ggml_backend_buffer_get_base      (ggml_backend_buffer_t buffer);
def ggml_backend_buffer_get_base(
    buffer: Union[ggml_backend_buffer_t, int], /
) -> Optional[int]:
    ...


ggml_backend_buffer_get_base = lib.ggml_backend_buffer_get_base
ggml_backend_buffer_get_base.argtypes = [ggml_backend_buffer_t_ctypes]
ggml_backend_buffer_get_base.restype = ctypes.c_void_p


# GGML_API           size_t                     ggml_backend_buffer_get_size      (ggml_backend_buffer_t buffer);
def ggml_backend_buffer_get_size(buffer: Union[ggml_backend_buffer_t, int], /) -> int:
    ...


ggml_backend_buffer_get_size = lib.ggml_backend_buffer_get_size
ggml_backend_buffer_get_size.argtypes = [ggml_backend_buffer_t_ctypes]
ggml_backend_buffer_get_size.restype = ctypes.c_size_t


# GGML_API GGML_CALL void                       ggml_backend_buffer_init_tensor   (ggml_backend_buffer_t buffer, struct ggml_tensor * tensor);
def ggml_backend_buffer_init_tensor(
    buffer: Union[ggml_backend_buffer_t, int], tensor: ggml_tensor_p, /
):
    ...


ggml_backend_buffer_init_tensor = lib.ggml_backend_buffer_init_tensor
ggml_backend_buffer_init_tensor.argtypes = [
    ggml_backend_buffer_t_ctypes,
    ctypes.POINTER(ggml_tensor),
]
ggml_backend_buffer_init_tensor.restype = None


# GGML_API           size_t                     ggml_backend_buffer_get_alignment (ggml_backend_buffer_t buffer);
def ggml_backend_buffer_get_alignment(
    buffer: Union[ggml_backend_buffer_t, int], /
) -> int:
    ...


ggml_backend_buffer_get_alignment = lib.ggml_backend_buffer_get_alignment
ggml_backend_buffer_get_alignment.argtypes = [ggml_backend_buffer_t_ctypes]
ggml_backend_buffer_get_alignment.restype = ctypes.c_size_t


# GGML_API           size_t                     ggml_backend_buffer_get_max_size  (ggml_backend_buffer_t buffer);
def ggml_backend_buffer_get_max_size(
    buffer: Union[ggml_backend_buffer_t, int], /
) -> int:
    ...


ggml_backend_buffer_get_max_size = lib.ggml_backend_buffer_get_max_size
ggml_backend_buffer_get_max_size.argtypes = [ggml_backend_buffer_t_ctypes]
ggml_backend_buffer_get_max_size.restype = ctypes.c_size_t


# GGML_API           size_t                     ggml_backend_buffer_get_alloc_size(ggml_backend_buffer_t buffer, struct ggml_tensor * tensor);
def ggml_backend_buffer_get_alloc_size(
    buffer: Union[ggml_backend_buffer_t, int], tensor: ggml_tensor_p, /
) -> int:
    ...


ggml_backend_buffer_get_alloc_size = lib.ggml_backend_buffer_get_alloc_size
ggml_backend_buffer_get_alloc_size.argtypes = [
    ggml_backend_buffer_t_ctypes,
    ctypes.POINTER(ggml_tensor),
]
ggml_backend_buffer_get_alloc_size.restype = ctypes.c_size_t


# GGML_API           void                       ggml_backend_buffer_clear         (ggml_backend_buffer_t buffer, uint8_t value);
def ggml_backend_buffer_clear(
    buffer: Union[ggml_backend_buffer_t, int], value: ctypes.c_uint8, /
):
    ...


ggml_backend_buffer_clear = lib.ggml_backend_buffer_clear
ggml_backend_buffer_clear.argtypes = [ggml_backend_buffer_t_ctypes, ctypes.c_uint8]
ggml_backend_buffer_clear.restype = None


# GGML_API           bool                       ggml_backend_buffer_is_host       (ggml_backend_buffer_t buffer);
def ggml_backend_buffer_is_host(buffer: Union[ggml_backend_buffer_t, int], /) -> bool:
    ...


ggml_backend_buffer_is_host = lib.ggml_backend_buffer_is_host
ggml_backend_buffer_is_host.argtypes = [ggml_backend_buffer_t_ctypes]
ggml_backend_buffer_is_host.restype = ctypes.c_bool


# GGML_API           void                       ggml_backend_buffer_set_usage     (ggml_backend_buffer_t buffer, enum ggml_backend_buffer_usage usage);
def ggml_backend_buffer_set_usage(
    buffer: Union[ggml_backend_buffer_t, int], usage: Union[ctypes.c_int, int], /
):
    ...


ggml_backend_buffer_set_usage = lib.ggml_backend_buffer_set_usage
ggml_backend_buffer_set_usage.argtypes = [ggml_backend_buffer_t_ctypes, ctypes.c_int]
ggml_backend_buffer_set_usage.restype = None


# GGML_API           ggml_backend_buffer_type_t ggml_backend_buffer_get_type      (ggml_backend_buffer_t buffer);
def ggml_backend_buffer_get_type(
    buffer: Union[ggml_backend_buffer_t, int], /
) -> Optional[ggml_backend_buffer_type_t]:
    ...


ggml_backend_buffer_get_type = lib.ggml_backend_buffer_get_type
ggml_backend_buffer_get_type.argtypes = [ggml_backend_buffer_t_ctypes]
ggml_backend_buffer_get_type.restype = ggml_backend_buffer_type_t_ctypes


# GGML_API           void                       ggml_backend_buffer_reset         (ggml_backend_buffer_t buffer);
def ggml_backend_buffer_reset(buffer: Union[ggml_backend_buffer_t, int], /):
    ...


ggml_backend_buffer_reset = lib.ggml_backend_buffer_reset
ggml_backend_buffer_reset.argtypes = [ggml_backend_buffer_t_ctypes]
ggml_backend_buffer_reset.restype = None

# //
# // Backend
# //


# GGML_API const char * ggml_backend_name(ggml_backend_t backend);
def ggml_backend_name(backend: Union[ggml_backend_t, int], /) -> bytes:
    ...


ggml_backend_name = lib.ggml_backend_name
ggml_backend_name.argtypes = [ggml_backend_t_ctypes]
ggml_backend_name.restype = ctypes.c_char_p


# GGML_API void         ggml_backend_free(ggml_backend_t backend);
def ggml_backend_free(backend: Union[ggml_backend_t, int], /):
    ...


ggml_backend_free = lib.ggml_backend_free
ggml_backend_free.argtypes = [ggml_backend_t_ctypes]
ggml_backend_free.restype = None


# GGML_API ggml_backend_buffer_type_t ggml_backend_get_default_buffer_type(ggml_backend_t backend);
def ggml_backend_get_default_buffer_type(
    backend: Union[ggml_backend_t, int], /
) -> Optional[ggml_backend_buffer_type_t]:
    ...


ggml_backend_get_default_buffer_type = lib.ggml_backend_get_default_buffer_type
ggml_backend_get_default_buffer_type.argtypes = [ggml_backend_t_ctypes]
ggml_backend_get_default_buffer_type.restype = ggml_backend_buffer_type_t_ctypes


# GGML_API ggml_backend_buffer_t      ggml_backend_alloc_buffer(ggml_backend_t backend, size_t size);
def ggml_backend_alloc_buffer(
    backend: Union[ggml_backend_t, int], size: Union[ctypes.c_size_t, int], /
) -> Optional[ggml_backend_buffer_t]:
    ...


ggml_backend_alloc_buffer = lib.ggml_backend_alloc_buffer
ggml_backend_alloc_buffer.argtypes = [ggml_backend_t_ctypes, ctypes.c_size_t]
ggml_backend_alloc_buffer.restype = ggml_backend_buffer_t


# GGML_API size_t                     ggml_backend_get_alignment(ggml_backend_t backend);
def ggml_backend_get_alignment(
    backend: Union[ggml_backend_t, int],
) -> int:
    ...


ggml_backend_get_alignment = lib.ggml_backend_get_alignment
ggml_backend_get_alignment.argtypes = [ggml_backend_t_ctypes]
ggml_backend_get_alignment.restype = ctypes.c_size_t


# GGML_API size_t                     ggml_backend_get_max_size(ggml_backend_t backend);
def ggml_backend_get_max_size(
    backend: Union[ggml_backend_t, int],
) -> int:
    ...


ggml_backend_get_max_size = lib.ggml_backend_get_max_size
ggml_backend_get_max_size.argtypes = [ggml_backend_t_ctypes]
ggml_backend_get_max_size.restype = ctypes.c_size_t


# GGML_API void ggml_backend_tensor_set_async(ggml_backend_t backend,       struct ggml_tensor * tensor, const void * data, size_t offset, size_t size);
def ggml_backend_tensor_set_async(
    backend: Union[ggml_backend_t, int],
    tensor: ggml_tensor_p,
    data: Union[ctypes.c_void_p, int, None],
    offset: Union[ctypes.c_size_t, int],
    size: Union[ctypes.c_size_t, int],
    /,
):
    ...


ggml_backend_tensor_set_async = lib.ggml_backend_tensor_set_async
ggml_backend_tensor_set_async.argtypes = [
    ggml_backend_t_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.c_void_p,
    ctypes.c_size_t,
    ctypes.c_size_t,
]
ggml_backend_tensor_set_async.restype = None


# GGML_API void ggml_backend_tensor_get_async(ggml_backend_t backend, const struct ggml_tensor * tensor,       void * data, size_t offset, size_t size);
def ggml_backend_tensor_get_async(
    backend: Union[ggml_backend_t, int],
    tensor: ggml_tensor_p,
    data: Union[ctypes.c_void_p, int, None],
    offset: Union[ctypes.c_size_t, int],
    size: Union[ctypes.c_size_t, int],
    /,
):
    ...


ggml_backend_tensor_get_async = lib.ggml_backend_tensor_get_async
ggml_backend_tensor_get_async.argtypes = [
    ggml_backend_t_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.c_void_p,
    ctypes.c_size_t,
    ctypes.c_size_t,
]
ggml_backend_tensor_get_async.restype = None


# GGML_API GGML_CALL void ggml_backend_tensor_set(      struct ggml_tensor * tensor, const void * data, size_t offset, size_t size);
def ggml_backend_tensor_set(
    tensor: ggml_tensor_p,
    data: Union[ctypes.c_void_p, int, None],
    offset: Union[ctypes.c_size_t, int],
    size: Union[ctypes.c_size_t, int],
    /,
):
    ...


ggml_backend_tensor_set = lib.ggml_backend_tensor_set
ggml_backend_tensor_set.argtypes = [
    ctypes.POINTER(ggml_tensor),
    ctypes.c_void_p,
    ctypes.c_size_t,
    ctypes.c_size_t,
]
ggml_backend_tensor_set.restype = None


# GGML_API GGML_CALL void ggml_backend_tensor_get(const struct ggml_tensor * tensor,       void * data, size_t offset, size_t size);
def ggml_backend_tensor_get(
    tensor: ggml_tensor_p,
    data: Union[ctypes.c_void_p, int, None],
    offset: Union[ctypes.c_size_t, int],
    size: Union[ctypes.c_size_t, int],
    /,
):
    ...


ggml_backend_tensor_get = lib.ggml_backend_tensor_get
ggml_backend_tensor_get.argtypes = [
    ctypes.POINTER(ggml_tensor),
    ctypes.c_void_p,
    ctypes.c_size_t,
    ctypes.c_size_t,
]
ggml_backend_tensor_get.restype = None


# GGML_API void ggml_backend_synchronize(ggml_backend_t backend);
def ggml_backend_synchronize(backend: Union[ggml_backend_t, int], /):
    ...


ggml_backend_synchronize = lib.ggml_backend_synchronize
ggml_backend_synchronize.argtypes = [ggml_backend_t_ctypes]
ggml_backend_synchronize.restype = None


# GGML_API ggml_backend_graph_plan_t ggml_backend_graph_plan_create (ggml_backend_t backend, struct ggml_cgraph * cgraph);
def ggml_backend_graph_plan_create(
    backend: Union[ggml_backend_t, int],
    cgraph: ggml_cgraph_p,
) -> ggml_backend_graph_plan_t:
    ...


ggml_backend_graph_plan_create = lib.ggml_backend_graph_plan_create
ggml_backend_graph_plan_create.argtypes = [
    ggml_backend_t_ctypes,
    ctypes.POINTER(ggml_cgraph),
]
ggml_backend_graph_plan_create.restype = ggml_backend_graph_plan_t_ctypes


# GGML_API void ggml_backend_graph_plan_free   (ggml_backend_t backend, ggml_backend_graph_plan_t plan);
def ggml_backend_graph_plan_free(
    backend: Union[ggml_backend_t, int], plan: ggml_backend_graph_plan_t, /
):
    ...


ggml_backend_graph_plan_free = lib.ggml_backend_graph_plan_free
ggml_backend_graph_plan_free.argtypes = [
    ggml_backend_t_ctypes,
    ggml_backend_graph_plan_t_ctypes,
]
ggml_backend_graph_plan_free.restype = None


# GGML_API void ggml_backend_graph_plan_compute(ggml_backend_t backend, ggml_backend_graph_plan_t plan);
def ggml_backend_graph_plan_compute(
    backend: Union[ggml_backend_t, int], plan: ggml_backend_graph_plan_t, /
):
    ...


ggml_backend_graph_plan_compute = lib.ggml_backend_graph_plan_compute
ggml_backend_graph_plan_compute.argtypes = [
    ggml_backend_t_ctypes,
    ggml_backend_graph_plan_t_ctypes,
]
ggml_backend_graph_plan_compute.restype = None


# GGML_API bool ggml_backend_graph_compute     (ggml_backend_t backend, struct ggml_cgraph * cgraph);
def ggml_backend_graph_compute(
    backend: Union[ggml_backend_t, int],
    cgraph: ggml_cgraph_p,
) -> bool:
    ...


ggml_backend_graph_compute = lib.ggml_backend_graph_compute
ggml_backend_graph_compute.argtypes = [
    ggml_backend_t_ctypes,
    ctypes.POINTER(ggml_cgraph),
]
ggml_backend_graph_compute.restype = ctypes.c_bool


# GGML_API bool ggml_backend_supports_op       (ggml_backend_t backend, const struct ggml_tensor * op);
def ggml_backend_supports_op(
    backend: Union[ggml_backend_t, int],
    op: ggml_tensor_p,
) -> Union[ctypes.c_bool, bool]:
    ...


ggml_backend_supports_op = lib.ggml_backend_supports_op
ggml_backend_supports_op.argtypes = [ggml_backend_t_ctypes, ctypes.POINTER(ggml_tensor)]
ggml_backend_supports_op.restype = ctypes.c_bool


# // tensor copy between different backends
# GGML_API void ggml_backend_tensor_copy(struct ggml_tensor * src, struct ggml_tensor * dst);
def ggml_backend_tensor_copy(src: ggml_tensor_p, dst: ggml_tensor_p, /):
    ...


ggml_backend_tensor_copy = lib.ggml_backend_tensor_copy
ggml_backend_tensor_copy.argtypes = [
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
]
ggml_backend_tensor_copy.restype = None


# GGML_API void ggml_backend_tensor_copy_async(ggml_backend_t backend, struct ggml_tensor * src, struct ggml_tensor * dst); // automatic fallback to sync copy
def ggml_backend_tensor_copy_async(
    backend: Union[ggml_backend_t, int], src: ggml_tensor_p, dst: ggml_tensor_p, /
):
    ...


# lib.ggml_backend_tensor_copy_async.argtypes = [
#     ggml_backend_t,
#     ctypes.POINTER(ggml_tensor),
#     ctypes.POINTER(ggml_tensor),
# ]
# lib.ggml_backend_tensor_copy_async.restype = None

# //
# // CPU backend
# //


# GGML_API ggml_backend_t ggml_backend_cpu_init(void);
def ggml_backend_cpu_init() -> Optional[ggml_backend_t]:
    ...


ggml_backend_cpu_init = lib.ggml_backend_cpu_init
ggml_backend_cpu_init.argtypes = []
ggml_backend_cpu_init.restype = ggml_backend_t_ctypes


# GGML_API GGML_CALL bool ggml_backend_is_cpu                (ggml_backend_t backend);
def ggml_backend_is_cpu(
    backend: Union[ggml_backend_t, int],
) -> bool:
    ...


ggml_backend_is_cpu = lib.ggml_backend_is_cpu
ggml_backend_is_cpu.argtypes = [ggml_backend_t_ctypes]
ggml_backend_is_cpu.restype = ctypes.c_bool


# GGML_API           void ggml_backend_cpu_set_n_threads     (ggml_backend_t backend_cpu, int n_threads);
def ggml_backend_cpu_set_n_threads(
    backend_cpu: Union[ggml_backend_t, int], n_threads: Union[ctypes.c_int, int], /
):
    ...


ggml_backend_cpu_set_n_threads = lib.ggml_backend_cpu_set_n_threads
ggml_backend_cpu_set_n_threads.argtypes = [ggml_backend_t_ctypes, ctypes.c_int]
ggml_backend_cpu_set_n_threads.restype = None


# GGML_API           void ggml_backend_cpu_set_abort_callback(ggml_backend_t backend_cpu, ggml_abort_callback abort_callback, void * abort_callback_data);
def ggml_backend_cpu_set_abort_callback(
    backend_cpu: Union[ggml_backend_t, int],
    abort_callback,  # type: ignore
    abort_callback_data: Union[ctypes.c_void_p, int, None],
    /,
):
    ...


ggml_backend_cpu_set_abort_callback = lib.ggml_backend_cpu_set_abort_callback
ggml_backend_cpu_set_abort_callback.argtypes = [
    ggml_backend_t_ctypes,
    ggml_abort_callback,
    ctypes.c_void_p,
]
ggml_backend_cpu_set_abort_callback.restype = None


# // Create a backend buffer from an existing pointer
# GGML_API GGML_CALL ggml_backend_buffer_t ggml_backend_cpu_buffer_from_ptr(void * ptr, size_t size);
def ggml_backend_cpu_buffer_from_ptr(
    ptr: Union[ctypes.c_void_p, int, None],
    size: Union[ctypes.c_size_t, int],
) -> Optional[ggml_backend_buffer_t]:
    ...


ggml_backend_cpu_buffer_from_ptr = lib.ggml_backend_cpu_buffer_from_ptr
ggml_backend_cpu_buffer_from_ptr.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
ggml_backend_cpu_buffer_from_ptr.restype = ggml_backend_buffer_t


# GGML_API GGML_CALL ggml_backend_buffer_type_t ggml_backend_cpu_buffer_type(void);
def ggml_backend_cpu_buffer_type() -> Optional[ggml_backend_buffer_type_t]:
    ...


ggml_backend_cpu_buffer_type = lib.ggml_backend_cpu_buffer_type
ggml_backend_cpu_buffer_type.argtypes = []
ggml_backend_cpu_buffer_type.restype = ggml_backend_buffer_type_t


# #ifdef GGML_USE_CPU_HBM
#     GGML_API ggml_backend_buffer_type_t ggml_backend_cpu_hbm_buffer_type(void);
# #endif
def ggml_backend_cpu_hbm_buffer_type() -> Optional[ggml_backend_buffer_type_t]:
    ...


if hasattr(lib, "ggml_backend_cpu_hbm_buffer_type"):
    ggml_backend_cpu_hbm_buffer_type = lib.ggml_backend_cpu_hbm_buffer_type
    ggml_backend_cpu_hbm_buffer_type.argtypes = []
    ggml_backend_cpu_hbm_buffer_type.restype = ggml_backend_buffer_type_t

# //
# // Backend registry
# //

# // The backend registry is a registry of all the available backends, and allows initializing backends in a generic way


# GGML_API size_t                     ggml_backend_reg_get_count(void);
def ggml_backend_reg_get_count() -> int:
    ...


ggml_backend_reg_get_count = lib.ggml_backend_reg_get_count
ggml_backend_reg_get_count.argtypes = []
ggml_backend_reg_get_count.restype = ctypes.c_size_t


# GGML_API size_t                     ggml_backend_reg_find_by_name(const char * name);
def ggml_backend_reg_find_by_name(
    name: bytes,
) -> int:
    ...


ggml_backend_reg_find_by_name = lib.ggml_backend_reg_find_by_name
ggml_backend_reg_find_by_name.argtypes = [ctypes.c_char_p]
ggml_backend_reg_find_by_name.restype = ctypes.c_size_t


# GGML_API ggml_backend_t             ggml_backend_reg_init_backend_from_str(const char * backend_str); // str is name[:params]
def ggml_backend_reg_init_backend_from_str(
    backend_str: bytes,
) -> Optional[ggml_backend_t]:
    ...


ggml_backend_reg_init_backend_from_str = lib.ggml_backend_reg_init_backend_from_str
ggml_backend_reg_init_backend_from_str.argtypes = [ctypes.c_char_p]
ggml_backend_reg_init_backend_from_str.restype = ggml_backend_t


# GGML_API const char *               ggml_backend_reg_get_name(size_t i);
def ggml_backend_reg_get_name(
    i: Union[ctypes.c_size_t, int],
) -> bytes:
    ...


ggml_backend_reg_get_name = lib.ggml_backend_reg_get_name
ggml_backend_reg_get_name.argtypes = [ctypes.c_size_t]
ggml_backend_reg_get_name.restype = ctypes.c_char_p


# GGML_API ggml_backend_t             ggml_backend_reg_init_backend(size_t i, const char * params); // params is backend-specific
def ggml_backend_reg_init_backend(
    i: Union[ctypes.c_size_t, int],
    params: bytes,
) -> Optional[ggml_backend_t]:
    ...


ggml_backend_reg_init_backend = lib.ggml_backend_reg_init_backend
ggml_backend_reg_init_backend.argtypes = [ctypes.c_size_t, ctypes.c_char_p]
ggml_backend_reg_init_backend.restype = ggml_backend_t


# GGML_API ggml_backend_buffer_type_t ggml_backend_reg_get_default_buffer_type(size_t i);
def ggml_backend_reg_get_default_buffer_type(
    i: Union[ctypes.c_size_t, int],
) -> Optional[ggml_backend_buffer_type_t]:
    ...


ggml_backend_reg_get_default_buffer_type = lib.ggml_backend_reg_get_default_buffer_type
ggml_backend_reg_get_default_buffer_type.argtypes = [ctypes.c_size_t]
ggml_backend_reg_get_default_buffer_type.restype = ggml_backend_buffer_type_t


# GGML_API ggml_backend_buffer_t      ggml_backend_reg_alloc_buffer(size_t i, size_t size);
def ggml_backend_reg_alloc_buffer(
    i: Union[ctypes.c_size_t, int],
    size: Union[ctypes.c_size_t, int],
) -> Optional[ggml_backend_buffer_t]:
    ...


ggml_backend_reg_alloc_buffer = lib.ggml_backend_reg_alloc_buffer
ggml_backend_reg_alloc_buffer.argtypes = [ctypes.c_size_t, ctypes.c_size_t]
ggml_backend_reg_alloc_buffer.restype = ggml_backend_buffer_t

# //
# // Backend scheduler
# //

# // The backend scheduler allows for multiple backends to be used together
# // Handles compute buffer allocation, assignment of tensors to backends, and copying of tensors between backends
# // The backends are selected based on:
# // - the backend that supports the operation
# // - the location of the pre-allocated tensors (e.g. the weights)
# /*
#   Example usage:

#     sched = ggml_backend_sched_new({backend_gpu, backend_gpu2, backend_cpu}, num_backends);
#     // sched is initialized with measure allocators and cannot be used until allocated with a measure graph

#     // initialize buffers from a measure graph
#     measure_graph = build_graph(sched); // use the allocr to allocate inputs as needed

#     // in build_graph:
#     build_graph(...) {
#         // manually assign nodes to a backend (optional, should not be needed in most cases)
#         struct ggml_tensor * node = ggml_mul_mat(ctx, ...);
#         ggml_backend_sched_set_node_backend(sched, node, backend_gpu);
#     }

#     // allocate backend buffers from measure graph
#     ggml_backend_sched_init_measure(sched, measure_graph);

#     // the scheduler is now ready to compute graphs

#     // compute
#     graph = build_graph(sched);
#     ggml_backend_sched_graph_compute(sched, graph);
# */

# struct ggml_backend_sched;
# typedef struct ggml_backend_sched * ggml_backend_sched_t;
ggml_backend_sched_t = NewType("ggml_backend_sched_t", int)
ggml_backend_sched_t_ctypes: TypeAlias = ctypes.c_void_p


# // when ask == true, the scheduler wants to know if the user wants to observe this node
# // this allows the scheduler to batch nodes together in order to evaluate them in a single call
# //
# // when ask == false, the scheduler is passing the node tensor to the user for observation
# // if the user returns false, the scheduler will cancel the graph compute
# //
# typedef bool (*ggml_backend_sched_eval_callback)(struct ggml_tensor * t, bool ask, void * user_data);
ggml_backend_sched_eval_callback = ctypes.CFUNCTYPE(
    ctypes.c_bool, ctypes.POINTER(ggml_tensor), ctypes.c_bool, ctypes.c_void_p
)


# // Initialize a backend scheduler
# GGML_API ggml_backend_sched_t  ggml_backend_sched_new(ggml_backend_t * backends, ggml_backend_buffer_type_t * bufts, int n_backends, size_t graph_size);
def ggml_backend_sched_new(
    backends: "ctypes._Pointer[ggml_backend_t]",  # type: ignore
    bufts: "ctypes._Pointer[ggml_backend_buffer_type_t]",  # type: ignore
    n_backends: Union[ctypes.c_int, int],
    graph_size: Union[ctypes.c_size_t, int],
) -> ggml_backend_sched_t:
    ...


ggml_backend_sched_new = lib.ggml_backend_sched_new
ggml_backend_sched_new.argtypes = [
    ctypes.POINTER(ggml_backend_t_ctypes),
    ctypes.POINTER(ggml_backend_buffer_type_t_ctypes),
    ctypes.c_int,
    ctypes.c_size_t,
]
ggml_backend_sched_new.restype = ggml_backend_sched_t


# GGML_API void                  ggml_backend_sched_free(ggml_backend_sched_t sched);
def ggml_backend_sched_free(sched: ggml_backend_sched_t, /):
    ...


ggml_backend_sched_free = lib.ggml_backend_sched_free
ggml_backend_sched_free.argtypes = [ggml_backend_sched_t_ctypes]
ggml_backend_sched_free.restype = None


# // Initialize backend buffers from a measure graph
# GGML_API bool                  ggml_backend_sched_reserve(ggml_backend_sched_t sched, struct ggml_cgraph * measure_graph);
def ggml_backend_sched_reserve(
    sched: ggml_backend_sched_t,
    measure_graph: ggml_cgraph_p,
) -> bool:
    """Initialize backend buffers from a measure graph."""
    ...


ggml_backend_sched_reserve = lib.ggml_backend_sched_reserve
ggml_backend_sched_reserve.argtypes = [
    ggml_backend_sched_t_ctypes,
    ctypes.POINTER(ggml_cgraph),
]
ggml_backend_sched_reserve.restype = ctypes.c_bool


# // Get the number of splits of the last graph
# GGML_API int                   ggml_backend_sched_get_n_splits(ggml_backend_sched_t sched);
def ggml_backend_sched_get_n_splits(
    sched: ggml_backend_sched_t,
) -> int:
    """Get the number of splits of the last graph."""
    ...


ggml_backend_sched_get_n_splits = lib.ggml_backend_sched_get_n_splits
ggml_backend_sched_get_n_splits.argtypes = [ggml_backend_sched_t_ctypes]
ggml_backend_sched_get_n_splits.restype = ctypes.c_int


# GGML_API size_t                ggml_backend_sched_get_buffer_size(ggml_backend_sched_t sched, ggml_backend_t backend);
def ggml_backend_sched_get_buffer_size(
    sched: ggml_backend_sched_t,
    backend: Union[ggml_backend_t, int],
) -> int:
    ...


ggml_backend_sched_get_buffer_size = lib.ggml_backend_sched_get_buffer_size
ggml_backend_sched_get_buffer_size.argtypes = [
    ggml_backend_sched_t_ctypes,
    ggml_backend_t_ctypes,
]
ggml_backend_sched_get_buffer_size.restype = ctypes.c_size_t


# GGML_API void                  ggml_backend_sched_set_node_backend(ggml_backend_sched_t sched, struct ggml_tensor * node, ggml_backend_t backend);
def ggml_backend_sched_set_node_backend(
    sched: ggml_backend_sched_t,
    node: ggml_tensor_p,
    backend: Union[ggml_backend_t, int],
    /,
):
    ...


ggml_backend_sched_set_node_backend = lib.ggml_backend_sched_set_node_backend
ggml_backend_sched_set_node_backend.argtypes = [
    ggml_backend_sched_t_ctypes,
    ctypes.POINTER(ggml_tensor),
    ggml_backend_t_ctypes,
]
ggml_backend_sched_set_node_backend.restype = None


# GGML_API ggml_backend_t        ggml_backend_sched_get_node_backend(ggml_backend_sched_t sched, struct ggml_tensor * node);
def ggml_backend_sched_get_node_backend(
    sched: ggml_backend_sched_t,
    node: ggml_tensor_p,
) -> Optional[ggml_backend_t]:
    ...


ggml_backend_sched_get_node_backend = lib.ggml_backend_sched_get_node_backend
ggml_backend_sched_get_node_backend.argtypes = [
    ggml_backend_sched_t_ctypes,
    ctypes.POINTER(ggml_tensor),
]
ggml_backend_sched_get_node_backend.restype = ggml_backend_t_ctypes


# // Allocate and compute graph on the backend scheduler
# GGML_API void                  ggml_backend_sched_graph_compute(ggml_backend_sched_t sched, struct ggml_cgraph * graph);
# GGML_API bool                  ggml_backend_sched_graph_compute(ggml_backend_sched_t sched, struct ggml_cgraph * graph);
def ggml_backend_sched_graph_compute(
    sched: ggml_backend_sched_t,
    graph: ggml_cgraph_p,
) -> bool:
    """Allocate and compute graph on the backend scheduler."""
    ...


ggml_backend_sched_graph_compute = lib.ggml_backend_sched_graph_compute
ggml_backend_sched_graph_compute.argtypes = [
    ggml_backend_sched_t_ctypes,
    ctypes.POINTER(ggml_cgraph),
]
ggml_backend_sched_graph_compute.restype = ctypes.c_bool


# // Reset all assignments and allocators - must be called before changing the node backends
# GGML_API void                  ggml_backend_sched_reset(ggml_backend_sched_t sched);
def ggml_backend_sched_reset(sched: ggml_backend_sched_t, /):
    """Reset all assignments and allocators - must be called before changing the node backends."""
    ...


ggml_backend_sched_reset = lib.ggml_backend_sched_reset
ggml_backend_sched_reset.argtypes = [ggml_backend_sched_t_ctypes]
ggml_backend_sched_reset.restype = None


# // Set a callback to be called for each resulting node during graph compute
# GGML_API void                  ggml_backend_sched_set_eval_callback(ggml_backend_sched_t sched, ggml_backend_sched_eval_callback callback, void * user_data);
def ggml_backend_sched_set_eval_callback(
    sched: ggml_backend_sched_t,
    callback,  # type: ignore
    user_data: Union[ctypes.c_void_p, int, None],
    /,
):
    ...


ggml_backend_sched_set_eval_callback = lib.ggml_backend_sched_set_eval_callback
ggml_backend_sched_set_eval_callback.argtypes = [
    ggml_backend_sched_t_ctypes,
    ggml_backend_sched_eval_callback,  # TODO: this may need to also accept NULL
    ctypes.c_void_p,
]
ggml_backend_sched_set_eval_callback.restype = None


# //
# // Utils
# //


# struct ggml_backend_graph_copy {
#     ggml_backend_buffer_t buffer;
#     struct ggml_context * ctx_allocated;
#     struct ggml_context * ctx_unallocated;
#     struct ggml_cgraph * graph;
# };
class ggml_backend_graph_copy(ctypes.Structure):
    _fields_ = [
        ("buffer", ggml_backend_buffer_t_ctypes),
        ("ctx_allocated", ggml_context_p_ctypes),
        ("ctx_unallocated", ggml_context_p_ctypes),
        ("graph", ctypes.POINTER(ggml_cgraph)),
    ]


ggml_backend_graph_copy_t = ggml_backend_graph_copy


# // Copy a graph to a different backend
# GGML_API struct ggml_backend_graph_copy ggml_backend_graph_copy(ggml_backend_t backend, struct ggml_cgraph * graph);
def ggml_backend_graph_copy_(
    backend: Union[ggml_backend_t, int],
    graph: ggml_cgraph_p,
) -> ggml_backend_graph_copy_t:
    ...


ggml_backend_graph_copy_ = lib.ggml_backend_graph_copy
ggml_backend_graph_copy_.argtypes = [
    ggml_backend_t_ctypes,
    ctypes.POINTER(ggml_cgraph),
]
ggml_backend_graph_copy_.restype = ggml_backend_graph_copy_t


# GGML_API void                           ggml_backend_graph_copy_free(struct ggml_backend_graph_copy copy);
def ggml_backend_graph_copy_free(copy: ggml_backend_graph_copy_t, /):
    ...


ggml_backend_graph_copy_free = lib.ggml_backend_graph_copy_free
ggml_backend_graph_copy_free.argtypes = [ggml_backend_graph_copy_t]
ggml_backend_graph_copy_free.restype = None

# typedef bool (*GGML_CALL ggml_backend_eval_callback)(int node_index, struct ggml_tensor * t1, struct ggml_tensor * t2, void * user_data);
ggml_backend_eval_callback = ctypes.CFUNCTYPE(
    ctypes.c_bool,
    ctypes.c_int,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
    ctypes.c_void_p,
)


# // Compare the output of two backends
# GGML_API bool ggml_backend_compare_graph_backend(ggml_backend_t backend1, ggml_backend_t backend2, struct ggml_cgraph * graph, ggml_backend_eval_callback callback, void * user_data);
def ggml_backend_compare_graph_backend(
    backend1: Union[ggml_backend_t, int],
    backend2: Union[ggml_backend_t, int],
    graph: ggml_cgraph_p,
    callback,  # type: ignore
    user_data: Union[ctypes.c_void_p, int, None],
) -> bool:
    ...


ggml_backend_compare_graph_backend = lib.ggml_backend_compare_graph_backend
ggml_backend_compare_graph_backend.argtypes = [
    ggml_backend_t_ctypes,
    ggml_backend_t_ctypes,
    ctypes.POINTER(ggml_cgraph),
    ggml_backend_eval_callback,
    ctypes.c_void_p,
]
ggml_backend_compare_graph_backend.restype = ctypes.c_bool


# // Tensor initialization
# GGML_API void ggml_backend_tensor_alloc(ggml_backend_buffer_t buffer, struct ggml_tensor * tensor, void * addr);
def ggml_backend_tensor_alloc(
    buffer: Union[ggml_backend_buffer_t, int],
    tensor: ggml_tensor_p,
    addr: Union[ctypes.c_void_p, int, None],
    /,
):
    ...


ggml_backend_tensor_alloc = lib.ggml_backend_tensor_alloc
ggml_backend_tensor_alloc.argtypes = [
    ggml_backend_buffer_t_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.c_void_p,
]
ggml_backend_tensor_alloc.restype = None


# GGML_API void ggml_backend_view_init(ggml_backend_buffer_t buffer, struct ggml_tensor * tensor);
def ggml_backend_view_init(
    buffer: Union[ggml_backend_buffer_t, int], tensor: ggml_tensor_p, /
):
    ...


ggml_backend_view_init = lib.ggml_backend_view_init
ggml_backend_view_init.argtypes = [
    ggml_backend_buffer_t_ctypes,
    ctypes.POINTER(ggml_tensor),
]
ggml_backend_view_init.restype = None


#####################################################
# GGML Backend Implementation API
# source: src/ggml-backend-impl.h
#####################################################

# NOTE: This API may be removed in the future from ggml-python

# //
# // Backend buffer
# //

# // buffer type
# typedef void * ggml_backend_buffer_type_context_t;
ggml_backend_buffer_type_context_t = NewType("ggml_backend_buffer_type_context_t", int)
ggml_backend_buffer_type_context_t_ctypes: TypeAlias = ctypes.c_void_p

# struct ggml_backend_buffer_type_i {
#     const char *          (*GGML_CALL get_name)        (ggml_backend_buffer_type_t buft);
#     ggml_backend_buffer_t (*GGML_CALL alloc_buffer)    (ggml_backend_buffer_type_t buft, size_t size);
#     size_t                (*GGML_CALL get_alignment)   (ggml_backend_buffer_type_t buft); // tensor alignment
#     size_t                (*GGML_CALL get_max_size)    (ggml_backend_buffer_type_t buft); // allocation max size
#     size_t                (*GGML_CALL get_alloc_size)  (ggml_backend_buffer_type_t buft, const struct ggml_tensor * tensor); // data size needed to allocate the tensor, including padding
#     bool                  (*GGML_CALL supports_backend)(ggml_backend_buffer_type_t buft, ggml_backend_t backend); // check if the buffer type is usable by the backend
#     // check if tensor data is in host memory
#     // should be equivalent to supports_backend(buft, ggml_backend_cpu_init())
#     bool                  (*GGML_CALL is_host)         (ggml_backend_buffer_type_t buft);
# };
ggml_backend_buffer_type_i_get_name = ctypes.CFUNCTYPE(
    ctypes.c_char_p, ggml_backend_buffer_type_t_ctypes
)
ggml_backend_buffer_i_alloc_buffer = ctypes.CFUNCTYPE(
    ggml_backend_buffer_t_ctypes, ggml_backend_buffer_type_t_ctypes, ctypes.c_size_t
)
ggml_backend_buffer_i_get_alignment = ctypes.CFUNCTYPE(
    ctypes.c_size_t, ggml_backend_buffer_type_t_ctypes
)
ggml_backend_buffer_i_get_max_size = ctypes.CFUNCTYPE(
    ctypes.c_size_t, ggml_backend_buffer_type_t_ctypes
)
ggml_backend_buffer_i_get_alloc_size = ctypes.CFUNCTYPE(
    ctypes.c_size_t, ggml_backend_buffer_type_t_ctypes, ctypes.POINTER(ggml_tensor)
)
ggml_backend_buffer_i_supports_backend = ctypes.CFUNCTYPE(
    ctypes.c_bool, ggml_backend_buffer_type_t_ctypes, ggml_backend_t_ctypes
)
ggml_backend_buffer_i_is_host = ctypes.CFUNCTYPE(
    ctypes.c_bool, ggml_backend_buffer_type_t_ctypes
)


class ggml_backend_buffer_type_i(ctypes.Structure):
    _fields_ = [
        ("get_name", ggml_backend_buffer_type_i_get_name),
        ("alloc_buffer", ggml_backend_buffer_i_alloc_buffer),
        ("get_alignment", ggml_backend_buffer_i_get_alignment),
        ("get_max_size", ggml_backend_buffer_i_get_max_size),
        ("get_alloc_size", ggml_backend_buffer_i_get_alloc_size),
        ("supports_backend", ggml_backend_buffer_i_supports_backend),
        ("is_host", ggml_backend_buffer_i_is_host),
    ]


# struct ggml_backend_buffer_type {
#     struct ggml_backend_buffer_type_i  iface;
#     ggml_backend_buffer_type_context_t context;
# };
class ggml_backend_buffer_type(ctypes.Structure):
    _fields_ = [
        ("iface", ggml_backend_buffer_type_i),
        ("context", ggml_backend_buffer_type_context_t_ctypes),
    ]


# typedef void * ggml_backend_buffer_context_t;
ggml_backend_buffer_context_t = NewType("ggml_backend_buffer_context_t", int)
ggml_backend_buffer_context_t_ctypes: TypeAlias = ctypes.c_void_p


# struct ggml_backend_buffer_i {
#     const char * (*GGML_CALL get_name)   (ggml_backend_buffer_t buffer);
#     void         (*GGML_CALL free_buffer)(ggml_backend_buffer_t buffer);
#     void *       (*GGML_CALL get_base)   (ggml_backend_buffer_t buffer);
#     void         (*GGML_CALL init_tensor)(ggml_backend_buffer_t buffer, struct ggml_tensor * tensor);
#     void         (*GGML_CALL set_tensor) (ggml_backend_buffer_t buffer,       struct ggml_tensor * tensor, const void * data, size_t offset, size_t size);
#     void         (*GGML_CALL get_tensor) (ggml_backend_buffer_t buffer, const struct ggml_tensor * tensor,       void * data, size_t offset, size_t size);
#     bool         (*GGML_CALL cpy_tensor) (ggml_backend_buffer_t buffer, const struct ggml_tensor * src, struct ggml_tensor * dst); // dst is in the buffer, src may be in any buffer
#     void         (*GGML_CALL clear)      (ggml_backend_buffer_t buffer, uint8_t value);
#     void         (*GGML_CALL reset)      (ggml_backend_buffer_t buffer); // reset any internal state due to tensor initialization, such as tensor extras
# };
ggml_backend_buffer_i_get_name = ctypes.CFUNCTYPE(
    ctypes.c_char_p, ggml_backend_buffer_t_ctypes
)
ggml_backend_buffer_i_free_buffer = ctypes.CFUNCTYPE(None, ggml_backend_buffer_t_ctypes)
ggml_backend_buffer_i_get_base = ctypes.CFUNCTYPE(
    ctypes.c_void_p, ggml_backend_buffer_t_ctypes
)
ggml_backend_buffer_i_init_tensor = ctypes.CFUNCTYPE(
    None, ggml_backend_buffer_t_ctypes, ctypes.POINTER(ggml_tensor)
)
ggml_backend_buffer_i_set_tensor = ctypes.CFUNCTYPE(
    None,
    ggml_backend_buffer_t_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.c_void_p,
    ctypes.c_size_t,
    ctypes.c_size_t,
)
ggml_backend_buffer_i_get_tensor = ctypes.CFUNCTYPE(
    None,
    ggml_backend_buffer_t_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.c_void_p,
    ctypes.c_size_t,
    ctypes.c_size_t,
)
ggml_backend_buffer_i_cpy_tensor = ctypes.CFUNCTYPE(
    ctypes.c_bool,
    ggml_backend_buffer_t_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
)
ggml_backend_buffer_i_clear = ctypes.CFUNCTYPE(
    None, ggml_backend_buffer_t_ctypes, ctypes.c_uint8
)
ggml_backend_buffer_i_reset = ctypes.CFUNCTYPE(None, ggml_backend_buffer_t_ctypes)


class ggml_backend_buffer_i(ctypes.Structure):
    _fields_ = [
        ("get_name", ggml_backend_buffer_i_get_name),
        ("free_buffer", ggml_backend_buffer_i_free_buffer),
        ("get_base", ggml_backend_buffer_i_get_base),
        ("init_tensor", ggml_backend_buffer_i_init_tensor),
        ("set_tensor", ggml_backend_buffer_i_set_tensor),
        ("get_tensor", ggml_backend_buffer_i_get_tensor),
        ("cpy_tensor", ggml_backend_buffer_i_cpy_tensor),
        ("clear", ggml_backend_buffer_i_clear),
        ("reset", ggml_backend_buffer_i_reset),
    ]


# struct ggml_backend_buffer {
#     struct ggml_backend_buffer_i  iface;
#     ggml_backend_buffer_type_t    buft;
#     ggml_backend_buffer_context_t context;
#     size_t size;
#     enum ggml_backend_buffer_usage usage;
# };
class ggml_backend_buffer(ctypes.Structure):
    _fields_ = [
        ("iface", ggml_backend_buffer_i),
        ("buft", ggml_backend_buffer_type_t_ctypes),
        ("context", ggml_backend_buffer_context_t_ctypes),
        ("size", ctypes.c_size_t),
    ]


# GGML_CALL ggml_backend_buffer_t ggml_backend_buffer_init(
#                ggml_backend_buffer_type_t      buft,
#         struct ggml_backend_buffer_i           iface,
#                ggml_backend_buffer_context_t   context,
#                size_t                          size);
def ggml_backend_buffer_init(
    buft: Union[ggml_backend_buffer_type_t, int],
    iface: ggml_backend_buffer_i,
    context: ggml_backend_buffer_context_t,
    size: Union[ctypes.c_size_t, int],
) -> Optional[ggml_backend_buffer_t]:
    ...


ggml_backend_buffer_init = lib.ggml_backend_buffer_init
ggml_backend_buffer_init.argtypes = [
    ggml_backend_buffer_type_t_ctypes,
    ggml_backend_buffer_i,
    ggml_backend_buffer_context_t_ctypes,
    ctypes.c_size_t,
]
ggml_backend_buffer_init.restype = ggml_backend_buffer_t_ctypes


# // do not use directly, use ggml_backend_tensor_copy instead
# bool ggml_backend_buffer_copy_tensor(const struct ggml_tensor * src, struct ggml_tensor * dst);
def ggml_backend_buffer_copy_tensor(
    src: ggml_tensor_p,
    dst: ggml_tensor_p,
) -> bool:
    ...


ggml_backend_buffer_copy_tensor = lib.ggml_backend_buffer_copy_tensor
ggml_backend_buffer_copy_tensor.argtypes = [
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
]
ggml_backend_buffer_copy_tensor.restype = ctypes.c_bool


# // buffer that contains a collection of buffers
# GGML_CALL ggml_backend_buffer_t ggml_backend_multi_buffer_alloc_buffer(ggml_backend_buffer_t * buffers, size_t n_buffers);
# GGML_CALL bool                  ggml_backend_buffer_is_multi_buffer(ggml_backend_buffer_t buffer);
# GGML_CALL void                  ggml_backend_multi_buffer_set_usage(ggml_backend_buffer_t buffer, enum ggml_backend_buffer_usage usage);
def ggml_backend_multi_buffer_alloc_buffer(
    buffers: "ctypes._Pointer(ggml_backend_buffer_t)",  # type: ignore
    n_buffers: Union[ctypes.c_size_t, int],
) -> Optional[ggml_backend_buffer_t]:
    ...


ggml_backend_multi_buffer_alloc_buffer = lib.ggml_backend_multi_buffer_alloc_buffer
ggml_backend_multi_buffer_alloc_buffer.argtypes = [
    ctypes.POINTER(ggml_backend_buffer_t_ctypes),
    ctypes.c_size_t,
]
ggml_backend_multi_buffer_alloc_buffer.restype = ggml_backend_buffer_t_ctypes


# //
# // Backend
# //

# typedef void * ggml_backend_context_t;
ggml_backend_context_t = NewType("ggml_backend_context_t", int)
ggml_backend_context_t_ctypes: TypeAlias = ctypes.c_void_p


# struct ggml_backend_i {
#     const char * (*GGML_CALL get_name)(ggml_backend_t backend);

#     void (*GGML_CALL free)(ggml_backend_t backend);

#     // buffer allocation
#     ggml_backend_buffer_type_t (*GGML_CALL get_default_buffer_type)(ggml_backend_t backend);

#     // (optional) asynchronous tensor data access
#     void (*GGML_CALL set_tensor_async)(ggml_backend_t backend,       struct ggml_tensor * tensor, const void * data, size_t offset, size_t size);
#     void (*GGML_CALL get_tensor_async)(ggml_backend_t backend, const struct ggml_tensor * tensor,       void * data, size_t offset, size_t size);
#     bool (*GGML_CALL cpy_tensor_async)(ggml_backend_t backend, const struct ggml_tensor * src, struct ggml_tensor * dst);

#     // (optional) complete all pending operations
#     void (*GGML_CALL synchronize)(ggml_backend_t backend);

#     // compute graph with a plan
#     ggml_backend_graph_plan_t (*GGML_CALL graph_plan_create) (ggml_backend_t backend, const struct ggml_cgraph * cgraph);
#     void                      (*GGML_CALL graph_plan_free)   (ggml_backend_t backend, ggml_backend_graph_plan_t plan);
#     void                      (*GGML_CALL graph_plan_compute)(ggml_backend_t backend, ggml_backend_graph_plan_t plan);

#     // compute graph without a plan (async)
#     bool (*GGML_CALL graph_compute)(ggml_backend_t backend, struct ggml_cgraph * cgraph);

#     // check if the backend supports an operation
#     bool (*GGML_CALL supports_op)(ggml_backend_t backend, const struct ggml_tensor * op);
# };
ggml_backend_i_get_name = ctypes.CFUNCTYPE(ctypes.c_char_p, ggml_backend_t_ctypes)
ggml_backend_i_free = ctypes.CFUNCTYPE(None, ggml_backend_t_ctypes)
ggml_backend_i_get_default_buffer_type = ctypes.CFUNCTYPE(
    ggml_backend_buffer_type_t_ctypes, ggml_backend_t_ctypes
)
ggml_backend_i_set_tensor_async = ctypes.CFUNCTYPE(
    None,
    ggml_backend_t_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.c_void_p,
    ctypes.c_size_t,
    ctypes.c_size_t,
)
ggml_backend_i_get_tensor_async = ctypes.CFUNCTYPE(
    None,
    ggml_backend_t_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.c_void_p,
    ctypes.c_size_t,
    ctypes.c_size_t,
)
ggml_backend_i_cpy_tensor_async = ctypes.CFUNCTYPE(
    ctypes.c_bool,
    ggml_backend_t_ctypes,
    ctypes.POINTER(ggml_tensor),
    ctypes.POINTER(ggml_tensor),
)
ggml_backend_i_synchronize = ctypes.CFUNCTYPE(None, ggml_backend_t_ctypes)
ggml_backend_i_graph_plan_create = ctypes.CFUNCTYPE(
    ggml_backend_graph_plan_t_ctypes, ggml_backend_t_ctypes, ctypes.POINTER(ggml_cgraph)
)
ggml_backend_i_graph_plan_free = ctypes.CFUNCTYPE(
    None, ggml_backend_t_ctypes, ggml_backend_graph_plan_t_ctypes
)
ggml_backend_i_graph_plan_compute = ctypes.CFUNCTYPE(
    None, ggml_backend_t_ctypes, ggml_backend_graph_plan_t_ctypes
)
ggml_backend_i_graph_compute = ctypes.CFUNCTYPE(
    ctypes.c_bool, ggml_backend_t_ctypes, ctypes.POINTER(ggml_cgraph)
)
ggml_backend_i_supports_op = ctypes.CFUNCTYPE(
    ctypes.c_bool, ggml_backend_t_ctypes, ctypes.POINTER(ggml_tensor)
)


class ggml_backend_i(ctypes.Structure):
    _fields_ = [
        ("get_name", ggml_backend_i_get_name),
        ("free", ggml_backend_i_free),
        ("get_default_buffer_type", ggml_backend_i_get_default_buffer_type),
        ("set_tensor_async", ggml_backend_i_set_tensor_async),
        ("get_tensor_async", ggml_backend_i_get_tensor_async),
        ("cpy_tensor_async", ggml_backend_i_cpy_tensor_async),
        ("synchronize", ggml_backend_i_synchronize),
        ("graph_plan_create", ggml_backend_i_graph_plan_create),
        ("graph_plan_free", ggml_backend_i_graph_plan_free),
        ("graph_plan_compute", ggml_backend_i_graph_plan_compute),
        ("graph_compute", ggml_backend_i_graph_compute),
        ("supports_op", ggml_backend_i_supports_op),
    ]


# struct ggml_backend {
#     struct ggml_backend_i iface;


#     ggml_backend_context_t context;
# };
class ggml_backend(ctypes.Structure):
    _fields_ = [
        ("iface", ggml_backend_i),
        ("context", ggml_backend_context_t_ctypes),
    ]


# //
# // Backend registry
# //

# typedef ggml_backend_t (*GGML_CALL ggml_backend_init_fn)(const char * params, void * user_data);
ggml_backend_init_fn = ctypes.CFUNCTYPE(
    ggml_backend_t_ctypes, ctypes.c_char_p, ctypes.c_void_p
)


# GGML_CALL void ggml_backend_register(const char * name, ggml_backend_init_fn init_fn, ggml_backend_buffer_type_t default_buffer_type, void * user_data);
def ggml_backend_register(
    name: bytes,
    init_fn,  # type: ignore
    default_buffer_type: Union[ggml_backend_buffer_type_t, int],
    user_data: Union[ctypes.c_void_p, int, None],
):
    ...


ggml_backend_register = lib.ggml_backend_register
ggml_backend_register.argtypes = [
    ctypes.c_char_p,
    ggml_backend_init_fn,
    ggml_backend_buffer_type_t_ctypes,
    ctypes.c_void_p,
]
ggml_backend_register.restype = None

#####################################################
# GGML CUDA API
# source: src/ggml-cuda.h
#####################################################


GGML_USE_CUBLAS = hasattr(lib, "ggml_init_cublas")


GGML_CUDA_MAX_DEVICES = 16


# // Always success. To check if CUDA is actually loaded, use `ggml_cublas_loaded`.
# GGML_API GGML_CALL void   ggml_init_cublas(void);
def ggml_init_cublas():
    ...


if GGML_USE_CUBLAS:
    ggml_init_cublas = lib.ggml_init_cublas
    ggml_init_cublas.argtypes = []
    ggml_init_cublas.restype = None


# // Returns `true` if there are available CUDA devices and cublas loads successfully; otherwise, it returns `false`.
# GGML_API GGML_CALL bool   ggml_cublas_loaded(void);
def ggml_cublas_loaded() -> bool:
    ...


if GGML_USE_CUBLAS:
    ggml_cublas_loaded = lib.ggml_cublas_loaded
    ggml_cublas_loaded.argtypes = []
    ggml_cublas_loaded.restype = ctypes.c_bool


# GGML_API GGML_CALL void * ggml_cuda_host_malloc(size_t size);
def ggml_cuda_host_malloc(
    size: Union[ctypes.c_size_t, int],
) -> Optional[int]:
    ...


if GGML_USE_CUBLAS:
    ggml_cuda_host_malloc = lib.ggml_cuda_host_malloc
    ggml_cuda_host_malloc.argtypes = [ctypes.c_size_t]
    ggml_cuda_host_malloc.restype = ctypes.c_void_p


# GGML_API GGML_CALL void   ggml_cuda_host_free(void * ptr);
def ggml_cuda_host_free(ptr: Union[ctypes.c_void_p, int, None], /):
    ...


if GGML_USE_CUBLAS:
    ggml_cuda_host_free = lib.ggml_cuda_host_free
    ggml_cuda_host_free.argtypes = [ctypes.c_void_p]
    ggml_cuda_host_free.restype = None


# GGML_API GGML_CALL bool   ggml_cuda_can_mul_mat(const struct ggml_tensor * src0, const struct ggml_tensor * src1, struct ggml_tensor * dst);
def ggml_cuda_can_mul_mat(
    src0: ggml_tensor_p,
    src1: ggml_tensor_p,
    dst: ggml_tensor_p,
) -> bool:
    ...


if GGML_USE_CUBLAS:
    ggml_cuda_can_mul_mat = lib.ggml_cuda_can_mul_mat
    ggml_cuda_can_mul_mat.argtypes = [
        ctypes.POINTER(ggml_tensor),
        ctypes.POINTER(ggml_tensor),
        ctypes.POINTER(ggml_tensor),
    ]
    ggml_cuda_can_mul_mat.restype = ctypes.c_bool


# GGML_API GGML_CALL bool   ggml_cuda_compute_forward(struct ggml_compute_params * params, struct ggml_tensor * tensor);
def ggml_cuda_compute_forward(
    params: ggml_compute_params_p,
    tensor: ggml_tensor_p,
) -> bool:
    ...


if GGML_USE_CUBLAS:
    ggml_cuda_compute_forward = lib.ggml_cuda_compute_forward
    ggml_cuda_compute_forward.argtypes = [
        ctypes.POINTER(ggml_compute_params),
        ctypes.POINTER(ggml_tensor),
    ]
    ggml_cuda_compute_forward.restype = ctypes.c_bool


# GGML_API GGML_CALL int    ggml_cuda_get_device_count(void);
def ggml_cuda_get_device_count() -> int:
    ...


if GGML_USE_CUBLAS:
    ggml_cuda_get_device_count = lib.ggml_cuda_get_device_count
    ggml_cuda_get_device_count.argtypes = []
    ggml_cuda_get_device_count.restype = ctypes.c_int


# GGML_API GGML_CALL void   ggml_cuda_get_device_description(int device, char * description, size_t description_size);
def ggml_cuda_get_device_description(
    device: Union[ctypes.c_int, int],
    description: bytes,
    description_size: Union[ctypes.c_size_t, int],
    /,
):
    ...


if GGML_USE_CUBLAS:
    ggml_cuda_get_device_description = lib.ggml_cuda_get_device_description
    ggml_cuda_get_device_description.argtypes = [
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_size_t,
    ]
    ggml_cuda_get_device_description.restype = None


# // backend API
# GGML_API GGML_CALL ggml_backend_t ggml_backend_cuda_init(int device);
def ggml_backend_cuda_init() -> Optional[ggml_backend_t]:
    ...


if GGML_USE_CUBLAS:
    ggml_backend_cuda_init = lib.ggml_backend_cuda_init
    ggml_backend_cuda_init.argtypes = []
    ggml_backend_cuda_init.restype = ggml_backend_t_ctypes


# GGML_API GGML_CALL bool ggml_backend_is_cuda(ggml_backend_t backend);
def ggml_backend_is_cuda(
    backend: Union[ggml_backend_t, int],
) -> bool:
    ...


if GGML_USE_CUBLAS:
    ggml_backend_is_cuda = lib.ggml_backend_is_cuda
    ggml_backend_is_cuda.argtypes = [ggml_backend_t_ctypes]
    ggml_backend_is_cuda.restype = ctypes.c_bool


# GGML_API GGML_CALL ggml_backend_buffer_type_t ggml_backend_cuda_buffer_type(int device);
def ggml_backend_cuda_buffer_type(
    device: Union[ctypes.c_int, int],
) -> Optional[ggml_backend_buffer_type_t]:
    ...


if GGML_USE_CUBLAS:
    ggml_backend_cuda_buffer_type = lib.ggml_backend_cuda_buffer_type
    ggml_backend_cuda_buffer_type.argtypes = [ctypes.c_int]
    ggml_backend_cuda_buffer_type.restype = ggml_backend_buffer_type_t_ctypes


# // split tensor buffer that splits matrices by rows across multiple devices
# GGML_API GGML_CALL ggml_backend_buffer_type_t ggml_backend_cuda_split_buffer_type(const float * tensor_split);
def ggml_backend_cuda_split_buffer_type(
    tensor_split: CtypesArray[ctypes.c_float],
) -> Optional[ggml_backend_buffer_type_t]:
    ...


if GGML_USE_CUBLAS:
    ggml_backend_cuda_split_buffer_type = lib.ggml_backend_cuda_split_buffer_type
    ggml_backend_cuda_split_buffer_type.argtypes = [ctypes.POINTER(ctypes.c_float)]
    ggml_backend_cuda_split_buffer_type.restype = ggml_backend_buffer_type_t_ctypes


# // pinned host buffer for use with the CPU backend for faster copies between CPU and GPU
# GGML_API GGML_CALL ggml_backend_buffer_type_t ggml_backend_cuda_host_buffer_type(void);
def ggml_backend_cuda_host_buffer_type() -> (
    Union[ggml_backend_buffer_type_t, int, None]
):
    ...


if GGML_USE_CUBLAS:
    ggml_backend_cuda_host_buffer_type = lib.ggml_backend_cuda_host_buffer_type
    ggml_backend_cuda_host_buffer_type.argtypes = []
    ggml_backend_cuda_host_buffer_type.restype = ggml_backend_buffer_type_t_ctypes


# GGML_API GGML_CALL int  ggml_backend_cuda_get_device_count(void);
def ggml_backend_cuda_get_device_count() -> int:
    ...


if GGML_USE_CUBLAS:
    ggml_backend_cuda_get_device_count = lib.ggml_backend_cuda_get_device_count
    ggml_backend_cuda_get_device_count.argtypes = []
    ggml_backend_cuda_get_device_count.restype = ctypes.c_int


# GGML_API GGML_CALL void ggml_backend_cuda_get_device_description(int device, char * description, size_t description_size);
def ggml_backend_cuda_get_device_description(
    device: Union[ctypes.c_int, int],
    description: ctypes.c_char_p,
    description_size: Union[ctypes.c_size_t, int],
    /,
):
    ...


if GGML_USE_CUBLAS:
    ggml_backend_cuda_get_device_description = (
        lib.ggml_backend_cuda_get_device_description
    )
    ggml_backend_cuda_get_device_description.argtypes = [
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_size_t,
    ]
    ggml_backend_cuda_get_device_description.restype = None


# GGML_API GGML_CALL void ggml_backend_cuda_get_device_memory(int device, size_t * free, size_t * total);
def ggml_backend_cuda_get_device_memory(
    device: Union[ctypes.c_int, int],
    free: "ctypes._Pointer[ctypes.c_size_t]",  # type: ignore
    total: "ctypes._Pointer[ctypes.c_size_t]",  # type: ignore
    /,
):
    ...


if GGML_USE_CUBLAS:
    ggml_backend_cuda_get_device_memory = lib.ggml_backend_cuda_get_device_memory
    ggml_backend_cuda_get_device_memory.argtypes = [
        ctypes.c_int,
        ctypes.POINTER(ctypes.c_size_t),
        ctypes.POINTER(ctypes.c_size_t),
    ]
    ggml_backend_cuda_get_device_memory.restype = None

#####################################################
# GGML METAL API
# source: src/ggml-metal.h
#####################################################


GGML_USE_METAL = hasattr(lib, "ggml_backend_metal_init")


# // max memory buffers that can be mapped to the device
# #define GGML_METAL_MAX_BUFFERS 64
GGML_METAL_MAX_BUFFERS = 64

# //
# // backend API
# // user-code should use only these functions
# //


# GGML_API void ggml_backend_metal_log_set_callback(ggml_log_callback log_callback, void * user_data);
def ggml_backend_metal_log_set_callback(
    log_callback, user_data: Union[ctypes.c_void_p, int, None], /  # type: ignore
):
    ...


if GGML_USE_METAL:
    ggml_backend_metal_log_set_callback = lib.ggml_backend_metal_log_set_callback
    ggml_backend_metal_log_set_callback.argtypes = [
        ggml_log_callback,
        ctypes.c_void_p,
    ]
    ggml_backend_metal_log_set_callback.restype = None


# GGML_API ggml_backend_t ggml_backend_metal_init(void);
def ggml_backend_metal_init() -> Optional[ggml_backend_t]:
    ...


if GGML_USE_METAL:
    ggml_backend_metal_init = lib.ggml_backend_metal_init
    ggml_backend_metal_init.argtypes = []
    ggml_backend_metal_init.restype = ggml_backend_t_ctypes


# GGML_API bool ggml_backend_is_metal(ggml_backend_t backend);
def ggml_backend_is_metal(
    backend: Union[ggml_backend_t, int],
) -> bool:
    ...


if GGML_USE_METAL:
    ggml_backend_is_metal = lib.ggml_backend_is_metal
    ggml_backend_is_metal.argtypes = [ggml_backend_t_ctypes]
    ggml_backend_is_metal.restype = ctypes.c_bool


# GGML_API GGML_CALL ggml_backend_buffer_t ggml_backend_metal_buffer_from_ptr(void * data, size_t size, size_t max_size);
def ggml_backend_metal_buffer_from_ptr(
    data: Union[ctypes.c_void_p, int, None],
    size: Union[ctypes.c_size_t, int],
    max_size: Union[ctypes.c_size_t, int],
) -> Optional[ggml_backend_buffer_t]:
    ...


if GGML_USE_METAL:
    ggml_backend_metal_buffer_from_ptr = lib.ggml_backend_metal_buffer_from_ptr
    ggml_backend_metal_buffer_from_ptr.argtypes = [
        ctypes.c_void_p,
        ctypes.c_size_t,
        ctypes.c_size_t,
    ]
    ggml_backend_metal_buffer_from_ptr.restype = ggml_backend_buffer_t_ctypes


# GGML_API void ggml_backend_metal_set_n_cb(ggml_backend_t backend, int n_cb);
def ggml_backend_metal_set_n_cb(
    backend: Union[ggml_backend_t, int], n_cb: Union[ctypes.c_int, int], /
):
    ...


if GGML_USE_METAL:
    ggml_backend_metal_set_n_cb = lib.ggml_backend_metal_set_n_cb
    ggml_backend_metal_set_n_cb.argtypes = [ggml_backend_t_ctypes, ctypes.c_int]
    ggml_backend_metal_set_n_cb.restype = None


# GGML_API GGML_CALL ggml_backend_buffer_type_t ggml_backend_metal_buffer_type(void);
def ggml_backend_metal_buffer_type() -> Optional[ggml_backend_buffer_type_t]:
    ...


if GGML_USE_METAL:
    ggml_backend_metal_buffer_type = lib.ggml_backend_metal_buffer_type
    ggml_backend_metal_buffer_type.argtypes = []
    ggml_backend_metal_buffer_type.restype = ggml_backend_buffer_type_t_ctypes


# // helper to check if the device supports a specific family
# // ideally, the user code should be doing these checks
# // ref: https://developer.apple.com/metal/Metal-Feature-Set-Tables.pdf
# GGML_API bool ggml_backend_metal_supports_family(ggml_backend_t backend, int family);
def ggml_backend_metal_supports_family(
    backend: Union[ggml_backend_t, int],
    family: Union[ctypes.c_int, int],
) -> bool:
    ...


if GGML_USE_METAL:
    ggml_backend_metal_supports_family = lib.ggml_backend_metal_supports_family
    ggml_backend_metal_supports_family.argtypes = [
        ggml_backend_t_ctypes,
        ctypes.c_int,
    ]
    ggml_backend_metal_supports_family.restype = ctypes.c_bool


# // capture all command buffers committed the next time `ggml_backend_graph_compute` is called
# GGML_API void ggml_backend_metal_capture_next_compute(ggml_backend_t backend);
def ggml_backend_metal_capture_next_compute(backend: Union[ggml_backend_t, int], /):
    ...


if GGML_USE_METAL:
    ggml_backend_metal_capture_next_compute = (
        lib.ggml_backend_metal_capture_next_compute
    )
    ggml_backend_metal_capture_next_compute.argtypes = [ggml_backend_t_ctypes]
    ggml_backend_metal_capture_next_compute.restype = None


#####################################################
# GGML OPENCL API
# source: ggml-opencl.h
#####################################################


GGML_USE_CLBLAST = hasattr(lib, "ggml_cl_init")


# GGML_API void ggml_cl_init(void);
def ggml_cl_init():
    ...


if GGML_USE_CLBLAST:
    ggml_cl_init = lib.ggml_cl_init
    ggml_cl_init.argtypes = []
    ggml_cl_init.restype = None


# GGML_API void   ggml_cl_mul(const struct ggml_tensor * src0, const struct ggml_tensor * src1, struct ggml_tensor * dst);
def ggml_cl_mul(src0: ggml_tensor_p, src1: ggml_tensor_p, dst: ggml_tensor_p, /):
    ...


if GGML_USE_CLBLAST:
    ggml_cl_mul = lib.ggml_cl_mul
    ggml_cl_mul.argtypes = [
        ctypes.POINTER(ggml_tensor),
        ctypes.POINTER(ggml_tensor),
        ctypes.POINTER(ggml_tensor),
    ]
    ggml_cl_mul.restype = None


# GGML_API void   ggml_cl_add(const struct ggml_tensor * src0, const struct ggml_tensor * src1, struct ggml_tensor * dst);
def ggml_cl_add(src0: ggml_tensor_p, src1: ggml_tensor_p, dst: ggml_tensor_p, /):
    ...


if GGML_USE_CLBLAST:
    ggml_cl_add = lib.ggml_cl_add
    ggml_cl_add.argtypes = [
        ctypes.POINTER(ggml_tensor),
        ctypes.POINTER(ggml_tensor),
        ctypes.POINTER(ggml_tensor),
    ]
    ggml_cl_add.restype = None


# GGML_API bool   ggml_cl_can_mul_mat(const struct ggml_tensor * src0, const struct ggml_tensor * src1, const struct ggml_tensor * dst);
def ggml_cl_can_mul_mat(
    src0: ggml_tensor_p,
    src1: ggml_tensor_p,
    dst: ggml_tensor_p,
) -> bool:
    ...


if GGML_USE_CLBLAST:
    ggml_cl_can_mul_mat = lib.ggml_cl_can_mul_mat
    ggml_cl_can_mul_mat.argtypes = [
        ctypes.POINTER(ggml_tensor),
        ctypes.POINTER(ggml_tensor),
        ctypes.POINTER(ggml_tensor),
    ]
    ggml_cl_can_mul_mat.restype = ctypes.c_bool


# GGML_API size_t ggml_cl_mul_mat_get_wsize(const struct ggml_tensor * src0, const struct ggml_tensor * src1, struct ggml_tensor * dst);
def ggml_cl_mul_mat_get_wsize(
    src0: ggml_tensor_p,
    src1: ggml_tensor_p,
    dst: ggml_tensor_p,
) -> int:
    ...


if GGML_USE_CLBLAST:
    ggml_cl_mul_mat_get_wsize = lib.ggml_cl_mul_mat_get_wsize
    ggml_cl_mul_mat_get_wsize.argtypes = [
        ctypes.POINTER(ggml_tensor),
        ctypes.POINTER(ggml_tensor),
        ctypes.POINTER(ggml_tensor),
    ]
    ggml_cl_mul_mat_get_wsize.restype = ctypes.c_size_t


# GGML_API void   ggml_cl_mul_mat(const struct ggml_tensor * src0, const struct ggml_tensor * src1, struct ggml_tensor * dst, void * wdata, size_t wsize);
def ggml_cl_mul_mat(
    src0: ggml_tensor_p,
    src1: ggml_tensor_p,
    dst: ggml_tensor_p,
    wdata: Union[ctypes.c_void_p, int, None],
    wsize: Union[ctypes.c_size_t, int],
    /,
):
    ...


if GGML_USE_CLBLAST:
    ggml_cl_mul_mat = lib.ggml_cl_mul_mat
    ggml_cl_mul_mat.argtypes = [
        ctypes.POINTER(ggml_tensor),
        ctypes.POINTER(ggml_tensor),
        ctypes.POINTER(ggml_tensor),
        ctypes.c_void_p,
        ctypes.c_size_t,
    ]
    ggml_cl_mul_mat.restype = None


# GGML_API void ggml_cl_free_data(const struct ggml_tensor* tensor);
def ggml_cl_free_data(tensor: ggml_tensor_p, /):
    ...


if GGML_USE_CLBLAST:
    ggml_cl_free_data = lib.ggml_cl_free_data
    ggml_cl_free_data.argtypes = [
        ctypes.POINTER(ggml_tensor),
    ]
    ggml_cl_free_data.restype = None


# GGML_API void ggml_cl_transform_tensor(void * data, struct ggml_tensor * tensor);
def ggml_cl_transform_tensor(
    data: Union[ctypes.c_void_p, int, None], tensor: ggml_tensor_p, /
):
    ...


if GGML_USE_CLBLAST:
    ggml_cl_transform_tensor = lib.ggml_cl_transform_tensor
    ggml_cl_transform_tensor.argtypes = [
        ctypes.c_void_p,
        ctypes.POINTER(ggml_tensor),
    ]
    ggml_cl_transform_tensor.restype = None

# // backend API

# // GGML_API ggml_backend_t ggml_backend_opencl_init(void);

# // GGML_API bool ggml_backend_is_opencl(ggml_backend_t backend);


# GGML_API ggml_backend_buffer_type_t ggml_backend_opencl_buffer_type(void);
# // GGML_API ggml_backend_buffer_type_t ggml_backend_opencl_host_buffer_type(void);
def ggml_backend_opencl_host_buffer_type() -> (
    Union[ggml_backend_buffer_type_t, int, None]
):
    ...


if GGML_USE_CLBLAST:
    ggml_backend_opencl_host_buffer_type = lib.ggml_backend_opencl_host_buffer_type
    ggml_backend_opencl_host_buffer_type.argtypes = []
    ggml_backend_opencl_host_buffer_type.restype = ggml_backend_buffer_type_t_ctypes


# TODO: Add ggml-quants.h

#####################################################
# GGML Vulkan API
# source: src/ggml-vulkan.h
#####################################################

GGML_HAS_VULKAN = hasattr(lib, "ggml_vk_init_cpu_assist")

# #define GGML_VK_NAME "Vulkan"
# #define GGML_VK_MAX_DEVICES 16
GGML_VK_NAME = "Vulkan"
GGML_VK_MAX_DEVICES = 16


# GGML_API void ggml_vk_init_cpu_assist(void);
def ggml_vk_init_cpu_assist():
    ...


if GGML_HAS_VULKAN:
    ggml_vk_init_cpu_assist = lib.ggml_vk_init_cpu_assist
    ggml_vk_init_cpu_assist.argtypes = []
    ggml_vk_init_cpu_assist.restype = None


# GGML_API void ggml_vk_preallocate_buffers_graph_cpu_assist(struct ggml_tensor * node);
def ggml_vk_preallocate_buffers_graph_cpu_assist(node: ggml_tensor_p, /):
    ...


if GGML_HAS_VULKAN:
    ggml_vk_preallocate_buffers_graph_cpu_assist = (
        lib.ggml_vk_preallocate_buffers_graph_cpu_assist
    )
    ggml_vk_preallocate_buffers_graph_cpu_assist.argtypes = [
        ctypes.POINTER(ggml_tensor)
    ]
    ggml_vk_preallocate_buffers_graph_cpu_assist.restype = None


# GGML_API void ggml_vk_preallocate_buffers_cpu_assist(void);
def ggml_vk_preallocate_buffers_cpu_assist():
    ...


if GGML_HAS_VULKAN:
    ggml_vk_preallocate_buffers_cpu_assist = lib.ggml_vk_preallocate_buffers_cpu_assist
    ggml_vk_preallocate_buffers_cpu_assist.argtypes = []
    ggml_vk_preallocate_buffers_cpu_assist.restype = None


# GGML_API void ggml_vk_build_graph_cpu_assist(struct ggml_tensor * node, bool last_node);
def ggml_vk_build_graph_cpu_assist(node: ggml_tensor_p, last_node: bool, /):
    ...


if GGML_HAS_VULKAN:
    ggml_vk_build_graph_cpu_assist = lib.ggml_vk_build_graph_cpu_assist
    ggml_vk_build_graph_cpu_assist.argtypes = [
        ctypes.POINTER(ggml_tensor),
        ctypes.c_bool,
    ]
    ggml_vk_build_graph_cpu_assist.restype = None


# GGML_API bool ggml_vk_compute_forward_cpu_assist(struct ggml_compute_params * params, struct ggml_tensor * tensor);
def ggml_vk_compute_forward_cpu_assist(
    params: ggml_compute_params_p, tensor: ggml_tensor_p, /
) -> bool:
    ...


if GGML_HAS_VULKAN:
    ggml_vk_compute_forward_cpu_assist = lib.ggml_vk_compute_forward_cpu_assist
    ggml_vk_compute_forward_cpu_assist.argtypes = [
        ctypes.POINTER(ggml_compute_params),
        ctypes.POINTER(ggml_tensor),
    ]
    ggml_vk_compute_forward_cpu_assist.restype = ctypes.c_bool

# #ifdef GGML_VULKAN_CHECK_RESULTS
# void ggml_vk_check_results_1_cpu_assist(struct ggml_compute_params * params, struct ggml_tensor * tensor);
# #endif


# GGML_API void ggml_vk_graph_cleanup_cpu_assist(void);
def ggml_vk_graph_cleanup_cpu_assist():
    ...


if GGML_HAS_VULKAN:
    ggml_vk_graph_cleanup_cpu_assist = lib.ggml_vk_graph_cleanup_cpu_assist
    ggml_vk_graph_cleanup_cpu_assist.argtypes = []
    ggml_vk_graph_cleanup_cpu_assist.restype = None


# GGML_API void ggml_vk_free_cpu_assist(void);
def ggml_vk_free_cpu_assist():
    ...


if GGML_HAS_VULKAN:
    ggml_vk_free_cpu_assist = lib.ggml_vk_free_cpu_assist
    ggml_vk_free_cpu_assist.argtypes = []
    ggml_vk_free_cpu_assist.restype = None


# // backend API
# GGML_API GGML_CALL ggml_backend_t ggml_backend_vk_init(size_t dev_num);
def ggml_backend_vk_init(
    dev_num: Union[ctypes.c_size_t, int], /
) -> Optional[ggml_backend_t]:
    ...


if GGML_HAS_VULKAN:
    ggml_backend_vk_init = lib.ggml_backend_vk_init
    ggml_backend_vk_init.argtypes = [ctypes.c_size_t]
    ggml_backend_vk_init.restype = ggml_backend_t_ctypes


# GGML_API GGML_CALL bool ggml_backend_is_vk(ggml_backend_t backend);
def ggml_backend_is_vk(backend: Union[ggml_backend_t, int], /) -> bool:
    ...


if GGML_HAS_VULKAN:
    ggml_backend_is_vk = lib.ggml_backend_is_vk
    ggml_backend_is_vk.argtypes = [ggml_backend_t_ctypes]
    ggml_backend_is_vk.restype = ctypes.c_bool


# GGML_API GGML_CALL int  ggml_backend_vk_get_device_count(void);
def ggml_backend_vk_get_device_count() -> int:
    ...


if GGML_HAS_VULKAN:
    ggml_backend_vk_get_device_count = lib.ggml_backend_vk_get_device_count
    ggml_backend_vk_get_device_count.argtypes = []
    ggml_backend_vk_get_device_count.restype = ctypes.c_int


# GGML_API GGML_CALL void ggml_backend_vk_get_device_description(int device, char * description, size_t description_size);
def ggml_backend_vk_get_device_description(
    device: Union[ctypes.c_int, int],
    description: bytes,
    description_size: Union[ctypes.c_size_t, int],
    /,
):
    ...


if GGML_HAS_VULKAN:
    ggml_backend_vk_get_device_description = lib.ggml_backend_vk_get_device_description
    ggml_backend_vk_get_device_description.argtypes = [
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_size_t,
    ]
    ggml_backend_vk_get_device_description.restype = None


# GGML_API GGML_CALL void ggml_backend_vk_get_device_memory(int device, size_t * free, size_t * total);
def ggml_backend_vk_get_device_memory(
    device: Union[ctypes.c_int, int],
    free: "ctypes._Pointer[ctypes.c_size_t]",  # type: ignore
    total: "ctypes._Pointer[ctypes.c_size_t]",  # type: ignore
    /,
):
    ...


if GGML_HAS_VULKAN:
    ggml_backend_vk_get_device_memory = lib.ggml_backend_vk_get_device_memory
    ggml_backend_vk_get_device_memory.argtypes = [
        ctypes.c_int,
        ctypes.POINTER(ctypes.c_size_t),
        ctypes.POINTER(ctypes.c_size_t),
    ]
    ggml_backend_vk_get_device_memory.restype = None


# GGML_API GGML_CALL ggml_backend_buffer_type_t ggml_backend_vk_buffer_type(size_t dev_num);
def ggml_backend_vk_buffer_type(
    dev_num: Union[ctypes.c_size_t, int], /
) -> Optional[ggml_backend_buffer_type_t]:
    ...


if GGML_HAS_VULKAN:
    ggml_backend_vk_buffer_type = lib.ggml_backend_vk_buffer_type
    ggml_backend_vk_buffer_type.argtypes = [ctypes.c_size_t]
    ggml_backend_vk_buffer_type.restype = ggml_backend_buffer_type_t_ctypes


# // pinned host buffer for use with the CPU backend for faster copies between CPU and GPU
# GGML_API GGML_CALL ggml_backend_buffer_type_t ggml_backend_vk_host_buffer_type(void);
def ggml_backend_vk_host_buffer_type() -> Optional[ggml_backend_buffer_type_t]:
    ...


if GGML_HAS_VULKAN:
    ggml_backend_vk_host_buffer_type = lib.ggml_backend_vk_host_buffer_type
    ggml_backend_vk_host_buffer_type.argtypes = []
    ggml_backend_vk_host_buffer_type.restype = ggml_backend_buffer_type_t_ctypes

# TODO: Add ggml-sycl.h

# TODO: Add ggml-kompute.h
