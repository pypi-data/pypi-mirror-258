#!/usr/bin/python

import pygame


import sys

pic = pygame.image.load(sys.argv[1])
color = (0,252,0)
for i in range(1920):
    for j in range(1080):
#        R,G,B,A = pic.get_at( (719+i,j) )
        R,G,B,A = pic.get_at( (i,j) )
        if G<140:
            continue # Don't change
        if R==0 and B==0:
            pass
            # CHANGE
        if R>60:
            continue
        if B>60:
            continue
        if R !=0 or B !=0:
            M = (R+B)/2
            green_ratio = G/M

            if green_ratio<3.7: # Not as green as it could be
                continue

            try:
                non_grey_ratio = max(R,B)/min(R,B)
            except:
                non_grey_ratio = max(R,B)

            if M > 40:
                if non_grey_ratio > 1.7:  # Colour imbalance more noticeable
#                if non_grey_ratio > 1.7:  # Colour imbalance more noticeable
                    continue

        pic.set_at((i,j), color)

pygame.image.save(pic, "cleaned/"+sys.argv[1])

