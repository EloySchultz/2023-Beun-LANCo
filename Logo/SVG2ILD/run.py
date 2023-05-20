import video_converter
import image_converter
import os




#Convert your videos here!   ["", Path to SVG sequence, Path to output file]
name="LANCo"
#name="Writing_effect"
video_converter.main(["",os.path.join(os.getcwd(),"content","SVG_sequences",name),os.path.join(os.getcwd(),"ILDA",name+".ild")])


##Convert your static images here
#name = "Logo_Teslan_Outline_Borders_Rainbow"
#image_converter.main(["", os.path.join(os.getcwd(),"content","SVG_static",name+".svg"),os.path.join(os.getcwd(),"ILDA",name+".ild")])


#
# name = "CY-Logo-White-Transparent_test"
# image_converter.main(["", os.path.join(os.getcwd(),"content","SVG_static",name+".svg"),os.path.join(os.getcwd(),"ILDA",name+".ild")])
#
