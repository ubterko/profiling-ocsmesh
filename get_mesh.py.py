from ocsmesh import Raster, Geom, Hfun, JigsawDriver, utils 
import geopandas as gpd

raster_files = [
    "rasterfiles/gebco_2024_n40.66_s40.6_w14.47_e14.62.tif",
    "rasterfiles/gebco_2024_n40.65_s40.61_w14.49_e14.61.tif",
    "rasterfiles/gebco_2024_n40.67_s40.59_w14.46_e14.64.tif",
    "rasterfiles/gebco_2024_n40.7_s40.58_w14.45_e14.65.tif"
]

geom_rasters = [Raster(i) for i in raster_files] 
geom = Geom(geom_rasters,zmax=15)

hfun_rasters = [Raster(i) for i in raster_files] 
hfun = Hfun(hfun_rasters, hmin=100, hmax=4100) 

hfun.add_contour(level=0, expansion_rate=0.005, target_size=100)
hfun.add_contour(level=-50, expansion_rate=0.005, target_size=200) 
print("Added contours")

hfun.add_constant_value(400,lower_bound=0)
hfun.add_constant_value(800, lower_bound=-50)  
print("Added constant values")


multipolygon = geom.get_multipolygon()
print("Processed multipolygon")

hfun_msh_t = hfun.msh_t()
print("Processed hfun.msh_t")

driver = JigsawDriver(geom, hfun)

mesh = driver.run()
print("Processed mesh") 


# interpolate on mesh from raster files
interpolation_rasters = []
for files in raster_files:
    interpolation_rasters.append(Raster(files))
mesh.interpolate(interpolation_rasters) 
print("Mesh interpolated")

mesh.write("data/data/mesh.2dm", format="2dm", overwrite=True)