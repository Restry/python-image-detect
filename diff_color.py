# from colormath.color_objects import sRGBColor, LabColor
# from colormath.color_conversions import convert_color
# from colormath.color_diff import delta_e_cie2000
import numpy
import math

# def compareColor(first, second):
#   return delta_e_cie2000(convert_color(sRGBColor(first[0],first[1],first[2]), LabColor),
#   convert_color(sRGBColor(second[0],second[1],second[2]), LabColor))

# print("黑和红 = " + str(delta_e_cie2000(convert_color(sRGBColor(0, 0, 0), LabColor), convert_color(sRGBColor(255, 0, 0), LabColor))))
# print("黑和白 = " + str(delta_e_cie2000(convert_color(sRGBColor(0, 0, 0), LabColor), convert_color(sRGBColor(255, 255, 255 ), LabColor))))
# print("蓝和白 = " + str(delta_e_cie2000(convert_color(sRGBColor(0, 55, 255), LabColor), convert_color(sRGBColor(255, 255, 255 ), LabColor))))
# print("白和白 = " + str(delta_e_cie2000(convert_color(sRGBColor(255, 255, 255), LabColor), convert_color(sRGBColor(255, 255, 255 ), LabColor))))
# print("白和灰{}".format(compareColor([255,255,255],[245,245,245])))

def compareColor(r1, r2):
    rgb1 = numpy.array(r1)
    rgb2 = numpy.array(r2)
    return math.sqrt(((rgb1[0]-rgb2[0])**2)+((rgb1[1]-rgb2[1])**2)+((rgb1[2]-rgb2[2])**2))
  

# def compareColor(r1, r2):
     
#     rgb1 = numpy.array(r1)
#     rgb2 = numpy.array(r2)
#     # rgb1 = r1
#     # rgb2 = r2

#     rm = 0.5*(rgb1[0]+rgb2[0])
#     d = sum((2+rm, 4, 3-rm)*(rgb1-rgb2)**2)**0.5
#     return d
