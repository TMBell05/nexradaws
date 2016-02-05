# WDSS-II processing utilizing Amazon AWS S3
This CLI provides a way to interact with and process archived NEXRAD data provided by AWS via S3. See here for more info: https://aws.amazon.com/noaa-big-data/nexrad/

### Requirements
- boto3
- click

## Installation 
Clone or download the repository to the desired location

To  install the CLI type  ```pip install -e .``` in the source directory.

## How to use

### ```getNexradData```
```sh
$ getNexradData --help
Usage: getNexradData [OPTIONS]

  Downloads specified radar data

Options:
  -r, --radars TEXT      Comma Separated list of radars
  -s, --start_date TEXT  YYYYmmdd-HHMMSS
  -e, --end_date TEXT    YYYYmmdd-HHMMSS
  -d, --work_dir TEXT    Directory where data should be downloaded
  --netcdf               Use if data needs to be converted to wdssii-netcdf
```

The ```getNexrad``` command downloads all available files between the specified times for the given radars. If the ```-d``` option is not specified, the files are downloaded to the current working directory. 
