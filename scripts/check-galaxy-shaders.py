"""Compile the actual WebGL 1 shaders using an EGL/OpenGL ES 2 context.

Optional Linux check, requires Mesa libEGL (no Python dependencies).
This validates GLSL compilation/linkage; it does not replace browser QA.
"""
from pathlib import Path
import ctypes as C
import ctypes.util
import re

root = Path(__file__).resolve().parents[1]
egl = C.CDLL(ctypes.util.find_library('EGL'))
def bind(name, result, *arguments):
    function = getattr(egl, name)
    function.restype, function.argtypes = result, arguments
    return function
get_proc = bind('eglGetProcAddress', C.c_void_p, C.c_char_p)
platform = C.CFUNCTYPE(C.c_void_p, C.c_uint, C.c_void_p, C.POINTER(C.c_int))(get_proc(b'eglGetPlatformDisplayEXT'))
display = platform(0x31DD, None, None)  # EGL_PLATFORM_SURFACELESS_MESA
initialize = bind('eglInitialize', C.c_uint, C.c_void_p, C.c_void_p, C.c_void_p)
assert initialize(display, None, None), 'EGL initialization failed'
bind('eglBindAPI', C.c_uint, C.c_uint)(0x30A0)  # OPENGL_ES_API
attributes = (C.c_int * 13)(0x3024,8,0x3023,8,0x3022,8,0x3033,1,0x3040,4,0x3025,24,0x3038)
config, count = C.c_void_p(), C.c_int()
choose = bind('eglChooseConfig', C.c_uint, C.c_void_p, C.POINTER(C.c_int), C.POINTER(C.c_void_p), C.c_int, C.POINTER(C.c_int))
assert choose(display,attributes,C.byref(config),1,C.byref(count)) and count.value
context = bind('eglCreateContext', C.c_void_p,C.c_void_p,C.c_void_p,C.c_void_p,C.POINTER(C.c_int))(display,config,None,(C.c_int*3)(0x3098,2,0x3038))
surface = bind('eglCreatePbufferSurface',C.c_void_p,C.c_void_p,C.c_void_p,C.POINTER(C.c_int))(display,config,(C.c_int*5)(0x3057,16,0x3056,16,0x3038))
assert context and surface
assert bind('eglMakeCurrent',C.c_uint,C.c_void_p,C.c_void_p,C.c_void_p,C.c_void_p)(display,surface,surface,context)
def gl(name, result, *arguments):
    return C.CFUNCTYPE(result,*arguments)(get_proc(name.encode()))
create = gl('glCreateShader',C.c_uint,C.c_uint)
source = gl('glShaderSource',None,C.c_uint,C.c_int,C.POINTER(C.c_char_p),C.c_void_p)
compile_shader = gl('glCompileShader',None,C.c_uint)
get_shader = gl('glGetShaderiv',None,C.c_uint,C.c_uint,C.POINTER(C.c_int))
shader_log = gl('glGetShaderInfoLog',None,C.c_uint,C.c_int,C.c_void_p,C.c_void_p)
program = gl('glCreateProgram',C.c_uint)
attach = gl('glAttachShader',None,C.c_uint,C.c_uint)
link = gl('glLinkProgram',None,C.c_uint)
get_program = gl('glGetProgramiv',None,C.c_uint,C.c_uint,C.POINTER(C.c_int))
program_log = gl('glGetProgramInfoLog',None,C.c_uint,C.c_int,C.c_void_p,C.c_void_p)
text = (root/'src/galaxy-scene.js').read_text()
for name in ['point','mesh','line']:
    handle = program()
    for suffix,kind in [('Vertex',0x8B31),('Fragment',0x8B30)]:
        code = re.search(r'const '+name+suffix+r'=`(.*?)`;',text,re.S).group(1).encode()
        shader=create(kind);ptr=C.c_char_p(code);source(shader,1,C.byref(ptr),None);compile_shader(shader)
        ok=C.c_int();get_shader(shader,0x8B81,C.byref(ok));log=C.create_string_buffer(8192)
        shader_log(shader,len(log),None,log);assert ok.value,(name+suffix,log.value.decode())
        attach(handle,shader);gl('glDeleteShader',None,C.c_uint)(shader)
    link(handle);ok=C.c_int();get_program(handle,0x8B82,C.byref(ok));log=C.create_string_buffer(8192)
    program_log(handle,len(log),None,log);assert ok.value,(name,log.value.decode())
    gl('glDeleteProgram',None,C.c_uint)(handle)
    print(name+': shaders compiled and program linked')
bind('eglMakeCurrent',C.c_uint,C.c_void_p,C.c_void_p,C.c_void_p,C.c_void_p)(display,None,None,None)
bind('eglDestroySurface',C.c_uint,C.c_void_p,C.c_void_p)(display,surface)
bind('eglDestroyContext',C.c_uint,C.c_void_p,C.c_void_p)(display,context)
bind('eglTerminate',C.c_uint,C.c_void_p)(display)
