#!/usr/bin/env python

import math

def mygrt(elt, eln, slt, sln):
    PI = 3.141592653

    # /*Go to radians*/
    slat = slt * PI / 180.0
    slon = sln * PI / 180.0
    elat = elt * PI / 180.0
    elon = eln * PI / 180.0

    # /*Correct for ellipticity*/
    slat = math.atan(0.996647 * math.tan(slat))
    elat = math.atan(0.996647 * math.tan(elat))

    # /*Got to colatitudes*/
    slat = PI / 2.0 - slat
    elat = PI / 2.0 - elat

    # /*Make all longitudes postive*/
    if slon < 0.0:
        slon = slon + 2.0 * PI
    if elon < 0.0:
        elon = elon + 2.0 * PI

    # /*compute direction cosines*/
    a = math.sin(elat) * math.cos(elon)
    b = math.sin(elat) * math.sin(elon)
    c = math.cos(elat)
    a1 = math.sin(slat) * math.cos(slon)
    b1 = math.sin(slat) * math.sin(slon)
    c1 = math.cos(slat)

    cd = a * a1 + b * b1 + c * c1
    # /*Make sure acos won't barf*/
    if cd > 1.0:
        cd = 1.0
    if cd < -1.0:
        cd = -1.0

    del_angle = math.acos(cd) * 180.0 / PI
    distance = del_angle * PI * 6371.0 / 180.0

    tmp1 = math.cos(elon) * math.cos(slon) + math.sin(elon) * math.sin(slon)
    tmp2a = 1.0 - cd * cd
    if tmp2a <= 0.0:
        tmp2 = 0.0
        tmp3 = 1.0
    else:
        tmp2 = math.sqrt(tmp2a)
        tmp3 = (math.sin(elat) * math.cos(slat) - math.cos(elat) * math.sin(slat) * tmp1) / tmp2
    # /*Make sure acos won't barf*/
    if tmp3 > 1.0:
        tmp3 = 1.0
    if tmp3 < -1.0:
        tmp3 = -1.0
    z = math.acos(tmp3)

    # /*This test gets correct orientation for az. */
    if (math.sin(slon) * math.cos(elon) - math.cos(slon) * math.sin(elon)) < 0.0:
        z = 2.0 * PI - z

    az = 180.0 * z / PI

    tmp1 = math.cos(slon) * math.cos(elon) + math.sin(slon) * math.sin(elon)
    tmp2a = 1.0 - cd * cd
    if tmp2a <= 0.0:
        tmp2 = 0.0
        tmp3 = 1.0
    else:
        tmp2 = math.sqrt(tmp2a)
        tmp3 = (math.sin(slat) * math.cos(elat) - math.cos(slat) * math.sin(elat) * tmp1) / tmp2
    # /*Make sure acos won't barf*/
    if tmp3 > 1.0:
        tmp3 = 1.0
    if tmp3 < -1.0:
        tmp3 = -1.0
    bz = math.acos(tmp3)
    # /*This test gets correct orientation for baz. */
    if (math.sin(elon) * math.cos(slon) - math.cos(elon) * math.sin(slon)) < 0.0:
        bz = 2.0 * PI - bz

    baz = 180.0 * bz / PI

    return {'del': del_angle, 'dist': distance, 'az': az, 'baz': baz}

# # 测试
# elt = 37.7749  # 经度
# eln = -122.4194  # 纬度
# slt = 40.7128  # 经度
# sln = -74.0060  # 纬度

# info = mygrt(elt, eln, slt, sln)
# print("结果：", info)

def sph2car(dell, az, dep):
    ddel = dell
    daz = az
    ddep = dep

    sfac = 180.0 / 3.1415926

    d1 = 6371.0
    d3 = d1 - ddep
    d2 = math.sqrt(d1 * d1 + d3 * d3 - 2.0 * d1 * d3 * math.cos(ddel / sfac))

    z = 0.5 * (d1 * d1 + d2 * d2 - d3 * d3) / d1

    dist = math.sqrt(d2 * d2 - z * z)

    x = dist * math.sin(daz / sfac)
    y = dist * math.cos(daz / sfac)

    return x, y, z

# # 测试
# del_val = 30.0 # del 值
# az_val = 45.0 # az 值
# dep_val = 100.0 # dep 值

# x, y, z = sph2car(del_val, az_val, dep_val)
# print("转换后的坐标 (x, y, z)：", x, y, z)

def rotate(x, y, theta):
    xr = x * math.cos(theta) - y * math.sin(theta)
    yr = x * math.sin(theta) + y * math.cos(theta)
    return xr, yr

def sph2car_ft(lat_ft, lon_ft, dep_ft, wlat_ft, wlon_ft, theta_ft):
    wlat = wlat_ft
    wlon = wlon_ft
    dep = dep_ft
    lat = lat_ft
    lon = lon_ft
    theta = theta_ft

    dat = mygrt(wlat, wlon, lat, lon)
    del_angle = dat['del']
    az = dat['az']

    x, y, z = sph2car(del_angle, az, dep)

    xr, yr = rotate(x, y, theta)
    x_ft = xr
    y_ft = yr
    z_ft = z

    return x_ft, y_ft, z_ft

# # 测试
# lat_ft = 37.7749 # 经度
# lon_ft = -122.4194 # 纬度
# dep_ft = 100 # 深度
# wlat_ft = 40.7128 # 经度
# wlon_ft = -74.0060 # 纬度
# theta_ft = 30 # 旋转角度

# x_ft, y_ft, z_ft = sph2car_ft(lat_ft, lon_ft, dep_ft, wlat_ft, wlon_ft, theta_ft)
# print("转换后的坐标 (x, y, z)：", x_ft, y_ft, z_ft)

