/* Orbital view and close approaches share the native 3D renderers. */
(function (root) {
  'use strict';
  const M = root.GeoGalaxyModel,
    A = root.GeoAstro,
    TAU = Math.PI * 2;
  function create(chart, system, onSelect) {
    let canvas = chart.querySelector('canvas'),
      renderer,
      disposed = false,
      raf = 0,
      last = 0,
      time = 0,
      years = 0,
      width = 1,
      height = 1,
      azimuth = 0,
      elevation = 0.85,
      distance = 40,
      selected = 'star',
      focusId = null,
      transition = null,
      drag = null;
    const listeners = [],
      bound = [],
      listen = (el, event, fn, options) => {
        el.addEventListener(event, fn, options);
        bound.push([el, event, fn, options]);
        listeners.push(() => el.removeEventListener(event, fn, options));
      };
    const paused = () => root.GeoSpace?.debug().paused ?? window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const star = {
      id: 'star',
      name: system.name,
      position: [0, 0, 0],
      radius: 1.35,
      land: system.star.color,
      deep: '#ab4f27',
      high: system.star.color,
      atmosphere: system.star.color,
      tilt: 0,
      phase: 0,
      speed: 0.04,
      kind: -1,
      emissive: true,
    };
    const worlds = [star, ...system.planets.map(p => ({ ...p, radius: p.visualRadius }))];
    const field = M.particles(6000)
      .stars.filter(p => Math.hypot(...p.p) > 8)
      .slice(0, 650)
      .map(p => ({ ...p, p: p.p.map((v, i) => v * (i === 1 ? 25 : 4)), a: p.a * 0.45, size: 0.025 }));
    const state = { width, height, time, angle: 0, worlds, camera: null, light: [0, 0, 0], selected };
    const invalidate = () => {
      if (!disposed && !raf) raf = requestAnimationFrame(tick);
    };
    try {
      renderer = root.GeoGalaxyScene.webgl(canvas, { stars: field, dust: [] }, worlds, invalidate);
    } catch (_) {
      const next = canvas.cloneNode(false);
      canvas.replaceWith(next);
      canvas = next;
      try {
        renderer = root.GeoGalaxyScene.software(canvas, { stars: field, dust: [] }, invalidate);
      } catch (_) {
        chart.dataset.renderer = 'essential';
      }
    }
    if (renderer) {
      chart.dataset.renderer = renderer.kind;
      chart.classList.add('scene-ready');
    }
    // A WebGL context that cannot keep up (software rasteriser, weak GPU) gives way to the canvas renderer.
    const slowFrames = root.GeoCore?.frameWatch?.() || (() => false);
    function downgrade() {
      const old = canvas,
        next = canvas.cloneNode(false);
      try {
        renderer?.dispose();
      } catch (_) {
        /* context already gone */
      }
      old.replaceWith(next);
      canvas = next;
      for (const [el, event, fn, options] of bound)
        if (el === old) {
          next.addEventListener(event, fn, options);
          listeners.push(() => next.removeEventListener(event, fn, options));
        }
      try {
        renderer = root.GeoGalaxyScene.software(canvas, { stars: field, dust: [] }, invalidate);
        chart.dataset.renderer = renderer.kind;
      } catch (_) {
        renderer = null;
        chart.dataset.renderer = 'essential';
      }
      resize();
    }
    const rings = chart.querySelector('.system-rings');
    const overlay = chart.querySelector('.system-orbits'),
      orbitPaths = [...overlay.querySelectorAll('path')],
      labels = [...chart.querySelectorAll('[data-body-label]')];
    function resize() {
      const r = chart.getBoundingClientRect();
      width = Math.max(1, r.width);
      height = Math.max(1, r.height);
      const dpr = Math.min(window.devicePixelRatio || 1, 1.7, 1900 / width);
      canvas.width = Math.round(width * dpr);
      canvas.height = Math.round(height * dpr);
      invalidate();
    }
    // Camera target and distance, eased while a focus transition runs.
    function cameraPose(now) {
      const target = focusId ? worlds.find(p => p.id === focusId).position : [0, 0, 0];
      let eyeTarget = target,
        camDistance = focusId
          ? worlds.find(p => p.id === focusId).radius * 5
          : distance * Math.max(1, (height / width) * 0.9);
      if (transition) {
        const t = M.clamp((now - transition.start) / 850, 0, 1),
          e = t * t * (3 - 2 * t);
        eyeTarget = target.map((v, i) => transition.from[i] + (v - transition.from[i]) * e);
        camDistance = transition.distance + (camDistance - transition.distance) * e;
        if (t === 1) transition = null;
      }
      return [eyeTarget, camDistance];
    }
    function projectWorlds() {
      for (const p of worlds) {
        p.screen = M.project(p.position, state.camera.vp, width, height);
        p.screen.radius = (p.radius * height * state.camera.f) / (2 * p.screen.depth);
      }
    }
    function drawRings() {
      if (!rings) return;
      rings.setAttribute('viewBox', `0 0 ${width} ${height}`);
      for (const g of rings.querySelectorAll('[data-ring]')) {
        const p = worlds.find(p => p.id === g.dataset.ring),
          q = p.screen,
          visible = q.visible && (!focusId || focusId === p.id);
        g.style.display = visible ? '' : 'none';
        g.classList.toggle('selected', selected === p.id);
        g.querySelectorAll('circle').forEach((c, i) => {
          c.setAttribute('cx', q.x);
          c.setAttribute('cy', q.y);
          c.setAttribute('r', Math.max(12, q.radius) + 6 + i * 5);
        });
        g.querySelector('path').setAttribute('d', `M${q.x},${q.y + q.radius + 5}L${q.x},${q.y + q.radius + 12}`);
      }
    }
    function drawOrbits() {
      overlay.setAttribute('viewBox', `0 0 ${width} ${height}`);
      overlay.style.opacity = focusId ? '0' : '1';
      orbitPaths.forEach((path, i) => {
        let d = '';
        for (let j = 0; j <= 180; j++) {
          const a = (j / 180) * TAU,
            r = system.planets[i].orbitRadius,
            q = M.project([Math.cos(a) * r, 0, Math.sin(a) * r], state.camera.vp, width, height);
          d += (j ? 'L' : 'M') + q.x.toFixed(1) + ',' + q.y.toFixed(1);
        }
        path.setAttribute('d', d);
        path.classList.toggle('target-orbit', system.planets[i].isTarget);
      });
    }
    function placeLabels() {
      for (const b of labels) {
        const p = worlds.find(p => p.id === b.dataset.bodyLabel),
          q = p.screen;
        b.style.left = q.x + 'px';
        b.style.top = q.y + q.radius + 12 + 'px';
        b.hidden = !q.visible || Boolean(focusId && focusId !== p.id) || q.x < 45 || q.x > width - 45;
        b.classList.toggle('selected', selected === p.id);
      }
    }
    // False when this animation frame should not draw (scene gone, hidden, or throttled to ~22 fps).
    function frameDue(now) {
      if (disposed || !chart.isConnected || !renderer || document.hidden) {
        last = 0;
        return false;
      }
      if (last && now - last < 45 && !transition) {
        raf = requestAnimationFrame(tick);
        return false;
      }
      return true;
    }
    function advance(now) {
      if (renderer?.kind === 'webgl' && last && slowFrames(now - last)) downgrade();
      const dt = last ? Math.min(0.1, (now - last) / 1000) : 0;
      last = now;
      if (!paused()) {
        time += dt;
        years += dt * system.yearsPerSecond;
      }
      for (const p of worlds) if (!p.emissive) p.position = A.position(p, years);
    }
    function tick(now) {
      raf = 0;
      if (!frameDue(now)) return;
      advance(now);
      const [eyeTarget, camDistance] = cameraPose(now);
      state.target = eyeTarget;
      state.distance = camDistance;
      state.width = width;
      state.height = height;
      state.time = time;
      state.selected = selected;
      state.camera = M.camera(azimuth, elevation, camDistance, eyeTarget, width / height);
      projectWorlds();
      drawRings();
      drawOrbits();
      placeLabels();
      renderer.draw(state);
      chart.dataset.textures = String(renderer.textureCount());
      if (!paused() || transition) raf = requestAnimationFrame(tick);
      else last = 0;
    }
    function focus(id) {
      const p = worlds.find(p => p.id === id);
      if (!p) return;
      selected = id;
      transition = paused()
        ? null
        : { start: performance.now(), from: state.target || [0, 0, 0], distance: state.distance || 40 };
      focusId = id === 'star' ? null : id;
      if (focusId) {
        const position = p.position || A.position(p, years);
        azimuth = Math.atan2(-position[0], -position[2]) + 0.45;
        elevation = 0.35;
      } else {
        azimuth = 0;
        elevation = 0.85;
      }
      chart.dataset.close = String(Boolean(focusId));
      invalidate();
    }
    function reset() {
      focusId = null;
      transition = null;
      azimuth = 0;
      elevation = 0.85;
      distance = 40;
      chart.dataset.close = 'false';
      invalidate();
    }
    function pick(x, y) {
      return worlds
        .filter(p => p.screen?.visible && Math.hypot(x - p.screen.x, y - p.screen.y) < Math.max(17, p.screen.radius))
        .sort((a, b) => a.screen.depth - b.screen.depth)[0];
    }
    listen(canvas, 'pointerdown', e => {
      drag = { x: e.clientX, y: e.clientY, startX: e.clientX, startY: e.clientY, moved: false };
      canvas.setPointerCapture(e.pointerId);
    });
    listen(canvas, 'pointermove', e => {
      if (!drag) {
        const r = canvas.getBoundingClientRect();
        canvas.style.cursor = pick(e.clientX - r.left, e.clientY - r.top) ? 'pointer' : 'grab';
        return;
      }
      azimuth -= (e.clientX - drag.x) * 0.005;
      elevation = M.clamp(elevation + (e.clientY - drag.y) * 0.004, 0.25, 1.4);
      drag.x = e.clientX;
      drag.y = e.clientY;
      drag.moved ||= Math.hypot(e.clientX - drag.startX, e.clientY - drag.startY) > 5;
      invalidate();
    });
    listen(canvas, 'pointerup', e => {
      if (drag && !drag.moved) {
        const r = canvas.getBoundingClientRect(),
          p = pick(e.clientX - r.left, e.clientY - r.top);
        if (p) onSelect(p.id);
      }
      drag = null;
    });
    listen(canvas, 'pointercancel', () => {
      drag = null;
    });
    listen(
      canvas,
      'wheel',
      e => {
        if (focusId) return;
        e.preventDefault();
        distance = M.clamp(distance * Math.exp(e.deltaY * 0.001), 26, 65);
        invalidate();
      },
      { passive: false },
    );
    listen(canvas, 'keydown', e => {
      if (!['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', '+', '-', 'Home', 'Escape'].includes(e.key)) return;
      e.preventDefault();
      if (e.key === 'ArrowLeft') azimuth += 0.12;
      if (e.key === 'ArrowRight') azimuth -= 0.12;
      if (e.key === 'ArrowUp') elevation = M.clamp(elevation + 0.1, 0.25, 1.4);
      if (e.key === 'ArrowDown') elevation = M.clamp(elevation - 0.1, 0.25, 1.4);
      if (e.key === '+') distance = M.clamp(distance - 3, 26, 65);
      if (e.key === '-') distance = M.clamp(distance + 3, 26, 65);
      if (e.key === 'Home' || e.key === 'Escape') reset();
      invalidate();
    });
    for (const b of chart.querySelectorAll('[data-system-camera]'))
      listen(b, 'click', () => {
        if (b.dataset.systemCamera === 'reset') reset();
        else {
          if (focusId) reset();
          distance = M.clamp(distance + (b.dataset.systemCamera === 'in' ? -4 : 4), 26, 65);
          invalidate();
        }
      });
    listen(document, 'geospace:pause', () => {
      last = 0;
      invalidate();
    });
    listen(document, 'visibilitychange', () => {
      last = 0;
      invalidate();
    });
    listen(window, 'resize', resize);
    listen(canvas, 'webglcontextlost', e => {
      e.preventDefault();
      renderer?.dispose();
      renderer = null;
      chart.dataset.renderer = 'essential';
      chart.classList.remove('scene-ready');
    });
    resize();
    return {
      focus,
      reset,
      dispose() {
        disposed = true;
        cancelAnimationFrame(raf);
        listeners.forEach(f => f());
        renderer?.dispose();
      },
      debug: () => ({
        renderer: renderer?.kind || 'essential',
        selected,
        focusId,
        years,
        worlds: worlds.map(p => ({ id: p.id, screen: p.screen })),
      }),
    };
  }
  root.GeoSystemScene = Object.freeze({ create });
})(globalThis);
