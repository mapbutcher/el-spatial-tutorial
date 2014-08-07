# #################################################################################
#  data-loader
#  Author: Simon Hope - Geoplex - September 2013
#
#  Loads a shapefile into an Elastic Search Index. Assumes Elastic search index, type and mapping has been set up to match the schema of the shapefile
#
#  Usage: data-loader.py <elastic search url> <shapefile> <simplify> <tolerance>
#    e.g. 'python data-loader.py 'http://ec2-54-253-58-186.ap-southeast-2.compute.amazonaws.com:9200/geo_suburbs/suburb/' '../data/SSC_2011_AUST_SIMPLIFY.shp''
#
# #################################################################################

import sys, argparse
import fiona
import shapely
import json
import urllib2
import logging
import pyes


logging.basicConfig(filename='data-loader.log',level=logging.DEBUG)

#loads single records over http using urllib2
def simpleHttpLoad(esurl, f):

    try:
        logging.info('Pushing to: '+ esurl+f['id']) 
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        request = urllib2.Request(esurl+f['id'], data=json.dumps(f))
        request.add_header('Content-Type', 'application/json')
        request.get_method = lambda: 'PUT'
        url = opener.open(request)
    except Exception as e:
        logging.error(e)


def validateGeometry(geom):
    from shapely.validation import explain_validity
    if (explain_validity(geom) == 'Valid Geometry'):
        return True
    else:
        return False


def simplifyGeometry(geom, tolerance):
    logging.info('Simplifying Geometry') 
    return geom.simplify(tolerance, preserve_topology=False)


def processData(esurl, esindex, estype,  shpPath, simplify, tolerance, startfrom):
    
    # Open a file for reading
    try:
       with open(shpPath): pass
    except IOError:
       print 'Unable to locate file: ' + shpPath

    #open the es connection
    from pyes import ES
    conn = ES(esurl, timeout=60, bulk_size=10)

    #check that a tolerance is passed when simplifying.
    if(simplify==True):
        if (tolerance==None):
            raise ValueError('You must pass a valid tolerance if simplifying geometry') 

    #use fiona to open the shapefile and read it
    try:    
        with fiona.open(shpPath) as source:


            for f in source:

                featid = int(f['id'])
                if(featid > startfrom):
                
                    #grab the geom
                    from shapely.geometry import shape
                    geom = shape(f['geometry'])

                    #simplify if required
                    if (validateGeometry(geom)):
                        if(simplify==True):
                            geom = simplifyGeometry(geom, tolerance)

                    #if the geom is valid then push it into es
                    if (validateGeometry(geom)):
                        data = json.dumps(f)
                        key = f['id']
                        conn.index(data,esindex,estype,key, bulk=True)
                        

                    else:
                        logging.error('Invalid Geometry: ' + f['id']) 

    except:
        raise

if __name__ == '__main__':

        #grab the args
        parser = argparse.ArgumentParser(description='Load data into Elastic Search')
        parser.add_argument('esurl', metavar='rooturl', type=str, help='Root url of elastic search, including index and type')
        parser.add_argument('esindex', metavar='esindex', type=str, help='The elastic search index youre loading into')
        parser.add_argument('estype', metavar='estype', type=str, help='The elastic search type your loading into')
        parser.add_argument('shpPath', metavar='shpPath', type=str, help='Path to the shapefile')
        parser.add_argument('--simplify', action='store_true', help='Whether to simplify the geometry')
        parser.add_argument('--tolerance', metavar='tolerance', type=float, help='simplification tolerance distance')
        parser.add_argument('--startfrom', metavar='startfrom', type=int, help='an index to start the load from')

        args = parser.parse_args()

        esurl = args.esurl
        esindex = args.esindex
        estype = args.estype
        shpPath = args.shpPath
        simplify = args.simplify
        tolerance = args.tolerance
        startfrom = args.startfrom

        processData(esurl, esindex, estype, shpPath, simplify, tolerance, startfrom)