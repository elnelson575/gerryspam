import pandas as pd
import fuzzy_pandas as fpd
import geopandas as gpd 
import re
from rich import print

"""
helper functions
"""
# strip letters from column 
def ignore_alpha(row):
    regex = re.compile('[\D_]+')
    return [regex.sub('', value) for value in row]

# ignore special election rows (mail-in, provisional, emergency, and overseas)
def ignore_special(df):
    patternDel = "mai|provision|emergency|overseas"
    filter = df[~df["precinct"].str.contains(patternDel, na=False)]
    return filter

"""
county-specific edit functions
"""
# edit precincts with matching issues
countyToCountyCleaner = {
    "033": edit_033,
}

# concat precinct words for sneaky precincts
# (e.g.: "salem north", "salem east" within the same county)
def rm_space(row, prec):
    with_space = prec + ' '
    regex = re.compile(with_space)
    return [regex.sub(prec, value) for value in row]

def edit_033(row):
    return rm_space(row, 'salem')

def edit_027(row):
    precs = ['salem', 'chester']
    to_replace = {(prec + ' '):prec for prec in precs}
    out = row.replace(to_replace, regex=True)
    out_list = out.tolist()
    print(type(out_list))
    return out_list


d = {'prec': ["chester east thing", "p", "salem west"], 'col2': ["dog", 4, "cat"]}
df = pd.DataFrame(data=d)

m_out = edit_033(df['prec'])

x_out = edit_027(df['prec'])

        



"""
direct data cleaning
"""
# OpenElections
elec_16 = pd.read_csv('/Users/hopecj/projects/gerryspam/NJ/dat/NJ_G16_OpenElex.csv')

# if using open elections data
# split apart county and precinct (only 1 comma split)
elec_16 = pd.concat([elec_16, elec_16['loc_prec'].str.split(',', 1, expand=True)], axis=1)
elec_16 = elec_16.rename(columns={0: "countynam", 1: "precinct"})
elec_16['precinct'] = elec_16['precinct'].str.lower()
crosswalk = pd.read_csv('/Users/hopecj/projects/gerryspam/NJ/dat/nj-county-crosswalk.csv')
elec_16 = elec_16.merge(crosswalk, left_on='countynam', right_on='county_nam')
elec_16['county_fips_st'] = elec_16['statefips_countyfips'].apply(str)
elec_16['county_fips'] = elec_16['county_fips_st'].str.slice(start=2)

# remove special election precinct rows 
print(elec_16.shape)
elec_16 = ignore_special(elec_16)
print(elec_16.shape) # got rid of 1238 rows

clean_elec = elec_16.sort_values(by=['county_fips'])
counties = pd.Series(clean_elec['county_fips']).unique()
clean_elec["prec_matching"] = clean_elec["precinct"].copy()
clean_elec.set_index(['county_fips', 'precinct'], inplace=True)
# print("duplicated indices", clean_elec[clean_elec.index.duplicated()])

# # FOR TESTING
# county_dat = clean_elec.loc['033']
# changed = countyToCountyCleaner.get(county, lambda x: x)(county_dat['prec_matching'])
# print("changed", changed)
# county_dat['prec_matching'] = changed
# print(county_dat['prec_matching'])

for county in counties:
    county_dat = clean_elec.loc[county]
    changed = countyToCountyCleaner.get(county, lambda x: x)(county_dat['prec_matching'])
    county_dat['prec_matching'] = changed
    clean_elec.update(county_dat)

# continue with the general clean 
clean_elec['elec_loc_prec'] = clean_elec['county_fips'].astype(str) + "," + clean_elec['prec_matching'].astype(str)
prec_split = clean_elec['prec_matching'].str.split(expand=True)
clean_elec['prec_word1'] = prec_split[0]
clean_elec = clean_elec.drop([2, 3, 'Unnamed: 6'], axis=1)

# make column of first word from precinct name and numbers 
elec_nums = ignore_alpha(clean_elec['elec_loc_prec'])
clean_elec["elec_loc_prec_nums"] = elec_nums
clean_elec["elec_loc_prec_code"] = clean_elec['elec_loc_prec_nums'].astype(str) + '_' + clean_elec['prec_word1']