import os
import click
from glob import glob

import numpy as np
import matplotlib.pyplot as plt
import pyart
from pyart.util.datetime_utils import datetime_from_radar


def make_plots(data_dirs, work_dir, site, products=None, elevs=None):
    """
    Plot ppis of the given products and elevations for all the files in the data dirs
    :param data_dirs: List of dirs containing data
    :param work_dir: Base dir fro the images
    :param site:
    :param products:
    :param elevs:
    :return:
    """
    files = []
    print data_dirs
    for dir in data_dirs:
        files += glob(os.path.join(dir, '*'))

    with click.progressbar(files, label="Plotting files", fill_char=click.style('#', fg='green')) as files:
        for f in files:
            try:
                radar = pyart.io.read_nexrad_archive(f)

                if products is None:
                    products = radar.fields.keys()

                elevs = _get_elevs(radar)

                # TODO - Implement multiple elevations
                elevs = [elevs[0]]

                # Create the radar display object
                display = pyart.graph.RadarDisplay(radar)
                for field in products:
                    for i, elev in enumerate(elevs):
                        save_dir = os.path.join(work_dir, site, "plots/{prod}/{elev}")
                        save_dir = save_dir.format(prod=field, elev=np.round(float(elev), 1))

                        save_file = os.path.join(save_dir, "%Y%m%d_%H%M%S_{prod}_{elev}.png")
                        save_file = save_file.format(prod=field, elev=np.round(float(elev), 1))
                        save_file = datetime_from_radar(radar).strftime(save_file)

                        try:
                            os.makedirs(save_dir)
                        except OSError:
                            pass

                        range = radar.range['data'][-1] / 1000.
                        fig = plt.figure()
                        display.plot(field, i)
                        display.plot_range_ring(range)
                        plt.xlim([-range, range])
                        plt.ylim([-range, range])
                        plt.savefig(save_file)
                        plt.clf()
                        plt.close()
                        del fig
            except Exception:
                print "Unknown error occured for file " + f


def _find_nearest(a, a0):
    pass


def _get_elevs(radar):
    elevs = []
    for sweep in range(0, radar.sweep_number['data'].size):
        data_slice = radar.get_slice(sweep)
        elev = np.round(np.mean(radar.elevation['data'][data_slice]), 2)
        elevs.append(elev)

    return elevs