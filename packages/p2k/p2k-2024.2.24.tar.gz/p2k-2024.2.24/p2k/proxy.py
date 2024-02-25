import copy
from . import utils, visual
from tqdm import tqdm
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
from matplotlib import gridspec
import cartopy.crs as ccrs

class ProxyRecord:
    def __init__(self, pid:str=None, ptype:str=None, time:float=None, value:float=None,
                 time_name:str=None, value_name:str=None, time_unit:str=None, value_unit:str=None,
                 lat:float=None, lon:float=None, elev:float=None, dt:float=None,
                 environment:str=None, archive:str=None, sensor:str=None, observation:str=None,
                 citation:str=None, url:str=None, ddoi:str=None, agemodel:str=None, source:object=None):
        self.pid = pid
        self.ptype = ptype
        self.time = time
        self.time_name = time_name
        self.time_unit = time_unit
        self.value = value
        self.value_name = value_name
        self.value_unit = value_unit
        self.dt = dt
        self.lat = lat
        self.lon = lon
        self.elev = elev
        self.environment = environment
        self.archive = archive
        self.sensor = sensor
        self.observation = observation
        self.citation = citation
        self.url = url
        self.ddoi = ddoi
        self.agemodel = agemodel
        self.source = source

    def copy(self):
        ''' Make a deepcopy of the object. '''
        return copy.deepcopy(self)

    def infer(self, data:dict, archive_colname:str='archiveType',
              time_colname:str='year', time_unit_colname:str='yearUnits',
              value_colname:str='paleoData_values', value_name_colname:str='paleoData_variableName', value_unit_colname:str='paleoData_units',
              lat_colname:str='geo_meanLat', lon_colname:str='geo_meanLon', elev_colname:str='geo_meanElev',):
        new_rec = self.copy()
        new_rec.ptype = f'{data[archive_colname]}.{data[value_name_colname]}'
        new_rec.time = np.array(data[time_colname])
        new_rec.time_name = 'Time'
        new_rec.time_unit = data[time_unit_colname]
        new_rec.value = np.array(data[value_colname])
        new_rec.value_name = data[value_name_colname]
        new_rec.value_unit = data[value_unit_colname]
        new_rec.lat = float(data[lat_colname])
        new_rec.lon = float(data[lon_colname])
        new_rec.elev = float(data[elev_colname])
        return new_rec

    def plotly(self, **kwargs):
        ''' Visualize the ProxyRecord with plotly
        '''
        time_lb = visual.make_lb(self.time_name, self.time_unit)
        value_lb = visual.make_lb(self.value_name, self.value_unit)

        _kwargs = {'markers': 'o', 'template': 'seaborn'}
        _kwargs.update(kwargs)
        fig = px.line(
            x=self.time, y=self.value,
            labels={'x': time_lb, 'y': value_lb},
            **_kwargs,
        )

        return fig

    def plot(self, figsize=[12, 4], wspace=0.1, hspace=0.1, legend=False, plot_map=True, stock_img=True, ms=200, edge_clr='w', **kwargs):
        ''' Visualize the ProxyRecord with Matplotlib
        '''
        fig = plt.figure(figsize=figsize)

        gs = gridspec.GridSpec(1, 3)
        gs.update(wspace=wspace, hspace=hspace)
        ax = {}

        # plot timeseries
        ax['ts'] = plt.subplot(gs[0, :2])

        _kwargs = {}
        _kwargs.update(kwargs)
        ax['ts'].plot(self.time, self.value, **_kwargs)

        time_lb = visual.make_lb(self.time_name, self.time_unit)
        value_lb = visual.make_lb(self.value_name, self.value_unit)
        ax['ts'].set_xlabel(time_lb)
        ax['ts'].set_ylabel(value_lb)

        title = f'{self.pid} ({self.ptype}) @ (lat:{self.lat:.2f}, lon:{self.lon:.2f})'
        ax['ts'].set_title(title)

        if legend:
            ax['ts'].legend()

        # plot map
        if plot_map:
            ax['map'] = plt.subplot(gs[0, 2], projection=ccrs.Orthographic(central_longitude=self.lon, central_latitude=self.lat))
            ax['map'].set_global()
            if stock_img:
                ax['map'].stock_img()

            transform=ccrs.PlateCarree()
            _kwargs = {'marker': 'o', 'color': 'tab:blue'}
            ax['map'].scatter(
                self.lon, self.lat, marker=_kwargs['marker'],
                s=ms, c=_kwargs['color'], edgecolor=edge_clr, transform=transform,
            )

        return fig, ax


class ProxyDatabase:
    def __init__(self, records:dict=None):
        self.records = {} if records is None else records

    def copy(self):
        ''' Make a deepcopy of the object. '''
        return copy.deepcopy(self)

    def __getitem__(self, key):
        ''' This makes the object subscriptable. '''
        if type(key) is str:
            new = self.records[key]
        else:
            new = self.copy()
            key = new.pids[key]
            new = new.filter(by='pid', keys=key, mode='exact')
            if len(new.records) == 1:
                pid = new.pids[0]
                new = new.records[pid]
        return new

    def __add__(self, records):
        ''' Add a list of records into a database
        '''
        new = ProxyDatabase()
        new.records[self.pid] = self.copy()
        if isinstance(records, ProxyRecord):
            # if only one record
            records = [records]

        if isinstance(records, ProxyDatabase):
            # if a database
            records = [records.records[pid] for pid in records.records.keys()]

        for record in records:
            new.records[record.pid] = record

        new.refresh()
        return new

    def __sub__(self, ref):
        ''' Substract the reference record
        '''
        new = self.copy()
        new.value = self.value - ref.value
        return new

    def filter(self, by, keys, mode='fuzzy'):
        ''' Filter the proxy database according to given ptype list.

        Args:
            by (str): filter by a keyword {'ptype', 'pid', 'dt', 'lat', 'lon', 'loc', 'tag'}
            keys (set): a set of keywords

                * For `by = 'ptype' or 'pid'`, keys take a fuzzy match
                * For `by = 'dt' or 'lat' or 'lon'`, keys = (min, max)
                * For `by = 'loc-squre'`, keys = (lat_min, lat_max, lon_min, lon_max)
                * For `by = 'loc-circle'`, keys = (center_lat, center_lon, distance)
                * For `by = 'tag'`, keys should be a list of tags

            mode (str): 'fuzzy' or 'exact' search when `by = 'ptype' or 'pid'`

        '''
        if isinstance(keys, str): keys = [keys]

        new_db = ProxyDatabase()
        pobjs = []
        for pid, pobj in self.records.items():
            target = {
                'ptype': pobj.ptype,
                'pid': pobj.pid,
                'dt': pobj.dt,
                'lat': pobj.lat,
                'lon': pobj.lon,
                'loc-square': (pobj.lat, pobj.lon),
                'loc-circle': (pobj.lat, pobj.lon),
                'tag': pobj.tags,
            }
            if by in ['ptype', 'pid']:
                for key in keys:
                    if mode == 'fuzzy':
                        if key in target[by]:
                            pobjs.append(pobj)
                    elif mode == 'exact':
                        if key == target[by]:
                            pobjs.append(pobj)
            elif by in ['dt', 'lat', 'lon']:
                if target[by] >= keys[0] and target[by] <= keys[-1]:
                    pobjs.append(pobj)
            elif by == 'loc-square':
                plat, plon = target[by]
                if plat >= keys[0] and plat <= keys[1] and plon >= keys[2] and plon <= keys[3]:
                    pobjs.append(pobj)
            elif by == 'loc-circle':
                plat, plon = target[by]
                d = utils.gcd(plat, plon, keys[0], keys[1])
                if d <= keys[2]:
                    pobjs.append(pobj)
            elif by == 'tag':
                if set(keys) <= target[by]:
                    pobjs.append(pobj)
            
        new_db += pobjs
        return new_db

    def load(self, df, tag='p2k'):
        new_db = self.copy()
        for idx, row in tqdm(df.iterrows(), total=len(df)):
            pid = f'{tag}/{idx+1:06d}'
            rec = ProxyRecord(pid=pid)
            rec.source = row
            rec = rec.infer(row)
            new_db.records[pid] = rec

        return new_db