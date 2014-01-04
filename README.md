Elasticsearch - Spatial Tutorial
===================

## Introduction

Search has been typically poorly implemented in GIS systems. Many implementations provide interfaces to make structured queries over GIS data, but (I hope you agree) this approach has some serious limitations.

In my experience many GIS solutions do a great deal of things, some of these things they do very well and some things they do very poorly. I would hope they do the GIS bits well. 

When designing a solution I rarely source all components from the same source. Search is a good example of this. A solution viewed by the end user is simply a facade over many moving parts, and each part should be selected for its ability to fulfill its respective responsibilities.

## Requirements 

To run this tutorial you'll need to install [virtulbox](https://www.virtualbox.org/) and [vagrant](http://www.vagrantup.com/).

I also recommend using the [Sense](https://chrome.google.com/webstore/detail/sense/doinijnbnggojdlcjifpdckfokbbfpbo?hl=en) extension for Chrome which provides a JSON aware interface to Elasticsearch.

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

