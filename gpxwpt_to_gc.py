# Goal:   To convert waypoints into geocaches.
#         There is a long hiking track in hungary called the "Kék túra"
#         There are checkpoints on this track wich are published on http://kektura.hu/szakaszok.html
#         This sript will convert waypoints into Geocaches, so you can use your
#         Geocaching device to help you to navigate to these checkpoints
# Input:  gpx file with waypoints
#         Source is: http://kektura.hu/assets/okt_teljes_belyegzohellyel_gpx_2019-09-11.gpx
# Output: gpx file with waypoints converted to geocaches
#         I have loaded the gpx file into BaseCamp and moved to my Garming eTrex device


import gpxpy.gpx
import datetime
import codecs
import xml.etree.ElementTree as ET

#
# Source: A kektura.hu/szakaszok.html
# http://kektura.hu/assets/okt_teljes_belyegzohellyel_gpx_2019-09-11.gpx
#
input_filename = 'C:\\Users\\apulai\\Downloads\\okt_teljes_belyegzohellyel_gpx_2019-09-11.gpx'
#input_filename = 'C:\\Users\\apulai\\Downloads\\Orszagos_Kektura-pecsetek.gpx'
#input_filename = 'C:\\Users\\apulai\\Downloads\\caches.gpx'
output_filename = 'C:\\Users\\apulai\\Downloads\\oktpecsetek_mint_geocache.gpx'

input_file = open(input_filename, 'r', encoding="utf8")

gpx = gpxpy.parse(input_file)
#print(gpx.to_xml())

gpxout = gpxpy.gpx.GPX()
# Adding groundsepak namespace to the output file
gpxout.nsmap["groundspeak"]="http://www.groundspeak.com/cache/1/0"

i=0
for waypoint in gpx.waypoints:
    #print('id {} waypoint {} -> ({},{})'.format(id(waypoint), waypoint.name, waypoint.latitude, waypoint.longitude))
    #print(waypoint.description)

    # We are creating a new_waypoint which we
    # will add to the output

    new_waypoint = gpxpy.gpx.GPXWaypoint()

    #print('id waypoint out: {}'.format(id(gpxout_waypoint)))
    new_waypoint.latitude = waypoint.latitude
    new_waypoint.longitude = waypoint.longitude
    new_waypoint.elevation = waypoint.elevation
    new_waypoint.name = waypoint.name
    new_waypoint.description = waypoint.description
    new_waypoint.symbol = "Geocache"
    new_waypoint.type = "Geocache"
    new_waypoint.time = datetime.datetime.now()



    i=i+1
    # I had problems with http:// links in the waypoint names
    # So I am removing anything after a "|" sign
    waypoint_name_without_httplink = waypoint.name.split("|")[0]

    # Waypoint is loadaed
    # Now we will add the geocaches attributes
    # Create an element tree
    gpx_extension_cache = ET.fromstring(f"""<?xml version="1.0" encoding="UTF-8"?>
    <groundspeak:cache id="{i}" available="True" archived="False" xmlns:groundspeak="http://www.groundspeak.com/cache/1/0">
    <groundspeak:name>{waypoint.name}</groundspeak:name>
    <groundspeak:placed_by>OKT</groundspeak:placed_by>
    <groundspeak:owner id="68838">Apulai</groundspeak:owner>
    <groundspeak:type>Traditional Cache</groundspeak:type>
    <groundspeak:difficulty>1</groundspeak:difficulty>
    <groundspeak:terrain>1</groundspeak:terrain>
    <groundspeak:country>na</groundspeak:country>
    <groundspeak:short_description html="True">{waypoint_name_without_httplink}</groundspeak:short_description>
    <groundspeak:long_description html="True">{waypoint.description}</groundspeak:long_description>
    </groundspeak:cache>""")

    new_waypoint.extensions.append(gpx_extension_cache)

    gpxout.waypoints.append(new_waypoint)


print('Created GPX:')
print(gpxout.to_xml())


print('Writing to file:')
out_file=codecs.open(output_filename,"w","utf-8")
out_file.write(gpxout.to_xml())
out_file.close()
print("...Done")


