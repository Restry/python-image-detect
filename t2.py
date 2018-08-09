from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
from mathutils import Vector, Color
import numpy
import math


def compareColor(first, second):
    return delta_e_cie2000(convert_color(sRGBColor(first[0], first[1], first[2]), LabColor),
                           convert_color(sRGBColor(second[0], second[1], second[2]), LabColor))


print("黑和红 = " + str(delta_e_cie2000(convert_color(sRGBColor(0, 0, 0),
                                                   LabColor), convert_color(sRGBColor(255, 0, 0), LabColor))))
print("黑和白 = " + str(delta_e_cie2000(convert_color(sRGBColor(0, 0, 0),
                                                   LabColor), convert_color(sRGBColor(255, 255, 255), LabColor))))
print("蓝和白 = " + str(delta_e_cie2000(convert_color(sRGBColor(0, 55, 255),
                                                   LabColor), convert_color(sRGBColor(255, 255, 255), LabColor))))
print("白和白 = " + str(delta_e_cie2000(convert_color(sRGBColor(255, 255, 255),
                                                   LabColor), convert_color(sRGBColor(255, 255, 255), LabColor))))
print("白和灰 = {}".format(compareColor([255, 255, 255], [245, 245, 245])))


# def color_match(col1, col2, tol=0.001):
#     '''
#     Return true if vector col1 is within tol of vector col2
#     '''
#     def vector(col):
#         # sanitize range (-2, 3, 5) = (0, 1, 1)
#         return Vector([max(0, min(1, c)) for c in col])

#     return vector(col1) - vector(col2)


# white = Color((255, 255, 255))
# w1 = Color((255, 255, 255))

# print(white == w1)
# # test code
# print("-蓝和白 = " + str(color_match(w1, white).length))
# print("-黑和红 = " + str(color_match(Color((0, 0, 0)),
#                                   Color((255, 0, 0))).length))
# print("-白和灰 = " + str(color_match(Color((255, 255, 255)),
#                                   Color((245, 245, 245)))))


# def ColorDistance(rgb1, rgb2):
#     '''d = {} distance between two colors(3)'''
#     rm = 0.5*(rgb1[0]+rgb2[0])
#     d = sum((2+rm, 4, 3-rm)*(rgb1-rgb2)**2)**0.5
#     return d


# # print("-黑和灰 = {}".format(ColorDistance(numpy.array([0, 0, 0]),numpy.array([245, 245, 245]))))
# # print("-黑和白 = {}".format(ColorDistance(numpy.array([0, 0, 0]),numpy.array([255, 255, 255]))))
# # print("-黑和红 = {}".format(ColorDistance(numpy.array([0, 0, 0]),numpy.array([255, 0, 0]))))
# print(
#     "-灰和白 = {}".format(ColorDistance(numpy.array([245, 245, 245]), numpy.array([255, 255, 255]))))

# print("-灰和白 = {}".format(ColorDistance(numpy.array((180, 133, 107)),
#       numpy.array((194, 195, 204)))))


def ColorDiff(r1, r2):
    rgb1 = numpy.array(r1)
    rgb2 = numpy.array(r2)
    return math.sqrt(((rgb1[0]-rgb2[0])**2)+((rgb1[1]-rgb2[1])**2)+((rgb1[2]-rgb2[2])**2))
  
print("-黑和灰 = {}".format(ColorDiff((0,0,0), (245, 245, 245))))
print("-黑和白 = {}".format(ColorDiff((0,0,0), (255, 255, 255))))
print("-黑和红 = {}".format(ColorDiff((0,0,0), (255, 0, 0))))
print("-蓝和白 = {}".format(ColorDiff((0, 55, 255), (255, 255, 255))))
print("-白和灰 = {}".format(ColorDiff([255, 255, 255], [245, 245, 245])))
print("-白和灰 = {}".format(ColorDiff([255, 255, 255], [235, 245, 245])))
print("-白和灰 = {}".format(ColorDiff([255, 255, 255], [225, 245, 245])))
print("-白和灰 = {}".format(ColorDiff([255, 255, 255], [215, 245, 245])))
print("-白和灰 = {}".format(ColorDiff([255, 255, 255], [205, 245, 245])))
print("-白和灰 = {}".format(ColorDiff([255, 255, 255], [195, 245, 245])))
print("-白和灰 = {}".format(ColorDiff([255, 255, 255], [185, 245, 245])))
