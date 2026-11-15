/* Persistent 3D environment shared with the orbital camera. No bitmap backdrop. */
(function (root) {
  'use strict';
  const host = document.getElementById('deep-space');
  if (!host || !root.GeoUniverse) return;
  const canvas = document.createElement('canvas');
  canvas.setAttribute('aria-hidden', 'true');
  host.append(canvas);
  let renderer,
    gl,
    frame = 0,
    disposed = false,
    dirty = true;
  let paused = root.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let pose = { azimuth: 0, elevation: 0.12, distance: 35, target: [0, 0, 0] };
  function draw() {
    frame = 0;
    if (disposed || document.hidden || !renderer || !dirty) return;
    dirty = false;
    const camera = root.GeoGalaxyModel.camera(
      pose.azimuth,
      pose.elevation,
      pose.distance,
      pose.target,
      canvas.width / canvas.height,
    );
    gl.clearColor(0.004, 0.009, 0.022, 1);
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
    renderer.draw(camera, canvas.width, canvas.height, 0.95);
  }
  function invalidate() {
    dirty = true;
    if (!frame && !disposed) frame = requestAnimationFrame(draw);
  }
  function resize() {
    const scale = Math.min(devicePixelRatio || 1, 1.5, 1800 / innerWidth);
    canvas.width = Math.max(1, Math.round(innerWidth * scale));
    canvas.height = Math.max(1, Math.round(innerHeight * scale));
    invalidate();
  }
  function initialize() {
    try {
      gl = canvas.getContext('webgl', { alpha: false, antialias: false, powerPreference: 'high-performance' });
      if (!gl) return;
      renderer = root.GeoUniverse.create(gl);
      host.dataset.ready = 'true';
    } catch {
      host.dataset.ready = 'false';
    }
    resize();
  }
  let poseKey = '';
  function setView(next) {
    const key = [next.azimuth, next.elevation, next.distance, ...next.target].map(x => Math.round(x * 1000)).join(',');
    if (key === poseKey) return;
    poseKey = key;
    pose = { ...pose, ...next };
    invalidate();
  }
  document.addEventListener('geospace:pause', e => {
    paused = !!e.detail.paused;
    invalidate();
  });
  document.addEventListener('visibilitychange', invalidate);
  root.addEventListener('resize', resize);
  canvas.addEventListener('webglcontextlost', e => {
    e.preventDefault();
    renderer?.dispose();
    renderer = null;
    host.dataset.ready = 'false';
  });
  canvas.addEventListener('webglcontextrestored', initialize);
  root.addEventListener('pagehide', e => {
    cancelAnimationFrame(frame);
    frame = 0;
    if (!e.persisted) {
      disposed = true;
      renderer?.dispose();
    }
  });
  root.addEventListener('pageshow', invalidate);
  root.GeoCosmos = Object.freeze({
    setView,
    debug: () => ({
      ready: !!renderer,
      renderer: renderer ? 'webgl-volume' : 'essential',
      paused,
      ...renderer?.debug(),
      pose,
    }),
  });
  initialize();
})(window);
