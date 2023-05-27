import video_converter
import image_converter
import os





from os import listdir
from os.path import isfile, join
#
# mypath = os.path.join(os.getcwd(), "content","SVG_static")
# onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
#
#
# for file in onlyfiles:
#     name=file
#     image_converter.main(["", os.path.join(os.getcwd(), "content", "SVG_static", name),
#                           os.path.join(os.getcwd(), "ILDA", name + ".ild")])
#
#


directory = os.path.join(os.getcwd(), "content","SVG_sequences")
films=[x[0] for x in os.walk(directory)]
print(films)
films = films[1:]

for film in films:
    name=film
    print(film)
    video_converter.main(["",os.path.join(os.getcwd(),"content","SVG_sequences",name),os.path.join(os.getcwd(),"ILDA",name+".ild")])

#print(onlyfiles)
#Convert your videos here!   ["", Path to SVG sequence, Path to output file]
# name="LANCo"
# #name="Writing_effect"
# video_converter.main(["",os.path.join(os.getcwd(),"content","SVG_sequences",name),os.path.join(os.getcwd(),"ILDA",name+".ild")])

#
# #Convert your static images here
# name = "Logo_Teslan_Outline_Borders_Rainbow"
# image_converter.main(["", os.path.join(os.getcwd(),"content","SVG_static",name+".svg"),os.path.join(os.getcwd(),"ILDA",name+".ild")])


#
# name = "CY-Logo-White-Transparent_test"
# image_converter.main(["", os.path.join(os.getcwd(),"content","SVG_static",name+".svg"),os.path.join(os.getcwd(),"ILDA",name+".ild")])
#
