#!/usr/bin/env python3
import argparse, json
from PIL import Image, ExifTags

def get_gps_coords(image_path):
    try:
        img = Image.open(image_path)
        exif = img._getexif()
        if not exif:
            return "No EXIF data found."
        gps = {}
        for tag, value in exif.items():
            tag_name = ExifTags.TAGS.get(tag, tag)
            if tag_name == "GPSInfo":
                gps = value
                break
        if not gps:
            return "No GPS data found."
        # Convert GPS coordinates from degree, minute, second to decimal
        def to_decimal(gps_data):
            # expecting tuple (deg, min, sec) for each coordinate
            lat_ref = gps_data.get(1, 'N')
            lon_ref = gps_data.get(3, 'E')
            lat = gps_data.get(2)
            lon = gps_data.get(4)
            if not lat or not lon:
                return None, None
            lat_dec = lat[0] + lat[1]/60 + lat[2]/3600
            lon_dec = lon[0] + lon[1]/60 + lon[2]/3600
            if lat_ref == 'S':
                lat_dec = -lat_dec
            if lon_ref == 'W':
                lon_dec = -lon_dec
            return lat_dec, lon_dec
        lat, lon = to_decimal(gps)
        if lat is None or lon is None:
            return "Incomplete GPS data."
        return f"Latitude: {lat}, Longitude: {lon}"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract GPS coordinates from EXIF")
    parser.add_argument("image", help="Image file path")
    args = parser.parse_args()
    print(get_gps_coords(args.image))
