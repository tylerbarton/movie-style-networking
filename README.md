# movie-style-networking
Create a movie-style visualization of the trace route a packet takes to reach a destination IP.

# Quick Start
`visual.py -t 146.97.33.2`

# ⚙ Options
    -t, --target                        Target IP
    --help                              Print this help text and exit
    --version                           Print program version and exit
    --hops                              Change The maximum number of hops for the traceroute command
    -q, --map_quality                   The quality of the map as crude (c), low (l), or intermediate (i)
    -map_draw_coast                     If true, will draw a light coast line dividing land and bodies of water

# ❓ Frequently Asked Questions 

## Why do some hops in the trace route not return?
Traceroute works by incrementing a packet's TTL by 1, causing the recipient server to return an error datagram (11 - Time Exceeded) back to the sender. This describes the hacky-nature of traceroute by allowing us to see that it is not a single packet but instead, many packets being sent until a destination is reached.

To protect some server information, Some firewalls suppress the error, making traceroute an imperfect solution. Even if there are some failures, the traceroute will continue to the destination node allowing for gaps.

## Why are some locations incorrect?
IP addresses *can* reveal a geolocation rather than a precise location. There is no exact science to IP mapping. Because of this, some IP addresses do not have an exact location and are instead given a default value.

For the United States, this location is 38°N 97°W, which is a pond in Kansas. 