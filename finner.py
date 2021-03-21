#!/usr/bin/env python

import requests, re 
import numpy as np
from PIL import Image
import urllib.request as urllib
import io
from datetime import date, datetime
import time
import sys


def main(url, t = 10, filename="found.txt"):
    while True:
        response= requests.get(url)
        raw = response.content.decode("utf-8")
        img_pattern = re.compile(r"(https://images\.finncdn\.no/dynamic/default/.+?\.(?:(?:jpg)|(?:png))?)+?", re.IGNORECASE)
        matches_raw = re.findall(img_pattern,raw)
        matches_new = []
        with open(filename, "a+") as file:
            stored = np.loadtxt(filename, dtype=str)
            for match_raw in matches_raw:
                if match_raw not in stored:
                    matches_new.append(match_raw)
            if len(matches_new) > 0:
                file.write("\n".join(matches_new)+"\n")
                print(f"New posting at {datetime.now()}")
                for match in matches_new:
                    fd = urllib.urlopen(match)
                    image_file = io.BytesIO(fd.read())
                    im = Image.open(image_file)
                    im.show()
        time.sleep(t)

if __name__ == "__main__":
    assert len(sys.argv) == 2, "Please provide one argument; the url of the Finn.no page you wish to surveil"
    print("Starting")
    url = sys.argv[1]
    main(url)