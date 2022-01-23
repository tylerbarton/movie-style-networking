import platform
import sys
import subprocess
import urllib.request
import json
import argparse

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from colour import Color

# Added to solve SSL: CERTIFICATE_VERIFY_FAILED in url request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
ssl.SSLContext.verify_mode = ssl.VerifyMode.CERT_OPTIONAL

green = Color("green")
colors = list(green.range_to(Color("red"), 30))

target = ''
max_hops = "30"
map_size = (20, 12)
map_draw_coast = True
map_quality = 'i'  # only crude, low, and intermediate are available


def get_loc(IP):
    """
    Convert an IP to a world location.

    :param IP: a string representation of an IP
    :return: (latitude, longitude) tuple
    """

    # Use a geolocation service to get a location
    url = "https://geolocation-db.com/json/" + IP
    response = urllib.request.urlopen(url)
    encoding = response.info().get_content_charset('utf8')

    data = json.loads(response.read().decode(encoding))
    try:
        lat = float(data["latitude"])
        lon = float(data["longitude"])
        if lat == 0.0 and lon == 0.0:
            return None, None
        return lat, lon
    except:
        return None, None


def plot_tracert():
    """
    Creates a plot of a traceroute command call.
    """
    # macOS and Linux
    if platform.system() == 'Linux' or platform.system() == 'Darwin':
        proc = subprocess.Popen(["traceroute -m " + max_hops + " -n " + target], stdout=subprocess.PIPE, shell=True,
                                universal_newlines=True)

        # plot world map
        fig = plt.figure(figsize=map_size, edgecolor='w')
        m = Basemap(projection='mill', lon_0=0, resolution=map_quality)
        m.shadedrelief(scale=0.1)

        # Parse traceroute results
        last_lon = None
        last_lat = None
        i = 1
        for line in proc.stdout:
            print(line, end="")
            hop_ip = line.split()[1]
            if hop_ip in ("*", "to"):
                continue
            lat, lon = get_loc(hop_ip)
            if lat is None:
                continue
            if last_lat is not None and (last_lat - lat + last_lon - lon) != 0.0:
                # print(lastLat,lastLon,lat,lon)
                x, y = m(lon, lat)
                m.scatter(x, y, 10, marker='o', color='b')
                line, = m.drawgreatcircle(last_lon, last_lat, lon, lat, color=colors[i])
            last_lat = lat
            last_lon = lon
            i += 1

        plt.tight_layout()
        plt.show()

    # Windows OS
    elif platform.system() == 'Windows':
        proc = subprocess.Popen("C:\\Windows\\System32\\TRACERT.exe -h " + max_hops + " -d -4 " + target,
                                stdout=subprocess.PIPE, shell=True, universal_newlines=True)

        fig = plt.figure(figsize=map_size, edgecolor='w')
        m = Basemap(projection='mill', lon_0=0, resolution=map_quality)
        m.shadedrelief(scale=0.05)

        # Parse traceroute results
        last_lon = None
        last_lat = None
        i = 1
        for line in proc.stdout:
            print(line, end="")
            if len(line.split()) != 8:
                continue
            else:
                hop = line.split()[7]
                if hop in ("*", "to"):
                    continue

                lat, lon = get_loc(hop)
                if lat is None:
                    continue
                if last_lon is not None and (last_lat - lat + last_lon - lon) != 0.0:
                    x, y = m(lon, lat)
                    m.scatter(x, y, 10, marker='o', color='b')
                    m.drawcoastlines(linewidth=0.05, linestyle='solid', color='k', antialiased=1, ax=None, zorder=None)
                    line, = m.drawgreatcircle(last_lon, last_lat, lon, lat, color=colors[i].get_hex())

                # Update
                last_lat = lat
                last_lon = lon
                i += 1

        plt.tight_layout()
        plt.show()

    # Unknown OS
    else:
        print("Unsupported Operating System")
        sys.exit(-1)


if __name__ == '__main__':
    # Parse args
    parser = argparse.ArgumentParser(description='Movie-Style Networking Visualization')

    requiredNamed = parser.add_argument_group('Required arguments:')
    requiredNamed.add_argument('-t', '--target', type=str,
                               help='Target IP', required=True)

    optionalNamed = parser.add_argument_group('Optional arguments:')
    optionalNamed.add_argument('--hops', '--max_hops', type=str, default="30",
                               help='The maximum number of hops for the traceroute command.', required=False)
    optionalNamed.add_argument('-q', '--map_quality', type=str, default='i',
                               help='The quality of the map as crude (c), low (l), or intermediate (i).',
                               required=False)
    optionalNamed.add_argument('-s', '--map_size', nargs=2, metavar=('W', 'H'), default='20, 12',
                               help='The size of the map (width, height) in 1000\'s of pixels.', required=False)
    optionalNamed.add_argument('--map_draw_coast', type=bool, default=True,
                               help='If true, will draw a light coast line dividing land and bodies of water.',
                               required=False)
    optionalNamed.add_argument('--version', action='version', version='0.0.1')
    args = parser.parse_args()

    target = args.target
    max_hops = args.hops
    map_quality = args.map_quality
    map_draw_coast = args.map_draw_coast

    # Draw the map
    plot_tracert()
