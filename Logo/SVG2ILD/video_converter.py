#!/usr/bin/python3
# -*- coding: utf-8 -*-
import core
import os, sys, math
import struct

if __name__ == "__main__":
    main(sys.argv)

def main(argv):
    global color_dict, current_frame, number_of_frames
    from os import listdir
    from os.path import isfile, join

    headers = []
    frames = []
    if argv[1] == "-q":
        verbose = False
        argv = [argv[0]] + argv[2:]

    if argv[1] == "-noopt":
        optimize = False
        argv = [argv[0]] + argv[2:]

    if argv[1] == "-noctr":
        center = False
        argv = [argv[0]] + argv[2:]

    if argv[1] == "-cfg":
        params.load(argv[2])
        sys.argv = [argv[0]] + argv[3:]

    onlyfiles = [f for f in listdir(argv[1]) if isfile(join(argv[1], f))]
    onlyfiles.sort()
    number_of_frames = len(onlyfiles)
    current_frame = 0;
    samples=[]
    print("Saving in:" + str(argv[2]))
    fout = open(argv[2], "wb")
    for path in onlyfiles:
        print("Processing" + str(path))
        path = os.path.join(argv[1],path)
        if current_frame==0:
            color_dict = core.create_color_table(path)
        optimize = True
        verbose = True
        center = True
        params = core.RenderParameters()



        if verbose:
            print("Parse")
        frame = core.load_svg(path)
        if verbose:
            print("Done")

        if optimize:
            frame.sort()

        if verbose:
            print("Render")
        rframe = frame.render(params)
        if verbose:
            print("Done")
        a,b = core.write_ild(fout,current_frame, params, rframe, argv[2], center)
        frames.append(a)
        samples.append(b)
        current_frame+=1
    current_frame=0;
    core.write_color(fout)
    for i in range(number_of_frames):
        hdr = struct.pack(">4s3xB8s8sHHHBx", b"ILDA", 1, b"svg2ilda", b"", samples[current_frame], current_frame, number_of_frames, 0)
        fout.write(hdr)
        fout.write(frames[current_frame])
        current_frame+=1;
    hdr = struct.pack(">4s3xB8s8sHHHBx", b"ILDA", 0, b"svg2ilda", b"", 0, 0, number_of_frames, 0)
    fout.write(hdr)
    fout.close()

    # if verbose:
    # 	print("Statistics:")
    # 	print(" Objects: %d"%params.objects)
    # 	print(" Subpaths: %d"%params.subpaths)
    # 	print(" Bezier subdivisions:")
    # 	print("  Due to rate: %d"%params.rate_divs)
    # 	print("  Due to flatness: %d"%params.flatness_divs)
    # 	print(" Points: %d"%params.points)
    # 	print("  Trip: %d"%params.points_trip)
    # 	print("  Line: %d"%params.points_line)
    # 	print("  Bezier: %d"%params.points_bezier)
    # 	print("  Start dwell: %d"%params.points_dwell_start)
    # 	print("  Curve dwell: %d"%params.points_dwell_curve)
    # 	print("  Corner dwell: %d"%params.points_dwell_corner)
    # 	print("  End dwell: %d"%params.points_dwell_end)
    # 	print("  Switch dwell: %d"%params.points_dwell_switch)
    # 	print(" Total on: %d"%params.points_on)
    # 	print(" Total off: %d"%(params.points - params.points_on))
    # 	print(" Efficiency: %.3f"%(params.points_on/float(params.points)))
    # 	print(" Framerate: %.3f"%(params.rate/float(params.points)))