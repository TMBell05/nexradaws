import os
import re
from datetime import datetime, timedelta

import boto3
import click

import nexradaws


def get_datetime_from_key(key, radar):
    tmp = key.split('/')[-1]
    end = re.search("V\d\d", tmp)

    # TODO - Temporary fix. Need to be able to download tars as well?
    if 'NXL2' in tmp:
        return None

    try:
        return datetime.strptime(tmp, radar + '%Y%m%d_%H%M%S_' + str(end.group()) + '.gz')
    except ValueError:
        return datetime.strptime(tmp, radar + '%Y%m%d_%H%M%S.gz')
    except AttributeError:
        return datetime.strptime(tmp, radar + '%Y%m%d_%H%M%S.gz')


def get_objects(radar, date):
    s3 = boto3.resource('s3')

    bucket = s3.Bucket(nexradaws.NEXRAD_BUCKET)

    # Create prefix to filter keys in bucket
    prefix = '%s/%s' % (date.strftime("%Y/%m/%d"), radar)

    objs = []
    for obj in bucket.objects.filter(Prefix=prefix):
        objs.append(obj)

    return objs


def download_radar_objects(s3_objects, work_dir, radar, date):
    dest_dirs = []
    with click.progressbar(s3_objects, label='Downloading files for %s %s' % (radar, date.strftime('%Y-%m-%d')),
                           fill_char=click.style('#', fg='green')) as s3_objects:
        for obj in s3_objects:
            # Get the filename 
            filename = obj.key.split('/')[-1]

            # Get the object date
            obj_date = get_datetime_from_key(obj.key, radar)

            if obj_date is not None:
                # Create the destination directory 
                dest_dir = os.path.join(work_dir, radar, 'raw', obj_date.strftime("%Y%m%d"))
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                if dest_dir not in dest_dirs:
                    dest_dirs.append(dest_dir)

                # Create the destination file
                filename = os.path.join(dest_dir, filename)

                # Download the file
                _download_from_obj_summary(obj, filename)
    return dest_dirs


def filter_objects_by_date(s3_objects, radar, start_date, end_date):
    good_objs = []
    for obj in s3_objects:
        tmp_date = get_datetime_from_key(obj.key, radar)

        if tmp_date is not None:
            if tmp_date >= start_date and tmp_date <= end_date:
                good_objs.append(obj)

    return good_objs


def get_nexrad_data(radar, start_date, end_date, work_dir):
    # Turn date strings into datetime objects
    start_date = datetime.strptime(start_date, "%Y%m%d-%H%M%S")
    end_date = datetime.strptime(end_date, "%Y%m%d-%H%M%S")

    # Create timedelta to iterate through the possible days
    td = timedelta(days=1)

    # Empty list for the dirs that contain data (used for other processes)
    out_dirs = []

    # Loop through the days
    date = start_date
    while date <= end_date:
        objects = get_objects(radar, date)
        if len(objects) != 0:
            objects = filter_objects_by_date(objects, radar, start_date, end_date)

            dest_dir = download_radar_objects(objects, work_dir, radar, date)
            out_dirs += dest_dir
        else:
            print "No files found for %s during hour %s" % (radar, date)
        date += td

    return out_dirs


def _download_from_obj_summary(obj, filename):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(obj.bucket_name)
    bucket.download_file(obj.key, filename)
