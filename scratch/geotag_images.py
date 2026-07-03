import os
import subprocess
import sys

def install_and_import(package):
    try:
        __import__(package)
    except ImportError:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Make sure piexif is installed
install_and_import("piexif")

import piexif

def degToMinSec(deg):
    # Convert decimal degrees to EXIF degrees, minutes, seconds format
    d = int(deg)
    md = abs(deg - d) * 60
    m = int(md)
    sd = (md - m) * 60
    return ((d, 1), (m, 1), (int(sd * 100), 100))

def geotag_image(image_path, lat, lon):
    print(f"Geotagging: {image_path}")
    try:
        # Load EXIF
        exif_dict = {"GPS": {}}
        try:
            exif_dict = piexif.load(image_path)
        except Exception:
            pass
            
        lat_ref = b"N" if lat >= 0 else b"S"
        lon_ref = b"E" if lon >= 0 else b"W"
        
        lat_val = degToMinSec(abs(lat))
        lon_val = degToMinSec(abs(lon))
        
        # Inject GPS info
        exif_dict["GPS"] = {
            piexif.GPSIFD.GPSVersionID: (2, 2, 0, 0),
            piexif.GPSIFD.GPSLatitudeRef: lat_ref,
            piexif.GPSIFD.GPSLatitude: lat_val,
            piexif.GPSIFD.GPSLongitudeRef: lon_ref,
            piexif.GPSIFD.GPSLongitude: lon_val,
        }
        
        # Convert EXIF dict to bytes
        exif_bytes = piexif.dump(exif_dict)
        
        # Insert back to JPEG
        piexif.insert(exif_bytes, image_path)
        print("  -> Success!")
    except Exception as e:
        print(f"  -> Error: {e}")

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Pocatello, Idaho coordinates
    pocatello_lat = 42.8713
    pocatello_lon = -112.4455
    
    images = [
        "wp-content/uploads/elementor/thumbs/Tree-Removal-Pocatello-p61zciz9krnb8ds2snv0gp8n4rcmly3potkirtuxhs.jpg",
        "wp-content/uploads/elementor/thumbs/Tree-Trimming-Pocatello-p61zlxd5x4ijc04jwq4pebukzh0rkzf2zcfbjfx79s.jpg",
        "wp-content/uploads/elementor/thumbs/Tree-Stump-Grinding-Tree-Removal-p62035qn7s3s6n3fa6ah3zat1s30p7txcmzsa2dd74.jpg",
        "wp-content/uploads/elementor/thumbs/Tree-Cabling-and-Bracing-Pocatello-p620azq862tsxnptjk6jw0539dh4uexefepg92r9cg.jpg",
        "wp-content/uploads/elementor/thumbs/Tree-Shrub-Removal-Pocatello-p620h9bhqbemc2m4y9p0if7ptul85rszaf9zfhgrv4.jpg",
        "wp-content/uploads/elementor/thumbs/Emergency-Tree-Service-Pocatello-p620lyifwhu8dvsdiatuz8ior7fanagnxopdtahwr4.jpg",
        "wp-content/uploads/2021/04/Tree-Service-Pocatello.jpg",
        "wp-content/uploads/2021/04/Pocatello-Tree-Service.jpg"
    ]
    
    for img in images:
        full_path = os.path.join(root_dir, img.replace('/', os.sep))
        if os.path.exists(full_path):
            geotag_image(full_path, pocatello_lat, pocatello_lon)
        else:
            print(f"File not found: {img}")

if __name__ == "__main__":
    main()
