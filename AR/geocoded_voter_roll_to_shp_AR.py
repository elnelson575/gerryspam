import time
import pandas as pd
import geopandas as gpd
import math
import shapely as shp
import warnings


df = df.groupby('GEOID10')['precinct'].apply(list).apply(Counter)
df = pd.DataFrame(df)
df.to_csv('/Volumes/GoogleDrive/Shared drives/princeton_gerrymandering_project/OpenPrecincts/States for site/Georgia/VR Shapefile/blocks/GAblocksVRprecinct.csv')

df = df.dropna()
for index, row in df.iterrows():
    df['precinct'][index]= df['precinct'][index].most_common()[0][0]
#for index, row in df_shp_test.iterrows():
#    df_shp_test['most_precinct'][index]= df_shp_test['precinct'][index].most_common()[0][0]
#df_shp_new = df_shp.loc['precinct'].apply(lambda x: x.most_common(1)[0][0])
# get census block shapefile and col to merge on
shp_path = "/Volumes/GoogleDrive/Shared drives/princeton_gerrymandering_project/mapping/2010 Census Block shapefiles/GA/tl_2017_13_tabblock10.shp"
shp_merge_col = 'GEOID10'

# load shapefile and delete precinct column if it exists
ht.delete_cpg(shp_path)
df_shp = gpd.read_file(shp_path)
df_shp = df_shp.set_index('GEOID10')
if 'precinct' in df_shp.columns:
    df_shp = df_shp.drop(columns=['precinct'])
    
# left match precinct name on GEOID
df.index = df.index.astype(str)
df_shp = df_shp.join(df)


# Assign NaN values to None
df_shp = df_shp.where((pd.notnull(df_shp)), None)

# Save original merge precincts
df_shp['orig_prec'] = df_shp['precinct']

# Replace None precinct with a unique character
for i, _ in df_shp.iterrows():
    # replace None with a unique character
    if df_shp.at[i, 'precinct'] == None:
        df_shp.at[i, 'precinct'] = 'None_' + str(i)
        
# Get unique values
prec_name = list(set(df_shp['precinct']))

# Initalize precinct dataframe
df_prec = pd.DataFrame(columns=['precinct', 'geometry'])


prec_name = list(set(df_shp['precinct']))
# Iterate through all of the precinct IDs and set geometry for df_prec
for i, elem in enumerate(prec_name):
    df_poly = df_shp[df_shp['precinct'] == elem]
    polys = list(df_poly['geometry'])
    df_prec.at[i, 'geometry'] = shp.ops.cascaded_union(polys)
    df_prec.at[i, 'precinct'] = elem

start_combine =  time.time()

# reset index
df_prec = df_prec.reset_index(drop=True)

# get rook contiguity and calculate shared perims
df_prec = ht.get_shared_perims(df_prec)

# get list of precinct indexes to merge
precincts_to_merge = []
for i, _ in df_prec.iterrows():
    if str(df_prec.at[i, 'precinct']).split('_')[0] == 'None':
        precincts_to_merge.append(i)
        
# merge geometries
df_prec = ht.merge_geometries(df_prec, precincts_to_merge)

# Save census block shapefile
block_path = "/Volumes/GoogleDrive/Shared drives/princeton_gerrymandering_project/OpenPrecincts/States for site/Georgia/VR Shapefile/blocks/GA_VR_blocks.shp"
prec_path = "/Volumes/GoogleDrive/Shared drives/princeton_gerrymandering_project/OpenPrecincts/States for site/Georgia/VR Shapefile/GA_VR_Precincts.shp" 
# Save precinct assignments down to the block
df = ai.aggregate(df_shp_c, df_prec, target_columns =['precinct'], spatial_index = False)[0]


# Save shapefiles
df.to_file(block_path)
#df_prec.to_file(prec_path)
#ht.save_shapefile(df, block_path, ['neighbors'])
#ht.save_shapefile(df_prec, prec_path, ['neighbors'])
