/* Geometry of the notable objects off the main thread: lensing tables, dense meshes and stream paths. */
'use strict';
// The build prepends both libraries to this file; importScripts serves the unbundled sources.
if (!self.GeoObjectGeometry) importScripts('objects-model.js', 'objects-geometry.js');
const G = self.GeoObjectGeometry,
  O = self.GeoObjects;
const tasks = {
  // Lensing tables for every camera level, sent one at a time from the level nearest to the first view.
  lens({ id, near = 42, far = 260, count = 12, first = 70, rays = 3072 }) {
    const radii = G.levelRadii(count, near, far),
      order = radii.map((rc, i) => [Math.abs(Math.log(rc / first)), i]).sort((a, b) => a[0] - b[0]);
    for (const [, i] of order) {
      const level = G.lensLevel(radii[i], { rays });
      self.postMessage({ id, partial: true, result: { index: i, ...level } }, [level.lens.buffer, level.sky.buffer]);
    }
    return { radii };
  },
  photons({ count, samples }) {
    return G.photonPaths({ count, samples });
  },
  smallBody(options) {
    return G.smallBody(options);
  },
  donor({ mu, potential, level }) {
    return G.rocheDonor({ mu, potential, level });
  },
  stream({ mu, l1, radius }) {
    return O.rocheStream(mu, l1, radius);
  },
  sphere({ level }) {
    const s = G.icosphere(level);
    return { positions: s.positions, normals: s.positions.slice(), indices: s.indices };
  },
  blackbody({ n }) {
    return { table: O.blackbodyTable(n) };
  },
};
self.onmessage = ({ data }) => {
  const { id, task } = data;
  try {
    if (!Object.hasOwn(tasks, task)) throw Error('Unknown task');
    const result = tasks[task](data),
      buffers = Object.values(result)
        .filter(v => ArrayBuffer.isView(v))
        .map(v => v.buffer);
    self.postMessage({ id, result }, buffers);
  } catch (err) {
    self.postMessage({ id, error: String(err?.message || err) });
  }
};
