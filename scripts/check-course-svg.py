"""Compare original and build SVG pixels with librsvg and Cairo (Linux QA)."""
from pathlib import Path
import concurrent.futures
import ctypes as C
import ctypes.util
import json

ROOT = Path(__file__).resolve().parents[1]


def raster(data):
    rsvg = C.CDLL(ctypes.util.find_library('rsvg-2'))
    cairo = C.CDLL(ctypes.util.find_library('cairo'))
    gobject = C.CDLL(ctypes.util.find_library('gobject-2.0'))
    rsvg.rsvg_handle_new_from_data.argtypes = [C.c_void_p, C.c_size_t, C.c_void_p]
    rsvg.rsvg_handle_new_from_data.restype = C.c_void_p
    rsvg.rsvg_handle_render_document.argtypes = [C.c_void_p, C.c_void_p, C.c_void_p, C.c_void_p]
    rsvg.rsvg_handle_render_document.restype = C.c_int
    cairo.cairo_image_surface_create.argtypes = [C.c_int, C.c_int, C.c_int]
    cairo.cairo_image_surface_create.restype = C.c_void_p
    cairo.cairo_create.argtypes = [C.c_void_p]
    cairo.cairo_create.restype = C.c_void_p
    cairo.cairo_image_surface_get_data.argtypes = [C.c_void_p]
    cairo.cairo_image_surface_get_data.restype = C.c_void_p
    for name in ['cairo_surface_flush', 'cairo_destroy', 'cairo_surface_destroy']:
        getattr(cairo, name).argtypes = [C.c_void_p]
    gobject.g_object_unref.argtypes = [C.c_void_p]
    width, height = 1134, 709
    handle = rsvg.rsvg_handle_new_from_data(data, len(data), None)
    if not handle:
        raise ValueError('SVG parse failed')
    surface = cairo.cairo_image_surface_create(0, width, height)
    context = cairo.cairo_create(surface)
    viewport = (C.c_double * 4)(0, 0, width, height)
    try:
        if not rsvg.rsvg_handle_render_document(handle, context, viewport, None):
            raise ValueError('SVG render failed')
        cairo.cairo_surface_flush(surface)
        return C.string_at(cairo.cairo_image_surface_get_data(surface), width * height * 4)
    finally:
        cairo.cairo_destroy(context)
        cairo.cairo_surface_destroy(surface)
        gobject.g_object_unref(handle)


def compare(relative):
    before = (ROOT / relative).read_bytes()
    after = (ROOT / 'dist' / relative).read_bytes()
    if raster(before) != raster(after):
        raise AssertionError('SVG rendering changed: ' + relative)
    return len(before) - len(after)


if __name__ == '__main__':
    files = sorted(str(f.relative_to(ROOT / 'dist'))
                   for folder in ['assets/slides', 'assets/visuals']
                   for f in (ROOT / 'dist' / folder).rglob('*.svg'))
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as pool:
        saved = sum(pool.map(compare, files))
    result = dict(files=len(files), identical_raster=True, width=1134, height=709,
                  bytes_saved=saved, backend='librsvg and Cairo',
                  scope='Every course slide and visual panel included in the build; original sources unchanged')
    (ROOT / 'qa/svg-compaction.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))
