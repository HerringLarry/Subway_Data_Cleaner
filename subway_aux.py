import shapefile
from shapely.geometry import Point # Point class
from shapely.geometry import shape
import csv
import string
import ogr

def add_zone(sub,sh,outp):
    with open(sub,'r') as rd:
        c = csv.reader(rd)
        new = []
        r = c.next()
        r.append('zone')
        new.append(r)
        drv = ogr.GetDriverByName('ESRI Shapefile')
        ds_in = drv.Open(sh)
        lyr_in = ds_in.GetLayer(0)
        with open(outp,'w') as writ:
            w = csv.writer(writ)
            w.writerows(r)
            for row in c:
                row = row[0].split()
                if len(row) >= 13:
                    pt = ogr.Geometry(ogr.wkbPoint)
                    x = only_numbers(row[11])
                    y = only_numbers(row[12])
                    pt.SetPoint_2D(0,x,y)
                    lyr_in.SetSpatialFilter(pt)
                    for feat in lyr_in:
                        ply = feat.GetGeometryRef()
                        if ply.Contains(pt):    
                            print "Name"
                            name = all_records[i][5]
                            print name
                            row.append(name)
                        
                w.writerows([row])

def only_numbers(num):
    a = string.maketrans('','')
    nodigs = a.translate(a,string.digits + '.')
    return float(num.translate(a,nodigs))



def main():
   f1 = '/Users/williamnewman/Desktop/dates/1126update.txt'
   out = '/Users/williamnewman/Desktop/dates/1126rolled.txt'
   sh = '/Users/williamnewman/Downloads/2010CensusTracts/geo_export_d465ff27-f129-49fa-a5c8-39394731f42c.shp'
   add_zone(f1,sh,out)


if __name__ == "__main__":
    main()
