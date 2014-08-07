Elasticsearch - Spatial Tutorial
===================

## Introduction

Search has been typically poorly implemented in GIS systems. Many implementations provide interfaces to make structured queries over GIS data, but (I hope you agree) this approach has some serious limitations.

In my experience many GIS solutions do a great deal of things, some of these things they do very well and some things they do very poorly. I would hope they do the GIS bits well. 

When designing a solution I rarely source all components from the same source. Search is a good example of this. A solution viewed by the end user is simply a facade over many moving parts, and each part should be selected for its ability to fulfill its respective responsibilities.

## Requirements 

To run this tutorial you'll need to install [virtulbox](https://www.virtualbox.org/) and [vagrant](http://www.vagrantup.com/).

I also recommend using the [Sense](https://chrome.google.com/webstore/detail/sense/doinijnbnggojdlcjifpdckfokbbfpbo?hl=en) extension for Chrome which provides a JSON aware interface to Elasticsearch.

Interactions with the Elasticsearch API are illustrated using [cURL]()

## Grab the repo
```bash
$ git clone https://github.com/mapbutcher/el-spatial-tutorial.git
```

## Exercise 1 - Installation

Firstly lets get the initial exercise ready.
```bash
$ cd el-spatial-tutorial
$ git checkout tags/1.0.0
```

OK now we need to create a virtual machine and install Elasticsearch. With vagrant this is easy. However the first time you do this Vagrant needs to do two things:

+ pull down a base machine
+ provision the base machine with Elasticsearch.

so it takes a little longer. To do these things run:
```bash
$ vagrant up
```

During the installation vagrant provisioned the machine with Elasticsearch and some useful plugins: 
+ [Paramedic](https://github.com/karmi/elasticsearch-paramedic)
+ [Head](http://mobz.github.io/elasticsearch-head/)
+ [BigDesk](https://github.com/lukas-vlcek/bigdesk)

Vagrant also sets up some port forwarding which allows us to access the machine using ssh as well as the Elasticsearch API.

If you want to ssh to the machine you can run:
```bash
$ vagrant ssh
```

Paramedic, Head and BigDesk should be accessible by accessing the following URL's:

+ http://127.0.0.1:9200/_plugin/paramedic/
+ http://127.0.0.1:9200/_plugin/head/
+ http://127.0.0.1:9200/_plugin/bigdesk/

## Exercise 2 - Indexing some spatial data.

### Basic Scenario

We need some data for our simple scenario. The datasets can be found in the data directory of the repository. The data we're going to use is information on road crashes as well as suburb boundaries. Both datasets are available for download via the [Victorian (Australia) State Government Data Directory](http://www.data.vic.gov.au/).

In our simple scenario we want to be able to do the following: 
+ search for crashes within a particular suburb
+ search for crashes within a distance of a particular point.

The road crash information is a point dataset and the suburb boundary dataset is a polygon dataset.

### Some background...

Basically you can think of an <strong>index</strong> in Elasticsearch as a database. Indexes contain <strong>documents</strong> and a document is of a given  <strong>type</strong>. For example we might have an index called 'suburbs' and a type called 'suburb'. The index would contain documents which define suburbs and conform to the type 'suburb'.

In Elasticsearch each index has a <strong>mapping</strong> which is ike a schema definition for all the types within the index.

There's a whole lot more information [here](http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/index.html).

Elasticsearch supports two spatial types <strong>geo point</strong> and <strong>geo shape</strong>. Elasticsearch accepts GeoJSON as it's input geometry format. Therefore we need to translate our source data into GeoJSON so we can insert our data into an index. You can think of each record within our source datasets as a document which we'll insert into an Elasticsearch index.

Elasticsearch will automatically create a mapping for a document type when a new document type is indexed. When creating the mapping, Elasticsearch infers the field data types from the document. For example if we have a field called 'Name' in our suburb dataset and it contains the suburb name 'Melbourne' then Elasticsearch will infer that the field type for the Name field is 'string'. Unfortunately Elasticsearch does not automatically infer the spatial types. In this exercise we're going to do the following:

1. Create the index
2. Insert a single document and get Elasticsearch to automatically create the mapping
3. Retrieve the mapping and modify the field type for the geometry
4. Delete and recreate the index
5. Insert the modified mapping
6. Index our data.

Lets get started and create our empty index ready for our suburb data.
```bash
$ curl -XPUT 'http://localhost:9200/suburbs/'
```




