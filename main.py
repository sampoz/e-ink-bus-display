# -*- coding: utf-8 -*-
##
 #  @filename   :   main.cpp
 #  @brief      :   2.9inch e-paper display (B) demo
 #  @author     :   Yehui from Waveshare
 #
 #  Copyright (C) Waveshare     July 31 2017
 #
 # Permission is hereby granted, free of charge, to any person obtaining a copy
 # of this software and associated documnetation files (the "Software"), to deal
 # in the Software without restriction, including without limitation the rights
 # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 # copies of the Software, and to permit persons to  whom the Software is
 # furished to do so, subject to the following conditions:
 #
 # The above copyright notice and this permission notice shall be included in
 # all copies or substantial portions of the Software.
 #
 # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 # FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 # LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 # THE SOFTWARE.
 ##

import epd2in7b
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import requests
import json
from datetime import datetime
import pickle


COLORED = 1
UNCOLORED = 0

def convert_secs_to_time(secs):
        h = (secs / 3600) % 24
        m = (secs % 3600) / 60
        if h < 10:
                h = '0' + str(h);
        if m < 10:
                m = '0' + str(m);
        return str(h) +':' + str(m);

def parse(req):
        vc_body = str(req.content)
        s_idx = vc_body.find("counter-number")
        vc = vc_body[s_idx:s_idx+100].split()
        return int(vc[1].strip('\\n'))

def main():
    epd = epd2in7b.EPD()
    epd.init()

    # clear the frame buffer
    frame_black = [0] * (epd.width * epd.height / 8)
    frame_red = [0] * (epd.width * epd.height / 8)

    # For simplicity, the arguments are explicit numerical coordinates
    #epd.draw_rectangle(frame_black, 10, 130, 50, 180, COLORED);
    #epd.draw_line(frame_black, 10, 130, 50, 180, COLORED);
    #epd.draw_line(frame_black, 50, 130, 10, 180, COLORED);
    #epd.draw_circle(frame_black, 120, 150, 30, COLORED);
    #epd.draw_filled_rectangle(frame_red, 10, 200, 50, 250, COLORED);
    #epd.draw_filled_rectangle(frame_red, 0, 76, 176, 96, COLORED);
    #epd.draw_filled_circle(frame_red, 120, 220, 30, COLORED);


    # draw strings to the buffer
    font = ImageFont.truetype('/home/pi/iosevka.ttf', 32)
    font_clock = ImageFont.truetype('/home/pi/iosevka.ttf', 48)
    font_date = ImageFont.truetype('/home/pi/iosevka.ttf', 24)
    font_delta = ImageFont.truetype('/home/pi/iosevka.ttf', 20)

    # epd.draw_string_at(frame_red, 18, 80, " [o_o] [o_o]  ", font, COLORED)
    # epd.draw_string_at(frame_red, 22, 110, " [o_o] ", font, COLORED)

    # Draw time
    epd.draw_string_at(frame_black, 15, 10, datetime.now().strftime('%H:%M'), font_clock, COLORED)
    epd.draw_string_at(frame_black, 52, 55, datetime.now().strftime('%m-%d'), font_date, COLORED)


    # Draw Temperature
    headers = {"Content-Type":"application/graphql"}
    r = requests.get('https://wttr.in/Otaniemi?format=j1')
    #print r.text
    data = json.loads(r.text)['current_condition']

    old_count = None

    list_count = []
    try:
        with open('/tmp/kk2020', 'r') as f:
           # Read the old count
           dat = f.readlines()
           old_count = dat[0]
    except IOError:
        print("Old status not found")

    try:
        with open('/tmp/e-ink-log_5min', 'r') as f:
           # Read the old count
           list_count = pickle.load(f)
    except IOError:
        print("Old 5min status not found")
    except EOFError:
        print("EOF while reading file")
        list_count = []


    # Victory status
    url_list = ['https://430.fi/kiitos/hyvinvointiyhteiskunta-vahvemmaksi/',
                'https://430.fi/kiitos/oikeudenmukaisia-ilmastotoimia/',
                'https://430.fi/kiitos/lisaa-luonnon-monimuotoisuutta/']

    victory_count = 0

    for url in url_list:
            req = requests.get(url)
            victory_count = victory_count + parse(req)

    # Append to list of values
    list_count.append(victory_count)

    try:
        with open('/tmp/kk2020', 'w') as f:
           # Read the old count
           f.write(str(victory_count))
    except IOError:
        print("Something wrong with writing")

    try:
        with open('/tmp/kk2020_5min', 'w') as f:
           # Read the old count
           pickle.dump(list_count, f)
    except IOError:
        print("Something wrong with writing")


    epd.draw_string_at(frame_black, 15, 90, u"Effective ℃", font_date, COLORED)

    epd.draw_string_at(frame_red, 75, 120, data[0]['FeelsLikeC'], font, COLORED)

    epd.draw_string_at(frame_black, 10, 160, datetime.now().strftime('Kunnollisuus:'), font_date, COLORED)

    epd.draw_string_at(frame_red, 40, 190, str(victory_count), font, COLORED)

    if old_count:
            start = 30
            epd.draw_string_at(frame_black, start, 235, u"Δ 1min:", font_delta, COLORED)

            epd.draw_string_at(frame_red, start + 80, 235, str(victory_count - int(old_count)), font_delta, COLORED)

    # display the frames
    epd.display_frame(frame_black, frame_red)

    # display images
    #frame_black = epd.get_frame_buffer(Image.open('black.bmp'))
    #frame_red = epd.get_frame_buffer(Image.open('red.bmp'))
    epd.display_frame(frame_black, frame_red)

    # You can get frame buffer from an image or import the buffer directly:
    #epd.display_frame(imagedata.IMAGE_BLACK, imagedata.IMAGE_RED)

    #print(str(list_count))
    #print(str(list_count[::-1]))
    #print(str((list_count[::-1])[::5]))

if __name__ == '__main__':
    main()
