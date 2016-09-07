import os

import click

import nexradaws


@click.command(help="Downloads specified radar data\n")
@click.option(
    '--radars', '-r',
    help="Comma Separated list of radars")
@click.option(
    '--start_date', '-s',
    help="YYYYmmdd-HHMMSS")
@click.option(
    '--end_date', '-e',
    help="YYYYmmdd-HHMMSS")
@click.option(
    '--work_dir', '-d',
    help="Directory where data should be downloaded")
@click.option(
    '--netcdf',
    default=False,
    is_flag=True,
    flag_value=True,
    help="(NOT IMPLEMENTED) Use if data needs to be converted to cf-netcdf"
    )
def get_nexrad(radars, start_date, end_date, work_dir, netcdf=False):
    
    if radars is None:
        raise click.ClickException("Please specify some radars")

    if start_date is None:
        raise click.ClickException("Please specify a start date")

    if end_date is None:
        raise click.ClickException("Please specify an end date")

    if work_dir is None:
        work_dir = os.getcwd()

    # Split up radars into list
    radars = radars.split(',')

    for radar in radars:
        data_dirs = nexradaws.scripts.aws.get_nexrad_data(radar, start_date, end_date, work_dir)

        # Convert to netcdf if desired
        if netcdf:
            pass  # TODO - Implement netcdf conversion

