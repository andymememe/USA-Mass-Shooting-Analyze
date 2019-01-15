import math
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import rgb2hex, Normalize
from matplotlib.cm import ScalarMappable
from matplotlib.patches import Polygon
from matplotlib.colorbar import ColorbarBase
from mpl_toolkits.basemap import Basemap
from geopy.geocoders import Nominatim

mpl.style.use('bmh')
mpl.rc('font', family='ITCOfficinaSans LT Book')
mpl.rcParams['axes.titlesize'] = 33
mpl.rcParams['figure.titlesize'] = 33

usecols = ["Location", "Date", "Fatalities", "Injured", "Total victims",
           "Mental Health Issues", "Race", "Gender"]
races = ["Asian", "Black", "Latino", "Native", "White", "Unknown"]
data = pd.read_csv("data/data.csv", header=0, usecols=usecols,
                   parse_dates=["Date"])

# Filting Location
data = data[data["Location"].notnull()]
# Fill NA
data = data.fillna("Unknown")
# Parsing Gender
data["Gender"] = data["Gender"].replace(to_replace=".+/.+", value="Unknown",
                                        regex=True)
data["Gender"] = data["Gender"].replace(to_replace="M", value="Male")
data["Gender"] = data["Gender"].replace(to_replace="F", value="Female")
# Parsing Mental Health Issues
data["Mental Health Issues"] = data["Mental Health Issues"].replace(
        to_replace="Unclear", value="Unknown")
data["Mental Health Issues"] = data["Mental Health Issues"].str.capitalize()
# Parsing Race
data["Race"] = data["Race"].replace(to_replace=".+/.+", value="Unknown",
                                    regex=True)
data["Race"] = data["Race"].replace(to_replace=".+more.+", value="Mixed",
                                    regex=True)
data["Race"] = data["Race"].replace(to_replace=".+[o|O]ther.+", value="Other",
                                    regex=True)
for r in races:
    data["Race"] = data["Race"].replace(to_replace=r + ".+",
                                        value=r,
                                        regex=True)
data["Race"] = data["Race"].str.capitalize()
# Add State
data["State"] = data["Location"].str.split(', ').str.get(1)
data["State"] = data["State"].str.strip()
data["State"] = data["State"].fillna("Other")
data["State"] = data["State"].replace(to_replace="CA", value="State")
data["State"] = data["State"].replace(to_replace="LA", value="Louisiana")
data["State"] = data["State"].replace(to_replace="NV", value="Nevada")
data["State"] = data["State"].replace(to_replace="PA", value="Pennsylvania")
data["State"] = data["State"].replace(to_replace="WA", value="Washington")

# Counting
# *MHI
mhi_count = data.groupby("Mental Health Issues").size()
mhi_count = mhi_count[~(mhi_count.index == 'Unknown')]
# *Race
race_count = data.groupby("Race").size().sort_values()
# *Gender
gender_count = data.groupby("Gender").size()
# *Month
month_count = data.groupby(data['Date'].dt.strftime('%m')).size()
# *Year
year_count = data.groupby(data['Date'].dt.strftime('%Y')).size()
# *State
state_count = data.groupby("State").size().sort_values()
# *RG
rg_count = data.groupby(["Race", "Gender"]).size().unstack()

# Victim Counting
# *MHI
mhi_v_count = data.groupby("Mental Health Issues")['Total victims'].sum()
mhi_v_count = mhi_v_count[~(mhi_v_count.index == 'Unknown')]
# *Race
race_v_count = data.groupby("Race")['Total victims'].sum().sort_values()
# *Gender
gender_v_count = data.groupby("Gender")['Total victims'].sum()
# *Month
month_v_count = data.groupby(data['Date'].dt.strftime('%m'))['Total victims']\
    .sum()
# *Year
year_v_count = data.groupby(data['Date'].dt.strftime('%Y'))['Total victims']\
    .sum()
# *State
state_v_count = data.groupby(data['State'])['Total victims'].sum()\
    .sort_values()
# *RG
rg_v_count = data.groupby(["Race", "Gender"])['Total victims'].sum().unstack()

# Fatal Counting
# *MHI
mhi_f_count = data.groupby("Mental Health Issues")['Fatalities'].sum()
mhi_f_count = mhi_f_count[~(mhi_f_count.index == 'Unknown')]
# *Race
race_f_count = data.groupby("Race")['Fatalities'].sum().sort_values()
# *Gender
gender_f_count = data.groupby("Gender")['Fatalities'].sum()
# *Month
month_f_count = data.groupby(data['Date'].dt.strftime('%m'))['Fatalities']\
    .sum()
# *Year
year_f_count = data.groupby(data['Date'].dt.strftime('%Y'))['Fatalities'].sum()
# *State
state_f_count = data.groupby(data['State'])['Fatalities'].sum().sort_values()
# *RG
rg_f_count = data.groupby(["Race", "Gender"])['Fatalities'].sum().unstack()

# Injured Counting
# *MHI
mhi_i_count = data.groupby("Mental Health Issues")['Injured'].sum()
mhi_i_count = mhi_i_count[~(mhi_i_count.index == 'Unknown')]
# *Race
race_i_count = data.groupby("Race")['Injured'].sum().sort_values()
# *Gender
gender_i_count = data.groupby("Gender")['Injured'].sum()
# *Month
month_i_count = data.groupby(data['Date'].dt.strftime('%m'))['Injured'].sum()
# *Year
year_i_count = data.groupby(data['Date'].dt.strftime('%Y'))['Injured'].sum()
# *State
state_i_count = data.groupby(data['State'])['Injured'].sum().sort_values()
# *RG
rg_i_count = data.groupby(["Race", "Gender"])['Injured'].sum().unstack()

# Plot
# *Pie
total = mhi_count.sum()
m_c = mhi_count.plot('pie', title='Cases (Total: ' + str(total) + ')',
                     label="",
                     autopct='%1.1f%%', figsize=(6, 6), fontsize=20)
fig = m_c.get_figure()
fig.savefig("result/m_c.png")
plt.close()

total = gender_count.sum()
g_c = gender_count.plot('pie', title='Cases (Total: ' + str(total) + ')',
                        label="",
                        autopct='%1.1f%%', figsize=(8, 8), fontsize=15)
fig = g_c.get_figure()
fig.savefig("result/g_c.png")
plt.close()

total = mhi_v_count.sum()
m_v = mhi_v_count.plot('pie', title='Victims (Total: ' + str(total) + ')',
                       label="",
                       autopct='%1.1f%%', figsize=(6, 6), fontsize=20)
fig = m_v.get_figure()
fig.savefig("result/m_v.png")
plt.close()

total = gender_v_count.sum()
g_v = gender_v_count.plot('pie', title='Victims (Total: ' + str(total) + ')',
                          label="",
                          autopct='%1.1f%%', figsize=(8, 8), fontsize=15)
fig = g_v.get_figure()
fig.savefig("result/g_v.png")
plt.close()

total = mhi_f_count.sum()
m_f = mhi_f_count.plot('pie', title='Fetalities (Total: ' + str(total) + ')',
                       label="",
                       autopct='%1.1f%%', figsize=(10, 10), fontsize=20)
fig = m_f.get_figure()
fig.savefig("result/m_f.png")
plt.close()

total = gender_f_count.sum()
g_f = gender_f_count.plot('pie',
                          title='Fetalities (Total: ' + str(total) + ')',
                          label="",
                          autopct='%1.1f%%', figsize=(8, 8), fontsize=15)
fig = g_f.get_figure()
fig.savefig("result/g_f.png")
plt.close()

total = mhi_i_count.sum()
m_i = mhi_i_count.plot('pie', title='Injured (Total: ' + str(total) + ')',
                       label="",
                       autopct='%1.1f%%', figsize=(10, 10), fontsize=20)
fig = m_i.get_figure()
fig.savefig("result/m_i.png")
plt.close()

total = gender_i_count.sum()
g_i = gender_i_count.plot('pie', title='Injured (Total: ' + str(total) + ')',
                          label="",
                          autopct='%1.1f%%', figsize=(8, 8), fontsize=15)
fig = g_i.get_figure()
fig.savefig("result/g_i.png")
plt.close()

# *bar
r_c = race_count.plot('bar', title='Cases', label="",
                      figsize=(20, 15), fontsize=25)
r_c.set_xlabel("Shooter's Race", fontsize=25)
r_c.set_ylabel("Cases", fontsize=25)
fig = r_c.get_figure()
fig.savefig("result/r_c.png")
plt.close()

mo_c = month_count.plot('bar', title='Cases by Month', label="",
                        figsize=(10, 10), fontsize=20)
mo_c.set_xlabel("Month", fontsize=25)
mo_c.set_ylabel("Cases", fontsize=25)
fig = mo_c.get_figure()
fig.savefig("result/mo_c.png")
plt.close()

y_c = year_count.plot('bar', title='Cases by Year', label="",
                      figsize=(20, 10), fontsize=20)
y_c.set_xlabel("Year", fontsize=25)
y_c.set_ylabel("Cases", fontsize=25)
fig = y_c.get_figure()
fig.savefig("result/y_c.png")
plt.close()

s_c = state_count.plot('bar', title='Cases by State', label="",
                       figsize=(36, 18), fontsize=20)
s_c.set_xlabel("State", fontsize=25)
s_c.set_ylabel("Cases", fontsize=25)
fig = s_c.get_figure()
fig.savefig("result/s_c.png")
plt.close()

rg_c = rg_count.plot(kind='bar', title='Cases', label="",
                     figsize=(20, 15), fontsize=25)
rg_c.set_xlabel("Shooter's Race", fontsize=25)
rg_c.set_ylabel("Cases", fontsize=25)
leg = rg_c.legend(fontsize=25)
leg.set_title("Shooter's Gender", prop={'size': '25'})
fig = rg_c.get_figure()
fig.savefig("result/rg_c.png")
plt.close()

r_v = race_v_count.plot('bar', title='Victims', label="",
                        figsize=(20, 15), fontsize=25)
r_v.set_xlabel("Shooter's Race", fontsize=25)
r_v.set_ylabel("Victims", fontsize=25)
fig = r_v.get_figure()
fig.savefig("result/r_v.png")
plt.close()

mo_v = month_v_count.plot('bar', title='Victims by Month', label="",
                          figsize=(10, 10), fontsize=20)
mo_v.set_xlabel("Month", fontsize=25)
mo_v.set_ylabel("Victims", fontsize=25)
fig = mo_v.get_figure()
fig.savefig("result/mo_v.png")
plt.close()

y_v = year_v_count.plot('bar', title='Victims by Year', label="",
                        figsize=(20, 10), fontsize=20)
y_v.set_xlabel("Year", fontsize=25)
y_v.set_ylabel("Victims", fontsize=25)
fig = y_v.get_figure()
fig.savefig("result/y_v.png")
plt.close()

s_v = state_v_count.plot('bar', title='Victims by State', label="",
                         figsize=(36, 18), fontsize=20)
s_v.set_xlabel("State", fontsize=25)
s_v.set_ylabel("Victims", fontsize=25)
fig = s_v.get_figure()
fig.savefig("result/s_v.png")
plt.close()

rg_v = rg_v_count.plot(kind='bar', title='Victims', label="",
                       figsize=(20, 15), fontsize=25)
rg_v.set_xlabel("Shooter's Race", fontsize=25)
rg_v.set_ylabel("Victims", fontsize=25)
leg = rg_v.legend(fontsize=25)
leg.set_title("Shooter's Gender", prop={'size': '25'})
fig = rg_v.get_figure()
fig.savefig("result/rg_v.png")
plt.close()

r_i = race_i_count.plot('bar', title='Injured', label="",
                        figsize=(20, 15), fontsize=25)
r_i.set_xlabel("Shooter's Race", fontsize=25)
r_i.set_ylabel("Injured", fontsize=25)
fig = r_i.get_figure()
fig.savefig("result/r_i.png")
plt.close()

mo_i = month_i_count.plot('bar', title='Injured by Month', label="",
                          figsize=(10, 10), fontsize=20)
mo_i.set_xlabel("Month", fontsize=25)
mo_i.set_ylabel("Injured", fontsize=25)
fig = mo_i.get_figure()
fig.savefig("result/mo_i.png")
plt.close()

y_i = year_i_count.plot('bar', title='Injured by Year', label="",
                        figsize=(20, 10), fontsize=20)
y_i.set_xlabel("Year", fontsize=25)
y_i.set_ylabel("Injured", fontsize=25)
fig = y_i.get_figure()
fig.savefig("result/y_i.png")
plt.close()

s_i = state_i_count.plot('bar', title='Injured by State', label="",
                         figsize=(36, 18), fontsize=20)
s_i.set_xlabel("State", fontsize=25)
s_i.set_ylabel("Injured", fontsize=25)
fig = s_i.get_figure()
fig.savefig("result/s_i.png")
plt.close()

rg_i = rg_i_count.plot(kind='bar', title='Injured', label="",
                       figsize=(20, 15), fontsize=25)
rg_i.set_xlabel("Shooter's Race", fontsize=25)
rg_i.set_ylabel("Injured", fontsize=25)
leg = rg_i.legend(fontsize=25)
leg.set_title("Shooter's Gender", prop={'size': '25'})
fig = rg_i.get_figure()
fig.savefig("result/rg_i.png")
plt.close()

r_f = race_f_count.plot('bar', title='Fetalities', label="",
                        figsize=(20, 15), fontsize=25)
r_f.set_xlabel("Shooter's Race", fontsize=25)
r_f.set_ylabel("Fetalities", fontsize=25)
fig = r_f.get_figure()
fig.savefig("result/r_f.png")
plt.close()

mo_f = month_f_count.plot('bar', title='Fetalities by Month', label="",
                          figsize=(10, 10), fontsize=20)
mo_f.set_xlabel("Month", fontsize=25)
mo_f.set_ylabel("Fetalities", fontsize=25)
fig = mo_f.get_figure()
fig.savefig("result/mo_f.png")
plt.close()

y_f = year_f_count.plot('bar', title='Fetalities by Year', label="",
                        figsize=(20, 10), fontsize=20)
y_f.set_xlabel("Year", fontsize=25)
y_f.set_ylabel("Fetalities", fontsize=25)
fig = y_f.get_figure()
fig.savefig("result/y_f.png")
plt.close()

s_f = state_f_count.plot('bar', title='Fetalities by State', label="",
                         figsize=(36, 18), fontsize=20)
s_f.set_xlabel("State", fontsize=25)
s_f.set_ylabel("Fetalities", fontsize=25)
fig = s_f.get_figure()
fig.savefig("result/s_f.png")
plt.close()

rg_f = rg_f_count.plot(kind='bar', title='Fetalities', label="",
                       figsize=(20, 15), fontsize=25)
rg_f.set_xlabel("Shooter's Race", fontsize=25)
rg_f.set_ylabel("Fetalities", fontsize=25)
leg = rg_f.legend(fontsize=25)
leg.set_title("Shooter's Gender", prop={'size': '25'})
fig = rg_f.get_figure()
fig.savefig("result/rg_f.png")
plt.close()

# Map
plt.figure(figsize=(20, 20))
usa_map = Basemap(llcrnrlon=-119, llcrnrlat=22, urcrnrlon=-64, urcrnrlat=49,
                  projection='lcc', lat_1=32, lat_2=45, lon_0=-95)
usa_map.readshapefile('shape/st99_d00', name='states', drawbounds=True)
c_max = state_count.max()
c_min = state_count.min()
ax = plt.gca()
fig = plt.gcf()
norm = Normalize(vmin=c_min, vmax=c_max)
cmap = plt.cm.Blues
mapper = ScalarMappable(norm=norm, cmap=cmap)
nodata_color = "white"
colors = {}
statenames = []
patches = []
for shapedict, state in zip(usa_map.states_info, usa_map.states):
    statename = shapedict['NAME'].capitalize()
    if statename in state_count.index:
        pop = state_count[statename]
        colors[statename] = mapper.to_rgba(pop)
        statenames.append(statename)
    else:
        statenames.append(statename)
        colors[statename] = nodata_color
for nshape, seg in enumerate(usa_map.states):
    if statenames[nshape] in colors:
        color = rgb2hex(colors[statenames[nshape]])
        poly = Polygon(seg, facecolor=color, edgecolor=color)
        ax.add_patch(poly)
plt.title("Cases density by State")
cax = fig.add_axes([0.27, 0.1, 0.5, 0.05])
cb = ColorbarBase(cax, cmap=cmap, norm=norm, orientation='horizontal')
cb.ax.set_xlabel('Cases Density', fontsize=25)
cb.ax.tick_params(labelsize=25)
plt.savefig("result/c_state_map.png")
plt.close()

plt.figure(figsize=(20, 20))
usa_map = Basemap(llcrnrlon=-119, llcrnrlat=22, urcrnrlon=-64, urcrnrlat=49,
                  projection='lcc', lat_1=32, lat_2=45, lon_0=-95)
geolocator = Nominatim()
usa_map.readshapefile('shape/st99_d00', name='states', drawbounds=True)
for k, v in state_count.iteritems():
    loc = geolocator.geocode(k, timeout=30)
    x, y = usa_map(loc.longitude, loc.latitude)
    usa_map.plot(x, y, marker='o', color='Red',
                 markersize=int(math.sqrt(v) * 10))
plt.title("Cases by City")
plt.savefig("result/c_city_map.png")
plt.close()
