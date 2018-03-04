import csv
from shapely.geometry import Point, Polygon,shape
import shapefile
import rtree 

def append_to_file(taxi,shp,new_taxi):
    idx = rtree.index.Index()
    sf = shapefile.Reader(shp)
    shapes = sf.shapes()
    polygon_points = [q.points for q in shapes]
    polygons = [Polygon(q) for q in polygon_points]
    for i,shape in enumerate(shapes):
        idx.insert(i,shape.bbox)
        print i
    print idx
    with open(taxi,'r') as c:
        with open(new_taxi,'w') as w:
            new_csv = csv.writer(w)    
            taxi_csv = csv.reader(c)
            zone = 0
            new_csv.writerow(taxi_csv.next())
            
            for row in taxi_csv:
                zone = 0
                point = [float(row[5]),float(row[6])]
                for j in idx.intersection([point[0],point[1]]):
                    print "in"
                    if(point.within(polygons[j])):
                       print "found" 
                    print shapes.record(j)[0]
                new_csv.writerow(row)
           
def main():
    taxi = '/Users/williamnewman/Desktop/Research/DataFiles/YellowTaxiData/TaxiMatrix/taxiCSV.csv'
    sh = '/Users/williamnewman/Desktop/fwtaz2012shapefiles/NYBPM2012_TAZBoundaryRev.shp'
    new_taxi = '/Users/williamnewman/Desktop/new_taxi.csv'
    append_to_file(taxi,sh,new_taxi)

if __name__=="__main__":
    main()
