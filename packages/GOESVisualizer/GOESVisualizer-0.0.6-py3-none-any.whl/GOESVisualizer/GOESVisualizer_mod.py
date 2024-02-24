# UTF-8
# Visualize GEOS16 (west+east) RGB (true) color for a given
# time and location
# Amir Souri (ahsouri@gmail.com)

import xarray as xr
import numpy as np
import os
import cv2
from datetime import timedelta, datetime, date
import requests
import netCDF4
import boto3
from botocore import UNSIGNED
from botocore.config import Config
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import warnings
import glob
from PIL import Image

warnings.filterwarnings("ignore", category=RuntimeWarning)

def datespan(startDate, endDate, delta=timedelta(days=1)):
    currentDate = startDate
    while currentDate < endDate:
        yield currentDate
        currentDate += delta


def get_s3_keys(bucket, s3_client, prefix=''):
    '''
    Generate the keys in an S3 bucket.
    ARGS:
         param bucket: Name of the S3 bucket.
         param prefix: Only fetch keys that start with this prefix (optional).
         source: https://github.com/HamedAlemo/visualize-goes16
    '''

    kwargs = {'Bucket': bucket}

    if isinstance(prefix, str):
        kwargs['Prefix'] = prefix

    while True:
        resp = s3_client.list_objects_v2(**kwargs)
        for obj in resp['Contents']:
            key = obj['Key']
            if key.startswith(prefix):
                yield key

        try:
            kwargs['ContinuationToken'] = resp['NextContinuationToken']
        except KeyError:
            break


def _get_geos(bucket_name, year, day_of_year, hour, gamma):

    # preparing for the amazon cloud connection
    s3_client = boto3.client('s3', config=Config(signature_version=UNSIGNED))

    # RGB colors are bands 2, 3 and 1
    Bands = [2, 3, 1]
    # radiance product name
    product_name = 'ABI-L1b-RadC'
    Rads = []
    for band in Bands:
        # getting the data from the bucket
        fkeys = get_s3_keys(bucket_name, s3_client,
                               prefix=f'{product_name}/{year}/{day_of_year:03.0f}/{hour:02.0f}/OR_{product_name}-M6C{band:02.0f}')
        key = [key for key in fkeys][0]
        resp = requests.get(f'https://{bucket_name}.s3.amazonaws.com/{key}')

        fname = key.split('/')[-1].split('.')[0]
        # opening
        nc4_data = netCDF4.Dataset(fname, memory=resp.content)
        rad = nc4_data.variables['Rad'][:]
        # normalization
        Rads.append(cv2.normalize(rad, np.zeros(
            rad.shape, np.double), 1.0, 0.0, cv2.NORM_MINMAX))
        timesec = nc4_data.variables['t'][:]
        timesec = np.array(timesec)
        # seconds since 2000-01-01 12:00:00
        goesdate = datetime(2000, 1, 1, 12, 0, 0) + \
            timedelta(seconds=float(timesec))
        if band == 1:
            '''
            the red band (band == 2) has a different spatial resolution (500 m)
            compared to others, so we'll take crs and x,y coordinates from the blue band
            the red band will be resized later on.
            '''
            interm = xr.backends.NetCDF4DataStore(nc4_data)
            interm = xr.open_dataset(interm)
            interm = interm.metpy.parse_cf('Rad')
            crs = interm.metpy.cartopy_crs
            x = interm.x
            y = interm.y
        # closing the file
        nc4_data.close()
    # sorting RGB
    R = np.power(np.array(Rads[0]), 1/gamma)
    G = np.power(np.array(Rads[1]), 1/gamma)
    B = np.power(np.array(Rads[2]), 1/gamma)
    # upscaling the R band
    R = cv2.resize(R, dsize=(G.shape[1], G.shape[0]),
                   interpolation=cv2.INTER_CUBIC)
    # apply an adaptive histogram eq to enhance the image contrast
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(100, 100))
    R = clahe.apply(np.uint8(R*255))
    G = clahe.apply(np.uint8(G*255))
    B = clahe.apply(np.uint8(B*255))
    # cashing other variables
    RGB = np.dstack([R, G, B])
    print('Read GOES on ' + '{}'.format(goesdate.strftime(
               '%d %B %Y %H:%M UTC ')))
    output = {}
    output["RGB"] = RGB
    output["goesdate"] = goesdate
    output["crs"] = crs
    output["x"] = x
    output["y"] = y

    return output


def _plotGS(fpng, lon1, lon2, lat1, lat2, RGB, x, y, sat, crs, goesdate):
    '''
    Plotting GOES RGB image
    ARGS:
        is_save (bool): whether we should save it as a png file (True)
                        or plot it (False)
        fpng (char): file.png
    '''
    # plate projection at the desired box
    pc = ccrs.PlateCarree()
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(1, 1, 1, projection=pc)
    ax.set_xlim([lon1, lon2])
    ax.set_ylim([lat1, lat2])
    # plotting GEOS
    ax.imshow(RGB, origin='upper',
              extent=(x.min(), x.max(), y.min(), y.max()),
              transform=crs,
              interpolation='none',
              )
    # plotting costlines
    ax.coastlines(resolution='50m', color='black', linewidth=2)
    ax.add_feature(ccrs.cartopy.feature.STATES)
    # plotting title
    plt.title(sat + ' True Color', loc='left', fontweight='bold', fontsize=16)
    plt.title('{}'.format(goesdate.strftime(
        '%d %B %Y %H:%M UTC ')), loc='right')
    plt.text(0.05, 0.05, 'GEOSVisualizer (by Amir Souri)', transform = ax.transAxes,
             bbox = {'facecolor': 'oldlace', 'pad': 8})
    # writing
    if not os.path.exists('pics'):
        os.makedirs('pics')
    fig.savefig('pics/' + fpng + '.png', format='png', dpi=300)


class GSVis(object):

    def __init__(self, eastorwest, year, month, day, hour, lon1, lon2, lat1, lat2, gamma=1.5):
        '''
        Initializing GSVis with the primary inputs
        ARGS: 
            eastorwest (char): 'east' or 'west' GEOS16/17
            year (int): year
            month (int): month
            day (int): day
            hour (int): hour
            lon1,lon2 (float): boundary longitudes (degree) lon2>lon1
            lat1,lat2 (float): boundary latitudes (degree) lat2>lat1
            gamma (float) : a gamma correction for brightness, for dark scenes
                            I recommend 2.5-3, for bright scenes, 1-2

        '''
        self.lat1 = lat1
        self.lat2 = lat2
        self.lon1 = lon1
        self.lon2 = lon2
        self.gamma = gamma
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        # east or west
        if eastorwest == 'east':
            self.bucket_name = 'noaa-goes16'
            self.sat = 'GOES16'
        elif eastorwest == 'west':
            self.bucket_name = 'noaa-goes17'
            self.sat = 'GOES17'
        else:
            print('the current program only supports east or west.')
            exit()
        # converting date to doy
        self.day_of_year = date(year, month, day).timetuple().tm_yday
        # removing pics folder
        os.system("rm -rf " + "pics")

    def snapshot(self):
        # one snapshot of geos for a given time
        goes = []
        goes.append(_get_geos(self.bucket_name, self.year,
                    self.day_of_year, self.hour, self.gamma))
        self.goes = goes
        goes = []

    def loop(self, end_day, end_hour):
        # find the number of hours
        goes = []
        for timestamp in datespan(datetime(self.year, self.month, self.day, self.hour, 0),
                                  datetime(self.year, self.month,
                                           end_day, end_hour, 0),
                                  delta=timedelta(hours=1)):
            day_of_year = date(timestamp.year, timestamp.month,
                               timestamp.day).timetuple().tm_yday
            goes.append(_get_geos(self.bucket_name, timestamp.year,
                        day_of_year, timestamp.hour, self.gamma))
        self.goes = goes
        goes = []

    def savepics(self):

        for goes_pic in self.goes:
            fpng = 'GEOS_' + \
                '{}'.format(goes_pic["goesdate"].strftime('%d_%B_%Y_%H_UTC'))
            _plotGS(fpng, self.lon1, self.lon2, self.lat1, self.lat2, goes_pic["RGB"], goes_pic["x"], goes_pic["y"], self.sat,
                    goes_pic["crs"], goes_pic["goesdate"])
            
    def animate(gifname):
        images = []
        for filename in sorted(glob.glob('pics/*.png')): # loop through all png files in the folder
            im = Image.open(filename) # open the image
            images.append(im) # add the image to the list

        # save as a gif   
        images[0].save('pics/final.gif',
               save_all=True, append_images=images[1:], optimize=False, duration=400, loop=0)

