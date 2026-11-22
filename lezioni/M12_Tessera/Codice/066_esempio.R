s_terra <- terra::terrain(r,
 v="slope",neighbors=4,
 unit="degrees")
terra::global(s_terra,"range",na.rm=TRUE)
