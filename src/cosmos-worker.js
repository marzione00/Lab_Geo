/* Generate and transfer packed 3D particles without blocking navigation. */
'use strict';
importScripts('galaxy-model.js');
self.onmessage = ({ data }) => {
  if (data?.count !== 1200000) return;
  const result = self.GeoGalaxyModel.packedParticles(data.count);
  self.postMessage(result, [result.stars.buffer, result.dust.buffer]);
};
