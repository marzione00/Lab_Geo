"""Seamless surface textures of the notable objects (asteroid regolith and comet crust).

Spectral synthesis: a random spectrum with a power-law amplitude is transformed back with the inverse FFT, so
every field is periodic and the texture tiles without seams. Craters and pits are placed on the torus with wrap.
RGB holds the albedo (sRGB), alpha a height field used by the shaders for relief lighting.
Output: assets/space/objects/<name>-4k.webp (4096 x 4096) and <name>.webp (2048 x 2048, Lanczos).

Requires NumPy and Pillow. Deterministic for a given seed.
"""
from pathlib import Path
import argparse

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/space/objects'


def spectral(n, beta, rng, low=1.0):
    """Periodic Gaussian field with amplitude spectrum k^-beta, normalised to zero mean and unit variance."""
    k = np.fft.fftfreq(n).astype(np.float32) * n
    kx, ky = np.meshgrid(k, k, indexing='xy')
    kk = np.sqrt(kx * kx + ky * ky)
    kk[0, 0] = 1.0
    amp = (np.maximum(kk, low) ** -beta).astype(np.float32)
    amp[0, 0] = 0.0
    phase = rng.random((n, n), dtype=np.float32) * np.float32(2 * np.pi)
    spec = amp * (np.cos(phase) + 1j * np.sin(phase)).astype(np.complex64)
    field = np.fft.ifft2(spec).real.astype(np.float32)
    field -= field.mean()
    field /= field.std() + 1e-9
    return field


def craters(height, rng, count, rmin, rmax, slope=2.2, depth=0.6):
    """Bowl-shaped craters with raised rims, sizes from a power law, placed with periodic wrap."""
    n = height.shape[0]
    u = rng.random(count)
    radii = (rmin ** (1 - slope) + u * (rmax ** (1 - slope) - rmin ** (1 - slope))) ** (1 / (1 - slope))
    for r in np.sort(radii)[::-1]:
        cx, cy = rng.random(2) * n
        span = int(np.ceil(r * 2.6))
        xs = (np.arange(int(cx) - span, int(cx) + span + 1)) % n
        ys = (np.arange(int(cy) - span, int(cy) + span + 1)) % n
        gx, gy = np.meshgrid(np.arange(-span, span + 1) + (int(cx) - cx), np.arange(-span, span + 1) + (int(cy) - cy))
        d = np.sqrt(gx * gx + gy * gy) / r
        prof = np.where(d < 1, (d * d - 1) * depth + 0.08 * d ** 6, 0.09 * np.exp(-((d - 1) * 3.6) ** 2))
        prof *= np.clip(2.6 - d, 0, 1)
        height[np.ix_(ys, xs)] += (prof * (r / rmax) ** 0.55).astype(np.float32)


def normalise(a):
    a = a - a.min()
    return a / (a.max() + 1e-9)


def regolith(n, seed):
    rng = np.random.default_rng(seed)
    # Detail texture: the large-scale shape comes from the mesh, so the lowest frequencies are flattened.
    h = spectral(n, 1.35, rng, low=10) * 0.32 + spectral(n, 0.85, rng, low=3) * 0.1
    craters(h, rng, int(3600 * (n / 4096) ** 2), n / 700, n / 11, depth=1.3)
    pebbles = spectral(n, 0.85, rng, low=48)
    h += np.clip(pebbles - 1.4, 0, None) * 0.3
    h = normalise(h)
    gx, gy = np.gradient(h)
    slope = normalise(np.sqrt(gx * gx + gy * gy))
    tone = 0.52 + 0.07 * spectral(n, 1.3, rng, low=4) + 0.16 * (h - 0.5) - 0.12 * slope
    fresh = np.clip(spectral(n, 1.1, rng, low=6) - 1.35, 0, None) * 0.3
    tone = np.clip(tone + fresh, 0, 1)
    hue = spectral(n, 1.6, rng, low=2) * 0.035
    rgb = np.stack([tone * (0.62 + hue), tone * (0.56 + hue * 0.5), tone * (0.49 - hue * 0.4)], -1)
    return np.clip(rgb, 0, 1), h


def crust(n, seed):
    rng = np.random.default_rng(seed)
    h = spectral(n, 1.45, rng, low=8) * 0.4 + spectral(n, 0.9, rng, low=3) * 0.12
    # Sublimation pits, terraces and cracks along the ridges of a second field.
    craters(h, rng, int(1400 * (n / 4096) ** 2), n / 600, n / 12, slope=2.0, depth=1.6)
    h = normalise(h)
    h = 0.65 * h + 0.35 * np.floor(h * 7) / 7
    ridge = 1 - np.abs(spectral(n, 1.15, rng, low=6))
    crack = np.clip((ridge - 0.94) / 0.06, 0, 1)
    h = normalise(h - crack * 0.12)
    tone = 0.2 + 0.05 * spectral(n, 1.3, rng, low=4) + 0.1 * (h - 0.5) - 0.12 * crack
    ice = np.clip(spectral(n, 1.35, rng, low=5) - 1.25, 0, None)
    ice = np.minimum(ice * 2.2, 1) * np.clip((0.5 - h) * 6, 0, 1)
    tone = np.clip(tone * (1 - ice) + ice * 0.8, 0, 1)
    rgb = np.stack([tone * 0.96, tone * 0.93, tone * (0.9 + 0.12 * ice)], -1)
    return np.clip(rgb, 0, 1), h


def save(name, rgb, height):
    OUT.mkdir(parents=True, exist_ok=True)
    srgb = np.where(rgb <= 0.0031308, rgb * 12.92, 1.055 * np.power(rgb, 1 / 2.4) - 0.055)
    data = np.concatenate([srgb, height[..., None]], -1)
    image = Image.fromarray((np.clip(data, 0, 1) * 255 + 0.5).astype(np.uint8), 'RGBA')
    options = {'quality': 80, 'method': 6, 'alpha_quality': 60}
    image.save(OUT / f'{name}-4k.webp', **options)
    image.resize((image.width // 2, image.height // 2), Image.LANCZOS).save(OUT / f'{name}.webp', **options)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--size', type=int, default=4096)
    args = parser.parse_args()
    save('regolite', *regolith(args.size, 20261127))
    save('nucleo', *crust(args.size, 20261128))
    for f in sorted(OUT.glob('*.webp')):
        print(f.relative_to(ROOT), f.stat().st_size, 'byte')


if __name__ == '__main__':
    main()
