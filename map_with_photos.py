# -*- coding: utf-8 -*-

# Create a single .html file that shows photos and recorded gps tracks on hybrid google maps.
#
# Usage: python map_with_photos.py `find . -iname '*.jpg'` `find . -iname '*.gpx'`
# This creates the file 'map.html' which shows photos on a google maps.
# map.html have a relative path to the photos, so moving it breaks the photos.
#
# Opening map.html requires internet to access google maps.
# js dependencies are bundled into map.html.
#
# leaflet https://leafletjs.com/
# leaflet plugin marker cluster https://github.com/Leaflet/Leaflet.markercluster
# leaflet plugin photo https://github.com/turban/Leaflet.Photo
# leaflet plugin gpx https://github.com/mpetazzoni/leaflet-gpx
#
# gpx have changed to use inline marker icons and extra code to show
# number of points

import string
import sys
import PIL.Image

template = """
<!DOCTYPE html>
<html>
  <head>
    <title>Title</title>

    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <!-- <link rel="stylesheet" href="https://unpkg.com/leaflet@1.5.1/dist/leaflet.css" integrity="sha512-xwE/Az9zrjBIphAcBb3F6JVqxf46+CDLwfLMHloNu6KEQCAWi6HcDUbeOfBIptF7tcCzusKFjFw2yuvEpDL9wQ==" crossorigin=""/> -->
    <!-- <script src="https://unpkg.com/leaflet@1.5.1/dist/leaflet.js" integrity="sha512-GffPMF3RvMeYyc1LWMHtK8EbPv0iNZ8/oTtHPx9/cc2ILxQ+u905qIwdpULaqDkyBKgOaB57QTMg7ztg8Jm2Og==" crossorigin=""></script> -->
    <!-- <link rel="stylesheet" href="https://combinatronics.com/Leaflet/Leaflet.markercluster/v1.4.0/dist/MarkerCluster.Default.css"/> -->
    <!-- <script src="https://combinatronics.com/Leaflet/Leaflet.markercluster/v1.4.0/dist/leaflet.markercluster.js"></script> -->
    <!-- <link rel="stylesheet" href="https://combinatronics.com/turban/Leaflet.Photo/gh-pages/Leaflet.Photo.css"/> -->
    <!-- <script src="https://combinatronics.com/turban/Leaflet.Photo/gh-pages/Leaflet.Photo.js"></script> -->
    <!-- <script src="https://combinatronics.com/mpetazzoni/leaflet-gpx/master/gpx.js"></script> -->
    <!-- <script src="https://cdnjs.cloudflare.com/ajax/libs/dygraph/2.1.0/dygraph.min.js"></script> -->
    <!-- <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/dygraph/2.1.0/dygraph.min.css" /> -->
    <style>
/* required styles */

.leaflet-pane,
.leaflet-tile,
.leaflet-marker-icon,
.leaflet-marker-shadow,
.leaflet-tile-container,
.leaflet-pane > svg,
.leaflet-pane > canvas,
.leaflet-zoom-box,
.leaflet-image-layer,
.leaflet-layer {
	position: absolute;
	left: 0;
	top: 0;
	}
.leaflet-container {
	overflow: hidden;
	}
.leaflet-tile,
.leaflet-marker-icon,
.leaflet-marker-shadow {
	-webkit-user-select: none;
	   -moz-user-select: none;
	        user-select: none;
	  -webkit-user-drag: none;
	}
/* Prevents IE11 from highlighting tiles in blue */
.leaflet-tile::selection {
	background: transparent;
}
/* Safari renders non-retina tile on retina better with this, but Chrome is worse */
.leaflet-safari .leaflet-tile {
	image-rendering: -webkit-optimize-contrast;
	}
/* hack that prevents hw layers "stretching" when loading new tiles */
.leaflet-safari .leaflet-tile-container {
	width: 1600px;
	height: 1600px;
	-webkit-transform-origin: 0 0;
	}
.leaflet-marker-icon,
.leaflet-marker-shadow {
	display: block;
	}
/* .leaflet-container svg: reset svg max-width decleration shipped in Joomla! (joomla.org) 3.x */
/* .leaflet-container img: map is broken in FF if you have max-width: 100% on tiles */
.leaflet-container .leaflet-overlay-pane svg,
.leaflet-container .leaflet-marker-pane img,
.leaflet-container .leaflet-shadow-pane img,
.leaflet-container .leaflet-tile-pane img,
.leaflet-container img.leaflet-image-layer,
.leaflet-container .leaflet-tile {
	max-width: none !important;
	max-height: none !important;
	}

.leaflet-container.leaflet-touch-zoom {
	-ms-touch-action: pan-x pan-y;
	touch-action: pan-x pan-y;
	}
.leaflet-container.leaflet-touch-drag {
	-ms-touch-action: pinch-zoom;
	/* Fallback for FF which doesn't support pinch-zoom */
	touch-action: none;
	touch-action: pinch-zoom;
}
.leaflet-container.leaflet-touch-drag.leaflet-touch-zoom {
	-ms-touch-action: none;
	touch-action: none;
}
.leaflet-container {
	-webkit-tap-highlight-color: transparent;
}
.leaflet-container a {
	-webkit-tap-highlight-color: rgba(51, 181, 229, 0.4);
}
.leaflet-tile {
	filter: inherit;
	visibility: hidden;
	}
.leaflet-tile-loaded {
	visibility: inherit;
	}
.leaflet-zoom-box {
	width: 0;
	height: 0;
	-moz-box-sizing: border-box;
	     box-sizing: border-box;
	z-index: 800;
	}
/* workaround for https://bugzilla.mozilla.org/show_bug.cgi?id=888319 */
.leaflet-overlay-pane svg {
	-moz-user-select: none;
	}

.leaflet-pane         { z-index: 400; }

.leaflet-tile-pane    { z-index: 200; }
.leaflet-overlay-pane { z-index: 400; }
.leaflet-shadow-pane  { z-index: 500; }
.leaflet-marker-pane  { z-index: 600; }
.leaflet-tooltip-pane   { z-index: 650; }
.leaflet-popup-pane   { z-index: 700; }

.leaflet-map-pane canvas { z-index: 100; }
.leaflet-map-pane svg    { z-index: 200; }

.leaflet-vml-shape {
	width: 1px;
	height: 1px;
	}
.lvml {
	behavior: url(#default#VML);
	display: inline-block;
	position: absolute;
	}


/* control positioning */

.leaflet-control {
	position: relative;
	z-index: 800;
	pointer-events: visiblePainted; /* IE 9-10 doesn't have auto */
	pointer-events: auto;
	}
.leaflet-top,
.leaflet-bottom {
	position: absolute;
	z-index: 1000;
	pointer-events: none;
	}
.leaflet-top {
	top: 0;
	}
.leaflet-right {
	right: 0;
	}
.leaflet-bottom {
	bottom: 0;
	}
.leaflet-left {
	left: 0;
	}
.leaflet-control {
	float: left;
	clear: both;
	}
.leaflet-right .leaflet-control {
	float: right;
	}
.leaflet-top .leaflet-control {
	margin-top: 10px;
	}
.leaflet-bottom .leaflet-control {
	margin-bottom: 10px;
	}
.leaflet-left .leaflet-control {
	margin-left: 10px;
	}
.leaflet-right .leaflet-control {
	margin-right: 10px;
	}


/* zoom and fade animations */

.leaflet-fade-anim .leaflet-tile {
	will-change: opacity;
	}
.leaflet-fade-anim .leaflet-popup {
	opacity: 0;
	-webkit-transition: opacity 0.2s linear;
	   -moz-transition: opacity 0.2s linear;
	        transition: opacity 0.2s linear;
	}
.leaflet-fade-anim .leaflet-map-pane .leaflet-popup {
	opacity: 1;
	}
.leaflet-zoom-animated {
	-webkit-transform-origin: 0 0;
	    -ms-transform-origin: 0 0;
	        transform-origin: 0 0;
	}
.leaflet-zoom-anim .leaflet-zoom-animated {
	will-change: transform;
	}
.leaflet-zoom-anim .leaflet-zoom-animated {
	-webkit-transition: -webkit-transform 0.25s cubic-bezier(0,0,0.25,1);
	   -moz-transition:    -moz-transform 0.25s cubic-bezier(0,0,0.25,1);
	        transition:         transform 0.25s cubic-bezier(0,0,0.25,1);
	}
.leaflet-zoom-anim .leaflet-tile,
.leaflet-pan-anim .leaflet-tile {
	-webkit-transition: none;
	   -moz-transition: none;
	        transition: none;
	}

.leaflet-zoom-anim .leaflet-zoom-hide {
	visibility: hidden;
	}


/* cursors */

.leaflet-interactive {
	cursor: pointer;
	}
.leaflet-grab {
	cursor: -webkit-grab;
	cursor:    -moz-grab;
	cursor:         grab;
	}
.leaflet-crosshair,
.leaflet-crosshair .leaflet-interactive {
	cursor: crosshair;
	}
.leaflet-popup-pane,
.leaflet-control {
	cursor: auto;
	}
.leaflet-dragging .leaflet-grab,
.leaflet-dragging .leaflet-grab .leaflet-interactive,
.leaflet-dragging .leaflet-marker-draggable {
	cursor: move;
	cursor: -webkit-grabbing;
	cursor:    -moz-grabbing;
	cursor:         grabbing;
	}

/* marker & overlays interactivity */
.leaflet-marker-icon,
.leaflet-marker-shadow,
.leaflet-image-layer,
.leaflet-pane > svg path,
.leaflet-tile-container {
	pointer-events: none;
	}

.leaflet-marker-icon.leaflet-interactive,
.leaflet-image-layer.leaflet-interactive,
.leaflet-pane > svg path.leaflet-interactive,
svg.leaflet-image-layer.leaflet-interactive path {
	pointer-events: visiblePainted; /* IE 9-10 doesn't have auto */
	pointer-events: auto;
	}

/* visual tweaks */

.leaflet-container {
	background: #ddd;
	outline: 0;
	}
.leaflet-container a {
	color: #0078A8;
	}
.leaflet-container a.leaflet-active {
	outline: 2px solid orange;
	}
.leaflet-zoom-box {
	border: 2px dotted #38f;
	background: rgba(255,255,255,0.5);
	}


/* general typography */
.leaflet-container {
	font: 12px/1.5 "Helvetica Neue", Arial, Helvetica, sans-serif;
	}


/* general toolbar styles */

.leaflet-bar {
	box-shadow: 0 1px 5px rgba(0,0,0,0.65);
	border-radius: 4px;
	}
.leaflet-bar a,
.leaflet-bar a:hover {
	background-color: #fff;
	border-bottom: 1px solid #ccc;
	width: 26px;
	height: 26px;
	line-height: 26px;
	display: block;
	text-align: center;
	text-decoration: none;
	color: black;
	}
.leaflet-bar a,
.leaflet-control-layers-toggle {
	background-position: 50% 50%;
	background-repeat: no-repeat;
	display: block;
	}
.leaflet-bar a:hover {
	background-color: #f4f4f4;
	}
.leaflet-bar a:first-child {
	border-top-left-radius: 4px;
	border-top-right-radius: 4px;
	}
.leaflet-bar a:last-child {
	border-bottom-left-radius: 4px;
	border-bottom-right-radius: 4px;
	border-bottom: none;
	}
.leaflet-bar a.leaflet-disabled {
	cursor: default;
	background-color: #f4f4f4;
	color: #bbb;
	}

.leaflet-touch .leaflet-bar a {
	width: 30px;
	height: 30px;
	line-height: 30px;
	}
.leaflet-touch .leaflet-bar a:first-child {
	border-top-left-radius: 2px;
	border-top-right-radius: 2px;
	}
.leaflet-touch .leaflet-bar a:last-child {
	border-bottom-left-radius: 2px;
	border-bottom-right-radius: 2px;
	}

/* zoom control */

.leaflet-control-zoom-in,
.leaflet-control-zoom-out {
	font: bold 18px 'Lucida Console', Monaco, monospace;
	text-indent: 1px;
	}

.leaflet-touch .leaflet-control-zoom-in, .leaflet-touch .leaflet-control-zoom-out  {
	font-size: 22px;
	}


/* layers control */

.leaflet-control-layers {
	box-shadow: 0 1px 5px rgba(0,0,0,0.4);
	background: #fff;
	border-radius: 5px;
	}
.leaflet-control-layers-toggle {
	background-image: url(images/layers.png);
	width: 36px;
	height: 36px;
	}
.leaflet-retina .leaflet-control-layers-toggle {
	background-image: url(images/layers-2x.png);
	background-size: 26px 26px;
	}
.leaflet-touch .leaflet-control-layers-toggle {
	width: 44px;
	height: 44px;
	}
.leaflet-control-layers .leaflet-control-layers-list,
.leaflet-control-layers-expanded .leaflet-control-layers-toggle {
	display: none;
	}
.leaflet-control-layers-expanded .leaflet-control-layers-list {
	display: block;
	position: relative;
	}
.leaflet-control-layers-expanded {
	padding: 6px 10px 6px 6px;
	color: #333;
	background: #fff;
	}
.leaflet-control-layers-scrollbar {
	overflow-y: scroll;
	overflow-x: hidden;
	padding-right: 5px;
	}
.leaflet-control-layers-selector {
	margin-top: 2px;
	position: relative;
	top: 1px;
	}
.leaflet-control-layers label {
	display: block;
	}
.leaflet-control-layers-separator {
	height: 0;
	border-top: 1px solid #ddd;
	margin: 5px -10px 5px -6px;
	}

/* Default icon URLs */
.leaflet-default-icon-path {
	background-image: url(images/marker-icon.png);
	}


/* attribution and scale controls */

.leaflet-container .leaflet-control-attribution {
	background: #fff;
	background: rgba(255, 255, 255, 0.7);
	margin: 0;
	}
.leaflet-control-attribution,
.leaflet-control-scale-line {
	padding: 0 5px;
	color: #333;
	}
.leaflet-control-attribution a {
	text-decoration: none;
	}
.leaflet-control-attribution a:hover {
	text-decoration: underline;
	}
.leaflet-container .leaflet-control-attribution,
.leaflet-container .leaflet-control-scale {
	font-size: 11px;
	}
.leaflet-left .leaflet-control-scale {
	margin-left: 5px;
	}
.leaflet-bottom .leaflet-control-scale {
	margin-bottom: 5px;
	}
.leaflet-control-scale-line {
	border: 2px solid #777;
	border-top: none;
	line-height: 1.1;
	padding: 2px 5px 1px;
	font-size: 11px;
	white-space: nowrap;
	overflow: hidden;
	-moz-box-sizing: border-box;
	     box-sizing: border-box;

	background: #fff;
	background: rgba(255, 255, 255, 0.5);
	}
.leaflet-control-scale-line:not(:first-child) {
	border-top: 2px solid #777;
	border-bottom: none;
	margin-top: -2px;
	}
.leaflet-control-scale-line:not(:first-child):not(:last-child) {
	border-bottom: 2px solid #777;
	}

.leaflet-touch .leaflet-control-attribution,
.leaflet-touch .leaflet-control-layers,
.leaflet-touch .leaflet-bar {
	box-shadow: none;
	}
.leaflet-touch .leaflet-control-layers,
.leaflet-touch .leaflet-bar {
	border: 2px solid rgba(0,0,0,0.2);
	background-clip: padding-box;
	}


/* popup */

.leaflet-popup {
	position: absolute;
	text-align: center;
	margin-bottom: 20px;
	}
.leaflet-popup-content-wrapper {
	padding: 1px;
	text-align: left;
	border-radius: 12px;
	}
.leaflet-popup-content {
	margin: 13px 19px;
	line-height: 1.4;
	}
.leaflet-popup-content p {
	margin: 18px 0;
	}
.leaflet-popup-tip-container {
	width: 40px;
	height: 20px;
	position: absolute;
	left: 50%;
	margin-left: -20px;
	overflow: hidden;
	pointer-events: none;
	}
.leaflet-popup-tip {
	width: 17px;
	height: 17px;
	padding: 1px;

	margin: -10px auto 0;

	-webkit-transform: rotate(45deg);
	   -moz-transform: rotate(45deg);
	    -ms-transform: rotate(45deg);
	        transform: rotate(45deg);
	}
.leaflet-popup-content-wrapper,
.leaflet-popup-tip {
	background: white;
	color: #333;
	box-shadow: 0 3px 14px rgba(0,0,0,0.4);
	}
.leaflet-container a.leaflet-popup-close-button {
	position: absolute;
	top: 0;
	right: 0;
	padding: 4px 4px 0 0;
	border: none;
	text-align: center;
	width: 18px;
	height: 14px;
	font: 16px/14px Tahoma, Verdana, sans-serif;
	color: #c3c3c3;
	text-decoration: none;
	font-weight: bold;
	background: transparent;
	}
.leaflet-container a.leaflet-popup-close-button:hover {
	color: #999;
	}
.leaflet-popup-scrolled {
	overflow: auto;
	border-bottom: 1px solid #ddd;
	border-top: 1px solid #ddd;
	}

.leaflet-oldie .leaflet-popup-content-wrapper {
	zoom: 1;
	}
.leaflet-oldie .leaflet-popup-tip {
	width: 24px;
	margin: 0 auto;

	-ms-filter: "progid:DXImageTransform.Microsoft.Matrix(M11=0.70710678, M12=0.70710678, M21=-0.70710678, M22=0.70710678)";
	filter: progid:DXImageTransform.Microsoft.Matrix(M11=0.70710678, M12=0.70710678, M21=-0.70710678, M22=0.70710678);
	}
.leaflet-oldie .leaflet-popup-tip-container {
	margin-top: -1px;
	}

.leaflet-oldie .leaflet-control-zoom,
.leaflet-oldie .leaflet-control-layers,
.leaflet-oldie .leaflet-popup-content-wrapper,
.leaflet-oldie .leaflet-popup-tip {
	border: 1px solid #999;
	}


/* div icon */

.leaflet-div-icon {
	background: #fff;
	border: 1px solid #666;
	}


/* Tooltip */
/* Base styles for the element that has a tooltip */
.leaflet-tooltip {
	position: absolute;
	padding: 6px;
	background-color: #fff;
	border: 1px solid #fff;
	border-radius: 3px;
	color: #222;
	white-space: nowrap;
	-webkit-user-select: none;
	-moz-user-select: none;
	-ms-user-select: none;
	user-select: none;
	pointer-events: none;
	box-shadow: 0 1px 3px rgba(0,0,0,0.4);
	}
.leaflet-tooltip.leaflet-clickable {
	cursor: pointer;
	pointer-events: auto;
	}
.leaflet-tooltip-top:before,
.leaflet-tooltip-bottom:before,
.leaflet-tooltip-left:before,
.leaflet-tooltip-right:before {
	position: absolute;
	pointer-events: none;
	border: 6px solid transparent;
	background: transparent;
	content: "";
	}

/* Directions */

.leaflet-tooltip-bottom {
	margin-top: 6px;
}
.leaflet-tooltip-top {
	margin-top: -6px;
}
.leaflet-tooltip-bottom:before,
.leaflet-tooltip-top:before {
	left: 50%;
	margin-left: -6px;
	}
.leaflet-tooltip-top:before {
	bottom: 0;
	margin-bottom: -12px;
	border-top-color: #fff;
	}
.leaflet-tooltip-bottom:before {
	top: 0;
	margin-top: -12px;
	margin-left: -6px;
	border-bottom-color: #fff;
	}
.leaflet-tooltip-left {
	margin-left: -6px;
}
.leaflet-tooltip-right {
	margin-left: 6px;
}
.leaflet-tooltip-left:before,
.leaflet-tooltip-right:before {
	top: 50%;
	margin-top: -6px;
	}
.leaflet-tooltip-left:before {
	right: 0;
	margin-right: -12px;
	border-left-color: #fff;
	}
.leaflet-tooltip-right:before {
	left: 0;
	margin-left: -12px;
	border-right-color: #fff;
	}



.marker-cluster-small {
	background-color: rgba(181, 226, 140, 0.6);
	}
.marker-cluster-small div {
	background-color: rgba(110, 204, 57, 0.6);
	}

.marker-cluster-medium {
	background-color: rgba(241, 211, 87, 0.6);
	}
.marker-cluster-medium div {
	background-color: rgba(240, 194, 12, 0.6);
	}

.marker-cluster-large {
	background-color: rgba(253, 156, 115, 0.6);
	}
.marker-cluster-large div {
	background-color: rgba(241, 128, 23, 0.6);
	}

	/* IE 6-8 fallback colors */
.leaflet-oldie .marker-cluster-small {
	background-color: rgb(181, 226, 140);
	}
.leaflet-oldie .marker-cluster-small div {
	background-color: rgb(110, 204, 57);
	}

.leaflet-oldie .marker-cluster-medium {
	background-color: rgb(241, 211, 87);
	}
.leaflet-oldie .marker-cluster-medium div {
	background-color: rgb(240, 194, 12);
	}

.leaflet-oldie .marker-cluster-large {
	background-color: rgb(253, 156, 115);
	}
.leaflet-oldie .marker-cluster-large div {
	background-color: rgb(241, 128, 23);
}

.marker-cluster {
	background-clip: padding-box;
	border-radius: 20px;
	}
.marker-cluster div {
	width: 30px;
	height: 30px;
	margin-left: 5px;
	margin-top: 5px;

	text-align: center;
	border-radius: 15px;
	font: 12px "Helvetica Neue", Arial, Helvetica, sans-serif;
	}
.marker-cluster span {
	line-height: 30px;
}




.leaflet-marker-photo { 
	border: 2px solid #fff; 
	box-shadow: 3px 3px 10px #888; 
}	

.leaflet-marker-photo div { 
    width: 100%;  
    height: 100%;
    background-size: cover;    
    background-position: center center;
    background-repeat: no-repeat;
}	

.leaflet-marker-photo b {
	position: absolute;
	top: -7px;
	right: -11px;
	color: #555;
	background-color: #fff;
	border-radius: 8px;
	height: 12px;
	min-width: 12px;
	line-height: 12px;
	text-align: center;
	padding: 3px;
	box-shadow: 0 3px 14px rgba(0,0,0,0.4);
}


.dygraph-annotation,.dygraph-legend{
    overflow:hidden
}.dygraph-legend{
    position:absolute;
    font-size:14px;
    z-index:10;
    width:250px;
    background:#fff;
    line-height:normal;
    text-align:left
}.dygraph-legend-dash,.dygraph-legend-line{
    display:inline-block;
    position:relative;
    bottom:.5ex;
    height:1px;
    border-bottom-width:2px;
    border-bottom-style:solid
}.dygraph-legend-line{
    padding-left:1em
}.dygraph-annotation,.dygraph-roller{
    position:absolute;
    z-index:10
}.dygraph-default-annotation{
    border:1px solid #000;
    background-color:#fff;
    text-align:center
}.dygraph-axis-label{
    z-index:10;
    line-height:normal;
    overflow:hidden;
    color:#000
}.dygraph-title{
    font-weight:700;
    z-index:10;
    text-align:center
}.dygraph-xlabel{
    text-align:center
}.dygraph-label-rotate-left{
    text-align:center;
    transform:rotate(90deg);
    -webkit-transform:rotate(90deg);
    -moz-transform:rotate(90deg);
    -o-transform:rotate(90deg);
    -ms-transform:rotate(90deg)
}.dygraph-label-rotate-right{
    text-align:center;
    transform:rotate(-90deg);
    -webkit-transform:rotate(-90deg);
    -moz-transform:rotate(-90deg);
    -o-transform:rotate(-90deg);
    -ms-transform:rotate(-90deg)
}


      body {
        padding: 0;
        margin: 0;
      }
      html, body, #mapid {
        height: 100%;
        width: 100%;
      }
    </style>
    <script>
/* @preserve
 * Leaflet 1.5.1+build.2e3e0ff, a JS library for interactive maps. http://leafletjs.com
 * (c) 2010-2018 Vladimir Agafonkin, (c) 2010-2011 CloudMade
 */
! function(t, i) {
  "object" == typeof exports && "undefined" != typeof module ? i(exports) : "function" == typeof define && define.amd ? define(["exports"], i) : i(t.L = {})
}(this, function(t) {
  "use strict";
  var i = Object.freeze;

  function h(t) {
    var i, e, n, o;
    for (e = 1, n = arguments.length; e < n; e++)
      for (i in o = arguments[e]) t[i] = o[i];
    return t
  }
  Object.freeze = function(t) {
    return t
  };
  var s = Object.create || function(t) {
    return e.prototype = t, new e
  };

  function e() {}

  function a(t, i) {
    var e = Array.prototype.slice;
    if (t.bind) return t.bind.apply(t, e.call(arguments, 1));
    var n = e.call(arguments, 2);
    return function() {
      return t.apply(i, n.length ? n.concat(e.call(arguments)) : arguments)
    }
  }
  var n = 0;

  function u(t) {
    return t._leaflet_id = t._leaflet_id || ++n, t._leaflet_id
  }

  function o(t, i, e) {
    var n, o, s, r;
    return r = function() {
      n = !1, o && (s.apply(e, o), o = !1)
    }, s = function() {
      n ? o = arguments : (t.apply(e, arguments), setTimeout(r, i), n = !0)
    }
  }

  function r(t, i, e) {
    var n = i[1],
      o = i[0],
      s = n - o;
    return t === n && e ? t : ((t - o) % s + s) % s + o
  }

  function l() {
    return !1
  }

  function c(t, i) {
    return i = void 0 === i ? 6 : i, +(Math.round(t + "e+" + i) + "e-" + i)
  }

  function _(t) {
    return t.trim ? t.trim() : t.replace(/^\s+|\s+$/g, "")
  }

  function d(t) {
    return _(t).split(/\s+/)
  }

  function p(t, i) {
    for (var e in t.hasOwnProperty("options") || (t.options = t.options ? s(t.options) : {}), i) t.options[e] = i[e];
    return t.options
  }

  function m(t, i, e) {
    var n = [];
    for (var o in t) n.push(encodeURIComponent(e ? o.toUpperCase() : o) + "=" + encodeURIComponent(t[o]));
    return (i && -1 !== i.indexOf("?") ? "&" : "?") + n.join("&")
  }
  var f = /\{ *([\w_-]+) *\}/g;

  function g(t, n) {
    return t.replace(f, function(t, i) {
      var e = n[i];
      if (void 0 === e) throw new Error("No value provided for variable " + t);
      return "function" == typeof e && (e = e(n)), e
    })
  }
  var v = Array.isArray || function(t) {
    return "[object Array]" === Object.prototype.toString.call(t)
  };

  function y(t, i) {
    for (var e = 0; e < t.length; e++)
      if (t[e] === i) return e;
    return -1
  }
  var x = "data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs=";

  function w(t) {
    return window["webkit" + t] || window["moz" + t] || window["ms" + t]
  }
  var P = 0;

  function b(t) {
    var i = +new Date,
      e = Math.max(0, 16 - (i - P));
    return P = i + e, window.setTimeout(t, e)
  }
  var T = window.requestAnimationFrame || w("RequestAnimationFrame") || b,
    z = window.cancelAnimationFrame || w("CancelAnimationFrame") || w("CancelRequestAnimationFrame") || function(t) {
      window.clearTimeout(t)
    };

  function M(t, i, e) {
    if (!e || T !== b) return T.call(window, a(t, i));
    t.call(i)
  }

  function C(t) {
    t && z.call(window, t)
  }
  var S = (Object.freeze || Object)({
    freeze: i,
    extend: h,
    create: s,
    bind: a,
    lastId: n,
    stamp: u,
    throttle: o,
    wrapNum: r,
    falseFn: l,
    formatNum: c,
    trim: _,
    splitWords: d,
    setOptions: p,
    getParamString: m,
    template: g,
    isArray: v,
    indexOf: y,
    emptyImageUrl: x,
    requestFn: T,
    cancelFn: z,
    requestAnimFrame: M,
    cancelAnimFrame: C
  });

  function Z() {}
  Z.extend = function(t) {
    function i() {
      this.initialize && this.initialize.apply(this, arguments), this.callInitHooks()
    }
    var e = i.__super__ = this.prototype,
      n = s(e);
    for (var o in (n.constructor = i).prototype = n, this) this.hasOwnProperty(o) && "prototype" !== o && "__super__" !== o && (i[o] = this[o]);
    return t.statics && (h(i, t.statics), delete t.statics), t.includes && (function(t) {
      if ("undefined" == typeof L || !L || !L.Mixin) return;
      t = v(t) ? t : [t];
      for (var i = 0; i < t.length; i++) t[i] === L.Mixin.Events && console.warn("Deprecated include of L.Mixin.Events: this property will be removed in future releases, please inherit from L.Evented instead.", (new Error).stack)
    }(t.includes), h.apply(null, [n].concat(t.includes)), delete t.includes), n.options && (t.options = h(s(n.options), t.options)), h(n, t), n._initHooks = [], n.callInitHooks = function() {
      if (!this._initHooksCalled) {
        e.callInitHooks && e.callInitHooks.call(this), this._initHooksCalled = !0;
        for (var t = 0, i = n._initHooks.length; t < i; t++) n._initHooks[t].call(this)
      }
    }, i
  }, Z.include = function(t) {
    return h(this.prototype, t), this
  }, Z.mergeOptions = function(t) {
    return h(this.prototype.options, t), this
  }, Z.addInitHook = function(t) {
    var i = Array.prototype.slice.call(arguments, 1),
      e = "function" == typeof t ? t : function() {
        this[t].apply(this, i)
      };
    return this.prototype._initHooks = this.prototype._initHooks || [], this.prototype._initHooks.push(e), this
  };
  var E = {
    on: function(t, i, e) {
      if ("object" == typeof t)
        for (var n in t) this._on(n, t[n], i);
      else
        for (var o = 0, s = (t = d(t)).length; o < s; o++) this._on(t[o], i, e);
      return this
    },
    off: function(t, i, e) {
      if (t)
        if ("object" == typeof t)
          for (var n in t) this._off(n, t[n], i);
        else
          for (var o = 0, s = (t = d(t)).length; o < s; o++) this._off(t[o], i, e);
      else delete this._events;
      return this
    },
    _on: function(t, i, e) {
      this._events = this._events || {};
      var n = this._events[t];
      n || (n = [], this._events[t] = n), e === this && (e = void 0);
      for (var o = {
          fn: i,
          ctx: e
        }, s = n, r = 0, a = s.length; r < a; r++)
        if (s[r].fn === i && s[r].ctx === e) return;
      s.push(o)
    },
    _off: function(t, i, e) {
      var n, o, s;
      if (this._events && (n = this._events[t]))
        if (i) {
          if (e === this && (e = void 0), n)
            for (o = 0, s = n.length; o < s; o++) {
              var r = n[o];
              if (r.ctx === e && r.fn === i) return r.fn = l, this._firingCount && (this._events[t] = n = n.slice()), void n.splice(o, 1)
            }
        } else {
          for (o = 0, s = n.length; o < s; o++) n[o].fn = l;
          delete this._events[t]
        }
    },
    fire: function(t, i, e) {
      if (!this.listens(t, e)) return this;
      var n = h({}, i, {
        type: t,
        target: this,
        sourceTarget: i && i.sourceTarget || this
      });
      if (this._events) {
        var o = this._events[t];
        if (o) {
          this._firingCount = this._firingCount + 1 || 1;
          for (var s = 0, r = o.length; s < r; s++) {
            var a = o[s];
            a.fn.call(a.ctx || this, n)
          }
          this._firingCount--
        }
      }
      return e && this._propagateEvent(n), this
    },
    listens: function(t, i) {
      var e = this._events && this._events[t];
      if (e && e.length) return !0;
      if (i)
        for (var n in this._eventParents)
          if (this._eventParents[n].listens(t, i)) return !0;
      return !1
    },
    once: function(t, i, e) {
      if ("object" == typeof t) {
        for (var n in t) this.once(n, t[n], i);
        return this
      }
      var o = a(function() {
        this.off(t, i, e).off(t, o, e)
      }, this);
      return this.on(t, i, e).on(t, o, e)
    },
    addEventParent: function(t) {
      return this._eventParents = this._eventParents || {}, this._eventParents[u(t)] = t, this
    },
    removeEventParent: function(t) {
      return this._eventParents && delete this._eventParents[u(t)], this
    },
    _propagateEvent: function(t) {
      for (var i in this._eventParents) this._eventParents[i].fire(t.type, h({
        layer: t.target,
        propagatedFrom: t.target
      }, t), !0)
    }
  };
  E.addEventListener = E.on, E.removeEventListener = E.clearAllEventListeners = E.off, E.addOneTimeEventListener = E.once, E.fireEvent = E.fire, E.hasEventListeners = E.listens;
  var k = Z.extend(E);

  function B(t, i, e) {
    this.x = e ? Math.round(t) : t, this.y = e ? Math.round(i) : i
  }
  var A = Math.trunc || function(t) {
    return 0 < t ? Math.floor(t) : Math.ceil(t)
  };

  function I(t, i, e) {
    return t instanceof B ? t : v(t) ? new B(t[0], t[1]) : null == t ? t : "object" == typeof t && "x" in t && "y" in t ? new B(t.x, t.y) : new B(t, i, e)
  }

  function O(t, i) {
    if (t)
      for (var e = i ? [t, i] : t, n = 0, o = e.length; n < o; n++) this.extend(e[n])
  }

  function R(t, i) {
    return !t || t instanceof O ? t : new O(t, i)
  }

  function N(t, i) {
    if (t)
      for (var e = i ? [t, i] : t, n = 0, o = e.length; n < o; n++) this.extend(e[n])
  }

  function D(t, i) {
    return t instanceof N ? t : new N(t, i)
  }

  function j(t, i, e) {
    if (isNaN(t) || isNaN(i)) throw new Error("Invalid LatLng object: (" + t + ", " + i + ")");
    this.lat = +t, this.lng = +i, void 0 !== e && (this.alt = +e)
  }

  function W(t, i, e) {
    return t instanceof j ? t : v(t) && "object" != typeof t[0] ? 3 === t.length ? new j(t[0], t[1], t[2]) : 2 === t.length ? new j(t[0], t[1]) : null : null == t ? t : "object" == typeof t && "lat" in t ? new j(t.lat, "lng" in t ? t.lng : t.lon, t.alt) : void 0 === i ? null : new j(t, i, e)
  }
  B.prototype = {
    clone: function() {
      return new B(this.x, this.y)
    },
    add: function(t) {
      return this.clone()._add(I(t))
    },
    _add: function(t) {
      return this.x += t.x, this.y += t.y, this
    },
    subtract: function(t) {
      return this.clone()._subtract(I(t))
    },
    _subtract: function(t) {
      return this.x -= t.x, this.y -= t.y, this
    },
    divideBy: function(t) {
      return this.clone()._divideBy(t)
    },
    _divideBy: function(t) {
      return this.x /= t, this.y /= t, this
    },
    multiplyBy: function(t) {
      return this.clone()._multiplyBy(t)
    },
    _multiplyBy: function(t) {
      return this.x *= t, this.y *= t, this
    },
    scaleBy: function(t) {
      return new B(this.x * t.x, this.y * t.y)
    },
    unscaleBy: function(t) {
      return new B(this.x / t.x, this.y / t.y)
    },
    round: function() {
      return this.clone()._round()
    },
    _round: function() {
      return this.x = Math.round(this.x), this.y = Math.round(this.y), this
    },
    floor: function() {
      return this.clone()._floor()
    },
    _floor: function() {
      return this.x = Math.floor(this.x), this.y = Math.floor(this.y), this
    },
    ceil: function() {
      return this.clone()._ceil()
    },
    _ceil: function() {
      return this.x = Math.ceil(this.x), this.y = Math.ceil(this.y), this
    },
    trunc: function() {
      return this.clone()._trunc()
    },
    _trunc: function() {
      return this.x = A(this.x), this.y = A(this.y), this
    },
    distanceTo: function(t) {
      var i = (t = I(t)).x - this.x,
        e = t.y - this.y;
      return Math.sqrt(i * i + e * e)
    },
    equals: function(t) {
      return (t = I(t)).x === this.x && t.y === this.y
    },
    contains: function(t) {
      return t = I(t), Math.abs(t.x) <= Math.abs(this.x) && Math.abs(t.y) <= Math.abs(this.y)
    },
    toString: function() {
      return "Point(" + c(this.x) + ", " + c(this.y) + ")"
    }
  }, O.prototype = {
    extend: function(t) {
      return t = I(t), this.min || this.max ? (this.min.x = Math.min(t.x, this.min.x), this.max.x = Math.max(t.x, this.max.x), this.min.y = Math.min(t.y, this.min.y), this.max.y = Math.max(t.y, this.max.y)) : (this.min = t.clone(), this.max = t.clone()), this
    },
    getCenter: function(t) {
      return new B((this.min.x + this.max.x) / 2, (this.min.y + this.max.y) / 2, t)
    },
    getBottomLeft: function() {
      return new B(this.min.x, this.max.y)
    },
    getTopRight: function() {
      return new B(this.max.x, this.min.y)
    },
    getTopLeft: function() {
      return this.min
    },
    getBottomRight: function() {
      return this.max
    },
    getSize: function() {
      return this.max.subtract(this.min)
    },
    contains: function(t) {
      var i, e;
      return (t = "number" == typeof t[0] || t instanceof B ? I(t) : R(t)) instanceof O ? (i = t.min, e = t.max) : i = e = t, i.x >= this.min.x && e.x <= this.max.x && i.y >= this.min.y && e.y <= this.max.y
    },
    intersects: function(t) {
      t = R(t);
      var i = this.min,
        e = this.max,
        n = t.min,
        o = t.max,
        s = o.x >= i.x && n.x <= e.x,
        r = o.y >= i.y && n.y <= e.y;
      return s && r
    },
    overlaps: function(t) {
      t = R(t);
      var i = this.min,
        e = this.max,
        n = t.min,
        o = t.max,
        s = o.x > i.x && n.x < e.x,
        r = o.y > i.y && n.y < e.y;
      return s && r
    },
    isValid: function() {
      return !(!this.min || !this.max)
    }
  }, N.prototype = {
    extend: function(t) {
      var i, e, n = this._southWest,
        o = this._northEast;
      if (t instanceof j) e = i = t;
      else {
        if (!(t instanceof N)) return t ? this.extend(W(t) || D(t)) : this;
        if (i = t._southWest, e = t._northEast, !i || !e) return this
      }
      return n || o ? (n.lat = Math.min(i.lat, n.lat), n.lng = Math.min(i.lng, n.lng), o.lat = Math.max(e.lat, o.lat), o.lng = Math.max(e.lng, o.lng)) : (this._southWest = new j(i.lat, i.lng), this._northEast = new j(e.lat, e.lng)), this
    },
    pad: function(t) {
      var i = this._southWest,
        e = this._northEast,
        n = Math.abs(i.lat - e.lat) * t,
        o = Math.abs(i.lng - e.lng) * t;
      return new N(new j(i.lat - n, i.lng - o), new j(e.lat + n, e.lng + o))
    },
    getCenter: function() {
      return new j((this._southWest.lat + this._northEast.lat) / 2, (this._southWest.lng + this._northEast.lng) / 2)
    },
    getSouthWest: function() {
      return this._southWest
    },
    getNorthEast: function() {
      return this._northEast
    },
    getNorthWest: function() {
      return new j(this.getNorth(), this.getWest())
    },
    getSouthEast: function() {
      return new j(this.getSouth(), this.getEast())
    },
    getWest: function() {
      return this._southWest.lng
    },
    getSouth: function() {
      return this._southWest.lat
    },
    getEast: function() {
      return this._northEast.lng
    },
    getNorth: function() {
      return this._northEast.lat
    },
    contains: function(t) {
      t = "number" == typeof t[0] || t instanceof j || "lat" in t ? W(t) : D(t);
      var i, e, n = this._southWest,
        o = this._northEast;
      return t instanceof N ? (i = t.getSouthWest(), e = t.getNorthEast()) : i = e = t, i.lat >= n.lat && e.lat <= o.lat && i.lng >= n.lng && e.lng <= o.lng
    },
    intersects: function(t) {
      t = D(t);
      var i = this._southWest,
        e = this._northEast,
        n = t.getSouthWest(),
        o = t.getNorthEast(),
        s = o.lat >= i.lat && n.lat <= e.lat,
        r = o.lng >= i.lng && n.lng <= e.lng;
      return s && r
    },
    overlaps: function(t) {
      t = D(t);
      var i = this._southWest,
        e = this._northEast,
        n = t.getSouthWest(),
        o = t.getNorthEast(),
        s = o.lat > i.lat && n.lat < e.lat,
        r = o.lng > i.lng && n.lng < e.lng;
      return s && r
    },
    toBBoxString: function() {
      return [this.getWest(), this.getSouth(), this.getEast(), this.getNorth()].join(",")
    },
    equals: function(t, i) {
      return !!t && (t = D(t), this._southWest.equals(t.getSouthWest(), i) && this._northEast.equals(t.getNorthEast(), i))
    },
    isValid: function() {
      return !(!this._southWest || !this._northEast)
    }
  };
  var H, F = {
      latLngToPoint: function(t, i) {
        var e = this.projection.project(t),
          n = this.scale(i);
        return this.transformation._transform(e, n)
      },
      pointToLatLng: function(t, i) {
        var e = this.scale(i),
          n = this.transformation.untransform(t, e);
        return this.projection.unproject(n)
      },
      project: function(t) {
        return this.projection.project(t)
      },
      unproject: function(t) {
        return this.projection.unproject(t)
      },
      scale: function(t) {
        return 256 * Math.pow(2, t)
      },
      zoom: function(t) {
        return Math.log(t / 256) / Math.LN2
      },
      getProjectedBounds: function(t) {
        if (this.infinite) return null;
        var i = this.projection.bounds,
          e = this.scale(t);
        return new O(this.transformation.transform(i.min, e), this.transformation.transform(i.max, e))
      },
      infinite: !(j.prototype = {
        equals: function(t, i) {
          return !!t && (t = W(t), Math.max(Math.abs(this.lat - t.lat), Math.abs(this.lng - t.lng)) <= (void 0 === i ? 1e-9 : i))
        },
        toString: function(t) {
          return "LatLng(" + c(this.lat, t) + ", " + c(this.lng, t) + ")"
        },
        distanceTo: function(t) {
          return U.distance(this, W(t))
        },
        wrap: function() {
          return U.wrapLatLng(this)
        },
        toBounds: function(t) {
          var i = 180 * t / 40075017,
            e = i / Math.cos(Math.PI / 180 * this.lat);
          return D([this.lat - i, this.lng - e], [this.lat + i, this.lng + e])
        },
        clone: function() {
          return new j(this.lat, this.lng, this.alt)
        }
      }),
      wrapLatLng: function(t) {
        var i = this.wrapLng ? r(t.lng, this.wrapLng, !0) : t.lng;
        return new j(this.wrapLat ? r(t.lat, this.wrapLat, !0) : t.lat, i, t.alt)
      },
      wrapLatLngBounds: function(t) {
        var i = t.getCenter(),
          e = this.wrapLatLng(i),
          n = i.lat - e.lat,
          o = i.lng - e.lng;
        if (0 == n && 0 == o) return t;
        var s = t.getSouthWest(),
          r = t.getNorthEast();
        return new N(new j(s.lat - n, s.lng - o), new j(r.lat - n, r.lng - o))
      }
    },
    U = h({}, F, {
      wrapLng: [-180, 180],
      R: 6371e3,
      distance: function(t, i) {
        var e = Math.PI / 180,
          n = t.lat * e,
          o = i.lat * e,
          s = Math.sin((i.lat - t.lat) * e / 2),
          r = Math.sin((i.lng - t.lng) * e / 2),
          a = s * s + Math.cos(n) * Math.cos(o) * r * r,
          h = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        return this.R * h
      }
    }),
    V = 6378137,
    q = {
      R: V,
      MAX_LATITUDE: 85.0511287798,
      project: function(t) {
        var i = Math.PI / 180,
          e = this.MAX_LATITUDE,
          n = Math.max(Math.min(e, t.lat), -e),
          o = Math.sin(n * i);
        return new B(this.R * t.lng * i, this.R * Math.log((1 + o) / (1 - o)) / 2)
      },
      unproject: function(t) {
        var i = 180 / Math.PI;
        return new j((2 * Math.atan(Math.exp(t.y / this.R)) - Math.PI / 2) * i, t.x * i / this.R)
      },
      bounds: (H = V * Math.PI, new O([-H, -H], [H, H]))
    };

  function G(t, i, e, n) {
    if (v(t)) return this._a = t[0], this._b = t[1], this._c = t[2], void(this._d = t[3]);
    this._a = t, this._b = i, this._c = e, this._d = n
  }

  function K(t, i, e, n) {
    return new G(t, i, e, n)
  }
  G.prototype = {
    transform: function(t, i) {
      return this._transform(t.clone(), i)
    },
    _transform: function(t, i) {
      return i = i || 1, t.x = i * (this._a * t.x + this._b), t.y = i * (this._c * t.y + this._d), t
    },
    untransform: function(t, i) {
      return i = i || 1, new B((t.x / i - this._b) / this._a, (t.y / i - this._d) / this._c)
    }
  };
  var Y, X = h({}, U, {
      code: "EPSG:3857",
      projection: q,
      transformation: (Y = .5 / (Math.PI * q.R), K(Y, .5, -Y, .5))
    }),
    J = h({}, X, {
      code: "EPSG:900913"
    });

  function $(t) {
    return document.createElementNS("http://www.w3.org/2000/svg", t)
  }

  function Q(t, i) {
    var e, n, o, s, r, a, h = "";
    for (e = 0, o = t.length; e < o; e++) {
      for (n = 0, s = (r = t[e]).length; n < s; n++) h += (n ? "L" : "M") + (a = r[n]).x + " " + a.y;
      h += i ? Zt ? "z" : "x" : ""
    }
    return h || "M0 0"
  }
  var tt = document.documentElement.style,
    it = "ActiveXObject" in window,
    et = it && !document.addEventListener,
    nt = "msLaunchUri" in navigator && !("documentMode" in document),
    ot = kt("webkit"),
    st = kt("android"),
    rt = kt("android 2") || kt("android 3"),
    at = parseInt(/WebKit\/([0-9]+)|$/.exec(navigator.userAgent)[1], 10),
    ht = st && kt("Google") && at < 537 && !("AudioNode" in window),
    ut = !!window.opera,
    lt = kt("chrome"),
    ct = kt("gecko") && !ot && !ut && !it,
    _t = !lt && kt("safari"),
    dt = kt("phantom"),
    pt = "OTransition" in tt,
    mt = 0 === navigator.platform.indexOf("Win"),
    ft = it && "transition" in tt,
    gt = "WebKitCSSMatrix" in window && "m11" in new window.WebKitCSSMatrix && !rt,
    vt = "MozPerspective" in tt,
    yt = !window.L_DISABLE_3D && (ft || gt || vt) && !pt && !dt,
    xt = "undefined" != typeof orientation || kt("mobile"),
    wt = xt && ot,
    Pt = xt && gt,
    bt = !window.PointerEvent && window.MSPointerEvent,
    Lt = !(!window.PointerEvent && !bt),
    Tt = !window.L_NO_TOUCH && (Lt || "ontouchstart" in window || window.DocumentTouch && document instanceof window.DocumentTouch),
    zt = xt && ut,
    Mt = xt && ct,
    Ct = 1 < (window.devicePixelRatio || window.screen.deviceXDPI / window.screen.logicalXDPI),
    St = !!document.createElement("canvas").getContext,
    Zt = !(!document.createElementNS || !$("svg").createSVGRect),
    Et = !Zt && function() {
      try {
        var t = document.createElement("div");
        t.innerHTML = '<v:shape adj="1"/>';
        var i = t.firstChild;
        return i.style.behavior = "url(#default#VML)", i && "object" == typeof i.adj
      } catch (t) {
        return !1
      }
    }();

  function kt(t) {
    return 0 <= navigator.userAgent.toLowerCase().indexOf(t)
  }
  var Bt = (Object.freeze || Object)({
      ie: it,
      ielt9: et,
      edge: nt,
      webkit: ot,
      android: st,
      android23: rt,
      androidStock: ht,
      opera: ut,
      chrome: lt,
      gecko: ct,
      safari: _t,
      phantom: dt,
      opera12: pt,
      win: mt,
      ie3d: ft,
      webkit3d: gt,
      gecko3d: vt,
      any3d: yt,
      mobile: xt,
      mobileWebkit: wt,
      mobileWebkit3d: Pt,
      msPointer: bt,
      pointer: Lt,
      touch: Tt,
      mobileOpera: zt,
      mobileGecko: Mt,
      retina: Ct,
      canvas: St,
      svg: Zt,
      vml: Et
    }),
    At = bt ? "MSPointerDown" : "pointerdown",
    It = bt ? "MSPointerMove" : "pointermove",
    Ot = bt ? "MSPointerUp" : "pointerup",
    Rt = bt ? "MSPointerCancel" : "pointercancel",
    Nt = ["INPUT", "SELECT", "OPTION"],
    Dt = {},
    jt = !1,
    Wt = 0;

  function Ht(t, i, e, n) {
    return "touchstart" === i ? function(t, i, e) {
      var n = a(function(t) {
        if ("mouse" !== t.pointerType && t.MSPOINTER_TYPE_MOUSE && t.pointerType !== t.MSPOINTER_TYPE_MOUSE) {
          if (!(Nt.indexOf(t.target.tagName) < 0)) return;
          Di(t)
        }
        qt(t, i)
      });
      t["_leaflet_touchstart" + e] = n, t.addEventListener(At, n, !1), jt || (document.documentElement.addEventListener(At, Ft, !0), document.documentElement.addEventListener(It, Ut, !0), document.documentElement.addEventListener(Ot, Vt, !0), document.documentElement.addEventListener(Rt, Vt, !0), jt = !0)
    }(t, e, n) : "touchmove" === i ? function(t, i, e) {
      var n = function(t) {
        (t.pointerType !== t.MSPOINTER_TYPE_MOUSE && "mouse" !== t.pointerType || 0 !== t.buttons) && qt(t, i)
      };
      t["_leaflet_touchmove" + e] = n, t.addEventListener(It, n, !1)
    }(t, e, n) : "touchend" === i && function(t, i, e) {
      var n = function(t) {
        qt(t, i)
      };
      t["_leaflet_touchend" + e] = n, t.addEventListener(Ot, n, !1), t.addEventListener(Rt, n, !1)
    }(t, e, n), this
  }

  function Ft(t) {
    Dt[t.pointerId] = t, Wt++
  }

  function Ut(t) {
    Dt[t.pointerId] && (Dt[t.pointerId] = t)
  }

  function Vt(t) {
    delete Dt[t.pointerId], Wt--
  }

  function qt(t, i) {
    for (var e in t.touches = [], Dt) t.touches.push(Dt[e]);
    t.changedTouches = [t], i(t)
  }
  var Gt = bt ? "MSPointerDown" : Lt ? "pointerdown" : "touchstart",
    Kt = bt ? "MSPointerUp" : Lt ? "pointerup" : "touchend",
    Yt = "_leaflet_";

  function Xt(t, o, i) {
    var s, r, a = !1;

    function e(t) {
      var i;
      if (Lt) {
        if (!nt || "mouse" === t.pointerType) return;
        i = Wt
      } else i = t.touches.length;
      if (!(1 < i)) {
        var e = Date.now(),
          n = e - (s || e);
        r = t.touches ? t.touches[0] : t, a = 0 < n && n <= 250, s = e
      }
    }

    function n(t) {
      if (a && !r.cancelBubble) {
        if (Lt) {
          if (!nt || "mouse" === t.pointerType) return;
          var i, e, n = {};
          for (e in r) i = r[e], n[e] = i && i.bind ? i.bind(r) : i;
          r = n
        }
        r.type = "dblclick", r.button = 0, o(r), s = null
      }
    }
    return t[Yt + Gt + i] = e, t[Yt + Kt + i] = n, t[Yt + "dblclick" + i] = o, t.addEventListener(Gt, e, !1), t.addEventListener(Kt, n, !1), t.addEventListener("dblclick", o, !1), this
  }

  function Jt(t, i) {
    var e = t[Yt + Gt + i],
      n = t[Yt + Kt + i],
      o = t[Yt + "dblclick" + i];
    return t.removeEventListener(Gt, e, !1), t.removeEventListener(Kt, n, !1), nt || t.removeEventListener("dblclick", o, !1), this
  }
  var $t, Qt, ti, ii, ei, ni = yi(["transform", "webkitTransform", "OTransform", "MozTransform", "msTransform"]),
    oi = yi(["webkitTransition", "transition", "OTransition", "MozTransition", "msTransition"]),
    si = "webkitTransition" === oi || "OTransition" === oi ? oi + "End" : "transitionend";

  function ri(t) {
    return "string" == typeof t ? document.getElementById(t) : t
  }

  function ai(t, i) {
    var e = t.style[i] || t.currentStyle && t.currentStyle[i];
    if ((!e || "auto" === e) && document.defaultView) {
      var n = document.defaultView.getComputedStyle(t, null);
      e = n ? n[i] : null
    }
    return "auto" === e ? null : e
  }

  function hi(t, i, e) {
    var n = document.createElement(t);
    return n.className = i || "", e && e.appendChild(n), n
  }

  function ui(t) {
    var i = t.parentNode;
    i && i.removeChild(t)
  }

  function li(t) {
    for (; t.firstChild;) t.removeChild(t.firstChild)
  }

  function ci(t) {
    var i = t.parentNode;
    i && i.lastChild !== t && i.appendChild(t)
  }

  function _i(t) {
    var i = t.parentNode;
    i && i.firstChild !== t && i.insertBefore(t, i.firstChild)
  }

  function di(t, i) {
    if (void 0 !== t.classList) return t.classList.contains(i);
    var e = gi(t);
    return 0 < e.length && new RegExp("(^|\\s)" + i + "(\\s|$)").test(e)
  }

  function pi(t, i) {
    if (void 0 !== t.classList)
      for (var e = d(i), n = 0, o = e.length; n < o; n++) t.classList.add(e[n]);
    else if (!di(t, i)) {
      var s = gi(t);
      fi(t, (s ? s + " " : "") + i)
    }
  }

  function mi(t, i) {
    void 0 !== t.classList ? t.classList.remove(i) : fi(t, _((" " + gi(t) + " ").replace(" " + i + " ", " ")))
  }

  function fi(t, i) {
    void 0 === t.className.baseVal ? t.className = i : t.className.baseVal = i
  }

  function gi(t) {
    return t.correspondingElement && (t = t.correspondingElement), void 0 === t.className.baseVal ? t.className : t.className.baseVal
  }

  function vi(t, i) {
    "opacity" in t.style ? t.style.opacity = i : "filter" in t.style && function(t, i) {
      var e = !1,
        n = "DXImageTransform.Microsoft.Alpha";
      try {
        e = t.filters.item(n)
      } catch (t) {
        if (1 === i) return
      }
      i = Math.round(100 * i), e ? (e.Enabled = 100 !== i, e.Opacity = i) : t.style.filter += " progid:" + n + "(opacity=" + i + ")"
    }(t, i)
  }

  function yi(t) {
    for (var i = document.documentElement.style, e = 0; e < t.length; e++)
      if (t[e] in i) return t[e];
    return !1
  }

  function xi(t, i, e) {
    var n = i || new B(0, 0);
    t.style[ni] = (ft ? "translate(" + n.x + "px," + n.y + "px)" : "translate3d(" + n.x + "px," + n.y + "px,0)") + (e ? " scale(" + e + ")" : "")
  }

  function wi(t, i) {
    t._leaflet_pos = i, yt ? xi(t, i) : (t.style.left = i.x + "px", t.style.top = i.y + "px")
  }

  function Pi(t) {
    return t._leaflet_pos || new B(0, 0)
  }
  if ("onselectstart" in document) $t = function() {
    Ei(window, "selectstart", Di)
  }, Qt = function() {
    Bi(window, "selectstart", Di)
  };
  else {
    var bi = yi(["userSelect", "WebkitUserSelect", "OUserSelect", "MozUserSelect", "msUserSelect"]);
    $t = function() {
      if (bi) {
        var t = document.documentElement.style;
        ti = t[bi], t[bi] = "none"
      }
    }, Qt = function() {
      bi && (document.documentElement.style[bi] = ti, ti = void 0)
    }
  }

  function Li() {
    Ei(window, "dragstart", Di)
  }

  function Ti() {
    Bi(window, "dragstart", Di)
  }

  function zi(t) {
    for (; - 1 === t.tabIndex;) t = t.parentNode;
    t.style && (Mi(), ei = (ii = t).style.outline, t.style.outline = "none", Ei(window, "keydown", Mi))
  }

  function Mi() {
    ii && (ii.style.outline = ei, ei = ii = void 0, Bi(window, "keydown", Mi))
  }

  function Ci(t) {
    for (; !((t = t.parentNode).offsetWidth && t.offsetHeight || t === document.body););
    return t
  }

  function Si(t) {
    var i = t.getBoundingClientRect();
    return {
      x: i.width / t.offsetWidth || 1,
      y: i.height / t.offsetHeight || 1,
      boundingClientRect: i
    }
  }
  var Zi = (Object.freeze || Object)({
    TRANSFORM: ni,
    TRANSITION: oi,
    TRANSITION_END: si,
    get: ri,
    getStyle: ai,
    create: hi,
    remove: ui,
    empty: li,
    toFront: ci,
    toBack: _i,
    hasClass: di,
    addClass: pi,
    removeClass: mi,
    setClass: fi,
    getClass: gi,
    setOpacity: vi,
    testProp: yi,
    setTransform: xi,
    setPosition: wi,
    getPosition: Pi,
    disableTextSelection: $t,
    enableTextSelection: Qt,
    disableImageDrag: Li,
    enableImageDrag: Ti,
    preventOutline: zi,
    restoreOutline: Mi,
    getSizedParentNode: Ci,
    getScale: Si
  });

  function Ei(t, i, e, n) {
    if ("object" == typeof i)
      for (var o in i) Ai(t, o, i[o], e);
    else
      for (var s = 0, r = (i = d(i)).length; s < r; s++) Ai(t, i[s], e, n);
    return this
  }
  var ki = "_leaflet_events";

  function Bi(t, i, e, n) {
    if ("object" == typeof i)
      for (var o in i) Ii(t, o, i[o], e);
    else if (i)
      for (var s = 0, r = (i = d(i)).length; s < r; s++) Ii(t, i[s], e, n);
    else {
      for (var a in t[ki]) Ii(t, a, t[ki][a]);
      delete t[ki]
    }
    return this
  }

  function Ai(i, t, e, n) {
    var o = t + u(e) + (n ? "_" + u(n) : "");
    if (i[ki] && i[ki][o]) return this;
    var s = function(t) {
        return e.call(n || i, t || window.event)
      },
      r = s;
    Lt && 0 === t.indexOf("touch") ? Ht(i, t, s, o) : !Tt || "dblclick" !== t || Lt && lt ? "addEventListener" in i ? "mousewheel" === t ? i.addEventListener("onwheel" in i ? "wheel" : "mousewheel", s, !1) : "mouseenter" === t || "mouseleave" === t ? (s = function(t) {
      t = t || window.event, Ki(i, t) && r(t)
    }, i.addEventListener("mouseenter" === t ? "mouseover" : "mouseout", s, !1)) : ("click" === t && st && (s = function(t) {
      ! function(t, i) {
        var e = t.timeStamp || t.originalEvent && t.originalEvent.timeStamp,
          n = Ui && e - Ui;
        if (n && 100 < n && n < 500 || t.target._simulatedClick && !t._simulated) return ji(t);
        Ui = e, i(t)
      }(t, r)
    }), i.addEventListener(t, s, !1)) : "attachEvent" in i && i.attachEvent("on" + t, s) : Xt(i, s, o), i[ki] = i[ki] || {}, i[ki][o] = s
  }

  function Ii(t, i, e, n) {
    var o = i + u(e) + (n ? "_" + u(n) : ""),
      s = t[ki] && t[ki][o];
    if (!s) return this;
    Lt && 0 === i.indexOf("touch") ? function(t, i, e) {
      var n = t["_leaflet_" + i + e];
      "touchstart" === i ? t.removeEventListener(At, n, !1) : "touchmove" === i ? t.removeEventListener(It, n, !1) : "touchend" === i && (t.removeEventListener(Ot, n, !1), t.removeEventListener(Rt, n, !1))
    }(t, i, o) : !Tt || "dblclick" !== i || Lt && lt ? "removeEventListener" in t ? "mousewheel" === i ? t.removeEventListener("onwheel" in t ? "wheel" : "mousewheel", s, !1) : t.removeEventListener("mouseenter" === i ? "mouseover" : "mouseleave" === i ? "mouseout" : i, s, !1) : "detachEvent" in t && t.detachEvent("on" + i, s) : Jt(t, o), t[ki][o] = null
  }

  function Oi(t) {
    return t.stopPropagation ? t.stopPropagation() : t.originalEvent ? t.originalEvent._stopped = !0 : t.cancelBubble = !0, Gi(t), this
  }

  function Ri(t) {
    return Ai(t, "mousewheel", Oi), this
  }

  function Ni(t) {
    return Ei(t, "mousedown touchstart dblclick", Oi), Ai(t, "click", qi), this
  }

  function Di(t) {
    return t.preventDefault ? t.preventDefault() : t.returnValue = !1, this
  }

  function ji(t) {
    return Di(t), Oi(t), this
  }

  function Wi(t, i) {
    if (!i) return new B(t.clientX, t.clientY);
    var e = Si(i),
      n = e.boundingClientRect;
    return new B((t.clientX - n.left) / e.x - i.clientLeft, (t.clientY - n.top) / e.y - i.clientTop)
  }
  var Hi = mt && lt ? 2 * window.devicePixelRatio : ct ? window.devicePixelRatio : 1;

  function Fi(t) {
    return nt ? t.wheelDeltaY / 2 : t.deltaY && 0 === t.deltaMode ? -t.deltaY / Hi : t.deltaY && 1 === t.deltaMode ? 20 * -t.deltaY : t.deltaY && 2 === t.deltaMode ? 60 * -t.deltaY : t.deltaX || t.deltaZ ? 0 : t.wheelDelta ? (t.wheelDeltaY || t.wheelDelta) / 2 : t.detail && Math.abs(t.detail) < 32765 ? 20 * -t.detail : t.detail ? t.detail / -32765 * 60 : 0
  }
  var Ui, Vi = {};

  function qi(t) {
    Vi[t.type] = !0
  }

  function Gi(t) {
    var i = Vi[t.type];
    return Vi[t.type] = !1, i
  }

  function Ki(t, i) {
    var e = i.relatedTarget;
    if (!e) return !0;
    try {
      for (; e && e !== t;) e = e.parentNode
    } catch (t) {
      return !1
    }
    return e !== t
  }
  var Yi = (Object.freeze || Object)({
      on: Ei,
      off: Bi,
      stopPropagation: Oi,
      disableScrollPropagation: Ri,
      disableClickPropagation: Ni,
      preventDefault: Di,
      stop: ji,
      getMousePosition: Wi,
      getWheelDelta: Fi,
      fakeStop: qi,
      skipped: Gi,
      isExternalTarget: Ki,
      addListener: Ei,
      removeListener: Bi
    }),
    Xi = k.extend({
      run: function(t, i, e, n) {
        this.stop(), this._el = t, this._inProgress = !0, this._duration = e || .25, this._easeOutPower = 1 / Math.max(n || .5, .2), this._startPos = Pi(t), this._offset = i.subtract(this._startPos), this._startTime = +new Date, this.fire("start"), this._animate()
      },
      stop: function() {
        this._inProgress && (this._step(!0), this._complete())
      },
      _animate: function() {
        this._animId = M(this._animate, this), this._step()
      },
      _step: function(t) {
        var i = +new Date - this._startTime,
          e = 1e3 * this._duration;
        i < e ? this._runFrame(this._easeOut(i / e), t) : (this._runFrame(1), this._complete())
      },
      _runFrame: function(t, i) {
        var e = this._startPos.add(this._offset.multiplyBy(t));
        i && e._round(), wi(this._el, e), this.fire("step")
      },
      _complete: function() {
        C(this._animId), this._inProgress = !1, this.fire("end")
      },
      _easeOut: function(t) {
        return 1 - Math.pow(1 - t, this._easeOutPower)
      }
    }),
    Ji = k.extend({
      options: {
        crs: X,
        center: void 0,
        zoom: void 0,
        minZoom: void 0,
        maxZoom: void 0,
        layers: [],
        maxBounds: void 0,
        renderer: void 0,
        zoomAnimation: !0,
        zoomAnimationThreshold: 4,
        fadeAnimation: !0,
        markerZoomAnimation: !0,
        transform3DLimit: 8388608,
        zoomSnap: 1,
        zoomDelta: 1,
        trackResize: !0
      },
      initialize: function(t, i) {
        i = p(this, i), this._handlers = [], this._layers = {}, this._zoomBoundLayers = {}, this._sizeChanged = !0, this._initContainer(t), this._initLayout(), this._onResize = a(this._onResize, this), this._initEvents(), i.maxBounds && this.setMaxBounds(i.maxBounds), void 0 !== i.zoom && (this._zoom = this._limitZoom(i.zoom)), i.center && void 0 !== i.zoom && this.setView(W(i.center), i.zoom, {
          reset: !0
        }), this.callInitHooks(), this._zoomAnimated = oi && yt && !zt && this.options.zoomAnimation, this._zoomAnimated && (this._createAnimProxy(), Ei(this._proxy, si, this._catchTransitionEnd, this)), this._addLayers(this.options.layers)
      },
      setView: function(t, i, e) {
        if ((i = void 0 === i ? this._zoom : this._limitZoom(i), t = this._limitCenter(W(t), i, this.options.maxBounds), e = e || {}, this._stop(), this._loaded && !e.reset && !0 !== e) && (void 0 !== e.animate && (e.zoom = h({
            animate: e.animate
          }, e.zoom), e.pan = h({
            animate: e.animate,
            duration: e.duration
          }, e.pan)), this._zoom !== i ? this._tryAnimatedZoom && this._tryAnimatedZoom(t, i, e.zoom) : this._tryAnimatedPan(t, e.pan))) return clearTimeout(this._sizeTimer), this;
        return this._resetView(t, i), this
      },
      setZoom: function(t, i) {
        return this._loaded ? this.setView(this.getCenter(), t, {
          zoom: i
        }) : (this._zoom = t, this)
      },
      zoomIn: function(t, i) {
        return t = t || (yt ? this.options.zoomDelta : 1), this.setZoom(this._zoom + t, i)
      },
      zoomOut: function(t, i) {
        return t = t || (yt ? this.options.zoomDelta : 1), this.setZoom(this._zoom - t, i)
      },
      setZoomAround: function(t, i, e) {
        var n = this.getZoomScale(i),
          o = this.getSize().divideBy(2),
          s = (t instanceof B ? t : this.latLngToContainerPoint(t)).subtract(o).multiplyBy(1 - 1 / n),
          r = this.containerPointToLatLng(o.add(s));
        return this.setView(r, i, {
          zoom: e
        })
      },
      _getBoundsCenterZoom: function(t, i) {
        i = i || {}, t = t.getBounds ? t.getBounds() : D(t);
        var e = I(i.paddingTopLeft || i.padding || [0, 0]),
          n = I(i.paddingBottomRight || i.padding || [0, 0]),
          o = this.getBoundsZoom(t, !1, e.add(n));
        if ((o = "number" == typeof i.maxZoom ? Math.min(i.maxZoom, o) : o) === 1 / 0) return {
          center: t.getCenter(),
          zoom: o
        };
        var s = n.subtract(e).divideBy(2),
          r = this.project(t.getSouthWest(), o),
          a = this.project(t.getNorthEast(), o);
        return {
          center: this.unproject(r.add(a).divideBy(2).add(s), o),
          zoom: o
        }
      },
      fitBounds: function(t, i) {
        if (!(t = D(t)).isValid()) throw new Error("Bounds are not valid.");
        var e = this._getBoundsCenterZoom(t, i);
        return this.setView(e.center, e.zoom, i)
      },
      fitWorld: function(t) {
        return this.fitBounds([
          [-90, -180],
          [90, 180]
        ], t)
      },
      panTo: function(t, i) {
        return this.setView(t, this._zoom, {
          pan: i
        })
      },
      panBy: function(t, i) {
        if (i = i || {}, !(t = I(t).round()).x && !t.y) return this.fire("moveend");
        if (!0 !== i.animate && !this.getSize().contains(t)) return this._resetView(this.unproject(this.project(this.getCenter()).add(t)), this.getZoom()), this;
        if (this._panAnim || (this._panAnim = new Xi, this._panAnim.on({
            step: this._onPanTransitionStep,
            end: this._onPanTransitionEnd
          }, this)), i.noMoveStart || this.fire("movestart"), !1 !== i.animate) {
          pi(this._mapPane, "leaflet-pan-anim");
          var e = this._getMapPanePos().subtract(t).round();
          this._panAnim.run(this._mapPane, e, i.duration || .25, i.easeLinearity)
        } else this._rawPanBy(t), this.fire("move").fire("moveend");
        return this
      },
      flyTo: function(n, o, t) {
        if (!1 === (t = t || {}).animate || !yt) return this.setView(n, o, t);
        this._stop();
        var s = this.project(this.getCenter()),
          r = this.project(n),
          i = this.getSize(),
          a = this._zoom;
        n = W(n), o = void 0 === o ? a : o;
        var h = Math.max(i.x, i.y),
          u = h * this.getZoomScale(a, o),
          l = r.distanceTo(s) || 1,
          c = 1.42,
          _ = c * c;

        function e(t) {
          var i = (u * u - h * h + (t ? -1 : 1) * _ * _ * l * l) / (2 * (t ? u : h) * _ * l),
            e = Math.sqrt(i * i + 1) - i;
          return e < 1e-9 ? -18 : Math.log(e)
        }

        function d(t) {
          return (Math.exp(t) - Math.exp(-t)) / 2
        }

        function p(t) {
          return (Math.exp(t) + Math.exp(-t)) / 2
        }
        var m = e(0);

        function f(t) {
          return h * (p(m) * function(t) {
            return d(t) / p(t)
          }(m + c * t) - d(m)) / _
        }
        var g = Date.now(),
          v = (e(1) - m) / c,
          y = t.duration ? 1e3 * t.duration : 1e3 * v * .8;
        return this._moveStart(!0, t.noMoveStart),
          function t() {
            var i = (Date.now() - g) / y,
              e = function(t) {
                return 1 - Math.pow(1 - t, 1.5)
              }(i) * v;
            i <= 1 ? (this._flyToFrame = M(t, this), this._move(this.unproject(s.add(r.subtract(s).multiplyBy(f(e) / l)), a), this.getScaleZoom(h / function(t) {
              return h * (p(m) / p(m + c * t))
            }(e), a), {
              flyTo: !0
            })) : this._move(n, o)._moveEnd(!0)
          }.call(this), this
      },
      flyToBounds: function(t, i) {
        var e = this._getBoundsCenterZoom(t, i);
        return this.flyTo(e.center, e.zoom, i)
      },
      setMaxBounds: function(t) {
        return (t = D(t)).isValid() ? (this.options.maxBounds && this.off("moveend", this._panInsideMaxBounds), this.options.maxBounds = t, this._loaded && this._panInsideMaxBounds(), this.on("moveend", this._panInsideMaxBounds)) : (this.options.maxBounds = null, this.off("moveend", this._panInsideMaxBounds))
      },
      setMinZoom: function(t) {
        var i = this.options.minZoom;
        return this.options.minZoom = t, this._loaded && i !== t && (this.fire("zoomlevelschange"), this.getZoom() < this.options.minZoom) ? this.setZoom(t) : this
      },
      setMaxZoom: function(t) {
        var i = this.options.maxZoom;
        return this.options.maxZoom = t, this._loaded && i !== t && (this.fire("zoomlevelschange"), this.getZoom() > this.options.maxZoom) ? this.setZoom(t) : this
      },
      panInsideBounds: function(t, i) {
        this._enforcingBounds = !0;
        var e = this.getCenter(),
          n = this._limitCenter(e, this._zoom, D(t));
        return e.equals(n) || this.panTo(n, i), this._enforcingBounds = !1, this
      },
      panInside: function(t, i) {
        var e = I((i = i || {}).paddingTopLeft || i.padding || [0, 0]),
          n = I(i.paddingBottomRight || i.padding || [0, 0]),
          o = this.getCenter(),
          s = this.project(o),
          r = this.project(t),
          a = this.getPixelBounds(),
          h = a.getSize().divideBy(2),
          u = R([a.min.add(e), a.max.subtract(n)]);
        if (!u.contains(r)) {
          this._enforcingBounds = !0;
          var l = s.subtract(r),
            c = I(r.x + l.x, r.y + l.y);
          (r.x < u.min.x || r.x > u.max.x) && (c.x = s.x - l.x, 0 < l.x ? c.x += h.x - e.x : c.x -= h.x - n.x), (r.y < u.min.y || r.y > u.max.y) && (c.y = s.y - l.y, 0 < l.y ? c.y += h.y - e.y : c.y -= h.y - n.y), this.panTo(this.unproject(c), i), this._enforcingBounds = !1
        }
        return this
      },
      invalidateSize: function(t) {
        if (!this._loaded) return this;
        t = h({
          animate: !1,
          pan: !0
        }, !0 === t ? {
          animate: !0
        } : t);
        var i = this.getSize();
        this._sizeChanged = !0, this._lastCenter = null;
        var e = this.getSize(),
          n = i.divideBy(2).round(),
          o = e.divideBy(2).round(),
          s = n.subtract(o);
        return s.x || s.y ? (t.animate && t.pan ? this.panBy(s) : (t.pan && this._rawPanBy(s), this.fire("move"), t.debounceMoveend ? (clearTimeout(this._sizeTimer), this._sizeTimer = setTimeout(a(this.fire, this, "moveend"), 200)) : this.fire("moveend")), this.fire("resize", {
          oldSize: i,
          newSize: e
        })) : this
      },
      stop: function() {
        return this.setZoom(this._limitZoom(this._zoom)), this.options.zoomSnap || this.fire("viewreset"), this._stop()
      },
      locate: function(t) {
        if (t = this._locateOptions = h({
            timeout: 1e4,
            watch: !1
          }, t), !("geolocation" in navigator)) return this._handleGeolocationError({
          code: 0,
          message: "Geolocation not supported."
        }), this;
        var i = a(this._handleGeolocationResponse, this),
          e = a(this._handleGeolocationError, this);
        return t.watch ? this._locationWatchId = navigator.geolocation.watchPosition(i, e, t) : navigator.geolocation.getCurrentPosition(i, e, t), this
      },
      stopLocate: function() {
        return navigator.geolocation && navigator.geolocation.clearWatch && navigator.geolocation.clearWatch(this._locationWatchId), this._locateOptions && (this._locateOptions.setView = !1), this
      },
      _handleGeolocationError: function(t) {
        var i = t.code,
          e = t.message || (1 === i ? "permission denied" : 2 === i ? "position unavailable" : "timeout");
        this._locateOptions.setView && !this._loaded && this.fitWorld(), this.fire("locationerror", {
          code: i,
          message: "Geolocation error: " + e + "."
        })
      },
      _handleGeolocationResponse: function(t) {
        var i = new j(t.coords.latitude, t.coords.longitude),
          e = i.toBounds(2 * t.coords.accuracy),
          n = this._locateOptions;
        if (n.setView) {
          var o = this.getBoundsZoom(e);
          this.setView(i, n.maxZoom ? Math.min(o, n.maxZoom) : o)
        }
        var s = {
          latlng: i,
          bounds: e,
          timestamp: t.timestamp
        };
        for (var r in t.coords) "number" == typeof t.coords[r] && (s[r] = t.coords[r]);
        this.fire("locationfound", s)
      },
      addHandler: function(t, i) {
        if (!i) return this;
        var e = this[t] = new i(this);
        return this._handlers.push(e), this.options[t] && e.enable(), this
      },
      remove: function() {
        if (this._initEvents(!0), this._containerId !== this._container._leaflet_id) throw new Error("Map container is being reused by another instance");
        try {
          delete this._container._leaflet_id, delete this._containerId
        } catch (t) {
          this._container._leaflet_id = void 0, this._containerId = void 0
        }
        var t;
        for (t in void 0 !== this._locationWatchId && this.stopLocate(), this._stop(), ui(this._mapPane), this._clearControlPos && this._clearControlPos(), this._resizeRequest && (C(this._resizeRequest), this._resizeRequest = null), this._clearHandlers(), this._loaded && this.fire("unload"), this._layers) this._layers[t].remove();
        for (t in this._panes) ui(this._panes[t]);
        return this._layers = [], this._panes = [], delete this._mapPane, delete this._renderer, this
      },
      createPane: function(t, i) {
        var e = hi("div", "leaflet-pane" + (t ? " leaflet-" + t.replace("Pane", "") + "-pane" : ""), i || this._mapPane);
        return t && (this._panes[t] = e), e
      },
      getCenter: function() {
        return this._checkIfLoaded(), this._lastCenter && !this._moved() ? this._lastCenter : this.layerPointToLatLng(this._getCenterLayerPoint())
      },
      getZoom: function() {
        return this._zoom
      },
      getBounds: function() {
        var t = this.getPixelBounds();
        return new N(this.unproject(t.getBottomLeft()), this.unproject(t.getTopRight()))
      },
      getMinZoom: function() {
        return void 0 === this.options.minZoom ? this._layersMinZoom || 0 : this.options.minZoom
      },
      getMaxZoom: function() {
        return void 0 === this.options.maxZoom ? void 0 === this._layersMaxZoom ? 1 / 0 : this._layersMaxZoom : this.options.maxZoom
      },
      getBoundsZoom: function(t, i, e) {
        t = D(t), e = I(e || [0, 0]);
        var n = this.getZoom() || 0,
          o = this.getMinZoom(),
          s = this.getMaxZoom(),
          r = t.getNorthWest(),
          a = t.getSouthEast(),
          h = this.getSize().subtract(e),
          u = R(this.project(a, n), this.project(r, n)).getSize(),
          l = yt ? this.options.zoomSnap : 1,
          c = h.x / u.x,
          _ = h.y / u.y,
          d = i ? Math.max(c, _) : Math.min(c, _);
        return n = this.getScaleZoom(d, n), l && (n = Math.round(n / (l / 100)) * (l / 100), n = i ? Math.ceil(n / l) * l : Math.floor(n / l) * l), Math.max(o, Math.min(s, n))
      },
      getSize: function() {
        return this._size && !this._sizeChanged || (this._size = new B(this._container.clientWidth || 0, this._container.clientHeight || 0), this._sizeChanged = !1), this._size.clone()
      },
      getPixelBounds: function(t, i) {
        var e = this._getTopLeftPoint(t, i);
        return new O(e, e.add(this.getSize()))
      },
      getPixelOrigin: function() {
        return this._checkIfLoaded(), this._pixelOrigin
      },
      getPixelWorldBounds: function(t) {
        return this.options.crs.getProjectedBounds(void 0 === t ? this.getZoom() : t)
      },
      getPane: function(t) {
        return "string" == typeof t ? this._panes[t] : t
      },
      getPanes: function() {
        return this._panes
      },
      getContainer: function() {
        return this._container
      },
      getZoomScale: function(t, i) {
        var e = this.options.crs;
        return i = void 0 === i ? this._zoom : i, e.scale(t) / e.scale(i)
      },
      getScaleZoom: function(t, i) {
        var e = this.options.crs;
        i = void 0 === i ? this._zoom : i;
        var n = e.zoom(t * e.scale(i));
        return isNaN(n) ? 1 / 0 : n
      },
      project: function(t, i) {
        return i = void 0 === i ? this._zoom : i, this.options.crs.latLngToPoint(W(t), i)
      },
      unproject: function(t, i) {
        return i = void 0 === i ? this._zoom : i, this.options.crs.pointToLatLng(I(t), i)
      },
      layerPointToLatLng: function(t) {
        var i = I(t).add(this.getPixelOrigin());
        return this.unproject(i)
      },
      latLngToLayerPoint: function(t) {
        return this.project(W(t))._round()._subtract(this.getPixelOrigin())
      },
      wrapLatLng: function(t) {
        return this.options.crs.wrapLatLng(W(t))
      },
      wrapLatLngBounds: function(t) {
        return this.options.crs.wrapLatLngBounds(D(t))
      },
      distance: function(t, i) {
        return this.options.crs.distance(W(t), W(i))
      },
      containerPointToLayerPoint: function(t) {
        return I(t).subtract(this._getMapPanePos())
      },
      layerPointToContainerPoint: function(t) {
        return I(t).add(this._getMapPanePos())
      },
      containerPointToLatLng: function(t) {
        var i = this.containerPointToLayerPoint(I(t));
        return this.layerPointToLatLng(i)
      },
      latLngToContainerPoint: function(t) {
        return this.layerPointToContainerPoint(this.latLngToLayerPoint(W(t)))
      },
      mouseEventToContainerPoint: function(t) {
        return Wi(t, this._container)
      },
      mouseEventToLayerPoint: function(t) {
        return this.containerPointToLayerPoint(this.mouseEventToContainerPoint(t))
      },
      mouseEventToLatLng: function(t) {
        return this.layerPointToLatLng(this.mouseEventToLayerPoint(t))
      },
      _initContainer: function(t) {
        var i = this._container = ri(t);
        if (!i) throw new Error("Map container not found.");
        if (i._leaflet_id) throw new Error("Map container is already initialized.");
        Ei(i, "scroll", this._onScroll, this), this._containerId = u(i)
      },
      _initLayout: function() {
        var t = this._container;
        this._fadeAnimated = this.options.fadeAnimation && yt, pi(t, "leaflet-container" + (Tt ? " leaflet-touch" : "") + (Ct ? " leaflet-retina" : "") + (et ? " leaflet-oldie" : "") + (_t ? " leaflet-safari" : "") + (this._fadeAnimated ? " leaflet-fade-anim" : ""));
        var i = ai(t, "position");
        "absolute" !== i && "relative" !== i && "fixed" !== i && (t.style.position = "relative"), this._initPanes(), this._initControlPos && this._initControlPos()
      },
      _initPanes: function() {
        var t = this._panes = {};
        this._paneRenderers = {}, this._mapPane = this.createPane("mapPane", this._container), wi(this._mapPane, new B(0, 0)), this.createPane("tilePane"), this.createPane("shadowPane"), this.createPane("overlayPane"), this.createPane("markerPane"), this.createPane("tooltipPane"), this.createPane("popupPane"), this.options.markerZoomAnimation || (pi(t.markerPane, "leaflet-zoom-hide"), pi(t.shadowPane, "leaflet-zoom-hide"))
      },
      _resetView: function(t, i) {
        wi(this._mapPane, new B(0, 0));
        var e = !this._loaded;
        this._loaded = !0, i = this._limitZoom(i), this.fire("viewprereset");
        var n = this._zoom !== i;
        this._moveStart(n, !1)._move(t, i)._moveEnd(n), this.fire("viewreset"), e && this.fire("load")
      },
      _moveStart: function(t, i) {
        return t && this.fire("zoomstart"), i || this.fire("movestart"), this
      },
      _move: function(t, i, e) {
        void 0 === i && (i = this._zoom);
        var n = this._zoom !== i;
        return this._zoom = i, this._lastCenter = t, this._pixelOrigin = this._getNewPixelOrigin(t), (n || e && e.pinch) && this.fire("zoom", e), this.fire("move", e)
      },
      _moveEnd: function(t) {
        return t && this.fire("zoomend"), this.fire("moveend")
      },
      _stop: function() {
        return C(this._flyToFrame), this._panAnim && this._panAnim.stop(), this
      },
      _rawPanBy: function(t) {
        wi(this._mapPane, this._getMapPanePos().subtract(t))
      },
      _getZoomSpan: function() {
        return this.getMaxZoom() - this.getMinZoom()
      },
      _panInsideMaxBounds: function() {
        this._enforcingBounds || this.panInsideBounds(this.options.maxBounds)
      },
      _checkIfLoaded: function() {
        if (!this._loaded) throw new Error("Set map center and zoom first.")
      },
      _initEvents: function(t) {
        this._targets = {};
        var i = t ? Bi : Ei;
        i((this._targets[u(this._container)] = this)._container, "click dblclick mousedown mouseup mouseover mouseout mousemove contextmenu keypress keydown keyup", this._handleDOMEvent, this), this.options.trackResize && i(window, "resize", this._onResize, this), yt && this.options.transform3DLimit && (t ? this.off : this.on).call(this, "moveend", this._onMoveEnd)
      },
      _onResize: function() {
        C(this._resizeRequest), this._resizeRequest = M(function() {
          this.invalidateSize({
            debounceMoveend: !0
          })
        }, this)
      },
      _onScroll: function() {
        this._container.scrollTop = 0, this._container.scrollLeft = 0
      },
      _onMoveEnd: function() {
        var t = this._getMapPanePos();
        Math.max(Math.abs(t.x), Math.abs(t.y)) >= this.options.transform3DLimit && this._resetView(this.getCenter(), this.getZoom())
      },
      _findEventTargets: function(t, i) {
        for (var e, n = [], o = "mouseout" === i || "mouseover" === i, s = t.target || t.srcElement, r = !1; s;) {
          if ((e = this._targets[u(s)]) && ("click" === i || "preclick" === i) && !t._simulated && this._draggableMoved(e)) {
            r = !0;
            break
          }
          if (e && e.listens(i, !0)) {
            if (o && !Ki(s, t)) break;
            if (n.push(e), o) break
          }
          if (s === this._container) break;
          s = s.parentNode
        }
        return n.length || r || o || !Ki(s, t) || (n = [this]), n
      },
      _handleDOMEvent: function(t) {
        if (this._loaded && !Gi(t)) {
          var i = t.type;
          "mousedown" !== i && "keypress" !== i && "keyup" !== i && "keydown" !== i || zi(t.target || t.srcElement), this._fireDOMEvent(t, i)
        }
      },
      _mouseEvents: ["click", "dblclick", "mouseover", "mouseout", "contextmenu"],
      _fireDOMEvent: function(t, i, e) {
        if ("click" === t.type) {
          var n = h({}, t);
          n.type = "preclick", this._fireDOMEvent(n, n.type, e)
        }
        if (!t._stopped && (e = (e || []).concat(this._findEventTargets(t, i))).length) {
          var o = e[0];
          "contextmenu" === i && o.listens(i, !0) && Di(t);
          var s = {
            originalEvent: t
          };
          if ("keypress" !== t.type && "keydown" !== t.type && "keyup" !== t.type) {
            var r = o.getLatLng && (!o._radius || o._radius <= 10);
            s.containerPoint = r ? this.latLngToContainerPoint(o.getLatLng()) : this.mouseEventToContainerPoint(t), s.layerPoint = this.containerPointToLayerPoint(s.containerPoint), s.latlng = r ? o.getLatLng() : this.layerPointToLatLng(s.layerPoint)
          }
          for (var a = 0; a < e.length; a++)
            if (e[a].fire(i, s, !0), s.originalEvent._stopped || !1 === e[a].options.bubblingMouseEvents && -1 !== y(this._mouseEvents, i)) return
        }
      },
      _draggableMoved: function(t) {
        return (t = t.dragging && t.dragging.enabled() ? t : this).dragging && t.dragging.moved() || this.boxZoom && this.boxZoom.moved()
      },
      _clearHandlers: function() {
        for (var t = 0, i = this._handlers.length; t < i; t++) this._handlers[t].disable()
      },
      whenReady: function(t, i) {
        return this._loaded ? t.call(i || this, {
          target: this
        }) : this.on("load", t, i), this
      },
      _getMapPanePos: function() {
        return Pi(this._mapPane) || new B(0, 0)
      },
      _moved: function() {
        var t = this._getMapPanePos();
        return t && !t.equals([0, 0])
      },
      _getTopLeftPoint: function(t, i) {
        return (t && void 0 !== i ? this._getNewPixelOrigin(t, i) : this.getPixelOrigin()).subtract(this._getMapPanePos())
      },
      _getNewPixelOrigin: function(t, i) {
        var e = this.getSize()._divideBy(2);
        return this.project(t, i)._subtract(e)._add(this._getMapPanePos())._round()
      },
      _latLngToNewLayerPoint: function(t, i, e) {
        var n = this._getNewPixelOrigin(e, i);
        return this.project(t, i)._subtract(n)
      },
      _latLngBoundsToNewLayerBounds: function(t, i, e) {
        var n = this._getNewPixelOrigin(e, i);
        return R([this.project(t.getSouthWest(), i)._subtract(n), this.project(t.getNorthWest(), i)._subtract(n), this.project(t.getSouthEast(), i)._subtract(n), this.project(t.getNorthEast(), i)._subtract(n)])
      },
      _getCenterLayerPoint: function() {
        return this.containerPointToLayerPoint(this.getSize()._divideBy(2))
      },
      _getCenterOffset: function(t) {
        return this.latLngToLayerPoint(t).subtract(this._getCenterLayerPoint())
      },
      _limitCenter: function(t, i, e) {
        if (!e) return t;
        var n = this.project(t, i),
          o = this.getSize().divideBy(2),
          s = new O(n.subtract(o), n.add(o)),
          r = this._getBoundsOffset(s, e, i);
        return r.round().equals([0, 0]) ? t : this.unproject(n.add(r), i)
      },
      _limitOffset: function(t, i) {
        if (!i) return t;
        var e = this.getPixelBounds(),
          n = new O(e.min.add(t), e.max.add(t));
        return t.add(this._getBoundsOffset(n, i))
      },
      _getBoundsOffset: function(t, i, e) {
        var n = R(this.project(i.getNorthEast(), e), this.project(i.getSouthWest(), e)),
          o = n.min.subtract(t.min),
          s = n.max.subtract(t.max);
        return new B(this._rebound(o.x, -s.x), this._rebound(o.y, -s.y))
      },
      _rebound: function(t, i) {
        return 0 < t + i ? Math.round(t - i) / 2 : Math.max(0, Math.ceil(t)) - Math.max(0, Math.floor(i))
      },
      _limitZoom: function(t) {
        var i = this.getMinZoom(),
          e = this.getMaxZoom(),
          n = yt ? this.options.zoomSnap : 1;
        return n && (t = Math.round(t / n) * n), Math.max(i, Math.min(e, t))
      },
      _onPanTransitionStep: function() {
        this.fire("move")
      },
      _onPanTransitionEnd: function() {
        mi(this._mapPane, "leaflet-pan-anim"), this.fire("moveend")
      },
      _tryAnimatedPan: function(t, i) {
        var e = this._getCenterOffset(t)._trunc();
        return !(!0 !== (i && i.animate) && !this.getSize().contains(e)) && (this.panBy(e, i), !0)
      },
      _createAnimProxy: function() {
        var t = this._proxy = hi("div", "leaflet-proxy leaflet-zoom-animated");
        this._panes.mapPane.appendChild(t), this.on("zoomanim", function(t) {
          var i = ni,
            e = this._proxy.style[i];
          xi(this._proxy, this.project(t.center, t.zoom), this.getZoomScale(t.zoom, 1)), e === this._proxy.style[i] && this._animatingZoom && this._onZoomTransitionEnd()
        }, this), this.on("load moveend", function() {
          var t = this.getCenter(),
            i = this.getZoom();
          xi(this._proxy, this.project(t, i), this.getZoomScale(i, 1))
        }, this), this._on("unload", this._destroyAnimProxy, this)
      },
      _destroyAnimProxy: function() {
        ui(this._proxy), delete this._proxy
      },
      _catchTransitionEnd: function(t) {
        this._animatingZoom && 0 <= t.propertyName.indexOf("transform") && this._onZoomTransitionEnd()
      },
      _nothingToAnimate: function() {
        return !this._container.getElementsByClassName("leaflet-zoom-animated").length
      },
      _tryAnimatedZoom: function(t, i, e) {
        if (this._animatingZoom) return !0;
        if (e = e || {}, !this._zoomAnimated || !1 === e.animate || this._nothingToAnimate() || Math.abs(i - this._zoom) > this.options.zoomAnimationThreshold) return !1;
        var n = this.getZoomScale(i),
          o = this._getCenterOffset(t)._divideBy(1 - 1 / n);
        return !(!0 !== e.animate && !this.getSize().contains(o)) && (M(function() {
          this._moveStart(!0, !1)._animateZoom(t, i, !0)
        }, this), !0)
      },
      _animateZoom: function(t, i, e, n) {
        this._mapPane && (e && (this._animatingZoom = !0, this._animateToCenter = t, this._animateToZoom = i, pi(this._mapPane, "leaflet-zoom-anim")), this.fire("zoomanim", {
          center: t,
          zoom: i,
          noUpdate: n
        }), setTimeout(a(this._onZoomTransitionEnd, this), 250))
      },
      _onZoomTransitionEnd: function() {
        this._animatingZoom && (this._mapPane && mi(this._mapPane, "leaflet-zoom-anim"), this._animatingZoom = !1, this._move(this._animateToCenter, this._animateToZoom), M(function() {
          this._moveEnd(!0)
        }, this))
      }
    });

  function $i(t) {
    return new Qi(t)
  }
  var Qi = Z.extend({
    options: {
      position: "topright"
    },
    initialize: function(t) {
      p(this, t)
    },
    getPosition: function() {
      return this.options.position
    },
    setPosition: function(t) {
      var i = this._map;
      return i && i.removeControl(this), this.options.position = t, i && i.addControl(this), this
    },
    getContainer: function() {
      return this._container
    },
    addTo: function(t) {
      this.remove(), this._map = t;
      var i = this._container = this.onAdd(t),
        e = this.getPosition(),
        n = t._controlCorners[e];
      return pi(i, "leaflet-control"), -1 !== e.indexOf("bottom") ? n.insertBefore(i, n.firstChild) : n.appendChild(i), this._map.on("unload", this.remove, this), this
    },
    remove: function() {
      return this._map && (ui(this._container), this.onRemove && this.onRemove(this._map), this._map.off("unload", this.remove, this), this._map = null), this
    },
    _refocusOnMap: function(t) {
      this._map && t && 0 < t.screenX && 0 < t.screenY && this._map.getContainer().focus()
    }
  });
  Ji.include({
    addControl: function(t) {
      return t.addTo(this), this
    },
    removeControl: function(t) {
      return t.remove(), this
    },
    _initControlPos: function() {
      var n = this._controlCorners = {},
        o = "leaflet-",
        s = this._controlContainer = hi("div", o + "control-container", this._container);

      function t(t, i) {
        var e = o + t + " " + o + i;
        n[t + i] = hi("div", e, s)
      }
      t("top", "left"), t("top", "right"), t("bottom", "left"), t("bottom", "right")
    },
    _clearControlPos: function() {
      for (var t in this._controlCorners) ui(this._controlCorners[t]);
      ui(this._controlContainer), delete this._controlCorners, delete this._controlContainer
    }
  });
  var te = Qi.extend({
      options: {
        collapsed: !0,
        position: "topright",
        autoZIndex: !0,
        hideSingleBase: !1,
        sortLayers: !1,
        sortFunction: function(t, i, e, n) {
          return e < n ? -1 : n < e ? 1 : 0
        }
      },
      initialize: function(t, i, e) {
        for (var n in p(this, e), this._layerControlInputs = [], this._layers = [], this._lastZIndex = 0, this._handlingClick = !1, t) this._addLayer(t[n], n);
        for (n in i) this._addLayer(i[n], n, !0)
      },
      onAdd: function(t) {
        this._initLayout(), this._update(), (this._map = t).on("zoomend", this._checkDisabledLayers, this);
        for (var i = 0; i < this._layers.length; i++) this._layers[i].layer.on("add remove", this._onLayerChange, this);
        return this._container
      },
      addTo: function(t) {
        return Qi.prototype.addTo.call(this, t), this._expandIfNotCollapsed()
      },
      onRemove: function() {
        this._map.off("zoomend", this._checkDisabledLayers, this);
        for (var t = 0; t < this._layers.length; t++) this._layers[t].layer.off("add remove", this._onLayerChange, this)
      },
      addBaseLayer: function(t, i) {
        return this._addLayer(t, i), this._map ? this._update() : this
      },
      addOverlay: function(t, i) {
        return this._addLayer(t, i, !0), this._map ? this._update() : this
      },
      removeLayer: function(t) {
        t.off("add remove", this._onLayerChange, this);
        var i = this._getLayer(u(t));
        return i && this._layers.splice(this._layers.indexOf(i), 1), this._map ? this._update() : this
      },
      expand: function() {
        pi(this._container, "leaflet-control-layers-expanded"), this._section.style.height = null;
        var t = this._map.getSize().y - (this._container.offsetTop + 50);
        return t < this._section.clientHeight ? (pi(this._section, "leaflet-control-layers-scrollbar"), this._section.style.height = t + "px") : mi(this._section, "leaflet-control-layers-scrollbar"), this._checkDisabledLayers(), this
      },
      collapse: function() {
        return mi(this._container, "leaflet-control-layers-expanded"), this
      },
      _initLayout: function() {
        var t = "leaflet-control-layers",
          i = this._container = hi("div", t),
          e = this.options.collapsed;
        i.setAttribute("aria-haspopup", !0), Ni(i), Ri(i);
        var n = this._section = hi("section", t + "-list");
        e && (this._map.on("click", this.collapse, this), st || Ei(i, {
          mouseenter: this.expand,
          mouseleave: this.collapse
        }, this));
        var o = this._layersLink = hi("a", t + "-toggle", i);
        o.href = "#", o.title = "Layers", Tt ? (Ei(o, "click", ji), Ei(o, "click", this.expand, this)) : Ei(o, "focus", this.expand, this), e || this.expand(), this._baseLayersList = hi("div", t + "-base", n), this._separator = hi("div", t + "-separator", n), this._overlaysList = hi("div", t + "-overlays", n), i.appendChild(n)
      },
      _getLayer: function(t) {
        for (var i = 0; i < this._layers.length; i++)
          if (this._layers[i] && u(this._layers[i].layer) === t) return this._layers[i]
      },
      _addLayer: function(t, i, e) {
        this._map && t.on("add remove", this._onLayerChange, this), this._layers.push({
          layer: t,
          name: i,
          overlay: e
        }), this.options.sortLayers && this._layers.sort(a(function(t, i) {
          return this.options.sortFunction(t.layer, i.layer, t.name, i.name)
        }, this)), this.options.autoZIndex && t.setZIndex && (this._lastZIndex++, t.setZIndex(this._lastZIndex)), this._expandIfNotCollapsed()
      },
      _update: function() {
        if (!this._container) return this;
        li(this._baseLayersList), li(this._overlaysList), this._layerControlInputs = [];
        var t, i, e, n, o = 0;
        for (e = 0; e < this._layers.length; e++) n = this._layers[e], this._addItem(n), i = i || n.overlay, t = t || !n.overlay, o += n.overlay ? 0 : 1;
        return this.options.hideSingleBase && (t = t && 1 < o, this._baseLayersList.style.display = t ? "" : "none"), this._separator.style.display = i && t ? "" : "none", this
      },
      _onLayerChange: function(t) {
        this._handlingClick || this._update();
        var i = this._getLayer(u(t.target)),
          e = i.overlay ? "add" === t.type ? "overlayadd" : "overlayremove" : "add" === t.type ? "baselayerchange" : null;
        e && this._map.fire(e, i)
      },
      _createRadioElement: function(t, i) {
        var e = '<input type="radio" class="leaflet-control-layers-selector" name="' + t + '"' + (i ? ' checked="checked"' : "") + "/>",
          n = document.createElement("div");
        return n.innerHTML = e, n.firstChild
      },
      _addItem: function(t) {
        var i, e = document.createElement("label"),
          n = this._map.hasLayer(t.layer);
        t.overlay ? ((i = document.createElement("input")).type = "checkbox", i.className = "leaflet-control-layers-selector", i.defaultChecked = n) : i = this._createRadioElement("leaflet-base-layers_" + u(this), n), this._layerControlInputs.push(i), i.layerId = u(t.layer), Ei(i, "click", this._onInputClick, this);
        var o = document.createElement("span");
        o.innerHTML = " " + t.name;
        var s = document.createElement("div");
        return e.appendChild(s), s.appendChild(i), s.appendChild(o), (t.overlay ? this._overlaysList : this._baseLayersList).appendChild(e), this._checkDisabledLayers(), e
      },
      _onInputClick: function() {
        var t, i, e = this._layerControlInputs,
          n = [],
          o = [];
        this._handlingClick = !0;
        for (var s = e.length - 1; 0 <= s; s--) t = e[s], i = this._getLayer(t.layerId).layer, t.checked ? n.push(i) : t.checked || o.push(i);
        for (s = 0; s < o.length; s++) this._map.hasLayer(o[s]) && this._map.removeLayer(o[s]);
        for (s = 0; s < n.length; s++) this._map.hasLayer(n[s]) || this._map.addLayer(n[s]);
        this._handlingClick = !1, this._refocusOnMap()
      },
      _checkDisabledLayers: function() {
        for (var t, i, e = this._layerControlInputs, n = this._map.getZoom(), o = e.length - 1; 0 <= o; o--) t = e[o], i = this._getLayer(t.layerId).layer, t.disabled = void 0 !== i.options.minZoom && n < i.options.minZoom || void 0 !== i.options.maxZoom && n > i.options.maxZoom
      },
      _expandIfNotCollapsed: function() {
        return this._map && !this.options.collapsed && this.expand(), this
      },
      _expand: function() {
        return this.expand()
      },
      _collapse: function() {
        return this.collapse()
      }
    }),
    ie = Qi.extend({
      options: {
        position: "topleft",
        zoomInText: "+",
        zoomInTitle: "Zoom in",
        zoomOutText: "&#x2212;",
        zoomOutTitle: "Zoom out"
      },
      onAdd: function(t) {
        var i = "leaflet-control-zoom",
          e = hi("div", i + " leaflet-bar"),
          n = this.options;
        return this._zoomInButton = this._createButton(n.zoomInText, n.zoomInTitle, i + "-in", e, this._zoomIn), this._zoomOutButton = this._createButton(n.zoomOutText, n.zoomOutTitle, i + "-out", e, this._zoomOut), this._updateDisabled(), t.on("zoomend zoomlevelschange", this._updateDisabled, this), e
      },
      onRemove: function(t) {
        t.off("zoomend zoomlevelschange", this._updateDisabled, this)
      },
      disable: function() {
        return this._disabled = !0, this._updateDisabled(), this
      },
      enable: function() {
        return this._disabled = !1, this._updateDisabled(), this
      },
      _zoomIn: function(t) {
        !this._disabled && this._map._zoom < this._map.getMaxZoom() && this._map.zoomIn(this._map.options.zoomDelta * (t.shiftKey ? 3 : 1))
      },
      _zoomOut: function(t) {
        !this._disabled && this._map._zoom > this._map.getMinZoom() && this._map.zoomOut(this._map.options.zoomDelta * (t.shiftKey ? 3 : 1))
      },
      _createButton: function(t, i, e, n, o) {
        var s = hi("a", e, n);
        return s.innerHTML = t, s.href = "#", s.title = i, s.setAttribute("role", "button"), s.setAttribute("aria-label", i), Ni(s), Ei(s, "click", ji), Ei(s, "click", o, this), Ei(s, "click", this._refocusOnMap, this), s
      },
      _updateDisabled: function() {
        var t = this._map,
          i = "leaflet-disabled";
        mi(this._zoomInButton, i), mi(this._zoomOutButton, i), !this._disabled && t._zoom !== t.getMinZoom() || pi(this._zoomOutButton, i), !this._disabled && t._zoom !== t.getMaxZoom() || pi(this._zoomInButton, i)
      }
    });
  Ji.mergeOptions({
    zoomControl: !0
  }), Ji.addInitHook(function() {
    this.options.zoomControl && (this.zoomControl = new ie, this.addControl(this.zoomControl))
  });
  var ee = Qi.extend({
      options: {
        position: "bottomleft",
        maxWidth: 100,
        metric: !0,
        imperial: !0
      },
      onAdd: function(t) {
        var i = "leaflet-control-scale",
          e = hi("div", i),
          n = this.options;
        return this._addScales(n, i + "-line", e), t.on(n.updateWhenIdle ? "moveend" : "move", this._update, this), t.whenReady(this._update, this), e
      },
      onRemove: function(t) {
        t.off(this.options.updateWhenIdle ? "moveend" : "move", this._update, this)
      },
      _addScales: function(t, i, e) {
        t.metric && (this._mScale = hi("div", i, e)), t.imperial && (this._iScale = hi("div", i, e))
      },
      _update: function() {
        var t = this._map,
          i = t.getSize().y / 2,
          e = t.distance(t.containerPointToLatLng([0, i]), t.containerPointToLatLng([this.options.maxWidth, i]));
        this._updateScales(e)
      },
      _updateScales: function(t) {
        this.options.metric && t && this._updateMetric(t), this.options.imperial && t && this._updateImperial(t)
      },
      _updateMetric: function(t) {
        var i = this._getRoundNum(t),
          e = i < 1e3 ? i + " m" : i / 1e3 + " km";
        this._updateScale(this._mScale, e, i / t)
      },
      _updateImperial: function(t) {
        var i, e, n, o = 3.2808399 * t;
        5280 < o ? (i = o / 5280, e = this._getRoundNum(i), this._updateScale(this._iScale, e + " mi", e / i)) : (n = this._getRoundNum(o), this._updateScale(this._iScale, n + " ft", n / o))
      },
      _updateScale: function(t, i, e) {
        t.style.width = Math.round(this.options.maxWidth * e) + "px", t.innerHTML = i
      },
      _getRoundNum: function(t) {
        var i = Math.pow(10, (Math.floor(t) + "").length - 1),
          e = t / i;
        return i * (e = 10 <= e ? 10 : 5 <= e ? 5 : 3 <= e ? 3 : 2 <= e ? 2 : 1)
      }
    }),
    ne = Qi.extend({
      options: {
        position: "bottomright",
        prefix: '<a href="https://leafletjs.com" title="A JS library for interactive maps">Leaflet</a>'
      },
      initialize: function(t) {
        p(this, t), this._attributions = {}
      },
      onAdd: function(t) {
        for (var i in (t.attributionControl = this)._container = hi("div", "leaflet-control-attribution"), Ni(this._container), t._layers) t._layers[i].getAttribution && this.addAttribution(t._layers[i].getAttribution());
        return this._update(), this._container
      },
      setPrefix: function(t) {
        return this.options.prefix = t, this._update(), this
      },
      addAttribution: function(t) {
        return t && (this._attributions[t] || (this._attributions[t] = 0), this._attributions[t]++, this._update()), this
      },
      removeAttribution: function(t) {
        return t && this._attributions[t] && (this._attributions[t]--, this._update()), this
      },
      _update: function() {
        if (this._map) {
          var t = [];
          for (var i in this._attributions) this._attributions[i] && t.push(i);
          var e = [];
          this.options.prefix && e.push(this.options.prefix), t.length && e.push(t.join(", ")), this._container.innerHTML = e.join(" | ")
        }
      }
    });
  Ji.mergeOptions({
    attributionControl: !0
  }), Ji.addInitHook(function() {
    this.options.attributionControl && (new ne).addTo(this)
  });
  Qi.Layers = te, Qi.Zoom = ie, Qi.Scale = ee, Qi.Attribution = ne, $i.layers = function(t, i, e) {
    return new te(t, i, e)
  }, $i.zoom = function(t) {
    return new ie(t)
  }, $i.scale = function(t) {
    return new ee(t)
  }, $i.attribution = function(t) {
    return new ne(t)
  };
  var oe = Z.extend({
    initialize: function(t) {
      this._map = t
    },
    enable: function() {
      return this._enabled || (this._enabled = !0, this.addHooks()), this
    },
    disable: function() {
      return this._enabled && (this._enabled = !1, this.removeHooks()), this
    },
    enabled: function() {
      return !!this._enabled
    }
  });
  oe.addTo = function(t, i) {
    return t.addHandler(i, this), this
  };
  var se, re = {
      Events: E
    },
    ae = Tt ? "touchstart mousedown" : "mousedown",
    he = {
      mousedown: "mouseup",
      touchstart: "touchend",
      pointerdown: "touchend",
      MSPointerDown: "touchend"
    },
    ue = {
      mousedown: "mousemove",
      touchstart: "touchmove",
      pointerdown: "touchmove",
      MSPointerDown: "touchmove"
    },
    le = k.extend({
      options: {
        clickTolerance: 3
      },
      initialize: function(t, i, e, n) {
        p(this, n), this._element = t, this._dragStartTarget = i || t, this._preventOutline = e
      },
      enable: function() {
        this._enabled || (Ei(this._dragStartTarget, ae, this._onDown, this), this._enabled = !0)
      },
      disable: function() {
        this._enabled && (le._dragging === this && this.finishDrag(), Bi(this._dragStartTarget, ae, this._onDown, this), this._enabled = !1, this._moved = !1)
      },
      _onDown: function(t) {
        if (!t._simulated && this._enabled && (this._moved = !1, !di(this._element, "leaflet-zoom-anim") && !(le._dragging || t.shiftKey || 1 !== t.which && 1 !== t.button && !t.touches || ((le._dragging = this)._preventOutline && zi(this._element), Li(), $t(), this._moving)))) {
          this.fire("down");
          var i = t.touches ? t.touches[0] : t,
            e = Ci(this._element);
          this._startPoint = new B(i.clientX, i.clientY), this._parentScale = Si(e), Ei(document, ue[t.type], this._onMove, this), Ei(document, he[t.type], this._onUp, this)
        }
      },
      _onMove: function(t) {
        if (!t._simulated && this._enabled)
          if (t.touches && 1 < t.touches.length) this._moved = !0;
          else {
            var i = t.touches && 1 === t.touches.length ? t.touches[0] : t,
              e = new B(i.clientX, i.clientY)._subtract(this._startPoint);
            (e.x || e.y) && (Math.abs(e.x) + Math.abs(e.y) < this.options.clickTolerance || (e.x /= this._parentScale.x, e.y /= this._parentScale.y, Di(t), this._moved || (this.fire("dragstart"), this._moved = !0, this._startPos = Pi(this._element).subtract(e), pi(document.body, "leaflet-dragging"), this._lastTarget = t.target || t.srcElement, window.SVGElementInstance && this._lastTarget instanceof SVGElementInstance && (this._lastTarget = this._lastTarget.correspondingUseElement), pi(this._lastTarget, "leaflet-drag-target")), this._newPos = this._startPos.add(e), this._moving = !0, C(this._animRequest), this._lastEvent = t, this._animRequest = M(this._updatePosition, this, !0)))
          }
      },
      _updatePosition: function() {
        var t = {
          originalEvent: this._lastEvent
        };
        this.fire("predrag", t), wi(this._element, this._newPos), this.fire("drag", t)
      },
      _onUp: function(t) {
        !t._simulated && this._enabled && this.finishDrag()
      },
      finishDrag: function() {
        for (var t in mi(document.body, "leaflet-dragging"), this._lastTarget && (mi(this._lastTarget, "leaflet-drag-target"), this._lastTarget = null), ue) Bi(document, ue[t], this._onMove, this), Bi(document, he[t], this._onUp, this);
        Ti(), Qt(), this._moved && this._moving && (C(this._animRequest), this.fire("dragend", {
          distance: this._newPos.distanceTo(this._startPos)
        })), this._moving = !1, le._dragging = !1
      }
    });

  function ce(t, i) {
    if (!i || !t.length) return t.slice();
    var e = i * i;
    return t = function(t, i) {
      var e = t.length,
        n = new(typeof Uint8Array != void 0 + "" ? Uint8Array : Array)(e);
      n[0] = n[e - 1] = 1,
        function t(i, e, n, o, s) {
          var r, a, h, u = 0;
          for (a = o + 1; a <= s - 1; a++) h = fe(i[a], i[o], i[s], !0), u < h && (r = a, u = h);
          n < u && (e[r] = 1, t(i, e, n, o, r), t(i, e, n, r, s))
        }(t, n, i, 0, e - 1);
      var o, s = [];
      for (o = 0; o < e; o++) n[o] && s.push(t[o]);
      return s
    }(t = function(t, i) {
      for (var e = [t[0]], n = 1, o = 0, s = t.length; n < s; n++) r = t[n], a = t[o], void 0, h = a.x - r.x, u = a.y - r.y, i < h * h + u * u && (e.push(t[n]), o = n);
      var r, a, h, u;
      o < s - 1 && e.push(t[s - 1]);
      return e
    }(t, e), e)
  }

  function _e(t, i, e) {
    return Math.sqrt(fe(t, i, e, !0))
  }

  function de(t, i, e, n, o) {
    var s, r, a, h = n ? se : me(t, e),
      u = me(i, e);
    for (se = u;;) {
      if (!(h | u)) return [t, i];
      if (h & u) return !1;
      a = me(r = pe(t, i, s = h || u, e, o), e), s === h ? (t = r, h = a) : (i = r, u = a)
    }
  }

  function pe(t, i, e, n, o) {
    var s, r, a = i.x - t.x,
      h = i.y - t.y,
      u = n.min,
      l = n.max;
    return 8 & e ? (s = t.x + a * (l.y - t.y) / h, r = l.y) : 4 & e ? (s = t.x + a * (u.y - t.y) / h, r = u.y) : 2 & e ? (s = l.x, r = t.y + h * (l.x - t.x) / a) : 1 & e && (s = u.x, r = t.y + h * (u.x - t.x) / a), new B(s, r, o)
  }

  function me(t, i) {
    var e = 0;
    return t.x < i.min.x ? e |= 1 : t.x > i.max.x && (e |= 2), t.y < i.min.y ? e |= 4 : t.y > i.max.y && (e |= 8), e
  }

  function fe(t, i, e, n) {
    var o, s = i.x,
      r = i.y,
      a = e.x - s,
      h = e.y - r,
      u = a * a + h * h;
    return 0 < u && (1 < (o = ((t.x - s) * a + (t.y - r) * h) / u) ? (s = e.x, r = e.y) : 0 < o && (s += a * o, r += h * o)), a = t.x - s, h = t.y - r, n ? a * a + h * h : new B(s, r)
  }

  function ge(t) {
    return !v(t[0]) || "object" != typeof t[0][0] && void 0 !== t[0][0]
  }

  function ve(t) {
    return console.warn("Deprecated use of _flat, please use L.LineUtil.isFlat instead."), ge(t)
  }
  var ye = (Object.freeze || Object)({
    simplify: ce,
    pointToSegmentDistance: _e,
    closestPointOnSegment: function(t, i, e) {
      return fe(t, i, e)
    },
    clipSegment: de,
    _getEdgeIntersection: pe,
    _getBitCode: me,
    _sqClosestPointOnSegment: fe,
    isFlat: ge,
    _flat: ve
  });

  function xe(t, i, e) {
    var n, o, s, r, a, h, u, l, c, _ = [1, 4, 2, 8];
    for (o = 0, u = t.length; o < u; o++) t[o]._code = me(t[o], i);
    for (r = 0; r < 4; r++) {
      for (l = _[r], n = [], o = 0, s = (u = t.length) - 1; o < u; s = o++) a = t[o], h = t[s], a._code & l ? h._code & l || ((c = pe(h, a, l, i, e))._code = me(c, i), n.push(c)) : (h._code & l && ((c = pe(h, a, l, i, e))._code = me(c, i), n.push(c)), n.push(a));
      t = n
    }
    return t
  }
  var we, Pe = (Object.freeze || Object)({
      clipPolygon: xe
    }),
    be = {
      project: function(t) {
        return new B(t.lng, t.lat)
      },
      unproject: function(t) {
        return new j(t.y, t.x)
      },
      bounds: new O([-180, -90], [180, 90])
    },
    Le = {
      R: 6378137,
      R_MINOR: 6356752.314245179,
      bounds: new O([-20037508.34279, -15496570.73972], [20037508.34279, 18764656.23138]),
      project: function(t) {
        var i = Math.PI / 180,
          e = this.R,
          n = t.lat * i,
          o = this.R_MINOR / e,
          s = Math.sqrt(1 - o * o),
          r = s * Math.sin(n),
          a = Math.tan(Math.PI / 4 - n / 2) / Math.pow((1 - r) / (1 + r), s / 2);
        return n = -e * Math.log(Math.max(a, 1e-10)), new B(t.lng * i * e, n)
      },
      unproject: function(t) {
        for (var i, e = 180 / Math.PI, n = this.R, o = this.R_MINOR / n, s = Math.sqrt(1 - o * o), r = Math.exp(-t.y / n), a = Math.PI / 2 - 2 * Math.atan(r), h = 0, u = .1; h < 15 && 1e-7 < Math.abs(u); h++) i = s * Math.sin(a), i = Math.pow((1 - i) / (1 + i), s / 2), a += u = Math.PI / 2 - 2 * Math.atan(r * i) - a;
        return new j(a * e, t.x * e / n)
      }
    },
    Te = (Object.freeze || Object)({
      LonLat: be,
      Mercator: Le,
      SphericalMercator: q
    }),
    ze = h({}, U, {
      code: "EPSG:3395",
      projection: Le,
      transformation: (we = .5 / (Math.PI * Le.R), K(we, .5, -we, .5))
    }),
    Me = h({}, U, {
      code: "EPSG:4326",
      projection: be,
      transformation: K(1 / 180, 1, -1 / 180, .5)
    }),
    Ce = h({}, F, {
      projection: be,
      transformation: K(1, 0, -1, 0),
      scale: function(t) {
        return Math.pow(2, t)
      },
      zoom: function(t) {
        return Math.log(t) / Math.LN2
      },
      distance: function(t, i) {
        var e = i.lng - t.lng,
          n = i.lat - t.lat;
        return Math.sqrt(e * e + n * n)
      },
      infinite: !0
    });
  F.Earth = U, F.EPSG3395 = ze, F.EPSG3857 = X, F.EPSG900913 = J, F.EPSG4326 = Me, F.Simple = Ce;
  var Se = k.extend({
    options: {
      pane: "overlayPane",
      attribution: null,
      bubblingMouseEvents: !0
    },
    addTo: function(t) {
      return t.addLayer(this), this
    },
    remove: function() {
      return this.removeFrom(this._map || this._mapToAdd)
    },
    removeFrom: function(t) {
      return t && t.removeLayer(this), this
    },
    getPane: function(t) {
      return this._map.getPane(t ? this.options[t] || t : this.options.pane)
    },
    addInteractiveTarget: function(t) {
      return this._map._targets[u(t)] = this
    },
    removeInteractiveTarget: function(t) {
      return delete this._map._targets[u(t)], this
    },
    getAttribution: function() {
      return this.options.attribution
    },
    _layerAdd: function(t) {
      var i = t.target;
      if (i.hasLayer(this)) {
        if (this._map = i, this._zoomAnimated = i._zoomAnimated, this.getEvents) {
          var e = this.getEvents();
          i.on(e, this), this.once("remove", function() {
            i.off(e, this)
          }, this)
        }
        this.onAdd(i), this.getAttribution && i.attributionControl && i.attributionControl.addAttribution(this.getAttribution()), this.fire("add"), i.fire("layeradd", {
          layer: this
        })
      }
    }
  });
  Ji.include({
    addLayer: function(t) {
      if (!t._layerAdd) throw new Error("The provided object is not a Layer.");
      var i = u(t);
      return this._layers[i] || ((this._layers[i] = t)._mapToAdd = this, t.beforeAdd && t.beforeAdd(this), this.whenReady(t._layerAdd, t)), this
    },
    removeLayer: function(t) {
      var i = u(t);
      return this._layers[i] && (this._loaded && t.onRemove(this), t.getAttribution && this.attributionControl && this.attributionControl.removeAttribution(t.getAttribution()), delete this._layers[i], this._loaded && (this.fire("layerremove", {
        layer: t
      }), t.fire("remove")), t._map = t._mapToAdd = null), this
    },
    hasLayer: function(t) {
      return !!t && u(t) in this._layers
    },
    eachLayer: function(t, i) {
      for (var e in this._layers) t.call(i, this._layers[e]);
      return this
    },
    _addLayers: function(t) {
      for (var i = 0, e = (t = t ? v(t) ? t : [t] : []).length; i < e; i++) this.addLayer(t[i])
    },
    _addZoomLimit: function(t) {
      !isNaN(t.options.maxZoom) && isNaN(t.options.minZoom) || (this._zoomBoundLayers[u(t)] = t, this._updateZoomLevels())
    },
    _removeZoomLimit: function(t) {
      var i = u(t);
      this._zoomBoundLayers[i] && (delete this._zoomBoundLayers[i], this._updateZoomLevels())
    },
    _updateZoomLevels: function() {
      var t = 1 / 0,
        i = -1 / 0,
        e = this._getZoomSpan();
      for (var n in this._zoomBoundLayers) {
        var o = this._zoomBoundLayers[n].options;
        t = void 0 === o.minZoom ? t : Math.min(t, o.minZoom), i = void 0 === o.maxZoom ? i : Math.max(i, o.maxZoom)
      }
      this._layersMaxZoom = i === -1 / 0 ? void 0 : i, this._layersMinZoom = t === 1 / 0 ? void 0 : t, e !== this._getZoomSpan() && this.fire("zoomlevelschange"), void 0 === this.options.maxZoom && this._layersMaxZoom && this.getZoom() > this._layersMaxZoom && this.setZoom(this._layersMaxZoom), void 0 === this.options.minZoom && this._layersMinZoom && this.getZoom() < this._layersMinZoom && this.setZoom(this._layersMinZoom)
    }
  });
  var Ze = Se.extend({
      initialize: function(t, i) {
        var e, n;
        if (p(this, i), this._layers = {}, t)
          for (e = 0, n = t.length; e < n; e++) this.addLayer(t[e])
      },
      addLayer: function(t) {
        var i = this.getLayerId(t);
        return this._layers[i] = t, this._map && this._map.addLayer(t), this
      },
      removeLayer: function(t) {
        var i = t in this._layers ? t : this.getLayerId(t);
        return this._map && this._layers[i] && this._map.removeLayer(this._layers[i]), delete this._layers[i], this
      },
      hasLayer: function(t) {
        return !!t && (t in this._layers || this.getLayerId(t) in this._layers)
      },
      clearLayers: function() {
        return this.eachLayer(this.removeLayer, this)
      },
      invoke: function(t) {
        var i, e, n = Array.prototype.slice.call(arguments, 1);
        for (i in this._layers)(e = this._layers[i])[t] && e[t].apply(e, n);
        return this
      },
      onAdd: function(t) {
        this.eachLayer(t.addLayer, t)
      },
      onRemove: function(t) {
        this.eachLayer(t.removeLayer, t)
      },
      eachLayer: function(t, i) {
        for (var e in this._layers) t.call(i, this._layers[e]);
        return this
      },
      getLayer: function(t) {
        return this._layers[t]
      },
      getLayers: function() {
        var t = [];
        return this.eachLayer(t.push, t), t
      },
      setZIndex: function(t) {
        return this.invoke("setZIndex", t)
      },
      getLayerId: function(t) {
        return u(t)
      }
    }),
    Ee = Ze.extend({
      addLayer: function(t) {
        return this.hasLayer(t) ? this : (t.addEventParent(this), Ze.prototype.addLayer.call(this, t), this.fire("layeradd", {
          layer: t
        }))
      },
      removeLayer: function(t) {
        return this.hasLayer(t) ? (t in this._layers && (t = this._layers[t]), t.removeEventParent(this), Ze.prototype.removeLayer.call(this, t), this.fire("layerremove", {
          layer: t
        })) : this
      },
      setStyle: function(t) {
        return this.invoke("setStyle", t)
      },
      bringToFront: function() {
        return this.invoke("bringToFront")
      },
      bringToBack: function() {
        return this.invoke("bringToBack")
      },
      getBounds: function() {
        var t = new N;
        for (var i in this._layers) {
          var e = this._layers[i];
          t.extend(e.getBounds ? e.getBounds() : e.getLatLng())
        }
        return t
      }
    }),
    ke = Z.extend({
      options: {
        popupAnchor: [0, 0],
        tooltipAnchor: [0, 0]
      },
      initialize: function(t) {
        p(this, t)
      },
      createIcon: function(t) {
        return this._createIcon("icon", t)
      },
      createShadow: function(t) {
        return this._createIcon("shadow", t)
      },
      _createIcon: function(t, i) {
        var e = this._getIconUrl(t);
        if (!e) {
          if ("icon" === t) throw new Error("iconUrl not set in Icon options (see the docs).");
          return null
        }
        var n = this._createImg(e, i && "IMG" === i.tagName ? i : null);
        return this._setIconStyles(n, t), n
      },
      _setIconStyles: function(t, i) {
        var e = this.options,
          n = e[i + "Size"];
        "number" == typeof n && (n = [n, n]);
        var o = I(n),
          s = I("shadow" === i && e.shadowAnchor || e.iconAnchor || o && o.divideBy(2, !0));
        t.className = "leaflet-marker-" + i + " " + (e.className || ""), s && (t.style.marginLeft = -s.x + "px", t.style.marginTop = -s.y + "px"), o && (t.style.width = o.x + "px", t.style.height = o.y + "px")
      },
      _createImg: function(t, i) {
        return (i = i || document.createElement("img")).src = t, i
      },
      _getIconUrl: function(t) {
        return Ct && this.options[t + "RetinaUrl"] || this.options[t + "Url"]
      }
    });
  var Be = ke.extend({
      options: {
        iconUrl: "marker-icon.png",
        iconRetinaUrl: "marker-icon-2x.png",
        shadowUrl: "marker-shadow.png",
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        tooltipAnchor: [16, -28],
        shadowSize: [41, 41]
      },
      _getIconUrl: function(t) {
        return Be.imagePath || (Be.imagePath = this._detectIconPath()), (this.options.imagePath || Be.imagePath) + ke.prototype._getIconUrl.call(this, t)
      },
      _detectIconPath: function() {
        var t = hi("div", "leaflet-default-icon-path", document.body),
          i = ai(t, "background-image") || ai(t, "backgroundImage");
        return document.body.removeChild(t), i = null === i || 0 !== i.indexOf("url") ? "" : i.replace(/^url\(["']?/, "").replace(/marker-icon\.png["']?\)$/, "")
      }
    }),
    Ae = oe.extend({
      initialize: function(t) {
        this._marker = t
      },
      addHooks: function() {
        var t = this._marker._icon;
        this._draggable || (this._draggable = new le(t, t, !0)), this._draggable.on({
          dragstart: this._onDragStart,
          predrag: this._onPreDrag,
          drag: this._onDrag,
          dragend: this._onDragEnd
        }, this).enable(), pi(t, "leaflet-marker-draggable")
      },
      removeHooks: function() {
        this._draggable.off({
          dragstart: this._onDragStart,
          predrag: this._onPreDrag,
          drag: this._onDrag,
          dragend: this._onDragEnd
        }, this).disable(), this._marker._icon && mi(this._marker._icon, "leaflet-marker-draggable")
      },
      moved: function() {
        return this._draggable && this._draggable._moved
      },
      _adjustPan: function(t) {
        var i = this._marker,
          e = i._map,
          n = this._marker.options.autoPanSpeed,
          o = this._marker.options.autoPanPadding,
          s = Pi(i._icon),
          r = e.getPixelBounds(),
          a = e.getPixelOrigin(),
          h = R(r.min._subtract(a).add(o), r.max._subtract(a).subtract(o));
        if (!h.contains(s)) {
          var u = I((Math.max(h.max.x, s.x) - h.max.x) / (r.max.x - h.max.x) - (Math.min(h.min.x, s.x) - h.min.x) / (r.min.x - h.min.x), (Math.max(h.max.y, s.y) - h.max.y) / (r.max.y - h.max.y) - (Math.min(h.min.y, s.y) - h.min.y) / (r.min.y - h.min.y)).multiplyBy(n);
          e.panBy(u, {
            animate: !1
          }), this._draggable._newPos._add(u), this._draggable._startPos._add(u), wi(i._icon, this._draggable._newPos), this._onDrag(t), this._panRequest = M(this._adjustPan.bind(this, t))
        }
      },
      _onDragStart: function() {
        this._oldLatLng = this._marker.getLatLng(), this._marker.closePopup().fire("movestart").fire("dragstart")
      },
      _onPreDrag: function(t) {
        this._marker.options.autoPan && (C(this._panRequest), this._panRequest = M(this._adjustPan.bind(this, t)))
      },
      _onDrag: function(t) {
        var i = this._marker,
          e = i._shadow,
          n = Pi(i._icon),
          o = i._map.layerPointToLatLng(n);
        e && wi(e, n), i._latlng = o, t.latlng = o, t.oldLatLng = this._oldLatLng, i.fire("move", t).fire("drag", t)
      },
      _onDragEnd: function(t) {
        C(this._panRequest), delete this._oldLatLng, this._marker.fire("moveend").fire("dragend", t)
      }
    }),
    Ie = Se.extend({
      options: {
        icon: new Be,
        interactive: !0,
        keyboard: !0,
        title: "",
        alt: "",
        zIndexOffset: 0,
        opacity: 1,
        riseOnHover: !1,
        riseOffset: 250,
        pane: "markerPane",
        shadowPane: "shadowPane",
        bubblingMouseEvents: !1,
        draggable: !1,
        autoPan: !1,
        autoPanPadding: [50, 50],
        autoPanSpeed: 10
      },
      initialize: function(t, i) {
        p(this, i), this._latlng = W(t)
      },
      onAdd: function(t) {
        this._zoomAnimated = this._zoomAnimated && t.options.markerZoomAnimation, this._zoomAnimated && t.on("zoomanim", this._animateZoom, this), this._initIcon(), this.update()
      },
      onRemove: function(t) {
        this.dragging && this.dragging.enabled() && (this.options.draggable = !0, this.dragging.removeHooks()), delete this.dragging, this._zoomAnimated && t.off("zoomanim", this._animateZoom, this), this._removeIcon(), this._removeShadow()
      },
      getEvents: function() {
        return {
          zoom: this.update,
          viewreset: this.update
        }
      },
      getLatLng: function() {
        return this._latlng
      },
      setLatLng: function(t) {
        var i = this._latlng;
        return this._latlng = W(t), this.update(), this.fire("move", {
          oldLatLng: i,
          latlng: this._latlng
        })
      },
      setZIndexOffset: function(t) {
        return this.options.zIndexOffset = t, this.update()
      },
      getIcon: function() {
        return this.options.icon
      },
      setIcon: function(t) {
        return this.options.icon = t, this._map && (this._initIcon(), this.update()), this._popup && this.bindPopup(this._popup, this._popup.options), this
      },
      getElement: function() {
        return this._icon
      },
      update: function() {
        if (this._icon && this._map) {
          var t = this._map.latLngToLayerPoint(this._latlng).round();
          this._setPos(t)
        }
        return this
      },
      _initIcon: function() {
        var t = this.options,
          i = "leaflet-zoom-" + (this._zoomAnimated ? "animated" : "hide"),
          e = t.icon.createIcon(this._icon),
          n = !1;
        e !== this._icon && (this._icon && this._removeIcon(), n = !0, t.title && (e.title = t.title), "IMG" === e.tagName && (e.alt = t.alt || "")), pi(e, i), t.keyboard && (e.tabIndex = "0"), this._icon = e, t.riseOnHover && this.on({
          mouseover: this._bringToFront,
          mouseout: this._resetZIndex
        });
        var o = t.icon.createShadow(this._shadow),
          s = !1;
        o !== this._shadow && (this._removeShadow(), s = !0), o && (pi(o, i), o.alt = ""), this._shadow = o, t.opacity < 1 && this._updateOpacity(), n && this.getPane().appendChild(this._icon), this._initInteraction(), o && s && this.getPane(t.shadowPane).appendChild(this._shadow)
      },
      _removeIcon: function() {
        this.options.riseOnHover && this.off({
          mouseover: this._bringToFront,
          mouseout: this._resetZIndex
        }), ui(this._icon), this.removeInteractiveTarget(this._icon), this._icon = null
      },
      _removeShadow: function() {
        this._shadow && ui(this._shadow), this._shadow = null
      },
      _setPos: function(t) {
        wi(this._icon, t), this._shadow && wi(this._shadow, t), this._zIndex = t.y + this.options.zIndexOffset, this._resetZIndex()
      },
      _updateZIndex: function(t) {
        this._icon.style.zIndex = this._zIndex + t
      },
      _animateZoom: function(t) {
        var i = this._map._latLngToNewLayerPoint(this._latlng, t.zoom, t.center).round();
        this._setPos(i)
      },
      _initInteraction: function() {
        if (this.options.interactive && (pi(this._icon, "leaflet-interactive"), this.addInteractiveTarget(this._icon), Ae)) {
          var t = this.options.draggable;
          this.dragging && (t = this.dragging.enabled(), this.dragging.disable()), this.dragging = new Ae(this), t && this.dragging.enable()
        }
      },
      setOpacity: function(t) {
        return this.options.opacity = t, this._map && this._updateOpacity(), this
      },
      _updateOpacity: function() {
        var t = this.options.opacity;
        this._icon && vi(this._icon, t), this._shadow && vi(this._shadow, t)
      },
      _bringToFront: function() {
        this._updateZIndex(this.options.riseOffset)
      },
      _resetZIndex: function() {
        this._updateZIndex(0)
      },
      _getPopupAnchor: function() {
        return this.options.icon.options.popupAnchor
      },
      _getTooltipAnchor: function() {
        return this.options.icon.options.tooltipAnchor
      }
    });
  var Oe = Se.extend({
      options: {
        stroke: !0,
        color: "#3388ff",
        weight: 3,
        opacity: 1,
        lineCap: "round",
        lineJoin: "round",
        dashArray: null,
        dashOffset: null,
        fill: !1,
        fillColor: null,
        fillOpacity: .2,
        fillRule: "evenodd",
        interactive: !0,
        bubblingMouseEvents: !0
      },
      beforeAdd: function(t) {
        this._renderer = t.getRenderer(this)
      },
      onAdd: function() {
        this._renderer._initPath(this), this._reset(), this._renderer._addPath(this)
      },
      onRemove: function() {
        this._renderer._removePath(this)
      },
      redraw: function() {
        return this._map && this._renderer._updatePath(this), this
      },
      setStyle: function(t) {
        return p(this, t), this._renderer && (this._renderer._updateStyle(this), this.options.stroke && t.hasOwnProperty("weight") && this._updateBounds()), this
      },
      bringToFront: function() {
        return this._renderer && this._renderer._bringToFront(this), this
      },
      bringToBack: function() {
        return this._renderer && this._renderer._bringToBack(this), this
      },
      getElement: function() {
        return this._path
      },
      _reset: function() {
        this._project(), this._update()
      },
      _clickTolerance: function() {
        return (this.options.stroke ? this.options.weight / 2 : 0) + this._renderer.options.tolerance
      }
    }),
    Re = Oe.extend({
      options: {
        fill: !0,
        radius: 10
      },
      initialize: function(t, i) {
        p(this, i), this._latlng = W(t), this._radius = this.options.radius
      },
      setLatLng: function(t) {
        return this._latlng = W(t), this.redraw(), this.fire("move", {
          latlng: this._latlng
        })
      },
      getLatLng: function() {
        return this._latlng
      },
      setRadius: function(t) {
        return this.options.radius = this._radius = t, this.redraw()
      },
      getRadius: function() {
        return this._radius
      },
      setStyle: function(t) {
        var i = t && t.radius || this._radius;
        return Oe.prototype.setStyle.call(this, t), this.setRadius(i), this
      },
      _project: function() {
        this._point = this._map.latLngToLayerPoint(this._latlng), this._updateBounds()
      },
      _updateBounds: function() {
        var t = this._radius,
          i = this._radiusY || t,
          e = this._clickTolerance(),
          n = [t + e, i + e];
        this._pxBounds = new O(this._point.subtract(n), this._point.add(n))
      },
      _update: function() {
        this._map && this._updatePath()
      },
      _updatePath: function() {
        this._renderer._updateCircle(this)
      },
      _empty: function() {
        return this._radius && !this._renderer._bounds.intersects(this._pxBounds)
      },
      _containsPoint: function(t) {
        return t.distanceTo(this._point) <= this._radius + this._clickTolerance()
      }
    });
  var Ne = Re.extend({
    initialize: function(t, i, e) {
      if ("number" == typeof i && (i = h({}, e, {
          radius: i
        })), p(this, i), this._latlng = W(t), isNaN(this.options.radius)) throw new Error("Circle radius cannot be NaN");
      this._mRadius = this.options.radius
    },
    setRadius: function(t) {
      return this._mRadius = t, this.redraw()
    },
    getRadius: function() {
      return this._mRadius
    },
    getBounds: function() {
      var t = [this._radius, this._radiusY || this._radius];
      return new N(this._map.layerPointToLatLng(this._point.subtract(t)), this._map.layerPointToLatLng(this._point.add(t)))
    },
    setStyle: Oe.prototype.setStyle,
    _project: function() {
      var t = this._latlng.lng,
        i = this._latlng.lat,
        e = this._map,
        n = e.options.crs;
      if (n.distance === U.distance) {
        var o = Math.PI / 180,
          s = this._mRadius / U.R / o,
          r = e.project([i + s, t]),
          a = e.project([i - s, t]),
          h = r.add(a).divideBy(2),
          u = e.unproject(h).lat,
          l = Math.acos((Math.cos(s * o) - Math.sin(i * o) * Math.sin(u * o)) / (Math.cos(i * o) * Math.cos(u * o))) / o;
        !isNaN(l) && 0 !== l || (l = s / Math.cos(Math.PI / 180 * i)), this._point = h.subtract(e.getPixelOrigin()), this._radius = isNaN(l) ? 0 : h.x - e.project([u, t - l]).x, this._radiusY = h.y - r.y
      } else {
        var c = n.unproject(n.project(this._latlng).subtract([this._mRadius, 0]));
        this._point = e.latLngToLayerPoint(this._latlng), this._radius = this._point.x - e.latLngToLayerPoint(c).x
      }
      this._updateBounds()
    }
  });
  var De = Oe.extend({
    options: {
      smoothFactor: 1,
      noClip: !1
    },
    initialize: function(t, i) {
      p(this, i), this._setLatLngs(t)
    },
    getLatLngs: function() {
      return this._latlngs
    },
    setLatLngs: function(t) {
      return this._setLatLngs(t), this.redraw()
    },
    isEmpty: function() {
      return !this._latlngs.length
    },
    closestLayerPoint: function(t) {
      for (var i, e, n = 1 / 0, o = null, s = fe, r = 0, a = this._parts.length; r < a; r++)
        for (var h = this._parts[r], u = 1, l = h.length; u < l; u++) {
          var c = s(t, i = h[u - 1], e = h[u], !0);
          c < n && (n = c, o = s(t, i, e))
        }
      return o && (o.distance = Math.sqrt(n)), o
    },
    getCenter: function() {
      if (!this._map) throw new Error("Must add layer to map before using getCenter()");
      var t, i, e, n, o, s, r, a = this._rings[0],
        h = a.length;
      if (!h) return null;
      for (i = t = 0; t < h - 1; t++) i += a[t].distanceTo(a[t + 1]) / 2;
      if (0 === i) return this._map.layerPointToLatLng(a[0]);
      for (n = t = 0; t < h - 1; t++)
        if (o = a[t], s = a[t + 1], i < (n += e = o.distanceTo(s))) return r = (n - i) / e, this._map.layerPointToLatLng([s.x - r * (s.x - o.x), s.y - r * (s.y - o.y)])
    },
    getBounds: function() {
      return this._bounds
    },
    addLatLng: function(t, i) {
      return i = i || this._defaultShape(), t = W(t), i.push(t), this._bounds.extend(t), this.redraw()
    },
    _setLatLngs: function(t) {
      this._bounds = new N, this._latlngs = this._convertLatLngs(t)
    },
    _defaultShape: function() {
      return ge(this._latlngs) ? this._latlngs : this._latlngs[0]
    },
    _convertLatLngs: function(t) {
      for (var i = [], e = ge(t), n = 0, o = t.length; n < o; n++) e ? (i[n] = W(t[n]), this._bounds.extend(i[n])) : i[n] = this._convertLatLngs(t[n]);
      return i
    },
    _project: function() {
      var t = new O;
      this._rings = [], this._projectLatlngs(this._latlngs, this._rings, t), this._bounds.isValid() && t.isValid() && (this._rawPxBounds = t, this._updateBounds())
    },
    _updateBounds: function() {
      var t = this._clickTolerance(),
        i = new B(t, t);
      this._pxBounds = new O([this._rawPxBounds.min.subtract(i), this._rawPxBounds.max.add(i)])
    },
    _projectLatlngs: function(t, i, e) {
      var n, o, s = t[0] instanceof j,
        r = t.length;
      if (s) {
        for (o = [], n = 0; n < r; n++) o[n] = this._map.latLngToLayerPoint(t[n]), e.extend(o[n]);
        i.push(o)
      } else
        for (n = 0; n < r; n++) this._projectLatlngs(t[n], i, e)
    },
    _clipPoints: function() {
      var t = this._renderer._bounds;
      if (this._parts = [], this._pxBounds && this._pxBounds.intersects(t))
        if (this.options.noClip) this._parts = this._rings;
        else {
          var i, e, n, o, s, r, a, h = this._parts;
          for (n = i = 0, o = this._rings.length; i < o; i++)
            for (e = 0, s = (a = this._rings[i]).length; e < s - 1; e++)(r = de(a[e], a[e + 1], t, e, !0)) && (h[n] = h[n] || [], h[n].push(r[0]), r[1] === a[e + 1] && e !== s - 2 || (h[n].push(r[1]), n++))
        }
    },
    _simplifyPoints: function() {
      for (var t = this._parts, i = this.options.smoothFactor, e = 0, n = t.length; e < n; e++) t[e] = ce(t[e], i)
    },
    _update: function() {
      this._map && (this._clipPoints(), this._simplifyPoints(), this._updatePath())
    },
    _updatePath: function() {
      this._renderer._updatePoly(this)
    },
    _containsPoint: function(t, i) {
      var e, n, o, s, r, a, h = this._clickTolerance();
      if (!this._pxBounds || !this._pxBounds.contains(t)) return !1;
      for (e = 0, s = this._parts.length; e < s; e++)
        for (n = 0, o = (r = (a = this._parts[e]).length) - 1; n < r; o = n++)
          if ((i || 0 !== n) && _e(t, a[o], a[n]) <= h) return !0;
      return !1
    }
  });
  De._flat = ve;
  var je = De.extend({
    options: {
      fill: !0
    },
    isEmpty: function() {
      return !this._latlngs.length || !this._latlngs[0].length
    },
    getCenter: function() {
      if (!this._map) throw new Error("Must add layer to map before using getCenter()");
      var t, i, e, n, o, s, r, a, h, u = this._rings[0],
        l = u.length;
      if (!l) return null;
      for (s = r = a = 0, t = 0, i = l - 1; t < l; i = t++) e = u[t], n = u[i], o = e.y * n.x - n.y * e.x, r += (e.x + n.x) * o, a += (e.y + n.y) * o, s += 3 * o;
      return h = 0 === s ? u[0] : [r / s, a / s], this._map.layerPointToLatLng(h)
    },
    _convertLatLngs: function(t) {
      var i = De.prototype._convertLatLngs.call(this, t),
        e = i.length;
      return 2 <= e && i[0] instanceof j && i[0].equals(i[e - 1]) && i.pop(), i
    },
    _setLatLngs: function(t) {
      De.prototype._setLatLngs.call(this, t), ge(this._latlngs) && (this._latlngs = [this._latlngs])
    },
    _defaultShape: function() {
      return ge(this._latlngs[0]) ? this._latlngs[0] : this._latlngs[0][0]
    },
    _clipPoints: function() {
      var t = this._renderer._bounds,
        i = this.options.weight,
        e = new B(i, i);
      if (t = new O(t.min.subtract(e), t.max.add(e)), this._parts = [], this._pxBounds && this._pxBounds.intersects(t))
        if (this.options.noClip) this._parts = this._rings;
        else
          for (var n, o = 0, s = this._rings.length; o < s; o++)(n = xe(this._rings[o], t, !0)).length && this._parts.push(n)
    },
    _updatePath: function() {
      this._renderer._updatePoly(this, !0)
    },
    _containsPoint: function(t) {
      var i, e, n, o, s, r, a, h, u = !1;
      if (!this._pxBounds || !this._pxBounds.contains(t)) return !1;
      for (o = 0, a = this._parts.length; o < a; o++)
        for (s = 0, r = (h = (i = this._parts[o]).length) - 1; s < h; r = s++) e = i[s], n = i[r], e.y > t.y != n.y > t.y && t.x < (n.x - e.x) * (t.y - e.y) / (n.y - e.y) + e.x && (u = !u);
      return u || De.prototype._containsPoint.call(this, t, !0)
    }
  });
  var We = Ee.extend({
    initialize: function(t, i) {
      p(this, i), this._layers = {}, t && this.addData(t)
    },
    addData: function(t) {
      var i, e, n, o = v(t) ? t : t.features;
      if (o) {
        for (i = 0, e = o.length; i < e; i++)((n = o[i]).geometries || n.geometry || n.features || n.coordinates) && this.addData(n);
        return this
      }
      var s = this.options;
      if (s.filter && !s.filter(t)) return this;
      var r = He(t, s);
      return r ? (r.feature = Ke(t), r.defaultOptions = r.options, this.resetStyle(r), s.onEachFeature && s.onEachFeature(t, r), this.addLayer(r)) : this
    },
    resetStyle: function(t) {
      return t.options = h({}, t.defaultOptions), this._setLayerStyle(t, this.options.style), this
    },
    setStyle: function(i) {
      return this.eachLayer(function(t) {
        this._setLayerStyle(t, i)
      }, this)
    },
    _setLayerStyle: function(t, i) {
      t.setStyle && ("function" == typeof i && (i = i(t.feature)), t.setStyle(i))
    }
  });

  function He(t, i) {
    var e, n, o, s, r = "Feature" === t.type ? t.geometry : t,
      a = r ? r.coordinates : null,
      h = [],
      u = i && i.pointToLayer,
      l = i && i.coordsToLatLng || Fe;
    if (!a && !r) return null;
    switch (r.type) {
      case "Point":
        return e = l(a), u ? u(t, e) : new Ie(e);
      case "MultiPoint":
        for (o = 0, s = a.length; o < s; o++) e = l(a[o]), h.push(u ? u(t, e) : new Ie(e));
        return new Ee(h);
      case "LineString":
      case "MultiLineString":
        return n = Ue(a, "LineString" === r.type ? 0 : 1, l), new De(n, i);
      case "Polygon":
      case "MultiPolygon":
        return n = Ue(a, "Polygon" === r.type ? 1 : 2, l), new je(n, i);
      case "GeometryCollection":
        for (o = 0, s = r.geometries.length; o < s; o++) {
          var c = He({
            geometry: r.geometries[o],
            type: "Feature",
            properties: t.properties
          }, i);
          c && h.push(c)
        }
        return new Ee(h);
      default:
        throw new Error("Invalid GeoJSON object.")
    }
  }

  function Fe(t) {
    return new j(t[1], t[0], t[2])
  }

  function Ue(t, i, e) {
    for (var n, o = [], s = 0, r = t.length; s < r; s++) n = i ? Ue(t[s], i - 1, e) : (e || Fe)(t[s]), o.push(n);
    return o
  }

  function Ve(t, i) {
    return i = "number" == typeof i ? i : 6, void 0 !== t.alt ? [c(t.lng, i), c(t.lat, i), c(t.alt, i)] : [c(t.lng, i), c(t.lat, i)]
  }

  function qe(t, i, e, n) {
    for (var o = [], s = 0, r = t.length; s < r; s++) o.push(i ? qe(t[s], i - 1, e, n) : Ve(t[s], n));
    return !i && e && o.push(o[0]), o
  }

  function Ge(t, i) {
    return t.feature ? h({}, t.feature, {
      geometry: i
    }) : Ke(i)
  }

  function Ke(t) {
    return "Feature" === t.type || "FeatureCollection" === t.type ? t : {
      type: "Feature",
      properties: {},
      geometry: t
    }
  }
  var Ye = {
    toGeoJSON: function(t) {
      return Ge(this, {
        type: "Point",
        coordinates: Ve(this.getLatLng(), t)
      })
    }
  };

  function Xe(t, i) {
    return new We(t, i)
  }
  Ie.include(Ye), Ne.include(Ye), Re.include(Ye), De.include({
    toGeoJSON: function(t) {
      var i = !ge(this._latlngs);
      return Ge(this, {
        type: (i ? "Multi" : "") + "LineString",
        coordinates: qe(this._latlngs, i ? 1 : 0, !1, t)
      })
    }
  }), je.include({
    toGeoJSON: function(t) {
      var i = !ge(this._latlngs),
        e = i && !ge(this._latlngs[0]),
        n = qe(this._latlngs, e ? 2 : i ? 1 : 0, !0, t);
      return i || (n = [n]), Ge(this, {
        type: (e ? "Multi" : "") + "Polygon",
        coordinates: n
      })
    }
  }), Ze.include({
    toMultiPoint: function(i) {
      var e = [];
      return this.eachLayer(function(t) {
        e.push(t.toGeoJSON(i).geometry.coordinates)
      }), Ge(this, {
        type: "MultiPoint",
        coordinates: e
      })
    },
    toGeoJSON: function(n) {
      var t = this.feature && this.feature.geometry && this.feature.geometry.type;
      if ("MultiPoint" === t) return this.toMultiPoint(n);
      var o = "GeometryCollection" === t,
        s = [];
      return this.eachLayer(function(t) {
        if (t.toGeoJSON) {
          var i = t.toGeoJSON(n);
          if (o) s.push(i.geometry);
          else {
            var e = Ke(i);
            "FeatureCollection" === e.type ? s.push.apply(s, e.features) : s.push(e)
          }
        }
      }), o ? Ge(this, {
        geometries: s,
        type: "GeometryCollection"
      }) : {
        type: "FeatureCollection",
        features: s
      }
    }
  });
  var Je = Xe,
    $e = Se.extend({
      options: {
        opacity: 1,
        alt: "",
        interactive: !1,
        crossOrigin: !1,
        errorOverlayUrl: "",
        zIndex: 1,
        className: ""
      },
      initialize: function(t, i, e) {
        this._url = t, this._bounds = D(i), p(this, e)
      },
      onAdd: function() {
        this._image || (this._initImage(), this.options.opacity < 1 && this._updateOpacity()), this.options.interactive && (pi(this._image, "leaflet-interactive"), this.addInteractiveTarget(this._image)), this.getPane().appendChild(this._image), this._reset()
      },
      onRemove: function() {
        ui(this._image), this.options.interactive && this.removeInteractiveTarget(this._image)
      },
      setOpacity: function(t) {
        return this.options.opacity = t, this._image && this._updateOpacity(), this
      },
      setStyle: function(t) {
        return t.opacity && this.setOpacity(t.opacity), this
      },
      bringToFront: function() {
        return this._map && ci(this._image), this
      },
      bringToBack: function() {
        return this._map && _i(this._image), this
      },
      setUrl: function(t) {
        return this._url = t, this._image && (this._image.src = t), this
      },
      setBounds: function(t) {
        return this._bounds = D(t), this._map && this._reset(), this
      },
      getEvents: function() {
        var t = {
          zoom: this._reset,
          viewreset: this._reset
        };
        return this._zoomAnimated && (t.zoomanim = this._animateZoom), t
      },
      setZIndex: function(t) {
        return this.options.zIndex = t, this._updateZIndex(), this
      },
      getBounds: function() {
        return this._bounds
      },
      getElement: function() {
        return this._image
      },
      _initImage: function() {
        var t = "IMG" === this._url.tagName,
          i = this._image = t ? this._url : hi("img");
        pi(i, "leaflet-image-layer"), this._zoomAnimated && pi(i, "leaflet-zoom-animated"), this.options.className && pi(i, this.options.className), i.onselectstart = l, i.onmousemove = l, i.onload = a(this.fire, this, "load"), i.onerror = a(this._overlayOnError, this, "error"), !this.options.crossOrigin && "" !== this.options.crossOrigin || (i.crossOrigin = !0 === this.options.crossOrigin ? "" : this.options.crossOrigin), this.options.zIndex && this._updateZIndex(), t ? this._url = i.src : (i.src = this._url, i.alt = this.options.alt)
      },
      _animateZoom: function(t) {
        var i = this._map.getZoomScale(t.zoom),
          e = this._map._latLngBoundsToNewLayerBounds(this._bounds, t.zoom, t.center).min;
        xi(this._image, e, i)
      },
      _reset: function() {
        var t = this._image,
          i = new O(this._map.latLngToLayerPoint(this._bounds.getNorthWest()), this._map.latLngToLayerPoint(this._bounds.getSouthEast())),
          e = i.getSize();
        wi(t, i.min), t.style.width = e.x + "px", t.style.height = e.y + "px"
      },
      _updateOpacity: function() {
        vi(this._image, this.options.opacity)
      },
      _updateZIndex: function() {
        this._image && void 0 !== this.options.zIndex && null !== this.options.zIndex && (this._image.style.zIndex = this.options.zIndex)
      },
      _overlayOnError: function() {
        this.fire("error");
        var t = this.options.errorOverlayUrl;
        t && this._url !== t && (this._url = t, this._image.src = t)
      }
    }),
    Qe = $e.extend({
      options: {
        autoplay: !0,
        loop: !0,
        keepAspectRatio: !0
      },
      _initImage: function() {
        var t = "VIDEO" === this._url.tagName,
          i = this._image = t ? this._url : hi("video");
        if (pi(i, "leaflet-image-layer"), this._zoomAnimated && pi(i, "leaflet-zoom-animated"), i.onselectstart = l, i.onmousemove = l, i.onloadeddata = a(this.fire, this, "load"), t) {
          for (var e = i.getElementsByTagName("source"), n = [], o = 0; o < e.length; o++) n.push(e[o].src);
          this._url = 0 < e.length ? n : [i.src]
        } else {
          v(this._url) || (this._url = [this._url]), !this.options.keepAspectRatio && i.style.hasOwnProperty("objectFit") && (i.style.objectFit = "fill"), i.autoplay = !!this.options.autoplay, i.loop = !!this.options.loop;
          for (var s = 0; s < this._url.length; s++) {
            var r = hi("source");
            r.src = this._url[s], i.appendChild(r)
          }
        }
      }
    });
  var tn = $e.extend({
    _initImage: function() {
      var t = this._image = this._url;
      pi(t, "leaflet-image-layer"), this._zoomAnimated && pi(t, "leaflet-zoom-animated"), t.onselectstart = l, t.onmousemove = l
    }
  });
  var en = Se.extend({
      options: {
        offset: [0, 7],
        className: "",
        pane: "popupPane"
      },
      initialize: function(t, i) {
        p(this, t), this._source = i
      },
      onAdd: function(t) {
        this._zoomAnimated = t._zoomAnimated, this._container || this._initLayout(), t._fadeAnimated && vi(this._container, 0), clearTimeout(this._removeTimeout), this.getPane().appendChild(this._container), this.update(), t._fadeAnimated && vi(this._container, 1), this.bringToFront()
      },
      onRemove: function(t) {
        t._fadeAnimated ? (vi(this._container, 0), this._removeTimeout = setTimeout(a(ui, void 0, this._container), 200)) : ui(this._container)
      },
      getLatLng: function() {
        return this._latlng
      },
      setLatLng: function(t) {
        return this._latlng = W(t), this._map && (this._updatePosition(), this._adjustPan()), this
      },
      getContent: function() {
        return this._content
      },
      setContent: function(t) {
        return this._content = t, this.update(), this
      },
      getElement: function() {
        return this._container
      },
      update: function() {
        this._map && (this._container.style.visibility = "hidden", this._updateContent(), this._updateLayout(), this._updatePosition(), this._container.style.visibility = "", this._adjustPan())
      },
      getEvents: function() {
        var t = {
          zoom: this._updatePosition,
          viewreset: this._updatePosition
        };
        return this._zoomAnimated && (t.zoomanim = this._animateZoom), t
      },
      isOpen: function() {
        return !!this._map && this._map.hasLayer(this)
      },
      bringToFront: function() {
        return this._map && ci(this._container), this
      },
      bringToBack: function() {
        return this._map && _i(this._container), this
      },
      _prepareOpen: function(t, i, e) {
        if (i instanceof Se || (e = i, i = t), i instanceof Ee)
          for (var n in t._layers) {
            i = t._layers[n];
            break
          }
        if (!e)
          if (i.getCenter) e = i.getCenter();
          else {
            if (!i.getLatLng) throw new Error("Unable to get source layer LatLng.");
            e = i.getLatLng()
          }
        return this._source = i, this.update(), e
      },
      _updateContent: function() {
        if (this._content) {
          var t = this._contentNode,
            i = "function" == typeof this._content ? this._content(this._source || this) : this._content;
          if ("string" == typeof i) t.innerHTML = i;
          else {
            for (; t.hasChildNodes();) t.removeChild(t.firstChild);
            t.appendChild(i)
          }
          this.fire("contentupdate")
        }
      },
      _updatePosition: function() {
        if (this._map) {
          var t = this._map.latLngToLayerPoint(this._latlng),
            i = I(this.options.offset),
            e = this._getAnchor();
          this._zoomAnimated ? wi(this._container, t.add(e)) : i = i.add(t).add(e);
          var n = this._containerBottom = -i.y,
            o = this._containerLeft = -Math.round(this._containerWidth / 2) + i.x;
          this._container.style.bottom = n + "px", this._container.style.left = o + "px"
        }
      },
      _getAnchor: function() {
        return [0, 0]
      }
    }),
    nn = en.extend({
      options: {
        maxWidth: 300,
        minWidth: 50,
        maxHeight: null,
        autoPan: !0,
        autoPanPaddingTopLeft: null,
        autoPanPaddingBottomRight: null,
        autoPanPadding: [5, 5],
        keepInView: !1,
        closeButton: !0,
        autoClose: !0,
        closeOnEscapeKey: !0,
        className: ""
      },
      openOn: function(t) {
        return t.openPopup(this), this
      },
      onAdd: function(t) {
        en.prototype.onAdd.call(this, t), t.fire("popupopen", {
          popup: this
        }), this._source && (this._source.fire("popupopen", {
          popup: this
        }, !0), this._source instanceof Oe || this._source.on("preclick", Oi))
      },
      onRemove: function(t) {
        en.prototype.onRemove.call(this, t), t.fire("popupclose", {
          popup: this
        }), this._source && (this._source.fire("popupclose", {
          popup: this
        }, !0), this._source instanceof Oe || this._source.off("preclick", Oi))
      },
      getEvents: function() {
        var t = en.prototype.getEvents.call(this);
        return (void 0 !== this.options.closeOnClick ? this.options.closeOnClick : this._map.options.closePopupOnClick) && (t.preclick = this._close), this.options.keepInView && (t.moveend = this._adjustPan), t
      },
      _close: function() {
        this._map && this._map.closePopup(this)
      },
      _initLayout: function() {
        var t = "leaflet-popup",
          i = this._container = hi("div", t + " " + (this.options.className || "") + " leaflet-zoom-animated"),
          e = this._wrapper = hi("div", t + "-content-wrapper", i);
        if (this._contentNode = hi("div", t + "-content", e), Ni(e), Ri(this._contentNode), Ei(e, "contextmenu", Oi), this._tipContainer = hi("div", t + "-tip-container", i), this._tip = hi("div", t + "-tip", this._tipContainer), this.options.closeButton) {
          var n = this._closeButton = hi("a", t + "-close-button", i);
          n.href = "#close", n.innerHTML = "&#215;", Ei(n, "click", this._onCloseButtonClick, this)
        }
      },
      _updateLayout: function() {
        var t = this._contentNode,
          i = t.style;
        i.width = "", i.whiteSpace = "nowrap";
        var e = t.offsetWidth;
        e = Math.min(e, this.options.maxWidth), e = Math.max(e, this.options.minWidth), i.width = e + 1 + "px", i.whiteSpace = "", i.height = "";
        var n = t.offsetHeight,
          o = this.options.maxHeight,
          s = "leaflet-popup-scrolled";
        o && o < n ? (i.height = o + "px", pi(t, s)) : mi(t, s), this._containerWidth = this._container.offsetWidth
      },
      _animateZoom: function(t) {
        var i = this._map._latLngToNewLayerPoint(this._latlng, t.zoom, t.center),
          e = this._getAnchor();
        wi(this._container, i.add(e))
      },
      _adjustPan: function() {
        if (this.options.autoPan) {
          this._map._panAnim && this._map._panAnim.stop();
          var t = this._map,
            i = parseInt(ai(this._container, "marginBottom"), 10) || 0,
            e = this._container.offsetHeight + i,
            n = this._containerWidth,
            o = new B(this._containerLeft, -e - this._containerBottom);
          o._add(Pi(this._container));
          var s = t.layerPointToContainerPoint(o),
            r = I(this.options.autoPanPadding),
            a = I(this.options.autoPanPaddingTopLeft || r),
            h = I(this.options.autoPanPaddingBottomRight || r),
            u = t.getSize(),
            l = 0,
            c = 0;
          s.x + n + h.x > u.x && (l = s.x + n - u.x + h.x), s.x - l - a.x < 0 && (l = s.x - a.x), s.y + e + h.y > u.y && (c = s.y + e - u.y + h.y), s.y - c - a.y < 0 && (c = s.y - a.y), (l || c) && t.fire("autopanstart").panBy([l, c])
        }
      },
      _onCloseButtonClick: function(t) {
        this._close(), ji(t)
      },
      _getAnchor: function() {
        return I(this._source && this._source._getPopupAnchor ? this._source._getPopupAnchor() : [0, 0])
      }
    });
  Ji.mergeOptions({
    closePopupOnClick: !0
  }), Ji.include({
    openPopup: function(t, i, e) {
      return t instanceof nn || (t = new nn(e).setContent(t)), i && t.setLatLng(i), this.hasLayer(t) ? this : (this._popup && this._popup.options.autoClose && this.closePopup(), this._popup = t, this.addLayer(t))
    },
    closePopup: function(t) {
      return t && t !== this._popup || (t = this._popup, this._popup = null), t && this.removeLayer(t), this
    }
  }), Se.include({
    bindPopup: function(t, i) {
      return t instanceof nn ? (p(t, i), (this._popup = t)._source = this) : (this._popup && !i || (this._popup = new nn(i, this)), this._popup.setContent(t)), this._popupHandlersAdded || (this.on({
        click: this._openPopup,
        keypress: this._onKeyPress,
        remove: this.closePopup,
        move: this._movePopup
      }), this._popupHandlersAdded = !0), this
    },
    unbindPopup: function() {
      return this._popup && (this.off({
        click: this._openPopup,
        keypress: this._onKeyPress,
        remove: this.closePopup,
        move: this._movePopup
      }), this._popupHandlersAdded = !1, this._popup = null), this
    },
    openPopup: function(t, i) {
      return this._popup && this._map && (i = this._popup._prepareOpen(this, t, i), this._map.openPopup(this._popup, i)), this
    },
    closePopup: function() {
      return this._popup && this._popup._close(), this
    },
    togglePopup: function(t) {
      return this._popup && (this._popup._map ? this.closePopup() : this.openPopup(t)), this
    },
    isPopupOpen: function() {
      return !!this._popup && this._popup.isOpen()
    },
    setPopupContent: function(t) {
      return this._popup && this._popup.setContent(t), this
    },
    getPopup: function() {
      return this._popup
    },
    _openPopup: function(t) {
      var i = t.layer || t.target;
      this._popup && this._map && (ji(t), i instanceof Oe ? this.openPopup(t.layer || t.target, t.latlng) : this._map.hasLayer(this._popup) && this._popup._source === i ? this.closePopup() : this.openPopup(i, t.latlng))
    },
    _movePopup: function(t) {
      this._popup.setLatLng(t.latlng)
    },
    _onKeyPress: function(t) {
      13 === t.originalEvent.keyCode && this._openPopup(t)
    }
  });
  var on = en.extend({
    options: {
      pane: "tooltipPane",
      offset: [0, 0],
      direction: "auto",
      permanent: !1,
      sticky: !1,
      interactive: !1,
      opacity: .9
    },
    onAdd: function(t) {
      en.prototype.onAdd.call(this, t), this.setOpacity(this.options.opacity), t.fire("tooltipopen", {
        tooltip: this
      }), this._source && this._source.fire("tooltipopen", {
        tooltip: this
      }, !0)
    },
    onRemove: function(t) {
      en.prototype.onRemove.call(this, t), t.fire("tooltipclose", {
        tooltip: this
      }), this._source && this._source.fire("tooltipclose", {
        tooltip: this
      }, !0)
    },
    getEvents: function() {
      var t = en.prototype.getEvents.call(this);
      return Tt && !this.options.permanent && (t.preclick = this._close), t
    },
    _close: function() {
      this._map && this._map.closeTooltip(this)
    },
    _initLayout: function() {
      var t = "leaflet-tooltip " + (this.options.className || "") + " leaflet-zoom-" + (this._zoomAnimated ? "animated" : "hide");
      this._contentNode = this._container = hi("div", t)
    },
    _updateLayout: function() {},
    _adjustPan: function() {},
    _setPosition: function(t) {
      var i = this._map,
        e = this._container,
        n = i.latLngToContainerPoint(i.getCenter()),
        o = i.layerPointToContainerPoint(t),
        s = this.options.direction,
        r = e.offsetWidth,
        a = e.offsetHeight,
        h = I(this.options.offset),
        u = this._getAnchor();
      t = "top" === s ? t.add(I(-r / 2 + h.x, -a + h.y + u.y, !0)) : "bottom" === s ? t.subtract(I(r / 2 - h.x, -h.y, !0)) : "center" === s ? t.subtract(I(r / 2 + h.x, a / 2 - u.y + h.y, !0)) : "right" === s || "auto" === s && o.x < n.x ? (s = "right", t.add(I(h.x + u.x, u.y - a / 2 + h.y, !0))) : (s = "left", t.subtract(I(r + u.x - h.x, a / 2 - u.y - h.y, !0))), mi(e, "leaflet-tooltip-right"), mi(e, "leaflet-tooltip-left"), mi(e, "leaflet-tooltip-top"), mi(e, "leaflet-tooltip-bottom"), pi(e, "leaflet-tooltip-" + s), wi(e, t)
    },
    _updatePosition: function() {
      var t = this._map.latLngToLayerPoint(this._latlng);
      this._setPosition(t)
    },
    setOpacity: function(t) {
      this.options.opacity = t, this._container && vi(this._container, t)
    },
    _animateZoom: function(t) {
      var i = this._map._latLngToNewLayerPoint(this._latlng, t.zoom, t.center);
      this._setPosition(i)
    },
    _getAnchor: function() {
      return I(this._source && this._source._getTooltipAnchor && !this.options.sticky ? this._source._getTooltipAnchor() : [0, 0])
    }
  });
  Ji.include({
    openTooltip: function(t, i, e) {
      return t instanceof on || (t = new on(e).setContent(t)), i && t.setLatLng(i), this.hasLayer(t) ? this : this.addLayer(t)
    },
    closeTooltip: function(t) {
      return t && this.removeLayer(t), this
    }
  }), Se.include({
    bindTooltip: function(t, i) {
      return t instanceof on ? (p(t, i), (this._tooltip = t)._source = this) : (this._tooltip && !i || (this._tooltip = new on(i, this)), this._tooltip.setContent(t)), this._initTooltipInteractions(), this._tooltip.options.permanent && this._map && this._map.hasLayer(this) && this.openTooltip(), this
    },
    unbindTooltip: function() {
      return this._tooltip && (this._initTooltipInteractions(!0), this.closeTooltip(), this._tooltip = null), this
    },
    _initTooltipInteractions: function(t) {
      if (t || !this._tooltipHandlersAdded) {
        var i = t ? "off" : "on",
          e = {
            remove: this.closeTooltip,
            move: this._moveTooltip
          };
        this._tooltip.options.permanent ? e.add = this._openTooltip : (e.mouseover = this._openTooltip, e.mouseout = this.closeTooltip, this._tooltip.options.sticky && (e.mousemove = this._moveTooltip), Tt && (e.click = this._openTooltip)), this[i](e), this._tooltipHandlersAdded = !t
      }
    },
    openTooltip: function(t, i) {
      return this._tooltip && this._map && (i = this._tooltip._prepareOpen(this, t, i), this._map.openTooltip(this._tooltip, i), this._tooltip.options.interactive && this._tooltip._container && (pi(this._tooltip._container, "leaflet-clickable"), this.addInteractiveTarget(this._tooltip._container))), this
    },
    closeTooltip: function() {
      return this._tooltip && (this._tooltip._close(), this._tooltip.options.interactive && this._tooltip._container && (mi(this._tooltip._container, "leaflet-clickable"), this.removeInteractiveTarget(this._tooltip._container))), this
    },
    toggleTooltip: function(t) {
      return this._tooltip && (this._tooltip._map ? this.closeTooltip() : this.openTooltip(t)), this
    },
    isTooltipOpen: function() {
      return this._tooltip.isOpen()
    },
    setTooltipContent: function(t) {
      return this._tooltip && this._tooltip.setContent(t), this
    },
    getTooltip: function() {
      return this._tooltip
    },
    _openTooltip: function(t) {
      var i = t.layer || t.target;
      this._tooltip && this._map && this.openTooltip(i, this._tooltip.options.sticky ? t.latlng : void 0)
    },
    _moveTooltip: function(t) {
      var i, e, n = t.latlng;
      this._tooltip.options.sticky && t.originalEvent && (i = this._map.mouseEventToContainerPoint(t.originalEvent), e = this._map.containerPointToLayerPoint(i), n = this._map.layerPointToLatLng(e)), this._tooltip.setLatLng(n)
    }
  });
  var sn = ke.extend({
    options: {
      iconSize: [12, 12],
      html: !1,
      bgPos: null,
      className: "leaflet-div-icon"
    },
    createIcon: function(t) {
      var i = t && "DIV" === t.tagName ? t : document.createElement("div"),
        e = this.options;
      if (e.html instanceof Element ? (li(i), i.appendChild(e.html)) : i.innerHTML = !1 !== e.html ? e.html : "", e.bgPos) {
        var n = I(e.bgPos);
        i.style.backgroundPosition = -n.x + "px " + -n.y + "px"
      }
      return this._setIconStyles(i, "icon"), i
    },
    createShadow: function() {
      return null
    }
  });
  ke.Default = Be;
  var rn = Se.extend({
    options: {
      tileSize: 256,
      opacity: 1,
      updateWhenIdle: xt,
      updateWhenZooming: !0,
      updateInterval: 200,
      zIndex: 1,
      bounds: null,
      minZoom: 0,
      maxZoom: void 0,
      maxNativeZoom: void 0,
      minNativeZoom: void 0,
      noWrap: !1,
      pane: "tilePane",
      className: "",
      keepBuffer: 2
    },
    initialize: function(t) {
      p(this, t)
    },
    onAdd: function() {
      this._initContainer(), this._levels = {}, this._tiles = {}, this._resetView(), this._update()
    },
    beforeAdd: function(t) {
      t._addZoomLimit(this)
    },
    onRemove: function(t) {
      this._removeAllTiles(), ui(this._container), t._removeZoomLimit(this), this._container = null, this._tileZoom = void 0
    },
    bringToFront: function() {
      return this._map && (ci(this._container), this._setAutoZIndex(Math.max)), this
    },
    bringToBack: function() {
      return this._map && (_i(this._container), this._setAutoZIndex(Math.min)), this
    },
    getContainer: function() {
      return this._container
    },
    setOpacity: function(t) {
      return this.options.opacity = t, this._updateOpacity(), this
    },
    setZIndex: function(t) {
      return this.options.zIndex = t, this._updateZIndex(), this
    },
    isLoading: function() {
      return this._loading
    },
    redraw: function() {
      return this._map && (this._removeAllTiles(), this._update()), this
    },
    getEvents: function() {
      var t = {
        viewprereset: this._invalidateAll,
        viewreset: this._resetView,
        zoom: this._resetView,
        moveend: this._onMoveEnd
      };
      return this.options.updateWhenIdle || (this._onMove || (this._onMove = o(this._onMoveEnd, this.options.updateInterval, this)), t.move = this._onMove), this._zoomAnimated && (t.zoomanim = this._animateZoom), t
    },
    createTile: function() {
      return document.createElement("div")
    },
    getTileSize: function() {
      var t = this.options.tileSize;
      return t instanceof B ? t : new B(t, t)
    },
    _updateZIndex: function() {
      this._container && void 0 !== this.options.zIndex && null !== this.options.zIndex && (this._container.style.zIndex = this.options.zIndex)
    },
    _setAutoZIndex: function(t) {
      for (var i, e = this.getPane().children, n = -t(-1 / 0, 1 / 0), o = 0, s = e.length; o < s; o++) i = e[o].style.zIndex, e[o] !== this._container && i && (n = t(n, +i));
      isFinite(n) && (this.options.zIndex = n + t(-1, 1), this._updateZIndex())
    },
    _updateOpacity: function() {
      if (this._map && !et) {
        vi(this._container, this.options.opacity);
        var t = +new Date,
          i = !1,
          e = !1;
        for (var n in this._tiles) {
          var o = this._tiles[n];
          if (o.current && o.loaded) {
            var s = Math.min(1, (t - o.loaded) / 200);
            vi(o.el, s), s < 1 ? i = !0 : (o.active ? e = !0 : this._onOpaqueTile(o), o.active = !0)
          }
        }
        e && !this._noPrune && this._pruneTiles(), i && (C(this._fadeFrame), this._fadeFrame = M(this._updateOpacity, this))
      }
    },
    _onOpaqueTile: l,
    _initContainer: function() {
      this._container || (this._container = hi("div", "leaflet-layer " + (this.options.className || "")), this._updateZIndex(), this.options.opacity < 1 && this._updateOpacity(), this.getPane().appendChild(this._container))
    },
    _updateLevels: function() {
      var t = this._tileZoom,
        i = this.options.maxZoom;
      if (void 0 !== t) {
        for (var e in this._levels) this._levels[e].el.children.length || e === t ? (this._levels[e].el.style.zIndex = i - Math.abs(t - e), this._onUpdateLevel(e)) : (ui(this._levels[e].el), this._removeTilesAtZoom(e), this._onRemoveLevel(e), delete this._levels[e]);
        var n = this._levels[t],
          o = this._map;
        return n || ((n = this._levels[t] = {}).el = hi("div", "leaflet-tile-container leaflet-zoom-animated", this._container), n.el.style.zIndex = i, n.origin = o.project(o.unproject(o.getPixelOrigin()), t).round(), n.zoom = t, this._setZoomTransform(n, o.getCenter(), o.getZoom()), n.el.offsetWidth, this._onCreateLevel(n)), this._level = n
      }
    },
    _onUpdateLevel: l,
    _onRemoveLevel: l,
    _onCreateLevel: l,
    _pruneTiles: function() {
      if (this._map) {
        var t, i, e = this._map.getZoom();
        if (e > this.options.maxZoom || e < this.options.minZoom) this._removeAllTiles();
        else {
          for (t in this._tiles)(i = this._tiles[t]).retain = i.current;
          for (t in this._tiles)
            if ((i = this._tiles[t]).current && !i.active) {
              var n = i.coords;
              this._retainParent(n.x, n.y, n.z, n.z - 5) || this._retainChildren(n.x, n.y, n.z, n.z + 2)
            }
          for (t in this._tiles) this._tiles[t].retain || this._removeTile(t)
        }
      }
    },
    _removeTilesAtZoom: function(t) {
      for (var i in this._tiles) this._tiles[i].coords.z === t && this._removeTile(i)
    },
    _removeAllTiles: function() {
      for (var t in this._tiles) this._removeTile(t)
    },
    _invalidateAll: function() {
      for (var t in this._levels) ui(this._levels[t].el), this._onRemoveLevel(t), delete this._levels[t];
      this._removeAllTiles(), this._tileZoom = void 0
    },
    _retainParent: function(t, i, e, n) {
      var o = Math.floor(t / 2),
        s = Math.floor(i / 2),
        r = e - 1,
        a = new B(+o, +s);
      a.z = +r;
      var h = this._tileCoordsToKey(a),
        u = this._tiles[h];
      return u && u.active ? u.retain = !0 : (u && u.loaded && (u.retain = !0), n < r && this._retainParent(o, s, r, n))
    },
    _retainChildren: function(t, i, e, n) {
      for (var o = 2 * t; o < 2 * t + 2; o++)
        for (var s = 2 * i; s < 2 * i + 2; s++) {
          var r = new B(o, s);
          r.z = e + 1;
          var a = this._tileCoordsToKey(r),
            h = this._tiles[a];
          h && h.active ? h.retain = !0 : (h && h.loaded && (h.retain = !0), e + 1 < n && this._retainChildren(o, s, e + 1, n))
        }
    },
    _resetView: function(t) {
      var i = t && (t.pinch || t.flyTo);
      this._setView(this._map.getCenter(), this._map.getZoom(), i, i)
    },
    _animateZoom: function(t) {
      this._setView(t.center, t.zoom, !0, t.noUpdate)
    },
    _clampZoom: function(t) {
      var i = this.options;
      return void 0 !== i.minNativeZoom && t < i.minNativeZoom ? i.minNativeZoom : void 0 !== i.maxNativeZoom && i.maxNativeZoom < t ? i.maxNativeZoom : t
    },
    _setView: function(t, i, e, n) {
      var o = this._clampZoom(Math.round(i));
      (void 0 !== this.options.maxZoom && o > this.options.maxZoom || void 0 !== this.options.minZoom && o < this.options.minZoom) && (o = void 0);
      var s = this.options.updateWhenZooming && o !== this._tileZoom;
      n && !s || (this._tileZoom = o, this._abortLoading && this._abortLoading(), this._updateLevels(), this._resetGrid(), void 0 !== o && this._update(t), e || this._pruneTiles(), this._noPrune = !!e), this._setZoomTransforms(t, i)
    },
    _setZoomTransforms: function(t, i) {
      for (var e in this._levels) this._setZoomTransform(this._levels[e], t, i)
    },
    _setZoomTransform: function(t, i, e) {
      var n = this._map.getZoomScale(e, t.zoom),
        o = t.origin.multiplyBy(n).subtract(this._map._getNewPixelOrigin(i, e)).round();
      yt ? xi(t.el, o, n) : wi(t.el, o)
    },
    _resetGrid: function() {
      var t = this._map,
        i = t.options.crs,
        e = this._tileSize = this.getTileSize(),
        n = this._tileZoom,
        o = this._map.getPixelWorldBounds(this._tileZoom);
      o && (this._globalTileRange = this._pxBoundsToTileRange(o)), this._wrapX = i.wrapLng && !this.options.noWrap && [Math.floor(t.project([0, i.wrapLng[0]], n).x / e.x), Math.ceil(t.project([0, i.wrapLng[1]], n).x / e.y)], this._wrapY = i.wrapLat && !this.options.noWrap && [Math.floor(t.project([i.wrapLat[0], 0], n).y / e.x), Math.ceil(t.project([i.wrapLat[1], 0], n).y / e.y)]
    },
    _onMoveEnd: function() {
      this._map && !this._map._animatingZoom && this._update()
    },
    _getTiledPixelBounds: function(t) {
      var i = this._map,
        e = i._animatingZoom ? Math.max(i._animateToZoom, i.getZoom()) : i.getZoom(),
        n = i.getZoomScale(e, this._tileZoom),
        o = i.project(t, this._tileZoom).floor(),
        s = i.getSize().divideBy(2 * n);
      return new O(o.subtract(s), o.add(s))
    },
    _update: function(t) {
      var i = this._map;
      if (i) {
        var e = this._clampZoom(i.getZoom());
        if (void 0 === t && (t = i.getCenter()), void 0 !== this._tileZoom) {
          var n = this._getTiledPixelBounds(t),
            o = this._pxBoundsToTileRange(n),
            s = o.getCenter(),
            r = [],
            a = this.options.keepBuffer,
            h = new O(o.getBottomLeft().subtract([a, -a]), o.getTopRight().add([a, -a]));
          if (!(isFinite(o.min.x) && isFinite(o.min.y) && isFinite(o.max.x) && isFinite(o.max.y))) throw new Error("Attempted to load an infinite number of tiles");
          for (var u in this._tiles) {
            var l = this._tiles[u].coords;
            l.z === this._tileZoom && h.contains(new B(l.x, l.y)) || (this._tiles[u].current = !1)
          }
          if (1 < Math.abs(e - this._tileZoom)) this._setView(t, e);
          else {
            for (var c = o.min.y; c <= o.max.y; c++)
              for (var _ = o.min.x; _ <= o.max.x; _++) {
                var d = new B(_, c);
                if (d.z = this._tileZoom, this._isValidTile(d)) {
                  var p = this._tiles[this._tileCoordsToKey(d)];
                  p ? p.current = !0 : r.push(d)
                }
              }
            if (r.sort(function(t, i) {
                return t.distanceTo(s) - i.distanceTo(s)
              }), 0 !== r.length) {
              this._loading || (this._loading = !0, this.fire("loading"));
              var m = document.createDocumentFragment();
              for (_ = 0; _ < r.length; _++) this._addTile(r[_], m);
              this._level.el.appendChild(m)
            }
          }
        }
      }
    },
    _isValidTile: function(t) {
      var i = this._map.options.crs;
      if (!i.infinite) {
        var e = this._globalTileRange;
        if (!i.wrapLng && (t.x < e.min.x || t.x > e.max.x) || !i.wrapLat && (t.y < e.min.y || t.y > e.max.y)) return !1
      }
      if (!this.options.bounds) return !0;
      var n = this._tileCoordsToBounds(t);
      return D(this.options.bounds).overlaps(n)
    },
    _keyToBounds: function(t) {
      return this._tileCoordsToBounds(this._keyToTileCoords(t))
    },
    _tileCoordsToNwSe: function(t) {
      var i = this._map,
        e = this.getTileSize(),
        n = t.scaleBy(e),
        o = n.add(e);
      return [i.unproject(n, t.z), i.unproject(o, t.z)]
    },
    _tileCoordsToBounds: function(t) {
      var i = this._tileCoordsToNwSe(t),
        e = new N(i[0], i[1]);
      return this.options.noWrap || (e = this._map.wrapLatLngBounds(e)), e
    },
    _tileCoordsToKey: function(t) {
      return t.x + ":" + t.y + ":" + t.z
    },
    _keyToTileCoords: function(t) {
      var i = t.split(":"),
        e = new B(+i[0], +i[1]);
      return e.z = +i[2], e
    },
    _removeTile: function(t) {
      var i = this._tiles[t];
      i && (ui(i.el), delete this._tiles[t], this.fire("tileunload", {
        tile: i.el,
        coords: this._keyToTileCoords(t)
      }))
    },
    _initTile: function(t) {
      pi(t, "leaflet-tile");
      var i = this.getTileSize();
      t.style.width = i.x + "px", t.style.height = i.y + "px", t.onselectstart = l, t.onmousemove = l, et && this.options.opacity < 1 && vi(t, this.options.opacity), st && !rt && (t.style.WebkitBackfaceVisibility = "hidden")
    },
    _addTile: function(t, i) {
      var e = this._getTilePos(t),
        n = this._tileCoordsToKey(t),
        o = this.createTile(this._wrapCoords(t), a(this._tileReady, this, t));
      this._initTile(o), this.createTile.length < 2 && M(a(this._tileReady, this, t, null, o)), wi(o, e), this._tiles[n] = {
        el: o,
        coords: t,
        current: !0
      }, i.appendChild(o), this.fire("tileloadstart", {
        tile: o,
        coords: t
      })
    },
    _tileReady: function(t, i, e) {
      i && this.fire("tileerror", {
        error: i,
        tile: e,
        coords: t
      });
      var n = this._tileCoordsToKey(t);
      (e = this._tiles[n]) && (e.loaded = +new Date, this._map._fadeAnimated ? (vi(e.el, 0), C(this._fadeFrame), this._fadeFrame = M(this._updateOpacity, this)) : (e.active = !0, this._pruneTiles()), i || (pi(e.el, "leaflet-tile-loaded"), this.fire("tileload", {
        tile: e.el,
        coords: t
      })), this._noTilesToLoad() && (this._loading = !1, this.fire("load"), et || !this._map._fadeAnimated ? M(this._pruneTiles, this) : setTimeout(a(this._pruneTiles, this), 250)))
    },
    _getTilePos: function(t) {
      return t.scaleBy(this.getTileSize()).subtract(this._level.origin)
    },
    _wrapCoords: function(t) {
      var i = new B(this._wrapX ? r(t.x, this._wrapX) : t.x, this._wrapY ? r(t.y, this._wrapY) : t.y);
      return i.z = t.z, i
    },
    _pxBoundsToTileRange: function(t) {
      var i = this.getTileSize();
      return new O(t.min.unscaleBy(i).floor(), t.max.unscaleBy(i).ceil().subtract([1, 1]))
    },
    _noTilesToLoad: function() {
      for (var t in this._tiles)
        if (!this._tiles[t].loaded) return !1;
      return !0
    }
  });
  var an = rn.extend({
    options: {
      minZoom: 0,
      maxZoom: 18,
      subdomains: "abc",
      errorTileUrl: "",
      zoomOffset: 0,
      tms: !1,
      zoomReverse: !1,
      detectRetina: !1,
      crossOrigin: !1
    },
    initialize: function(t, i) {
      this._url = t, (i = p(this, i)).detectRetina && Ct && 0 < i.maxZoom && (i.tileSize = Math.floor(i.tileSize / 2), i.zoomReverse ? (i.zoomOffset--, i.minZoom++) : (i.zoomOffset++, i.maxZoom--), i.minZoom = Math.max(0, i.minZoom)), "string" == typeof i.subdomains && (i.subdomains = i.subdomains.split("")), st || this.on("tileunload", this._onTileRemove)
    },
    setUrl: function(t, i) {
      return this._url === t && void 0 === i && (i = !0), this._url = t, i || this.redraw(), this
    },
    createTile: function(t, i) {
      var e = document.createElement("img");
      return Ei(e, "load", a(this._tileOnLoad, this, i, e)), Ei(e, "error", a(this._tileOnError, this, i, e)), !this.options.crossOrigin && "" !== this.options.crossOrigin || (e.crossOrigin = !0 === this.options.crossOrigin ? "" : this.options.crossOrigin), e.alt = "", e.setAttribute("role", "presentation"), e.src = this.getTileUrl(t), e
    },
    getTileUrl: function(t) {
      var i = {
        r: Ct ? "@2x" : "",
        s: this._getSubdomain(t),
        x: t.x,
        y: t.y,
        z: this._getZoomForUrl()
      };
      if (this._map && !this._map.options.crs.infinite) {
        var e = this._globalTileRange.max.y - t.y;
        this.options.tms && (i.y = e), i["-y"] = e
      }
      return g(this._url, h(i, this.options))
    },
    _tileOnLoad: function(t, i) {
      et ? setTimeout(a(t, this, null, i), 0) : t(null, i)
    },
    _tileOnError: function(t, i, e) {
      var n = this.options.errorTileUrl;
      n && i.getAttribute("src") !== n && (i.src = n), t(e, i)
    },
    _onTileRemove: function(t) {
      t.tile.onload = null
    },
    _getZoomForUrl: function() {
      var t = this._tileZoom,
        i = this.options.maxZoom;
      return this.options.zoomReverse && (t = i - t), t + this.options.zoomOffset
    },
    _getSubdomain: function(t) {
      var i = Math.abs(t.x + t.y) % this.options.subdomains.length;
      return this.options.subdomains[i]
    },
    _abortLoading: function() {
      var t, i;
      for (t in this._tiles) this._tiles[t].coords.z !== this._tileZoom && ((i = this._tiles[t].el).onload = l, i.onerror = l, i.complete || (i.src = x, ui(i), delete this._tiles[t]))
    },
    _removeTile: function(t) {
      var i = this._tiles[t];
      if (i) return ht || i.el.setAttribute("src", x), rn.prototype._removeTile.call(this, t)
    },
    _tileReady: function(t, i, e) {
      if (this._map && (!e || e.getAttribute("src") !== x)) return rn.prototype._tileReady.call(this, t, i, e)
    }
  });

  function hn(t, i) {
    return new an(t, i)
  }
  var un = an.extend({
    defaultWmsParams: {
      service: "WMS",
      request: "GetMap",
      layers: "",
      styles: "",
      format: "image/jpeg",
      transparent: !1,
      version: "1.1.1"
    },
    options: {
      crs: null,
      uppercase: !1
    },
    initialize: function(t, i) {
      this._url = t;
      var e = h({}, this.defaultWmsParams);
      for (var n in i) n in this.options || (e[n] = i[n]);
      var o = (i = p(this, i)).detectRetina && Ct ? 2 : 1,
        s = this.getTileSize();
      e.width = s.x * o, e.height = s.y * o, this.wmsParams = e
    },
    onAdd: function(t) {
      this._crs = this.options.crs || t.options.crs, this._wmsVersion = parseFloat(this.wmsParams.version);
      var i = 1.3 <= this._wmsVersion ? "crs" : "srs";
      this.wmsParams[i] = this._crs.code, an.prototype.onAdd.call(this, t)
    },
    getTileUrl: function(t) {
      var i = this._tileCoordsToNwSe(t),
        e = this._crs,
        n = R(e.project(i[0]), e.project(i[1])),
        o = n.min,
        s = n.max,
        r = (1.3 <= this._wmsVersion && this._crs === Me ? [o.y, o.x, s.y, s.x] : [o.x, o.y, s.x, s.y]).join(","),
        a = an.prototype.getTileUrl.call(this, t);
      return a + m(this.wmsParams, a, this.options.uppercase) + (this.options.uppercase ? "&BBOX=" : "&bbox=") + r
    },
    setParams: function(t, i) {
      return h(this.wmsParams, t), i || this.redraw(), this
    }
  });
  an.WMS = un, hn.wms = function(t, i) {
    return new un(t, i)
  };
  var ln = Se.extend({
      options: {
        padding: .1,
        tolerance: 0
      },
      initialize: function(t) {
        p(this, t), u(this), this._layers = this._layers || {}
      },
      onAdd: function() {
        this._container || (this._initContainer(), this._zoomAnimated && pi(this._container, "leaflet-zoom-animated")), this.getPane().appendChild(this._container), this._update(), this.on("update", this._updatePaths, this)
      },
      onRemove: function() {
        this.off("update", this._updatePaths, this), this._destroyContainer()
      },
      getEvents: function() {
        var t = {
          viewreset: this._reset,
          zoom: this._onZoom,
          moveend: this._update,
          zoomend: this._onZoomEnd
        };
        return this._zoomAnimated && (t.zoomanim = this._onAnimZoom), t
      },
      _onAnimZoom: function(t) {
        this._updateTransform(t.center, t.zoom)
      },
      _onZoom: function() {
        this._updateTransform(this._map.getCenter(), this._map.getZoom())
      },
      _updateTransform: function(t, i) {
        var e = this._map.getZoomScale(i, this._zoom),
          n = Pi(this._container),
          o = this._map.getSize().multiplyBy(.5 + this.options.padding),
          s = this._map.project(this._center, i),
          r = this._map.project(t, i).subtract(s),
          a = o.multiplyBy(-e).add(n).add(o).subtract(r);
        yt ? xi(this._container, a, e) : wi(this._container, a)
      },
      _reset: function() {
        for (var t in this._update(), this._updateTransform(this._center, this._zoom), this._layers) this._layers[t]._reset()
      },
      _onZoomEnd: function() {
        for (var t in this._layers) this._layers[t]._project()
      },
      _updatePaths: function() {
        for (var t in this._layers) this._layers[t]._update()
      },
      _update: function() {
        var t = this.options.padding,
          i = this._map.getSize(),
          e = this._map.containerPointToLayerPoint(i.multiplyBy(-t)).round();
        this._bounds = new O(e, e.add(i.multiplyBy(1 + 2 * t)).round()), this._center = this._map.getCenter(), this._zoom = this._map.getZoom()
      }
    }),
    cn = ln.extend({
      getEvents: function() {
        var t = ln.prototype.getEvents.call(this);
        return t.viewprereset = this._onViewPreReset, t
      },
      _onViewPreReset: function() {
        this._postponeUpdatePaths = !0
      },
      onAdd: function() {
        ln.prototype.onAdd.call(this), this._draw()
      },
      _initContainer: function() {
        var t = this._container = document.createElement("canvas");
        Ei(t, "mousemove", o(this._onMouseMove, 32, this), this), Ei(t, "click dblclick mousedown mouseup contextmenu", this._onClick, this), Ei(t, "mouseout", this._handleMouseOut, this), this._ctx = t.getContext("2d")
      },
      _destroyContainer: function() {
        C(this._redrawRequest), delete this._ctx, ui(this._container), Bi(this._container), delete this._container
      },
      _updatePaths: function() {
        if (!this._postponeUpdatePaths) {
          for (var t in this._redrawBounds = null, this._layers) this._layers[t]._update();
          this._redraw()
        }
      },
      _update: function() {
        if (!this._map._animatingZoom || !this._bounds) {
          ln.prototype._update.call(this);
          var t = this._bounds,
            i = this._container,
            e = t.getSize(),
            n = Ct ? 2 : 1;
          wi(i, t.min), i.width = n * e.x, i.height = n * e.y, i.style.width = e.x + "px", i.style.height = e.y + "px", Ct && this._ctx.scale(2, 2), this._ctx.translate(-t.min.x, -t.min.y), this.fire("update")
        }
      },
      _reset: function() {
        ln.prototype._reset.call(this), this._postponeUpdatePaths && (this._postponeUpdatePaths = !1, this._updatePaths())
      },
      _initPath: function(t) {
        this._updateDashArray(t);
        var i = (this._layers[u(t)] = t)._order = {
          layer: t,
          prev: this._drawLast,
          next: null
        };
        this._drawLast && (this._drawLast.next = i), this._drawLast = i, this._drawFirst = this._drawFirst || this._drawLast
      },
      _addPath: function(t) {
        this._requestRedraw(t)
      },
      _removePath: function(t) {
        var i = t._order,
          e = i.next,
          n = i.prev;
        e ? e.prev = n : this._drawLast = n, n ? n.next = e : this._drawFirst = e, delete t._order, delete this._layers[u(t)], this._requestRedraw(t)
      },
      _updatePath: function(t) {
        this._extendRedrawBounds(t), t._project(), t._update(), this._requestRedraw(t)
      },
      _updateStyle: function(t) {
        this._updateDashArray(t), this._requestRedraw(t)
      },
      _updateDashArray: function(t) {
        if ("string" == typeof t.options.dashArray) {
          var i, e, n = t.options.dashArray.split(/[, ]+/),
            o = [];
          for (e = 0; e < n.length; e++) {
            if (i = Number(n[e]), isNaN(i)) return;
            o.push(i)
          }
          t.options._dashArray = o
        } else t.options._dashArray = t.options.dashArray
      },
      _requestRedraw: function(t) {
        this._map && (this._extendRedrawBounds(t), this._redrawRequest = this._redrawRequest || M(this._redraw, this))
      },
      _extendRedrawBounds: function(t) {
        if (t._pxBounds) {
          var i = (t.options.weight || 0) + 1;
          this._redrawBounds = this._redrawBounds || new O, this._redrawBounds.extend(t._pxBounds.min.subtract([i, i])), this._redrawBounds.extend(t._pxBounds.max.add([i, i]))
        }
      },
      _redraw: function() {
        this._redrawRequest = null, this._redrawBounds && (this._redrawBounds.min._floor(), this._redrawBounds.max._ceil()), this._clear(), this._draw(), this._redrawBounds = null
      },
      _clear: function() {
        var t = this._redrawBounds;
        if (t) {
          var i = t.getSize();
          this._ctx.clearRect(t.min.x, t.min.y, i.x, i.y)
        } else this._ctx.clearRect(0, 0, this._container.width, this._container.height)
      },
      _draw: function() {
        var t, i = this._redrawBounds;
        if (this._ctx.save(), i) {
          var e = i.getSize();
          this._ctx.beginPath(), this._ctx.rect(i.min.x, i.min.y, e.x, e.y), this._ctx.clip()
        }
        this._drawing = !0;
        for (var n = this._drawFirst; n; n = n.next) t = n.layer, (!i || t._pxBounds && t._pxBounds.intersects(i)) && t._updatePath();
        this._drawing = !1, this._ctx.restore()
      },
      _updatePoly: function(t, i) {
        if (this._drawing) {
          var e, n, o, s, r = t._parts,
            a = r.length,
            h = this._ctx;
          if (a) {
            for (h.beginPath(), e = 0; e < a; e++) {
              for (n = 0, o = r[e].length; n < o; n++) s = r[e][n], h[n ? "lineTo" : "moveTo"](s.x, s.y);
              i && h.closePath()
            }
            this._fillStroke(h, t)
          }
        }
      },
      _updateCircle: function(t) {
        if (this._drawing && !t._empty()) {
          var i = t._point,
            e = this._ctx,
            n = Math.max(Math.round(t._radius), 1),
            o = (Math.max(Math.round(t._radiusY), 1) || n) / n;
          1 != o && (e.save(), e.scale(1, o)), e.beginPath(), e.arc(i.x, i.y / o, n, 0, 2 * Math.PI, !1), 1 != o && e.restore(), this._fillStroke(e, t)
        }
      },
      _fillStroke: function(t, i) {
        var e = i.options;
        e.fill && (t.globalAlpha = e.fillOpacity, t.fillStyle = e.fillColor || e.color, t.fill(e.fillRule || "evenodd")), e.stroke && 0 !== e.weight && (t.setLineDash && t.setLineDash(i.options && i.options._dashArray || []), t.globalAlpha = e.opacity, t.lineWidth = e.weight, t.strokeStyle = e.color, t.lineCap = e.lineCap, t.lineJoin = e.lineJoin, t.stroke())
      },
      _onClick: function(t) {
        for (var i, e, n = this._map.mouseEventToLayerPoint(t), o = this._drawFirst; o; o = o.next)(i = o.layer).options.interactive && i._containsPoint(n) && !this._map._draggableMoved(i) && (e = i);
        e && (qi(t), this._fireEvent([e], t))
      },
      _onMouseMove: function(t) {
        if (this._map && !this._map.dragging.moving() && !this._map._animatingZoom) {
          var i = this._map.mouseEventToLayerPoint(t);
          this._handleMouseHover(t, i)
        }
      },
      _handleMouseOut: function(t) {
        var i = this._hoveredLayer;
        i && (mi(this._container, "leaflet-interactive"), this._fireEvent([i], t, "mouseout"), this._hoveredLayer = null)
      },
      _handleMouseHover: function(t, i) {
        for (var e, n, o = this._drawFirst; o; o = o.next)(e = o.layer).options.interactive && e._containsPoint(i) && (n = e);
        n !== this._hoveredLayer && (this._handleMouseOut(t), n && (pi(this._container, "leaflet-interactive"), this._fireEvent([n], t, "mouseover"), this._hoveredLayer = n)), this._hoveredLayer && this._fireEvent([this._hoveredLayer], t)
      },
      _fireEvent: function(t, i, e) {
        this._map._fireDOMEvent(i, e || i.type, t)
      },
      _bringToFront: function(t) {
        var i = t._order;
        if (i) {
          var e = i.next,
            n = i.prev;
          e && ((e.prev = n) ? n.next = e : e && (this._drawFirst = e), i.prev = this._drawLast, (this._drawLast.next = i).next = null, this._drawLast = i, this._requestRedraw(t))
        }
      },
      _bringToBack: function(t) {
        var i = t._order;
        if (i) {
          var e = i.next,
            n = i.prev;
          n && ((n.next = e) ? e.prev = n : n && (this._drawLast = n), i.prev = null, i.next = this._drawFirst, this._drawFirst.prev = i, this._drawFirst = i, this._requestRedraw(t))
        }
      }
    });

  function _n(t) {
    return St ? new cn(t) : null
  }
  var dn = function() {
      try {
        return document.namespaces.add("lvml", "urn:schemas-microsoft-com:vml"),
          function(t) {
            return document.createElement("<lvml:" + t + ' class="lvml">')
          }
      } catch (t) {
        return function(t) {
          return document.createElement("<" + t + ' xmlns="urn:schemas-microsoft.com:vml" class="lvml">')
        }
      }
    }(),
    pn = {
      _initContainer: function() {
        this._container = hi("div", "leaflet-vml-container")
      },
      _update: function() {
        this._map._animatingZoom || (ln.prototype._update.call(this), this.fire("update"))
      },
      _initPath: function(t) {
        var i = t._container = dn("shape");
        pi(i, "leaflet-vml-shape " + (this.options.className || "")), i.coordsize = "1 1", t._path = dn("path"), i.appendChild(t._path), this._updateStyle(t), this._layers[u(t)] = t
      },
      _addPath: function(t) {
        var i = t._container;
        this._container.appendChild(i), t.options.interactive && t.addInteractiveTarget(i)
      },
      _removePath: function(t) {
        var i = t._container;
        ui(i), t.removeInteractiveTarget(i), delete this._layers[u(t)]
      },
      _updateStyle: function(t) {
        var i = t._stroke,
          e = t._fill,
          n = t.options,
          o = t._container;
        o.stroked = !!n.stroke, o.filled = !!n.fill, n.stroke ? (i || (i = t._stroke = dn("stroke")), o.appendChild(i), i.weight = n.weight + "px", i.color = n.color, i.opacity = n.opacity, n.dashArray ? i.dashStyle = v(n.dashArray) ? n.dashArray.join(" ") : n.dashArray.replace(/( *, *)/g, " ") : i.dashStyle = "", i.endcap = n.lineCap.replace("butt", "flat"), i.joinstyle = n.lineJoin) : i && (o.removeChild(i), t._stroke = null), n.fill ? (e || (e = t._fill = dn("fill")), o.appendChild(e), e.color = n.fillColor || n.color, e.opacity = n.fillOpacity) : e && (o.removeChild(e), t._fill = null)
      },
      _updateCircle: function(t) {
        var i = t._point.round(),
          e = Math.round(t._radius),
          n = Math.round(t._radiusY || e);
        this._setPath(t, t._empty() ? "M0 0" : "AL " + i.x + "," + i.y + " " + e + "," + n + " 0,23592600")
      },
      _setPath: function(t, i) {
        t._path.v = i
      },
      _bringToFront: function(t) {
        ci(t._container)
      },
      _bringToBack: function(t) {
        _i(t._container)
      }
    },
    mn = Et ? dn : $,
    fn = ln.extend({
      getEvents: function() {
        var t = ln.prototype.getEvents.call(this);
        return t.zoomstart = this._onZoomStart, t
      },
      _initContainer: function() {
        this._container = mn("svg"), this._container.setAttribute("pointer-events", "none"), this._rootGroup = mn("g"), this._container.appendChild(this._rootGroup)
      },
      _destroyContainer: function() {
        ui(this._container), Bi(this._container), delete this._container, delete this._rootGroup, delete this._svgSize
      },
      _onZoomStart: function() {
        this._update()
      },
      _update: function() {
        if (!this._map._animatingZoom || !this._bounds) {
          ln.prototype._update.call(this);
          var t = this._bounds,
            i = t.getSize(),
            e = this._container;
          this._svgSize && this._svgSize.equals(i) || (this._svgSize = i, e.setAttribute("width", i.x), e.setAttribute("height", i.y)), wi(e, t.min), e.setAttribute("viewBox", [t.min.x, t.min.y, i.x, i.y].join(" ")), this.fire("update")
        }
      },
      _initPath: function(t) {
        var i = t._path = mn("path");
        t.options.className && pi(i, t.options.className), t.options.interactive && pi(i, "leaflet-interactive"), this._updateStyle(t), this._layers[u(t)] = t
      },
      _addPath: function(t) {
        this._rootGroup || this._initContainer(), this._rootGroup.appendChild(t._path), t.addInteractiveTarget(t._path)
      },
      _removePath: function(t) {
        ui(t._path), t.removeInteractiveTarget(t._path), delete this._layers[u(t)]
      },
      _updatePath: function(t) {
        t._project(), t._update()
      },
      _updateStyle: function(t) {
        var i = t._path,
          e = t.options;
        i && (e.stroke ? (i.setAttribute("stroke", e.color), i.setAttribute("stroke-opacity", e.opacity), i.setAttribute("stroke-width", e.weight), i.setAttribute("stroke-linecap", e.lineCap), i.setAttribute("stroke-linejoin", e.lineJoin), e.dashArray ? i.setAttribute("stroke-dasharray", e.dashArray) : i.removeAttribute("stroke-dasharray"), e.dashOffset ? i.setAttribute("stroke-dashoffset", e.dashOffset) : i.removeAttribute("stroke-dashoffset")) : i.setAttribute("stroke", "none"), e.fill ? (i.setAttribute("fill", e.fillColor || e.color), i.setAttribute("fill-opacity", e.fillOpacity), i.setAttribute("fill-rule", e.fillRule || "evenodd")) : i.setAttribute("fill", "none"))
      },
      _updatePoly: function(t, i) {
        this._setPath(t, Q(t._parts, i))
      },
      _updateCircle: function(t) {
        var i = t._point,
          e = Math.max(Math.round(t._radius), 1),
          n = "a" + e + "," + (Math.max(Math.round(t._radiusY), 1) || e) + " 0 1,0 ",
          o = t._empty() ? "M0 0" : "M" + (i.x - e) + "," + i.y + n + 2 * e + ",0 " + n + 2 * -e + ",0 ";
        this._setPath(t, o)
      },
      _setPath: function(t, i) {
        t._path.setAttribute("d", i)
      },
      _bringToFront: function(t) {
        ci(t._path)
      },
      _bringToBack: function(t) {
        _i(t._path)
      }
    });

  function gn(t) {
    return Zt || Et ? new fn(t) : null
  }
  Et && fn.include(pn), Ji.include({
    getRenderer: function(t) {
      var i = t.options.renderer || this._getPaneRenderer(t.options.pane) || this.options.renderer || this._renderer;
      return i || (i = this._renderer = this._createRenderer()), this.hasLayer(i) || this.addLayer(i), i
    },
    _getPaneRenderer: function(t) {
      if ("overlayPane" === t || void 0 === t) return !1;
      var i = this._paneRenderers[t];
      return void 0 === i && (i = this._createRenderer({
        pane: t
      }), this._paneRenderers[t] = i), i
    },
    _createRenderer: function(t) {
      return this.options.preferCanvas && _n(t) || gn(t)
    }
  });
  var vn = je.extend({
    initialize: function(t, i) {
      je.prototype.initialize.call(this, this._boundsToLatLngs(t), i)
    },
    setBounds: function(t) {
      return this.setLatLngs(this._boundsToLatLngs(t))
    },
    _boundsToLatLngs: function(t) {
      return [(t = D(t)).getSouthWest(), t.getNorthWest(), t.getNorthEast(), t.getSouthEast()]
    }
  });
  fn.create = mn, fn.pointsToPath = Q, We.geometryToLayer = He, We.coordsToLatLng = Fe, We.coordsToLatLngs = Ue, We.latLngToCoords = Ve, We.latLngsToCoords = qe, We.getFeature = Ge, We.asFeature = Ke, Ji.mergeOptions({
    boxZoom: !0
  });
  var yn = oe.extend({
    initialize: function(t) {
      this._map = t, this._container = t._container, this._pane = t._panes.overlayPane, this._resetStateTimeout = 0, t.on("unload", this._destroy, this)
    },
    addHooks: function() {
      Ei(this._container, "mousedown", this._onMouseDown, this)
    },
    removeHooks: function() {
      Bi(this._container, "mousedown", this._onMouseDown, this)
    },
    moved: function() {
      return this._moved
    },
    _destroy: function() {
      ui(this._pane), delete this._pane
    },
    _resetState: function() {
      this._resetStateTimeout = 0, this._moved = !1
    },
    _clearDeferredResetState: function() {
      0 !== this._resetStateTimeout && (clearTimeout(this._resetStateTimeout), this._resetStateTimeout = 0)
    },
    _onMouseDown: function(t) {
      if (!t.shiftKey || 1 !== t.which && 1 !== t.button) return !1;
      this._clearDeferredResetState(), this._resetState(), $t(), Li(), this._startPoint = this._map.mouseEventToContainerPoint(t), Ei(document, {
        contextmenu: ji,
        mousemove: this._onMouseMove,
        mouseup: this._onMouseUp,
        keydown: this._onKeyDown
      }, this)
    },
    _onMouseMove: function(t) {
      this._moved || (this._moved = !0, this._box = hi("div", "leaflet-zoom-box", this._container), pi(this._container, "leaflet-crosshair"), this._map.fire("boxzoomstart")), this._point = this._map.mouseEventToContainerPoint(t);
      var i = new O(this._point, this._startPoint),
        e = i.getSize();
      wi(this._box, i.min), this._box.style.width = e.x + "px", this._box.style.height = e.y + "px"
    },
    _finish: function() {
      this._moved && (ui(this._box), mi(this._container, "leaflet-crosshair")), Qt(), Ti(), Bi(document, {
        contextmenu: ji,
        mousemove: this._onMouseMove,
        mouseup: this._onMouseUp,
        keydown: this._onKeyDown
      }, this)
    },
    _onMouseUp: function(t) {
      if ((1 === t.which || 1 === t.button) && (this._finish(), this._moved)) {
        this._clearDeferredResetState(), this._resetStateTimeout = setTimeout(a(this._resetState, this), 0);
        var i = new N(this._map.containerPointToLatLng(this._startPoint), this._map.containerPointToLatLng(this._point));
        this._map.fitBounds(i).fire("boxzoomend", {
          boxZoomBounds: i
        })
      }
    },
    _onKeyDown: function(t) {
      27 === t.keyCode && this._finish()
    }
  });
  Ji.addInitHook("addHandler", "boxZoom", yn), Ji.mergeOptions({
    doubleClickZoom: !0
  });
  var xn = oe.extend({
    addHooks: function() {
      this._map.on("dblclick", this._onDoubleClick, this)
    },
    removeHooks: function() {
      this._map.off("dblclick", this._onDoubleClick, this)
    },
    _onDoubleClick: function(t) {
      var i = this._map,
        e = i.getZoom(),
        n = i.options.zoomDelta,
        o = t.originalEvent.shiftKey ? e - n : e + n;
      "center" === i.options.doubleClickZoom ? i.setZoom(o) : i.setZoomAround(t.containerPoint, o)
    }
  });
  Ji.addInitHook("addHandler", "doubleClickZoom", xn), Ji.mergeOptions({
    dragging: !0,
    inertia: !rt,
    inertiaDeceleration: 3400,
    inertiaMaxSpeed: 1 / 0,
    easeLinearity: .2,
    worldCopyJump: !1,
    maxBoundsViscosity: 0
  });
  var wn = oe.extend({
    addHooks: function() {
      if (!this._draggable) {
        var t = this._map;
        this._draggable = new le(t._mapPane, t._container), this._draggable.on({
          dragstart: this._onDragStart,
          drag: this._onDrag,
          dragend: this._onDragEnd
        }, this), this._draggable.on("predrag", this._onPreDragLimit, this), t.options.worldCopyJump && (this._draggable.on("predrag", this._onPreDragWrap, this), t.on("zoomend", this._onZoomEnd, this), t.whenReady(this._onZoomEnd, this))
      }
      pi(this._map._container, "leaflet-grab leaflet-touch-drag"), this._draggable.enable(), this._positions = [], this._times = []
    },
    removeHooks: function() {
      mi(this._map._container, "leaflet-grab"), mi(this._map._container, "leaflet-touch-drag"), this._draggable.disable()
    },
    moved: function() {
      return this._draggable && this._draggable._moved
    },
    moving: function() {
      return this._draggable && this._draggable._moving
    },
    _onDragStart: function() {
      var t = this._map;
      if (t._stop(), this._map.options.maxBounds && this._map.options.maxBoundsViscosity) {
        var i = D(this._map.options.maxBounds);
        this._offsetLimit = R(this._map.latLngToContainerPoint(i.getNorthWest()).multiplyBy(-1), this._map.latLngToContainerPoint(i.getSouthEast()).multiplyBy(-1).add(this._map.getSize())), this._viscosity = Math.min(1, Math.max(0, this._map.options.maxBoundsViscosity))
      } else this._offsetLimit = null;
      t.fire("movestart").fire("dragstart"), t.options.inertia && (this._positions = [], this._times = [])
    },
    _onDrag: function(t) {
      if (this._map.options.inertia) {
        var i = this._lastTime = +new Date,
          e = this._lastPos = this._draggable._absPos || this._draggable._newPos;
        this._positions.push(e), this._times.push(i), this._prunePositions(i)
      }
      this._map.fire("move", t).fire("drag", t)
    },
    _prunePositions: function(t) {
      for (; 1 < this._positions.length && 50 < t - this._times[0];) this._positions.shift(), this._times.shift()
    },
    _onZoomEnd: function() {
      var t = this._map.getSize().divideBy(2),
        i = this._map.latLngToLayerPoint([0, 0]);
      this._initialWorldOffset = i.subtract(t).x, this._worldWidth = this._map.getPixelWorldBounds().getSize().x
    },
    _viscousLimit: function(t, i) {
      return t - (t - i) * this._viscosity
    },
    _onPreDragLimit: function() {
      if (this._viscosity && this._offsetLimit) {
        var t = this._draggable._newPos.subtract(this._draggable._startPos),
          i = this._offsetLimit;
        t.x < i.min.x && (t.x = this._viscousLimit(t.x, i.min.x)), t.y < i.min.y && (t.y = this._viscousLimit(t.y, i.min.y)), t.x > i.max.x && (t.x = this._viscousLimit(t.x, i.max.x)), t.y > i.max.y && (t.y = this._viscousLimit(t.y, i.max.y)), this._draggable._newPos = this._draggable._startPos.add(t)
      }
    },
    _onPreDragWrap: function() {
      var t = this._worldWidth,
        i = Math.round(t / 2),
        e = this._initialWorldOffset,
        n = this._draggable._newPos.x,
        o = (n - i + e) % t + i - e,
        s = (n + i + e) % t - i - e,
        r = Math.abs(o + e) < Math.abs(s + e) ? o : s;
      this._draggable._absPos = this._draggable._newPos.clone(), this._draggable._newPos.x = r
    },
    _onDragEnd: function(t) {
      var i = this._map,
        e = i.options,
        n = !e.inertia || this._times.length < 2;
      if (i.fire("dragend", t), n) i.fire("moveend");
      else {
        this._prunePositions(+new Date);
        var o = this._lastPos.subtract(this._positions[0]),
          s = (this._lastTime - this._times[0]) / 1e3,
          r = e.easeLinearity,
          a = o.multiplyBy(r / s),
          h = a.distanceTo([0, 0]),
          u = Math.min(e.inertiaMaxSpeed, h),
          l = a.multiplyBy(u / h),
          c = u / (e.inertiaDeceleration * r),
          _ = l.multiplyBy(-c / 2).round();
        _.x || _.y ? (_ = i._limitOffset(_, i.options.maxBounds), M(function() {
          i.panBy(_, {
            duration: c,
            easeLinearity: r,
            noMoveStart: !0,
            animate: !0
          })
        })) : i.fire("moveend")
      }
    }
  });
  Ji.addInitHook("addHandler", "dragging", wn), Ji.mergeOptions({
    keyboard: !0,
    keyboardPanDelta: 80
  });
  var Pn = oe.extend({
    keyCodes: {
      left: [37],
      right: [39],
      down: [40],
      up: [38],
      zoomIn: [187, 107, 61, 171],
      zoomOut: [189, 109, 54, 173]
    },
    initialize: function(t) {
      this._map = t, this._setPanDelta(t.options.keyboardPanDelta), this._setZoomDelta(t.options.zoomDelta)
    },
    addHooks: function() {
      var t = this._map._container;
      t.tabIndex <= 0 && (t.tabIndex = "0"), Ei(t, {
        focus: this._onFocus,
        blur: this._onBlur,
        mousedown: this._onMouseDown
      }, this), this._map.on({
        focus: this._addHooks,
        blur: this._removeHooks
      }, this)
    },
    removeHooks: function() {
      this._removeHooks(), Bi(this._map._container, {
        focus: this._onFocus,
        blur: this._onBlur,
        mousedown: this._onMouseDown
      }, this), this._map.off({
        focus: this._addHooks,
        blur: this._removeHooks
      }, this)
    },
    _onMouseDown: function() {
      if (!this._focused) {
        var t = document.body,
          i = document.documentElement,
          e = t.scrollTop || i.scrollTop,
          n = t.scrollLeft || i.scrollLeft;
        this._map._container.focus(), window.scrollTo(n, e)
      }
    },
    _onFocus: function() {
      this._focused = !0, this._map.fire("focus")
    },
    _onBlur: function() {
      this._focused = !1, this._map.fire("blur")
    },
    _setPanDelta: function(t) {
      var i, e, n = this._panKeys = {},
        o = this.keyCodes;
      for (i = 0, e = o.left.length; i < e; i++) n[o.left[i]] = [-1 * t, 0];
      for (i = 0, e = o.right.length; i < e; i++) n[o.right[i]] = [t, 0];
      for (i = 0, e = o.down.length; i < e; i++) n[o.down[i]] = [0, t];
      for (i = 0, e = o.up.length; i < e; i++) n[o.up[i]] = [0, -1 * t]
    },
    _setZoomDelta: function(t) {
      var i, e, n = this._zoomKeys = {},
        o = this.keyCodes;
      for (i = 0, e = o.zoomIn.length; i < e; i++) n[o.zoomIn[i]] = t;
      for (i = 0, e = o.zoomOut.length; i < e; i++) n[o.zoomOut[i]] = -t
    },
    _addHooks: function() {
      Ei(document, "keydown", this._onKeyDown, this)
    },
    _removeHooks: function() {
      Bi(document, "keydown", this._onKeyDown, this)
    },
    _onKeyDown: function(t) {
      if (!(t.altKey || t.ctrlKey || t.metaKey)) {
        var i, e = t.keyCode,
          n = this._map;
        if (e in this._panKeys) n._panAnim && n._panAnim._inProgress || (i = this._panKeys[e], t.shiftKey && (i = I(i).multiplyBy(3)), n.panBy(i), n.options.maxBounds && n.panInsideBounds(n.options.maxBounds));
        else if (e in this._zoomKeys) n.setZoom(n.getZoom() + (t.shiftKey ? 3 : 1) * this._zoomKeys[e]);
        else {
          if (27 !== e || !n._popup || !n._popup.options.closeOnEscapeKey) return;
          n.closePopup()
        }
        ji(t)
      }
    }
  });
  Ji.addInitHook("addHandler", "keyboard", Pn), Ji.mergeOptions({
    scrollWheelZoom: !0,
    wheelDebounceTime: 40,
    wheelPxPerZoomLevel: 60
  });
  var bn = oe.extend({
    addHooks: function() {
      Ei(this._map._container, "mousewheel", this._onWheelScroll, this), this._delta = 0
    },
    removeHooks: function() {
      Bi(this._map._container, "mousewheel", this._onWheelScroll, this)
    },
    _onWheelScroll: function(t) {
      var i = Fi(t),
        e = this._map.options.wheelDebounceTime;
      this._delta += i, this._lastMousePos = this._map.mouseEventToContainerPoint(t), this._startTime || (this._startTime = +new Date);
      var n = Math.max(e - (+new Date - this._startTime), 0);
      clearTimeout(this._timer), this._timer = setTimeout(a(this._performZoom, this), n), ji(t)
    },
    _performZoom: function() {
      var t = this._map,
        i = t.getZoom(),
        e = this._map.options.zoomSnap || 0;
      t._stop();
      var n = this._delta / (4 * this._map.options.wheelPxPerZoomLevel),
        o = 4 * Math.log(2 / (1 + Math.exp(-Math.abs(n)))) / Math.LN2,
        s = e ? Math.ceil(o / e) * e : o,
        r = t._limitZoom(i + (0 < this._delta ? s : -s)) - i;
      this._delta = 0, this._startTime = null, r && ("center" === t.options.scrollWheelZoom ? t.setZoom(i + r) : t.setZoomAround(this._lastMousePos, i + r))
    }
  });
  Ji.addInitHook("addHandler", "scrollWheelZoom", bn), Ji.mergeOptions({
    tap: !0,
    tapTolerance: 15
  });
  var Ln = oe.extend({
    addHooks: function() {
      Ei(this._map._container, "touchstart", this._onDown, this)
    },
    removeHooks: function() {
      Bi(this._map._container, "touchstart", this._onDown, this)
    },
    _onDown: function(t) {
      if (t.touches) {
        if (Di(t), this._fireClick = !0, 1 < t.touches.length) return this._fireClick = !1, void clearTimeout(this._holdTimeout);
        var i = t.touches[0],
          e = i.target;
        this._startPos = this._newPos = new B(i.clientX, i.clientY), e.tagName && "a" === e.tagName.toLowerCase() && pi(e, "leaflet-active"), this._holdTimeout = setTimeout(a(function() {
          this._isTapValid() && (this._fireClick = !1, this._onUp(), this._simulateEvent("contextmenu", i))
        }, this), 1e3), this._simulateEvent("mousedown", i), Ei(document, {
          touchmove: this._onMove,
          touchend: this._onUp
        }, this)
      }
    },
    _onUp: function(t) {
      if (clearTimeout(this._holdTimeout), Bi(document, {
          touchmove: this._onMove,
          touchend: this._onUp
        }, this), this._fireClick && t && t.changedTouches) {
        var i = t.changedTouches[0],
          e = i.target;
        e && e.tagName && "a" === e.tagName.toLowerCase() && mi(e, "leaflet-active"), this._simulateEvent("mouseup", i), this._isTapValid() && this._simulateEvent("click", i)
      }
    },
    _isTapValid: function() {
      return this._newPos.distanceTo(this._startPos) <= this._map.options.tapTolerance
    },
    _onMove: function(t) {
      var i = t.touches[0];
      this._newPos = new B(i.clientX, i.clientY), this._simulateEvent("mousemove", i)
    },
    _simulateEvent: function(t, i) {
      var e = document.createEvent("MouseEvents");
      e._simulated = !0, i.target._simulatedClick = !0, e.initMouseEvent(t, !0, !0, window, 1, i.screenX, i.screenY, i.clientX, i.clientY, !1, !1, !1, !1, 0, null), i.target.dispatchEvent(e)
    }
  });
  Tt && !Lt && Ji.addInitHook("addHandler", "tap", Ln), Ji.mergeOptions({
    touchZoom: Tt && !rt,
    bounceAtZoomLimits: !0
  });
  var Tn = oe.extend({
    addHooks: function() {
      pi(this._map._container, "leaflet-touch-zoom"), Ei(this._map._container, "touchstart", this._onTouchStart, this)
    },
    removeHooks: function() {
      mi(this._map._container, "leaflet-touch-zoom"), Bi(this._map._container, "touchstart", this._onTouchStart, this)
    },
    _onTouchStart: function(t) {
      var i = this._map;
      if (t.touches && 2 === t.touches.length && !i._animatingZoom && !this._zooming) {
        var e = i.mouseEventToContainerPoint(t.touches[0]),
          n = i.mouseEventToContainerPoint(t.touches[1]);
        this._centerPoint = i.getSize()._divideBy(2), this._startLatLng = i.containerPointToLatLng(this._centerPoint), "center" !== i.options.touchZoom && (this._pinchStartLatLng = i.containerPointToLatLng(e.add(n)._divideBy(2))), this._startDist = e.distanceTo(n), this._startZoom = i.getZoom(), this._moved = !1, this._zooming = !0, i._stop(), Ei(document, "touchmove", this._onTouchMove, this), Ei(document, "touchend", this._onTouchEnd, this), Di(t)
      }
    },
    _onTouchMove: function(t) {
      if (t.touches && 2 === t.touches.length && this._zooming) {
        var i = this._map,
          e = i.mouseEventToContainerPoint(t.touches[0]),
          n = i.mouseEventToContainerPoint(t.touches[1]),
          o = e.distanceTo(n) / this._startDist;
        if (this._zoom = i.getScaleZoom(o, this._startZoom), !i.options.bounceAtZoomLimits && (this._zoom < i.getMinZoom() && o < 1 || this._zoom > i.getMaxZoom() && 1 < o) && (this._zoom = i._limitZoom(this._zoom)), "center" === i.options.touchZoom) {
          if (this._center = this._startLatLng, 1 == o) return
        } else {
          var s = e._add(n)._divideBy(2)._subtract(this._centerPoint);
          if (1 == o && 0 === s.x && 0 === s.y) return;
          this._center = i.unproject(i.project(this._pinchStartLatLng, this._zoom).subtract(s), this._zoom)
        }
        this._moved || (i._moveStart(!0, !1), this._moved = !0), C(this._animRequest);
        var r = a(i._move, i, this._center, this._zoom, {
          pinch: !0,
          round: !1
        });
        this._animRequest = M(r, this, !0), Di(t)
      }
    },
    _onTouchEnd: function() {
      this._moved && this._zooming ? (this._zooming = !1, C(this._animRequest), Bi(document, "touchmove", this._onTouchMove), Bi(document, "touchend", this._onTouchEnd), this._map.options.zoomAnimation ? this._map._animateZoom(this._center, this._map._limitZoom(this._zoom), !0, this._map.options.zoomSnap) : this._map._resetView(this._center, this._map._limitZoom(this._zoom))) : this._zooming = !1
    }
  });
  Ji.addInitHook("addHandler", "touchZoom", Tn), Ji.BoxZoom = yn, Ji.DoubleClickZoom = xn, Ji.Drag = wn, Ji.Keyboard = Pn, Ji.ScrollWheelZoom = bn, Ji.Tap = Ln, Ji.TouchZoom = Tn, Object.freeze = i, t.version = "1.5.1+build.2e3e0ffb", t.Control = Qi, t.control = $i, t.Browser = Bt, t.Evented = k, t.Mixin = re, t.Util = S, t.Class = Z, t.Handler = oe, t.extend = h, t.bind = a, t.stamp = u, t.setOptions = p, t.DomEvent = Yi, t.DomUtil = Zi, t.PosAnimation = Xi, t.Draggable = le, t.LineUtil = ye, t.PolyUtil = Pe, t.Point = B, t.point = I, t.Bounds = O, t.bounds = R, t.Transformation = G, t.transformation = K, t.Projection = Te, t.LatLng = j, t.latLng = W, t.LatLngBounds = N, t.latLngBounds = D, t.CRS = F, t.GeoJSON = We, t.geoJSON = Xe, t.geoJson = Je, t.Layer = Se, t.LayerGroup = Ze, t.layerGroup = function(t, i) {
    return new Ze(t, i)
  }, t.FeatureGroup = Ee, t.featureGroup = function(t) {
    return new Ee(t)
  }, t.ImageOverlay = $e, t.imageOverlay = function(t, i, e) {
    return new $e(t, i, e)
  }, t.VideoOverlay = Qe, t.videoOverlay = function(t, i, e) {
    return new Qe(t, i, e)
  }, t.SVGOverlay = tn, t.svgOverlay = function(t, i, e) {
    return new tn(t, i, e)
  }, t.DivOverlay = en, t.Popup = nn, t.popup = function(t, i) {
    return new nn(t, i)
  }, t.Tooltip = on, t.tooltip = function(t, i) {
    return new on(t, i)
  }, t.Icon = ke, t.icon = function(t) {
    return new ke(t)
  }, t.DivIcon = sn, t.divIcon = function(t) {
    return new sn(t)
  }, t.Marker = Ie, t.marker = function(t, i) {
    return new Ie(t, i)
  }, t.TileLayer = an, t.tileLayer = hn, t.GridLayer = rn, t.gridLayer = function(t) {
    return new rn(t)
  }, t.SVG = fn, t.svg = gn, t.Renderer = ln, t.Canvas = cn, t.canvas = _n, t.Path = Oe, t.CircleMarker = Re, t.circleMarker = function(t, i) {
    return new Re(t, i)
  }, t.Circle = Ne, t.circle = function(t, i, e) {
    return new Ne(t, i, e)
  }, t.Polyline = De, t.polyline = function(t, i) {
    return new De(t, i)
  }, t.Polygon = je, t.polygon = function(t, i) {
    return new je(t, i)
  }, t.Rectangle = vn, t.rectangle = function(t, i) {
    return new vn(t, i)
  }, t.Map = Ji, t.map = function(t, i) {
    return new Ji(t, i)
  };
  var zn = window.L;
  t.noConflict = function() {
    return window.L = zn, this
  }, window.L = t
});


! function(e, t) {
  "object" == typeof exports && "undefined" != typeof module ? t(exports) : "function" == typeof define && define.amd ? define(["exports"], t) : t((e.Leaflet = e.Leaflet || {}, e.Leaflet.markercluster = e.Leaflet.markercluster || {}))
}(this, function(e) {
  "use strict";
  var t = L.MarkerClusterGroup = L.FeatureGroup.extend({
    options: {
      maxClusterRadius: 80,
      iconCreateFunction: null,
      clusterPane: L.Marker.prototype.options.pane,
      spiderfyOnMaxZoom: !0,
      showCoverageOnHover: !0,
      zoomToBoundsOnClick: !0,
      singleMarkerMode: !1,
      disableClusteringAtZoom: null,
      removeOutsideVisibleBounds: !0,
      animate: !0,
      animateAddingMarkers: !1,
      spiderfyDistanceMultiplier: 1,
      spiderLegPolylineOptions: {
        weight: 1.5,
        color: "#222",
        opacity: .5
      },
      chunkedLoading: !1,
      chunkInterval: 200,
      chunkDelay: 50,
      chunkProgress: null,
      polygonOptions: {}
    },
    initialize: function(e) {
      L.Util.setOptions(this, e), this.options.iconCreateFunction || (this.options.iconCreateFunction = this._defaultIconCreateFunction), this._featureGroup = L.featureGroup(), this._featureGroup.addEventParent(this), this._nonPointGroup = L.featureGroup(), this._nonPointGroup.addEventParent(this), this._inZoomAnimation = 0, this._needsClustering = [], this._needsRemoving = [], this._currentShownBounds = null, this._queue = [], this._childMarkerEventHandlers = {
        dragstart: this._childMarkerDragStart,
        move: this._childMarkerMoved,
        dragend: this._childMarkerDragEnd
      };
      var t = L.DomUtil.TRANSITION && this.options.animate;
      L.extend(this, t ? this._withAnimation : this._noAnimation), this._markerCluster = t ? L.MarkerCluster : L.MarkerClusterNonAnimated
    },
    addLayer: function(e) {
      if (e instanceof L.LayerGroup) return this.addLayers([e]);
      if (!e.getLatLng) return this._nonPointGroup.addLayer(e), this.fire("layeradd", {
        layer: e
      }), this;
      if (!this._map) return this._needsClustering.push(e), this.fire("layeradd", {
        layer: e
      }), this;
      if (this.hasLayer(e)) return this;
      this._unspiderfy && this._unspiderfy(), this._addLayer(e, this._maxZoom), this.fire("layeradd", {
        layer: e
      }), this._topClusterLevel._recalculateBounds(), this._refreshClustersIcons();
      var t = e,
        i = this._zoom;
      if (e.__parent)
        for (; t.__parent._zoom >= i;) t = t.__parent;
      return this._currentShownBounds.contains(t.getLatLng()) && (this.options.animateAddingMarkers ? this._animationAddLayer(e, t) : this._animationAddLayerNonAnimated(e, t)), this
    },
    removeLayer: function(e) {
      return e instanceof L.LayerGroup ? this.removeLayers([e]) : e.getLatLng ? this._map ? e.__parent ? (this._unspiderfy && (this._unspiderfy(), this._unspiderfyLayer(e)), this._removeLayer(e, !0), this.fire("layerremove", {
        layer: e
      }), this._topClusterLevel._recalculateBounds(), this._refreshClustersIcons(), e.off(this._childMarkerEventHandlers, this), this._featureGroup.hasLayer(e) && (this._featureGroup.removeLayer(e), e.clusterShow && e.clusterShow()), this) : this : (!this._arraySplice(this._needsClustering, e) && this.hasLayer(e) && this._needsRemoving.push({
        layer: e,
        latlng: e._latlng
      }), this.fire("layerremove", {
        layer: e
      }), this) : (this._nonPointGroup.removeLayer(e), this.fire("layerremove", {
        layer: e
      }), this)
    },
    addLayers: function(e, t) {
      if (!L.Util.isArray(e)) return this.addLayer(e);
      var i, n = this._featureGroup,
        r = this._nonPointGroup,
        s = this.options.chunkedLoading,
        o = this.options.chunkInterval,
        a = this.options.chunkProgress,
        h = e.length,
        l = 0,
        u = !0;
      if (this._map) {
        var _ = (new Date).getTime(),
          d = L.bind(function() {
            for (var c = (new Date).getTime(); h > l; l++) {
              if (s && 0 === l % 200) {
                var p = (new Date).getTime() - c;
                if (p > o) break
              }
              if (i = e[l], i instanceof L.LayerGroup) u && (e = e.slice(), u = !1), this._extractNonGroupLayers(i, e), h = e.length;
              else if (i.getLatLng) {
                if (!this.hasLayer(i) && (this._addLayer(i, this._maxZoom), t || this.fire("layeradd", {
                    layer: i
                  }), i.__parent && 2 === i.__parent.getChildCount())) {
                  var f = i.__parent.getAllChildMarkers(),
                    m = f[0] === i ? f[1] : f[0];
                  n.removeLayer(m)
                }
              } else r.addLayer(i), t || this.fire("layeradd", {
                layer: i
              })
            }
            a && a(l, h, (new Date).getTime() - _), l === h ? (this._topClusterLevel._recalculateBounds(), this._refreshClustersIcons(), this._topClusterLevel._recursivelyAddChildrenToMap(null, this._zoom, this._currentShownBounds)) : setTimeout(d, this.options.chunkDelay)
          }, this);
        d()
      } else
        for (var c = this._needsClustering; h > l; l++) i = e[l], i instanceof L.LayerGroup ? (u && (e = e.slice(), u = !1), this._extractNonGroupLayers(i, e), h = e.length) : i.getLatLng ? this.hasLayer(i) || c.push(i) : r.addLayer(i);
      return this
    },
    removeLayers: function(e) {
      var t, i, n = e.length,
        r = this._featureGroup,
        s = this._nonPointGroup,
        o = !0;
      if (!this._map) {
        for (t = 0; n > t; t++) i = e[t], i instanceof L.LayerGroup ? (o && (e = e.slice(), o = !1), this._extractNonGroupLayers(i, e), n = e.length) : (this._arraySplice(this._needsClustering, i), s.removeLayer(i), this.hasLayer(i) && this._needsRemoving.push({
          layer: i,
          latlng: i._latlng
        }), this.fire("layerremove", {
          layer: i
        }));
        return this
      }
      if (this._unspiderfy) {
        this._unspiderfy();
        var a = e.slice(),
          h = n;
        for (t = 0; h > t; t++) i = a[t], i instanceof L.LayerGroup ? (this._extractNonGroupLayers(i, a), h = a.length) : this._unspiderfyLayer(i)
      }
      for (t = 0; n > t; t++) i = e[t], i instanceof L.LayerGroup ? (o && (e = e.slice(), o = !1), this._extractNonGroupLayers(i, e), n = e.length) : i.__parent ? (this._removeLayer(i, !0, !0), this.fire("layerremove", {
        layer: i
      }), r.hasLayer(i) && (r.removeLayer(i), i.clusterShow && i.clusterShow())) : (s.removeLayer(i), this.fire("layerremove", {
        layer: i
      }));
      return this._topClusterLevel._recalculateBounds(), this._refreshClustersIcons(), this._topClusterLevel._recursivelyAddChildrenToMap(null, this._zoom, this._currentShownBounds), this
    },
    clearLayers: function() {
      return this._map || (this._needsClustering = [], this._needsRemoving = [], delete this._gridClusters, delete this._gridUnclustered), this._noanimationUnspiderfy && this._noanimationUnspiderfy(), this._featureGroup.clearLayers(), this._nonPointGroup.clearLayers(), this.eachLayer(function(e) {
        e.off(this._childMarkerEventHandlers, this), delete e.__parent
      }, this), this._map && this._generateInitialClusters(), this
    },
    getBounds: function() {
      var e = new L.LatLngBounds;
      this._topClusterLevel && e.extend(this._topClusterLevel._bounds);
      for (var t = this._needsClustering.length - 1; t >= 0; t--) e.extend(this._needsClustering[t].getLatLng());
      return e.extend(this._nonPointGroup.getBounds()), e
    },
    eachLayer: function(e, t) {
      var i, n, r, s = this._needsClustering.slice(),
        o = this._needsRemoving;
      for (this._topClusterLevel && this._topClusterLevel.getAllChildMarkers(s), n = s.length - 1; n >= 0; n--) {
        for (i = !0, r = o.length - 1; r >= 0; r--)
          if (o[r].layer === s[n]) {
            i = !1;
            break
          }
        i && e.call(t, s[n])
      }
      this._nonPointGroup.eachLayer(e, t)
    },
    getLayers: function() {
      var e = [];
      return this.eachLayer(function(t) {
        e.push(t)
      }), e
    },
    getLayer: function(e) {
      var t = null;
      return e = parseInt(e, 10), this.eachLayer(function(i) {
        L.stamp(i) === e && (t = i)
      }), t
    },
    hasLayer: function(e) {
      if (!e) return !1;
      var t, i = this._needsClustering;
      for (t = i.length - 1; t >= 0; t--)
        if (i[t] === e) return !0;
      for (i = this._needsRemoving, t = i.length - 1; t >= 0; t--)
        if (i[t].layer === e) return !1;
      return !(!e.__parent || e.__parent._group !== this) || this._nonPointGroup.hasLayer(e)
    },
    zoomToShowLayer: function(e, t) {
      "function" != typeof t && (t = function() {});
      var i = function() {
        !e._icon && !e.__parent._icon || this._inZoomAnimation || (this._map.off("moveend", i, this), this.off("animationend", i, this), e._icon ? t() : e.__parent._icon && (this.once("spiderfied", t, this), e.__parent.spiderfy()))
      };
      e._icon && this._map.getBounds().contains(e.getLatLng()) ? t() : e.__parent._zoom < Math.round(this._map._zoom) ? (this._map.on("moveend", i, this), this._map.panTo(e.getLatLng())) : (this._map.on("moveend", i, this), this.on("animationend", i, this), e.__parent.zoomToBounds())
    },
    onAdd: function(e) {
      this._map = e;
      var t, i, n;
      if (!isFinite(this._map.getMaxZoom())) throw "Map has no maxZoom specified";
      for (this._featureGroup.addTo(e), this._nonPointGroup.addTo(e), this._gridClusters || this._generateInitialClusters(), this._maxLat = e.options.crs.projection.MAX_LATITUDE, t = 0, i = this._needsRemoving.length; i > t; t++) n = this._needsRemoving[t], n.newlatlng = n.layer._latlng, n.layer._latlng = n.latlng;
      for (t = 0, i = this._needsRemoving.length; i > t; t++) n = this._needsRemoving[t], this._removeLayer(n.layer, !0), n.layer._latlng = n.newlatlng;
      this._needsRemoving = [], this._zoom = Math.round(this._map._zoom), this._currentShownBounds = this._getExpandedVisibleBounds(), this._map.on("zoomend", this._zoomEnd, this), this._map.on("moveend", this._moveEnd, this), this._spiderfierOnAdd && this._spiderfierOnAdd(), this._bindEvents(), i = this._needsClustering, this._needsClustering = [], this.addLayers(i, !0)
    },
    onRemove: function(e) {
      e.off("zoomend", this._zoomEnd, this), e.off("moveend", this._moveEnd, this), this._unbindEvents(), this._map._mapPane.className = this._map._mapPane.className.replace(" leaflet-cluster-anim", ""), this._spiderfierOnRemove && this._spiderfierOnRemove(), delete this._maxLat, this._hideCoverage(), this._featureGroup.remove(), this._nonPointGroup.remove(), this._featureGroup.clearLayers(), this._map = null
    },
    getVisibleParent: function(e) {
      for (var t = e; t && !t._icon;) t = t.__parent;
      return t || null
    },
    _arraySplice: function(e, t) {
      for (var i = e.length - 1; i >= 0; i--)
        if (e[i] === t) return e.splice(i, 1), !0
    },
    _removeFromGridUnclustered: function(e, t) {
      for (var i = this._map, n = this._gridUnclustered, r = Math.floor(this._map.getMinZoom()); t >= r && n[t].removeObject(e, i.project(e.getLatLng(), t)); t--);
    },
    _childMarkerDragStart: function(e) {
      e.target.__dragStart = e.target._latlng
    },
    _childMarkerMoved: function(e) {
      if (!this._ignoreMove && !e.target.__dragStart) {
        var t = e.target._popup && e.target._popup.isOpen();
        this._moveChild(e.target, e.oldLatLng, e.latlng), t && e.target.openPopup()
      }
    },
    _moveChild: function(e, t, i) {
      e._latlng = t, this.removeLayer(e), e._latlng = i, this.addLayer(e)
    },
    _childMarkerDragEnd: function(e) {
      e.target.__dragStart && this._moveChild(e.target, e.target.__dragStart, e.target._latlng), delete e.target.__dragStart
    },
    _removeLayer: function(e, t, i) {
      var n = this._gridClusters,
        r = this._gridUnclustered,
        s = this._featureGroup,
        o = this._map,
        a = Math.floor(this._map.getMinZoom());
      t && this._removeFromGridUnclustered(e, this._maxZoom);
      var h, l = e.__parent,
        u = l._markers;
      for (this._arraySplice(u, e); l && (l._childCount--, l._boundsNeedUpdate = !0, !(l._zoom < a));) t && l._childCount <= 1 ? (h = l._markers[0] === e ? l._markers[1] : l._markers[0], n[l._zoom].removeObject(l, o.project(l._cLatLng, l._zoom)), r[l._zoom].addObject(h, o.project(h.getLatLng(), l._zoom)), this._arraySplice(l.__parent._childClusters, l), l.__parent._markers.push(h), h.__parent = l.__parent, l._icon && (s.removeLayer(l), i || s.addLayer(h))) : l._iconNeedsUpdate = !0, l = l.__parent;
      delete e.__parent
    },
    _isOrIsParent: function(e, t) {
      for (; t;) {
        if (e === t) return !0;
        t = t.parentNode
      }
      return !1
    },
    fire: function(e, t, i) {
      if (t && t.layer instanceof L.MarkerCluster) {
        if (t.originalEvent && this._isOrIsParent(t.layer._icon, t.originalEvent.relatedTarget)) return;
        e = "cluster" + e
      }
      L.FeatureGroup.prototype.fire.call(this, e, t, i)
    },
    listens: function(e, t) {
      return L.FeatureGroup.prototype.listens.call(this, e, t) || L.FeatureGroup.prototype.listens.call(this, "cluster" + e, t)
    },
    _defaultIconCreateFunction: function(e) {
      var t = e.getChildCount(),
        i = " marker-cluster-";
      return i += 10 > t ? "small" : 100 > t ? "medium" : "large", new L.DivIcon({
        html: "<div><span>" + t + "</span></div>",
        className: "marker-cluster" + i,
        iconSize: new L.Point(40, 40)
      })
    },
    _bindEvents: function() {
      var e = this._map,
        t = this.options.spiderfyOnMaxZoom,
        i = this.options.showCoverageOnHover,
        n = this.options.zoomToBoundsOnClick;
      (t || n) && this.on("clusterclick", this._zoomOrSpiderfy, this), i && (this.on("clustermouseover", this._showCoverage, this), this.on("clustermouseout", this._hideCoverage, this), e.on("zoomend", this._hideCoverage, this))
    },
    _zoomOrSpiderfy: function(e) {
      for (var t = e.layer, i = t; 1 === i._childClusters.length;) i = i._childClusters[0];
      i._zoom === this._maxZoom && i._childCount === t._childCount && this.options.spiderfyOnMaxZoom ? t.spiderfy() : this.options.zoomToBoundsOnClick && t.zoomToBounds(), e.originalEvent && 13 === e.originalEvent.keyCode && this._map._container.focus()
    },
    _showCoverage: function(e) {
      var t = this._map;
      this._inZoomAnimation || (this._shownPolygon && t.removeLayer(this._shownPolygon), e.layer.getChildCount() > 2 && e.layer !== this._spiderfied && (this._shownPolygon = new L.Polygon(e.layer.getConvexHull(), this.options.polygonOptions), t.addLayer(this._shownPolygon)))
    },
    _hideCoverage: function() {
      this._shownPolygon && (this._map.removeLayer(this._shownPolygon), this._shownPolygon = null)
    },
    _unbindEvents: function() {
      var e = this.options.spiderfyOnMaxZoom,
        t = this.options.showCoverageOnHover,
        i = this.options.zoomToBoundsOnClick,
        n = this._map;
      (e || i) && this.off("clusterclick", this._zoomOrSpiderfy, this), t && (this.off("clustermouseover", this._showCoverage, this), this.off("clustermouseout", this._hideCoverage, this), n.off("zoomend", this._hideCoverage, this))
    },
    _zoomEnd: function() {
      this._map && (this._mergeSplitClusters(), this._zoom = Math.round(this._map._zoom), this._currentShownBounds = this._getExpandedVisibleBounds())
    },
    _moveEnd: function() {
      if (!this._inZoomAnimation) {
        var e = this._getExpandedVisibleBounds();
        this._topClusterLevel._recursivelyRemoveChildrenFromMap(this._currentShownBounds, Math.floor(this._map.getMinZoom()), this._zoom, e), this._topClusterLevel._recursivelyAddChildrenToMap(null, Math.round(this._map._zoom), e), this._currentShownBounds = e
      }
    },
    _generateInitialClusters: function() {
      var e = Math.ceil(this._map.getMaxZoom()),
        t = Math.floor(this._map.getMinZoom()),
        i = this.options.maxClusterRadius,
        n = i;
      "function" != typeof i && (n = function() {
        return i
      }), null !== this.options.disableClusteringAtZoom && (e = this.options.disableClusteringAtZoom - 1), this._maxZoom = e, this._gridClusters = {}, this._gridUnclustered = {};
      for (var r = e; r >= t; r--) this._gridClusters[r] = new L.DistanceGrid(n(r)), this._gridUnclustered[r] = new L.DistanceGrid(n(r));
      this._topClusterLevel = new this._markerCluster(this, t - 1)
    },
    _addLayer: function(e, t) {
      var i, n, r = this._gridClusters,
        s = this._gridUnclustered,
        o = Math.floor(this._map.getMinZoom());
      for (this.options.singleMarkerMode && this._overrideMarkerIcon(e), e.on(this._childMarkerEventHandlers, this); t >= o; t--) {
        i = this._map.project(e.getLatLng(), t);
        var a = r[t].getNearObject(i);
        if (a) return a._addChild(e), e.__parent = a, void 0;
        if (a = s[t].getNearObject(i)) {
          var h = a.__parent;
          h && this._removeLayer(a, !1);
          var l = new this._markerCluster(this, t, a, e);
          r[t].addObject(l, this._map.project(l._cLatLng, t)), a.__parent = l, e.__parent = l;
          var u = l;
          for (n = t - 1; n > h._zoom; n--) u = new this._markerCluster(this, n, u), r[n].addObject(u, this._map.project(a.getLatLng(), n));
          return h._addChild(u), this._removeFromGridUnclustered(a, t), void 0
        }
        s[t].addObject(e, i)
      }
      this._topClusterLevel._addChild(e), e.__parent = this._topClusterLevel
    },
    _refreshClustersIcons: function() {
      this._featureGroup.eachLayer(function(e) {
        e instanceof L.MarkerCluster && e._iconNeedsUpdate && e._updateIcon()
      })
    },
    _enqueue: function(e) {
      this._queue.push(e), this._queueTimeout || (this._queueTimeout = setTimeout(L.bind(this._processQueue, this), 300))
    },
    _processQueue: function() {
      for (var e = 0; e < this._queue.length; e++) this._queue[e].call(this);
      this._queue.length = 0, clearTimeout(this._queueTimeout), this._queueTimeout = null
    },
    _mergeSplitClusters: function() {
      var e = Math.round(this._map._zoom);
      this._processQueue(), this._zoom < e && this._currentShownBounds.intersects(this._getExpandedVisibleBounds()) ? (this._animationStart(), this._topClusterLevel._recursivelyRemoveChildrenFromMap(this._currentShownBounds, Math.floor(this._map.getMinZoom()), this._zoom, this._getExpandedVisibleBounds()), this._animationZoomIn(this._zoom, e)) : this._zoom > e ? (this._animationStart(), this._animationZoomOut(this._zoom, e)) : this._moveEnd()
    },
    _getExpandedVisibleBounds: function() {
      return this.options.removeOutsideVisibleBounds ? L.Browser.mobile ? this._checkBoundsMaxLat(this._map.getBounds()) : this._checkBoundsMaxLat(this._map.getBounds().pad(1)) : this._mapBoundsInfinite
    },
    _checkBoundsMaxLat: function(e) {
      var t = this._maxLat;
      return void 0 !== t && (e.getNorth() >= t && (e._northEast.lat = 1 / 0), e.getSouth() <= -t && (e._southWest.lat = -1 / 0)), e
    },
    _animationAddLayerNonAnimated: function(e, t) {
      if (t === e) this._featureGroup.addLayer(e);
      else if (2 === t._childCount) {
        t._addToMap();
        var i = t.getAllChildMarkers();
        this._featureGroup.removeLayer(i[0]), this._featureGroup.removeLayer(i[1])
      } else t._updateIcon()
    },
    _extractNonGroupLayers: function(e, t) {
      var i, n = e.getLayers(),
        r = 0;
      for (t = t || []; r < n.length; r++) i = n[r], i instanceof L.LayerGroup ? this._extractNonGroupLayers(i, t) : t.push(i);
      return t
    },
    _overrideMarkerIcon: function(e) {
      var t = e.options.icon = this.options.iconCreateFunction({
        getChildCount: function() {
          return 1
        },
        getAllChildMarkers: function() {
          return [e]
        }
      });
      return t
    }
  });
  L.MarkerClusterGroup.include({
    _mapBoundsInfinite: new L.LatLngBounds(new L.LatLng(-1 / 0, -1 / 0), new L.LatLng(1 / 0, 1 / 0))
  }), L.MarkerClusterGroup.include({
    _noAnimation: {
      _animationStart: function() {},
      _animationZoomIn: function(e, t) {
        this._topClusterLevel._recursivelyRemoveChildrenFromMap(this._currentShownBounds, Math.floor(this._map.getMinZoom()), e), this._topClusterLevel._recursivelyAddChildrenToMap(null, t, this._getExpandedVisibleBounds()), this.fire("animationend")
      },
      _animationZoomOut: function(e, t) {
        this._topClusterLevel._recursivelyRemoveChildrenFromMap(this._currentShownBounds, Math.floor(this._map.getMinZoom()), e), this._topClusterLevel._recursivelyAddChildrenToMap(null, t, this._getExpandedVisibleBounds()), this.fire("animationend")
      },
      _animationAddLayer: function(e, t) {
        this._animationAddLayerNonAnimated(e, t)
      }
    },
    _withAnimation: {
      _animationStart: function() {
        this._map._mapPane.className += " leaflet-cluster-anim", this._inZoomAnimation++
      },
      _animationZoomIn: function(e, t) {
        var i, n = this._getExpandedVisibleBounds(),
          r = this._featureGroup,
          s = Math.floor(this._map.getMinZoom());
        this._ignoreMove = !0, this._topClusterLevel._recursively(n, e, s, function(s) {
          var o, a = s._latlng,
            h = s._markers;
          for (n.contains(a) || (a = null), s._isSingleParent() && e + 1 === t ? (r.removeLayer(s), s._recursivelyAddChildrenToMap(null, t, n)) : (s.clusterHide(), s._recursivelyAddChildrenToMap(a, t, n)), i = h.length - 1; i >= 0; i--) o = h[i], n.contains(o._latlng) || r.removeLayer(o)
        }), this._forceLayout(), this._topClusterLevel._recursivelyBecomeVisible(n, t), r.eachLayer(function(e) {
          e instanceof L.MarkerCluster || !e._icon || e.clusterShow()
        }), this._topClusterLevel._recursively(n, e, t, function(e) {
          e._recursivelyRestoreChildPositions(t)
        }), this._ignoreMove = !1, this._enqueue(function() {
          this._topClusterLevel._recursively(n, e, s, function(e) {
            r.removeLayer(e), e.clusterShow()
          }), this._animationEnd()
        })
      },
      _animationZoomOut: function(e, t) {
        this._animationZoomOutSingle(this._topClusterLevel, e - 1, t), this._topClusterLevel._recursivelyAddChildrenToMap(null, t, this._getExpandedVisibleBounds()), this._topClusterLevel._recursivelyRemoveChildrenFromMap(this._currentShownBounds, Math.floor(this._map.getMinZoom()), e, this._getExpandedVisibleBounds())
      },
      _animationAddLayer: function(e, t) {
        var i = this,
          n = this._featureGroup;
        n.addLayer(e), t !== e && (t._childCount > 2 ? (t._updateIcon(), this._forceLayout(), this._animationStart(), e._setPos(this._map.latLngToLayerPoint(t.getLatLng())), e.clusterHide(), this._enqueue(function() {
          n.removeLayer(e), e.clusterShow(), i._animationEnd()
        })) : (this._forceLayout(), i._animationStart(), i._animationZoomOutSingle(t, this._map.getMaxZoom(), this._zoom)))
      }
    },
    _animationZoomOutSingle: function(e, t, i) {
      var n = this._getExpandedVisibleBounds(),
        r = Math.floor(this._map.getMinZoom());
      e._recursivelyAnimateChildrenInAndAddSelfToMap(n, r, t + 1, i);
      var s = this;
      this._forceLayout(), e._recursivelyBecomeVisible(n, i), this._enqueue(function() {
        if (1 === e._childCount) {
          var o = e._markers[0];
          this._ignoreMove = !0, o.setLatLng(o.getLatLng()), this._ignoreMove = !1, o.clusterShow && o.clusterShow()
        } else e._recursively(n, i, r, function(e) {
          e._recursivelyRemoveChildrenFromMap(n, r, t + 1)
        });
        s._animationEnd()
      })
    },
    _animationEnd: function() {
      this._map && (this._map._mapPane.className = this._map._mapPane.className.replace(" leaflet-cluster-anim", "")), this._inZoomAnimation--, this.fire("animationend")
    },
    _forceLayout: function() {
      L.Util.falseFn(document.body.offsetWidth)
    }
  }), L.markerClusterGroup = function(e) {
    return new L.MarkerClusterGroup(e)
  };
  var i = L.MarkerCluster = L.Marker.extend({
    options: L.Icon.prototype.options,
    initialize: function(e, t, i, n) {
      L.Marker.prototype.initialize.call(this, i ? i._cLatLng || i.getLatLng() : new L.LatLng(0, 0), {
        icon: this,
        pane: e.options.clusterPane
      }), this._group = e, this._zoom = t, this._markers = [], this._childClusters = [], this._childCount = 0, this._iconNeedsUpdate = !0, this._boundsNeedUpdate = !0, this._bounds = new L.LatLngBounds, i && this._addChild(i), n && this._addChild(n)
    },
    getAllChildMarkers: function(e) {
      e = e || [];
      for (var t = this._childClusters.length - 1; t >= 0; t--) this._childClusters[t].getAllChildMarkers(e);
      for (var i = this._markers.length - 1; i >= 0; i--) e.push(this._markers[i]);
      return e
    },
    getChildCount: function() {
      return this._childCount
    },
    zoomToBounds: function(e) {
      for (var t, i = this._childClusters.slice(), n = this._group._map, r = n.getBoundsZoom(this._bounds), s = this._zoom + 1, o = n.getZoom(); i.length > 0 && r > s;) {
        s++;
        var a = [];
        for (t = 0; t < i.length; t++) a = a.concat(i[t]._childClusters);
        i = a
      }
      r > s ? this._group._map.setView(this._latlng, s) : o >= r ? this._group._map.setView(this._latlng, o + 1) : this._group._map.fitBounds(this._bounds, e)
    },
    getBounds: function() {
      var e = new L.LatLngBounds;
      return e.extend(this._bounds), e
    },
    _updateIcon: function() {
      this._iconNeedsUpdate = !0, this._icon && this.setIcon(this)
    },
    createIcon: function() {
      return this._iconNeedsUpdate && (this._iconObj = this._group.options.iconCreateFunction(this), this._iconNeedsUpdate = !1), this._iconObj.createIcon()
    },
    createShadow: function() {
      return this._iconObj.createShadow()
    },
    _addChild: function(e, t) {
      this._iconNeedsUpdate = !0, this._boundsNeedUpdate = !0, this._setClusterCenter(e), e instanceof L.MarkerCluster ? (t || (this._childClusters.push(e), e.__parent = this), this._childCount += e._childCount) : (t || this._markers.push(e), this._childCount++), this.__parent && this.__parent._addChild(e, !0)
    },
    _setClusterCenter: function(e) {
      this._cLatLng || (this._cLatLng = e._cLatLng || e._latlng)
    },
    _resetBounds: function() {
      var e = this._bounds;
      e._southWest && (e._southWest.lat = 1 / 0, e._southWest.lng = 1 / 0), e._northEast && (e._northEast.lat = -1 / 0, e._northEast.lng = -1 / 0)
    },
    _recalculateBounds: function() {
      var e, t, i, n, r = this._markers,
        s = this._childClusters,
        o = 0,
        a = 0,
        h = this._childCount;
      if (0 !== h) {
        for (this._resetBounds(), e = 0; e < r.length; e++) i = r[e]._latlng, this._bounds.extend(i), o += i.lat, a += i.lng;
        for (e = 0; e < s.length; e++) t = s[e], t._boundsNeedUpdate && t._recalculateBounds(), this._bounds.extend(t._bounds), i = t._wLatLng, n = t._childCount, o += i.lat * n, a += i.lng * n;
        this._latlng = this._wLatLng = new L.LatLng(o / h, a / h), this._boundsNeedUpdate = !1
      }
    },
    _addToMap: function(e) {
      e && (this._backupLatlng = this._latlng, this.setLatLng(e)), this._group._featureGroup.addLayer(this)
    },
    _recursivelyAnimateChildrenIn: function(e, t, i) {
      this._recursively(e, this._group._map.getMinZoom(), i - 1, function(e) {
        var i, n, r = e._markers;
        for (i = r.length - 1; i >= 0; i--) n = r[i], n._icon && (n._setPos(t), n.clusterHide())
      }, function(e) {
        var i, n, r = e._childClusters;
        for (i = r.length - 1; i >= 0; i--) n = r[i], n._icon && (n._setPos(t), n.clusterHide())
      })
    },
    _recursivelyAnimateChildrenInAndAddSelfToMap: function(e, t, i, n) {
      this._recursively(e, n, t, function(r) {
        r._recursivelyAnimateChildrenIn(e, r._group._map.latLngToLayerPoint(r.getLatLng()).round(), i), r._isSingleParent() && i - 1 === n ? (r.clusterShow(), r._recursivelyRemoveChildrenFromMap(e, t, i)) : r.clusterHide(), r._addToMap()
      })
    },
    _recursivelyBecomeVisible: function(e, t) {
      this._recursively(e, this._group._map.getMinZoom(), t, null, function(e) {
        e.clusterShow()
      })
    },
    _recursivelyAddChildrenToMap: function(e, t, i) {
      this._recursively(i, this._group._map.getMinZoom() - 1, t, function(n) {
        if (t !== n._zoom)
          for (var r = n._markers.length - 1; r >= 0; r--) {
            var s = n._markers[r];
            i.contains(s._latlng) && (e && (s._backupLatlng = s.getLatLng(), s.setLatLng(e), s.clusterHide && s.clusterHide()), n._group._featureGroup.addLayer(s))
          }
      }, function(t) {
        t._addToMap(e)
      })
    },
    _recursivelyRestoreChildPositions: function(e) {
      for (var t = this._markers.length - 1; t >= 0; t--) {
        var i = this._markers[t];
        i._backupLatlng && (i.setLatLng(i._backupLatlng), delete i._backupLatlng)
      }
      if (e - 1 === this._zoom)
        for (var n = this._childClusters.length - 1; n >= 0; n--) this._childClusters[n]._restorePosition();
      else
        for (var r = this._childClusters.length - 1; r >= 0; r--) this._childClusters[r]._recursivelyRestoreChildPositions(e)
    },
    _restorePosition: function() {
      this._backupLatlng && (this.setLatLng(this._backupLatlng), delete this._backupLatlng)
    },
    _recursivelyRemoveChildrenFromMap: function(e, t, i, n) {
      var r, s;
      this._recursively(e, t - 1, i - 1, function(e) {
        for (s = e._markers.length - 1; s >= 0; s--) r = e._markers[s], n && n.contains(r._latlng) || (e._group._featureGroup.removeLayer(r), r.clusterShow && r.clusterShow())
      }, function(e) {
        for (s = e._childClusters.length - 1; s >= 0; s--) r = e._childClusters[s], n && n.contains(r._latlng) || (e._group._featureGroup.removeLayer(r), r.clusterShow && r.clusterShow())
      })
    },
    _recursively: function(e, t, i, n, r) {
      var s, o, a = this._childClusters,
        h = this._zoom;
      if (h >= t && (n && n(this), r && h === i && r(this)), t > h || i > h)
        for (s = a.length - 1; s >= 0; s--) o = a[s], o._boundsNeedUpdate && o._recalculateBounds(), e.intersects(o._bounds) && o._recursively(e, t, i, n, r)
    },
    _isSingleParent: function() {
      return this._childClusters.length > 0 && this._childClusters[0]._childCount === this._childCount
    }
  });
  L.Marker.include({
      clusterHide: function() {
        var e = this.options.opacity;
        return this.setOpacity(0), this.options.opacity = e, this
      },
      clusterShow: function() {
        return this.setOpacity(this.options.opacity)
      }
    }), L.DistanceGrid = function(e) {
      this._cellSize = e, this._sqCellSize = e * e, this._grid = {}, this._objectPoint = {}
    }, L.DistanceGrid.prototype = {
      addObject: function(e, t) {
        var i = this._getCoord(t.x),
          n = this._getCoord(t.y),
          r = this._grid,
          s = r[n] = r[n] || {},
          o = s[i] = s[i] || [],
          a = L.Util.stamp(e);
        this._objectPoint[a] = t, o.push(e)
      },
      updateObject: function(e, t) {
        this.removeObject(e), this.addObject(e, t)
      },
      removeObject: function(e, t) {
        var i, n, r = this._getCoord(t.x),
          s = this._getCoord(t.y),
          o = this._grid,
          a = o[s] = o[s] || {},
          h = a[r] = a[r] || [];
        for (delete this._objectPoint[L.Util.stamp(e)], i = 0, n = h.length; n > i; i++)
          if (h[i] === e) return h.splice(i, 1), 1 === n && delete a[r], !0
      },
      eachObject: function(e, t) {
        var i, n, r, s, o, a, h, l = this._grid;
        for (i in l) {
          o = l[i];
          for (n in o)
            for (a = o[n], r = 0, s = a.length; s > r; r++) h = e.call(t, a[r]), h && (r--, s--)
        }
      },
      getNearObject: function(e) {
        var t, i, n, r, s, o, a, h, l = this._getCoord(e.x),
          u = this._getCoord(e.y),
          _ = this._objectPoint,
          d = this._sqCellSize,
          c = null;
        for (t = u - 1; u + 1 >= t; t++)
          if (r = this._grid[t])
            for (i = l - 1; l + 1 >= i; i++)
              if (s = r[i])
                for (n = 0, o = s.length; o > n; n++) a = s[n], h = this._sqDist(_[L.Util.stamp(a)], e), (d > h || d >= h && null === c) && (d = h, c = a);
        return c
      },
      _getCoord: function(e) {
        var t = Math.floor(e / this._cellSize);
        return isFinite(t) ? t : e
      },
      _sqDist: function(e, t) {
        var i = t.x - e.x,
          n = t.y - e.y;
        return i * i + n * n
      }
    },
    function() {
      L.QuickHull = {
        getDistant: function(e, t) {
          var i = t[1].lat - t[0].lat,
            n = t[0].lng - t[1].lng;
          return n * (e.lat - t[0].lat) + i * (e.lng - t[0].lng)
        },
        findMostDistantPointFromBaseLine: function(e, t) {
          var i, n, r, s = 0,
            o = null,
            a = [];
          for (i = t.length - 1; i >= 0; i--) n = t[i], r = this.getDistant(n, e), r > 0 && (a.push(n), r > s && (s = r, o = n));
          return {
            maxPoint: o,
            newPoints: a
          }
        },
        buildConvexHull: function(e, t) {
          var i = [],
            n = this.findMostDistantPointFromBaseLine(e, t);
          return n.maxPoint ? (i = i.concat(this.buildConvexHull([e[0], n.maxPoint], n.newPoints)), i = i.concat(this.buildConvexHull([n.maxPoint, e[1]], n.newPoints))) : [e[0]]
        },
        getConvexHull: function(e) {
          var t, i = !1,
            n = !1,
            r = !1,
            s = !1,
            o = null,
            a = null,
            h = null,
            l = null,
            u = null,
            _ = null;
          for (t = e.length - 1; t >= 0; t--) {
            var d = e[t];
            (i === !1 || d.lat > i) && (o = d, i = d.lat), (n === !1 || d.lat < n) && (a = d, n = d.lat), (r === !1 || d.lng > r) && (h = d, r = d.lng), (s === !1 || d.lng < s) && (l = d, s = d.lng)
          }
          n !== i ? (_ = a, u = o) : (_ = l, u = h);
          var c = [].concat(this.buildConvexHull([_, u], e), this.buildConvexHull([u, _], e));
          return c
        }
      }
    }(), L.MarkerCluster.include({
      getConvexHull: function() {
        var e, t, i = this.getAllChildMarkers(),
          n = [];
        for (t = i.length - 1; t >= 0; t--) e = i[t].getLatLng(), n.push(e);
        return L.QuickHull.getConvexHull(n)
      }
    }), L.MarkerCluster.include({
      _2PI: 2 * Math.PI,
      _circleFootSeparation: 25,
      _circleStartAngle: 0,
      _spiralFootSeparation: 28,
      _spiralLengthStart: 11,
      _spiralLengthFactor: 5,
      _circleSpiralSwitchover: 9,
      spiderfy: function() {
        if (this._group._spiderfied !== this && !this._group._inZoomAnimation) {
          var e, t = this.getAllChildMarkers(),
            i = this._group,
            n = i._map,
            r = n.latLngToLayerPoint(this._latlng);
          this._group._unspiderfy(), this._group._spiderfied = this, t.length >= this._circleSpiralSwitchover ? e = this._generatePointsSpiral(t.length, r) : (r.y += 10, e = this._generatePointsCircle(t.length, r)), this._animationSpiderfy(t, e)
        }
      },
      unspiderfy: function(e) {
        this._group._inZoomAnimation || (this._animationUnspiderfy(e), this._group._spiderfied = null)
      },
      _generatePointsCircle: function(e, t) {
        var i, n, r = this._group.options.spiderfyDistanceMultiplier * this._circleFootSeparation * (2 + e),
          s = r / this._2PI,
          o = this._2PI / e,
          a = [];
        for (s = Math.max(s, 35), a.length = e, i = 0; e > i; i++) n = this._circleStartAngle + i * o, a[i] = new L.Point(t.x + s * Math.cos(n), t.y + s * Math.sin(n))._round();
        return a
      },
      _generatePointsSpiral: function(e, t) {
        var i, n = this._group.options.spiderfyDistanceMultiplier,
          r = n * this._spiralLengthStart,
          s = n * this._spiralFootSeparation,
          o = n * this._spiralLengthFactor * this._2PI,
          a = 0,
          h = [];
        for (h.length = e, i = e; i >= 0; i--) e > i && (h[i] = new L.Point(t.x + r * Math.cos(a), t.y + r * Math.sin(a))._round()), a += s / r + 5e-4 * i, r += o / a;
        return h
      },
      _noanimationUnspiderfy: function() {
        var e, t, i = this._group,
          n = i._map,
          r = i._featureGroup,
          s = this.getAllChildMarkers();
        for (i._ignoreMove = !0, this.setOpacity(1), t = s.length - 1; t >= 0; t--) e = s[t], r.removeLayer(e), e._preSpiderfyLatlng && (e.setLatLng(e._preSpiderfyLatlng), delete e._preSpiderfyLatlng), e.setZIndexOffset && e.setZIndexOffset(0), e._spiderLeg && (n.removeLayer(e._spiderLeg), delete e._spiderLeg);
        i.fire("unspiderfied", {
          cluster: this,
          markers: s
        }), i._ignoreMove = !1, i._spiderfied = null
      }
    }), L.MarkerClusterNonAnimated = L.MarkerCluster.extend({
      _animationSpiderfy: function(e, t) {
        var i, n, r, s, o = this._group,
          a = o._map,
          h = o._featureGroup,
          l = this._group.options.spiderLegPolylineOptions;
        for (o._ignoreMove = !0, i = 0; i < e.length; i++) s = a.layerPointToLatLng(t[i]), n = e[i], r = new L.Polyline([this._latlng, s], l), a.addLayer(r), n._spiderLeg = r, n._preSpiderfyLatlng = n._latlng, n.setLatLng(s), n.setZIndexOffset && n.setZIndexOffset(1e6), h.addLayer(n);
        this.setOpacity(.3), o._ignoreMove = !1, o.fire("spiderfied", {
          cluster: this,
          markers: e
        })
      },
      _animationUnspiderfy: function() {
        this._noanimationUnspiderfy()
      }
    }), L.MarkerCluster.include({
      _animationSpiderfy: function(e, t) {
        var i, n, r, s, o, a, h = this,
          l = this._group,
          u = l._map,
          _ = l._featureGroup,
          d = this._latlng,
          c = u.latLngToLayerPoint(d),
          p = L.Path.SVG,
          f = L.extend({}, this._group.options.spiderLegPolylineOptions),
          m = f.opacity;
        for (void 0 === m && (m = L.MarkerClusterGroup.prototype.options.spiderLegPolylineOptions.opacity), p ? (f.opacity = 0, f.className = (f.className || "") + " leaflet-cluster-spider-leg") : f.opacity = m, l._ignoreMove = !0, i = 0; i < e.length; i++) n = e[i], a = u.layerPointToLatLng(t[i]), r = new L.Polyline([d, a], f), u.addLayer(r), n._spiderLeg = r, p && (s = r._path, o = s.getTotalLength() + .1, s.style.strokeDasharray = o, s.style.strokeDashoffset = o), n.setZIndexOffset && n.setZIndexOffset(1e6), n.clusterHide && n.clusterHide(), _.addLayer(n), n._setPos && n._setPos(c);
        for (l._forceLayout(), l._animationStart(), i = e.length - 1; i >= 0; i--) a = u.layerPointToLatLng(t[i]), n = e[i], n._preSpiderfyLatlng = n._latlng, n.setLatLng(a), n.clusterShow && n.clusterShow(), p && (r = n._spiderLeg, s = r._path, s.style.strokeDashoffset = 0, r.setStyle({
          opacity: m
        }));
        this.setOpacity(.3), l._ignoreMove = !1, setTimeout(function() {
          l._animationEnd(), l.fire("spiderfied", {
            cluster: h,
            markers: e
          })
        }, 200)
      },
      _animationUnspiderfy: function(e) {
        var t, i, n, r, s, o, a = this,
          h = this._group,
          l = h._map,
          u = h._featureGroup,
          _ = e ? l._latLngToNewLayerPoint(this._latlng, e.zoom, e.center) : l.latLngToLayerPoint(this._latlng),
          d = this.getAllChildMarkers(),
          c = L.Path.SVG;
        for (h._ignoreMove = !0, h._animationStart(), this.setOpacity(1), i = d.length - 1; i >= 0; i--) t = d[i], t._preSpiderfyLatlng && (t.closePopup(), t.setLatLng(t._preSpiderfyLatlng), delete t._preSpiderfyLatlng, o = !0, t._setPos && (t._setPos(_), o = !1), t.clusterHide && (t.clusterHide(), o = !1), o && u.removeLayer(t), c && (n = t._spiderLeg, r = n._path, s = r.getTotalLength() + .1, r.style.strokeDashoffset = s, n.setStyle({
          opacity: 0
        })));
        h._ignoreMove = !1, setTimeout(function() {
          var e = 0;
          for (i = d.length - 1; i >= 0; i--) t = d[i], t._spiderLeg && e++;
          for (i = d.length - 1; i >= 0; i--) t = d[i], t._spiderLeg && (t.clusterShow && t.clusterShow(), t.setZIndexOffset && t.setZIndexOffset(0), e > 1 && u.removeLayer(t), l.removeLayer(t._spiderLeg), delete t._spiderLeg);
          h._animationEnd(), h.fire("unspiderfied", {
            cluster: a,
            markers: d
          })
        }, 200)
      }
    }), L.MarkerClusterGroup.include({
      _spiderfied: null,
      unspiderfy: function() {
        this._unspiderfy.apply(this, arguments)
      },
      _spiderfierOnAdd: function() {
        this._map.on("click", this._unspiderfyWrapper, this), this._map.options.zoomAnimation && this._map.on("zoomstart", this._unspiderfyZoomStart, this), this._map.on("zoomend", this._noanimationUnspiderfy, this), L.Browser.touch || this._map.getRenderer(this)
      },
      _spiderfierOnRemove: function() {
        this._map.off("click", this._unspiderfyWrapper, this), this._map.off("zoomstart", this._unspiderfyZoomStart, this), this._map.off("zoomanim", this._unspiderfyZoomAnim, this), this._map.off("zoomend", this._noanimationUnspiderfy, this), this._noanimationUnspiderfy()
      },
      _unspiderfyZoomStart: function() {
        this._map && this._map.on("zoomanim", this._unspiderfyZoomAnim, this)
      },
      _unspiderfyZoomAnim: function(e) {
        L.DomUtil.hasClass(this._map._mapPane, "leaflet-touching") || (this._map.off("zoomanim", this._unspiderfyZoomAnim, this), this._unspiderfy(e))
      },
      _unspiderfyWrapper: function() {
        this._unspiderfy()
      },
      _unspiderfy: function(e) {
        this._spiderfied && this._spiderfied.unspiderfy(e)
      },
      _noanimationUnspiderfy: function() {
        this._spiderfied && this._spiderfied._noanimationUnspiderfy()
      },
      _unspiderfyLayer: function(e) {
        e._spiderLeg && (this._featureGroup.removeLayer(e), e.clusterShow && e.clusterShow(), e.setZIndexOffset && e.setZIndexOffset(0), this._map.removeLayer(e._spiderLeg), delete e._spiderLeg)
      }
    }), L.MarkerClusterGroup.include({
      refreshClusters: function(e) {
        return e ? e instanceof L.MarkerClusterGroup ? e = e._topClusterLevel.getAllChildMarkers() : e instanceof L.LayerGroup ? e = e._layers : e instanceof L.MarkerCluster ? e = e.getAllChildMarkers() : e instanceof L.Marker && (e = [e]) : e = this._topClusterLevel.getAllChildMarkers(), this._flagParentsIconsNeedUpdate(e), this._refreshClustersIcons(), this.options.singleMarkerMode && this._refreshSingleMarkerModeMarkers(e), this
      },
      _flagParentsIconsNeedUpdate: function(e) {
        var t, i;
        for (t in e)
          for (i = e[t].__parent; i;) i._iconNeedsUpdate = !0, i = i.__parent
      },
      _refreshSingleMarkerModeMarkers: function(e) {
        var t, i;
        for (t in e) i = e[t], this.hasLayer(i) && i.setIcon(this._overrideMarkerIcon(i))
      }
    }), L.Marker.include({
      refreshIconOptions: function(e, t) {
        var i = this.options.icon;
        return L.setOptions(i, e), this.setIcon(i), t && this.__parent && this.__parent._group.refreshClusters(this), this
      }
    }), e.MarkerClusterGroup = t, e.MarkerCluster = i
});
//# sourceMappingURL=leaflet.markercluster.js.map



L.Photo = L.FeatureGroup.extend({
	options: {
		icon: {						
			iconSize: [40, 40]
		}
	},

	initialize: function (photos, options) {
		L.setOptions(this, options);
		L.FeatureGroup.prototype.initialize.call(this, photos);
	},

	addLayers: function (photos) {
		if (photos) {
			for (var i = 0, len = photos.length; i < len; i++) {
				this.addLayer(photos[i]);
			}
		}
		return this;
	},

	addLayer: function (photo) {	
		L.FeatureGroup.prototype.addLayer.call(this, this.createMarker(photo));
	},

	createMarker: function (photo) {
		var marker = L.marker(photo, {
			icon: L.divIcon(L.extend({
				html: '<div style="background-image: url(' + photo.thumbnail + ');"></div>',
				className: 'leaflet-marker-photo'
			}, photo, this.options.icon)),
			title: photo.caption || ''
		});		
		marker.photo = photo;
		return marker;
	}
});

L.photo = function (photos, options) {
	return new L.Photo(photos, options);
};

if (L.MarkerClusterGroup) {

	L.Photo.Cluster = L.MarkerClusterGroup.extend({
		options: {
			featureGroup: L.photo,		
			maxClusterRadius: 100,		
			showCoverageOnHover: false,
			iconCreateFunction: function(cluster) {
				return new L.DivIcon(L.extend({
					className: 'leaflet-marker-photo', 
					html: '<div style="background-image: url(' + cluster.getAllChildMarkers()[0].photo.thumbnail + ');"></div><b>' + cluster.getChildCount() + '</b>'
				}, this.icon));
		   	},	
			icon: {						
				iconSize: [40, 40]
			}		   		
		},

		initialize: function (options) {	
			options = L.Util.setOptions(this, options);
			L.MarkerClusterGroup.prototype.initialize.call(this);
			this._photos = options.featureGroup(null, options);
		},

		add: function (photos) {
			this.addLayer(this._photos.addLayers(photos));
			return this;
		},

		clear: function () {
			this._photos.clearLayers();
			this.clearLayers();
		}

	});

	L.photo.cluster = function (options) {
		return new L.Photo.Cluster(options);	
	};

}



/**
 * Copyright (C) 2011-2012 Pavel Shramov
 * Copyright (C) 2013-2017 Maxime Petazzoni <maxime.petazzoni@bulix.org>
 * All Rights Reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * - Redistributions of source code must retain the above copyright notice,
 *   this list of conditions and the following disclaimer.
 *
 * - Redistributions in binary form must reproduce the above copyright notice,
 *   this list of conditions and the following disclaimer in the documentation
 *   and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 */

/*
 * Thanks to Pavel Shramov who provided the initial implementation and Leaflet
 * integration. Original code was at https://github.com/shramov/leaflet-plugins.
 *
 * It was then cleaned-up and modified to record and make available more
 * information about the GPX track while it is being parsed so that the result
 * can be used to display additional information about the track that is
 * rendered on the Leaflet map.
 */

var L = L || require('leaflet');

var _MAX_POINT_INTERVAL_MS = 15000;
var _SECOND_IN_MILLIS = 1000;
var _MINUTE_IN_MILLIS = 60 * _SECOND_IN_MILLIS;
var _HOUR_IN_MILLIS = 60 * _MINUTE_IN_MILLIS;
var _DAY_IN_MILLIS = 24 * _HOUR_IN_MILLIS;

var _GPX_STYLE_NS = 'http://www.topografix.com/GPX/gpx_style/0/2';

var _DEFAULT_MARKER_OPTS = {
  startIconUrl: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACEAAAAtCAMAAAAX+PImAAABC1BMVEUAAAAAgAAAgAAAgAAAgAAAgAAAgAAAgAAAgAAAgAAAgAAAgAAAgAAAgAAAgAAAgAAAgAAAgAAAgAAAgAAAgAAAgAAAgAAAgAAAgAAAgAAAgAAAgAAAgAAAgAAAgAAAgAAAgAAAgAAAgAAAgAAAgAAAgAAAgAAAgAAAgAAAgAAAgAAAgAAAgAAAgAD///8AlAAAkgAAgQAAgwAAhgAAjQAAkAAAhwAElQQAigD7/fv3/PcfoR8LmQsAjABRtlFGskY8rTw0qjQAkQDx+fHp9unX7te+5L6W05ZjvmMUnRTi8+Lc8NzP68+q26qc1px0xXRAr0DM6szI6Mi04LSIzYhyxHJpwGkupy4spyzxfiXGAAAALXRSTlMA/QL59OffBr60qG9iDuzPujoJ746Ff3l0TUhAMycjGxJd18WunJhZLRgMZVI0U6/AAAACQklEQVQ4y32U53baQBBGR6L33k1zjZ0sLJJA9GoDjmt63v9JMrNarELs+4ODVvd8MxrtCmzU62opmg6no6VqU4VjQieFVI4JFH8qnwl5hUY+wJwkL+vgRK2kmJfTL6pDiMuAnqbrutaTMbGQLVgNaMM+J9YzXUj+8kGpioTekHcPcENjSK4NguaZCDDELUL8GTAkeAJEUQh9WjYny8XrxORvynmCnvOUSoiE1e5uMxo/PC9NUqiQ7wqNGLkDXDL3XzsWt7+meG1Qu5EbyEYogmrsN50D4xdT1glkoBG0IvjKSpApr9wKUWJQ8aNhYI3njpMnU3YShbgiivDJg8u4/YMhVCYMMTQ03uWLscsYzdEYonEGZWnMRx0Xv8mwM46N0V4aEYhLY7lxGeOFNPL0LKLT++8u426Cho5DbUOd5jHDR3txlfkp5x78BIk0GjrHkK1D+EYRBrWRBSjKqfPVo11jiQLHIiwGAJkcjZ1W/j6NrS5/rLh8c0Hazzfi1c2o7nSx2z5ud/MpCWua+YUKSNv3tkF4d3o/xV8SqEayBkQrzGSKJQn6JLBoFgRXfoWUQd/eyTONyQhB4pyhQo6x5kh/SPdx7TIEkkyAKYo8UvJE4QJN64BaVAhmQ5e+Mthch5nihaVb4KAWYF4hUHMf/rLPY/hKKrhIRJk7ItICD/WUU6ETe0Ql6VD8cThGLTlayctxv9cKCzfhvzRSTDaRAS/2x8jVxDHqZz9NohCCdwkVsduLBHxAtuBLN+FDWgXvqP4Bkoed0xIT03MAAAAASUVORK5CYII=',
  endIconUrl: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACEAAAAtCAMAAAAX+PImAAABAlBMVEUAAADGQkLGQkLGQkLGQkLGQkLGQkLGQkLGQkLGQkLGQkLGQkLGQkLGQkLGQkLGQkLGQkLGQkLGQkLGQkLGQkLGQkLGQkLGQkLGQkLGQkLGQkLGQkLGQkLGQkLGQkLGQkLGQkLGQkLGQkLGQkLGQkLGQkLGQkLGQkLGQkLGQkLGQkLGQkLGQkL///+3LCy4Li62KSnFQEDDPT3COzu7MjK9NDT9+Pi6MDC/NzfARUXBOTn+/PzUf3/Ob2/GV1e6NTX57e303t7iqKjYjIzLZGTJX1/78/P35+f14uLx19fx1NTtysrrxMTkrq7MaGjIXFzEUVG8PDznubnnuLjdnJy+Pz/5SaUvAAAALHRSTlMA/AL5Cgb08ObdurSoGg3sz75zbmM6joV/eVpNSEAzJyMSX+jh18SunJgtUvqwWL0AAAJBSURBVDjLfZN3e6JAEIcHsAXF3kssudRbAQFBjSWx5NLLle//VW5nWaUYff/hYZ+X3wyzu+AhKs1aSpblVK2piLBP9LSSjROGEM+WS9Gw0CkniJ/MdRv8iI0sCXP+U/QJxTPCGBimaRoDHlOI7oSe24AxsjRN1TRnaDIplt8qzQT7fqSpWzTLwKV4HRjKBRMsFdEpzDFx8eQUkOpO0LXxZr0Za/pOuUzjf56jMFQp8+W9bduPbx8sBQtJWKeA7gSXpr/6LncrTLSw3WQEIkmMcOjK9KG/xV5hCtY5K0HnxI3Q524CT1nrNAR3IA+NGH0OaY23vp8/Fu8kBUWBFdHHjwHj7pOGTKiRgwI1DE3V13bAuJ1RY0SNC8hzY3bbDzBFg2ccN5JQ5MbHQ0Cw37lRxn9h4/h6Dhj3Y50NROpBG+eBM18FyvzFIdOh/riBtEwNk77/e/EJzxhhuVOHKt9Zff7k1djofHcLAFCKY4hGlc/fttvl61ylDLFIGwC3jneiL96Xr08vy9kCD4iDM78SgVKXdgdEVxdfC9U7ZJkWIN0c4YoPBwWSigCjHhNQmTjeScYeeASSviRUQcdyNIo1whbo2nUUOKUEEQR+pQxjgN/jwsmNd+eqAkI88FXKg4eSI0IYInfBRytBwkKiBX7EvBQypJoIAdIpEoxIdiFEO+tX8Mbu0cj4lFgR9hFrvlbKfNyHWiE5Bb6lkyW8iRIcoOlOJdaDQ4jFOE6iEoWDRKu026s0HCFSkWQFjtKthEf1H+4TmsxXLEfyAAAAAElFTkSuQmCC',
  shadowUrl: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAQAAAC0NkA6AAAELklEQVR4AWIYBaNgFIyCUTAKRsEoADRLF2uSFEEcwCMjpaRlfb9vcXeHK+5whjP+GuzzMFfuzBl3d4fx6ZK0iGC2exenC4d/tHdV/NL+bNTf2kf+ODLUFEF9X4sIMMip+tPIouX16FWLEROKYiXzAlh80FxQyWfQ6gL8w4gCvB53cJ/2OMZOJ8xIyEjYLeYiyGM2VOVp5rxLl9GKAP8RBEFdrqe60EaLAYM66KiTbjWjR1CMAEqQKprkKpWhjhTLDLQyn436nUukz9Ejc451dmLRZkOms9F0xuuwVwlPQ4Av2VGR98ex399N+txvxQP5NAIGMMdhWY6fBFozsUedcVOHBRbksh3Z7DbsV0Y0acKvEECxpiPxaBi11iBMOfNnvMUAAOaNJcSKAgR9mtmxh1xdmBJLXx2uUvlcEV2y4cSMNCMhICiAzMzrcdZPzU2s0nbyaZzX1BxZG9jq00xb7C/rkutcQ/1J/VxFZXbZRkNzAhQrWJwuFsoGoEkvuwvsTAfcVhOYI78trCrAM8ysmNR6lEcXTF4eh5pLLnORjGjWCQF5TgAszhYAI++B6+os+EZa2IUXABTIso3HC+xmMRnh1E7Hk0+mapQqKcixBUx4cg7zoIAgIUlErxrcOXPTb/KO7sB/nICWzgSUx8PO1WdNPtr3yZQmeUQFWdCsfzJ+QUYG0hmSCtxhc6T5phVPqcprDLJ8udQtCjSYfcWn9bcjGu8RVXKMgKcAFGBkJEuaIKnEUXpoj862d2SWuzY0CWgIgZm6BMFku1GYMhfiyLL5MWBIE5LNOpnMUYL41J3drM2kyW3bQwQCHkSuhwNqot7W1rCJBjQj4wJARtJksk4um2iiRB1Cf2nP3Uetabu+9ZAgL4hBJEiCs+BFyDDvrkAQgM0ccEnHItpog/Xkr+t3+22/04Nv/Sg2+RQxgAisyq4EtnQRvSpOohgGQNH5BOBOAL7wyl/fH+sb33rrdaBYpgPpYwJeEIOIkmdgKkl62S9aNGvmrBBzuQeYUPqyt/29fdUpzz2FFEOC1OY5IPOCQWSRo7Ah1V5ZimQTihKdquB83evu/u5wZzrnfQixSZyYZvzxL4Eh5BZ4E2owotmQSbWiBFSGsnPd/e2xbtzZ3gUKmD7Mn9Mar/Iv2w8iokAdVZ8pB4pcYp8zAEbX39uc1h7oRp3zOu7GNmf6nC+X478BDCCLsCCnbAOyKKRrwg1t0Rzs9nv0IULeogP8MAOsLAEGkBdgDB1s88fR9jrUfG9y/aSbdpWHAHmSP+QnGERgOGbZReuwxbOUPeQ7ZJSLtM8f6DFMUpXfoAf4+uH+gzNRAC0jfRDOkmtUSzVVCQLElGf0ND8pIPC7o+Q3/1nVL9novLU6SkEVTQlTpK/ojwEDyIN4ud7RQY9VI5lPY+A36Cn+/cAwMpz/G/IdAqGyx1q2VHAAAAAASUVORK5CYII=',
  wptIcons: [],
  wptIconUrls : {
    '': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACEAAAAzCAMAAAAuJJHNAAAAkFBMVEUAAAAAru8Aru8Aru8Aru8Aru8Aru8Aru8Aru8Aru8Aru8Aru8Aru8Aru8Aru8Aru8Aru8Aru8Aru8Aru8Aru8Aru8Aru8Aru8Aru8Aru8Aru8Aru8Aru8Aru8Aru8Aru8Aru8Aru8Aru8Aru8Aru8Aru8Aru8Aru8Aru8Aru8Aru8Aru8Aru8Aru8Aru8Aru9ovJP8AAAAL3RSTlMA+AT68Fr0FA8H3MSXQDkL6+bg1o6CUkcxwbitbV8sJyQZz76neH1yTB6yolWHaUf8FCEAAAGESURBVDjLfdTnloIwEAXgmyxVKUoTxLWsvezO+7/dqkgGDPH7B2dOuJkwQVe8Dgv7Fq48DIqjfJtYQggrGWczvcifXSxiTmXH6DkHFvWJeomOcky6dNYp+KEhiSrZbGlY+vqQzMikbuKGEzIRNu7klcwqD8BySmbiEXbRi18Hu/SLWAbIHSlOtpaQm30n2NjFhnvxtZd4srnB0xIlx5h7aMiAgxSYOdT6RivklwvYQqWI+CATVZHjWyW3uGIzUhW/uAkV1EYr4qgHRLy1nY+XvNt3l3frtFHDKe92CQTEj38egLhISZnHQNFpsqjyxWHuENs/cqdkNilxl5FZ7fPWdNwAvyaTHxdPhSCDIxqe6V8frfHCZ9OXo+WOh5dYAZ8XycHcypCC2YI0B3R5c31oz+g5Oe/tXKDPV2PDg/ImmmgzzYbuiEsMzWpEbBJiwJFYIMG03nO/NYXDpz7Mv1KjcmFQJvRgnWC0b2L6YENhR0t8cLLUgRjIgG8ig9U2xGdy/R7zH4uopdSUohgfAAAAAElFTkSuQmCC',
  },
  pointMatchers: [],
  iconSize: [33, 50],
  shadowSize: [50, 50],
  iconAnchor: [16, 45],
  shadowAnchor: [16, 47],
  clickable: false
};
var _DEFAULT_POLYLINE_OPTS = {
  color: 'blue'
};
var _DEFAULT_GPX_OPTS = {
  parseElements: ['track', 'route', 'waypoint']
};
L.GPX = L.FeatureGroup.extend({
  initialize: function(gpx, options) {
    options.max_point_interval = options.max_point_interval || _MAX_POINT_INTERVAL_MS;
    options.marker_options = this._merge_objs(
      _DEFAULT_MARKER_OPTS,
      options.marker_options || {});
    options.polyline_options = options.polyline_options || {};
    options.gpx_options = this._merge_objs(
      _DEFAULT_GPX_OPTS,
      options.gpx_options || {});

    L.Util.setOptions(this, options);

    // Base icon class for track pins.
    L.GPXTrackIcon = L.Icon.extend({ options: options.marker_options });

    this._gpx = gpx;
    this._layers = {};
    this._init_info();

    if (gpx) {
      this._parse(gpx, options, this.options.async);
    }
  },

  get_duration_string: function(duration, hidems) {
    var s = '';

    if (duration >= _DAY_IN_MILLIS) {
      s += Math.floor(duration / _DAY_IN_MILLIS) + 'd ';
      duration = duration % _DAY_IN_MILLIS;
    }

    if (duration >= _HOUR_IN_MILLIS) {
      s += Math.floor(duration / _HOUR_IN_MILLIS) + ':';
      duration = duration % _HOUR_IN_MILLIS;
    }

    var mins = Math.floor(duration / _MINUTE_IN_MILLIS);
    duration = duration % _MINUTE_IN_MILLIS;
    if (mins < 10) s += '0';
    s += mins + '\\'';

    var secs = Math.floor(duration / _SECOND_IN_MILLIS);
    duration = duration % _SECOND_IN_MILLIS;
    if (secs < 10) s += '0';
    s += secs;

    if (!hidems && duration > 0) s += '.' + Math.round(Math.floor(duration)*1000)/1000;
    else s += '"';

    return s;
  },

  get_duration_string_iso: function(duration, hidems) {
    var s = this.get_duration_string(duration, hidems);
    return s.replace("'",':').replace('"','');
  },

  // Public methods
  to_miles:            function(v) { return v / 1.60934; },
  to_ft:               function(v) { return v * 3.28084; },
  m_to_km:             function(v) { return v / 1000; },
  m_to_mi:             function(v) { return v / 1609.34; },

  get_name:            function() { return this._info.name; },
  get_desc:            function() { return this._info.desc; },
  get_author:          function() { return this._info.author; },
  get_copyright:       function() { return this._info.copyright; },
  get_distance:        function() { return this._info.length; },
  get_distance_imp:    function() { return this.to_miles(this.m_to_km(this.get_distance())); },

  get_start_time:      function() { return this._info.duration.start; },
  get_end_time:        function() { return this._info.duration.end; },
  get_moving_time:     function() { return this._info.duration.moving; },
  get_total_time:      function() { return this._info.duration.total; },

  get_moving_pace:     function() { return this.get_moving_time() / this.m_to_km(this.get_distance()); },
  get_moving_pace_imp: function() { return this.get_moving_time() / this.get_distance_imp(); },

  get_moving_speed:    function() { return this.m_to_km(this.get_distance()) / (this.get_moving_time() / (3600 * 1000)) ; },
  get_moving_speed_imp:function() { return this.to_miles(this.m_to_km(this.get_distance())) / (this.get_moving_time() / (3600 * 1000)) ; },

  get_total_speed:     function() { return this.m_to_km(this.get_distance()) / (this.get_total_time() / (3600 * 1000)); },
  get_total_speed_imp: function() { return this.to_miles(this.m_to_km(this.get_distance())) / (this.get_total_time() / (3600 * 1000)); },

  get_elevation_gain:     function() { return this._info.elevation.gain; },
  get_elevation_loss:     function() { return this._info.elevation.loss; },
  get_elevation_gain_imp: function() { return this.to_ft(this.get_elevation_gain()); },
  get_elevation_loss_imp: function() { return this.to_ft(this.get_elevation_loss()); },
  get_elevation_data:     function() {
    var _this = this;
    return this._info.elevation._points.map(
      function(p) { return _this._prepare_data_point(p, _this.m_to_km, null,
        function(a, b) { return a.toFixed(2) + ' km, ' + b.toFixed(0) + ' m'; });
      });
  },
  get_elevation_data_imp: function() {
    var _this = this;
    return this._info.elevation._points.map(
      function(p) { return _this._prepare_data_point(p, _this.m_to_mi, _this.to_ft,
        function(a, b) { return a.toFixed(2) + ' mi, ' + b.toFixed(0) + ' ft'; });
      });
  },
  get_elevation_max:      function() { return this._info.elevation.max; },
  get_elevation_min:      function() { return this._info.elevation.min; },
  get_elevation_max_imp:  function() { return this.to_ft(this.get_elevation_max()); },
  get_elevation_min_imp:  function() { return this.to_ft(this.get_elevation_min()); },

  get_average_hr:         function() { return this._info.hr.avg; },
  get_average_temp:         function() { return this._info.atemp.avg; },
  get_average_cadence:         function() { return this._info.cad.avg; },
  get_heartrate_data:     function() {
    var _this = this;
    return this._info.hr._points.map(
      function(p) { return _this._prepare_data_point(p, _this.m_to_km, null,
        function(a, b) { return a.toFixed(2) + ' km, ' + b.toFixed(0) + ' bpm'; });
      });
  },
  get_heartrate_data_imp: function() {
    var _this = this;
    return this._info.hr._points.map(
      function(p) { return _this._prepare_data_point(p, _this.m_to_mi, null,
        function(a, b) { return a.toFixed(2) + ' mi, ' + b.toFixed(0) + ' bpm'; });
      });
  },
  get_cadence_data:     function() {
    var _this = this;
    return this._info.cad._points.map(
      function(p) { return _this._prepare_data_point(p, _this.m_to_km, null,
        function(a, b) { return a.toFixed(2) + ' km, ' + b.toFixed(0) + ' rpm'; });
      });
  },
  get_temp_data:     function() {
    var _this = this;
    return this._info.atemp._points.map(
      function(p) { return _this._prepare_data_point(p, _this.m_to_km, null,
        function(a, b) { return a.toFixed(2) + ' km, ' + b.toFixed(0) + ' degrees'; });
      });
  },
  get_cadence_data_imp:     function() {
    var _this = this;
    return this._info.cad._points.map(
      function(p) { return _this._prepare_data_point(p, _this.m_to_mi, null,
        function(a, b) { return a.toFixed(2) + ' mi, ' + b.toFixed(0) + ' rpm'; });
      });
  },
  get_temp_data_imp:     function() {
    var _this = this;
    return this._info.atemp._points.map(
      function(p) { return _this._prepare_data_point(p, _this.m_to_mi, null,
        function(a, b) { return a.toFixed(2) + ' mi, ' + b.toFixed(0) + ' degrees'; });
      });
  },

  reload: function() {
    this._init_info();
    this.clearLayers();
    this._parse(this._gpx, this.options, this.options.async);
  },

  // Private methods
  _merge_objs: function(a, b) {
    var _ = {};
    for (var attr in a) { _[attr] = a[attr]; }
    for (var attr in b) { _[attr] = b[attr]; }
    return _;
  },

  _prepare_data_point: function(p, trans1, trans2, trans_tooltip) {
    var r = [trans1 && trans1(p[0]) || p[0], trans2 && trans2(p[1]) || p[1]];
    r.push(trans_tooltip && trans_tooltip(r[0], r[1]) || (r[0] + ': ' + r[1]));
    return r;
  },

  _init_info: function() {
    this._info = {
      name: null,
      length: 0.0,
      elevation: {gain: 0.0, loss: 0.0, max: 0.0, min: Infinity, _points: []},
      hr: {avg: 0, _total: 0, _points: []},
      duration: {start: null, end: null, moving: 0, total: 0},
      atemp: {avg: 0, _total: 0, _points: []},
      cad: {avg: 0, _total: 0, _points: []}
    };
  },

  _load_xml: function(url, cb, options, async) {
    if (async == undefined) async = this.options.async;
    if (options == undefined) options = this.options;

    var req = new window.XMLHttpRequest();
    req.open('GET', url, async);
    try {
      req.overrideMimeType('text/xml'); // unsupported by IE
    } catch(e) {}
    req.onreadystatechange = function() {
      if (req.readyState != 4) return;
      if(req.status == 200) cb(req.responseXML, options);
    };
    req.send(null);
  },

  _parse: function(input, options, async) {
    var _this = this;
    var cb = function(gpx, options) {
      var layers = _this._parse_gpx_data(gpx, options);
      if (!layers) {
        _this.fire('error', { err: 'No parseable layers of type(s) ' + JSON.stringify(options.gpx_options.parseElements) });
        return;
      }
      _this.addLayer(layers);
      _this.fire('loaded', { layers: layers, element: gpx });
    }
    if (input.substr(0,1)==='<') { // direct XML has to start with a <
      var parser = new DOMParser();
      if (async) {
        setTimeout(function() {
          cb(parser.parseFromString(input, "text/xml"), options);
        });
      } else {
        cb(parser.parseFromString(input, "text/xml"), options);
      }
    } else {
      this._load_xml(input, cb, options, async);
    }
  },

  _parse_gpx_data: function(xml, options) {
    var i, t, l, el, layers = [];
    var tags = [];

    var parseElements = options.gpx_options.parseElements;
    if (parseElements.indexOf('route') > -1) {
      tags.push(['rte','rtept']);
    }
    if (parseElements.indexOf('track') > -1) {
      tags.push(['trkseg','trkpt']);
    }

    var name = xml.getElementsByTagName('name');
    if (name.length > 0) {
      this._info.name = name[0].textContent;
    }
    var desc = xml.getElementsByTagName('desc');
    if (desc.length > 0) {
      this._info.desc = desc[0].textContent;
    }
    var author = xml.getElementsByTagName('author');
    if (author.length > 0) {
      this._info.author = author[0].textContent;
    }
    var copyright = xml.getElementsByTagName('copyright');
    if (copyright.length > 0) {
      this._info.copyright = copyright[0].textContent;
    }
this._info.number_of_points = 0;
    for (t = 0; t < tags.length; t++) {
      el = xml.getElementsByTagName(tags[t][0]);
      for (i = 0; i < el.length; i++) {
        var trackLayers = this._parse_trkseg(el[i], options, tags[t][1]);
        for (l = 0; l < trackLayers.length; l++) {
          layers.push(trackLayers[l]);
        }
      }
    }

    this._info.hr.avg = Math.round(this._info.hr._total / this._info.hr._points.length);
    this._info.cad.avg = Math.round(this._info.cad._total / this._info.cad._points.length);
    this._info.atemp.avg = Math.round(this._info.atemp._total / this._info.atemp._points.length);

    // parse waypoints and add markers for each of them
    if (parseElements.indexOf('waypoint') > -1) {
      el = xml.getElementsByTagName('wpt');
      for (i = 0; i < el.length; i++) {
        var ll = new L.LatLng(
            el[i].getAttribute('lat'),
            el[i].getAttribute('lon'));

        var nameEl = el[i].getElementsByTagName('name');
        var name = '';
        if (nameEl.length > 0) {
          name = nameEl[0].textContent;
        }

        var descEl = el[i].getElementsByTagName('desc');
        var desc = '';
        if (descEl.length > 0) {
          desc = descEl[0].textContent;
        }

        var symEl = el[i].getElementsByTagName('sym');
        var symKey = '';
        if (symEl.length > 0) {
          symKey = symEl[0].textContent;
        }

        /*
         * Add waypoint marker based on the waypoint symbol key.
         *
         * First look for a configured icon for that symKey. If not found, look
         * for a configured icon URL for that symKey and build an icon from it.
         * Otherwise, fall back to the default icon if one was configured, or
         * finally to the default icon URL.
         */
        var wptIcons = options.marker_options.wptIcons;
        var wptIconUrls = options.marker_options.wptIconUrls;
        var symIcon;
        if (wptIcons && wptIcons[symKey]) {
          symIcon = wptIcons[symKey];
        } else if (wptIconUrls && wptIconUrls[symKey]) {
          symIcon = new L.GPXTrackIcon({iconUrl: wptIconUrls[symKey]});
        } else if (wptIcons && wptIcons['']) {
          symIcon = wptIcons[''];
        } else if (wptIconUrls && wptIconUrls['']) {
          symIcon = new L.GPXTrackIcon({iconUrl: wptIconUrls['']});
        } else {
          console.log('No icon or icon URL configured for symbol type "' + symKey
            + '", and no fallback configured; ignoring waypoint.');
          continue;
        }

        var marker = new L.Marker(ll, {
          clickable: options.marker_options.clickable,
          title: name,
          icon: symIcon
        });
        marker.bindPopup("<b>" + name + "</b>" + (desc.length > 0 ? '<br>' + desc : '')).openPopup();
        this.fire('addpoint', { point: marker, point_type: 'waypoint', element: el[i] });
        layers.push(marker);
      }
    }

    if (layers.length > 1) {
       return new L.FeatureGroup(layers);
    } else if (layers.length == 1) {
      return layers[0];
    }
  },

  _parse_trkseg: function(line, options, tag) {
    var el = line.getElementsByTagName(tag);
    if (!el.length) return [];

    var coords = [];
    var markers = [];
    var layers = [];
    var last = null;

    for (var i = 0; i < el.length; i++) {
this._info.number_of_points++;
      var _, ll = new L.LatLng(
        el[i].getAttribute('lat'),
        el[i].getAttribute('lon'));
      ll.meta = { time: null, ele: null, hr: null, cad: null, atemp: null };

      _ = el[i].getElementsByTagName('time');
      if (_.length > 0) {
        ll.meta.time = new Date(Date.parse(_[0].textContent));
      } else {
        ll.meta.time = new Date('1970-01-01T00:00:00');
      }

      _ = el[i].getElementsByTagName('ele');
      if (_.length > 0) {
        ll.meta.ele = parseFloat(_[0].textContent);
      }

      _ = el[i].getElementsByTagName('name');
      if (_.length > 0) {
        var name = _[0].textContent;
        var ptMatchers = options.marker_options.pointMatchers || [];

        for (var j = 0; j < ptMatchers.length; j++) {
          if (ptMatchers[j].regex.test(name)) {
            markers.push({ label: name, coords: ll, icon: ptMatchers[j].icon, element: el[i] });
            break;
          }
        }
      }

      _ = el[i].getElementsByTagNameNS('*', 'hr');
      if (_.length > 0) {
        ll.meta.hr = parseInt(_[0].textContent);
        this._info.hr._points.push([this._info.length, ll.meta.hr]);
        this._info.hr._total += ll.meta.hr;
      }

      _ = el[i].getElementsByTagNameNS('*', 'cad');
      if (_.length > 0) {
        ll.meta.cad = parseInt(_[0].textContent);
        this._info.cad._points.push([this._info.length, ll.meta.cad]);
        this._info.cad._total += ll.meta.cad;
      }

      _ = el[i].getElementsByTagNameNS('*', 'atemp');
      if (_.length > 0) {
        ll.meta.atemp = parseInt(_[0].textContent);
        this._info.atemp._points.push([this._info.length, ll.meta.atemp]);
        this._info.atemp._total += ll.meta.atemp;
      }

      if (ll.meta.ele > this._info.elevation.max) {
        this._info.elevation.max = ll.meta.ele;
      }

      if (ll.meta.ele < this._info.elevation.min) {
        this._info.elevation.min = ll.meta.ele;
      }

      this._info.elevation._points.push([this._info.length, ll.meta.ele]);
      this._info.duration.end = ll.meta.time;

      if (last != null) {
        this._info.length += this._dist3d(last, ll);

        var t = ll.meta.ele - last.meta.ele;
        if (t > 0) {
          this._info.elevation.gain += t;
        } else {
          this._info.elevation.loss += Math.abs(t);
        }

        t = Math.abs(ll.meta.time - last.meta.time);
        this._info.duration.total += t;
        if (t < options.max_point_interval) {
          this._info.duration.moving += t;
        }
      } else if (this._info.duration.start == null) {
        this._info.duration.start = ll.meta.time;
      }

      last = ll;
      coords.push(ll);
    }

    // check for gpx_style styling extension
    var polyline_options = this._merge_objs(_DEFAULT_POLYLINE_OPTS, {});
    var e = line.getElementsByTagNameNS(_GPX_STYLE_NS, 'line');
    if (e.length > 0) {
      var _ = e[0].getElementsByTagName('color');
      if (_.length > 0) polyline_options.color = '#' + _[0].textContent;
      var _ = e[0].getElementsByTagName('opacity');
      if (_.length > 0) polyline_options.opacity = _[0].textContent;
      var _ = e[0].getElementsByTagName('weight');
      if (_.length > 0) polyline_options.weight = _[0].textContent;
      var _ = e[0].getElementsByTagName('linecap');
      if (_.length > 0) polyline_options.lineCap = _[0].textContent;
    }

    // add track
    var l = new L.Polyline(coords, this._merge_objs(polyline_options, options.polyline_options));
    this.fire('addline', { line: l, element: line });
    layers.push(l);

    if (options.marker_options.startIcon || options.marker_options.startIconUrl) {
      // add start pin
      var marker = new L.Marker(coords[0], {
        clickable: options.marker_options.clickable,
        icon: options.marker_options.startIcon || new L.GPXTrackIcon({iconUrl: options.marker_options.startIconUrl})
      });
      this.fire('addpoint', { point: marker, point_type: 'start', element: el[0] });
      layers.push(marker);
    }

    if (options.marker_options.endIcon || options.marker_options.endIconUrl) {
      // add end pin
      var marker = new L.Marker(coords[coords.length-1], {
        clickable: options.marker_options.clickable,
        icon: options.marker_options.endIcon || new L.GPXTrackIcon({iconUrl: options.marker_options.endIconUrl})
      });
      this.fire('addpoint', { point: marker, point_type: 'end', element: el[el.length-1] });
      layers.push(marker);
    }

    // add named markers
    for (var i = 0; i < markers.length; i++) {
      var marker = new L.Marker(markers[i].coords, {
        clickable: options.marker_options.clickable,
        title: markers[i].label,
        icon: markers[i].icon
      });
      this.fire('addpoint', { point: marker, point_type: 'label', element: markers[i].element });
      layers.push(marker);
    }

    return layers;
  },

  _dist2d: function(a, b) {
    var R = 6371000;
    var dLat = this._deg2rad(b.lat - a.lat);
    var dLon = this._deg2rad(b.lng - a.lng);
    var r = Math.sin(dLat/2) *
      Math.sin(dLat/2) +
      Math.cos(this._deg2rad(a.lat)) *
      Math.cos(this._deg2rad(b.lat)) *
      Math.sin(dLon/2) *
      Math.sin(dLon/2);
    var c = 2 * Math.atan2(Math.sqrt(r), Math.sqrt(1-r));
    var d = R * c;
    return d;
  },

  _dist3d: function(a, b) {
    var planar = this._dist2d(a, b);
    var height = Math.abs(b.meta.ele - a.meta.ele);
    return Math.sqrt(Math.pow(planar, 2) + Math.pow(height, 2));
  },

  _deg2rad: function(deg) {
    return deg * Math.PI / 180;
  }
});

if (typeof module === 'object' && typeof module.exports === 'object') {
  module.exports = L;
} else if (typeof define === 'function' && define.amd) {
  define(L);
}



(function(f){if(typeof exports==="object"&&typeof module!=="undefined"){module.exports=f()}else if(typeof define==="function"&&define.amd){define([],f)}else{var g;if(typeof window!=="undefined"){g=window}else if(typeof global!=="undefined"){g=global}else if(typeof self!=="undefined"){g=self}else{g=this}g.Dygraph = f()}})(function(){var define,module,exports;return (function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
// shim for using process in browser
var process = module.exports = {};

// cached from whatever global is present so that test runners that stub it
// don't break things.  But we need to wrap it in a try catch in case it is
// wrapped in strict mode code which doesn't define any globals.  It's inside a
// function because try/catches deoptimize in certain engines.

var cachedSetTimeout;
var cachedClearTimeout;

function defaultSetTimout() {
    throw new Error('setTimeout has not been defined');
}
function defaultClearTimeout () {
    throw new Error('clearTimeout has not been defined');
}
(function () {
    try {
        if (typeof setTimeout === 'function') {
            cachedSetTimeout = setTimeout;
        } else {
            cachedSetTimeout = defaultSetTimout;
        }
    } catch (e) {
        cachedSetTimeout = defaultSetTimout;
    }
    try {
        if (typeof clearTimeout === 'function') {
            cachedClearTimeout = clearTimeout;
        } else {
            cachedClearTimeout = defaultClearTimeout;
        }
    } catch (e) {
        cachedClearTimeout = defaultClearTimeout;
    }
} ())
function runTimeout(fun) {
    if (cachedSetTimeout === setTimeout) {
        //normal enviroments in sane situations
        return setTimeout(fun, 0);
    }
    // if setTimeout wasn't available but was latter defined
    if ((cachedSetTimeout === defaultSetTimout || !cachedSetTimeout) && setTimeout) {
        cachedSetTimeout = setTimeout;
        return setTimeout(fun, 0);
    }
    try {
        // when when somebody has screwed with setTimeout but no I.E. maddness
        return cachedSetTimeout(fun, 0);
    } catch(e){
        try {
            // When we are in I.E. but the script has been evaled so I.E. doesn't trust the global object when called normally
            return cachedSetTimeout.call(null, fun, 0);
        } catch(e){
            // same as above but when it's a version of I.E. that must have the global object for 'this', hopfully our context correct otherwise it will throw a global error
            return cachedSetTimeout.call(this, fun, 0);
        }
    }


}
function runClearTimeout(marker) {
    if (cachedClearTimeout === clearTimeout) {
        //normal enviroments in sane situations
        return clearTimeout(marker);
    }
    // if clearTimeout wasn't available but was latter defined
    if ((cachedClearTimeout === defaultClearTimeout || !cachedClearTimeout) && clearTimeout) {
        cachedClearTimeout = clearTimeout;
        return clearTimeout(marker);
    }
    try {
        // when when somebody has screwed with setTimeout but no I.E. maddness
        return cachedClearTimeout(marker);
    } catch (e){
        try {
            // When we are in I.E. but the script has been evaled so I.E. doesn't  trust the global object when called normally
            return cachedClearTimeout.call(null, marker);
        } catch (e){
            // same as above but when it's a version of I.E. that must have the global object for 'this', hopfully our context correct otherwise it will throw a global error.
            // Some versions of I.E. have different rules for clearTimeout vs setTimeout
            return cachedClearTimeout.call(this, marker);
        }
    }



}
var queue = [];
var draining = false;
var currentQueue;
var queueIndex = -1;

function cleanUpNextTick() {
    if (!draining || !currentQueue) {
        return;
    }
    draining = false;
    if (currentQueue.length) {
        queue = currentQueue.concat(queue);
    } else {
        queueIndex = -1;
    }
    if (queue.length) {
        drainQueue();
    }
}

function drainQueue() {
    if (draining) {
        return;
    }
    var timeout = runTimeout(cleanUpNextTick);
    draining = true;

    var len = queue.length;
    while(len) {
        currentQueue = queue;
        queue = [];
        while (++queueIndex < len) {
            if (currentQueue) {
                currentQueue[queueIndex].run();
            }
        }
        queueIndex = -1;
        len = queue.length;
    }
    currentQueue = null;
    draining = false;
    runClearTimeout(timeout);
}

process.nextTick = function (fun) {
    var args = new Array(arguments.length - 1);
    if (arguments.length > 1) {
        for (var i = 1; i < arguments.length; i++) {
            args[i - 1] = arguments[i];
        }
    }
    queue.push(new Item(fun, args));
    if (queue.length === 1 && !draining) {
        runTimeout(drainQueue);
    }
};

// v8 likes predictible objects
function Item(fun, array) {
    this.fun = fun;
    this.array = array;
}
Item.prototype.run = function () {
    this.fun.apply(null, this.array);
};
process.title = 'browser';
process.browser = true;
process.env = {};
process.argv = [];
process.version = ''; // empty string to avoid regexp issues
process.versions = {};

function noop() {}

process.on = noop;
process.addListener = noop;
process.once = noop;
process.off = noop;
process.removeListener = noop;
process.removeAllListeners = noop;
process.emit = noop;
process.prependListener = noop;
process.prependOnceListener = noop;

process.listeners = function (name) { return [] }

process.binding = function (name) {
    throw new Error('process.binding is not supported');
};

process.cwd = function () { return '/' };
process.chdir = function (dir) {
    throw new Error('process.chdir is not supported');
};
process.umask = function() { return 0; };

},{}],2:[function(require,module,exports){
/**
 * @license
 * Copyright 2013 David Eberlein (david.eberlein@ch.sauter-bc.com)
 * MIT-licensed (http://opensource.org/licenses/MIT)
 */

/**
 * @fileoverview DataHandler implementation for the custom bars option.
 * @author David Eberlein (david.eberlein@ch.sauter-bc.com)
 */

/*global Dygraph:false */
"use strict";

Object.defineProperty(exports, '__esModule', {
  value: true
});

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { 'default': obj }; }

var _bars = require('./bars');

var _bars2 = _interopRequireDefault(_bars);

/**
 * @constructor
 * @extends Dygraph.DataHandlers.BarsHandler
 */
var CustomBarsHandler = function CustomBarsHandler() {};

CustomBarsHandler.prototype = new _bars2['default']();

/** @inheritDoc */
CustomBarsHandler.prototype.extractSeries = function (rawData, i, options) {
  // TODO(danvk): pre-allocate series here.
  var series = [];
  var x, y, point;
  var logScale = options.get('logscale');
  for (var j = 0; j < rawData.length; j++) {
    x = rawData[j][0];
    point = rawData[j][i];
    if (logScale && point !== null) {
      // On the log scale, points less than zero do not exist.
      // This will create a gap in the chart.
      if (point[0] <= 0 || point[1] <= 0 || point[2] <= 0) {
        point = null;
      }
    }
    // Extract to the unified data format.
    if (point !== null) {
      y = point[1];
      if (y !== null && !isNaN(y)) {
        series.push([x, y, [point[0], point[2]]]);
      } else {
        series.push([x, y, [y, y]]);
      }
    } else {
      series.push([x, null, [null, null]]);
    }
  }
  return series;
};

/** @inheritDoc */
CustomBarsHandler.prototype.rollingAverage = function (originalData, rollPeriod, options) {
  rollPeriod = Math.min(rollPeriod, originalData.length);
  var rollingData = [];
  var y, low, high, mid, count, i, extremes;

  low = 0;
  mid = 0;
  high = 0;
  count = 0;
  for (i = 0; i < originalData.length; i++) {
    y = originalData[i][1];
    extremes = originalData[i][2];
    rollingData[i] = originalData[i];

    if (y !== null && !isNaN(y)) {
      low += extremes[0];
      mid += y;
      high += extremes[1];
      count += 1;
    }
    if (i - rollPeriod >= 0) {
      var prev = originalData[i - rollPeriod];
      if (prev[1] !== null && !isNaN(prev[1])) {
        low -= prev[2][0];
        mid -= prev[1];
        high -= prev[2][1];
        count -= 1;
      }
    }
    if (count) {
      rollingData[i] = [originalData[i][0], 1.0 * mid / count, [1.0 * low / count, 1.0 * high / count]];
    } else {
      rollingData[i] = [originalData[i][0], null, [null, null]];
    }
  }

  return rollingData;
};

exports['default'] = CustomBarsHandler;
module.exports = exports['default'];

},{"./bars":5}],3:[function(require,module,exports){
/**
 * @license
 * Copyright 2013 David Eberlein (david.eberlein@ch.sauter-bc.com)
 * MIT-licensed (http://opensource.org/licenses/MIT)
 */

/**
 * @fileoverview DataHandler implementation for the error bars option.
 * @author David Eberlein (david.eberlein@ch.sauter-bc.com)
 */

/*global Dygraph:false */
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { "default": obj }; }

var _bars = require('./bars');

var _bars2 = _interopRequireDefault(_bars);

/**
 * @constructor
 * @extends BarsHandler
 */
var ErrorBarsHandler = function ErrorBarsHandler() {};

ErrorBarsHandler.prototype = new _bars2["default"]();

/** @inheritDoc */
ErrorBarsHandler.prototype.extractSeries = function (rawData, i, options) {
  // TODO(danvk): pre-allocate series here.
  var series = [];
  var x, y, variance, point;
  var sigma = options.get("sigma");
  var logScale = options.get('logscale');
  for (var j = 0; j < rawData.length; j++) {
    x = rawData[j][0];
    point = rawData[j][i];
    if (logScale && point !== null) {
      // On the log scale, points less than zero do not exist.
      // This will create a gap in the chart.
      if (point[0] <= 0 || point[0] - sigma * point[1] <= 0) {
        point = null;
      }
    }
    // Extract to the unified data format.
    if (point !== null) {
      y = point[0];
      if (y !== null && !isNaN(y)) {
        variance = sigma * point[1];
        // preserve original error value in extras for further
        // filtering
        series.push([x, y, [y - variance, y + variance, point[1]]]);
      } else {
        series.push([x, y, [y, y, y]]);
      }
    } else {
      series.push([x, null, [null, null, null]]);
    }
  }
  return series;
};

/** @inheritDoc */
ErrorBarsHandler.prototype.rollingAverage = function (originalData, rollPeriod, options) {
  rollPeriod = Math.min(rollPeriod, originalData.length);
  var rollingData = [];
  var sigma = options.get("sigma");

  var i, j, y, v, sum, num_ok, stddev, variance, value;

  // Calculate the rolling average for the first rollPeriod - 1 points
  // where there is not enough data to roll over the full number of points
  for (i = 0; i < originalData.length; i++) {
    sum = 0;
    variance = 0;
    num_ok = 0;
    for (j = Math.max(0, i - rollPeriod + 1); j < i + 1; j++) {
      y = originalData[j][1];
      if (y === null || isNaN(y)) continue;
      num_ok++;
      sum += y;
      variance += Math.pow(originalData[j][2][2], 2);
    }
    if (num_ok) {
      stddev = Math.sqrt(variance) / num_ok;
      value = sum / num_ok;
      rollingData[i] = [originalData[i][0], value, [value - sigma * stddev, value + sigma * stddev]];
    } else {
      // This explicitly preserves NaNs to aid with "independent
      // series".
      // See testRollingAveragePreservesNaNs.
      v = rollPeriod == 1 ? originalData[i][1] : null;
      rollingData[i] = [originalData[i][0], v, [v, v]];
    }
  }

  return rollingData;
};

exports["default"] = ErrorBarsHandler;
module.exports = exports["default"];

},{"./bars":5}],4:[function(require,module,exports){
/**
 * @license
 * Copyright 2013 David Eberlein (david.eberlein@ch.sauter-bc.com)
 * MIT-licensed (http://opensource.org/licenses/MIT)
 */

/**
 * @fileoverview DataHandler implementation for the combination 
 * of error bars and fractions options.
 * @author David Eberlein (david.eberlein@ch.sauter-bc.com)
 */

/*global Dygraph:false */
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { "default": obj }; }

var _bars = require('./bars');

var _bars2 = _interopRequireDefault(_bars);

/**
 * @constructor
 * @extends Dygraph.DataHandlers.BarsHandler
 */
var FractionsBarsHandler = function FractionsBarsHandler() {};

FractionsBarsHandler.prototype = new _bars2["default"]();

/** @inheritDoc */
FractionsBarsHandler.prototype.extractSeries = function (rawData, i, options) {
  // TODO(danvk): pre-allocate series here.
  var series = [];
  var x, y, point, num, den, value, stddev, variance;
  var mult = 100.0;
  var sigma = options.get("sigma");
  var logScale = options.get('logscale');
  for (var j = 0; j < rawData.length; j++) {
    x = rawData[j][0];
    point = rawData[j][i];
    if (logScale && point !== null) {
      // On the log scale, points less than zero do not exist.
      // This will create a gap in the chart.
      if (point[0] <= 0 || point[1] <= 0) {
        point = null;
      }
    }
    // Extract to the unified data format.
    if (point !== null) {
      num = point[0];
      den = point[1];
      if (num !== null && !isNaN(num)) {
        value = den ? num / den : 0.0;
        stddev = den ? sigma * Math.sqrt(value * (1 - value) / den) : 1.0;
        variance = mult * stddev;
        y = mult * value;
        // preserve original values in extras for further filtering
        series.push([x, y, [y - variance, y + variance, num, den]]);
      } else {
        series.push([x, num, [num, num, num, den]]);
      }
    } else {
      series.push([x, null, [null, null, null, null]]);
    }
  }
  return series;
};

/** @inheritDoc */
FractionsBarsHandler.prototype.rollingAverage = function (originalData, rollPeriod, options) {
  rollPeriod = Math.min(rollPeriod, originalData.length);
  var rollingData = [];
  var sigma = options.get("sigma");
  var wilsonInterval = options.get("wilsonInterval");

  var low, high, i, stddev;
  var num = 0;
  var den = 0; // numerator/denominator
  var mult = 100.0;
  for (i = 0; i < originalData.length; i++) {
    num += originalData[i][2][2];
    den += originalData[i][2][3];
    if (i - rollPeriod >= 0) {
      num -= originalData[i - rollPeriod][2][2];
      den -= originalData[i - rollPeriod][2][3];
    }

    var date = originalData[i][0];
    var value = den ? num / den : 0.0;
    if (wilsonInterval) {
      // For more details on this confidence interval, see:
      // http://en.wikipedia.org/wiki/Binomial_confidence_interval
      if (den) {
        var p = value < 0 ? 0 : value,
            n = den;
        var pm = sigma * Math.sqrt(p * (1 - p) / n + sigma * sigma / (4 * n * n));
        var denom = 1 + sigma * sigma / den;
        low = (p + sigma * sigma / (2 * den) - pm) / denom;
        high = (p + sigma * sigma / (2 * den) + pm) / denom;
        rollingData[i] = [date, p * mult, [low * mult, high * mult]];
      } else {
        rollingData[i] = [date, 0, [0, 0]];
      }
    } else {
      stddev = den ? sigma * Math.sqrt(value * (1 - value) / den) : 1.0;
      rollingData[i] = [date, mult * value, [mult * (value - stddev), mult * (value + stddev)]];
    }
  }

  return rollingData;
};

exports["default"] = FractionsBarsHandler;
module.exports = exports["default"];

},{"./bars":5}],5:[function(require,module,exports){
/**
 * @license
 * Copyright 2013 David Eberlein (david.eberlein@ch.sauter-bc.com)
 * MIT-licensed (http://opensource.org/licenses/MIT)
 */

/**
 * @fileoverview DataHandler base implementation for the "bar" 
 * data formats. This implementation must be extended and the
 * extractSeries and rollingAverage must be implemented.
 * @author David Eberlein (david.eberlein@ch.sauter-bc.com)
 */

/*global Dygraph:false */
/*global DygraphLayout:false */
"use strict";

Object.defineProperty(exports, '__esModule', {
  value: true
});

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { 'default': obj }; }

var _datahandler = require('./datahandler');

var _datahandler2 = _interopRequireDefault(_datahandler);

var _dygraphLayout = require('../dygraph-layout');

var _dygraphLayout2 = _interopRequireDefault(_dygraphLayout);

/**
 * @constructor
 * @extends {Dygraph.DataHandler}
 */
var BarsHandler = function BarsHandler() {
  _datahandler2['default'].call(this);
};
BarsHandler.prototype = new _datahandler2['default']();

// TODO(danvk): figure out why the jsdoc has to be copy/pasted from superclass.
//   (I get closure compiler errors if this isn't here.)
/**
 * @override
 * @param {!Array.<Array>} rawData The raw data passed into dygraphs where 
 *     rawData[i] = [x,ySeries1,...,ySeriesN].
 * @param {!number} seriesIndex Index of the series to extract. All other
 *     series should be ignored.
 * @param {!DygraphOptions} options Dygraph options.
 * @return {Array.<[!number,?number,?]>} The series in the unified data format
 *     where series[i] = [x,y,{extras}]. 
 */
BarsHandler.prototype.extractSeries = function (rawData, seriesIndex, options) {
  // Not implemented here must be extended
};

/**
 * @override
 * @param {!Array.<[!number,?number,?]>} series The series in the unified 
 *          data format where series[i] = [x,y,{extras}].
 * @param {!number} rollPeriod The number of points over which to average the data
 * @param {!DygraphOptions} options The dygraph options.
 * TODO(danvk): be more specific than "Array" here.
 * @return {!Array.<[!number,?number,?]>} the rolled series.
 */
BarsHandler.prototype.rollingAverage = function (series, rollPeriod, options) {
  // Not implemented here, must be extended.
};

/** @inheritDoc */
BarsHandler.prototype.onPointsCreated_ = function (series, points) {
  for (var i = 0; i < series.length; ++i) {
    var item = series[i];
    var point = points[i];
    point.y_top = NaN;
    point.y_bottom = NaN;
    point.yval_minus = _datahandler2['default'].parseFloat(item[2][0]);
    point.yval_plus = _datahandler2['default'].parseFloat(item[2][1]);
  }
};

/** @inheritDoc */
BarsHandler.prototype.getExtremeYValues = function (series, dateWindow, options) {
  var minY = null,
      maxY = null,
      y;

  var firstIdx = 0;
  var lastIdx = series.length - 1;

  for (var j = firstIdx; j <= lastIdx; j++) {
    y = series[j][1];
    if (y === null || isNaN(y)) continue;

    var low = series[j][2][0];
    var high = series[j][2][1];

    if (low > y) low = y; // this can happen with custom bars,
    if (high < y) high = y; // e.g. in tests/custom-bars.html

    if (maxY === null || high > maxY) maxY = high;
    if (minY === null || low < minY) minY = low;
  }

  return [minY, maxY];
};

/** @inheritDoc */
BarsHandler.prototype.onLineEvaluated = function (points, axis, logscale) {
  var point;
  for (var j = 0; j < points.length; j++) {
    // Copy over the error terms
    point = points[j];
    point.y_top = _dygraphLayout2['default'].calcYNormal_(axis, point.yval_minus, logscale);
    point.y_bottom = _dygraphLayout2['default'].calcYNormal_(axis, point.yval_plus, logscale);
  }
};

exports['default'] = BarsHandler;
module.exports = exports['default'];

},{"../dygraph-layout":13,"./datahandler":6}],6:[function(require,module,exports){
/**
 * @license
 * Copyright 2013 David Eberlein (david.eberlein@ch.sauter-bc.com)
 * MIT-licensed (http://opensource.org/licenses/MIT)
 */

/**
 * @fileoverview This file contains the managment of data handlers
 * @author David Eberlein (david.eberlein@ch.sauter-bc.com)
 *
 * The idea is to define a common, generic data format that works for all data
 * structures supported by dygraphs. To make this possible, the DataHandler
 * interface is introduced. This makes it possible, that dygraph itself can work
 * with the same logic for every data type independent of the actual format and
 * the DataHandler takes care of the data format specific jobs.
 * DataHandlers are implemented for all data types supported by Dygraphs and
 * return Dygraphs compliant formats.
 * By default the correct DataHandler is chosen based on the options set.
 * Optionally the user may use his own DataHandler (similar to the plugin
 * system).
 *
 *
 * The unified data format returend by each handler is defined as so:
 * series[n][point] = [x,y,(extras)]
 *
 * This format contains the common basis that is needed to draw a simple line
 * series extended by optional extras for more complex graphing types. It
 * contains a primitive x value as first array entry, a primitive y value as
 * second array entry and an optional extras object for additional data needed.
 *
 * x must always be a number.
 * y must always be a number, NaN of type number or null.
 * extras is optional and must be interpreted by the DataHandler. It may be of
 * any type.
 *
 * In practice this might look something like this:
 * default: [x, yVal]
 * errorBar / customBar: [x, yVal, [yTopVariance, yBottomVariance] ]
 *
 */
/*global Dygraph:false */
/*global DygraphLayout:false */

"use strict";

/**
 *
 * The data handler is responsible for all data specific operations. All of the
 * series data it receives and returns is always in the unified data format.
 * Initially the unified data is created by the extractSeries method
 * @constructor
 */
Object.defineProperty(exports, "__esModule", {
  value: true
});
var DygraphDataHandler = function DygraphDataHandler() {};

var handler = DygraphDataHandler;

/**
 * X-value array index constant for unified data samples.
 * @const
 * @type {number}
 */
handler.X = 0;

/**
 * Y-value array index constant for unified data samples.
 * @const
 * @type {number}
 */
handler.Y = 1;

/**
 * Extras-value array index constant for unified data samples.
 * @const
 * @type {number}
 */
handler.EXTRAS = 2;

/**
 * Extracts one series from the raw data (a 2D array) into an array of the
 * unified data format.
 * This is where undesirable points (i.e. negative values on log scales and
 * missing values through which we wish to connect lines) are dropped.
 * TODO(danvk): the "missing values" bit above doesn't seem right.
 *
 * @param {!Array.<Array>} rawData The raw data passed into dygraphs where
 *     rawData[i] = [x,ySeries1,...,ySeriesN].
 * @param {!number} seriesIndex Index of the series to extract. All other
 *     series should be ignored.
 * @param {!DygraphOptions} options Dygraph options.
 * @return {Array.<[!number,?number,?]>} The series in the unified data format
 *     where series[i] = [x,y,{extras}].
 */
handler.prototype.extractSeries = function (rawData, seriesIndex, options) {};

/**
 * Converts a series to a Point array.  The resulting point array must be
 * returned in increasing order of idx property.
 *
 * @param {!Array.<[!number,?number,?]>} series The series in the unified
 *          data format where series[i] = [x,y,{extras}].
 * @param {!string} setName Name of the series.
 * @param {!number} boundaryIdStart Index offset of the first point, equal to the
 *          number of skipped points left of the date window minimum (if any).
 * @return {!Array.<Dygraph.PointType>} List of points for this series.
 */
handler.prototype.seriesToPoints = function (series, setName, boundaryIdStart) {
  // TODO(bhs): these loops are a hot-spot for high-point-count charts. In
  // fact,
  // on chrome+linux, they are 6 times more expensive than iterating through
  // the
  // points and drawing the lines. The brunt of the cost comes from allocating
  // the |point| structures.
  var points = [];
  for (var i = 0; i < series.length; ++i) {
    var item = series[i];
    var yraw = item[1];
    var yval = yraw === null ? null : handler.parseFloat(yraw);
    var point = {
      x: NaN,
      y: NaN,
      xval: handler.parseFloat(item[0]),
      yval: yval,
      name: setName, // TODO(danvk): is this really necessary?
      idx: i + boundaryIdStart
    };
    points.push(point);
  }
  this.onPointsCreated_(series, points);
  return points;
};

/**
 * Callback called for each series after the series points have been generated
 * which will later be used by the plotters to draw the graph.
 * Here data may be added to the seriesPoints which is needed by the plotters.
 * The indexes of series and points are in sync meaning the original data
 * sample for series[i] is points[i].
 *
 * @param {!Array.<[!number,?number,?]>} series The series in the unified
 *     data format where series[i] = [x,y,{extras}].
 * @param {!Array.<Dygraph.PointType>} points The corresponding points passed
 *     to the plotter.
 * @protected
 */
handler.prototype.onPointsCreated_ = function (series, points) {};

/**
 * Calculates the rolling average of a data set.
 *
 * @param {!Array.<[!number,?number,?]>} series The series in the unified
 *          data format where series[i] = [x,y,{extras}].
 * @param {!number} rollPeriod The number of points over which to average the data
 * @param {!DygraphOptions} options The dygraph options.
 * @return {!Array.<[!number,?number,?]>} the rolled series.
 */
handler.prototype.rollingAverage = function (series, rollPeriod, options) {};

/**
 * Computes the range of the data series (including confidence intervals).
 *
 * @param {!Array.<[!number,?number,?]>} series The series in the unified
 *     data format where series[i] = [x, y, {extras}].
 * @param {!Array.<number>} dateWindow The x-value range to display with
 *     the format: [min, max].
 * @param {!DygraphOptions} options The dygraph options.
 * @return {Array.<number>} The low and high extremes of the series in the
 *     given window with the format: [low, high].
 */
handler.prototype.getExtremeYValues = function (series, dateWindow, options) {};

/**
 * Callback called for each series after the layouting data has been
 * calculated before the series is drawn. Here normalized positioning data
 * should be calculated for the extras of each point.
 *
 * @param {!Array.<Dygraph.PointType>} points The points passed to
 *          the plotter.
 * @param {!Object} axis The axis on which the series will be plotted.
 * @param {!boolean} logscale Weather or not to use a logscale.
 */
handler.prototype.onLineEvaluated = function (points, axis, logscale) {};

/**
 * Optimized replacement for parseFloat, which was way too slow when almost
 * all values were type number, with few edge cases, none of which were strings.
 * @param {?number} val
 * @return {number}
 * @protected
 */
handler.parseFloat = function (val) {
  // parseFloat(null) is NaN
  if (val === null) {
    return NaN;
  }

  // Assume it's a number or NaN. If it's something else, I'll be shocked.
  return val;
};

exports["default"] = DygraphDataHandler;
module.exports = exports["default"];

},{}],7:[function(require,module,exports){
/**
 * @license
 * Copyright 2013 David Eberlein (david.eberlein@ch.sauter-bc.com)
 * MIT-licensed (http://opensource.org/licenses/MIT)
 */

/**
 * @fileoverview DataHandler implementation for the fractions option.
 * @author David Eberlein (david.eberlein@ch.sauter-bc.com)
 */

/*global Dygraph:false */
"use strict";

Object.defineProperty(exports, '__esModule', {
  value: true
});

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { 'default': obj }; }

var _datahandler = require('./datahandler');

var _datahandler2 = _interopRequireDefault(_datahandler);

var _default = require('./default');

var _default2 = _interopRequireDefault(_default);

/**
 * @extends DefaultHandler
 * @constructor
 */
var DefaultFractionHandler = function DefaultFractionHandler() {};

DefaultFractionHandler.prototype = new _default2['default']();

DefaultFractionHandler.prototype.extractSeries = function (rawData, i, options) {
  // TODO(danvk): pre-allocate series here.
  var series = [];
  var x, y, point, num, den, value;
  var mult = 100.0;
  var logScale = options.get('logscale');
  for (var j = 0; j < rawData.length; j++) {
    x = rawData[j][0];
    point = rawData[j][i];
    if (logScale && point !== null) {
      // On the log scale, points less than zero do not exist.
      // This will create a gap in the chart.
      if (point[0] <= 0 || point[1] <= 0) {
        point = null;
      }
    }
    // Extract to the unified data format.
    if (point !== null) {
      num = point[0];
      den = point[1];
      if (num !== null && !isNaN(num)) {
        value = den ? num / den : 0.0;
        y = mult * value;
        // preserve original values in extras for further filtering
        series.push([x, y, [num, den]]);
      } else {
        series.push([x, num, [num, den]]);
      }
    } else {
      series.push([x, null, [null, null]]);
    }
  }
  return series;
};

DefaultFractionHandler.prototype.rollingAverage = function (originalData, rollPeriod, options) {
  rollPeriod = Math.min(rollPeriod, originalData.length);
  var rollingData = [];

  var i;
  var num = 0;
  var den = 0; // numerator/denominator
  var mult = 100.0;
  for (i = 0; i < originalData.length; i++) {
    num += originalData[i][2][0];
    den += originalData[i][2][1];
    if (i - rollPeriod >= 0) {
      num -= originalData[i - rollPeriod][2][0];
      den -= originalData[i - rollPeriod][2][1];
    }

    var date = originalData[i][0];
    var value = den ? num / den : 0.0;
    rollingData[i] = [date, mult * value];
  }

  return rollingData;
};

exports['default'] = DefaultFractionHandler;
module.exports = exports['default'];

},{"./datahandler":6,"./default":8}],8:[function(require,module,exports){
/**
 * @license
 * Copyright 2013 David Eberlein (david.eberlein@ch.sauter-bc.com)
 * MIT-licensed (http://opensource.org/licenses/MIT)
 */

/**
 * @fileoverview DataHandler default implementation used for simple line charts.
 * @author David Eberlein (david.eberlein@ch.sauter-bc.com)
 */

/*global Dygraph:false */
"use strict";

Object.defineProperty(exports, '__esModule', {
  value: true
});

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { 'default': obj }; }

var _datahandler = require('./datahandler');

var _datahandler2 = _interopRequireDefault(_datahandler);

/**
 * @constructor
 * @extends Dygraph.DataHandler
 */
var DefaultHandler = function DefaultHandler() {};

DefaultHandler.prototype = new _datahandler2['default']();

/** @inheritDoc */
DefaultHandler.prototype.extractSeries = function (rawData, i, options) {
  // TODO(danvk): pre-allocate series here.
  var series = [];
  var logScale = options.get('logscale');
  for (var j = 0; j < rawData.length; j++) {
    var x = rawData[j][0];
    var point = rawData[j][i];
    if (logScale) {
      // On the log scale, points less than zero do not exist.
      // This will create a gap in the chart.
      if (point <= 0) {
        point = null;
      }
    }
    series.push([x, point]);
  }
  return series;
};

/** @inheritDoc */
DefaultHandler.prototype.rollingAverage = function (originalData, rollPeriod, options) {
  rollPeriod = Math.min(rollPeriod, originalData.length);
  var rollingData = [];

  var i, j, y, sum, num_ok;
  // Calculate the rolling average for the first rollPeriod - 1 points
  // where
  // there is not enough data to roll over the full number of points
  if (rollPeriod == 1) {
    return originalData;
  }
  for (i = 0; i < originalData.length; i++) {
    sum = 0;
    num_ok = 0;
    for (j = Math.max(0, i - rollPeriod + 1); j < i + 1; j++) {
      y = originalData[j][1];
      if (y === null || isNaN(y)) continue;
      num_ok++;
      sum += originalData[j][1];
    }
    if (num_ok) {
      rollingData[i] = [originalData[i][0], sum / num_ok];
    } else {
      rollingData[i] = [originalData[i][0], null];
    }
  }

  return rollingData;
};

/** @inheritDoc */
DefaultHandler.prototype.getExtremeYValues = function (series, dateWindow, options) {
  var minY = null,
      maxY = null,
      y;
  var firstIdx = 0,
      lastIdx = series.length - 1;

  for (var j = firstIdx; j <= lastIdx; j++) {
    y = series[j][1];
    if (y === null || isNaN(y)) continue;
    if (maxY === null || y > maxY) {
      maxY = y;
    }
    if (minY === null || y < minY) {
      minY = y;
    }
  }
  return [minY, maxY];
};

exports['default'] = DefaultHandler;
module.exports = exports['default'];

},{"./datahandler":6}],9:[function(require,module,exports){
/**
 * @license
 * Copyright 2006 Dan Vanderkam (danvdk@gmail.com)
 * MIT-licensed (http://opensource.org/licenses/MIT)
 */

/**
 * @fileoverview Based on PlotKit.CanvasRenderer, but modified to meet the
 * needs of dygraphs.
 *
 * In particular, support for:
 * - grid overlays
 * - error bars
 * - dygraphs attribute system
 */

/**
 * The DygraphCanvasRenderer class does the actual rendering of the chart onto
 * a canvas. It's based on PlotKit.CanvasRenderer.
 * @param {Object} element The canvas to attach to
 * @param {Object} elementContext The 2d context of the canvas (injected so it
 * can be mocked for testing.)
 * @param {Layout} layout The DygraphLayout object for this graph.
 * @constructor
 */

/*global Dygraph:false */
"use strict";

Object.defineProperty(exports, '__esModule', {
  value: true
});

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { 'default': obj }; }

function _interopRequireWildcard(obj) { if (obj && obj.__esModule) { return obj; } else { var newObj = {}; if (obj != null) { for (var key in obj) { if (Object.prototype.hasOwnProperty.call(obj, key)) newObj[key] = obj[key]; } } newObj['default'] = obj; return newObj; } }

var _dygraphUtils = require('./dygraph-utils');

var utils = _interopRequireWildcard(_dygraphUtils);

var _dygraph = require('./dygraph');

var _dygraph2 = _interopRequireDefault(_dygraph);

/**
 * @constructor
 *
 * This gets called when there are "new points" to chart. This is generally the
 * case when the underlying data being charted has changed. It is _not_ called
 * in the common case that the user has zoomed or is panning the view.
 *
 * The chart canvas has already been created by the Dygraph object. The
 * renderer simply gets a drawing context.
 *
 * @param {Dygraph} dygraph The chart to which this renderer belongs.
 * @param {HTMLCanvasElement} element The &lt;canvas&gt; DOM element on which to draw.
 * @param {CanvasRenderingContext2D} elementContext The drawing context.
 * @param {DygraphLayout} layout The chart's DygraphLayout object.
 *
 * TODO(danvk): remove the elementContext property.
 */
var DygraphCanvasRenderer = function DygraphCanvasRenderer(dygraph, element, elementContext, layout) {
  this.dygraph_ = dygraph;

  this.layout = layout;
  this.element = element;
  this.elementContext = elementContext;

  this.height = dygraph.height_;
  this.width = dygraph.width_;

  // --- check whether everything is ok before we return
  if (!utils.isCanvasSupported(this.element)) {
    throw "Canvas is not supported.";
  }

  // internal state
  this.area = layout.getPlotArea();

  // Set up a clipping area for the canvas (and the interaction canvas).
  // This ensures that we don't overdraw.
  var ctx = this.dygraph_.canvas_ctx_;
  ctx.beginPath();
  ctx.rect(this.area.x, this.area.y, this.area.w, this.area.h);
  ctx.clip();

  ctx = this.dygraph_.hidden_ctx_;
  ctx.beginPath();
  ctx.rect(this.area.x, this.area.y, this.area.w, this.area.h);
  ctx.clip();
};

/**
 * Clears out all chart content and DOM elements.
 * This is called immediately before render() on every frame, including
 * during zooms and pans.
 * @private
 */
DygraphCanvasRenderer.prototype.clear = function () {
  this.elementContext.clearRect(0, 0, this.width, this.height);
};

/**
 * This method is responsible for drawing everything on the chart, including
 * lines, error bars, fills and axes.
 * It is called immediately after clear() on every frame, including during pans
 * and zooms.
 * @private
 */
DygraphCanvasRenderer.prototype.render = function () {
  // attaches point.canvas{x,y}
  this._updatePoints();

  // actually draws the chart.
  this._renderLineChart();
};

/**
 * Returns a predicate to be used with an iterator, which will
 * iterate over points appropriately, depending on whether
 * connectSeparatedPoints is true. When it's false, the predicate will
 * skip over points with missing yVals.
 */
DygraphCanvasRenderer._getIteratorPredicate = function (connectSeparatedPoints) {
  return connectSeparatedPoints ? DygraphCanvasRenderer._predicateThatSkipsEmptyPoints : null;
};

DygraphCanvasRenderer._predicateThatSkipsEmptyPoints = function (array, idx) {
  return array[idx].yval !== null;
};

/**
 * Draws a line with the styles passed in and calls all the drawPointCallbacks.
 * @param {Object} e The dictionary passed to the plotter function.
 * @private
 */
DygraphCanvasRenderer._drawStyledLine = function (e, color, strokeWidth, strokePattern, drawPoints, drawPointCallback, pointSize) {
  var g = e.dygraph;
  // TODO(konigsberg): Compute attributes outside this method call.
  var stepPlot = g.getBooleanOption("stepPlot", e.setName);

  if (!utils.isArrayLike(strokePattern)) {
    strokePattern = null;
  }

  var drawGapPoints = g.getBooleanOption('drawGapEdgePoints', e.setName);

  var points = e.points;
  var setName = e.setName;
  var iter = utils.createIterator(points, 0, points.length, DygraphCanvasRenderer._getIteratorPredicate(g.getBooleanOption("connectSeparatedPoints", setName)));

  var stroking = strokePattern && strokePattern.length >= 2;

  var ctx = e.drawingContext;
  ctx.save();
  if (stroking) {
    if (ctx.setLineDash) ctx.setLineDash(strokePattern);
  }

  var pointsOnLine = DygraphCanvasRenderer._drawSeries(e, iter, strokeWidth, pointSize, drawPoints, drawGapPoints, stepPlot, color);
  DygraphCanvasRenderer._drawPointsOnLine(e, pointsOnLine, drawPointCallback, color, pointSize);

  if (stroking) {
    if (ctx.setLineDash) ctx.setLineDash([]);
  }

  ctx.restore();
};

/**
 * This does the actual drawing of lines on the canvas, for just one series.
 * Returns a list of [canvasx, canvasy] pairs for points for which a
 * drawPointCallback should be fired.  These include isolated points, or all
 * points if drawPoints=true.
 * @param {Object} e The dictionary passed to the plotter function.
 * @private
 */
DygraphCanvasRenderer._drawSeries = function (e, iter, strokeWidth, pointSize, drawPoints, drawGapPoints, stepPlot, color) {

  var prevCanvasX = null;
  var prevCanvasY = null;
  var nextCanvasY = null;
  var isIsolated; // true if this point is isolated (no line segments)
  var point; // the point being processed in the while loop
  var pointsOnLine = []; // Array of [canvasx, canvasy] pairs.
  var first = true; // the first cycle through the while loop

  var ctx = e.drawingContext;
  ctx.beginPath();
  ctx.strokeStyle = color;
  ctx.lineWidth = strokeWidth;

  // NOTE: we break the iterator's encapsulation here for about a 25% speedup.
  var arr = iter.array_;
  var limit = iter.end_;
  var predicate = iter.predicate_;

  for (var i = iter.start_; i < limit; i++) {
    point = arr[i];
    if (predicate) {
      while (i < limit && !predicate(arr, i)) {
        i++;
      }
      if (i == limit) break;
      point = arr[i];
    }

    // FIXME: The 'canvasy != canvasy' test here catches NaN values but the test
    // doesn't catch Infinity values. Could change this to
    // !isFinite(point.canvasy), but I assume it avoids isNaN for performance?
    if (point.canvasy === null || point.canvasy != point.canvasy) {
      if (stepPlot && prevCanvasX !== null) {
        // Draw a horizontal line to the start of the missing data
        ctx.moveTo(prevCanvasX, prevCanvasY);
        ctx.lineTo(point.canvasx, prevCanvasY);
      }
      prevCanvasX = prevCanvasY = null;
    } else {
      isIsolated = false;
      if (drawGapPoints || prevCanvasX === null) {
        iter.nextIdx_ = i;
        iter.next();
        nextCanvasY = iter.hasNext ? iter.peek.canvasy : null;

        var isNextCanvasYNullOrNaN = nextCanvasY === null || nextCanvasY != nextCanvasY;
        isIsolated = prevCanvasX === null && isNextCanvasYNullOrNaN;
        if (drawGapPoints) {
          // Also consider a point to be "isolated" if it's adjacent to a
          // null point, excluding the graph edges.
          if (!first && prevCanvasX === null || iter.hasNext && isNextCanvasYNullOrNaN) {
            isIsolated = true;
          }
        }
      }

      if (prevCanvasX !== null) {
        if (strokeWidth) {
          if (stepPlot) {
            ctx.moveTo(prevCanvasX, prevCanvasY);
            ctx.lineTo(point.canvasx, prevCanvasY);
          }

          ctx.lineTo(point.canvasx, point.canvasy);
        }
      } else {
        ctx.moveTo(point.canvasx, point.canvasy);
      }
      if (drawPoints || isIsolated) {
        pointsOnLine.push([point.canvasx, point.canvasy, point.idx]);
      }
      prevCanvasX = point.canvasx;
      prevCanvasY = point.canvasy;
    }
    first = false;
  }
  ctx.stroke();
  return pointsOnLine;
};

/**
 * This fires the drawPointCallback functions, which draw dots on the points by
 * default. This gets used when the "drawPoints" option is set, or when there
 * are isolated points.
 * @param {Object} e The dictionary passed to the plotter function.
 * @private
 */
DygraphCanvasRenderer._drawPointsOnLine = function (e, pointsOnLine, drawPointCallback, color, pointSize) {
  var ctx = e.drawingContext;
  for (var idx = 0; idx < pointsOnLine.length; idx++) {
    var cb = pointsOnLine[idx];
    ctx.save();
    drawPointCallback.call(e.dygraph, e.dygraph, e.setName, ctx, cb[0], cb[1], color, pointSize, cb[2]);
    ctx.restore();
  }
};

/**
 * Attaches canvas coordinates to the points array.
 * @private
 */
DygraphCanvasRenderer.prototype._updatePoints = function () {
  // Update Points
  // TODO(danvk): here
  //
  // TODO(bhs): this loop is a hot-spot for high-point-count charts. These
  // transformations can be pushed into the canvas via linear transformation
  // matrices.
  // NOTE(danvk): this is trickier than it sounds at first. The transformation
  // needs to be done before the .moveTo() and .lineTo() calls, but must be
  // undone before the .stroke() call to ensure that the stroke width is
  // unaffected.  An alternative is to reduce the stroke width in the
  // transformed coordinate space, but you can't specify different values for
  // each dimension (as you can with .scale()). The speedup here is ~12%.
  var sets = this.layout.points;
  for (var i = sets.length; i--;) {
    var points = sets[i];
    for (var j = points.length; j--;) {
      var point = points[j];
      point.canvasx = this.area.w * point.x + this.area.x;
      point.canvasy = this.area.h * point.y + this.area.y;
    }
  }
};

/**
 * Add canvas Actually draw the lines chart, including error bars.
 *
 * This function can only be called if DygraphLayout's points array has been
 * updated with canvas{x,y} attributes, i.e. by
 * DygraphCanvasRenderer._updatePoints.
 *
 * @param {string=} opt_seriesName when specified, only that series will
 *     be drawn. (This is used for expedited redrawing with highlightSeriesOpts)
 * @param {CanvasRenderingContext2D} opt_ctx when specified, the drawing
 *     context.  However, lines are typically drawn on the object's
 *     elementContext.
 * @private
 */
DygraphCanvasRenderer.prototype._renderLineChart = function (opt_seriesName, opt_ctx) {
  var ctx = opt_ctx || this.elementContext;
  var i;

  var sets = this.layout.points;
  var setNames = this.layout.setNames;
  var setName;

  this.colors = this.dygraph_.colorsMap_;

  // Determine which series have specialized plotters.
  var plotter_attr = this.dygraph_.getOption("plotter");
  var plotters = plotter_attr;
  if (!utils.isArrayLike(plotters)) {
    plotters = [plotters];
  }

  var setPlotters = {}; // series name -> plotter fn.
  for (i = 0; i < setNames.length; i++) {
    setName = setNames[i];
    var setPlotter = this.dygraph_.getOption("plotter", setName);
    if (setPlotter == plotter_attr) continue; // not specialized.

    setPlotters[setName] = setPlotter;
  }

  for (i = 0; i < plotters.length; i++) {
    var plotter = plotters[i];
    var is_last = i == plotters.length - 1;

    for (var j = 0; j < sets.length; j++) {
      setName = setNames[j];
      if (opt_seriesName && setName != opt_seriesName) continue;

      var points = sets[j];

      // Only throw in the specialized plotters on the last iteration.
      var p = plotter;
      if (setName in setPlotters) {
        if (is_last) {
          p = setPlotters[setName];
        } else {
          // Don't use the standard plotters in this case.
          continue;
        }
      }

      var color = this.colors[setName];
      var strokeWidth = this.dygraph_.getOption("strokeWidth", setName);

      ctx.save();
      ctx.strokeStyle = color;
      ctx.lineWidth = strokeWidth;
      p({
        points: points,
        setName: setName,
        drawingContext: ctx,
        color: color,
        strokeWidth: strokeWidth,
        dygraph: this.dygraph_,
        axis: this.dygraph_.axisPropertiesForSeries(setName),
        plotArea: this.area,
        seriesIndex: j,
        seriesCount: sets.length,
        singleSeriesName: opt_seriesName,
        allSeriesPoints: sets
      });
      ctx.restore();
    }
  }
};

/**
 * Standard plotters. These may be used by clients via Dygraph.Plotters.
 * See comments there for more details.
 */
DygraphCanvasRenderer._Plotters = {
  linePlotter: function linePlotter(e) {
    DygraphCanvasRenderer._linePlotter(e);
  },

  fillPlotter: function fillPlotter(e) {
    DygraphCanvasRenderer._fillPlotter(e);
  },

  errorPlotter: function errorPlotter(e) {
    DygraphCanvasRenderer._errorPlotter(e);
  }
};

/**
 * Plotter which draws the central lines for a series.
 * @private
 */
DygraphCanvasRenderer._linePlotter = function (e) {
  var g = e.dygraph;
  var setName = e.setName;
  var strokeWidth = e.strokeWidth;

  // TODO(danvk): Check if there's any performance impact of just calling
  // getOption() inside of _drawStyledLine. Passing in so many parameters makes
  // this code a bit nasty.
  var borderWidth = g.getNumericOption("strokeBorderWidth", setName);
  var drawPointCallback = g.getOption("drawPointCallback", setName) || utils.Circles.DEFAULT;
  var strokePattern = g.getOption("strokePattern", setName);
  var drawPoints = g.getBooleanOption("drawPoints", setName);
  var pointSize = g.getNumericOption("pointSize", setName);

  if (borderWidth && strokeWidth) {
    DygraphCanvasRenderer._drawStyledLine(e, g.getOption("strokeBorderColor", setName), strokeWidth + 2 * borderWidth, strokePattern, drawPoints, drawPointCallback, pointSize);
  }

  DygraphCanvasRenderer._drawStyledLine(e, e.color, strokeWidth, strokePattern, drawPoints, drawPointCallback, pointSize);
};

/**
 * Draws the shaded error bars/confidence intervals for each series.
 * This happens before the center lines are drawn, since the center lines
 * need to be drawn on top of the error bars for all series.
 * @private
 */
DygraphCanvasRenderer._errorPlotter = function (e) {
  var g = e.dygraph;
  var setName = e.setName;
  var errorBars = g.getBooleanOption("errorBars") || g.getBooleanOption("customBars");
  if (!errorBars) return;

  var fillGraph = g.getBooleanOption("fillGraph", setName);
  if (fillGraph) {
    console.warn("Can't use fillGraph option with error bars");
  }

  var ctx = e.drawingContext;
  var color = e.color;
  var fillAlpha = g.getNumericOption('fillAlpha', setName);
  var stepPlot = g.getBooleanOption("stepPlot", setName);
  var points = e.points;

  var iter = utils.createIterator(points, 0, points.length, DygraphCanvasRenderer._getIteratorPredicate(g.getBooleanOption("connectSeparatedPoints", setName)));

  var newYs;

  // setup graphics context
  var prevX = NaN;
  var prevY = NaN;
  var prevYs = [-1, -1];
  // should be same color as the lines but only 15% opaque.
  var rgb = utils.toRGB_(color);
  var err_color = 'rgba(' + rgb.r + ',' + rgb.g + ',' + rgb.b + ',' + fillAlpha + ')';
  ctx.fillStyle = err_color;
  ctx.beginPath();

  var isNullUndefinedOrNaN = function isNullUndefinedOrNaN(x) {
    return x === null || x === undefined || isNaN(x);
  };

  while (iter.hasNext) {
    var point = iter.next();
    if (!stepPlot && isNullUndefinedOrNaN(point.y) || stepPlot && !isNaN(prevY) && isNullUndefinedOrNaN(prevY)) {
      prevX = NaN;
      continue;
    }

    newYs = [point.y_bottom, point.y_top];
    if (stepPlot) {
      prevY = point.y;
    }

    // The documentation specifically disallows nulls inside the point arrays,
    // but in case it happens we should do something sensible.
    if (isNaN(newYs[0])) newYs[0] = point.y;
    if (isNaN(newYs[1])) newYs[1] = point.y;

    newYs[0] = e.plotArea.h * newYs[0] + e.plotArea.y;
    newYs[1] = e.plotArea.h * newYs[1] + e.plotArea.y;
    if (!isNaN(prevX)) {
      if (stepPlot) {
        ctx.moveTo(prevX, prevYs[0]);
        ctx.lineTo(point.canvasx, prevYs[0]);
        ctx.lineTo(point.canvasx, prevYs[1]);
      } else {
        ctx.moveTo(prevX, prevYs[0]);
        ctx.lineTo(point.canvasx, newYs[0]);
        ctx.lineTo(point.canvasx, newYs[1]);
      }
      ctx.lineTo(prevX, prevYs[1]);
      ctx.closePath();
    }
    prevYs = newYs;
    prevX = point.canvasx;
  }
  ctx.fill();
};

/**
 * Proxy for CanvasRenderingContext2D which drops moveTo/lineTo calls which are
 * superfluous. It accumulates all movements which haven't changed the x-value
 * and only applies the two with the most extreme y-values.
 *
 * Calls to lineTo/moveTo must have non-decreasing x-values.
 */
DygraphCanvasRenderer._fastCanvasProxy = function (context) {
  var pendingActions = []; // array of [type, x, y] tuples
  var lastRoundedX = null;
  var lastFlushedX = null;

  var LINE_TO = 1,
      MOVE_TO = 2;

  var actionCount = 0; // number of moveTos and lineTos passed to context.

  // Drop superfluous motions
  // Assumes all pendingActions have the same (rounded) x-value.
  var compressActions = function compressActions(opt_losslessOnly) {
    if (pendingActions.length <= 1) return;

    // Lossless compression: drop inconsequential moveTos.
    for (var i = pendingActions.length - 1; i > 0; i--) {
      var action = pendingActions[i];
      if (action[0] == MOVE_TO) {
        var prevAction = pendingActions[i - 1];
        if (prevAction[1] == action[1] && prevAction[2] == action[2]) {
          pendingActions.splice(i, 1);
        }
      }
    }

    // Lossless compression: ... drop consecutive moveTos ...
    for (var i = 0; i < pendingActions.length - 1;) /* incremented internally */{
      var action = pendingActions[i];
      if (action[0] == MOVE_TO && pendingActions[i + 1][0] == MOVE_TO) {
        pendingActions.splice(i, 1);
      } else {
        i++;
      }
    }

    // Lossy compression: ... drop all but the extreme y-values ...
    if (pendingActions.length > 2 && !opt_losslessOnly) {
      // keep an initial moveTo, but drop all others.
      var startIdx = 0;
      if (pendingActions[0][0] == MOVE_TO) startIdx++;
      var minIdx = null,
          maxIdx = null;
      for (var i = startIdx; i < pendingActions.length; i++) {
        var action = pendingActions[i];
        if (action[0] != LINE_TO) continue;
        if (minIdx === null && maxIdx === null) {
          minIdx = i;
          maxIdx = i;
        } else {
          var y = action[2];
          if (y < pendingActions[minIdx][2]) {
            minIdx = i;
          } else if (y > pendingActions[maxIdx][2]) {
            maxIdx = i;
          }
        }
      }
      var minAction = pendingActions[minIdx],
          maxAction = pendingActions[maxIdx];
      pendingActions.splice(startIdx, pendingActions.length - startIdx);
      if (minIdx < maxIdx) {
        pendingActions.push(minAction);
        pendingActions.push(maxAction);
      } else if (minIdx > maxIdx) {
        pendingActions.push(maxAction);
        pendingActions.push(minAction);
      } else {
        pendingActions.push(minAction);
      }
    }
  };

  var flushActions = function flushActions(opt_noLossyCompression) {
    compressActions(opt_noLossyCompression);
    for (var i = 0, len = pendingActions.length; i < len; i++) {
      var action = pendingActions[i];
      if (action[0] == LINE_TO) {
        context.lineTo(action[1], action[2]);
      } else if (action[0] == MOVE_TO) {
        context.moveTo(action[1], action[2]);
      }
    }
    if (pendingActions.length) {
      lastFlushedX = pendingActions[pendingActions.length - 1][1];
    }
    actionCount += pendingActions.length;
    pendingActions = [];
  };

  var addAction = function addAction(action, x, y) {
    var rx = Math.round(x);
    if (lastRoundedX === null || rx != lastRoundedX) {
      // if there are large gaps on the x-axis, it's essential to keep the
      // first and last point as well.
      var hasGapOnLeft = lastRoundedX - lastFlushedX > 1,
          hasGapOnRight = rx - lastRoundedX > 1,
          hasGap = hasGapOnLeft || hasGapOnRight;
      flushActions(hasGap);
      lastRoundedX = rx;
    }
    pendingActions.push([action, x, y]);
  };

  return {
    moveTo: function moveTo(x, y) {
      addAction(MOVE_TO, x, y);
    },
    lineTo: function lineTo(x, y) {
      addAction(LINE_TO, x, y);
    },

    // for major operations like stroke/fill, we skip compression to ensure
    // that there are no artifacts at the right edge.
    stroke: function stroke() {
      flushActions(true);context.stroke();
    },
    fill: function fill() {
      flushActions(true);context.fill();
    },
    beginPath: function beginPath() {
      flushActions(true);context.beginPath();
    },
    closePath: function closePath() {
      flushActions(true);context.closePath();
    },

    _count: function _count() {
      return actionCount;
    }
  };
};

/**
 * Draws the shaded regions when "fillGraph" is set. Not to be confused with
 * error bars.
 *
 * For stacked charts, it's more convenient to handle all the series
 * simultaneously. So this plotter plots all the points on the first series
 * it's asked to draw, then ignores all the other series.
 *
 * @private
 */
DygraphCanvasRenderer._fillPlotter = function (e) {
  // Skip if we're drawing a single series for interactive highlight overlay.
  if (e.singleSeriesName) return;

  // We'll handle all the series at once, not one-by-one.
  if (e.seriesIndex !== 0) return;

  var g = e.dygraph;
  var setNames = g.getLabels().slice(1); // remove x-axis

  // getLabels() includes names for invisible series, which are not included in
  // allSeriesPoints. We remove those to make the two match.
  // TODO(danvk): provide a simpler way to get this information.
  for (var i = setNames.length; i >= 0; i--) {
    if (!g.visibility()[i]) setNames.splice(i, 1);
  }

  var anySeriesFilled = (function () {
    for (var i = 0; i < setNames.length; i++) {
      if (g.getBooleanOption("fillGraph", setNames[i])) return true;
    }
    return false;
  })();

  if (!anySeriesFilled) return;

  var area = e.plotArea;
  var sets = e.allSeriesPoints;
  var setCount = sets.length;

  var stackedGraph = g.getBooleanOption("stackedGraph");
  var colors = g.getColors();

  // For stacked graphs, track the baseline for filling.
  //
  // The filled areas below graph lines are trapezoids with two
  // vertical edges. The top edge is the line segment being drawn, and
  // the baseline is the bottom edge. Each baseline corresponds to the
  // top line segment from the previous stacked line. In the case of
  // step plots, the trapezoids are rectangles.
  var baseline = {};
  var currBaseline;
  var prevStepPlot; // for different line drawing modes (line/step) per series

  // Helper function to trace a line back along the baseline.
  var traceBackPath = function traceBackPath(ctx, baselineX, baselineY, pathBack) {
    ctx.lineTo(baselineX, baselineY);
    if (stackedGraph) {
      for (var i = pathBack.length - 1; i >= 0; i--) {
        var pt = pathBack[i];
        ctx.lineTo(pt[0], pt[1]);
      }
    }
  };

  // process sets in reverse order (needed for stacked graphs)
  for (var setIdx = setCount - 1; setIdx >= 0; setIdx--) {
    var ctx = e.drawingContext;
    var setName = setNames[setIdx];
    if (!g.getBooleanOption('fillGraph', setName)) continue;

    var fillAlpha = g.getNumericOption('fillAlpha', setName);
    var stepPlot = g.getBooleanOption('stepPlot', setName);
    var color = colors[setIdx];
    var axis = g.axisPropertiesForSeries(setName);
    var axisY = 1.0 + axis.minyval * axis.yscale;
    if (axisY < 0.0) axisY = 0.0;else if (axisY > 1.0) axisY = 1.0;
    axisY = area.h * axisY + area.y;

    var points = sets[setIdx];
    var iter = utils.createIterator(points, 0, points.length, DygraphCanvasRenderer._getIteratorPredicate(g.getBooleanOption("connectSeparatedPoints", setName)));

    // setup graphics context
    var prevX = NaN;
    var prevYs = [-1, -1];
    var newYs;
    // should be same color as the lines but only 15% opaque.
    var rgb = utils.toRGB_(color);
    var err_color = 'rgba(' + rgb.r + ',' + rgb.g + ',' + rgb.b + ',' + fillAlpha + ')';
    ctx.fillStyle = err_color;
    ctx.beginPath();
    var last_x,
        is_first = true;

    // If the point density is high enough, dropping segments on their way to
    // the canvas justifies the overhead of doing so.
    if (points.length > 2 * g.width_ || _dygraph2['default'].FORCE_FAST_PROXY) {
      ctx = DygraphCanvasRenderer._fastCanvasProxy(ctx);
    }

    // For filled charts, we draw points from left to right, then back along
    // the x-axis to complete a shape for filling.
    // For stacked plots, this "back path" is a more complex shape. This array
    // stores the [x, y] values needed to trace that shape.
    var pathBack = [];

    // TODO(danvk): there are a lot of options at play in this loop.
    //     The logic would be much clearer if some (e.g. stackGraph and
    //     stepPlot) were split off into separate sub-plotters.
    var point;
    while (iter.hasNext) {
      point = iter.next();
      if (!utils.isOK(point.y) && !stepPlot) {
        traceBackPath(ctx, prevX, prevYs[1], pathBack);
        pathBack = [];
        prevX = NaN;
        if (point.y_stacked !== null && !isNaN(point.y_stacked)) {
          baseline[point.canvasx] = area.h * point.y_stacked + area.y;
        }
        continue;
      }
      if (stackedGraph) {
        if (!is_first && last_x == point.xval) {
          continue;
        } else {
          is_first = false;
          last_x = point.xval;
        }

        currBaseline = baseline[point.canvasx];
        var lastY;
        if (currBaseline === undefined) {
          lastY = axisY;
        } else {
          if (prevStepPlot) {
            lastY = currBaseline[0];
          } else {
            lastY = currBaseline;
          }
        }
        newYs = [point.canvasy, lastY];

        if (stepPlot) {
          // Step plots must keep track of the top and bottom of
          // the baseline at each point.
          if (prevYs[0] === -1) {
            baseline[point.canvasx] = [point.canvasy, axisY];
          } else {
            baseline[point.canvasx] = [point.canvasy, prevYs[0]];
          }
        } else {
          baseline[point.canvasx] = point.canvasy;
        }
      } else {
        if (isNaN(point.canvasy) && stepPlot) {
          newYs = [area.y + area.h, axisY];
        } else {
          newYs = [point.canvasy, axisY];
        }
      }
      if (!isNaN(prevX)) {
        // Move to top fill point
        if (stepPlot) {
          ctx.lineTo(point.canvasx, prevYs[0]);
          ctx.lineTo(point.canvasx, newYs[0]);
        } else {
          ctx.lineTo(point.canvasx, newYs[0]);
        }

        // Record the baseline for the reverse path.
        if (stackedGraph) {
          pathBack.push([prevX, prevYs[1]]);
          if (prevStepPlot && currBaseline) {
            // Draw to the bottom of the baseline
            pathBack.push([point.canvasx, currBaseline[1]]);
          } else {
            pathBack.push([point.canvasx, newYs[1]]);
          }
        }
      } else {
        ctx.moveTo(point.canvasx, newYs[1]);
        ctx.lineTo(point.canvasx, newYs[0]);
      }
      prevYs = newYs;
      prevX = point.canvasx;
    }
    prevStepPlot = stepPlot;
    if (newYs && point) {
      traceBackPath(ctx, point.canvasx, newYs[1], pathBack);
      pathBack = [];
    }
    ctx.fill();
  }
};

exports['default'] = DygraphCanvasRenderer;
module.exports = exports['default'];

},{"./dygraph":18,"./dygraph-utils":17}],10:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, '__esModule', {
  value: true
});

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { 'default': obj }; }

function _interopRequireWildcard(obj) { if (obj && obj.__esModule) { return obj; } else { var newObj = {}; if (obj != null) { for (var key in obj) { if (Object.prototype.hasOwnProperty.call(obj, key)) newObj[key] = obj[key]; } } newObj['default'] = obj; return newObj; } }

var _dygraphTickers = require('./dygraph-tickers');

var DygraphTickers = _interopRequireWildcard(_dygraphTickers);

var _dygraphInteractionModel = require('./dygraph-interaction-model');

var _dygraphInteractionModel2 = _interopRequireDefault(_dygraphInteractionModel);

var _dygraphCanvas = require('./dygraph-canvas');

var _dygraphCanvas2 = _interopRequireDefault(_dygraphCanvas);

var _dygraphUtils = require('./dygraph-utils');

var utils = _interopRequireWildcard(_dygraphUtils);

// Default attribute values.
var DEFAULT_ATTRS = {
  highlightCircleSize: 3,
  highlightSeriesOpts: null,
  highlightSeriesBackgroundAlpha: 0.5,
  highlightSeriesBackgroundColor: 'rgb(255, 255, 255)',

  labelsSeparateLines: false,
  labelsShowZeroValues: true,
  labelsKMB: false,
  labelsKMG2: false,
  showLabelsOnHighlight: true,

  digitsAfterDecimal: 2,
  maxNumberWidth: 6,
  sigFigs: null,

  strokeWidth: 1.0,
  strokeBorderWidth: 0,
  strokeBorderColor: "white",

  axisTickSize: 3,
  axisLabelFontSize: 14,
  rightGap: 5,

  showRoller: false,
  xValueParser: undefined,

  delimiter: ',',

  sigma: 2.0,
  errorBars: false,
  fractions: false,
  wilsonInterval: true, // only relevant if fractions is true
  customBars: false,
  fillGraph: false,
  fillAlpha: 0.15,
  connectSeparatedPoints: false,

  stackedGraph: false,
  stackedGraphNaNFill: 'all',
  hideOverlayOnMouseOut: true,

  legend: 'onmouseover',
  stepPlot: false,
  xRangePad: 0,
  yRangePad: null,
  drawAxesAtZero: false,

  // Sizes of the various chart labels.
  titleHeight: 28,
  xLabelHeight: 18,
  yLabelWidth: 18,

  axisLineColor: "black",
  axisLineWidth: 0.3,
  gridLineWidth: 0.3,
  axisLabelWidth: 50,
  gridLineColor: "rgb(128,128,128)",

  interactionModel: _dygraphInteractionModel2['default'].defaultModel,
  animatedZooms: false, // (for now)

  // Range selector options
  showRangeSelector: false,
  rangeSelectorHeight: 40,
  rangeSelectorPlotStrokeColor: "#808FAB",
  rangeSelectorPlotFillGradientColor: "white",
  rangeSelectorPlotFillColor: "#A7B1C4",
  rangeSelectorBackgroundStrokeColor: "gray",
  rangeSelectorBackgroundLineWidth: 1,
  rangeSelectorPlotLineWidth: 1.5,
  rangeSelectorForegroundStrokeColor: "black",
  rangeSelectorForegroundLineWidth: 1,
  rangeSelectorAlpha: 0.6,
  showInRangeSelector: null,

  // The ordering here ensures that central lines always appear above any
  // fill bars/error bars.
  plotter: [_dygraphCanvas2['default']._fillPlotter, _dygraphCanvas2['default']._errorPlotter, _dygraphCanvas2['default']._linePlotter],

  plugins: [],

  // per-axis options
  axes: {
    x: {
      pixelsPerLabel: 70,
      axisLabelWidth: 60,
      axisLabelFormatter: utils.dateAxisLabelFormatter,
      valueFormatter: utils.dateValueFormatter,
      drawGrid: true,
      drawAxis: true,
      independentTicks: true,
      ticker: DygraphTickers.dateTicker
    },
    y: {
      axisLabelWidth: 50,
      pixelsPerLabel: 30,
      valueFormatter: utils.numberValueFormatter,
      axisLabelFormatter: utils.numberAxisLabelFormatter,
      drawGrid: true,
      drawAxis: true,
      independentTicks: true,
      ticker: DygraphTickers.numericTicks
    },
    y2: {
      axisLabelWidth: 50,
      pixelsPerLabel: 30,
      valueFormatter: utils.numberValueFormatter,
      axisLabelFormatter: utils.numberAxisLabelFormatter,
      drawAxis: true, // only applies when there are two axes of data.
      drawGrid: false,
      independentTicks: false,
      ticker: DygraphTickers.numericTicks
    }
  }
};

exports['default'] = DEFAULT_ATTRS;
module.exports = exports['default'];

},{"./dygraph-canvas":9,"./dygraph-interaction-model":12,"./dygraph-tickers":16,"./dygraph-utils":17}],11:[function(require,module,exports){
/**
 * @license
 * Copyright 2011 Dan Vanderkam (danvdk@gmail.com)
 * MIT-licensed (http://opensource.org/licenses/MIT)
 */

/**
 * @fileoverview A wrapper around the Dygraph class which implements the
 * interface for a GViz (aka Google Visualization API) visualization.
 * It is designed to be a drop-in replacement for Google's AnnotatedTimeline,
 * so the documentation at
 * http://code.google.com/apis/chart/interactive/docs/gallery/annotatedtimeline.html
 * translates over directly.
 *
 * For a full demo, see:
 * - http://dygraphs.com/tests/gviz.html
 * - http://dygraphs.com/tests/annotation-gviz.html
 */

/*global Dygraph:false */
"use strict";

Object.defineProperty(exports, '__esModule', {
  value: true
});

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { 'default': obj }; }

var _dygraph = require('./dygraph');

var _dygraph2 = _interopRequireDefault(_dygraph);

/**
 * A wrapper around Dygraph that implements the gviz API.
 * @param {!HTMLDivElement} container The DOM object the visualization should
 *     live in.
 * @constructor
 */
var GVizChart = function GVizChart(container) {
  this.container = container;
};

/**
 * @param {GVizDataTable} data
 * @param {Object.<*>} options
 */
GVizChart.prototype.draw = function (data, options) {
  // Clear out any existing dygraph.
  // TODO(danvk): would it make more sense to simply redraw using the current
  // date_graph object?
  this.container.innerHTML = '';
  if (typeof this.date_graph != 'undefined') {
    this.date_graph.destroy();
  }

  this.date_graph = new _dygraph2['default'](this.container, data, options);
};

/**
 * Google charts compatible setSelection
 * Only row selection is supported, all points in the row will be highlighted
 * @param {Array.<{row:number}>} selection_array array of the selected cells
 * @public
 */
GVizChart.prototype.setSelection = function (selection_array) {
  var row = false;
  if (selection_array.length) {
    row = selection_array[0].row;
  }
  this.date_graph.setSelection(row);
};

/**
 * Google charts compatible getSelection implementation
 * @return {Array.<{row:number,column:number}>} array of the selected cells
 * @public
 */
GVizChart.prototype.getSelection = function () {
  var selection = [];

  var row = this.date_graph.getSelection();

  if (row < 0) return selection;

  var points = this.date_graph.layout_.points;
  for (var setIdx = 0; setIdx < points.length; ++setIdx) {
    selection.push({ row: row, column: setIdx + 1 });
  }

  return selection;
};

exports['default'] = GVizChart;
module.exports = exports['default'];

},{"./dygraph":18}],12:[function(require,module,exports){
/**
 * @license
 * Copyright 2011 Robert Konigsberg (konigsberg@google.com)
 * MIT-licensed (http://opensource.org/licenses/MIT)
 */

/**
 * @fileoverview The default interaction model for Dygraphs. This is kept out
 * of dygraph.js for better navigability.
 * @author Robert Konigsberg (konigsberg@google.com)
 */

/*global Dygraph:false */
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});

function _interopRequireWildcard(obj) { if (obj && obj.__esModule) { return obj; } else { var newObj = {}; if (obj != null) { for (var key in obj) { if (Object.prototype.hasOwnProperty.call(obj, key)) newObj[key] = obj[key]; } } newObj["default"] = obj; return newObj; } }

var _dygraphUtils = require('./dygraph-utils');

var utils = _interopRequireWildcard(_dygraphUtils);

/**
 * You can drag this many pixels past the edge of the chart and still have it
 * be considered a zoom. This makes it easier to zoom to the exact edge of the
 * chart, a fairly common operation.
 */
var DRAG_EDGE_MARGIN = 100;

/**
 * A collection of functions to facilitate build custom interaction models.
 * @class
 */
var DygraphInteraction = {};

/**
 * Checks whether the beginning & ending of an event were close enough that it
 * should be considered a click. If it should, dispatch appropriate events.
 * Returns true if the event was treated as a click.
 *
 * @param {Event} event
 * @param {Dygraph} g
 * @param {Object} context
 */
DygraphInteraction.maybeTreatMouseOpAsClick = function (event, g, context) {
  context.dragEndX = utils.dragGetX_(event, context);
  context.dragEndY = utils.dragGetY_(event, context);
  var regionWidth = Math.abs(context.dragEndX - context.dragStartX);
  var regionHeight = Math.abs(context.dragEndY - context.dragStartY);

  if (regionWidth < 2 && regionHeight < 2 && g.lastx_ !== undefined && g.lastx_ != -1) {
    DygraphInteraction.treatMouseOpAsClick(g, event, context);
  }

  context.regionWidth = regionWidth;
  context.regionHeight = regionHeight;
};

/**
 * Called in response to an interaction model operation that
 * should start the default panning behavior.
 *
 * It's used in the default callback for "mousedown" operations.
 * Custom interaction model builders can use it to provide the default
 * panning behavior.
 *
 * @param {Event} event the event object which led to the startPan call.
 * @param {Dygraph} g The dygraph on which to act.
 * @param {Object} context The dragging context object (with
 *     dragStartX/dragStartY/etc. properties). This function modifies the
 *     context.
 */
DygraphInteraction.startPan = function (event, g, context) {
  var i, axis;
  context.isPanning = true;
  var xRange = g.xAxisRange();

  if (g.getOptionForAxis("logscale", "x")) {
    context.initialLeftmostDate = utils.log10(xRange[0]);
    context.dateRange = utils.log10(xRange[1]) - utils.log10(xRange[0]);
  } else {
    context.initialLeftmostDate = xRange[0];
    context.dateRange = xRange[1] - xRange[0];
  }
  context.xUnitsPerPixel = context.dateRange / (g.plotter_.area.w - 1);

  if (g.getNumericOption("panEdgeFraction")) {
    var maxXPixelsToDraw = g.width_ * g.getNumericOption("panEdgeFraction");
    var xExtremes = g.xAxisExtremes(); // I REALLY WANT TO CALL THIS xTremes!

    var boundedLeftX = g.toDomXCoord(xExtremes[0]) - maxXPixelsToDraw;
    var boundedRightX = g.toDomXCoord(xExtremes[1]) + maxXPixelsToDraw;

    var boundedLeftDate = g.toDataXCoord(boundedLeftX);
    var boundedRightDate = g.toDataXCoord(boundedRightX);
    context.boundedDates = [boundedLeftDate, boundedRightDate];

    var boundedValues = [];
    var maxYPixelsToDraw = g.height_ * g.getNumericOption("panEdgeFraction");

    for (i = 0; i < g.axes_.length; i++) {
      axis = g.axes_[i];
      var yExtremes = axis.extremeRange;

      var boundedTopY = g.toDomYCoord(yExtremes[0], i) + maxYPixelsToDraw;
      var boundedBottomY = g.toDomYCoord(yExtremes[1], i) - maxYPixelsToDraw;

      var boundedTopValue = g.toDataYCoord(boundedTopY, i);
      var boundedBottomValue = g.toDataYCoord(boundedBottomY, i);

      boundedValues[i] = [boundedTopValue, boundedBottomValue];
    }
    context.boundedValues = boundedValues;
  }

  // Record the range of each y-axis at the start of the drag.
  // If any axis has a valueRange, then we want a 2D pan.
  // We can't store data directly in g.axes_, because it does not belong to us
  // and could change out from under us during a pan (say if there's a data
  // update).
  context.is2DPan = false;
  context.axes = [];
  for (i = 0; i < g.axes_.length; i++) {
    axis = g.axes_[i];
    var axis_data = {};
    var yRange = g.yAxisRange(i);
    // TODO(konigsberg): These values should be in |context|.
    // In log scale, initialTopValue, dragValueRange and unitsPerPixel are log scale.
    var logscale = g.attributes_.getForAxis("logscale", i);
    if (logscale) {
      axis_data.initialTopValue = utils.log10(yRange[1]);
      axis_data.dragValueRange = utils.log10(yRange[1]) - utils.log10(yRange[0]);
    } else {
      axis_data.initialTopValue = yRange[1];
      axis_data.dragValueRange = yRange[1] - yRange[0];
    }
    axis_data.unitsPerPixel = axis_data.dragValueRange / (g.plotter_.area.h - 1);
    context.axes.push(axis_data);

    // While calculating axes, set 2dpan.
    if (axis.valueRange) context.is2DPan = true;
  }
};

/**
 * Called in response to an interaction model operation that
 * responds to an event that pans the view.
 *
 * It's used in the default callback for "mousemove" operations.
 * Custom interaction model builders can use it to provide the default
 * panning behavior.
 *
 * @param {Event} event the event object which led to the movePan call.
 * @param {Dygraph} g The dygraph on which to act.
 * @param {Object} context The dragging context object (with
 *     dragStartX/dragStartY/etc. properties). This function modifies the
 *     context.
 */
DygraphInteraction.movePan = function (event, g, context) {
  context.dragEndX = utils.dragGetX_(event, context);
  context.dragEndY = utils.dragGetY_(event, context);

  var minDate = context.initialLeftmostDate - (context.dragEndX - context.dragStartX) * context.xUnitsPerPixel;
  if (context.boundedDates) {
    minDate = Math.max(minDate, context.boundedDates[0]);
  }
  var maxDate = minDate + context.dateRange;
  if (context.boundedDates) {
    if (maxDate > context.boundedDates[1]) {
      // Adjust minDate, and recompute maxDate.
      minDate = minDate - (maxDate - context.boundedDates[1]);
      maxDate = minDate + context.dateRange;
    }
  }

  if (g.getOptionForAxis("logscale", "x")) {
    g.dateWindow_ = [Math.pow(utils.LOG_SCALE, minDate), Math.pow(utils.LOG_SCALE, maxDate)];
  } else {
    g.dateWindow_ = [minDate, maxDate];
  }

  // y-axis scaling is automatic unless this is a full 2D pan.
  if (context.is2DPan) {

    var pixelsDragged = context.dragEndY - context.dragStartY;

    // Adjust each axis appropriately.
    for (var i = 0; i < g.axes_.length; i++) {
      var axis = g.axes_[i];
      var axis_data = context.axes[i];
      var unitsDragged = pixelsDragged * axis_data.unitsPerPixel;

      var boundedValue = context.boundedValues ? context.boundedValues[i] : null;

      // In log scale, maxValue and minValue are the logs of those values.
      var maxValue = axis_data.initialTopValue + unitsDragged;
      if (boundedValue) {
        maxValue = Math.min(maxValue, boundedValue[1]);
      }
      var minValue = maxValue - axis_data.dragValueRange;
      if (boundedValue) {
        if (minValue < boundedValue[0]) {
          // Adjust maxValue, and recompute minValue.
          maxValue = maxValue - (minValue - boundedValue[0]);
          minValue = maxValue - axis_data.dragValueRange;
        }
      }
      if (g.attributes_.getForAxis("logscale", i)) {
        axis.valueRange = [Math.pow(utils.LOG_SCALE, minValue), Math.pow(utils.LOG_SCALE, maxValue)];
      } else {
        axis.valueRange = [minValue, maxValue];
      }
    }
  }

  g.drawGraph_(false);
};

/**
 * Called in response to an interaction model operation that
 * responds to an event that ends panning.
 *
 * It's used in the default callback for "mouseup" operations.
 * Custom interaction model builders can use it to provide the default
 * panning behavior.
 *
 * @param {Event} event the event object which led to the endPan call.
 * @param {Dygraph} g The dygraph on which to act.
 * @param {Object} context The dragging context object (with
 *     dragStartX/dragStartY/etc. properties). This function modifies the
 *     context.
 */
DygraphInteraction.endPan = DygraphInteraction.maybeTreatMouseOpAsClick;

/**
 * Called in response to an interaction model operation that
 * responds to an event that starts zooming.
 *
 * It's used in the default callback for "mousedown" operations.
 * Custom interaction model builders can use it to provide the default
 * zooming behavior.
 *
 * @param {Event} event the event object which led to the startZoom call.
 * @param {Dygraph} g The dygraph on which to act.
 * @param {Object} context The dragging context object (with
 *     dragStartX/dragStartY/etc. properties). This function modifies the
 *     context.
 */
DygraphInteraction.startZoom = function (event, g, context) {
  context.isZooming = true;
  context.zoomMoved = false;
};

/**
 * Called in response to an interaction model operation that
 * responds to an event that defines zoom boundaries.
 *
 * It's used in the default callback for "mousemove" operations.
 * Custom interaction model builders can use it to provide the default
 * zooming behavior.
 *
 * @param {Event} event the event object which led to the moveZoom call.
 * @param {Dygraph} g The dygraph on which to act.
 * @param {Object} context The dragging context object (with
 *     dragStartX/dragStartY/etc. properties). This function modifies the
 *     context.
 */
DygraphInteraction.moveZoom = function (event, g, context) {
  context.zoomMoved = true;
  context.dragEndX = utils.dragGetX_(event, context);
  context.dragEndY = utils.dragGetY_(event, context);

  var xDelta = Math.abs(context.dragStartX - context.dragEndX);
  var yDelta = Math.abs(context.dragStartY - context.dragEndY);

  // drag direction threshold for y axis is twice as large as x axis
  context.dragDirection = xDelta < yDelta / 2 ? utils.VERTICAL : utils.HORIZONTAL;

  g.drawZoomRect_(context.dragDirection, context.dragStartX, context.dragEndX, context.dragStartY, context.dragEndY, context.prevDragDirection, context.prevEndX, context.prevEndY);

  context.prevEndX = context.dragEndX;
  context.prevEndY = context.dragEndY;
  context.prevDragDirection = context.dragDirection;
};

/**
 * TODO(danvk): move this logic into dygraph.js
 * @param {Dygraph} g
 * @param {Event} event
 * @param {Object} context
 */
DygraphInteraction.treatMouseOpAsClick = function (g, event, context) {
  var clickCallback = g.getFunctionOption('clickCallback');
  var pointClickCallback = g.getFunctionOption('pointClickCallback');

  var selectedPoint = null;

  // Find out if the click occurs on a point.
  var closestIdx = -1;
  var closestDistance = Number.MAX_VALUE;

  // check if the click was on a particular point.
  for (var i = 0; i < g.selPoints_.length; i++) {
    var p = g.selPoints_[i];
    var distance = Math.pow(p.canvasx - context.dragEndX, 2) + Math.pow(p.canvasy - context.dragEndY, 2);
    if (!isNaN(distance) && (closestIdx == -1 || distance < closestDistance)) {
      closestDistance = distance;
      closestIdx = i;
    }
  }

  // Allow any click within two pixels of the dot.
  var radius = g.getNumericOption('highlightCircleSize') + 2;
  if (closestDistance <= radius * radius) {
    selectedPoint = g.selPoints_[closestIdx];
  }

  if (selectedPoint) {
    var e = {
      cancelable: true,
      point: selectedPoint,
      canvasx: context.dragEndX,
      canvasy: context.dragEndY
    };
    var defaultPrevented = g.cascadeEvents_('pointClick', e);
    if (defaultPrevented) {
      // Note: this also prevents click / clickCallback from firing.
      return;
    }
    if (pointClickCallback) {
      pointClickCallback.call(g, event, selectedPoint);
    }
  }

  var e = {
    cancelable: true,
    xval: g.lastx_, // closest point by x value
    pts: g.selPoints_,
    canvasx: context.dragEndX,
    canvasy: context.dragEndY
  };
  if (!g.cascadeEvents_('click', e)) {
    if (clickCallback) {
      // TODO(danvk): pass along more info about the points, e.g. 'x'
      clickCallback.call(g, event, g.lastx_, g.selPoints_);
    }
  }
};

/**
 * Called in response to an interaction model operation that
 * responds to an event that performs a zoom based on previously defined
 * bounds..
 *
 * It's used in the default callback for "mouseup" operations.
 * Custom interaction model builders can use it to provide the default
 * zooming behavior.
 *
 * @param {Event} event the event object which led to the endZoom call.
 * @param {Dygraph} g The dygraph on which to end the zoom.
 * @param {Object} context The dragging context object (with
 *     dragStartX/dragStartY/etc. properties). This function modifies the
 *     context.
 */
DygraphInteraction.endZoom = function (event, g, context) {
  g.clearZoomRect_();
  context.isZooming = false;
  DygraphInteraction.maybeTreatMouseOpAsClick(event, g, context);

  // The zoom rectangle is visibly clipped to the plot area, so its behavior
  // should be as well.
  // See http://code.google.com/p/dygraphs/issues/detail?id=280
  var plotArea = g.getArea();
  if (context.regionWidth >= 10 && context.dragDirection == utils.HORIZONTAL) {
    var left = Math.min(context.dragStartX, context.dragEndX),
        right = Math.max(context.dragStartX, context.dragEndX);
    left = Math.max(left, plotArea.x);
    right = Math.min(right, plotArea.x + plotArea.w);
    if (left < right) {
      g.doZoomX_(left, right);
    }
    context.cancelNextDblclick = true;
  } else if (context.regionHeight >= 10 && context.dragDirection == utils.VERTICAL) {
    var top = Math.min(context.dragStartY, context.dragEndY),
        bottom = Math.max(context.dragStartY, context.dragEndY);
    top = Math.max(top, plotArea.y);
    bottom = Math.min(bottom, plotArea.y + plotArea.h);
    if (top < bottom) {
      g.doZoomY_(top, bottom);
    }
    context.cancelNextDblclick = true;
  }
  context.dragStartX = null;
  context.dragStartY = null;
};

/**
 * @private
 */
DygraphInteraction.startTouch = function (event, g, context) {
  event.preventDefault(); // touch browsers are all nice.
  if (event.touches.length > 1) {
    // If the user ever puts two fingers down, it's not a double tap.
    context.startTimeForDoubleTapMs = null;
  }

  var touches = [];
  for (var i = 0; i < event.touches.length; i++) {
    var t = event.touches[i];
    // we dispense with 'dragGetX_' because all touchBrowsers support pageX
    touches.push({
      pageX: t.pageX,
      pageY: t.pageY,
      dataX: g.toDataXCoord(t.pageX),
      dataY: g.toDataYCoord(t.pageY)
      // identifier: t.identifier
    });
  }
  context.initialTouches = touches;

  if (touches.length == 1) {
    // This is just a swipe.
    context.initialPinchCenter = touches[0];
    context.touchDirections = { x: true, y: true };
  } else if (touches.length >= 2) {
    // It's become a pinch!
    // In case there are 3+ touches, we ignore all but the "first" two.

    // only screen coordinates can be averaged (data coords could be log scale).
    context.initialPinchCenter = {
      pageX: 0.5 * (touches[0].pageX + touches[1].pageX),
      pageY: 0.5 * (touches[0].pageY + touches[1].pageY),

      // TODO(danvk): remove
      dataX: 0.5 * (touches[0].dataX + touches[1].dataX),
      dataY: 0.5 * (touches[0].dataY + touches[1].dataY)
    };

    // Make pinches in a 45-degree swath around either axis 1-dimensional zooms.
    var initialAngle = 180 / Math.PI * Math.atan2(context.initialPinchCenter.pageY - touches[0].pageY, touches[0].pageX - context.initialPinchCenter.pageX);

    // use symmetry to get it into the first quadrant.
    initialAngle = Math.abs(initialAngle);
    if (initialAngle > 90) initialAngle = 90 - initialAngle;

    context.touchDirections = {
      x: initialAngle < 90 - 45 / 2,
      y: initialAngle > 45 / 2
    };
  }

  // save the full x & y ranges.
  context.initialRange = {
    x: g.xAxisRange(),
    y: g.yAxisRange()
  };
};

/**
 * @private
 */
DygraphInteraction.moveTouch = function (event, g, context) {
  // If the tap moves, then it's definitely not part of a double-tap.
  context.startTimeForDoubleTapMs = null;

  var i,
      touches = [];
  for (i = 0; i < event.touches.length; i++) {
    var t = event.touches[i];
    touches.push({
      pageX: t.pageX,
      pageY: t.pageY
    });
  }
  var initialTouches = context.initialTouches;

  var c_now;

  // old and new centers.
  var c_init = context.initialPinchCenter;
  if (touches.length == 1) {
    c_now = touches[0];
  } else {
    c_now = {
      pageX: 0.5 * (touches[0].pageX + touches[1].pageX),
      pageY: 0.5 * (touches[0].pageY + touches[1].pageY)
    };
  }

  // this is the "swipe" component
  // we toss it out for now, but could use it in the future.
  var swipe = {
    pageX: c_now.pageX - c_init.pageX,
    pageY: c_now.pageY - c_init.pageY
  };
  var dataWidth = context.initialRange.x[1] - context.initialRange.x[0];
  var dataHeight = context.initialRange.y[0] - context.initialRange.y[1];
  swipe.dataX = swipe.pageX / g.plotter_.area.w * dataWidth;
  swipe.dataY = swipe.pageY / g.plotter_.area.h * dataHeight;
  var xScale, yScale;

  // The residual bits are usually split into scale & rotate bits, but we split
  // them into x-scale and y-scale bits.
  if (touches.length == 1) {
    xScale = 1.0;
    yScale = 1.0;
  } else if (touches.length >= 2) {
    var initHalfWidth = initialTouches[1].pageX - c_init.pageX;
    xScale = (touches[1].pageX - c_now.pageX) / initHalfWidth;

    var initHalfHeight = initialTouches[1].pageY - c_init.pageY;
    yScale = (touches[1].pageY - c_now.pageY) / initHalfHeight;
  }

  // Clip scaling to [1/8, 8] to prevent too much blowup.
  xScale = Math.min(8, Math.max(0.125, xScale));
  yScale = Math.min(8, Math.max(0.125, yScale));

  var didZoom = false;
  if (context.touchDirections.x) {
    g.dateWindow_ = [c_init.dataX - swipe.dataX + (context.initialRange.x[0] - c_init.dataX) / xScale, c_init.dataX - swipe.dataX + (context.initialRange.x[1] - c_init.dataX) / xScale];
    didZoom = true;
  }

  if (context.touchDirections.y) {
    for (i = 0; i < 1 /*g.axes_.length*/; i++) {
      var axis = g.axes_[i];
      var logscale = g.attributes_.getForAxis("logscale", i);
      if (logscale) {
        // TODO(danvk): implement
      } else {
          axis.valueRange = [c_init.dataY - swipe.dataY + (context.initialRange.y[0] - c_init.dataY) / yScale, c_init.dataY - swipe.dataY + (context.initialRange.y[1] - c_init.dataY) / yScale];
          didZoom = true;
        }
    }
  }

  g.drawGraph_(false);

  // We only call zoomCallback on zooms, not pans, to mirror desktop behavior.
  if (didZoom && touches.length > 1 && g.getFunctionOption('zoomCallback')) {
    var viewWindow = g.xAxisRange();
    g.getFunctionOption("zoomCallback").call(g, viewWindow[0], viewWindow[1], g.yAxisRanges());
  }
};

/**
 * @private
 */
DygraphInteraction.endTouch = function (event, g, context) {
  if (event.touches.length !== 0) {
    // this is effectively a "reset"
    DygraphInteraction.startTouch(event, g, context);
  } else if (event.changedTouches.length == 1) {
    // Could be part of a "double tap"
    // The heuristic here is that it's a double-tap if the two touchend events
    // occur within 500ms and within a 50x50 pixel box.
    var now = new Date().getTime();
    var t = event.changedTouches[0];
    if (context.startTimeForDoubleTapMs && now - context.startTimeForDoubleTapMs < 500 && context.doubleTapX && Math.abs(context.doubleTapX - t.screenX) < 50 && context.doubleTapY && Math.abs(context.doubleTapY - t.screenY) < 50) {
      g.resetZoom();
    } else {
      context.startTimeForDoubleTapMs = now;
      context.doubleTapX = t.screenX;
      context.doubleTapY = t.screenY;
    }
  }
};

// Determine the distance from x to [left, right].
var distanceFromInterval = function distanceFromInterval(x, left, right) {
  if (x < left) {
    return left - x;
  } else if (x > right) {
    return x - right;
  } else {
    return 0;
  }
};

/**
 * Returns the number of pixels by which the event happens from the nearest
 * edge of the chart. For events in the interior of the chart, this returns zero.
 */
var distanceFromChart = function distanceFromChart(event, g) {
  var chartPos = utils.findPos(g.canvas_);
  var box = {
    left: chartPos.x,
    right: chartPos.x + g.canvas_.offsetWidth,
    top: chartPos.y,
    bottom: chartPos.y + g.canvas_.offsetHeight
  };

  var pt = {
    x: utils.pageX(event),
    y: utils.pageY(event)
  };

  var dx = distanceFromInterval(pt.x, box.left, box.right),
      dy = distanceFromInterval(pt.y, box.top, box.bottom);
  return Math.max(dx, dy);
};

/**
 * Default interation model for dygraphs. You can refer to specific elements of
 * this when constructing your own interaction model, e.g.:
 * g.updateOptions( {
 *   interactionModel: {
 *     mousedown: DygraphInteraction.defaultInteractionModel.mousedown
 *   }
 * } );
 */
DygraphInteraction.defaultModel = {
  // Track the beginning of drag events
  mousedown: function mousedown(event, g, context) {
    // Right-click should not initiate a zoom.
    if (event.button && event.button == 2) return;

    context.initializeMouseDown(event, g, context);

    if (event.altKey || event.shiftKey) {
      DygraphInteraction.startPan(event, g, context);
    } else {
      DygraphInteraction.startZoom(event, g, context);
    }

    // Note: we register mousemove/mouseup on document to allow some leeway for
    // events to move outside of the chart. Interaction model events get
    // registered on the canvas, which is too small to allow this.
    var mousemove = function mousemove(event) {
      if (context.isZooming) {
        // When the mouse moves >200px from the chart edge, cancel the zoom.
        var d = distanceFromChart(event, g);
        if (d < DRAG_EDGE_MARGIN) {
          DygraphInteraction.moveZoom(event, g, context);
        } else {
          if (context.dragEndX !== null) {
            context.dragEndX = null;
            context.dragEndY = null;
            g.clearZoomRect_();
          }
        }
      } else if (context.isPanning) {
        DygraphInteraction.movePan(event, g, context);
      }
    };
    var mouseup = function mouseup(event) {
      if (context.isZooming) {
        if (context.dragEndX !== null) {
          DygraphInteraction.endZoom(event, g, context);
        } else {
          DygraphInteraction.maybeTreatMouseOpAsClick(event, g, context);
        }
      } else if (context.isPanning) {
        DygraphInteraction.endPan(event, g, context);
      }

      utils.removeEvent(document, 'mousemove', mousemove);
      utils.removeEvent(document, 'mouseup', mouseup);
      context.destroy();
    };

    g.addAndTrackEvent(document, 'mousemove', mousemove);
    g.addAndTrackEvent(document, 'mouseup', mouseup);
  },
  willDestroyContextMyself: true,

  touchstart: function touchstart(event, g, context) {
    DygraphInteraction.startTouch(event, g, context);
  },
  touchmove: function touchmove(event, g, context) {
    DygraphInteraction.moveTouch(event, g, context);
  },
  touchend: function touchend(event, g, context) {
    DygraphInteraction.endTouch(event, g, context);
  },

  // Disable zooming out if panning.
  dblclick: function dblclick(event, g, context) {
    if (context.cancelNextDblclick) {
      context.cancelNextDblclick = false;
      return;
    }

    // Give plugins a chance to grab this event.
    var e = {
      canvasx: context.dragEndX,
      canvasy: context.dragEndY,
      cancelable: true
    };
    if (g.cascadeEvents_('dblclick', e)) {
      return;
    }

    if (event.altKey || event.shiftKey) {
      return;
    }
    g.resetZoom();
  }
};

/*
Dygraph.DEFAULT_ATTRS.interactionModel = DygraphInteraction.defaultModel;

// old ways of accessing these methods/properties
Dygraph.defaultInteractionModel = DygraphInteraction.defaultModel;
Dygraph.endZoom = DygraphInteraction.endZoom;
Dygraph.moveZoom = DygraphInteraction.moveZoom;
Dygraph.startZoom = DygraphInteraction.startZoom;
Dygraph.endPan = DygraphInteraction.endPan;
Dygraph.movePan = DygraphInteraction.movePan;
Dygraph.startPan = DygraphInteraction.startPan;
*/

DygraphInteraction.nonInteractiveModel_ = {
  mousedown: function mousedown(event, g, context) {
    context.initializeMouseDown(event, g, context);
  },
  mouseup: DygraphInteraction.maybeTreatMouseOpAsClick
};

// Default interaction model when using the range selector.
DygraphInteraction.dragIsPanInteractionModel = {
  mousedown: function mousedown(event, g, context) {
    context.initializeMouseDown(event, g, context);
    DygraphInteraction.startPan(event, g, context);
  },
  mousemove: function mousemove(event, g, context) {
    if (context.isPanning) {
      DygraphInteraction.movePan(event, g, context);
    }
  },
  mouseup: function mouseup(event, g, context) {
    if (context.isPanning) {
      DygraphInteraction.endPan(event, g, context);
    }
  }
};

exports["default"] = DygraphInteraction;
module.exports = exports["default"];

},{"./dygraph-utils":17}],13:[function(require,module,exports){
/**
 * @license
 * Copyright 2011 Dan Vanderkam (danvdk@gmail.com)
 * MIT-licensed (http://opensource.org/licenses/MIT)
 */

/**
 * @fileoverview Based on PlotKitLayout, but modified to meet the needs of
 * dygraphs.
 */

/*global Dygraph:false */
"use strict";

Object.defineProperty(exports, '__esModule', {
  value: true
});

function _interopRequireWildcard(obj) { if (obj && obj.__esModule) { return obj; } else { var newObj = {}; if (obj != null) { for (var key in obj) { if (Object.prototype.hasOwnProperty.call(obj, key)) newObj[key] = obj[key]; } } newObj['default'] = obj; return newObj; } }

var _dygraphUtils = require('./dygraph-utils');

var utils = _interopRequireWildcard(_dygraphUtils);

/**
 * Creates a new DygraphLayout object.
 *
 * This class contains all the data to be charted.
 * It uses data coordinates, but also records the chart range (in data
 * coordinates) and hence is able to calculate percentage positions ('In this
 * view, Point A lies 25% down the x-axis.')
 *
 * Two things that it does not do are:
 * 1. Record pixel coordinates for anything.
 * 2. (oddly) determine anything about the layout of chart elements.
 *
 * The naming is a vestige of Dygraph's original PlotKit roots.
 *
 * @constructor
 */
var DygraphLayout = function DygraphLayout(dygraph) {
  this.dygraph_ = dygraph;
  /**
   * Array of points for each series.
   *
   * [series index][row index in series] = |Point| structure,
   * where series index refers to visible series only, and the
   * point index is for the reduced set of points for the current
   * zoom region (including one point just outside the window).
   * All points in the same row index share the same X value.
   *
   * @type {Array.<Array.<Dygraph.PointType>>}
   */
  this.points = [];
  this.setNames = [];
  this.annotations = [];
  this.yAxes_ = null;

  // TODO(danvk): it's odd that xTicks_ and yTicks_ are inputs, but xticks and
  // yticks are outputs. Clean this up.
  this.xTicks_ = null;
  this.yTicks_ = null;
};

/**
 * Add points for a single series.
 *
 * @param {string} setname Name of the series.
 * @param {Array.<Dygraph.PointType>} set_xy Points for the series.
 */
DygraphLayout.prototype.addDataset = function (setname, set_xy) {
  this.points.push(set_xy);
  this.setNames.push(setname);
};

/**
 * Returns the box which the chart should be drawn in. This is the canvas's
 * box, less space needed for the axis and chart labels.
 *
 * @return {{x: number, y: number, w: number, h: number}}
 */
DygraphLayout.prototype.getPlotArea = function () {
  return this.area_;
};

// Compute the box which the chart should be drawn in. This is the canvas's
// box, less space needed for axis, chart labels, and other plug-ins.
// NOTE: This should only be called by Dygraph.predraw_().
DygraphLayout.prototype.computePlotArea = function () {
  var area = {
    // TODO(danvk): per-axis setting.
    x: 0,
    y: 0
  };

  area.w = this.dygraph_.width_ - area.x - this.dygraph_.getOption('rightGap');
  area.h = this.dygraph_.height_;

  // Let plugins reserve space.
  var e = {
    chart_div: this.dygraph_.graphDiv,
    reserveSpaceLeft: function reserveSpaceLeft(px) {
      var r = {
        x: area.x,
        y: area.y,
        w: px,
        h: area.h
      };
      area.x += px;
      area.w -= px;
      return r;
    },
    reserveSpaceRight: function reserveSpaceRight(px) {
      var r = {
        x: area.x + area.w - px,
        y: area.y,
        w: px,
        h: area.h
      };
      area.w -= px;
      return r;
    },
    reserveSpaceTop: function reserveSpaceTop(px) {
      var r = {
        x: area.x,
        y: area.y,
        w: area.w,
        h: px
      };
      area.y += px;
      area.h -= px;
      return r;
    },
    reserveSpaceBottom: function reserveSpaceBottom(px) {
      var r = {
        x: area.x,
        y: area.y + area.h - px,
        w: area.w,
        h: px
      };
      area.h -= px;
      return r;
    },
    chartRect: function chartRect() {
      return { x: area.x, y: area.y, w: area.w, h: area.h };
    }
  };
  this.dygraph_.cascadeEvents_('layout', e);

  this.area_ = area;
};

DygraphLayout.prototype.setAnnotations = function (ann) {
  // The Dygraph object's annotations aren't parsed. We parse them here and
  // save a copy. If there is no parser, then the user must be using raw format.
  this.annotations = [];
  var parse = this.dygraph_.getOption('xValueParser') || function (x) {
    return x;
  };
  for (var i = 0; i < ann.length; i++) {
    var a = {};
    if (!ann[i].xval && ann[i].x === undefined) {
      console.error("Annotations must have an 'x' property");
      return;
    }
    if (ann[i].icon && !(ann[i].hasOwnProperty('width') && ann[i].hasOwnProperty('height'))) {
      console.error("Must set width and height when setting " + "annotation.icon property");
      return;
    }
    utils.update(a, ann[i]);
    if (!a.xval) a.xval = parse(a.x);
    this.annotations.push(a);
  }
};

DygraphLayout.prototype.setXTicks = function (xTicks) {
  this.xTicks_ = xTicks;
};

// TODO(danvk): add this to the Dygraph object's API or move it into Layout.
DygraphLayout.prototype.setYAxes = function (yAxes) {
  this.yAxes_ = yAxes;
};

DygraphLayout.prototype.evaluate = function () {
  this._xAxis = {};
  this._evaluateLimits();
  this._evaluateLineCharts();
  this._evaluateLineTicks();
  this._evaluateAnnotations();
};

DygraphLayout.prototype._evaluateLimits = function () {
  var xlimits = this.dygraph_.xAxisRange();
  this._xAxis.minval = xlimits[0];
  this._xAxis.maxval = xlimits[1];
  var xrange = xlimits[1] - xlimits[0];
  this._xAxis.scale = xrange !== 0 ? 1 / xrange : 1.0;

  if (this.dygraph_.getOptionForAxis("logscale", 'x')) {
    this._xAxis.xlogrange = utils.log10(this._xAxis.maxval) - utils.log10(this._xAxis.minval);
    this._xAxis.xlogscale = this._xAxis.xlogrange !== 0 ? 1.0 / this._xAxis.xlogrange : 1.0;
  }
  for (var i = 0; i < this.yAxes_.length; i++) {
    var axis = this.yAxes_[i];
    axis.minyval = axis.computedValueRange[0];
    axis.maxyval = axis.computedValueRange[1];
    axis.yrange = axis.maxyval - axis.minyval;
    axis.yscale = axis.yrange !== 0 ? 1.0 / axis.yrange : 1.0;

    if (this.dygraph_.getOption("logscale")) {
      axis.ylogrange = utils.log10(axis.maxyval) - utils.log10(axis.minyval);
      axis.ylogscale = axis.ylogrange !== 0 ? 1.0 / axis.ylogrange : 1.0;
      if (!isFinite(axis.ylogrange) || isNaN(axis.ylogrange)) {
        console.error('axis ' + i + ' of graph at ' + axis.g + ' can\\'t be displayed in log scale for range [' + axis.minyval + ' - ' + axis.maxyval + ']');
      }
    }
  }
};

DygraphLayout.calcXNormal_ = function (value, xAxis, logscale) {
  if (logscale) {
    return (utils.log10(value) - utils.log10(xAxis.minval)) * xAxis.xlogscale;
  } else {
    return (value - xAxis.minval) * xAxis.scale;
  }
};

/**
 * @param {DygraphAxisType} axis
 * @param {number} value
 * @param {boolean} logscale
 * @return {number}
 */
DygraphLayout.calcYNormal_ = function (axis, value, logscale) {
  if (logscale) {
    var x = 1.0 - (utils.log10(value) - utils.log10(axis.minyval)) * axis.ylogscale;
    return isFinite(x) ? x : NaN; // shim for v8 issue; see pull request 276
  } else {
      return 1.0 - (value - axis.minyval) * axis.yscale;
    }
};

DygraphLayout.prototype._evaluateLineCharts = function () {
  var isStacked = this.dygraph_.getOption("stackedGraph");
  var isLogscaleForX = this.dygraph_.getOptionForAxis("logscale", 'x');

  for (var setIdx = 0; setIdx < this.points.length; setIdx++) {
    var points = this.points[setIdx];
    var setName = this.setNames[setIdx];
    var connectSeparated = this.dygraph_.getOption('connectSeparatedPoints', setName);
    var axis = this.dygraph_.axisPropertiesForSeries(setName);
    // TODO (konigsberg): use optionsForAxis instead.
    var logscale = this.dygraph_.attributes_.getForSeries("logscale", setName);

    for (var j = 0; j < points.length; j++) {
      var point = points[j];

      // Range from 0-1 where 0 represents left and 1 represents right.
      point.x = DygraphLayout.calcXNormal_(point.xval, this._xAxis, isLogscaleForX);
      // Range from 0-1 where 0 represents top and 1 represents bottom
      var yval = point.yval;
      if (isStacked) {
        point.y_stacked = DygraphLayout.calcYNormal_(axis, point.yval_stacked, logscale);
        if (yval !== null && !isNaN(yval)) {
          yval = point.yval_stacked;
        }
      }
      if (yval === null) {
        yval = NaN;
        if (!connectSeparated) {
          point.yval = NaN;
        }
      }
      point.y = DygraphLayout.calcYNormal_(axis, yval, logscale);
    }

    this.dygraph_.dataHandler_.onLineEvaluated(points, axis, logscale);
  }
};

DygraphLayout.prototype._evaluateLineTicks = function () {
  var i, tick, label, pos, v, has_tick;
  this.xticks = [];
  for (i = 0; i < this.xTicks_.length; i++) {
    tick = this.xTicks_[i];
    label = tick.label;
    has_tick = !('label_v' in tick);
    v = has_tick ? tick.v : tick.label_v;
    pos = this.dygraph_.toPercentXCoord(v);
    if (pos >= 0.0 && pos < 1.0) {
      this.xticks.push({ pos: pos, label: label, has_tick: has_tick });
    }
  }

  this.yticks = [];
  for (i = 0; i < this.yAxes_.length; i++) {
    var axis = this.yAxes_[i];
    for (var j = 0; j < axis.ticks.length; j++) {
      tick = axis.ticks[j];
      label = tick.label;
      has_tick = !('label_v' in tick);
      v = has_tick ? tick.v : tick.label_v;
      pos = this.dygraph_.toPercentYCoord(v, i);
      if (pos > 0.0 && pos <= 1.0) {
        this.yticks.push({ axis: i, pos: pos, label: label, has_tick: has_tick });
      }
    }
  }
};

DygraphLayout.prototype._evaluateAnnotations = function () {
  // Add the annotations to the point to which they belong.
  // Make a map from (setName, xval) to annotation for quick lookups.
  var i;
  var annotations = {};
  for (i = 0; i < this.annotations.length; i++) {
    var a = this.annotations[i];
    annotations[a.xval + "," + a.series] = a;
  }

  this.annotated_points = [];

  // Exit the function early if there are no annotations.
  if (!this.annotations || !this.annotations.length) {
    return;
  }

  // TODO(antrob): loop through annotations not points.
  for (var setIdx = 0; setIdx < this.points.length; setIdx++) {
    var points = this.points[setIdx];
    for (i = 0; i < points.length; i++) {
      var p = points[i];
      var k = p.xval + "," + p.name;
      if (k in annotations) {
        p.annotation = annotations[k];
        this.annotated_points.push(p);
      }
    }
  }
};

/**
 * Convenience function to remove all the data sets from a graph
 */
DygraphLayout.prototype.removeAllDatasets = function () {
  delete this.points;
  delete this.setNames;
  delete this.setPointsLengths;
  delete this.setPointsOffsets;
  this.points = [];
  this.setNames = [];
  this.setPointsLengths = [];
  this.setPointsOffsets = [];
};

exports['default'] = DygraphLayout;
module.exports = exports['default'];

},{"./dygraph-utils":17}],14:[function(require,module,exports){
(function (process){
/**
 * @license
 * Copyright 2011 Dan Vanderkam (danvdk@gmail.com)
 * MIT-licensed (http://opensource.org/licenses/MIT)
 */

"use strict";

Object.defineProperty(exports, '__esModule', {
  value: true
});
var OPTIONS_REFERENCE = null;

// For "production" code, this gets removed by uglifyjs.
if (typeof process !== 'undefined') {
  if ("development" != 'production') {

    // NOTE: in addition to parsing as JS, this snippet is expected to be valid
    // JSON. This assumption cannot be checked in JS, but it will be checked when
    // documentation is generated by the generate-documentation.py script. For the
    // most part, this just means that you should always use double quotes.
    OPTIONS_REFERENCE = // <JSON>
    {
      "xValueParser": {
        "default": "parseFloat() or Date.parse()*",
        "labels": ["CSV parsing"],
        "type": "function(str) -> number",
        "description": "A function which parses x-values (i.e. the dependent series). Must return a number, even when the values are dates. In this case, millis since epoch are used. This is used primarily for parsing CSV data. *=Dygraphs is slightly more accepting in the dates which it will parse. See code for details."
      },
      "stackedGraph": {
        "default": "false",
        "labels": ["Data Line display"],
        "type": "boolean",
        "description": "If set, stack series on top of one another rather than drawing them independently. The first series specified in the input data will wind up on top of the chart and the last will be on bottom. NaN values are drawn as white areas without a line on top, see stackedGraphNaNFill for details."
      },
      "stackedGraphNaNFill": {
        "default": "all",
        "labels": ["Data Line display"],
        "type": "string",
        "description": "Controls handling of NaN values inside a stacked graph. NaN values are interpolated/extended for stacking purposes, but the actual point value remains NaN in the legend display. Valid option values are \\"all\\" (interpolate internally, repeat leftmost and rightmost value as needed), \\"inside\\" (interpolate internally only, use zero outside leftmost and rightmost value), and \\"none\\" (treat NaN as zero everywhere)."
      },
      "pointSize": {
        "default": "1",
        "labels": ["Data Line display"],
        "type": "integer",
        "description": "The size of the dot to draw on each point in pixels (see drawPoints). A dot is always drawn when a point is \\"isolated\\", i.e. there is a missing point on either side of it. This also controls the size of those dots."
      },
      "drawPoints": {
        "default": "false",
        "labels": ["Data Line display"],
        "type": "boolean",
        "description": "Draw a small dot at each point, in addition to a line going through the point. This makes the individual data points easier to see, but can increase visual clutter in the chart. The small dot can be replaced with a custom rendering by supplying a <a href='#drawPointCallback'>drawPointCallback</a>."
      },
      "drawGapEdgePoints": {
        "default": "false",
        "labels": ["Data Line display"],
        "type": "boolean",
        "description": "Draw points at the edges of gaps in the data. This improves visibility of small data segments or other data irregularities."
      },
      "drawPointCallback": {
        "default": "null",
        "labels": ["Data Line display"],
        "type": "function(g, seriesName, canvasContext, cx, cy, color, pointSize)",
        "parameters": [["g", "the reference graph"], ["seriesName", "the name of the series"], ["canvasContext", "the canvas to draw on"], ["cx", "center x coordinate"], ["cy", "center y coordinate"], ["color", "series color"], ["pointSize", "the radius of the image."], ["idx", "the row-index of the point in the data."]],
        "description": "Draw a custom item when drawPoints is enabled. Default is a small dot matching the series color. This method should constrain drawing to within pointSize pixels from (cx, cy).  Also see <a href='#drawHighlightPointCallback'>drawHighlightPointCallback</a>"
      },
      "height": {
        "default": "320",
        "labels": ["Overall display"],
        "type": "integer",
        "description": "Height, in pixels, of the chart. If the container div has been explicitly sized, this will be ignored."
      },
      "zoomCallback": {
        "default": "null",
        "labels": ["Callbacks"],
        "type": "function(minDate, maxDate, yRanges)",
        "parameters": [["minDate", "milliseconds since epoch"], ["maxDate", "milliseconds since epoch."], ["yRanges", "is an array of [bottom, top] pairs, one for each y-axis."]],
        "description": "A function to call when the zoom window is changed (either by zooming in or out). When animatedZooms is set, zoomCallback is called once at the end of the transition (it will not be called for intermediate frames)."
      },
      "pointClickCallback": {
        "snippet": "function(e, point){<br>&nbsp;&nbsp;alert(point);<br>}",
        "default": "null",
        "labels": ["Callbacks", "Interactive Elements"],
        "type": "function(e, point)",
        "parameters": [["e", "the event object for the click"], ["point", "the point that was clicked See <a href='#point_properties'>Point properties</a> for details"]],
        "description": "A function to call when a data point is clicked. and the point that was clicked."
      },
      "color": {
        "default": "(see description)",
        "labels": ["Data Series Colors"],
        "type": "string",
        "example": "red",
        "description": "A per-series color definition. Used in conjunction with, and overrides, the colors option."
      },
      "colors": {
        "default": "(see description)",
        "labels": ["Data Series Colors"],
        "type": "array<string>",
        "example": "['red', '#00FF00']",
        "description": "List of colors for the data series. These can be of the form \\"#AABBCC\\" or \\"rgb(255,100,200)\\" or \\"yellow\\", etc. If not specified, equally-spaced points around a color wheel are used. Overridden by the 'color' option."
      },
      "connectSeparatedPoints": {
        "default": "false",
        "labels": ["Data Line display"],
        "type": "boolean",
        "description": "Usually, when Dygraphs encounters a missing value in a data series, it interprets this as a gap and draws it as such. If, instead, the missing values represents an x-value for which only a different series has data, then you'll want to connect the dots by setting this to true. To explicitly include a gap with this option set, use a value of NaN."
      },
      "highlightCallback": {
        "default": "null",
        "labels": ["Callbacks"],
        "type": "function(event, x, points, row, seriesName)",
        "description": "When set, this callback gets called every time a new point is highlighted.",
        "parameters": [["event", "the JavaScript mousemove event"], ["x", "the x-coordinate of the highlighted points"], ["points", "an array of highlighted points: <code>[ {name: 'series', yval: y-value}, &hellip; ]</code>"], ["row", "integer index of the highlighted row in the data table, starting from 0"], ["seriesName", "name of the highlighted series, only present if highlightSeriesOpts is set."]]
      },
      "drawHighlightPointCallback": {
        "default": "null",
        "labels": ["Data Line display"],
        "type": "function(g, seriesName, canvasContext, cx, cy, color, pointSize)",
        "parameters": [["g", "the reference graph"], ["seriesName", "the name of the series"], ["canvasContext", "the canvas to draw on"], ["cx", "center x coordinate"], ["cy", "center y coordinate"], ["color", "series color"], ["pointSize", "the radius of the image."], ["idx", "the row-index of the point in the data."]],
        "description": "Draw a custom item when a point is highlighted.  Default is a small dot matching the series color. This method should constrain drawing to within pointSize pixels from (cx, cy) Also see <a href='#drawPointCallback'>drawPointCallback</a>"
      },
      "highlightSeriesOpts": {
        "default": "null",
        "labels": ["Interactive Elements"],
        "type": "Object",
        "description": "When set, the options from this object are applied to the timeseries closest to the mouse pointer for interactive highlighting. See also 'highlightCallback'. Example: highlightSeriesOpts: { strokeWidth: 3 }."
      },
      "highlightSeriesBackgroundAlpha": {
        "default": "0.5",
        "labels": ["Interactive Elements"],
        "type": "float",
        "description": "Fade the background while highlighting series. 1=fully visible background (disable fading), 0=hiddden background (show highlighted series only)."
      },
      "highlightSeriesBackgroundColor": {
        "default": "rgb(255, 255, 255)",
        "labels": ["Interactive Elements"],
        "type": "string",
        "description": "Sets the background color used to fade out the series in conjunction with 'highlightSeriesBackgroundAlpha'."
      },
      "includeZero": {
        "default": "false",
        "labels": ["Axis display"],
        "type": "boolean",
        "description": "Usually, dygraphs will use the range of the data plus some padding to set the range of the y-axis. If this option is set, the y-axis will always include zero, typically as the lowest value. This can be used to avoid exaggerating the variance in the data"
      },
      "rollPeriod": {
        "default": "1",
        "labels": ["Error Bars", "Rolling Averages"],
        "type": "integer &gt;= 1",
        "description": "Number of days over which to average data. Discussed extensively above."
      },
      "unhighlightCallback": {
        "default": "null",
        "labels": ["Callbacks"],
        "type": "function(event)",
        "parameters": [["event", "the mouse event"]],
        "description": "When set, this callback gets called every time the user stops highlighting any point by mousing out of the graph."
      },
      "axisTickSize": {
        "default": "3.0",
        "labels": ["Axis display"],
        "type": "number",
        "description": "The size of the line to display next to each tick mark on x- or y-axes."
      },
      "labelsSeparateLines": {
        "default": "false",
        "labels": ["Legend"],
        "type": "boolean",
        "description": "Put <code>&lt;br/&gt;</code> between lines in the label string. Often used in conjunction with <strong>labelsDiv</strong>."
      },
      "valueFormatter": {
        "default": "Depends on the type of your data.",
        "labels": ["Legend", "Value display/formatting"],
        "type": "function(num or millis, opts, seriesName, dygraph, row, col)",
        "description": "Function to provide a custom display format for the values displayed on mouseover. This does not affect the values that appear on tick marks next to the axes. To format those, see axisLabelFormatter. This is usually set on a <a href='per-axis.html'>per-axis</a> basis. .",
        "parameters": [["num_or_millis", "The value to be formatted. This is always a number. For date axes, it's millis since epoch. You can call new Date(millis) to get a Date object."], ["opts", "This is a function you can call to access various options (e.g. opts('labelsKMB')). It returns per-axis values for the option when available."], ["seriesName", "The name of the series from which the point came, e.g. 'X', 'Y', 'A', etc."], ["dygraph", "The dygraph object for which the formatting is being done"], ["row", "The row of the data from which this point comes. g.getValue(row, 0) will return the x-value for this point."], ["col", "The column of the data from which this point comes. g.getValue(row, col) will return the original y-value for this point. This can be used to get the full confidence interval for the point, or access un-rolled values for the point."]]
      },
      "annotationMouseOverHandler": {
        "default": "null",
        "labels": ["Annotations"],
        "type": "function(annotation, point, dygraph, event)",
        "description": "If provided, this function is called whenever the user mouses over an annotation."
      },
      "annotationMouseOutHandler": {
        "default": "null",
        "labels": ["Annotations"],
        "type": "function(annotation, point, dygraph, event)",
        "parameters": [["annotation", "the annotation left"], ["point", "the point associated with the annotation"], ["dygraph", "the reference graph"], ["event", "the mouse event"]],
        "description": "If provided, this function is called whenever the user mouses out of an annotation."
      },
      "annotationClickHandler": {
        "default": "null",
        "labels": ["Annotations"],
        "type": "function(annotation, point, dygraph, event)",
        "parameters": [["annotation", "the annotation left"], ["point", "the point associated with the annotation"], ["dygraph", "the reference graph"], ["event", "the mouse event"]],
        "description": "If provided, this function is called whenever the user clicks on an annotation."
      },
      "annotationDblClickHandler": {
        "default": "null",
        "labels": ["Annotations"],
        "type": "function(annotation, point, dygraph, event)",
        "parameters": [["annotation", "the annotation left"], ["point", "the point associated with the annotation"], ["dygraph", "the reference graph"], ["event", "the mouse event"]],
        "description": "If provided, this function is called whenever the user double-clicks on an annotation."
      },
      "drawCallback": {
        "default": "null",
        "labels": ["Callbacks"],
        "type": "function(dygraph, is_initial)",
        "parameters": [["dygraph", "The graph being drawn"], ["is_initial", "True if this is the initial draw, false for subsequent draws."]],
        "description": "When set, this callback gets called every time the dygraph is drawn. This includes the initial draw, after zooming and repeatedly while panning."
      },
      "labelsKMG2": {
        "default": "false",
        "labels": ["Value display/formatting"],
        "type": "boolean",
        "description": "Show k/M/G for kilo/Mega/Giga on y-axis. This is different than <code>labelsKMB</code> in that it uses base 2, not 10."
      },
      "delimiter": {
        "default": ",",
        "labels": ["CSV parsing"],
        "type": "string",
        "description": "The delimiter to look for when separating fields of a CSV file. Setting this to a tab is not usually necessary, since tab-delimited data is auto-detected."
      },
      "axisLabelFontSize": {
        "default": "14",
        "labels": ["Axis display"],
        "type": "integer",
        "description": "Size of the font (in pixels) to use in the axis labels, both x- and y-axis."
      },
      "underlayCallback": {
        "default": "null",
        "labels": ["Callbacks"],
        "type": "function(context, area, dygraph)",
        "parameters": [["context", "the canvas drawing context on which to draw"], ["area", "An object with {x,y,w,h} properties describing the drawing area."], ["dygraph", "the reference graph"]],
        "description": "When set, this callback gets called before the chart is drawn. It details on how to use this."
      },
      "width": {
        "default": "480",
        "labels": ["Overall display"],
        "type": "integer",
        "description": "Width, in pixels, of the chart. If the container div has been explicitly sized, this will be ignored."
      },
      "pixelRatio": {
        "default": "(devicePixelRatio / context.backingStoreRatio)",
        "labels": ["Overall display"],
        "type": "float",
        "description": "Overrides the pixel ratio scaling factor for the canvas's 2d context. Ordinarily, this is set to the devicePixelRatio / (context.backingStoreRatio || 1), so on mobile devices, where the devicePixelRatio can be somewhere around 3, performance can be improved by overriding this value to something less precise, like 1, at the expense of resolution."
      },
      "interactionModel": {
        "default": "...",
        "labels": ["Interactive Elements"],
        "type": "Object",
        "description": "TODO(konigsberg): document this"
      },
      "ticker": {
        "default": "Dygraph.dateTicker or Dygraph.numericTicks",
        "labels": ["Axis display"],
        "type": "function(min, max, pixels, opts, dygraph, vals) -> [{v: ..., label: ...}, ...]",
        "parameters": [["min", ""], ["max", ""], ["pixels", ""], ["opts", ""], ["dygraph", "the reference graph"], ["vals", ""]],
        "description": "This lets you specify an arbitrary function to generate tick marks on an axis. The tick marks are an array of (value, label) pairs. The built-in functions go to great lengths to choose good tick marks so, if you set this option, you'll most likely want to call one of them and modify the result. See dygraph-tickers.js for an extensive discussion. This is set on a <a href='per-axis.html'>per-axis</a> basis."
      },
      "xAxisHeight": {
        "default": "(null)",
        "labels": ["Axis display"],
        "type": "integer",
        "description": "Height, in pixels, of the x-axis. If not set explicitly, this is computed based on axisLabelFontSize and axisTickSize."
      },
      "showLabelsOnHighlight": {
        "default": "true",
        "labels": ["Interactive Elements", "Legend"],
        "type": "boolean",
        "description": "Whether to show the legend upon mouseover."
      },
      "axis": {
        "default": "(none)",
        "labels": ["Axis display"],
        "type": "string",
        "description": "Set to either 'y1' or 'y2' to assign a series to a y-axis (primary or secondary). Must be set per-series."
      },
      "pixelsPerLabel": {
        "default": "70 (x-axis) or 30 (y-axes)",
        "labels": ["Axis display", "Grid"],
        "type": "integer",
        "description": "Number of pixels to require between each x- and y-label. Larger values will yield a sparser axis with fewer ticks. This is set on a <a href='per-axis.html'>per-axis</a> basis."
      },
      "labelsDiv": {
        "default": "null",
        "labels": ["Legend"],
        "type": "DOM element or string",
        "example": "<code style='font-size: small'>document.getElementById('foo')</code>or<code>'foo'",
        "description": "Show data labels in an external div, rather than on the graph.  This value can either be a div element or a div id."
      },
      "fractions": {
        "default": "false",
        "labels": ["CSV parsing", "Error Bars"],
        "type": "boolean",
        "description": "When set, attempt to parse each cell in the CSV file as \\"a/b\\", where a and b are integers. The ratio will be plotted. This allows computation of Wilson confidence intervals (see below)."
      },
      "logscale": {
        "default": "false",
        "labels": ["Axis display"],
        "type": "boolean",
        "description": "When set for the y-axis or x-axis, the graph shows that axis in log scale. Any values less than or equal to zero are not displayed. Showing log scale with ranges that go below zero will result in an unviewable graph.\\n\\n Not compatible with showZero. connectSeparatedPoints is ignored. This is ignored for date-based x-axes."
      },
      "strokeWidth": {
        "default": "1.0",
        "labels": ["Data Line display"],
        "type": "float",
        "example": "0.5, 2.0",
        "description": "The width of the lines connecting data points. This can be used to increase the contrast or some graphs."
      },
      "strokePattern": {
        "default": "null",
        "labels": ["Data Line display"],
        "type": "array<integer>",
        "example": "[10, 2, 5, 2]",
        "description": "A custom pattern array where the even index is a draw and odd is a space in pixels. If null then it draws a solid line. The array should have a even length as any odd lengthed array could be expressed as a smaller even length array. This is used to create dashed lines."
      },
      "strokeBorderWidth": {
        "default": "null",
        "labels": ["Data Line display"],
        "type": "float",
        "example": "1.0",
        "description": "Draw a border around graph lines to make crossing lines more easily distinguishable. Useful for graphs with many lines."
      },
      "strokeBorderColor": {
        "default": "white",
        "labels": ["Data Line display"],
        "type": "string",
        "example": "red, #ccffdd",
        "description": "Color for the line border used if strokeBorderWidth is set."
      },
      "wilsonInterval": {
        "default": "true",
        "labels": ["Error Bars"],
        "type": "boolean",
        "description": "Use in conjunction with the \\"fractions\\" option. Instead of plotting +/- N standard deviations, dygraphs will compute a Wilson confidence interval and plot that. This has more reasonable behavior for ratios close to 0 or 1."
      },
      "fillGraph": {
        "default": "false",
        "labels": ["Data Line display"],
        "type": "boolean",
        "description": "Should the area underneath the graph be filled? This option is not compatible with error bars. This may be set on a <a href='per-axis.html'>per-series</a> basis."
      },
      "highlightCircleSize": {
        "default": "3",
        "labels": ["Interactive Elements"],
        "type": "integer",
        "description": "The size in pixels of the dot drawn over highlighted points."
      },
      "gridLineColor": {
        "default": "rgb(128,128,128)",
        "labels": ["Grid"],
        "type": "red, blue",
        "description": "The color of the gridlines. This may be set on a per-axis basis to define each axis' grid separately."
      },
      "gridLinePattern": {
        "default": "null",
        "labels": ["Grid"],
        "type": "array<integer>",
        "example": "[10, 2, 5, 2]",
        "description": "A custom pattern array where the even index is a draw and odd is a space in pixels. If null then it draws a solid line. The array should have a even length as any odd lengthed array could be expressed as a smaller even length array. This is used to create dashed gridlines."
      },
      "visibility": {
        "default": "[true, true, ...]",
        "labels": ["Data Line display"],
        "type": "Array of booleans",
        "description": "Which series should initially be visible? Once the Dygraph has been constructed, you can access and modify the visibility of each series using the <code>visibility</code> and <code>setVisibility</code> methods."
      },
      "valueRange": {
        "default": "Full range of the input is shown",
        "labels": ["Axis display"],
        "type": "Array of two numbers",
        "example": "[10, 110]",
        "description": "Explicitly set the vertical range of the graph to [low, high]. This may be set on a per-axis basis to define each y-axis separately. If either limit is unspecified, it will be calculated automatically (e.g. [null, 30] to automatically calculate just the lower bound)"
      },
      "colorSaturation": {
        "default": "1.0",
        "labels": ["Data Series Colors"],
        "type": "float (0.0 - 1.0)",
        "description": "If <strong>colors</strong> is not specified, saturation of the automatically-generated data series colors."
      },
      "hideOverlayOnMouseOut": {
        "default": "true",
        "labels": ["Interactive Elements", "Legend"],
        "type": "boolean",
        "description": "Whether to hide the legend when the mouse leaves the chart area."
      },
      "legend": {
        "default": "onmouseover",
        "labels": ["Legend"],
        "type": "string",
        "description": "When to display the legend. By default, it only appears when a user mouses over the chart. Set it to \\"always\\" to always display a legend of some sort. When set to \\"follow\\", legend follows highlighted points."
      },
      "legendFormatter": {
        "default": "null",
        "labels": ["Legend"],
        "type": "function(data): string",
        "params": [["data", "An object containing information about the selection (or lack of a selection). This includes formatted values and series information. See <a href=\\"https://github.com/danvk/dygraphs/pull/683\\">here</a> for sample values."]],
        "description": "Set this to supply a custom formatter for the legend. See <a href=\\"https://github.com/danvk/dygraphs/pull/683\\">this comment</a> and the <a href=\\"tests/legend-formatter.html\\">legendFormatter demo</a> for usage."
      },
      "labelsShowZeroValues": {
        "default": "true",
        "labels": ["Legend"],
        "type": "boolean",
        "description": "Show zero value labels in the labelsDiv."
      },
      "stepPlot": {
        "default": "false",
        "labels": ["Data Line display"],
        "type": "boolean",
        "description": "When set, display the graph as a step plot instead of a line plot. This option may either be set for the whole graph or for single series."
      },
      "labelsUTC": {
        "default": "false",
        "labels": ["Value display/formatting", "Axis display"],
        "type": "boolean",
        "description": "Show date/time labels according to UTC (instead of local time)."
      },
      "labelsKMB": {
        "default": "false",
        "labels": ["Value display/formatting"],
        "type": "boolean",
        "description": "Show K/M/B for thousands/millions/billions on y-axis."
      },
      "rightGap": {
        "default": "5",
        "labels": ["Overall display"],
        "type": "integer",
        "description": "Number of pixels to leave blank at the right edge of the Dygraph. This makes it easier to highlight the right-most data point."
      },
      "drawAxesAtZero": {
        "default": "false",
        "labels": ["Axis display"],
        "type": "boolean",
        "description": "When set, draw the X axis at the Y=0 position and the Y axis at the X=0 position if those positions are inside the graph's visible area. Otherwise, draw the axes at the bottom or left graph edge as usual."
      },
      "xRangePad": {
        "default": "0",
        "labels": ["Axis display"],
        "type": "float",
        "description": "Add the specified amount of extra space (in pixels) around the X-axis value range to ensure points at the edges remain visible."
      },
      "yRangePad": {
        "default": "null",
        "labels": ["Axis display"],
        "type": "float",
        "description": "If set, add the specified amount of extra space (in pixels) around the Y-axis value range to ensure points at the edges remain visible. If unset, use the traditional Y padding algorithm."
      },
      "axisLabelFormatter": {
        "default": "Depends on the data type",
        "labels": ["Axis display"],
        "type": "function(number or Date, granularity, opts, dygraph)",
        "parameters": [["number or date", "Either a number (for a numeric axis) or a Date object (for a date axis)"], ["granularity", "specifies how fine-grained the axis is. For date axes, this is a reference to the time granularity enumeration, defined in dygraph-tickers.js, e.g. Dygraph.WEEKLY."], ["opts", "a function which provides access to various options on the dygraph, e.g. opts('labelsKMB')."], ["dygraph", "the referenced graph"]],
        "description": "Function to call to format the tick values that appear along an axis. This is usually set on a <a href='per-axis.html'>per-axis</a> basis."
      },
      "clickCallback": {
        "snippet": "function(e, date_millis){<br>&nbsp;&nbsp;alert(new Date(date_millis));<br>}",
        "default": "null",
        "labels": ["Callbacks"],
        "type": "function(e, x, points)",
        "parameters": [["e", "The event object for the click"], ["x", "The x value that was clicked (for dates, this is milliseconds since epoch)"], ["points", "The closest points along that date. See <a href='#point_properties'>Point properties</a> for details."]],
        "description": "A function to call when the canvas is clicked."
      },
      "labels": {
        "default": "[\\"X\\", \\"Y1\\", \\"Y2\\", ...]*",
        "labels": ["Legend"],
        "type": "array<string>",
        "description": "A name for each data series, including the independent (X) series. For CSV files and DataTable objections, this is determined by context. For raw data, this must be specified. If it is not, default values are supplied and a warning is logged."
      },
      "dateWindow": {
        "default": "Full range of the input is shown",
        "labels": ["Axis display"],
        "type": "Array of two numbers",
        "example": "[<br>&nbsp;&nbsp;Date.parse('2006-01-01'),<br>&nbsp;&nbsp;(new Date()).valueOf()<br>]",
        "description": "Initially zoom in on a section of the graph. Is of the form [earliest, latest], where earliest/latest are milliseconds since epoch. If the data for the x-axis is numeric, the values in dateWindow must also be numbers."
      },
      "showRoller": {
        "default": "false",
        "labels": ["Interactive Elements", "Rolling Averages"],
        "type": "boolean",
        "description": "If the rolling average period text box should be shown."
      },
      "sigma": {
        "default": "2.0",
        "labels": ["Error Bars"],
        "type": "float",
        "description": "When errorBars is set, shade this many standard deviations above/below each point."
      },
      "customBars": {
        "default": "false",
        "labels": ["CSV parsing", "Error Bars"],
        "type": "boolean",
        "description": "When set, parse each CSV cell as \\"low;middle;high\\". Error bars will be drawn for each point between low and high, with the series itself going through middle."
      },
      "colorValue": {
        "default": "1.0",
        "labels": ["Data Series Colors"],
        "type": "float (0.0 - 1.0)",
        "description": "If colors is not specified, value of the data series colors, as in hue/saturation/value. (0.0-1.0, default 0.5)"
      },
      "errorBars": {
        "default": "false",
        "labels": ["CSV parsing", "Error Bars"],
        "type": "boolean",
        "description": "Does the data contain standard deviations? Setting this to true alters the input format (see above)."
      },
      "displayAnnotations": {
        "default": "false",
        "labels": ["Annotations"],
        "type": "boolean",
        "description": "Only applies when Dygraphs is used as a GViz chart. Causes string columns following a data series to be interpreted as annotations on points in that series. This is the same format used by Google's AnnotatedTimeLine chart."
      },
      "panEdgeFraction": {
        "default": "null",
        "labels": ["Axis display", "Interactive Elements"],
        "type": "float",
        "description": "A value representing the farthest a graph may be panned, in percent of the display. For example, a value of 0.1 means that the graph can only be panned 10% passed the edges of the displayed values. null means no bounds."
      },
      "title": {
        "labels": ["Chart labels"],
        "type": "string",
        "default": "null",
        "description": "Text to display above the chart. You can supply any HTML for this value, not just text. If you wish to style it using CSS, use the 'dygraph-label' or 'dygraph-title' classes."
      },
      "titleHeight": {
        "default": "18",
        "labels": ["Chart labels"],
        "type": "integer",
        "description": "Height of the chart title, in pixels. This also controls the default font size of the title. If you style the title on your own, this controls how much space is set aside above the chart for the title's div."
      },
      "xlabel": {
        "labels": ["Chart labels"],
        "type": "string",
        "default": "null",
        "description": "Text to display below the chart's x-axis. You can supply any HTML for this value, not just text. If you wish to style it using CSS, use the 'dygraph-label' or 'dygraph-xlabel' classes."
      },
      "xLabelHeight": {
        "labels": ["Chart labels"],
        "type": "integer",
        "default": "18",
        "description": "Height of the x-axis label, in pixels. This also controls the default font size of the x-axis label. If you style the label on your own, this controls how much space is set aside below the chart for the x-axis label's div."
      },
      "ylabel": {
        "labels": ["Chart labels"],
        "type": "string",
        "default": "null",
        "description": "Text to display to the left of the chart's y-axis. You can supply any HTML for this value, not just text. If you wish to style it using CSS, use the 'dygraph-label' or 'dygraph-ylabel' classes. The text will be rotated 90 degrees by default, so CSS rules may behave in unintuitive ways. No additional space is set aside for a y-axis label. If you need more space, increase the width of the y-axis tick labels using the yAxisLabelWidth option. If you need a wider div for the y-axis label, either style it that way with CSS (but remember that it's rotated, so width is controlled by the 'height' property) or set the yLabelWidth option."
      },
      "y2label": {
        "labels": ["Chart labels"],
        "type": "string",
        "default": "null",
        "description": "Text to display to the right of the chart's secondary y-axis. This label is only displayed if a secondary y-axis is present. See <a href='http://dygraphs.com/tests/two-axes.html'>this test</a> for an example of how to do this. The comments for the 'ylabel' option generally apply here as well. This label gets a 'dygraph-y2label' instead of a 'dygraph-ylabel' class."
      },
      "yLabelWidth": {
        "labels": ["Chart labels"],
        "type": "integer",
        "default": "18",
        "description": "Width of the div which contains the y-axis label. Since the y-axis label appears rotated 90 degrees, this actually affects the height of its div."
      },
      "drawGrid": {
        "default": "true for x and y, false for y2",
        "labels": ["Grid"],
        "type": "boolean",
        "description": "Whether to display gridlines in the chart. This may be set on a per-axis basis to define the visibility of each axis' grid separately."
      },
      "independentTicks": {
        "default": "true for y, false for y2",
        "labels": ["Axis display", "Grid"],
        "type": "boolean",
        "description": "Only valid for y and y2, has no effect on x: This option defines whether the y axes should align their ticks or if they should be independent. Possible combinations: 1.) y=true, y2=false (default): y is the primary axis and the y2 ticks are aligned to the the ones of y. (only 1 grid) 2.) y=false, y2=true: y2 is the primary axis and the y ticks are aligned to the the ones of y2. (only 1 grid) 3.) y=true, y2=true: Both axis are independent and have their own ticks. (2 grids) 4.) y=false, y2=false: Invalid configuration causes an error."
      },
      "drawAxis": {
        "default": "true for x and y, false for y2",
        "labels": ["Axis display"],
        "type": "boolean",
        "description": "Whether to draw the specified axis. This may be set on a per-axis basis to define the visibility of each axis separately. Setting this to false also prevents axis ticks from being drawn and reclaims the space for the chart grid/lines."
      },
      "gridLineWidth": {
        "default": "0.3",
        "labels": ["Grid"],
        "type": "float",
        "description": "Thickness (in pixels) of the gridlines drawn under the chart. The vertical/horizontal gridlines can be turned off entirely by using the drawGrid option. This may be set on a per-axis basis to define each axis' grid separately."
      },
      "axisLineWidth": {
        "default": "0.3",
        "labels": ["Axis display"],
        "type": "float",
        "description": "Thickness (in pixels) of the x- and y-axis lines."
      },
      "axisLineColor": {
        "default": "black",
        "labels": ["Axis display"],
        "type": "string",
        "description": "Color of the x- and y-axis lines. Accepts any value which the HTML canvas strokeStyle attribute understands, e.g. 'black' or 'rgb(0, 100, 255)'."
      },
      "fillAlpha": {
        "default": "0.15",
        "labels": ["Error Bars", "Data Series Colors"],
        "type": "float (0.0 - 1.0)",
        "description": "Error bars (or custom bars) for each series are drawn in the same color as the series, but with partial transparency. This sets the transparency. A value of 0.0 means that the error bars will not be drawn, whereas a value of 1.0 means that the error bars will be as dark as the line for the series itself. This can be used to produce chart lines whose thickness varies at each point."
      },
      "axisLabelWidth": {
        "default": "50 (y-axis), 60 (x-axis)",
        "labels": ["Axis display", "Chart labels"],
        "type": "integer",
        "description": "Width (in pixels) of the containing divs for x- and y-axis labels. For the y-axis, this also controls the width of the y-axis. Note that for the x-axis, this is independent from pixelsPerLabel, which controls the spacing between labels."
      },
      "sigFigs": {
        "default": "null",
        "labels": ["Value display/formatting"],
        "type": "integer",
        "description": "By default, dygraphs displays numbers with a fixed number of digits after the decimal point. If you'd prefer to have a fixed number of significant figures, set this option to that number of sig figs. A value of 2, for instance, would cause 1 to be display as 1.0 and 1234 to be displayed as 1.23e+3."
      },
      "digitsAfterDecimal": {
        "default": "2",
        "labels": ["Value display/formatting"],
        "type": "integer",
        "description": "Unless it's run in scientific mode (see the <code>sigFigs</code> option), dygraphs displays numbers with <code>digitsAfterDecimal</code> digits after the decimal point. Trailing zeros are not displayed, so with a value of 2 you'll get '0', '0.1', '0.12', '123.45' but not '123.456' (it will be rounded to '123.46'). Numbers with absolute value less than 0.1^digitsAfterDecimal (i.e. those which would show up as '0.00') will be displayed in scientific notation."
      },
      "maxNumberWidth": {
        "default": "6",
        "labels": ["Value display/formatting"],
        "type": "integer",
        "description": "When displaying numbers in normal (not scientific) mode, large numbers will be displayed with many trailing zeros (e.g. 100000000 instead of 1e9). This can lead to unwieldy y-axis labels. If there are more than <code>maxNumberWidth</code> digits to the left of the decimal in a number, dygraphs will switch to scientific notation, even when not operating in scientific mode. If you'd like to see all those digits, set this to something large, like 20 or 30."
      },
      "file": {
        "default": "(set when constructed)",
        "labels": ["Data"],
        "type": "string (URL of CSV or CSV), GViz DataTable or 2D Array",
        "description": "Sets the data being displayed in the chart. This can only be set when calling updateOptions; it cannot be set from the constructor. For a full description of valid data formats, see the <a href='http://dygraphs.com/data.html'>Data Formats</a> page."
      },
      "timingName": {
        "default": "null",
        "labels": ["Debugging", "Deprecated"],
        "type": "string",
        "description": "Set this option to log timing information. The value of the option will be logged along with the timimg, so that you can distinguish multiple dygraphs on the same page."
      },
      "showRangeSelector": {
        "default": "false",
        "labels": ["Range Selector"],
        "type": "boolean",
        "description": "Show or hide the range selector widget."
      },
      "rangeSelectorHeight": {
        "default": "40",
        "labels": ["Range Selector"],
        "type": "integer",
        "description": "Height, in pixels, of the range selector widget. This option can only be specified at Dygraph creation time."
      },
      "rangeSelectorPlotStrokeColor": {
        "default": "#808FAB",
        "labels": ["Range Selector"],
        "type": "string",
        "description": "The range selector mini plot stroke color. This can be of the form \\"#AABBCC\\" or \\"rgb(255,100,200)\\" or \\"yellow\\". You can also specify null or \\"\\" to turn off stroke."
      },
      "rangeSelectorPlotFillColor": {
        "default": "#A7B1C4",
        "labels": ["Range Selector"],
        "type": "string",
        "description": "The range selector mini plot fill color. This can be of the form \\"#AABBCC\\" or \\"rgb(255,100,200)\\" or \\"yellow\\". You can also specify null or \\"\\" to turn off fill."
      },
      "rangeSelectorPlotFillGradientColor": {
        "default": "white",
        "labels": ["Range Selector"],
        "type": "string",
        "description": "The top color for the range selector mini plot fill color gradient. This can be of the form \\"#AABBCC\\" or \\"rgb(255,100,200)\\" or \\"rgba(255,100,200,42)\\" or \\"yellow\\". You can also specify null or \\"\\" to disable the gradient and fill with one single color."
      },
      "rangeSelectorBackgroundStrokeColor": {
        "default": "gray",
        "labels": ["Range Selector"],
        "type": "string",
        "description": "The color of the lines below and on both sides of the range selector mini plot. This can be of the form \\"#AABBCC\\" or \\"rgb(255,100,200)\\" or \\"yellow\\"."
      },
      "rangeSelectorBackgroundLineWidth": {
        "default": "1",
        "labels": ["Range Selector"],
        "type": "float",
        "description": "The width of the lines below and on both sides of the range selector mini plot."
      },
      "rangeSelectorPlotLineWidth": {
        "default": "1.5",
        "labels": ["Range Selector"],
        "type": "float",
        "description": "The width of the range selector mini plot line."
      },
      "rangeSelectorForegroundStrokeColor": {
        "default": "black",
        "labels": ["Range Selector"],
        "type": "string",
        "description": "The color of the lines in the interactive layer of the range selector. This can be of the form \\"#AABBCC\\" or \\"rgb(255,100,200)\\" or \\"yellow\\"."
      },
      "rangeSelectorForegroundLineWidth": {
        "default": "1",
        "labels": ["Range Selector"],
        "type": "float",
        "description": "The width the lines in the interactive layer of the range selector."
      },
      "rangeSelectorAlpha": {
        "default": "0.6",
        "labels": ["Range Selector"],
        "type": "float (0.0 - 1.0)",
        "description": "The transparency of the veil that is drawn over the unselected portions of the range selector mini plot. A value of 0 represents full transparency and the unselected portions of the mini plot will appear as normal. A value of 1 represents full opacity and the unselected portions of the mini plot will be hidden."
      },
      "showInRangeSelector": {
        "default": "null",
        "labels": ["Range Selector"],
        "type": "boolean",
        "description": "Mark this series for inclusion in the range selector. The mini plot curve will be an average of all such series. If this is not specified for any series, the default behavior is to average all the visible series. Setting it for one series will result in that series being charted alone in the range selector. Once it's set for a single series, it needs to be set for all series which should be included (regardless of visibility)."
      },
      "animatedZooms": {
        "default": "false",
        "labels": ["Interactive Elements"],
        "type": "boolean",
        "description": "Set this option to animate the transition between zoom windows. Applies to programmatic and interactive zooms. Note that if you also set a drawCallback, it will be called several times on each zoom. If you set a zoomCallback, it will only be called after the animation is complete."
      },
      "plotter": {
        "default": "[DygraphCanvasRenderer.Plotters.fillPlotter, DygraphCanvasRenderer.Plotters.errorPlotter, DygraphCanvasRenderer.Plotters.linePlotter]",
        "labels": ["Data Line display"],
        "type": "array or function",
        "description": "A function (or array of functions) which plot each data series on the chart. TODO(danvk): more details! May be set per-series."
      },
      "axes": {
        "default": "null",
        "labels": ["Configuration"],
        "type": "Object",
        "description": "Defines per-axis options. Valid keys are 'x', 'y' and 'y2'. Only some options may be set on a per-axis basis. If an option may be set in this way, it will be noted on this page. See also documentation on <a href='http://dygraphs.com/per-axis.html'>per-series and per-axis options</a>."
      },
      "series": {
        "default": "null",
        "labels": ["Series"],
        "type": "Object",
        "description": "Defines per-series options. Its keys match the y-axis label names, and the values are dictionaries themselves that contain options specific to that series."
      },
      "plugins": {
        "default": "[]",
        "labels": ["Configuration"],
        "type": "Array<plugin>",
        "description": "Defines per-graph plugins. Useful for per-graph customization"
      },
      "dataHandler": {
        "default": "(depends on data)",
        "labels": ["Data"],
        "type": "Dygraph.DataHandler",
        "description": "Custom DataHandler. This is an advanced customization. See http://bit.ly/151E7Aq."
      }
    }; // </JSON>
    // NOTE: in addition to parsing as JS, this snippet is expected to be valid
    // JSON. This assumption cannot be checked in JS, but it will be checked when
    // documentation is generated by the generate-documentation.py script. For the
    // most part, this just means that you should always use double quotes.

    // Do a quick sanity check on the options reference.
    var warn = function warn(msg) {
      if (window.console) window.console.warn(msg);
    };
    var flds = ['type', 'default', 'description'];
    var valid_cats = ['Annotations', 'Axis display', 'Chart labels', 'CSV parsing', 'Callbacks', 'Data', 'Data Line display', 'Data Series Colors', 'Error Bars', 'Grid', 'Interactive Elements', 'Range Selector', 'Legend', 'Overall display', 'Rolling Averages', 'Series', 'Value display/formatting', 'Zooming', 'Debugging', 'Configuration', 'Deprecated'];
    var i;
    var cats = {};
    for (i = 0; i < valid_cats.length; i++) cats[valid_cats[i]] = true;

    for (var k in OPTIONS_REFERENCE) {
      if (!OPTIONS_REFERENCE.hasOwnProperty(k)) continue;
      var op = OPTIONS_REFERENCE[k];
      for (i = 0; i < flds.length; i++) {
        if (!op.hasOwnProperty(flds[i])) {
          warn('Option ' + k + ' missing "' + flds[i] + '" property');
        } else if (typeof op[flds[i]] != 'string') {
          warn(k + '.' + flds[i] + ' must be of type string');
        }
      }
      var labels = op.labels;
      if (typeof labels !== 'object') {
        warn('Option "' + k + '" is missing a "labels": [...] option');
      } else {
        for (i = 0; i < labels.length; i++) {
          if (!cats.hasOwnProperty(labels[i])) {
            warn('Option "' + k + '" has label "' + labels[i] + '", which is invalid.');
          }
        }
      }
    }
  }
}

exports['default'] = OPTIONS_REFERENCE;
module.exports = exports['default'];

}).call(this,require('_process'))

},{"_process":1}],15:[function(require,module,exports){
(function (process){
/**
 * @license
 * Copyright 2011 Dan Vanderkam (danvdk@gmail.com)
 * MIT-licensed (http://opensource.org/licenses/MIT)
 */

/**
 * @fileoverview DygraphOptions is responsible for parsing and returning
 * information about options.
 */

// TODO: remove this jshint directive & fix the warnings.
/*jshint sub:true */
"use strict";

Object.defineProperty(exports, '__esModule', {
  value: true
});

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { 'default': obj }; }

function _interopRequireWildcard(obj) { if (obj && obj.__esModule) { return obj; } else { var newObj = {}; if (obj != null) { for (var key in obj) { if (Object.prototype.hasOwnProperty.call(obj, key)) newObj[key] = obj[key]; } } newObj['default'] = obj; return newObj; } }

var _dygraphUtils = require('./dygraph-utils');

var utils = _interopRequireWildcard(_dygraphUtils);

var _dygraphDefaultAttrs = require('./dygraph-default-attrs');

var _dygraphDefaultAttrs2 = _interopRequireDefault(_dygraphDefaultAttrs);

var _dygraphOptionsReference = require('./dygraph-options-reference');

var _dygraphOptionsReference2 = _interopRequireDefault(_dygraphOptionsReference);

/*
 * Interesting member variables: (REMOVING THIS LIST AS I CLOSURIZE)
 * global_ - global attributes (common among all graphs, AIUI)
 * user - attributes set by the user
 * series_ - { seriesName -> { idx, yAxis, options }}
 */

/**
 * This parses attributes into an object that can be easily queried.
 *
 * It doesn't necessarily mean that all options are available, specifically
 * if labels are not yet available, since those drive details of the per-series
 * and per-axis options.
 *
 * @param {Dygraph} dygraph The chart to which these options belong.
 * @constructor
 */
var DygraphOptions = function DygraphOptions(dygraph) {
  /**
   * The dygraph.
   * @type {!Dygraph}
   */
  this.dygraph_ = dygraph;

  /**
   * Array of axis index to { series : [ series names ] , options : { axis-specific options. }
   * @type {Array.<{series : Array.<string>, options : Object}>} @private
   */
  this.yAxes_ = [];

  /**
   * Contains x-axis specific options, which are stored in the options key.
   * This matches the yAxes_ object structure (by being a dictionary with an
   * options element) allowing for shared code.
   * @type {options: Object} @private
   */
  this.xAxis_ = {};
  this.series_ = {};

  // Once these two objects are initialized, you can call get();
  this.global_ = this.dygraph_.attrs_;
  this.user_ = this.dygraph_.user_attrs_ || {};

  /**
   * A list of series in columnar order.
   * @type {Array.<string>}
   */
  this.labels_ = [];

  this.highlightSeries_ = this.get("highlightSeriesOpts") || {};
  this.reparseSeries();
};

/**
 * Not optimal, but does the trick when you're only using two axes.
 * If we move to more axes, this can just become a function.
 *
 * @type {Object.<number>}
 * @private
 */
DygraphOptions.AXIS_STRING_MAPPINGS_ = {
  'y': 0,
  'Y': 0,
  'y1': 0,
  'Y1': 0,
  'y2': 1,
  'Y2': 1
};

/**
 * @param {string|number} axis
 * @private
 */
DygraphOptions.axisToIndex_ = function (axis) {
  if (typeof axis == "string") {
    if (DygraphOptions.AXIS_STRING_MAPPINGS_.hasOwnProperty(axis)) {
      return DygraphOptions.AXIS_STRING_MAPPINGS_[axis];
    }
    throw "Unknown axis : " + axis;
  }
  if (typeof axis == "number") {
    if (axis === 0 || axis === 1) {
      return axis;
    }
    throw "Dygraphs only supports two y-axes, indexed from 0-1.";
  }
  if (axis) {
    throw "Unknown axis : " + axis;
  }
  // No axis specification means axis 0.
  return 0;
};

/**
 * Reparses options that are all related to series. This typically occurs when
 * options are either updated, or source data has been made available.
 *
 * TODO(konigsberg): The method name is kind of weak; fix.
 */
DygraphOptions.prototype.reparseSeries = function () {
  var labels = this.get("labels");
  if (!labels) {
    return; // -- can't do more for now, will parse after getting the labels.
  }

  this.labels_ = labels.slice(1);

  this.yAxes_ = [{ series: [], options: {} }]; // Always one axis at least.
  this.xAxis_ = { options: {} };
  this.series_ = {};

  // Series are specified in the series element:
  //
  // {
  //   labels: [ "X", "foo", "bar" ],
  //   pointSize: 3,
  //   series : {
  //     foo : {}, // options for foo
  //     bar : {} // options for bar
  //   }
  // }
  //
  // So, if series is found, it's expected to contain per-series data, otherwise set a
  // default.
  var seriesDict = this.user_.series || {};
  for (var idx = 0; idx < this.labels_.length; idx++) {
    var seriesName = this.labels_[idx];
    var optionsForSeries = seriesDict[seriesName] || {};
    var yAxis = DygraphOptions.axisToIndex_(optionsForSeries["axis"]);

    this.series_[seriesName] = {
      idx: idx,
      yAxis: yAxis,
      options: optionsForSeries };

    if (!this.yAxes_[yAxis]) {
      this.yAxes_[yAxis] = { series: [seriesName], options: {} };
    } else {
      this.yAxes_[yAxis].series.push(seriesName);
    }
  }

  var axis_opts = this.user_["axes"] || {};
  utils.update(this.yAxes_[0].options, axis_opts["y"] || {});
  if (this.yAxes_.length > 1) {
    utils.update(this.yAxes_[1].options, axis_opts["y2"] || {});
  }
  utils.update(this.xAxis_.options, axis_opts["x"] || {});

  // For "production" code, this gets removed by uglifyjs.
  if (typeof process !== 'undefined') {
    if ("development" != 'production') {
      this.validateOptions_();
    }
  }
};

/**
 * Get a global value.
 *
 * @param {string} name the name of the option.
 */
DygraphOptions.prototype.get = function (name) {
  var result = this.getGlobalUser_(name);
  if (result !== null) {
    return result;
  }
  return this.getGlobalDefault_(name);
};

DygraphOptions.prototype.getGlobalUser_ = function (name) {
  if (this.user_.hasOwnProperty(name)) {
    return this.user_[name];
  }
  return null;
};

DygraphOptions.prototype.getGlobalDefault_ = function (name) {
  if (this.global_.hasOwnProperty(name)) {
    return this.global_[name];
  }
  if (_dygraphDefaultAttrs2['default'].hasOwnProperty(name)) {
    return _dygraphDefaultAttrs2['default'][name];
  }
  return null;
};

/**
 * Get a value for a specific axis. If there is no specific value for the axis,
 * the global value is returned.
 *
 * @param {string} name the name of the option.
 * @param {string|number} axis the axis to search. Can be the string representation
 * ("y", "y2") or the axis number (0, 1).
 */
DygraphOptions.prototype.getForAxis = function (name, axis) {
  var axisIdx;
  var axisString;

  // Since axis can be a number or a string, straighten everything out here.
  if (typeof axis == 'number') {
    axisIdx = axis;
    axisString = axisIdx === 0 ? "y" : "y2";
  } else {
    if (axis == "y1") {
      axis = "y";
    } // Standardize on 'y'. Is this bad? I think so.
    if (axis == "y") {
      axisIdx = 0;
    } else if (axis == "y2") {
      axisIdx = 1;
    } else if (axis == "x") {
      axisIdx = -1; // simply a placeholder for below.
    } else {
        throw "Unknown axis " + axis;
      }
    axisString = axis;
  }

  var userAxis = axisIdx == -1 ? this.xAxis_ : this.yAxes_[axisIdx];

  // Search the user-specified axis option first.
  if (userAxis) {
    // This condition could be removed if we always set up this.yAxes_ for y2.
    var axisOptions = userAxis.options;
    if (axisOptions.hasOwnProperty(name)) {
      return axisOptions[name];
    }
  }

  // User-specified global options second.
  // But, hack, ignore globally-specified 'logscale' for 'x' axis declaration.
  if (!(axis === 'x' && name === 'logscale')) {
    var result = this.getGlobalUser_(name);
    if (result !== null) {
      return result;
    }
  }
  // Default axis options third.
  var defaultAxisOptions = _dygraphDefaultAttrs2['default'].axes[axisString];
  if (defaultAxisOptions.hasOwnProperty(name)) {
    return defaultAxisOptions[name];
  }

  // Default global options last.
  return this.getGlobalDefault_(name);
};

/**
 * Get a value for a specific series. If there is no specific value for the series,
 * the value for the axis is returned (and afterwards, the global value.)
 *
 * @param {string} name the name of the option.
 * @param {string} series the series to search.
 */
DygraphOptions.prototype.getForSeries = function (name, series) {
  // Honors indexes as series.
  if (series === this.dygraph_.getHighlightSeries()) {
    if (this.highlightSeries_.hasOwnProperty(name)) {
      return this.highlightSeries_[name];
    }
  }

  if (!this.series_.hasOwnProperty(series)) {
    throw "Unknown series: " + series;
  }

  var seriesObj = this.series_[series];
  var seriesOptions = seriesObj["options"];
  if (seriesOptions.hasOwnProperty(name)) {
    return seriesOptions[name];
  }

  return this.getForAxis(name, seriesObj["yAxis"]);
};

/**
 * Returns the number of y-axes on the chart.
 * @return {number} the number of axes.
 */
DygraphOptions.prototype.numAxes = function () {
  return this.yAxes_.length;
};

/**
 * Return the y-axis for a given series, specified by name.
 */
DygraphOptions.prototype.axisForSeries = function (series) {
  return this.series_[series].yAxis;
};

/**
 * Returns the options for the specified axis.
 */
// TODO(konigsberg): this is y-axis specific. Support the x axis.
DygraphOptions.prototype.axisOptions = function (yAxis) {
  return this.yAxes_[yAxis].options;
};

/**
 * Return the series associated with an axis.
 */
DygraphOptions.prototype.seriesForAxis = function (yAxis) {
  return this.yAxes_[yAxis].series;
};

/**
 * Return the list of all series, in their columnar order.
 */
DygraphOptions.prototype.seriesNames = function () {
  return this.labels_;
};

// For "production" code, this gets removed by uglifyjs.
if (typeof process !== 'undefined') {
  if ("development" != 'production') {

    /**
     * Validate all options.
     * This requires OPTIONS_REFERENCE, which is only available in debug builds.
     * @private
     */
    DygraphOptions.prototype.validateOptions_ = function () {
      if (typeof _dygraphOptionsReference2['default'] === 'undefined') {
        throw 'Called validateOptions_ in prod build.';
      }

      var that = this;
      var validateOption = function validateOption(optionName) {
        if (!_dygraphOptionsReference2['default'][optionName]) {
          that.warnInvalidOption_(optionName);
        }
      };

      var optionsDicts = [this.xAxis_.options, this.yAxes_[0].options, this.yAxes_[1] && this.yAxes_[1].options, this.global_, this.user_, this.highlightSeries_];
      var names = this.seriesNames();
      for (var i = 0; i < names.length; i++) {
        var name = names[i];
        if (this.series_.hasOwnProperty(name)) {
          optionsDicts.push(this.series_[name].options);
        }
      }
      for (var i = 0; i < optionsDicts.length; i++) {
        var dict = optionsDicts[i];
        if (!dict) continue;
        for (var optionName in dict) {
          if (dict.hasOwnProperty(optionName)) {
            validateOption(optionName);
          }
        }
      }
    };

    var WARNINGS = {}; // Only show any particular warning once.

    /**
     * Logs a warning about invalid options.
     * TODO: make this throw for testing
     * @private
     */
    DygraphOptions.prototype.warnInvalidOption_ = function (optionName) {
      if (!WARNINGS[optionName]) {
        WARNINGS[optionName] = true;
        var isSeries = this.labels_.indexOf(optionName) >= 0;
        if (isSeries) {
          console.warn('Use new-style per-series options (saw ' + optionName + ' as top-level options key). See http://bit.ly/1tceaJs');
        } else {
          console.warn('Unknown option ' + optionName + ' (full list of options at dygraphs.com/options.html');
        }
        throw "invalid option " + optionName;
      }
    };

    // Reset list of previously-shown warnings. Used for testing.
    DygraphOptions.resetWarnings_ = function () {
      WARNINGS = {};
    };
  }
}

exports['default'] = DygraphOptions;
module.exports = exports['default'];

}).call(this,require('_process'))

},{"./dygraph-default-attrs":10,"./dygraph-options-reference":14,"./dygraph-utils":17,"_process":1}],16:[function(require,module,exports){
/**
 * @license
 * Copyright 2011 Dan Vanderkam (danvdk@gmail.com)
 * MIT-licensed (http://opensource.org/licenses/MIT)
 */

/**
 * @fileoverview Description of this file.
 * @author danvk@google.com (Dan Vanderkam)
 *
 * A ticker is a function with the following interface:
 *
 * function(a, b, pixels, options_view, dygraph, forced_values);
 * -> [ { v: tick1_v, label: tick1_label[, label_v: label_v1] },
 *      { v: tick2_v, label: tick2_label[, label_v: label_v2] },
 *      ...
 *    ]
 *
 * The returned value is called a "tick list".
 *
 * Arguments
 * ---------
 *
 * [a, b] is the range of the axis for which ticks are being generated. For a
 * numeric axis, these will simply be numbers. For a date axis, these will be
 * millis since epoch (convertable to Date objects using "new Date(a)" and "new
 * Date(b)").
 *
 * opts provides access to chart- and axis-specific options. It can be used to
 * access number/date formatting code/options, check for a log scale, etc.
 *
 * pixels is the length of the axis in pixels. opts('pixelsPerLabel') is the
 * minimum amount of space to be allotted to each label. For instance, if
 * pixels=400 and opts('pixelsPerLabel')=40 then the ticker should return
 * between zero and ten (400/40) ticks.
 *
 * dygraph is the Dygraph object for which an axis is being constructed.
 *
 * forced_values is used for secondary y-axes. The tick positions are typically
 * set by the primary y-axis, so the secondary y-axis has no choice in where to
 * put these. It simply has to generate labels for these data values.
 *
 * Tick lists
 * ----------
 * Typically a tick will have both a grid/tick line and a label at one end of
 * that line (at the bottom for an x-axis, at left or right for the y-axis).
 *
 * A tick may be missing one of these two components:
 * - If "label_v" is specified instead of "v", then there will be no tick or
 *   gridline, just a label.
 * - Similarly, if "label" is not specified, then there will be a gridline
 *   without a label.
 *
 * This flexibility is useful in a few situations:
 * - For log scales, some of the tick lines may be too close to all have labels.
 * - For date scales where years are being displayed, it is desirable to display
 *   tick marks at the beginnings of years but labels (e.g. "2006") in the
 *   middle of the years.
 */

/*jshint sub:true */
/*global Dygraph:false */
"use strict";

Object.defineProperty(exports, '__esModule', {
  value: true
});

function _interopRequireWildcard(obj) { if (obj && obj.__esModule) { return obj; } else { var newObj = {}; if (obj != null) { for (var key in obj) { if (Object.prototype.hasOwnProperty.call(obj, key)) newObj[key] = obj[key]; } } newObj['default'] = obj; return newObj; } }

var _dygraphUtils = require('./dygraph-utils');

var utils = _interopRequireWildcard(_dygraphUtils);

/** @typedef {Array.<{v:number, label:string, label_v:(string|undefined)}>} */
var TickList = undefined; // the ' = undefined' keeps jshint happy.

/** @typedef {function(
 *    number,
 *    number,
 *    number,
 *    function(string):*,
 *    Dygraph=,
 *    Array.<number>=
 *  ): TickList}
 */
var Ticker = undefined; // the ' = undefined' keeps jshint happy.

/** @type {Ticker} */
var numericLinearTicks = function numericLinearTicks(a, b, pixels, opts, dygraph, vals) {
  var nonLogscaleOpts = function nonLogscaleOpts(opt) {
    if (opt === 'logscale') return false;
    return opts(opt);
  };
  return numericTicks(a, b, pixels, nonLogscaleOpts, dygraph, vals);
};

exports.numericLinearTicks = numericLinearTicks;
/** @type {Ticker} */
var numericTicks = function numericTicks(a, b, pixels, opts, dygraph, vals) {
  var pixels_per_tick = /** @type{number} */opts('pixelsPerLabel');
  var ticks = [];
  var i, j, tickV, nTicks;
  if (vals) {
    for (i = 0; i < vals.length; i++) {
      ticks.push({ v: vals[i] });
    }
  } else {
    // TODO(danvk): factor this log-scale block out into a separate function.
    if (opts("logscale")) {
      nTicks = Math.floor(pixels / pixels_per_tick);
      var minIdx = utils.binarySearch(a, PREFERRED_LOG_TICK_VALUES, 1);
      var maxIdx = utils.binarySearch(b, PREFERRED_LOG_TICK_VALUES, -1);
      if (minIdx == -1) {
        minIdx = 0;
      }
      if (maxIdx == -1) {
        maxIdx = PREFERRED_LOG_TICK_VALUES.length - 1;
      }
      // Count the number of tick values would appear, if we can get at least
      // nTicks / 4 accept them.
      var lastDisplayed = null;
      if (maxIdx - minIdx >= nTicks / 4) {
        for (var idx = maxIdx; idx >= minIdx; idx--) {
          var tickValue = PREFERRED_LOG_TICK_VALUES[idx];
          var pixel_coord = Math.log(tickValue / a) / Math.log(b / a) * pixels;
          var tick = { v: tickValue };
          if (lastDisplayed === null) {
            lastDisplayed = {
              tickValue: tickValue,
              pixel_coord: pixel_coord
            };
          } else {
            if (Math.abs(pixel_coord - lastDisplayed.pixel_coord) >= pixels_per_tick) {
              lastDisplayed = {
                tickValue: tickValue,
                pixel_coord: pixel_coord
              };
            } else {
              tick.label = "";
            }
          }
          ticks.push(tick);
        }
        // Since we went in backwards order.
        ticks.reverse();
      }
    }

    // ticks.length won't be 0 if the log scale function finds values to insert.
    if (ticks.length === 0) {
      // Basic idea:
      // Try labels every 1, 2, 5, 10, 20, 50, 100, etc.
      // Calculate the resulting tick spacing (i.e. this.height_ / nTicks).
      // The first spacing greater than pixelsPerYLabel is what we use.
      // TODO(danvk): version that works on a log scale.
      var kmg2 = opts("labelsKMG2");
      var mults, base;
      if (kmg2) {
        mults = [1, 2, 4, 8, 16, 32, 64, 128, 256];
        base = 16;
      } else {
        mults = [1, 2, 5, 10, 20, 50, 100];
        base = 10;
      }

      // Get the maximum number of permitted ticks based on the
      // graph's pixel size and pixels_per_tick setting.
      var max_ticks = Math.ceil(pixels / pixels_per_tick);

      // Now calculate the data unit equivalent of this tick spacing.
      // Use abs() since graphs may have a reversed Y axis.
      var units_per_tick = Math.abs(b - a) / max_ticks;

      // Based on this, get a starting scale which is the largest
      // integer power of the chosen base (10 or 16) that still remains
      // below the requested pixels_per_tick spacing.
      var base_power = Math.floor(Math.log(units_per_tick) / Math.log(base));
      var base_scale = Math.pow(base, base_power);

      // Now try multiples of the starting scale until we find one
      // that results in tick marks spaced sufficiently far apart.
      // The "mults" array should cover the range 1 .. base^2 to
      // adjust for rounding and edge effects.
      var scale, low_val, high_val, spacing;
      for (j = 0; j < mults.length; j++) {
        scale = base_scale * mults[j];
        low_val = Math.floor(a / scale) * scale;
        high_val = Math.ceil(b / scale) * scale;
        nTicks = Math.abs(high_val - low_val) / scale;
        spacing = pixels / nTicks;
        if (spacing > pixels_per_tick) break;
      }

      // Construct the set of ticks.
      // Allow reverse y-axis if it's explicitly requested.
      if (low_val > high_val) scale *= -1;
      for (i = 0; i <= nTicks; i++) {
        tickV = low_val + i * scale;
        ticks.push({ v: tickV });
      }
    }
  }

  var formatter = /**@type{AxisLabelFormatter}*/opts('axisLabelFormatter');

  // Add labels to the ticks.
  for (i = 0; i < ticks.length; i++) {
    if (ticks[i].label !== undefined) continue; // Use current label.
    // TODO(danvk): set granularity to something appropriate here.
    ticks[i].label = formatter.call(dygraph, ticks[i].v, 0, opts, dygraph);
  }

  return ticks;
};

exports.numericTicks = numericTicks;
/** @type {Ticker} */
var dateTicker = function dateTicker(a, b, pixels, opts, dygraph, vals) {
  var chosen = pickDateTickGranularity(a, b, pixels, opts);

  if (chosen >= 0) {
    return getDateAxis(a, b, chosen, opts, dygraph);
  } else {
    // this can happen if self.width_ is zero.
    return [];
  }
};

exports.dateTicker = dateTicker;
// Time granularity enumeration
var Granularity = {
  MILLISECONDLY: 0,
  TWO_MILLISECONDLY: 1,
  FIVE_MILLISECONDLY: 2,
  TEN_MILLISECONDLY: 3,
  FIFTY_MILLISECONDLY: 4,
  HUNDRED_MILLISECONDLY: 5,
  FIVE_HUNDRED_MILLISECONDLY: 6,
  SECONDLY: 7,
  TWO_SECONDLY: 8,
  FIVE_SECONDLY: 9,
  TEN_SECONDLY: 10,
  THIRTY_SECONDLY: 11,
  MINUTELY: 12,
  TWO_MINUTELY: 13,
  FIVE_MINUTELY: 14,
  TEN_MINUTELY: 15,
  THIRTY_MINUTELY: 16,
  HOURLY: 17,
  TWO_HOURLY: 18,
  SIX_HOURLY: 19,
  DAILY: 20,
  TWO_DAILY: 21,
  WEEKLY: 22,
  MONTHLY: 23,
  QUARTERLY: 24,
  BIANNUAL: 25,
  ANNUAL: 26,
  DECADAL: 27,
  CENTENNIAL: 28,
  NUM_GRANULARITIES: 29
};

exports.Granularity = Granularity;
// Date components enumeration (in the order of the arguments in Date)
// TODO: make this an @enum
var DateField = {
  DATEFIELD_Y: 0,
  DATEFIELD_M: 1,
  DATEFIELD_D: 2,
  DATEFIELD_HH: 3,
  DATEFIELD_MM: 4,
  DATEFIELD_SS: 5,
  DATEFIELD_MS: 6,
  NUM_DATEFIELDS: 7
};

/**
 * The value of datefield will start at an even multiple of "step", i.e.
 *   if datefield=SS and step=5 then the first tick will be on a multiple of 5s.
 *
 * For granularities <= HOURLY, ticks are generated every `spacing` ms.
 *
 * At coarser granularities, ticks are generated by incrementing `datefield` by
 *   `step`. In this case, the `spacing` value is only used to estimate the
 *   number of ticks. It should roughly correspond to the spacing between
 *   adjacent ticks.
 *
 * @type {Array.<{datefield:number, step:number, spacing:number}>}
 */
var TICK_PLACEMENT = [];
TICK_PLACEMENT[Granularity.MILLISECONDLY] = { datefield: DateField.DATEFIELD_MS, step: 1, spacing: 1 };
TICK_PLACEMENT[Granularity.TWO_MILLISECONDLY] = { datefield: DateField.DATEFIELD_MS, step: 2, spacing: 2 };
TICK_PLACEMENT[Granularity.FIVE_MILLISECONDLY] = { datefield: DateField.DATEFIELD_MS, step: 5, spacing: 5 };
TICK_PLACEMENT[Granularity.TEN_MILLISECONDLY] = { datefield: DateField.DATEFIELD_MS, step: 10, spacing: 10 };
TICK_PLACEMENT[Granularity.FIFTY_MILLISECONDLY] = { datefield: DateField.DATEFIELD_MS, step: 50, spacing: 50 };
TICK_PLACEMENT[Granularity.HUNDRED_MILLISECONDLY] = { datefield: DateField.DATEFIELD_MS, step: 100, spacing: 100 };
TICK_PLACEMENT[Granularity.FIVE_HUNDRED_MILLISECONDLY] = { datefield: DateField.DATEFIELD_MS, step: 500, spacing: 500 };
TICK_PLACEMENT[Granularity.SECONDLY] = { datefield: DateField.DATEFIELD_SS, step: 1, spacing: 1000 * 1 };
TICK_PLACEMENT[Granularity.TWO_SECONDLY] = { datefield: DateField.DATEFIELD_SS, step: 2, spacing: 1000 * 2 };
TICK_PLACEMENT[Granularity.FIVE_SECONDLY] = { datefield: DateField.DATEFIELD_SS, step: 5, spacing: 1000 * 5 };
TICK_PLACEMENT[Granularity.TEN_SECONDLY] = { datefield: DateField.DATEFIELD_SS, step: 10, spacing: 1000 * 10 };
TICK_PLACEMENT[Granularity.THIRTY_SECONDLY] = { datefield: DateField.DATEFIELD_SS, step: 30, spacing: 1000 * 30 };
TICK_PLACEMENT[Granularity.MINUTELY] = { datefield: DateField.DATEFIELD_MM, step: 1, spacing: 1000 * 60 };
TICK_PLACEMENT[Granularity.TWO_MINUTELY] = { datefield: DateField.DATEFIELD_MM, step: 2, spacing: 1000 * 60 * 2 };
TICK_PLACEMENT[Granularity.FIVE_MINUTELY] = { datefield: DateField.DATEFIELD_MM, step: 5, spacing: 1000 * 60 * 5 };
TICK_PLACEMENT[Granularity.TEN_MINUTELY] = { datefield: DateField.DATEFIELD_MM, step: 10, spacing: 1000 * 60 * 10 };
TICK_PLACEMENT[Granularity.THIRTY_MINUTELY] = { datefield: DateField.DATEFIELD_MM, step: 30, spacing: 1000 * 60 * 30 };
TICK_PLACEMENT[Granularity.HOURLY] = { datefield: DateField.DATEFIELD_HH, step: 1, spacing: 1000 * 3600 };
TICK_PLACEMENT[Granularity.TWO_HOURLY] = { datefield: DateField.DATEFIELD_HH, step: 2, spacing: 1000 * 3600 * 2 };
TICK_PLACEMENT[Granularity.SIX_HOURLY] = { datefield: DateField.DATEFIELD_HH, step: 6, spacing: 1000 * 3600 * 6 };
TICK_PLACEMENT[Granularity.DAILY] = { datefield: DateField.DATEFIELD_D, step: 1, spacing: 1000 * 86400 };
TICK_PLACEMENT[Granularity.TWO_DAILY] = { datefield: DateField.DATEFIELD_D, step: 2, spacing: 1000 * 86400 * 2 };
TICK_PLACEMENT[Granularity.WEEKLY] = { datefield: DateField.DATEFIELD_D, step: 7, spacing: 1000 * 604800 };
TICK_PLACEMENT[Granularity.MONTHLY] = { datefield: DateField.DATEFIELD_M, step: 1, spacing: 1000 * 7200 * 365.2524 }; // 1e3 * 60 * 60 * 24 * 365.2524 / 12
TICK_PLACEMENT[Granularity.QUARTERLY] = { datefield: DateField.DATEFIELD_M, step: 3, spacing: 1000 * 21600 * 365.2524 }; // 1e3 * 60 * 60 * 24 * 365.2524 / 4
TICK_PLACEMENT[Granularity.BIANNUAL] = { datefield: DateField.DATEFIELD_M, step: 6, spacing: 1000 * 43200 * 365.2524 }; // 1e3 * 60 * 60 * 24 * 365.2524 / 2
TICK_PLACEMENT[Granularity.ANNUAL] = { datefield: DateField.DATEFIELD_Y, step: 1, spacing: 1000 * 86400 * 365.2524 }; // 1e3 * 60 * 60 * 24 * 365.2524 * 1
TICK_PLACEMENT[Granularity.DECADAL] = { datefield: DateField.DATEFIELD_Y, step: 10, spacing: 1000 * 864000 * 365.2524 }; // 1e3 * 60 * 60 * 24 * 365.2524 * 10
TICK_PLACEMENT[Granularity.CENTENNIAL] = { datefield: DateField.DATEFIELD_Y, step: 100, spacing: 1000 * 8640000 * 365.2524 }; // 1e3 * 60 * 60 * 24 * 365.2524 * 100

/**
 * This is a list of human-friendly values at which to show tick marks on a log
 * scale. It is k * 10^n, where k=1..9 and n=-39..+39, so:
 * ..., 1, 2, 3, 4, 5, ..., 9, 10, 20, 30, ..., 90, 100, 200, 300, ...
 * NOTE: this assumes that utils.LOG_SCALE = 10.
 * @type {Array.<number>}
 */
var PREFERRED_LOG_TICK_VALUES = (function () {
  var vals = [];
  for (var power = -39; power <= 39; power++) {
    var range = Math.pow(10, power);
    for (var mult = 1; mult <= 9; mult++) {
      var val = range * mult;
      vals.push(val);
    }
  }
  return vals;
})();

/**
 * Determine the correct granularity of ticks on a date axis.
 *
 * @param {number} a Left edge of the chart (ms)
 * @param {number} b Right edge of the chart (ms)
 * @param {number} pixels Size of the chart in the relevant dimension (width).
 * @param {function(string):*} opts Function mapping from option name -&gt; value.
 * @return {number} The appropriate axis granularity for this chart. See the
 *     enumeration of possible values in dygraph-tickers.js.
 */
var pickDateTickGranularity = function pickDateTickGranularity(a, b, pixels, opts) {
  var pixels_per_tick = /** @type{number} */opts('pixelsPerLabel');
  for (var i = 0; i < Granularity.NUM_GRANULARITIES; i++) {
    var num_ticks = numDateTicks(a, b, i);
    if (pixels / num_ticks >= pixels_per_tick) {
      return i;
    }
  }
  return -1;
};

/**
 * Compute the number of ticks on a date axis for a given granularity.
 * @param {number} start_time
 * @param {number} end_time
 * @param {number} granularity (one of the granularities enumerated above)
 * @return {number} (Approximate) number of ticks that would result.
 */
var numDateTicks = function numDateTicks(start_time, end_time, granularity) {
  var spacing = TICK_PLACEMENT[granularity].spacing;
  return Math.round(1.0 * (end_time - start_time) / spacing);
};

/**
 * Compute the positions and labels of ticks on a date axis for a given granularity.
 * @param {number} start_time
 * @param {number} end_time
 * @param {number} granularity (one of the granularities enumerated above)
 * @param {function(string):*} opts Function mapping from option name -&gt; value.
 * @param {Dygraph=} dg
 * @return {!TickList}
 */
var getDateAxis = function getDateAxis(start_time, end_time, granularity, opts, dg) {
  var formatter = /** @type{AxisLabelFormatter} */opts("axisLabelFormatter");
  var utc = opts("labelsUTC");
  var accessors = utc ? utils.DateAccessorsUTC : utils.DateAccessorsLocal;

  var datefield = TICK_PLACEMENT[granularity].datefield;
  var step = TICK_PLACEMENT[granularity].step;
  var spacing = TICK_PLACEMENT[granularity].spacing;

  // Choose a nice tick position before the initial instant.
  // Currently, this code deals properly with the existent daily granularities:
  // DAILY (with step of 1) and WEEKLY (with step of 7 but specially handled).
  // Other daily granularities (say TWO_DAILY) should also be handled specially
  // by setting the start_date_offset to 0.
  var start_date = new Date(start_time);
  var date_array = [];
  date_array[DateField.DATEFIELD_Y] = accessors.getFullYear(start_date);
  date_array[DateField.DATEFIELD_M] = accessors.getMonth(start_date);
  date_array[DateField.DATEFIELD_D] = accessors.getDate(start_date);
  date_array[DateField.DATEFIELD_HH] = accessors.getHours(start_date);
  date_array[DateField.DATEFIELD_MM] = accessors.getMinutes(start_date);
  date_array[DateField.DATEFIELD_SS] = accessors.getSeconds(start_date);
  date_array[DateField.DATEFIELD_MS] = accessors.getMilliseconds(start_date);

  var start_date_offset = date_array[datefield] % step;
  if (granularity == Granularity.WEEKLY) {
    // This will put the ticks on Sundays.
    start_date_offset = accessors.getDay(start_date);
  }

  date_array[datefield] -= start_date_offset;
  for (var df = datefield + 1; df < DateField.NUM_DATEFIELDS; df++) {
    // The minimum value is 1 for the day of month, and 0 for all other fields.
    date_array[df] = df === DateField.DATEFIELD_D ? 1 : 0;
  }

  // Generate the ticks.
  // For granularities not coarser than HOURLY we use the fact that:
  //   the number of milliseconds between ticks is constant
  //   and equal to the defined spacing.
  // Otherwise we rely on the 'roll over' property of the Date functions:
  //   when some date field is set to a value outside of its logical range,
  //   the excess 'rolls over' the next (more significant) field.
  // However, when using local time with DST transitions,
  // there are dates that do not represent any time value at all
  // (those in the hour skipped at the 'spring forward'),
  // and the JavaScript engines usually return an equivalent value.
  // Hence we have to check that the date is properly increased at each step,
  // returning a date at a nice tick position.
  var ticks = [];
  var tick_date = accessors.makeDate.apply(null, date_array);
  var tick_time = tick_date.getTime();
  if (granularity <= Granularity.HOURLY) {
    if (tick_time < start_time) {
      tick_time += spacing;
      tick_date = new Date(tick_time);
    }
    while (tick_time <= end_time) {
      ticks.push({ v: tick_time,
        label: formatter.call(dg, tick_date, granularity, opts, dg)
      });
      tick_time += spacing;
      tick_date = new Date(tick_time);
    }
  } else {
    if (tick_time < start_time) {
      date_array[datefield] += step;
      tick_date = accessors.makeDate.apply(null, date_array);
      tick_time = tick_date.getTime();
    }
    while (tick_time <= end_time) {
      if (granularity >= Granularity.DAILY || accessors.getHours(tick_date) % step === 0) {
        ticks.push({ v: tick_time,
          label: formatter.call(dg, tick_date, granularity, opts, dg)
        });
      }
      date_array[datefield] += step;
      tick_date = accessors.makeDate.apply(null, date_array);
      tick_time = tick_date.getTime();
    }
  }
  return ticks;
};
exports.getDateAxis = getDateAxis;

},{"./dygraph-utils":17}],17:[function(require,module,exports){
/**
 * @license
 * Copyright 2011 Dan Vanderkam (danvdk@gmail.com)
 * MIT-licensed (http://opensource.org/licenses/MIT)
 */

/**
 * @fileoverview This file contains utility functions used by dygraphs. These
 * are typically static (i.e. not related to any particular dygraph). Examples
 * include date/time formatting functions, basic algorithms (e.g. binary
 * search) and generic DOM-manipulation functions.
 */

/*global Dygraph:false, Node:false */
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.removeEvent = removeEvent;
exports.cancelEvent = cancelEvent;
exports.hsvToRGB = hsvToRGB;
exports.findPos = findPos;
exports.pageX = pageX;
exports.pageY = pageY;
exports.dragGetX_ = dragGetX_;
exports.dragGetY_ = dragGetY_;
exports.isOK = isOK;
exports.isValidPoint = isValidPoint;
exports.floatFormat = floatFormat;
exports.zeropad = zeropad;
exports.hmsString_ = hmsString_;
exports.dateString_ = dateString_;
exports.round_ = round_;
exports.binarySearch = binarySearch;
exports.dateParser = dateParser;
exports.dateStrToMillis = dateStrToMillis;
exports.update = update;
exports.updateDeep = updateDeep;
exports.isArrayLike = isArrayLike;
exports.isDateLike = isDateLike;
exports.clone = clone;
exports.createCanvas = createCanvas;
exports.getContextPixelRatio = getContextPixelRatio;
exports.Iterator = Iterator;
exports.createIterator = createIterator;
exports.repeatAndCleanup = repeatAndCleanup;
exports.isPixelChangingOptionList = isPixelChangingOptionList;
exports.detectLineDelimiter = detectLineDelimiter;
exports.isNodeContainedBy = isNodeContainedBy;
exports.pow = pow;
exports.toRGB_ = toRGB_;
exports.isCanvasSupported = isCanvasSupported;
exports.parseFloat_ = parseFloat_;
exports.numberValueFormatter = numberValueFormatter;
exports.numberAxisLabelFormatter = numberAxisLabelFormatter;
exports.dateAxisLabelFormatter = dateAxisLabelFormatter;
exports.dateValueFormatter = dateValueFormatter;

function _interopRequireWildcard(obj) { if (obj && obj.__esModule) { return obj; } else { var newObj = {}; if (obj != null) { for (var key in obj) { if (Object.prototype.hasOwnProperty.call(obj, key)) newObj[key] = obj[key]; } } newObj["default"] = obj; return newObj; } }

var _dygraphTickers = require('./dygraph-tickers');

var DygraphTickers = _interopRequireWildcard(_dygraphTickers);

var LOG_SCALE = 10;
exports.LOG_SCALE = LOG_SCALE;
var LN_TEN = Math.log(LOG_SCALE);

exports.LN_TEN = LN_TEN;
/**
 * @private
 * @param {number} x
 * @return {number}
 */
var log10 = function log10(x) {
  return Math.log(x) / LN_TEN;
};

exports.log10 = log10;
/**
 * @private
 * @param {number} r0
 * @param {number} r1
 * @param {number} pct
 * @return {number}
 */
var logRangeFraction = function logRangeFraction(r0, r1, pct) {
  // Computing the inverse of toPercentXCoord. The function was arrived at with
  // the following steps:
  //
  // Original calcuation:
  // pct = (log(x) - log(xRange[0])) / (log(xRange[1]) - log(xRange[0])));
  //
  // Multiply both sides by the right-side denominator.
  // pct * (log(xRange[1] - log(xRange[0]))) = log(x) - log(xRange[0])
  //
  // add log(xRange[0]) to both sides
  // log(xRange[0]) + (pct * (log(xRange[1]) - log(xRange[0])) = log(x);
  //
  // Swap both sides of the equation,
  // log(x) = log(xRange[0]) + (pct * (log(xRange[1]) - log(xRange[0]))
  //
  // Use both sides as the exponent in 10^exp and we're done.
  // x = 10 ^ (log(xRange[0]) + (pct * (log(xRange[1]) - log(xRange[0])))

  var logr0 = log10(r0);
  var logr1 = log10(r1);
  var exponent = logr0 + pct * (logr1 - logr0);
  var value = Math.pow(LOG_SCALE, exponent);
  return value;
};

exports.logRangeFraction = logRangeFraction;
/** A dotted line stroke pattern. */
var DOTTED_LINE = [2, 2];
exports.DOTTED_LINE = DOTTED_LINE;
/** A dashed line stroke pattern. */
var DASHED_LINE = [7, 3];
exports.DASHED_LINE = DASHED_LINE;
/** A dot dash stroke pattern. */
var DOT_DASH_LINE = [7, 2, 2, 2];

exports.DOT_DASH_LINE = DOT_DASH_LINE;
// Directions for panning and zooming. Use bit operations when combined
// values are possible.
var HORIZONTAL = 1;
exports.HORIZONTAL = HORIZONTAL;
var VERTICAL = 2;

exports.VERTICAL = VERTICAL;
/**
 * Return the 2d context for a dygraph canvas.
 *
 * This method is only exposed for the sake of replacing the function in
 * automated tests.
 *
 * @param {!HTMLCanvasElement} canvas
 * @return {!CanvasRenderingContext2D}
 * @private
 */
var getContext = function getContext(canvas) {
  return (/** @type{!CanvasRenderingContext2D}*/canvas.getContext("2d")
  );
};

exports.getContext = getContext;
/**
 * Add an event handler.
 * @param {!Node} elem The element to add the event to.
 * @param {string} type The type of the event, e.g. 'click' or 'mousemove'.
 * @param {function(Event):(boolean|undefined)} fn The function to call
 *     on the event. The function takes one parameter: the event object.
 * @private
 */
var addEvent = function addEvent(elem, type, fn) {
  elem.addEventListener(type, fn, false);
};

exports.addEvent = addEvent;
/**
 * Remove an event handler.
 * @param {!Node} elem The element to remove the event from.
 * @param {string} type The type of the event, e.g. 'click' or 'mousemove'.
 * @param {function(Event):(boolean|undefined)} fn The function to call
 *     on the event. The function takes one parameter: the event object.
 */

function removeEvent(elem, type, fn) {
  elem.removeEventListener(type, fn, false);
}

;

/**
 * Cancels further processing of an event. This is useful to prevent default
 * browser actions, e.g. highlighting text on a double-click.
 * Based on the article at
 * http://www.switchonthecode.com/tutorials/javascript-tutorial-the-scroll-wheel
 * @param {!Event} e The event whose normal behavior should be canceled.
 * @private
 */

function cancelEvent(e) {
  e = e ? e : window.event;
  if (e.stopPropagation) {
    e.stopPropagation();
  }
  if (e.preventDefault) {
    e.preventDefault();
  }
  e.cancelBubble = true;
  e.cancel = true;
  e.returnValue = false;
  return false;
}

;

/**
 * Convert hsv values to an rgb(r,g,b) string. Taken from MochiKit.Color. This
 * is used to generate default series colors which are evenly spaced on the
 * color wheel.
 * @param { number } hue Range is 0.0-1.0.
 * @param { number } saturation Range is 0.0-1.0.
 * @param { number } value Range is 0.0-1.0.
 * @return { string } "rgb(r,g,b)" where r, g and b range from 0-255.
 * @private
 */

function hsvToRGB(hue, saturation, value) {
  var red;
  var green;
  var blue;
  if (saturation === 0) {
    red = value;
    green = value;
    blue = value;
  } else {
    var i = Math.floor(hue * 6);
    var f = hue * 6 - i;
    var p = value * (1 - saturation);
    var q = value * (1 - saturation * f);
    var t = value * (1 - saturation * (1 - f));
    switch (i) {
      case 1:
        red = q;green = value;blue = p;break;
      case 2:
        red = p;green = value;blue = t;break;
      case 3:
        red = p;green = q;blue = value;break;
      case 4:
        red = t;green = p;blue = value;break;
      case 5:
        red = value;green = p;blue = q;break;
      case 6: // fall through
      case 0:
        red = value;green = t;blue = p;break;
    }
  }
  red = Math.floor(255 * red + 0.5);
  green = Math.floor(255 * green + 0.5);
  blue = Math.floor(255 * blue + 0.5);
  return 'rgb(' + red + ',' + green + ',' + blue + ')';
}

;

/**
 * Find the coordinates of an object relative to the top left of the page.
 *
 * @param {Node} obj
 * @return {{x:number,y:number}}
 * @private
 */

function findPos(obj) {
  var p = obj.getBoundingClientRect(),
      w = window,
      d = document.documentElement;

  return {
    x: p.left + (w.pageXOffset || d.scrollLeft),
    y: p.top + (w.pageYOffset || d.scrollTop)
  };
}

;

/**
 * Returns the x-coordinate of the event in a coordinate system where the
 * top-left corner of the page (not the window) is (0,0).
 * Taken from MochiKit.Signal
 * @param {!Event} e
 * @return {number}
 * @private
 */

function pageX(e) {
  return !e.pageX || e.pageX < 0 ? 0 : e.pageX;
}

;

/**
 * Returns the y-coordinate of the event in a coordinate system where the
 * top-left corner of the page (not the window) is (0,0).
 * Taken from MochiKit.Signal
 * @param {!Event} e
 * @return {number}
 * @private
 */

function pageY(e) {
  return !e.pageY || e.pageY < 0 ? 0 : e.pageY;
}

;

/**
 * Converts page the x-coordinate of the event to pixel x-coordinates on the
 * canvas (i.e. DOM Coords).
 * @param {!Event} e Drag event.
 * @param {!DygraphInteractionContext} context Interaction context object.
 * @return {number} The amount by which the drag has moved to the right.
 */

function dragGetX_(e, context) {
  return pageX(e) - context.px;
}

;

/**
 * Converts page the y-coordinate of the event to pixel y-coordinates on the
 * canvas (i.e. DOM Coords).
 * @param {!Event} e Drag event.
 * @param {!DygraphInteractionContext} context Interaction context object.
 * @return {number} The amount by which the drag has moved down.
 */

function dragGetY_(e, context) {
  return pageY(e) - context.py;
}

;

/**
 * This returns true unless the parameter is 0, null, undefined or NaN.
 * TODO(danvk): rename this function to something like 'isNonZeroNan'.
 *
 * @param {number} x The number to consider.
 * @return {boolean} Whether the number is zero or NaN.
 * @private
 */

function isOK(x) {
  return !!x && !isNaN(x);
}

;

/**
 * @param {{x:?number,y:?number,yval:?number}} p The point to consider, valid
 *     points are {x, y} objects
 * @param {boolean=} opt_allowNaNY Treat point with y=NaN as valid
 * @return {boolean} Whether the point has numeric x and y.
 * @private
 */

function isValidPoint(p, opt_allowNaNY) {
  if (!p) return false; // null or undefined object
  if (p.yval === null) return false; // missing point
  if (p.x === null || p.x === undefined) return false;
  if (p.y === null || p.y === undefined) return false;
  if (isNaN(p.x) || !opt_allowNaNY && isNaN(p.y)) return false;
  return true;
}

;

/**
 * Number formatting function which mimics the behavior of %g in printf, i.e.
 * either exponential or fixed format (without trailing 0s) is used depending on
 * the length of the generated string.  The advantage of this format is that
 * there is a predictable upper bound on the resulting string length,
 * significant figures are not dropped, and normal numbers are not displayed in
 * exponential notation.
 *
 * NOTE: JavaScript's native toPrecision() is NOT a drop-in replacement for %g.
 * It creates strings which are too long for absolute values between 10^-4 and
 * 10^-6, e.g. '0.00001' instead of '1e-5'. See tests/number-format.html for
 * output examples.
 *
 * @param {number} x The number to format
 * @param {number=} opt_precision The precision to use, default 2.
 * @return {string} A string formatted like %g in printf.  The max generated
 *                  string length should be precision + 6 (e.g 1.123e+300).
 */

function floatFormat(x, opt_precision) {
  // Avoid invalid precision values; [1, 21] is the valid range.
  var p = Math.min(Math.max(1, opt_precision || 2), 21);

  // This is deceptively simple.  The actual algorithm comes from:
  //
  // Max allowed length = p + 4
  // where 4 comes from 'e+n' and '.'.
  //
  // Length of fixed format = 2 + y + p
  // where 2 comes from '0.' and y = # of leading zeroes.
  //
  // Equating the two and solving for y yields y = 2, or 0.00xxxx which is
  // 1.0e-3.
  //
  // Since the behavior of toPrecision() is identical for larger numbers, we
  // don't have to worry about the other bound.
  //
  // Finally, the argument for toExponential() is the number of trailing digits,
  // so we take off 1 for the value before the '.'.
  return Math.abs(x) < 1.0e-3 && x !== 0.0 ? x.toExponential(p - 1) : x.toPrecision(p);
}

;

/**
 * Converts '9' to '09' (useful for dates)
 * @param {number} x
 * @return {string}
 * @private
 */

function zeropad(x) {
  if (x < 10) return "0" + x;else return "" + x;
}

;

/**
 * Date accessors to get the parts of a calendar date (year, month,
 * day, hour, minute, second and millisecond) according to local time,
 * and factory method to call the Date constructor with an array of arguments.
 */
var DateAccessorsLocal = {
  getFullYear: function getFullYear(d) {
    return d.getFullYear();
  },
  getMonth: function getMonth(d) {
    return d.getMonth();
  },
  getDate: function getDate(d) {
    return d.getDate();
  },
  getHours: function getHours(d) {
    return d.getHours();
  },
  getMinutes: function getMinutes(d) {
    return d.getMinutes();
  },
  getSeconds: function getSeconds(d) {
    return d.getSeconds();
  },
  getMilliseconds: function getMilliseconds(d) {
    return d.getMilliseconds();
  },
  getDay: function getDay(d) {
    return d.getDay();
  },
  makeDate: function makeDate(y, m, d, hh, mm, ss, ms) {
    return new Date(y, m, d, hh, mm, ss, ms);
  }
};

exports.DateAccessorsLocal = DateAccessorsLocal;
/**
 * Date accessors to get the parts of a calendar date (year, month,
 * day of month, hour, minute, second and millisecond) according to UTC time,
 * and factory method to call the Date constructor with an array of arguments.
 */
var DateAccessorsUTC = {
  getFullYear: function getFullYear(d) {
    return d.getUTCFullYear();
  },
  getMonth: function getMonth(d) {
    return d.getUTCMonth();
  },
  getDate: function getDate(d) {
    return d.getUTCDate();
  },
  getHours: function getHours(d) {
    return d.getUTCHours();
  },
  getMinutes: function getMinutes(d) {
    return d.getUTCMinutes();
  },
  getSeconds: function getSeconds(d) {
    return d.getUTCSeconds();
  },
  getMilliseconds: function getMilliseconds(d) {
    return d.getUTCMilliseconds();
  },
  getDay: function getDay(d) {
    return d.getUTCDay();
  },
  makeDate: function makeDate(y, m, d, hh, mm, ss, ms) {
    return new Date(Date.UTC(y, m, d, hh, mm, ss, ms));
  }
};

exports.DateAccessorsUTC = DateAccessorsUTC;
/**
 * Return a string version of the hours, minutes and seconds portion of a date.
 * @param {number} hh The hours (from 0-23)
 * @param {number} mm The minutes (from 0-59)
 * @param {number} ss The seconds (from 0-59)
 * @return {string} A time of the form "HH:MM" or "HH:MM:SS"
 * @private
 */

function hmsString_(hh, mm, ss, ms) {
  var ret = zeropad(hh) + ":" + zeropad(mm);
  if (ss) {
    ret += ":" + zeropad(ss);
    if (ms) {
      var str = "" + ms;
      ret += "." + ('000' + str).substring(str.length);
    }
  }
  return ret;
}

;

/**
 * Convert a JS date (millis since epoch) to a formatted string.
 * @param {number} time The JavaScript time value (ms since epoch)
 * @param {boolean} utc Whether output UTC or local time
 * @return {string} A date of one of these forms:
 *     "YYYY/MM/DD", "YYYY/MM/DD HH:MM" or "YYYY/MM/DD HH:MM:SS"
 * @private
 */

function dateString_(time, utc) {
  var accessors = utc ? DateAccessorsUTC : DateAccessorsLocal;
  var date = new Date(time);
  var y = accessors.getFullYear(date);
  var m = accessors.getMonth(date);
  var d = accessors.getDate(date);
  var hh = accessors.getHours(date);
  var mm = accessors.getMinutes(date);
  var ss = accessors.getSeconds(date);
  var ms = accessors.getMilliseconds(date);
  // Get a year string:
  var year = "" + y;
  // Get a 0 padded month string
  var month = zeropad(m + 1); //months are 0-offset, sigh
  // Get a 0 padded day string
  var day = zeropad(d);
  var frac = hh * 3600 + mm * 60 + ss + 1e-3 * ms;
  var ret = year + "/" + month + "/" + day;
  if (frac) {
    ret += " " + hmsString_(hh, mm, ss, ms);
  }
  return ret;
}

;

/**
 * Round a number to the specified number of digits past the decimal point.
 * @param {number} num The number to round
 * @param {number} places The number of decimals to which to round
 * @return {number} The rounded number
 * @private
 */

function round_(num, places) {
  var shift = Math.pow(10, places);
  return Math.round(num * shift) / shift;
}

;

/**
 * Implementation of binary search over an array.
 * Currently does not work when val is outside the range of arry's values.
 * @param {number} val the value to search for
 * @param {Array.<number>} arry is the value over which to search
 * @param {number} abs If abs > 0, find the lowest entry greater than val
 *     If abs < 0, find the highest entry less than val.
 *     If abs == 0, find the entry that equals val.
 * @param {number=} low The first index in arry to consider (optional)
 * @param {number=} high The last index in arry to consider (optional)
 * @return {number} Index of the element, or -1 if it isn't found.
 * @private
 */

function binarySearch(_x, _x2, _x3, _x4, _x5) {
  var _again = true;

  _function: while (_again) {
    var val = _x,
        arry = _x2,
        abs = _x3,
        low = _x4,
        high = _x5;
    _again = false;

    if (low === null || low === undefined || high === null || high === undefined) {
      low = 0;
      high = arry.length - 1;
    }
    if (low > high) {
      return -1;
    }
    if (abs === null || abs === undefined) {
      abs = 0;
    }
    var validIndex = function validIndex(idx) {
      return idx >= 0 && idx < arry.length;
    };
    var mid = parseInt((low + high) / 2, 10);
    var element = arry[mid];
    var idx;
    if (element == val) {
      return mid;
    } else if (element > val) {
      if (abs > 0) {
        // Accept if element > val, but also if prior element < val.
        idx = mid - 1;
        if (validIndex(idx) && arry[idx] < val) {
          return mid;
        }
      }
      _x = val;
      _x2 = arry;
      _x3 = abs;
      _x4 = low;
      _x5 = mid - 1;
      _again = true;
      validIndex = mid = element = idx = undefined;
      continue _function;
    } else if (element < val) {
      if (abs < 0) {
        // Accept if element < val, but also if prior element > val.
        idx = mid + 1;
        if (validIndex(idx) && arry[idx] > val) {
          return mid;
        }
      }
      _x = val;
      _x2 = arry;
      _x3 = abs;
      _x4 = mid + 1;
      _x5 = high;
      _again = true;
      validIndex = mid = element = idx = undefined;
      continue _function;
    }
    return -1; // can't actually happen, but makes closure compiler happy
  }
}

;

/**
 * Parses a date, returning the number of milliseconds since epoch. This can be
 * passed in as an xValueParser in the Dygraph constructor.
 * TODO(danvk): enumerate formats that this understands.
 *
 * @param {string} dateStr A date in a variety of possible string formats.
 * @return {number} Milliseconds since epoch.
 * @private
 */

function dateParser(dateStr) {
  var dateStrSlashed;
  var d;

  // Let the system try the format first, with one caveat:
  // YYYY-MM-DD[ HH:MM:SS] is interpreted as UTC by a variety of browsers.
  // dygraphs displays dates in local time, so this will result in surprising
  // inconsistencies. But if you specify "T" or "Z" (i.e. YYYY-MM-DDTHH:MM:SS),
  // then you probably know what you're doing, so we'll let you go ahead.
  // Issue: http://code.google.com/p/dygraphs/issues/detail?id=255
  if (dateStr.search("-") == -1 || dateStr.search("T") != -1 || dateStr.search("Z") != -1) {
    d = dateStrToMillis(dateStr);
    if (d && !isNaN(d)) return d;
  }

  if (dateStr.search("-") != -1) {
    // e.g. '2009-7-12' or '2009-07-12'
    dateStrSlashed = dateStr.replace("-", "/", "g");
    while (dateStrSlashed.search("-") != -1) {
      dateStrSlashed = dateStrSlashed.replace("-", "/");
    }
    d = dateStrToMillis(dateStrSlashed);
  } else if (dateStr.length == 8) {
    // e.g. '20090712'
    // TODO(danvk): remove support for this format. It's confusing.
    dateStrSlashed = dateStr.substr(0, 4) + "/" + dateStr.substr(4, 2) + "/" + dateStr.substr(6, 2);
    d = dateStrToMillis(dateStrSlashed);
  } else {
    // Any format that Date.parse will accept, e.g. "2009/07/12" or
    // "2009/07/12 12:34:56"
    d = dateStrToMillis(dateStr);
  }

  if (!d || isNaN(d)) {
    console.error("Couldn't parse " + dateStr + " as a date");
  }
  return d;
}

;

/**
 * This is identical to JavaScript's built-in Date.parse() method, except that
 * it doesn't get replaced with an incompatible method by aggressive JS
 * libraries like MooTools or Joomla.
 * @param {string} str The date string, e.g. "2011/05/06"
 * @return {number} millis since epoch
 * @private
 */

function dateStrToMillis(str) {
  return new Date(str).getTime();
}

;

// These functions are all based on MochiKit.
/**
 * Copies all the properties from o to self.
 *
 * @param {!Object} self
 * @param {!Object} o
 * @return {!Object}
 */

function update(self, o) {
  if (typeof o != 'undefined' && o !== null) {
    for (var k in o) {
      if (o.hasOwnProperty(k)) {
        self[k] = o[k];
      }
    }
  }
  return self;
}

;

/**
 * Copies all the properties from o to self.
 *
 * @param {!Object} self
 * @param {!Object} o
 * @return {!Object}
 * @private
 */

function updateDeep(self, o) {
  // Taken from http://stackoverflow.com/questions/384286/javascript-isdom-how-do-you-check-if-a-javascript-object-is-a-dom-object
  function isNode(o) {
    return typeof Node === "object" ? o instanceof Node : typeof o === "object" && typeof o.nodeType === "number" && typeof o.nodeName === "string";
  }

  if (typeof o != 'undefined' && o !== null) {
    for (var k in o) {
      if (o.hasOwnProperty(k)) {
        if (o[k] === null) {
          self[k] = null;
        } else if (isArrayLike(o[k])) {
          self[k] = o[k].slice();
        } else if (isNode(o[k])) {
          // DOM objects are shallowly-copied.
          self[k] = o[k];
        } else if (typeof o[k] == 'object') {
          if (typeof self[k] != 'object' || self[k] === null) {
            self[k] = {};
          }
          updateDeep(self[k], o[k]);
        } else {
          self[k] = o[k];
        }
      }
    }
  }
  return self;
}

;

/**
 * @param {*} o
 * @return {boolean}
 * @private
 */

function isArrayLike(o) {
  var typ = typeof o;
  if (typ != 'object' && !(typ == 'function' && typeof o.item == 'function') || o === null || typeof o.length != 'number' || o.nodeType === 3) {
    return false;
  }
  return true;
}

;

/**
 * @param {Object} o
 * @return {boolean}
 * @private
 */

function isDateLike(o) {
  if (typeof o != "object" || o === null || typeof o.getTime != 'function') {
    return false;
  }
  return true;
}

;

/**
 * Note: this only seems to work for arrays.
 * @param {!Array} o
 * @return {!Array}
 * @private
 */

function clone(o) {
  // TODO(danvk): figure out how MochiKit's version works
  var r = [];
  for (var i = 0; i < o.length; i++) {
    if (isArrayLike(o[i])) {
      r.push(clone(o[i]));
    } else {
      r.push(o[i]);
    }
  }
  return r;
}

;

/**
 * Create a new canvas element.
 *
 * @return {!HTMLCanvasElement}
 * @private
 */

function createCanvas() {
  return document.createElement('canvas');
}

;

/**
 * Returns the context's pixel ratio, which is the ratio between the device
 * pixel ratio and the backing store ratio. Typically this is 1 for conventional
 * displays, and > 1 for HiDPI displays (such as the Retina MBP).
 * See http://www.html5rocks.com/en/tutorials/canvas/hidpi/ for more details.
 *
 * @param {!CanvasRenderingContext2D} context The canvas's 2d context.
 * @return {number} The ratio of the device pixel ratio and the backing store
 * ratio for the specified context.
 */

function getContextPixelRatio(context) {
  try {
    var devicePixelRatio = window.devicePixelRatio;
    var backingStoreRatio = context.webkitBackingStorePixelRatio || context.mozBackingStorePixelRatio || context.msBackingStorePixelRatio || context.oBackingStorePixelRatio || context.backingStorePixelRatio || 1;
    if (devicePixelRatio !== undefined) {
      return devicePixelRatio / backingStoreRatio;
    } else {
      // At least devicePixelRatio must be defined for this ratio to make sense.
      // We default backingStoreRatio to 1: this does not exist on some browsers
      // (i.e. desktop Chrome).
      return 1;
    }
  } catch (e) {
    return 1;
  }
}

;

/**
 * TODO(danvk): use @template here when it's better supported for classes.
 * @param {!Array} array
 * @param {number} start
 * @param {number} length
 * @param {function(!Array,?):boolean=} predicate
 * @constructor
 */

function Iterator(array, start, length, predicate) {
  start = start || 0;
  length = length || array.length;
  this.hasNext = true; // Use to identify if there's another element.
  this.peek = null; // Use for look-ahead
  this.start_ = start;
  this.array_ = array;
  this.predicate_ = predicate;
  this.end_ = Math.min(array.length, start + length);
  this.nextIdx_ = start - 1; // use -1 so initial advance works.
  this.next(); // ignoring result.
}

;

/**
 * @return {Object}
 */
Iterator.prototype.next = function () {
  if (!this.hasNext) {
    return null;
  }
  var obj = this.peek;

  var nextIdx = this.nextIdx_ + 1;
  var found = false;
  while (nextIdx < this.end_) {
    if (!this.predicate_ || this.predicate_(this.array_, nextIdx)) {
      this.peek = this.array_[nextIdx];
      found = true;
      break;
    }
    nextIdx++;
  }
  this.nextIdx_ = nextIdx;
  if (!found) {
    this.hasNext = false;
    this.peek = null;
  }
  return obj;
};

/**
 * Returns a new iterator over array, between indexes start and
 * start + length, and only returns entries that pass the accept function
 *
 * @param {!Array} array the array to iterate over.
 * @param {number} start the first index to iterate over, 0 if absent.
 * @param {number} length the number of elements in the array to iterate over.
 *     This, along with start, defines a slice of the array, and so length
 *     doesn't imply the number of elements in the iterator when accept doesn't
 *     always accept all values. array.length when absent.
 * @param {function(?):boolean=} opt_predicate a function that takes
 *     parameters array and idx, which returns true when the element should be
 *     returned.  If omitted, all elements are accepted.
 * @private
 */

function createIterator(array, start, length, opt_predicate) {
  return new Iterator(array, start, length, opt_predicate);
}

;

// Shim layer with setTimeout fallback.
// From: http://paulirish.com/2011/requestanimationframe-for-smart-animating/
// Should be called with the window context:
//   Dygraph.requestAnimFrame.call(window, function() {})
var requestAnimFrame = (function () {
  return window.requestAnimationFrame || window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame || window.oRequestAnimationFrame || window.msRequestAnimationFrame || function (callback) {
    window.setTimeout(callback, 1000 / 60);
  };
})();

exports.requestAnimFrame = requestAnimFrame;
/**
 * Call a function at most maxFrames times at an attempted interval of
 * framePeriodInMillis, then call a cleanup function once. repeatFn is called
 * once immediately, then at most (maxFrames - 1) times asynchronously. If
 * maxFrames==1, then cleanup_fn() is also called synchronously.  This function
 * is used to sequence animation.
 * @param {function(number)} repeatFn Called repeatedly -- takes the frame
 *     number (from 0 to maxFrames-1) as an argument.
 * @param {number} maxFrames The max number of times to call repeatFn
 * @param {number} framePeriodInMillis Max requested time between frames.
 * @param {function()} cleanupFn A function to call after all repeatFn calls.
 * @private
 */

function repeatAndCleanup(repeatFn, maxFrames, framePeriodInMillis, cleanupFn) {
  var frameNumber = 0;
  var previousFrameNumber;
  var startTime = new Date().getTime();
  repeatFn(frameNumber);
  if (maxFrames == 1) {
    cleanupFn();
    return;
  }
  var maxFrameArg = maxFrames - 1;

  (function loop() {
    if (frameNumber >= maxFrames) return;
    requestAnimFrame.call(window, function () {
      // Determine which frame to draw based on the delay so far.  Will skip
      // frames if necessary.
      var currentTime = new Date().getTime();
      var delayInMillis = currentTime - startTime;
      previousFrameNumber = frameNumber;
      frameNumber = Math.floor(delayInMillis / framePeriodInMillis);
      var frameDelta = frameNumber - previousFrameNumber;
      // If we predict that the subsequent repeatFn call will overshoot our
      // total frame target, so our last call will cause a stutter, then jump to
      // the last call immediately.  If we're going to cause a stutter, better
      // to do it faster than slower.
      var predictOvershootStutter = frameNumber + frameDelta > maxFrameArg;
      if (predictOvershootStutter || frameNumber >= maxFrameArg) {
        repeatFn(maxFrameArg); // Ensure final call with maxFrameArg.
        cleanupFn();
      } else {
        if (frameDelta !== 0) {
          // Don't call repeatFn with duplicate frames.
          repeatFn(frameNumber);
        }
        loop();
      }
    });
  })();
}

;

// A whitelist of options that do not change pixel positions.
var pixelSafeOptions = {
  'annotationClickHandler': true,
  'annotationDblClickHandler': true,
  'annotationMouseOutHandler': true,
  'annotationMouseOverHandler': true,
  'axisLineColor': true,
  'axisLineWidth': true,
  'clickCallback': true,
  'drawCallback': true,
  'drawHighlightPointCallback': true,
  'drawPoints': true,
  'drawPointCallback': true,
  'drawGrid': true,
  'fillAlpha': true,
  'gridLineColor': true,
  'gridLineWidth': true,
  'hideOverlayOnMouseOut': true,
  'highlightCallback': true,
  'highlightCircleSize': true,
  'interactionModel': true,
  'labelsDiv': true,
  'labelsKMB': true,
  'labelsKMG2': true,
  'labelsSeparateLines': true,
  'labelsShowZeroValues': true,
  'legend': true,
  'panEdgeFraction': true,
  'pixelsPerYLabel': true,
  'pointClickCallback': true,
  'pointSize': true,
  'rangeSelectorPlotFillColor': true,
  'rangeSelectorPlotFillGradientColor': true,
  'rangeSelectorPlotStrokeColor': true,
  'rangeSelectorBackgroundStrokeColor': true,
  'rangeSelectorBackgroundLineWidth': true,
  'rangeSelectorPlotLineWidth': true,
  'rangeSelectorForegroundStrokeColor': true,
  'rangeSelectorForegroundLineWidth': true,
  'rangeSelectorAlpha': true,
  'showLabelsOnHighlight': true,
  'showRoller': true,
  'strokeWidth': true,
  'underlayCallback': true,
  'unhighlightCallback': true,
  'zoomCallback': true
};

/**
 * This function will scan the option list and determine if they
 * require us to recalculate the pixel positions of each point.
 * TODO: move this into dygraph-options.js
 * @param {!Array.<string>} labels a list of options to check.
 * @param {!Object} attrs
 * @return {boolean} true if the graph needs new points else false.
 * @private
 */

function isPixelChangingOptionList(labels, attrs) {
  // Assume that we do not require new points.
  // This will change to true if we actually do need new points.

  // Create a dictionary of series names for faster lookup.
  // If there are no labels, then the dictionary stays empty.
  var seriesNamesDictionary = {};
  if (labels) {
    for (var i = 1; i < labels.length; i++) {
      seriesNamesDictionary[labels[i]] = true;
    }
  }

  // Scan through a flat (i.e. non-nested) object of options.
  // Returns true/false depending on whether new points are needed.
  var scanFlatOptions = function scanFlatOptions(options) {
    for (var property in options) {
      if (options.hasOwnProperty(property) && !pixelSafeOptions[property]) {
        return true;
      }
    }
    return false;
  };

  // Iterate through the list of updated options.
  for (var property in attrs) {
    if (!attrs.hasOwnProperty(property)) continue;

    // Find out of this field is actually a series specific options list.
    if (property == 'highlightSeriesOpts' || seriesNamesDictionary[property] && !attrs.series) {
      // This property value is a list of options for this series.
      if (scanFlatOptions(attrs[property])) return true;
    } else if (property == 'series' || property == 'axes') {
      // This is twice-nested options list.
      var perSeries = attrs[property];
      for (var series in perSeries) {
        if (perSeries.hasOwnProperty(series) && scanFlatOptions(perSeries[series])) {
          return true;
        }
      }
    } else {
      // If this was not a series specific option list, check if it's a pixel
      // changing property.
      if (!pixelSafeOptions[property]) return true;
    }
  }

  return false;
}

;

var Circles = {
  DEFAULT: function DEFAULT(g, name, ctx, canvasx, canvasy, color, radius) {
    ctx.beginPath();
    ctx.fillStyle = color;
    ctx.arc(canvasx, canvasy, radius, 0, 2 * Math.PI, false);
    ctx.fill();
  }
  // For more shapes, include extras/shapes.js
};

exports.Circles = Circles;
/**
 * Determine whether |data| is delimited by CR, CRLF, LF, LFCR.
 * @param {string} data
 * @return {?string} the delimiter that was detected (or null on failure).
 */

function detectLineDelimiter(data) {
  for (var i = 0; i < data.length; i++) {
    var code = data.charAt(i);
    if (code === '\\r') {
      // Might actually be "\\r\\n".
      if (i + 1 < data.length && data.charAt(i + 1) === '\\n') {
        return '\\r\\n';
      }
      return code;
    }
    if (code === '\\n') {
      // Might actually be "\\n\\r".
      if (i + 1 < data.length && data.charAt(i + 1) === '\\r') {
        return '\\n\\r';
      }
      return code;
    }
  }

  return null;
}

;

/**
 * Is one node contained by another?
 * @param {Node} containee The contained node.
 * @param {Node} container The container node.
 * @return {boolean} Whether containee is inside (or equal to) container.
 * @private
 */

function isNodeContainedBy(containee, container) {
  if (container === null || containee === null) {
    return false;
  }
  var containeeNode = /** @type {Node} */containee;
  while (containeeNode && containeeNode !== container) {
    containeeNode = containeeNode.parentNode;
  }
  return containeeNode === container;
}

;

// This masks some numeric issues in older versions of Firefox,
// where 1.0/Math.pow(10,2) != Math.pow(10,-2).
/** @type {function(number,number):number} */

function pow(base, exp) {
  if (exp < 0) {
    return 1.0 / Math.pow(base, -exp);
  }
  return Math.pow(base, exp);
}

;

var RGBA_RE = /^rgba?\((\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})(?:,\s*([01](?:\.\d+)?))?\)$/;

/**
 * Helper for toRGB_ which parses strings of the form:
 * rgb(123, 45, 67)
 * rgba(123, 45, 67, 0.5)
 * @return parsed {r,g,b,a?} tuple or null.
 */
function parseRGBA(rgbStr) {
  var bits = RGBA_RE.exec(rgbStr);
  if (!bits) return null;
  var r = parseInt(bits[1], 10),
      g = parseInt(bits[2], 10),
      b = parseInt(bits[3], 10);
  if (bits[4]) {
    return { r: r, g: g, b: b, a: parseFloat(bits[4]) };
  } else {
    return { r: r, g: g, b: b };
  }
}

/**
 * Converts any valid CSS color (hex, rgb(), named color) to an RGB tuple.
 *
 * @param {!string} colorStr Any valid CSS color string.
 * @return {{r:number,g:number,b:number,a:number?}} Parsed RGB tuple.
 * @private
 */

function toRGB_(colorStr) {
  // Strategy: First try to parse colorStr directly. This is fast & avoids DOM
  // manipulation.  If that fails (e.g. for named colors like 'red'), then
  // create a hidden DOM element and parse its computed color.
  var rgb = parseRGBA(colorStr);
  if (rgb) return rgb;

  var div = document.createElement('div');
  div.style.backgroundColor = colorStr;
  div.style.visibility = 'hidden';
  document.body.appendChild(div);
  var rgbStr = window.getComputedStyle(div, null).backgroundColor;
  document.body.removeChild(div);
  return parseRGBA(rgbStr);
}

;

/**
 * Checks whether the browser supports the &lt;canvas&gt; tag.
 * @param {HTMLCanvasElement=} opt_canvasElement Pass a canvas element as an
 *     optimization if you have one.
 * @return {boolean} Whether the browser supports canvas.
 */

function isCanvasSupported(opt_canvasElement) {
  try {
    var canvas = opt_canvasElement || document.createElement("canvas");
    canvas.getContext("2d");
  } catch (e) {
    return false;
  }
  return true;
}

;

/**
 * Parses the value as a floating point number. This is like the parseFloat()
 * built-in, but with a few differences:
 * - the empty string is parsed as null, rather than NaN.
 * - if the string cannot be parsed at all, an error is logged.
 * If the string can't be parsed, this method returns null.
 * @param {string} x The string to be parsed
 * @param {number=} opt_line_no The line number from which the string comes.
 * @param {string=} opt_line The text of the line from which the string comes.
 */

function parseFloat_(x, opt_line_no, opt_line) {
  var val = parseFloat(x);
  if (!isNaN(val)) return val;

  // Try to figure out what happeend.
  // If the value is the empty string, parse it as null.
  if (/^ *$/.test(x)) return null;

  // If it was actually "NaN", return it as NaN.
  if (/^ *nan *$/i.test(x)) return NaN;

  // Looks like a parsing error.
  var msg = "Unable to parse '" + x + "' as a number";
  if (opt_line !== undefined && opt_line_no !== undefined) {
    msg += " on line " + (1 + (opt_line_no || 0)) + " ('" + opt_line + "') of CSV.";
  }
  console.error(msg);

  return null;
}

;

// Label constants for the labelsKMB and labelsKMG2 options.
// (i.e. '100000' -> '100K')
var KMB_LABELS = ['K', 'M', 'B', 'T', 'Q'];
var KMG2_BIG_LABELS = ['k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y'];
var KMG2_SMALL_LABELS = ['m', 'u', 'n', 'p', 'f', 'a', 'z', 'y'];

/**
 * @private
 * Return a string version of a number. This respects the digitsAfterDecimal
 * and maxNumberWidth options.
 * @param {number} x The number to be formatted
 * @param {Dygraph} opts An options view
 */

function numberValueFormatter(x, opts) {
  var sigFigs = opts('sigFigs');

  if (sigFigs !== null) {
    // User has opted for a fixed number of significant figures.
    return floatFormat(x, sigFigs);
  }

  var digits = opts('digitsAfterDecimal');
  var maxNumberWidth = opts('maxNumberWidth');

  var kmb = opts('labelsKMB');
  var kmg2 = opts('labelsKMG2');

  var label;

  // switch to scientific notation if we underflow or overflow fixed display.
  if (x !== 0.0 && (Math.abs(x) >= Math.pow(10, maxNumberWidth) || Math.abs(x) < Math.pow(10, -digits))) {
    label = x.toExponential(digits);
  } else {
    label = '' + round_(x, digits);
  }

  if (kmb || kmg2) {
    var k;
    var k_labels = [];
    var m_labels = [];
    if (kmb) {
      k = 1000;
      k_labels = KMB_LABELS;
    }
    if (kmg2) {
      if (kmb) console.warn("Setting both labelsKMB and labelsKMG2. Pick one!");
      k = 1024;
      k_labels = KMG2_BIG_LABELS;
      m_labels = KMG2_SMALL_LABELS;
    }

    var absx = Math.abs(x);
    var n = pow(k, k_labels.length);
    for (var j = k_labels.length - 1; j >= 0; j--, n /= k) {
      if (absx >= n) {
        label = round_(x / n, digits) + k_labels[j];
        break;
      }
    }
    if (kmg2) {
      // TODO(danvk): clean up this logic. Why so different than kmb?
      var x_parts = String(x.toExponential()).split('e-');
      if (x_parts.length === 2 && x_parts[1] >= 3 && x_parts[1] <= 24) {
        if (x_parts[1] % 3 > 0) {
          label = round_(x_parts[0] / pow(10, x_parts[1] % 3), digits);
        } else {
          label = Number(x_parts[0]).toFixed(2);
        }
        label += m_labels[Math.floor(x_parts[1] / 3) - 1];
      }
    }
  }

  return label;
}

;

/**
 * variant for use as an axisLabelFormatter.
 * @private
 */

function numberAxisLabelFormatter(x, granularity, opts) {
  return numberValueFormatter.call(this, x, opts);
}

;

/**
 * @type {!Array.<string>}
 * @private
 * @constant
 */
var SHORT_MONTH_NAMES_ = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

/**
 * Convert a JS date to a string appropriate to display on an axis that
 * is displaying values at the stated granularity. This respects the
 * labelsUTC option.
 * @param {Date} date The date to format
 * @param {number} granularity One of the Dygraph granularity constants
 * @param {Dygraph} opts An options view
 * @return {string} The date formatted as local time
 * @private
 */

function dateAxisLabelFormatter(date, granularity, opts) {
  var utc = opts('labelsUTC');
  var accessors = utc ? DateAccessorsUTC : DateAccessorsLocal;

  var year = accessors.getFullYear(date),
      month = accessors.getMonth(date),
      day = accessors.getDate(date),
      hours = accessors.getHours(date),
      mins = accessors.getMinutes(date),
      secs = accessors.getSeconds(date),
      millis = accessors.getMilliseconds(date);

  if (granularity >= DygraphTickers.Granularity.DECADAL) {
    return '' + year;
  } else if (granularity >= DygraphTickers.Granularity.MONTHLY) {
    return SHORT_MONTH_NAMES_[month] + '&#160;' + year;
  } else {
    var frac = hours * 3600 + mins * 60 + secs + 1e-3 * millis;
    if (frac === 0 || granularity >= DygraphTickers.Granularity.DAILY) {
      // e.g. '21 Jan' (%d%b)
      return zeropad(day) + '&#160;' + SHORT_MONTH_NAMES_[month];
    } else if (granularity < DygraphTickers.Granularity.SECONDLY) {
      // e.g. 40.310 (meaning 40 seconds and 310 milliseconds)
      var str = "" + millis;
      return zeropad(secs) + "." + ('000' + str).substring(str.length);
    } else if (granularity > DygraphTickers.Granularity.MINUTELY) {
      return hmsString_(hours, mins, secs, 0);
    } else {
      return hmsString_(hours, mins, secs, millis);
    }
  }
}

;
// alias in case anyone is referencing the old method.
// Dygraph.dateAxisFormatter = Dygraph.dateAxisLabelFormatter;

/**
 * Return a string version of a JS date for a value label. This respects the
 * labelsUTC option.
 * @param {Date} date The date to be formatted
 * @param {Dygraph} opts An options view
 * @private
 */

function dateValueFormatter(d, opts) {
  return dateString_(d, opts('labelsUTC'));
}

;

},{"./dygraph-tickers":16}],18:[function(require,module,exports){
(function (process){
/**
 * @license
 * Copyright 2006 Dan Vanderkam (danvdk@gmail.com)
 * MIT-licensed (http://opensource.org/licenses/MIT)
 */ /**
 * @fileoverview Creates an interactive, zoomable graph based on a CSV file or
 * string. Dygraph can handle multiple series with or without error bars. The
 * date/value ranges will be automatically set. Dygraph uses the
 * &lt;canvas&gt; tag, so it only works in FF1.5+.
 * @author danvdk@gmail.com (Dan Vanderkam)

  Usage:
   <div id="graphdiv" style="width:800px; height:500px;"></div>
   script type="text/javascript">
     new Dygraph(document.getElementById("graphdiv"),
                 "datafile.csv",  // CSV file with headers
                 { }); // options
   /script>

 The CSV file is of the form

   Date,SeriesA,SeriesB,SeriesC
   YYYYMMDD,A1,B1,C1
   YYYYMMDD,A2,B2,C2

 If the 'errorBars' option is set in the constructor, the input should be of
 the form
   Date,SeriesA,SeriesB,...
   YYYYMMDD,A1,sigmaA1,B1,sigmaB1,...
   YYYYMMDD,A2,sigmaA2,B2,sigmaB2,...

 If the 'fractions' option is set, the input should be of the form:

   Date,SeriesA,SeriesB,...
   YYYYMMDD,A1/B1,A2/B2,...
   YYYYMMDD,A1/B1,A2/B2,...

 And error bars will be calculated automatically using a binomial distribution.

 For further documentation and examples, see http://dygraphs.com/
 */'use strict';Object.defineProperty(exports,'__esModule',{value:true});var _slicedToArray=(function(){function sliceIterator(arr,i){var _arr=[];var _n=true;var _d=false;var _e=undefined;try{for(var _i=arr[Symbol.iterator](),_s;!(_n = (_s = _i.next()).done);_n = true) {_arr.push(_s.value);if(i && _arr.length === i)break;}}catch(err) {_d = true;_e = err;}finally {try{if(!_n && _i['return'])_i['return']();}finally {if(_d)throw _e;}}return _arr;}return function(arr,i){if(Array.isArray(arr)){return arr;}else if(Symbol.iterator in Object(arr)){return sliceIterator(arr,i);}else {throw new TypeError('Invalid attempt to destructure non-iterable instance');}};})();function _interopRequireWildcard(obj){if(obj && obj.__esModule){return obj;}else {var newObj={};if(obj != null){for(var key in obj) {if(Object.prototype.hasOwnProperty.call(obj,key))newObj[key] = obj[key];}}newObj['default'] = obj;return newObj;}}function _interopRequireDefault(obj){return obj && obj.__esModule?obj:{'default':obj};}var _dygraphLayout=require('./dygraph-layout');var _dygraphLayout2=_interopRequireDefault(_dygraphLayout);var _dygraphCanvas=require('./dygraph-canvas');var _dygraphCanvas2=_interopRequireDefault(_dygraphCanvas);var _dygraphOptions=require('./dygraph-options');var _dygraphOptions2=_interopRequireDefault(_dygraphOptions);var _dygraphInteractionModel=require('./dygraph-interaction-model');var _dygraphInteractionModel2=_interopRequireDefault(_dygraphInteractionModel);var _dygraphTickers=require('./dygraph-tickers');var DygraphTickers=_interopRequireWildcard(_dygraphTickers);var _dygraphUtils=require('./dygraph-utils');var utils=_interopRequireWildcard(_dygraphUtils);var _dygraphDefaultAttrs=require('./dygraph-default-attrs');var _dygraphDefaultAttrs2=_interopRequireDefault(_dygraphDefaultAttrs);var _dygraphOptionsReference=require('./dygraph-options-reference');var _dygraphOptionsReference2=_interopRequireDefault(_dygraphOptionsReference);var _iframeTarp=require('./iframe-tarp');var _iframeTarp2=_interopRequireDefault(_iframeTarp);var _datahandlerDefault=require('./datahandler/default');var _datahandlerDefault2=_interopRequireDefault(_datahandlerDefault);var _datahandlerBarsError=require('./datahandler/bars-error');var _datahandlerBarsError2=_interopRequireDefault(_datahandlerBarsError);var _datahandlerBarsCustom=require('./datahandler/bars-custom');var _datahandlerBarsCustom2=_interopRequireDefault(_datahandlerBarsCustom);var _datahandlerDefaultFractions=require('./datahandler/default-fractions');var _datahandlerDefaultFractions2=_interopRequireDefault(_datahandlerDefaultFractions);var _datahandlerBarsFractions=require('./datahandler/bars-fractions');var _datahandlerBarsFractions2=_interopRequireDefault(_datahandlerBarsFractions);var _datahandlerBars=require('./datahandler/bars');var _datahandlerBars2=_interopRequireDefault(_datahandlerBars);var _pluginsAnnotations=require('./plugins/annotations');var _pluginsAnnotations2=_interopRequireDefault(_pluginsAnnotations);var _pluginsAxes=require('./plugins/axes');var _pluginsAxes2=_interopRequireDefault(_pluginsAxes);var _pluginsChartLabels=require('./plugins/chart-labels');var _pluginsChartLabels2=_interopRequireDefault(_pluginsChartLabels);var _pluginsGrid=require('./plugins/grid');var _pluginsGrid2=_interopRequireDefault(_pluginsGrid);var _pluginsLegend=require('./plugins/legend');var _pluginsLegend2=_interopRequireDefault(_pluginsLegend);var _pluginsRangeSelector=require('./plugins/range-selector');var _pluginsRangeSelector2=_interopRequireDefault(_pluginsRangeSelector);var _dygraphGviz=require('./dygraph-gviz');var _dygraphGviz2=_interopRequireDefault(_dygraphGviz);"use strict"; /**
 * Creates an interactive, zoomable chart.
 *
 * @constructor
 * @param {div | String} div A div or the id of a div into which to construct
 * the chart.
 * @param {String | Function} file A file containing CSV data or a function
 * that returns this data. The most basic expected format for each line is
 * "YYYY/MM/DD,val1,val2,...". For more information, see
 * http://dygraphs.com/data.html.
 * @param {Object} attrs Various other attributes, e.g. errorBars determines
 * whether the input data contains error ranges. For a complete list of
 * options, see http://dygraphs.com/options.html.
 */var Dygraph=function Dygraph(div,data,opts){this.__init__(div,data,opts);};Dygraph.NAME = "Dygraph";Dygraph.VERSION = "2.0.0"; // Various default values
Dygraph.DEFAULT_ROLL_PERIOD = 1;Dygraph.DEFAULT_WIDTH = 480;Dygraph.DEFAULT_HEIGHT = 320; // For max 60 Hz. animation:
Dygraph.ANIMATION_STEPS = 12;Dygraph.ANIMATION_DURATION = 200; /**
 * Standard plotters. These may be used by clients.
 * Available plotters are:
 * - Dygraph.Plotters.linePlotter: draws central lines (most common)
 * - Dygraph.Plotters.errorPlotter: draws error bars
 * - Dygraph.Plotters.fillPlotter: draws fills under lines (used with fillGraph)
 *
 * By default, the plotter is [fillPlotter, errorPlotter, linePlotter].
 * This causes all the lines to be drawn over all the fills/error bars.
 */Dygraph.Plotters = _dygraphCanvas2['default']._Plotters; // Used for initializing annotation CSS rules only once.
Dygraph.addedAnnotationCSS = false; /**
 * Initializes the Dygraph. This creates a new DIV and constructs the PlotKit
 * and context &lt;canvas&gt; inside of it. See the constructor for details.
 * on the parameters.
 * @param {Element} div the Element to render the graph into.
 * @param {string | Function} file Source data
 * @param {Object} attrs Miscellaneous other options
 * @private
 */Dygraph.prototype.__init__ = function(div,file,attrs){this.is_initial_draw_ = true;this.readyFns_ = []; // Support two-argument constructor
if(attrs === null || attrs === undefined){attrs = {};}attrs = Dygraph.copyUserAttrs_(attrs);if(typeof div == 'string'){div = document.getElementById(div);}if(!div){throw new Error('Constructing dygraph with a non-existent div!');} // Copy the important bits into the object
// TODO(danvk): most of these should just stay in the attrs_ dictionary.
this.maindiv_ = div;this.file_ = file;this.rollPeriod_ = attrs.rollPeriod || Dygraph.DEFAULT_ROLL_PERIOD;this.previousVerticalX_ = -1;this.fractions_ = attrs.fractions || false;this.dateWindow_ = attrs.dateWindow || null;this.annotations_ = []; // Clear the div. This ensure that, if multiple dygraphs are passed the same
// div, then only one will be drawn.
div.innerHTML = ""; // For historical reasons, the 'width' and 'height' options trump all CSS
// rules _except_ for an explicit 'width' or 'height' on the div.
// As an added convenience, if the div has zero height (like <div></div> does
// without any styles), then we use a default height/width.
if(div.style.width === '' && attrs.width){div.style.width = attrs.width + "px";}if(div.style.height === '' && attrs.height){div.style.height = attrs.height + "px";}if(div.style.height === '' && div.clientHeight === 0){div.style.height = Dygraph.DEFAULT_HEIGHT + "px";if(div.style.width === ''){div.style.width = Dygraph.DEFAULT_WIDTH + "px";}} // These will be zero if the dygraph's div is hidden. In that case,
// use the user-specified attributes if present. If not, use zero
// and assume the user will call resize to fix things later.
this.width_ = div.clientWidth || attrs.width || 0;this.height_ = div.clientHeight || attrs.height || 0; // TODO(danvk): set fillGraph to be part of attrs_ here, not user_attrs_.
if(attrs.stackedGraph){attrs.fillGraph = true; // TODO(nikhilk): Add any other stackedGraph checks here.
} // DEPRECATION WARNING: All option processing should be moved from
// attrs_ and user_attrs_ to options_, which holds all this information.
//
// Dygraphs has many options, some of which interact with one another.
// To keep track of everything, we maintain two sets of options:
//
//  this.user_attrs_   only options explicitly set by the user.
//  this.attrs_        defaults, options derived from user_attrs_, data.
//
// Options are then accessed this.attr_('attr'), which first looks at
// user_attrs_ and then computed attrs_. This way Dygraphs can set intelligent
// defaults without overriding behavior that the user specifically asks for.
this.user_attrs_ = {};utils.update(this.user_attrs_,attrs); // This sequence ensures that Dygraph.DEFAULT_ATTRS is never modified.
this.attrs_ = {};utils.updateDeep(this.attrs_,_dygraphDefaultAttrs2['default']);this.boundaryIds_ = [];this.setIndexByName_ = {};this.datasetIndex_ = [];this.registeredEvents_ = [];this.eventListeners_ = {};this.attributes_ = new _dygraphOptions2['default'](this); // Create the containing DIV and other interactive elements
this.createInterface_(); // Activate plugins.
this.plugins_ = [];var plugins=Dygraph.PLUGINS.concat(this.getOption('plugins'));for(var i=0;i < plugins.length;i++) { // the plugins option may contain either plugin classes or instances.
// Plugin instances contain an activate method.
var Plugin=plugins[i]; // either a constructor or an instance.
var pluginInstance;if(typeof Plugin.activate !== 'undefined'){pluginInstance = Plugin;}else {pluginInstance = new Plugin();}var pluginDict={plugin:pluginInstance,events:{},options:{},pluginOptions:{}};var handlers=pluginInstance.activate(this);for(var eventName in handlers) {if(!handlers.hasOwnProperty(eventName))continue; // TODO(danvk): validate eventName.
pluginDict.events[eventName] = handlers[eventName];}this.plugins_.push(pluginDict);} // At this point, plugins can no longer register event handlers.
// Construct a map from event -> ordered list of [callback, plugin].
for(var i=0;i < this.plugins_.length;i++) {var plugin_dict=this.plugins_[i];for(var eventName in plugin_dict.events) {if(!plugin_dict.events.hasOwnProperty(eventName))continue;var callback=plugin_dict.events[eventName];var pair=[plugin_dict.plugin,callback];if(!(eventName in this.eventListeners_)){this.eventListeners_[eventName] = [pair];}else {this.eventListeners_[eventName].push(pair);}}}this.createDragInterface_();this.start_();}; /**
 * Triggers a cascade of events to the various plugins which are interested in them.
 * Returns true if the "default behavior" should be prevented, i.e. if one
 * of the event listeners called event.preventDefault().
 * @private
 */Dygraph.prototype.cascadeEvents_ = function(name,extra_props){if(!(name in this.eventListeners_))return false; // QUESTION: can we use objects & prototypes to speed this up?
var e={dygraph:this,cancelable:false,defaultPrevented:false,preventDefault:function preventDefault(){if(!e.cancelable)throw "Cannot call preventDefault on non-cancelable event.";e.defaultPrevented = true;},propagationStopped:false,stopPropagation:function stopPropagation(){e.propagationStopped = true;}};utils.update(e,extra_props);var callback_plugin_pairs=this.eventListeners_[name];if(callback_plugin_pairs){for(var i=callback_plugin_pairs.length - 1;i >= 0;i--) {var plugin=callback_plugin_pairs[i][0];var callback=callback_plugin_pairs[i][1];callback.call(plugin,e);if(e.propagationStopped)break;}}return e.defaultPrevented;}; /**
 * Fetch a plugin instance of a particular class. Only for testing.
 * @private
 * @param {!Class} type The type of the plugin.
 * @return {Object} Instance of the plugin, or null if there is none.
 */Dygraph.prototype.getPluginInstance_ = function(type){for(var i=0;i < this.plugins_.length;i++) {var p=this.plugins_[i];if(p.plugin instanceof type){return p.plugin;}}return null;}; /**
 * Returns the zoomed status of the chart for one or both axes.
 *
 * Axis is an optional parameter. Can be set to 'x' or 'y'.
 *
 * The zoomed status for an axis is set whenever a user zooms using the mouse
 * or when the dateWindow or valueRange are updated. Double-clicking or calling
 * resetZoom() resets the zoom status for the chart.
 */Dygraph.prototype.isZoomed = function(axis){var isZoomedX=!!this.dateWindow_;if(axis === 'x')return isZoomedX;var isZoomedY=this.axes_.map(function(axis){return !!axis.valueRange;}).indexOf(true) >= 0;if(axis === null || axis === undefined){return isZoomedX || isZoomedY;}if(axis === 'y')return isZoomedY;throw new Error('axis parameter is [' + axis + '] must be null, \\'x\\' or \\'y\\'.');}; /**
 * Returns information about the Dygraph object, including its containing ID.
 */Dygraph.prototype.toString = function(){var maindiv=this.maindiv_;var id=maindiv && maindiv.id?maindiv.id:maindiv;return "[Dygraph " + id + "]";}; /**
 * @private
 * Returns the value of an option. This may be set by the user (either in the
 * constructor or by calling updateOptions) or by dygraphs, and may be set to a
 * per-series value.
 * @param {string} name The name of the option, e.g. 'rollPeriod'.
 * @param {string} [seriesName] The name of the series to which the option
 * will be applied. If no per-series value of this option is available, then
 * the global value is returned. This is optional.
 * @return { ... } The value of the option.
 */Dygraph.prototype.attr_ = function(name,seriesName){ // For "production" code, this gets removed by uglifyjs.
if(typeof process !== 'undefined'){if("development" != 'production'){if(typeof _dygraphOptionsReference2['default'] === 'undefined'){console.error('Must include options reference JS for testing');}else if(!_dygraphOptionsReference2['default'].hasOwnProperty(name)){console.error('Dygraphs is using property ' + name + ', which has no ' + 'entry in the Dygraphs.OPTIONS_REFERENCE listing.'); // Only log this error once.
_dygraphOptionsReference2['default'][name] = true;}}}return seriesName?this.attributes_.getForSeries(name,seriesName):this.attributes_.get(name);}; /**
 * Returns the current value for an option, as set in the constructor or via
 * updateOptions. You may pass in an (optional) series name to get per-series
 * values for the option.
 *
 * All values returned by this method should be considered immutable. If you
 * modify them, there is no guarantee that the changes will be honored or that
 * dygraphs will remain in a consistent state. If you want to modify an option,
 * use updateOptions() instead.
 *
 * @param {string} name The name of the option (e.g. 'strokeWidth')
 * @param {string=} opt_seriesName Series name to get per-series values.
 * @return {*} The value of the option.
 */Dygraph.prototype.getOption = function(name,opt_seriesName){return this.attr_(name,opt_seriesName);}; /**
 * Like getOption(), but specifically returns a number.
 * This is a convenience function for working with the Closure Compiler.
 * @param {string} name The name of the option (e.g. 'strokeWidth')
 * @param {string=} opt_seriesName Series name to get per-series values.
 * @return {number} The value of the option.
 * @private
 */Dygraph.prototype.getNumericOption = function(name,opt_seriesName){return  (/** @type{number} */this.getOption(name,opt_seriesName));}; /**
 * Like getOption(), but specifically returns a string.
 * This is a convenience function for working with the Closure Compiler.
 * @param {string} name The name of the option (e.g. 'strokeWidth')
 * @param {string=} opt_seriesName Series name to get per-series values.
 * @return {string} The value of the option.
 * @private
 */Dygraph.prototype.getStringOption = function(name,opt_seriesName){return  (/** @type{string} */this.getOption(name,opt_seriesName));}; /**
 * Like getOption(), but specifically returns a boolean.
 * This is a convenience function for working with the Closure Compiler.
 * @param {string} name The name of the option (e.g. 'strokeWidth')
 * @param {string=} opt_seriesName Series name to get per-series values.
 * @return {boolean} The value of the option.
 * @private
 */Dygraph.prototype.getBooleanOption = function(name,opt_seriesName){return  (/** @type{boolean} */this.getOption(name,opt_seriesName));}; /**
 * Like getOption(), but specifically returns a function.
 * This is a convenience function for working with the Closure Compiler.
 * @param {string} name The name of the option (e.g. 'strokeWidth')
 * @param {string=} opt_seriesName Series name to get per-series values.
 * @return {function(...)} The value of the option.
 * @private
 */Dygraph.prototype.getFunctionOption = function(name,opt_seriesName){return  (/** @type{function(...)} */this.getOption(name,opt_seriesName));};Dygraph.prototype.getOptionForAxis = function(name,axis){return this.attributes_.getForAxis(name,axis);}; /**
 * @private
 * @param {string} axis The name of the axis (i.e. 'x', 'y' or 'y2')
 * @return { ... } A function mapping string -> option value
 */Dygraph.prototype.optionsViewForAxis_ = function(axis){var self=this;return function(opt){var axis_opts=self.user_attrs_.axes;if(axis_opts && axis_opts[axis] && axis_opts[axis].hasOwnProperty(opt)){return axis_opts[axis][opt];} // I don't like that this is in a second spot.
if(axis === 'x' && opt === 'logscale'){ // return the default value.
// TODO(konigsberg): pull the default from a global default.
return false;} // user-specified attributes always trump defaults, even if they're less
// specific.
if(typeof self.user_attrs_[opt] != 'undefined'){return self.user_attrs_[opt];}axis_opts = self.attrs_.axes;if(axis_opts && axis_opts[axis] && axis_opts[axis].hasOwnProperty(opt)){return axis_opts[axis][opt];} // check old-style axis options
// TODO(danvk): add a deprecation warning if either of these match.
if(axis == 'y' && self.axes_[0].hasOwnProperty(opt)){return self.axes_[0][opt];}else if(axis == 'y2' && self.axes_[1].hasOwnProperty(opt)){return self.axes_[1][opt];}return self.attr_(opt);};}; /**
 * Returns the current rolling period, as set by the user or an option.
 * @return {number} The number of points in the rolling window
 */Dygraph.prototype.rollPeriod = function(){return this.rollPeriod_;}; /**
 * Returns the currently-visible x-range. This can be affected by zooming,
 * panning or a call to updateOptions.
 * Returns a two-element array: [left, right].
 * If the Dygraph has dates on the x-axis, these will be millis since epoch.
 */Dygraph.prototype.xAxisRange = function(){return this.dateWindow_?this.dateWindow_:this.xAxisExtremes();}; /**
 * Returns the lower- and upper-bound x-axis values of the data set.
 */Dygraph.prototype.xAxisExtremes = function(){var pad=this.getNumericOption('xRangePad') / this.plotter_.area.w;if(this.numRows() === 0){return [0 - pad,1 + pad];}var left=this.rawData_[0][0];var right=this.rawData_[this.rawData_.length - 1][0];if(pad){ // Must keep this in sync with dygraph-layout _evaluateLimits()
var range=right - left;left -= range * pad;right += range * pad;}return [left,right];}; /**
 * Returns the lower- and upper-bound y-axis values for each axis. These are
 * the ranges you'll get if you double-click to zoom out or call resetZoom().
 * The return value is an array of [low, high] tuples, one for each y-axis.
 */Dygraph.prototype.yAxisExtremes = function(){ // TODO(danvk): this is pretty inefficient
var packed=this.gatherDatasets_(this.rolledSeries_,null);var extremes=packed.extremes;var saveAxes=this.axes_;this.computeYAxisRanges_(extremes);var newAxes=this.axes_;this.axes_ = saveAxes;return newAxes.map(function(axis){return axis.extremeRange;});}; /**
 * Returns the currently-visible y-range for an axis. This can be affected by
 * zooming, panning or a call to updateOptions. Axis indices are zero-based. If
 * called with no arguments, returns the range of the first axis.
 * Returns a two-element array: [bottom, top].
 */Dygraph.prototype.yAxisRange = function(idx){if(typeof idx == "undefined")idx = 0;if(idx < 0 || idx >= this.axes_.length){return null;}var axis=this.axes_[idx];return [axis.computedValueRange[0],axis.computedValueRange[1]];}; /**
 * Returns the currently-visible y-ranges for each axis. This can be affected by
 * zooming, panning, calls to updateOptions, etc.
 * Returns an array of [bottom, top] pairs, one for each y-axis.
 */Dygraph.prototype.yAxisRanges = function(){var ret=[];for(var i=0;i < this.axes_.length;i++) {ret.push(this.yAxisRange(i));}return ret;}; // TODO(danvk): use these functions throughout dygraphs.
/**
 * Convert from data coordinates to canvas/div X/Y coordinates.
 * If specified, do this conversion for the coordinate system of a particular
 * axis. Uses the first axis by default.
 * Returns a two-element array: [X, Y]
 *
 * Note: use toDomXCoord instead of toDomCoords(x, null) and use toDomYCoord
 * instead of toDomCoords(null, y, axis).
 */Dygraph.prototype.toDomCoords = function(x,y,axis){return [this.toDomXCoord(x),this.toDomYCoord(y,axis)];}; /**
 * Convert from data x coordinates to canvas/div X coordinate.
 * If specified, do this conversion for the coordinate system of a particular
 * axis.
 * Returns a single value or null if x is null.
 */Dygraph.prototype.toDomXCoord = function(x){if(x === null){return null;}var area=this.plotter_.area;var xRange=this.xAxisRange();return area.x + (x - xRange[0]) / (xRange[1] - xRange[0]) * area.w;}; /**
 * Convert from data x coordinates to canvas/div Y coordinate and optional
 * axis. Uses the first axis by default.
 *
 * returns a single value or null if y is null.
 */Dygraph.prototype.toDomYCoord = function(y,axis){var pct=this.toPercentYCoord(y,axis);if(pct === null){return null;}var area=this.plotter_.area;return area.y + pct * area.h;}; /**
 * Convert from canvas/div coords to data coordinates.
 * If specified, do this conversion for the coordinate system of a particular
 * axis. Uses the first axis by default.
 * Returns a two-element array: [X, Y].
 *
 * Note: use toDataXCoord instead of toDataCoords(x, null) and use toDataYCoord
 * instead of toDataCoords(null, y, axis).
 */Dygraph.prototype.toDataCoords = function(x,y,axis){return [this.toDataXCoord(x),this.toDataYCoord(y,axis)];}; /**
 * Convert from canvas/div x coordinate to data coordinate.
 *
 * If x is null, this returns null.
 */Dygraph.prototype.toDataXCoord = function(x){if(x === null){return null;}var area=this.plotter_.area;var xRange=this.xAxisRange();if(!this.attributes_.getForAxis("logscale",'x')){return xRange[0] + (x - area.x) / area.w * (xRange[1] - xRange[0]);}else {var pct=(x - area.x) / area.w;return utils.logRangeFraction(xRange[0],xRange[1],pct);}}; /**
 * Convert from canvas/div y coord to value.
 *
 * If y is null, this returns null.
 * if axis is null, this uses the first axis.
 */Dygraph.prototype.toDataYCoord = function(y,axis){if(y === null){return null;}var area=this.plotter_.area;var yRange=this.yAxisRange(axis);if(typeof axis == "undefined")axis = 0;if(!this.attributes_.getForAxis("logscale",axis)){return yRange[0] + (area.y + area.h - y) / area.h * (yRange[1] - yRange[0]);}else { // Computing the inverse of toDomCoord.
var pct=(y - area.y) / area.h; // Note reversed yRange, y1 is on top with pct==0.
return utils.logRangeFraction(yRange[1],yRange[0],pct);}}; /**
 * Converts a y for an axis to a percentage from the top to the
 * bottom of the drawing area.
 *
 * If the coordinate represents a value visible on the canvas, then
 * the value will be between 0 and 1, where 0 is the top of the canvas.
 * However, this method will return values outside the range, as
 * values can fall outside the canvas.
 *
 * If y is null, this returns null.
 * if axis is null, this uses the first axis.
 *
 * @param {number} y The data y-coordinate.
 * @param {number} [axis] The axis number on which the data coordinate lives.
 * @return {number} A fraction in [0, 1] where 0 = the top edge.
 */Dygraph.prototype.toPercentYCoord = function(y,axis){if(y === null){return null;}if(typeof axis == "undefined")axis = 0;var yRange=this.yAxisRange(axis);var pct;var logscale=this.attributes_.getForAxis("logscale",axis);if(logscale){var logr0=utils.log10(yRange[0]);var logr1=utils.log10(yRange[1]);pct = (logr1 - utils.log10(y)) / (logr1 - logr0);}else { // yRange[1] - y is unit distance from the bottom.
// yRange[1] - yRange[0] is the scale of the range.
// (yRange[1] - y) / (yRange[1] - yRange[0]) is the % from the bottom.
pct = (yRange[1] - y) / (yRange[1] - yRange[0]);}return pct;}; /**
 * Converts an x value to a percentage from the left to the right of
 * the drawing area.
 *
 * If the coordinate represents a value visible on the canvas, then
 * the value will be between 0 and 1, where 0 is the left of the canvas.
 * However, this method will return values outside the range, as
 * values can fall outside the canvas.
 *
 * If x is null, this returns null.
 * @param {number} x The data x-coordinate.
 * @return {number} A fraction in [0, 1] where 0 = the left edge.
 */Dygraph.prototype.toPercentXCoord = function(x){if(x === null){return null;}var xRange=this.xAxisRange();var pct;var logscale=this.attributes_.getForAxis("logscale",'x');if(logscale === true){ // logscale can be null so we test for true explicitly.
var logr0=utils.log10(xRange[0]);var logr1=utils.log10(xRange[1]);pct = (utils.log10(x) - logr0) / (logr1 - logr0);}else { // x - xRange[0] is unit distance from the left.
// xRange[1] - xRange[0] is the scale of the range.
// The full expression below is the % from the left.
pct = (x - xRange[0]) / (xRange[1] - xRange[0]);}return pct;}; /**
 * Returns the number of columns (including the independent variable).
 * @return {number} The number of columns.
 */Dygraph.prototype.numColumns = function(){if(!this.rawData_)return 0;return this.rawData_[0]?this.rawData_[0].length:this.attr_("labels").length;}; /**
 * Returns the number of rows (excluding any header/label row).
 * @return {number} The number of rows, less any header.
 */Dygraph.prototype.numRows = function(){if(!this.rawData_)return 0;return this.rawData_.length;}; /**
 * Returns the value in the given row and column. If the row and column exceed
 * the bounds on the data, returns null. Also returns null if the value is
 * missing.
 * @param {number} row The row number of the data (0-based). Row 0 is the
 *     first row of data, not a header row.
 * @param {number} col The column number of the data (0-based)
 * @return {number} The value in the specified cell or null if the row/col
 *     were out of range.
 */Dygraph.prototype.getValue = function(row,col){if(row < 0 || row > this.rawData_.length)return null;if(col < 0 || col > this.rawData_[row].length)return null;return this.rawData_[row][col];}; /**
 * Generates interface elements for the Dygraph: a containing div, a div to
 * display the current point, and a textbox to adjust the rolling average
 * period. Also creates the Renderer/Layout elements.
 * @private
 */Dygraph.prototype.createInterface_ = function(){ // Create the all-enclosing graph div
var enclosing=this.maindiv_;this.graphDiv = document.createElement("div"); // TODO(danvk): any other styles that are useful to set here?
this.graphDiv.style.textAlign = 'left'; // This is a CSS "reset"
this.graphDiv.style.position = 'relative';enclosing.appendChild(this.graphDiv); // Create the canvas for interactive parts of the chart.
this.canvas_ = utils.createCanvas();this.canvas_.style.position = "absolute"; // ... and for static parts of the chart.
this.hidden_ = this.createPlotKitCanvas_(this.canvas_);this.canvas_ctx_ = utils.getContext(this.canvas_);this.hidden_ctx_ = utils.getContext(this.hidden_);this.resizeElements_(); // The interactive parts of the graph are drawn on top of the chart.
this.graphDiv.appendChild(this.hidden_);this.graphDiv.appendChild(this.canvas_);this.mouseEventElement_ = this.createMouseEventElement_(); // Create the grapher
this.layout_ = new _dygraphLayout2['default'](this);var dygraph=this;this.mouseMoveHandler_ = function(e){dygraph.mouseMove_(e);};this.mouseOutHandler_ = function(e){ // The mouse has left the chart if:
// 1. e.target is inside the chart
// 2. e.relatedTarget is outside the chart
var target=e.target || e.fromElement;var relatedTarget=e.relatedTarget || e.toElement;if(utils.isNodeContainedBy(target,dygraph.graphDiv) && !utils.isNodeContainedBy(relatedTarget,dygraph.graphDiv)){dygraph.mouseOut_(e);}};this.addAndTrackEvent(window,'mouseout',this.mouseOutHandler_);this.addAndTrackEvent(this.mouseEventElement_,'mousemove',this.mouseMoveHandler_); // Don't recreate and register the resize handler on subsequent calls.
// This happens when the graph is resized.
if(!this.resizeHandler_){this.resizeHandler_ = function(e){dygraph.resize();}; // Update when the window is resized.
// TODO(danvk): drop frames depending on complexity of the chart.
this.addAndTrackEvent(window,'resize',this.resizeHandler_);}};Dygraph.prototype.resizeElements_ = function(){this.graphDiv.style.width = this.width_ + "px";this.graphDiv.style.height = this.height_ + "px";var pixelRatioOption=this.getNumericOption('pixelRatio');var canvasScale=pixelRatioOption || utils.getContextPixelRatio(this.canvas_ctx_);this.canvas_.width = this.width_ * canvasScale;this.canvas_.height = this.height_ * canvasScale;this.canvas_.style.width = this.width_ + "px"; // for IE
this.canvas_.style.height = this.height_ + "px"; // for IE
if(canvasScale !== 1){this.canvas_ctx_.scale(canvasScale,canvasScale);}var hiddenScale=pixelRatioOption || utils.getContextPixelRatio(this.hidden_ctx_);this.hidden_.width = this.width_ * hiddenScale;this.hidden_.height = this.height_ * hiddenScale;this.hidden_.style.width = this.width_ + "px"; // for IE
this.hidden_.style.height = this.height_ + "px"; // for IE
if(hiddenScale !== 1){this.hidden_ctx_.scale(hiddenScale,hiddenScale);}}; /**
 * Detach DOM elements in the dygraph and null out all data references.
 * Calling this when you're done with a dygraph can dramatically reduce memory
 * usage. See, e.g., the tests/perf.html example.
 */Dygraph.prototype.destroy = function(){this.canvas_ctx_.restore();this.hidden_ctx_.restore(); // Destroy any plugins, in the reverse order that they were registered.
for(var i=this.plugins_.length - 1;i >= 0;i--) {var p=this.plugins_.pop();if(p.plugin.destroy)p.plugin.destroy();}var removeRecursive=function removeRecursive(node){while(node.hasChildNodes()) {removeRecursive(node.firstChild);node.removeChild(node.firstChild);}};this.removeTrackedEvents_(); // remove mouse event handlers (This may not be necessary anymore)
utils.removeEvent(window,'mouseout',this.mouseOutHandler_);utils.removeEvent(this.mouseEventElement_,'mousemove',this.mouseMoveHandler_); // remove window handlers
utils.removeEvent(window,'resize',this.resizeHandler_);this.resizeHandler_ = null;removeRecursive(this.maindiv_);var nullOut=function nullOut(obj){for(var n in obj) {if(typeof obj[n] === 'object'){obj[n] = null;}}}; // These may not all be necessary, but it can't hurt...
nullOut(this.layout_);nullOut(this.plotter_);nullOut(this);}; /**
 * Creates the canvas on which the chart will be drawn. Only the Renderer ever
 * draws on this particular canvas. All Dygraph work (i.e. drawing hover dots
 * or the zoom rectangles) is done on this.canvas_.
 * @param {Object} canvas The Dygraph canvas over which to overlay the plot
 * @return {Object} The newly-created canvas
 * @private
 */Dygraph.prototype.createPlotKitCanvas_ = function(canvas){var h=utils.createCanvas();h.style.position = "absolute"; // TODO(danvk): h should be offset from canvas. canvas needs to include
// some extra area to make it easier to zoom in on the far left and far
// right. h needs to be precisely the plot area, so that clipping occurs.
h.style.top = canvas.style.top;h.style.left = canvas.style.left;h.width = this.width_;h.height = this.height_;h.style.width = this.width_ + "px"; // for IE
h.style.height = this.height_ + "px"; // for IE
return h;}; /**
 * Creates an overlay element used to handle mouse events.
 * @return {Object} The mouse event element.
 * @private
 */Dygraph.prototype.createMouseEventElement_ = function(){return this.canvas_;}; /**
 * Generate a set of distinct colors for the data series. This is done with a
 * color wheel. Saturation/Value are customizable, and the hue is
 * equally-spaced around the color wheel. If a custom set of colors is
 * specified, that is used instead.
 * @private
 */Dygraph.prototype.setColors_ = function(){var labels=this.getLabels();var num=labels.length - 1;this.colors_ = [];this.colorsMap_ = {}; // These are used for when no custom colors are specified.
var sat=this.getNumericOption('colorSaturation') || 1.0;var val=this.getNumericOption('colorValue') || 0.5;var half=Math.ceil(num / 2);var colors=this.getOption('colors');var visibility=this.visibility();for(var i=0;i < num;i++) {if(!visibility[i]){continue;}var label=labels[i + 1];var colorStr=this.attributes_.getForSeries('color',label);if(!colorStr){if(colors){colorStr = colors[i % colors.length];}else { // alternate colors for high contrast.
var idx=i % 2?half + (i + 1) / 2:Math.ceil((i + 1) / 2);var hue=1.0 * idx / (1 + num);colorStr = utils.hsvToRGB(hue,sat,val);}}this.colors_.push(colorStr);this.colorsMap_[label] = colorStr;}}; /**
 * Return the list of colors. This is either the list of colors passed in the
 * attributes or the autogenerated list of rgb(r,g,b) strings.
 * This does not return colors for invisible series.
 * @return {Array.<string>} The list of colors.
 */Dygraph.prototype.getColors = function(){return this.colors_;}; /**
 * Returns a few attributes of a series, i.e. its color, its visibility, which
 * axis it's assigned to, and its column in the original data.
 * Returns null if the series does not exist.
 * Otherwise, returns an object with column, visibility, color and axis properties.
 * The "axis" property will be set to 1 for y1 and 2 for y2.
 * The "column" property can be fed back into getValue(row, column) to get
 * values for this series.
 */Dygraph.prototype.getPropertiesForSeries = function(series_name){var idx=-1;var labels=this.getLabels();for(var i=1;i < labels.length;i++) {if(labels[i] == series_name){idx = i;break;}}if(idx == -1)return null;return {name:series_name,column:idx,visible:this.visibility()[idx - 1],color:this.colorsMap_[series_name],axis:1 + this.attributes_.axisForSeries(series_name)};}; /**
 * Create the text box to adjust the averaging period
 * @private
 */Dygraph.prototype.createRollInterface_ = function(){var _this=this; // Create a roller if one doesn't exist already.
var roller=this.roller_;if(!roller){this.roller_ = roller = document.createElement("input");roller.type = "text";roller.style.display = "none";roller.className = 'dygraph-roller';this.graphDiv.appendChild(roller);}var display=this.getBooleanOption('showRoller')?'block':'none';var area=this.getArea();var textAttr={"top":area.y + area.h - 25 + "px","left":area.x + 1 + "px","display":display};roller.size = "2";roller.value = this.rollPeriod_;utils.update(roller.style,textAttr);roller.onchange = function(){return _this.adjustRoll(roller.value);};}; /**
 * Set up all the mouse handlers needed to capture dragging behavior for zoom
 * events.
 * @private
 */Dygraph.prototype.createDragInterface_ = function(){var context={ // Tracks whether the mouse is down right now
isZooming:false,isPanning:false, // is this drag part of a pan?
is2DPan:false, // if so, is that pan 1- or 2-dimensional?
dragStartX:null, // pixel coordinates
dragStartY:null, // pixel coordinates
dragEndX:null, // pixel coordinates
dragEndY:null, // pixel coordinates
dragDirection:null,prevEndX:null, // pixel coordinates
prevEndY:null, // pixel coordinates
prevDragDirection:null,cancelNextDblclick:false, // see comment in dygraph-interaction-model.js
// The value on the left side of the graph when a pan operation starts.
initialLeftmostDate:null, // The number of units each pixel spans. (This won't be valid for log
// scales)
xUnitsPerPixel:null, // TODO(danvk): update this comment
// The range in second/value units that the viewport encompasses during a
// panning operation.
dateRange:null, // Top-left corner of the canvas, in DOM coords
// TODO(konigsberg): Rename topLeftCanvasX, topLeftCanvasY.
px:0,py:0, // Values for use with panEdgeFraction, which limit how far outside the
// graph's data boundaries it can be panned.
boundedDates:null, // [minDate, maxDate]
boundedValues:null, // [[minValue, maxValue] ...]
// We cover iframes during mouse interactions. See comments in
// dygraph-utils.js for more info on why this is a good idea.
tarp:new _iframeTarp2['default'](), // contextB is the same thing as this context object but renamed.
initializeMouseDown:function initializeMouseDown(event,g,contextB){ // prevents mouse drags from selecting page text.
if(event.preventDefault){event.preventDefault(); // Firefox, Chrome, etc.
}else {event.returnValue = false; // IE
event.cancelBubble = true;}var canvasPos=utils.findPos(g.canvas_);contextB.px = canvasPos.x;contextB.py = canvasPos.y;contextB.dragStartX = utils.dragGetX_(event,contextB);contextB.dragStartY = utils.dragGetY_(event,contextB);contextB.cancelNextDblclick = false;contextB.tarp.cover();},destroy:function destroy(){var context=this;if(context.isZooming || context.isPanning){context.isZooming = false;context.dragStartX = null;context.dragStartY = null;}if(context.isPanning){context.isPanning = false;context.draggingDate = null;context.dateRange = null;for(var i=0;i < self.axes_.length;i++) {delete self.axes_[i].draggingValue;delete self.axes_[i].dragValueRange;}}context.tarp.uncover();}};var interactionModel=this.getOption("interactionModel"); // Self is the graph.
var self=this; // Function that binds the graph and context to the handler.
var bindHandler=function bindHandler(handler){return function(event){handler(event,self,context);};};for(var eventName in interactionModel) {if(!interactionModel.hasOwnProperty(eventName))continue;this.addAndTrackEvent(this.mouseEventElement_,eventName,bindHandler(interactionModel[eventName]));} // If the user releases the mouse button during a drag, but not over the
// canvas, then it doesn't count as a zooming action.
if(!interactionModel.willDestroyContextMyself){var mouseUpHandler=function mouseUpHandler(event){context.destroy();};this.addAndTrackEvent(document,'mouseup',mouseUpHandler);}}; /**
 * Draw a gray zoom rectangle over the desired area of the canvas. Also clears
 * up any previous zoom rectangles that were drawn. This could be optimized to
 * avoid extra redrawing, but it's tricky to avoid interactions with the status
 * dots.
 *
 * @param {number} direction the direction of the zoom rectangle. Acceptable
 *     values are utils.HORIZONTAL and utils.VERTICAL.
 * @param {number} startX The X position where the drag started, in canvas
 *     coordinates.
 * @param {number} endX The current X position of the drag, in canvas coords.
 * @param {number} startY The Y position where the drag started, in canvas
 *     coordinates.
 * @param {number} endY The current Y position of the drag, in canvas coords.
 * @param {number} prevDirection the value of direction on the previous call to
 *     this function. Used to avoid excess redrawing
 * @param {number} prevEndX The value of endX on the previous call to this
 *     function. Used to avoid excess redrawing
 * @param {number} prevEndY The value of endY on the previous call to this
 *     function. Used to avoid excess redrawing
 * @private
 */Dygraph.prototype.drawZoomRect_ = function(direction,startX,endX,startY,endY,prevDirection,prevEndX,prevEndY){var ctx=this.canvas_ctx_; // Clean up from the previous rect if necessary
if(prevDirection == utils.HORIZONTAL){ctx.clearRect(Math.min(startX,prevEndX),this.layout_.getPlotArea().y,Math.abs(startX - prevEndX),this.layout_.getPlotArea().h);}else if(prevDirection == utils.VERTICAL){ctx.clearRect(this.layout_.getPlotArea().x,Math.min(startY,prevEndY),this.layout_.getPlotArea().w,Math.abs(startY - prevEndY));} // Draw a light-grey rectangle to show the new viewing area
if(direction == utils.HORIZONTAL){if(endX && startX){ctx.fillStyle = "rgba(128,128,128,0.33)";ctx.fillRect(Math.min(startX,endX),this.layout_.getPlotArea().y,Math.abs(endX - startX),this.layout_.getPlotArea().h);}}else if(direction == utils.VERTICAL){if(endY && startY){ctx.fillStyle = "rgba(128,128,128,0.33)";ctx.fillRect(this.layout_.getPlotArea().x,Math.min(startY,endY),this.layout_.getPlotArea().w,Math.abs(endY - startY));}}}; /**
 * Clear the zoom rectangle (and perform no zoom).
 * @private
 */Dygraph.prototype.clearZoomRect_ = function(){this.currentZoomRectArgs_ = null;this.canvas_ctx_.clearRect(0,0,this.width_,this.height_);}; /**
 * Zoom to something containing [lowX, highX]. These are pixel coordinates in
 * the canvas. The exact zoom window may be slightly larger if there are no data
 * points near lowX or highX. Don't confuse this function with doZoomXDates,
 * which accepts dates that match the raw data. This function redraws the graph.
 *
 * @param {number} lowX The leftmost pixel value that should be visible.
 * @param {number} highX The rightmost pixel value that should be visible.
 * @private
 */Dygraph.prototype.doZoomX_ = function(lowX,highX){this.currentZoomRectArgs_ = null; // Find the earliest and latest dates contained in this canvasx range.
// Convert the call to date ranges of the raw data.
var minDate=this.toDataXCoord(lowX);var maxDate=this.toDataXCoord(highX);this.doZoomXDates_(minDate,maxDate);}; /**
 * Zoom to something containing [minDate, maxDate] values. Don't confuse this
 * method with doZoomX which accepts pixel coordinates. This function redraws
 * the graph.
 *
 * @param {number} minDate The minimum date that should be visible.
 * @param {number} maxDate The maximum date that should be visible.
 * @private
 */Dygraph.prototype.doZoomXDates_ = function(minDate,maxDate){var _this2=this; // TODO(danvk): when xAxisRange is null (i.e. "fit to data", the animation
// can produce strange effects. Rather than the x-axis transitioning slowly
// between values, it can jerk around.)
var old_window=this.xAxisRange();var new_window=[minDate,maxDate];var zoomCallback=this.getFunctionOption('zoomCallback');this.doAnimatedZoom(old_window,new_window,null,null,function(){if(zoomCallback){zoomCallback.call(_this2,minDate,maxDate,_this2.yAxisRanges());}});}; /**
 * Zoom to something containing [lowY, highY]. These are pixel coordinates in
 * the canvas. This function redraws the graph.
 *
 * @param {number} lowY The topmost pixel value that should be visible.
 * @param {number} highY The lowest pixel value that should be visible.
 * @private
 */Dygraph.prototype.doZoomY_ = function(lowY,highY){var _this3=this;this.currentZoomRectArgs_ = null; // Find the highest and lowest values in pixel range for each axis.
// Note that lowY (in pixels) corresponds to the max Value (in data coords).
// This is because pixels increase as you go down on the screen, whereas data
// coordinates increase as you go up the screen.
var oldValueRanges=this.yAxisRanges();var newValueRanges=[];for(var i=0;i < this.axes_.length;i++) {var hi=this.toDataYCoord(lowY,i);var low=this.toDataYCoord(highY,i);newValueRanges.push([low,hi]);}var zoomCallback=this.getFunctionOption('zoomCallback');this.doAnimatedZoom(null,null,oldValueRanges,newValueRanges,function(){if(zoomCallback){var _xAxisRange=_this3.xAxisRange();var _xAxisRange2=_slicedToArray(_xAxisRange,2);var minX=_xAxisRange2[0];var maxX=_xAxisRange2[1];zoomCallback.call(_this3,minX,maxX,_this3.yAxisRanges());}});}; /**
 * Transition function to use in animations. Returns values between 0.0
 * (totally old values) and 1.0 (totally new values) for each frame.
 * @private
 */Dygraph.zoomAnimationFunction = function(frame,numFrames){var k=1.5;return (1.0 - Math.pow(k,-frame)) / (1.0 - Math.pow(k,-numFrames));}; /**
 * Reset the zoom to the original view coordinates. This is the same as
 * double-clicking on the graph.
 */Dygraph.prototype.resetZoom = function(){var _this4=this;var dirtyX=this.isZoomed('x');var dirtyY=this.isZoomed('y');var dirty=dirtyX || dirtyY; // Clear any selection, since it's likely to be drawn in the wrong place.
this.clearSelection();if(!dirty)return; // Calculate extremes to avoid lack of padding on reset.
var _xAxisExtremes=this.xAxisExtremes();var _xAxisExtremes2=_slicedToArray(_xAxisExtremes,2);var minDate=_xAxisExtremes2[0];var maxDate=_xAxisExtremes2[1];var animatedZooms=this.getBooleanOption('animatedZooms');var zoomCallback=this.getFunctionOption('zoomCallback'); // TODO(danvk): merge this block w/ the code below.
// TODO(danvk): factor out a generic, public zoomTo method.
if(!animatedZooms){this.dateWindow_ = null;this.axes_.forEach(function(axis){if(axis.valueRange)delete axis.valueRange;});this.drawGraph_();if(zoomCallback){zoomCallback.call(this,minDate,maxDate,this.yAxisRanges());}return;}var oldWindow=null,newWindow=null,oldValueRanges=null,newValueRanges=null;if(dirtyX){oldWindow = this.xAxisRange();newWindow = [minDate,maxDate];}if(dirtyY){oldValueRanges = this.yAxisRanges();newValueRanges = this.yAxisExtremes();}this.doAnimatedZoom(oldWindow,newWindow,oldValueRanges,newValueRanges,function(){_this4.dateWindow_ = null;_this4.axes_.forEach(function(axis){if(axis.valueRange)delete axis.valueRange;});if(zoomCallback){zoomCallback.call(_this4,minDate,maxDate,_this4.yAxisRanges());}});}; /**
 * Combined animation logic for all zoom functions.
 * either the x parameters or y parameters may be null.
 * @private
 */Dygraph.prototype.doAnimatedZoom = function(oldXRange,newXRange,oldYRanges,newYRanges,callback){var _this5=this;var steps=this.getBooleanOption("animatedZooms")?Dygraph.ANIMATION_STEPS:1;var windows=[];var valueRanges=[];var step,frac;if(oldXRange !== null && newXRange !== null){for(step = 1;step <= steps;step++) {frac = Dygraph.zoomAnimationFunction(step,steps);windows[step - 1] = [oldXRange[0] * (1 - frac) + frac * newXRange[0],oldXRange[1] * (1 - frac) + frac * newXRange[1]];}}if(oldYRanges !== null && newYRanges !== null){for(step = 1;step <= steps;step++) {frac = Dygraph.zoomAnimationFunction(step,steps);var thisRange=[];for(var j=0;j < this.axes_.length;j++) {thisRange.push([oldYRanges[j][0] * (1 - frac) + frac * newYRanges[j][0],oldYRanges[j][1] * (1 - frac) + frac * newYRanges[j][1]]);}valueRanges[step - 1] = thisRange;}}utils.repeatAndCleanup(function(step){if(valueRanges.length){for(var i=0;i < _this5.axes_.length;i++) {var w=valueRanges[step][i];_this5.axes_[i].valueRange = [w[0],w[1]];}}if(windows.length){_this5.dateWindow_ = windows[step];}_this5.drawGraph_();},steps,Dygraph.ANIMATION_DURATION / steps,callback);}; /**
 * Get the current graph's area object.
 *
 * Returns: {x, y, w, h}
 */Dygraph.prototype.getArea = function(){return this.plotter_.area;}; /**
 * Convert a mouse event to DOM coordinates relative to the graph origin.
 *
 * Returns a two-element array: [X, Y].
 */Dygraph.prototype.eventToDomCoords = function(event){if(event.offsetX && event.offsetY){return [event.offsetX,event.offsetY];}else {var eventElementPos=utils.findPos(this.mouseEventElement_);var canvasx=utils.pageX(event) - eventElementPos.x;var canvasy=utils.pageY(event) - eventElementPos.y;return [canvasx,canvasy];}}; /**
 * Given a canvas X coordinate, find the closest row.
 * @param {number} domX graph-relative DOM X coordinate
 * Returns {number} row number.
 * @private
 */Dygraph.prototype.findClosestRow = function(domX){var minDistX=Infinity;var closestRow=-1;var sets=this.layout_.points;for(var i=0;i < sets.length;i++) {var points=sets[i];var len=points.length;for(var j=0;j < len;j++) {var point=points[j];if(!utils.isValidPoint(point,true))continue;var dist=Math.abs(point.canvasx - domX);if(dist < minDistX){minDistX = dist;closestRow = point.idx;}}}return closestRow;}; /**
 * Given canvas X,Y coordinates, find the closest point.
 *
 * This finds the individual data point across all visible series
 * that's closest to the supplied DOM coordinates using the standard
 * Euclidean X,Y distance.
 *
 * @param {number} domX graph-relative DOM X coordinate
 * @param {number} domY graph-relative DOM Y coordinate
 * Returns: {row, seriesName, point}
 * @private
 */Dygraph.prototype.findClosestPoint = function(domX,domY){var minDist=Infinity;var dist,dx,dy,point,closestPoint,closestSeries,closestRow;for(var setIdx=this.layout_.points.length - 1;setIdx >= 0;--setIdx) {var points=this.layout_.points[setIdx];for(var i=0;i < points.length;++i) {point = points[i];if(!utils.isValidPoint(point))continue;dx = point.canvasx - domX;dy = point.canvasy - domY;dist = dx * dx + dy * dy;if(dist < minDist){minDist = dist;closestPoint = point;closestSeries = setIdx;closestRow = point.idx;}}}var name=this.layout_.setNames[closestSeries];return {row:closestRow,seriesName:name,point:closestPoint};}; /**
 * Given canvas X,Y coordinates, find the touched area in a stacked graph.
 *
 * This first finds the X data point closest to the supplied DOM X coordinate,
 * then finds the series which puts the Y coordinate on top of its filled area,
 * using linear interpolation between adjacent point pairs.
 *
 * @param {number} domX graph-relative DOM X coordinate
 * @param {number} domY graph-relative DOM Y coordinate
 * Returns: {row, seriesName, point}
 * @private
 */Dygraph.prototype.findStackedPoint = function(domX,domY){var row=this.findClosestRow(domX);var closestPoint,closestSeries;for(var setIdx=0;setIdx < this.layout_.points.length;++setIdx) {var boundary=this.getLeftBoundary_(setIdx);var rowIdx=row - boundary;var points=this.layout_.points[setIdx];if(rowIdx >= points.length)continue;var p1=points[rowIdx];if(!utils.isValidPoint(p1))continue;var py=p1.canvasy;if(domX > p1.canvasx && rowIdx + 1 < points.length){ // interpolate series Y value using next point
var p2=points[rowIdx + 1];if(utils.isValidPoint(p2)){var dx=p2.canvasx - p1.canvasx;if(dx > 0){var r=(domX - p1.canvasx) / dx;py += r * (p2.canvasy - p1.canvasy);}}}else if(domX < p1.canvasx && rowIdx > 0){ // interpolate series Y value using previous point
var p0=points[rowIdx - 1];if(utils.isValidPoint(p0)){var dx=p1.canvasx - p0.canvasx;if(dx > 0){var r=(p1.canvasx - domX) / dx;py += r * (p0.canvasy - p1.canvasy);}}} // Stop if the point (domX, py) is above this series' upper edge
if(setIdx === 0 || py < domY){closestPoint = p1;closestSeries = setIdx;}}var name=this.layout_.setNames[closestSeries];return {row:row,seriesName:name,point:closestPoint};}; /**
 * When the mouse moves in the canvas, display information about a nearby data
 * point and draw dots over those points in the data series. This function
 * takes care of cleanup of previously-drawn dots.
 * @param {Object} event The mousemove event from the browser.
 * @private
 */Dygraph.prototype.mouseMove_ = function(event){ // This prevents JS errors when mousing over the canvas before data loads.
var points=this.layout_.points;if(points === undefined || points === null)return;var canvasCoords=this.eventToDomCoords(event);var canvasx=canvasCoords[0];var canvasy=canvasCoords[1];var highlightSeriesOpts=this.getOption("highlightSeriesOpts");var selectionChanged=false;if(highlightSeriesOpts && !this.isSeriesLocked()){var closest;if(this.getBooleanOption("stackedGraph")){closest = this.findStackedPoint(canvasx,canvasy);}else {closest = this.findClosestPoint(canvasx,canvasy);}selectionChanged = this.setSelection(closest.row,closest.seriesName);}else {var idx=this.findClosestRow(canvasx);selectionChanged = this.setSelection(idx);}var callback=this.getFunctionOption("highlightCallback");if(callback && selectionChanged){callback.call(this,event,this.lastx_,this.selPoints_,this.lastRow_,this.highlightSet_);}}; /**
 * Fetch left offset from the specified set index or if not passed, the
 * first defined boundaryIds record (see bug #236).
 * @private
 */Dygraph.prototype.getLeftBoundary_ = function(setIdx){if(this.boundaryIds_[setIdx]){return this.boundaryIds_[setIdx][0];}else {for(var i=0;i < this.boundaryIds_.length;i++) {if(this.boundaryIds_[i] !== undefined){return this.boundaryIds_[i][0];}}return 0;}};Dygraph.prototype.animateSelection_ = function(direction){var totalSteps=10;var millis=30;if(this.fadeLevel === undefined)this.fadeLevel = 0;if(this.animateId === undefined)this.animateId = 0;var start=this.fadeLevel;var steps=direction < 0?start:totalSteps - start;if(steps <= 0){if(this.fadeLevel){this.updateSelection_(1.0);}return;}var thisId=++this.animateId;var that=this;var cleanupIfClearing=function cleanupIfClearing(){ // if we haven't reached fadeLevel 0 in the max frame time,
// ensure that the clear happens and just go to 0
if(that.fadeLevel !== 0 && direction < 0){that.fadeLevel = 0;that.clearSelection();}};utils.repeatAndCleanup(function(n){ // ignore simultaneous animations
if(that.animateId != thisId)return;that.fadeLevel += direction;if(that.fadeLevel === 0){that.clearSelection();}else {that.updateSelection_(that.fadeLevel / totalSteps);}},steps,millis,cleanupIfClearing);}; /**
 * Draw dots over the selectied points in the data series. This function
 * takes care of cleanup of previously-drawn dots.
 * @private
 */Dygraph.prototype.updateSelection_ = function(opt_animFraction){ /*var defaultPrevented = */this.cascadeEvents_('select',{selectedRow:this.lastRow_ === -1?undefined:this.lastRow_,selectedX:this.lastx_ === -1?undefined:this.lastx_,selectedPoints:this.selPoints_}); // TODO(danvk): use defaultPrevented here?
// Clear the previously drawn vertical, if there is one
var i;var ctx=this.canvas_ctx_;if(this.getOption('highlightSeriesOpts')){ctx.clearRect(0,0,this.width_,this.height_);var alpha=1.0 - this.getNumericOption('highlightSeriesBackgroundAlpha');var backgroundColor=utils.toRGB_(this.getOption('highlightSeriesBackgroundColor'));if(alpha){ // Activating background fade includes an animation effect for a gradual
// fade. TODO(klausw): make this independently configurable if it causes
// issues? Use a shared preference to control animations?
var animateBackgroundFade=true;if(animateBackgroundFade){if(opt_animFraction === undefined){ // start a new animation
this.animateSelection_(1);return;}alpha *= opt_animFraction;}ctx.fillStyle = 'rgba(' + backgroundColor.r + ',' + backgroundColor.g + ',' + backgroundColor.b + ',' + alpha + ')';ctx.fillRect(0,0,this.width_,this.height_);} // Redraw only the highlighted series in the interactive canvas (not the
// static plot canvas, which is where series are usually drawn).
this.plotter_._renderLineChart(this.highlightSet_,ctx);}else if(this.previousVerticalX_ >= 0){ // Determine the maximum highlight circle size.
var maxCircleSize=0;var labels=this.attr_('labels');for(i = 1;i < labels.length;i++) {var r=this.getNumericOption('highlightCircleSize',labels[i]);if(r > maxCircleSize)maxCircleSize = r;}var px=this.previousVerticalX_;ctx.clearRect(px - maxCircleSize - 1,0,2 * maxCircleSize + 2,this.height_);}if(this.selPoints_.length > 0){ // Draw colored circles over the center of each selected point
var canvasx=this.selPoints_[0].canvasx;ctx.save();for(i = 0;i < this.selPoints_.length;i++) {var pt=this.selPoints_[i];if(isNaN(pt.canvasy))continue;var circleSize=this.getNumericOption('highlightCircleSize',pt.name);var callback=this.getFunctionOption("drawHighlightPointCallback",pt.name);var color=this.plotter_.colors[pt.name];if(!callback){callback = utils.Circles.DEFAULT;}ctx.lineWidth = this.getNumericOption('strokeWidth',pt.name);ctx.strokeStyle = color;ctx.fillStyle = color;callback.call(this,this,pt.name,ctx,canvasx,pt.canvasy,color,circleSize,pt.idx);}ctx.restore();this.previousVerticalX_ = canvasx;}}; /**
 * Manually set the selected points and display information about them in the
 * legend. The selection can be cleared using clearSelection() and queried
 * using getSelection().
 *
 * To set a selected series but not a selected point, call setSelection with
 * row=false and the selected series name.
 *
 * @param {number} row Row number that should be highlighted (i.e. appear with
 * hover dots on the chart).
 * @param {seriesName} optional series name to highlight that series with the
 * the highlightSeriesOpts setting.
 * @param { locked } optional If true, keep seriesName selected when mousing
 * over the graph, disabling closest-series highlighting. Call clearSelection()
 * to unlock it.
 */Dygraph.prototype.setSelection = function(row,opt_seriesName,opt_locked){ // Extract the points we've selected
this.selPoints_ = [];var changed=false;if(row !== false && row >= 0){if(row != this.lastRow_)changed = true;this.lastRow_ = row;for(var setIdx=0;setIdx < this.layout_.points.length;++setIdx) {var points=this.layout_.points[setIdx]; // Check if the point at the appropriate index is the point we're looking
// for.  If it is, just use it, otherwise search the array for a point
// in the proper place.
var setRow=row - this.getLeftBoundary_(setIdx);if(setRow >= 0 && setRow < points.length && points[setRow].idx == row){var point=points[setRow];if(point.yval !== null)this.selPoints_.push(point);}else {for(var pointIdx=0;pointIdx < points.length;++pointIdx) {var point=points[pointIdx];if(point.idx == row){if(point.yval !== null){this.selPoints_.push(point);}break;}}}}}else {if(this.lastRow_ >= 0)changed = true;this.lastRow_ = -1;}if(this.selPoints_.length){this.lastx_ = this.selPoints_[0].xval;}else {this.lastx_ = -1;}if(opt_seriesName !== undefined){if(this.highlightSet_ !== opt_seriesName)changed = true;this.highlightSet_ = opt_seriesName;}if(opt_locked !== undefined){this.lockedSet_ = opt_locked;}if(changed){this.updateSelection_(undefined);}return changed;}; /**
 * The mouse has left the canvas. Clear out whatever artifacts remain
 * @param {Object} event the mouseout event from the browser.
 * @private
 */Dygraph.prototype.mouseOut_ = function(event){if(this.getFunctionOption("unhighlightCallback")){this.getFunctionOption("unhighlightCallback").call(this,event);}if(this.getBooleanOption("hideOverlayOnMouseOut") && !this.lockedSet_){this.clearSelection();}}; /**
 * Clears the current selection (i.e. points that were highlighted by moving
 * the mouse over the chart).
 */Dygraph.prototype.clearSelection = function(){this.cascadeEvents_('deselect',{});this.lockedSet_ = false; // Get rid of the overlay data
if(this.fadeLevel){this.animateSelection_(-1);return;}this.canvas_ctx_.clearRect(0,0,this.width_,this.height_);this.fadeLevel = 0;this.selPoints_ = [];this.lastx_ = -1;this.lastRow_ = -1;this.highlightSet_ = null;}; /**
 * Returns the number of the currently selected row. To get data for this row,
 * you can use the getValue method.
 * @return {number} row number, or -1 if nothing is selected
 */Dygraph.prototype.getSelection = function(){if(!this.selPoints_ || this.selPoints_.length < 1){return -1;}for(var setIdx=0;setIdx < this.layout_.points.length;setIdx++) {var points=this.layout_.points[setIdx];for(var row=0;row < points.length;row++) {if(points[row].x == this.selPoints_[0].x){return points[row].idx;}}}return -1;}; /**
 * Returns the name of the currently-highlighted series.
 * Only available when the highlightSeriesOpts option is in use.
 */Dygraph.prototype.getHighlightSeries = function(){return this.highlightSet_;}; /**
 * Returns true if the currently-highlighted series was locked
 * via setSelection(..., seriesName, true).
 */Dygraph.prototype.isSeriesLocked = function(){return this.lockedSet_;}; /**
 * Fires when there's data available to be graphed.
 * @param {string} data Raw CSV data to be plotted
 * @private
 */Dygraph.prototype.loadedEvent_ = function(data){this.rawData_ = this.parseCSV_(data);this.cascadeDataDidUpdateEvent_();this.predraw_();}; /**
 * Add ticks on the x-axis representing years, months, quarters, weeks, or days
 * @private
 */Dygraph.prototype.addXTicks_ = function(){ // Determine the correct ticks scale on the x-axis: quarterly, monthly, ...
var range;if(this.dateWindow_){range = [this.dateWindow_[0],this.dateWindow_[1]];}else {range = this.xAxisExtremes();}var xAxisOptionsView=this.optionsViewForAxis_('x');var xTicks=xAxisOptionsView('ticker')(range[0],range[1],this.plotter_.area.w, // TODO(danvk): should be area.width
xAxisOptionsView,this); // var msg = 'ticker(' + range[0] + ', ' + range[1] + ', ' + this.width_ + ', ' + this.attr_('pixelsPerXLabel') + ') -> ' + JSON.stringify(xTicks);
// console.log(msg);
this.layout_.setXTicks(xTicks);}; /**
 * Returns the correct handler class for the currently set options.
 * @private
 */Dygraph.prototype.getHandlerClass_ = function(){var handlerClass;if(this.attr_('dataHandler')){handlerClass = this.attr_('dataHandler');}else if(this.fractions_){if(this.getBooleanOption('errorBars')){handlerClass = _datahandlerBarsFractions2['default'];}else {handlerClass = _datahandlerDefaultFractions2['default'];}}else if(this.getBooleanOption('customBars')){handlerClass = _datahandlerBarsCustom2['default'];}else if(this.getBooleanOption('errorBars')){handlerClass = _datahandlerBarsError2['default'];}else {handlerClass = _datahandlerDefault2['default'];}return handlerClass;}; /**
 * @private
 * This function is called once when the chart's data is changed or the options
 * dictionary is updated. It is _not_ called when the user pans or zooms. The
 * idea is that values derived from the chart's data can be computed here,
 * rather than every time the chart is drawn. This includes things like the
 * number of axes, rolling averages, etc.
 */Dygraph.prototype.predraw_ = function(){var start=new Date(); // Create the correct dataHandler
this.dataHandler_ = new (this.getHandlerClass_())();this.layout_.computePlotArea(); // TODO(danvk): move more computations out of drawGraph_ and into here.
this.computeYAxes_();if(!this.is_initial_draw_){this.canvas_ctx_.restore();this.hidden_ctx_.restore();}this.canvas_ctx_.save();this.hidden_ctx_.save(); // Create a new plotter.
this.plotter_ = new _dygraphCanvas2['default'](this,this.hidden_,this.hidden_ctx_,this.layout_); // The roller sits in the bottom left corner of the chart. We don't know where
// this will be until the options are available, so it's positioned here.
this.createRollInterface_();this.cascadeEvents_('predraw'); // Convert the raw data (a 2D array) into the internal format and compute
// rolling averages.
this.rolledSeries_ = [null]; // x-axis is the first series and it's special
for(var i=1;i < this.numColumns();i++) { // var logScale = this.attr_('logscale', i); // TODO(klausw): this looks wrong // konigsberg thinks so too.
var series=this.dataHandler_.extractSeries(this.rawData_,i,this.attributes_);if(this.rollPeriod_ > 1){series = this.dataHandler_.rollingAverage(series,this.rollPeriod_,this.attributes_);}this.rolledSeries_.push(series);} // If the data or options have changed, then we'd better redraw.
this.drawGraph_(); // This is used to determine whether to do various animations.
var end=new Date();this.drawingTimeMs_ = end - start;}; /**
 * Point structure.
 *
 * xval_* and yval_* are the original unscaled data values,
 * while x_* and y_* are scaled to the range (0.0-1.0) for plotting.
 * yval_stacked is the cumulative Y value used for stacking graphs,
 * and bottom/top/minus/plus are used for error bar graphs.
 *
 * @typedef {{
 *     idx: number,
 *     name: string,
 *     x: ?number,
 *     xval: ?number,
 *     y_bottom: ?number,
 *     y: ?number,
 *     y_stacked: ?number,
 *     y_top: ?number,
 *     yval_minus: ?number,
 *     yval: ?number,
 *     yval_plus: ?number,
 *     yval_stacked
 * }}
 */Dygraph.PointType = undefined; /**
 * Calculates point stacking for stackedGraph=true.
 *
 * For stacking purposes, interpolate or extend neighboring data across
 * NaN values based on stackedGraphNaNFill settings. This is for display
 * only, the underlying data value as shown in the legend remains NaN.
 *
 * @param {Array.<Dygraph.PointType>} points Point array for a single series.
 *     Updates each Point's yval_stacked property.
 * @param {Array.<number>} cumulativeYval Accumulated top-of-graph stacked Y
 *     values for the series seen so far. Index is the row number. Updated
 *     based on the current series's values.
 * @param {Array.<number>} seriesExtremes Min and max values, updated
 *     to reflect the stacked values.
 * @param {string} fillMethod Interpolation method, one of 'all', 'inside', or
 *     'none'.
 * @private
 */Dygraph.stackPoints_ = function(points,cumulativeYval,seriesExtremes,fillMethod){var lastXval=null;var prevPoint=null;var nextPoint=null;var nextPointIdx=-1; // Find the next stackable point starting from the given index.
var updateNextPoint=function updateNextPoint(idx){ // If we've previously found a non-NaN point and haven't gone past it yet,
// just use that.
if(nextPointIdx >= idx)return; // We haven't found a non-NaN point yet or have moved past it,
// look towards the right to find a non-NaN point.
for(var j=idx;j < points.length;++j) { // Clear out a previously-found point (if any) since it's no longer
// valid, we shouldn't use it for interpolation anymore.
nextPoint = null;if(!isNaN(points[j].yval) && points[j].yval !== null){nextPointIdx = j;nextPoint = points[j];break;}}};for(var i=0;i < points.length;++i) {var point=points[i];var xval=point.xval;if(cumulativeYval[xval] === undefined){cumulativeYval[xval] = 0;}var actualYval=point.yval;if(isNaN(actualYval) || actualYval === null){if(fillMethod == 'none'){actualYval = 0;}else { // Interpolate/extend for stacking purposes if possible.
updateNextPoint(i);if(prevPoint && nextPoint && fillMethod != 'none'){ // Use linear interpolation between prevPoint and nextPoint.
actualYval = prevPoint.yval + (nextPoint.yval - prevPoint.yval) * ((xval - prevPoint.xval) / (nextPoint.xval - prevPoint.xval));}else if(prevPoint && fillMethod == 'all'){actualYval = prevPoint.yval;}else if(nextPoint && fillMethod == 'all'){actualYval = nextPoint.yval;}else {actualYval = 0;}}}else {prevPoint = point;}var stackedYval=cumulativeYval[xval];if(lastXval != xval){ // If an x-value is repeated, we ignore the duplicates.
stackedYval += actualYval;cumulativeYval[xval] = stackedYval;}lastXval = xval;point.yval_stacked = stackedYval;if(stackedYval > seriesExtremes[1]){seriesExtremes[1] = stackedYval;}if(stackedYval < seriesExtremes[0]){seriesExtremes[0] = stackedYval;}}}; /**
 * Loop over all fields and create datasets, calculating extreme y-values for
 * each series and extreme x-indices as we go.
 *
 * dateWindow is passed in as an explicit parameter so that we can compute
 * extreme values "speculatively", i.e. without actually setting state on the
 * dygraph.
 *
 * @param {Array.<Array.<Array.<(number|Array<number>)>>} rolledSeries, where
 *     rolledSeries[seriesIndex][row] = raw point, where
 *     seriesIndex is the column number starting with 1, and
 *     rawPoint is [x,y] or [x, [y, err]] or [x, [y, yminus, yplus]].
 * @param {?Array.<number>} dateWindow [xmin, xmax] pair, or null.
 * @return {{
 *     points: Array.<Array.<Dygraph.PointType>>,
 *     seriesExtremes: Array.<Array.<number>>,
 *     boundaryIds: Array.<number>}}
 * @private
 */Dygraph.prototype.gatherDatasets_ = function(rolledSeries,dateWindow){var boundaryIds=[];var points=[];var cumulativeYval=[]; // For stacked series.
var extremes={}; // series name -> [low, high]
var seriesIdx,sampleIdx;var firstIdx,lastIdx;var axisIdx; // Loop over the fields (series).  Go from the last to the first,
// because if they're stacked that's how we accumulate the values.
var num_series=rolledSeries.length - 1;var series;for(seriesIdx = num_series;seriesIdx >= 1;seriesIdx--) {if(!this.visibility()[seriesIdx - 1])continue; // Prune down to the desired range, if necessary (for zooming)
// Because there can be lines going to points outside of the visible area,
// we actually prune to visible points, plus one on either side.
if(dateWindow){series = rolledSeries[seriesIdx];var low=dateWindow[0];var high=dateWindow[1]; // TODO(danvk): do binary search instead of linear search.
// TODO(danvk): pass firstIdx and lastIdx directly to the renderer.
firstIdx = null;lastIdx = null;for(sampleIdx = 0;sampleIdx < series.length;sampleIdx++) {if(series[sampleIdx][0] >= low && firstIdx === null){firstIdx = sampleIdx;}if(series[sampleIdx][0] <= high){lastIdx = sampleIdx;}}if(firstIdx === null)firstIdx = 0;var correctedFirstIdx=firstIdx;var isInvalidValue=true;while(isInvalidValue && correctedFirstIdx > 0) {correctedFirstIdx--; // check if the y value is null.
isInvalidValue = series[correctedFirstIdx][1] === null;}if(lastIdx === null)lastIdx = series.length - 1;var correctedLastIdx=lastIdx;isInvalidValue = true;while(isInvalidValue && correctedLastIdx < series.length - 1) {correctedLastIdx++;isInvalidValue = series[correctedLastIdx][1] === null;}if(correctedFirstIdx !== firstIdx){firstIdx = correctedFirstIdx;}if(correctedLastIdx !== lastIdx){lastIdx = correctedLastIdx;}boundaryIds[seriesIdx - 1] = [firstIdx,lastIdx]; // .slice's end is exclusive, we want to include lastIdx.
series = series.slice(firstIdx,lastIdx + 1);}else {series = rolledSeries[seriesIdx];boundaryIds[seriesIdx - 1] = [0,series.length - 1];}var seriesName=this.attr_("labels")[seriesIdx];var seriesExtremes=this.dataHandler_.getExtremeYValues(series,dateWindow,this.getBooleanOption("stepPlot",seriesName));var seriesPoints=this.dataHandler_.seriesToPoints(series,seriesName,boundaryIds[seriesIdx - 1][0]);if(this.getBooleanOption("stackedGraph")){axisIdx = this.attributes_.axisForSeries(seriesName);if(cumulativeYval[axisIdx] === undefined){cumulativeYval[axisIdx] = [];}Dygraph.stackPoints_(seriesPoints,cumulativeYval[axisIdx],seriesExtremes,this.getBooleanOption("stackedGraphNaNFill"));}extremes[seriesName] = seriesExtremes;points[seriesIdx] = seriesPoints;}return {points:points,extremes:extremes,boundaryIds:boundaryIds};}; /**
 * Update the graph with new data. This method is called when the viewing area
 * has changed. If the underlying data or options have changed, predraw_ will
 * be called before drawGraph_ is called.
 *
 * @private
 */Dygraph.prototype.drawGraph_ = function(){var start=new Date(); // This is used to set the second parameter to drawCallback, below.
var is_initial_draw=this.is_initial_draw_;this.is_initial_draw_ = false;this.layout_.removeAllDatasets();this.setColors_();this.attrs_.pointSize = 0.5 * this.getNumericOption('highlightCircleSize');var packed=this.gatherDatasets_(this.rolledSeries_,this.dateWindow_);var points=packed.points;var extremes=packed.extremes;this.boundaryIds_ = packed.boundaryIds;this.setIndexByName_ = {};var labels=this.attr_("labels");var dataIdx=0;for(var i=1;i < points.length;i++) {if(!this.visibility()[i - 1])continue;this.layout_.addDataset(labels[i],points[i]);this.datasetIndex_[i] = dataIdx++;}for(var i=0;i < labels.length;i++) {this.setIndexByName_[labels[i]] = i;}this.computeYAxisRanges_(extremes);this.layout_.setYAxes(this.axes_);this.addXTicks_(); // Tell PlotKit to use this new data and render itself
this.layout_.evaluate();this.renderGraph_(is_initial_draw);if(this.getStringOption("timingName")){var end=new Date();console.log(this.getStringOption("timingName") + " - drawGraph: " + (end - start) + "ms");}}; /**
 * This does the work of drawing the chart. It assumes that the layout and axis
 * scales have already been set (e.g. by predraw_).
 *
 * @private
 */Dygraph.prototype.renderGraph_ = function(is_initial_draw){this.cascadeEvents_('clearChart');this.plotter_.clear();var underlayCallback=this.getFunctionOption('underlayCallback');if(underlayCallback){ // NOTE: we pass the dygraph object to this callback twice to avoid breaking
// users who expect a deprecated form of this callback.
underlayCallback.call(this,this.hidden_ctx_,this.layout_.getPlotArea(),this,this);}var e={canvas:this.hidden_,drawingContext:this.hidden_ctx_};this.cascadeEvents_('willDrawChart',e);this.plotter_.render();this.cascadeEvents_('didDrawChart',e);this.lastRow_ = -1; // because plugins/legend.js clears the legend
// TODO(danvk): is this a performance bottleneck when panning?
// The interaction canvas should already be empty in that situation.
this.canvas_.getContext('2d').clearRect(0,0,this.width_,this.height_);var drawCallback=this.getFunctionOption("drawCallback");if(drawCallback !== null){drawCallback.call(this,this,is_initial_draw);}if(is_initial_draw){this.readyFired_ = true;while(this.readyFns_.length > 0) {var fn=this.readyFns_.pop();fn(this);}}}; /**
 * @private
 * Determine properties of the y-axes which are independent of the data
 * currently being displayed. This includes things like the number of axes and
 * the style of the axes. It does not include the range of each axis and its
 * tick marks.
 * This fills in this.axes_.
 * axes_ = [ { options } ]
 *   indices are into the axes_ array.
 */Dygraph.prototype.computeYAxes_ = function(){var axis,index,opts,v; // this.axes_ doesn't match this.attributes_.axes_.options. It's used for
// data computation as well as options storage.
// Go through once and add all the axes.
this.axes_ = [];for(axis = 0;axis < this.attributes_.numAxes();axis++) { // Add a new axis, making a copy of its per-axis options.
opts = {g:this};utils.update(opts,this.attributes_.axisOptions(axis));this.axes_[axis] = opts;}for(axis = 0;axis < this.axes_.length;axis++) {if(axis === 0){opts = this.optionsViewForAxis_('y' + (axis?'2':''));v = opts("valueRange");if(v)this.axes_[axis].valueRange = v;}else { // To keep old behavior
var axes=this.user_attrs_.axes;if(axes && axes.y2){v = axes.y2.valueRange;if(v)this.axes_[axis].valueRange = v;}}}}; /**
 * Returns the number of y-axes on the chart.
 * @return {number} the number of axes.
 */Dygraph.prototype.numAxes = function(){return this.attributes_.numAxes();}; /**
 * @private
 * Returns axis properties for the given series.
 * @param {string} setName The name of the series for which to get axis
 * properties, e.g. 'Y1'.
 * @return {Object} The axis properties.
 */Dygraph.prototype.axisPropertiesForSeries = function(series){ // TODO(danvk): handle errors.
return this.axes_[this.attributes_.axisForSeries(series)];}; /**
 * @private
 * Determine the value range and tick marks for each axis.
 * @param {Object} extremes A mapping from seriesName -> [low, high]
 * This fills in the valueRange and ticks fields in each entry of this.axes_.
 */Dygraph.prototype.computeYAxisRanges_ = function(extremes){var isNullUndefinedOrNaN=function isNullUndefinedOrNaN(num){return isNaN(parseFloat(num));};var numAxes=this.attributes_.numAxes();var ypadCompat,span,series,ypad;var p_axis; // Compute extreme values, a span and tick marks for each axis.
for(var i=0;i < numAxes;i++) {var axis=this.axes_[i];var logscale=this.attributes_.getForAxis("logscale",i);var includeZero=this.attributes_.getForAxis("includeZero",i);var independentTicks=this.attributes_.getForAxis("independentTicks",i);series = this.attributes_.seriesForAxis(i); // Add some padding. This supports two Y padding operation modes:
//
// - backwards compatible (yRangePad not set):
//   10% padding for automatic Y ranges, but not for user-supplied
//   ranges, and move a close-to-zero edge to zero, since drawing at the edge
//   results in invisible lines. Unfortunately lines drawn at the edge of a
//   user-supplied range will still be invisible. If logscale is
//   set, add a variable amount of padding at the top but
//   none at the bottom.
//
// - new-style (yRangePad set by the user):
//   always add the specified Y padding.
//
ypadCompat = true;ypad = 0.1; // add 10%
var yRangePad=this.getNumericOption('yRangePad');if(yRangePad !== null){ypadCompat = false; // Convert pixel padding to ratio
ypad = yRangePad / this.plotter_.area.h;}if(series.length === 0){ // If no series are defined or visible then use a reasonable default
axis.extremeRange = [0,1];}else { // Calculate the extremes of extremes.
var minY=Infinity; // extremes[series[0]][0];
var maxY=-Infinity; // extremes[series[0]][1];
var extremeMinY,extremeMaxY;for(var j=0;j < series.length;j++) { // this skips invisible series
if(!extremes.hasOwnProperty(series[j]))continue; // Only use valid extremes to stop null data series' from corrupting the scale.
extremeMinY = extremes[series[j]][0];if(extremeMinY !== null){minY = Math.min(extremeMinY,minY);}extremeMaxY = extremes[series[j]][1];if(extremeMaxY !== null){maxY = Math.max(extremeMaxY,maxY);}} // Include zero if requested by the user.
if(includeZero && !logscale){if(minY > 0)minY = 0;if(maxY < 0)maxY = 0;} // Ensure we have a valid scale, otherwise default to [0, 1] for safety.
if(minY == Infinity)minY = 0;if(maxY == -Infinity)maxY = 1;span = maxY - minY; // special case: if we have no sense of scale, center on the sole value.
if(span === 0){if(maxY !== 0){span = Math.abs(maxY);}else { // ... and if the sole value is zero, use range 0-1.
maxY = 1;span = 1;}}var maxAxisY=maxY,minAxisY=minY;if(ypadCompat){if(logscale){maxAxisY = maxY + ypad * span;minAxisY = minY;}else {maxAxisY = maxY + ypad * span;minAxisY = minY - ypad * span; // Backwards-compatible behavior: Move the span to start or end at zero if it's
// close to zero.
if(minAxisY < 0 && minY >= 0)minAxisY = 0;if(maxAxisY > 0 && maxY <= 0)maxAxisY = 0;}}axis.extremeRange = [minAxisY,maxAxisY];}if(axis.valueRange){ // This is a user-set value range for this axis.
var y0=isNullUndefinedOrNaN(axis.valueRange[0])?axis.extremeRange[0]:axis.valueRange[0];var y1=isNullUndefinedOrNaN(axis.valueRange[1])?axis.extremeRange[1]:axis.valueRange[1];axis.computedValueRange = [y0,y1];}else {axis.computedValueRange = axis.extremeRange;}if(!ypadCompat){ // When using yRangePad, adjust the upper/lower bounds to add
// padding unless the user has zoomed/panned the Y axis range.
if(logscale){y0 = axis.computedValueRange[0];y1 = axis.computedValueRange[1];var y0pct=ypad / (2 * ypad - 1);var y1pct=(ypad - 1) / (2 * ypad - 1);axis.computedValueRange[0] = utils.logRangeFraction(y0,y1,y0pct);axis.computedValueRange[1] = utils.logRangeFraction(y0,y1,y1pct);}else {y0 = axis.computedValueRange[0];y1 = axis.computedValueRange[1];span = y1 - y0;axis.computedValueRange[0] = y0 - span * ypad;axis.computedValueRange[1] = y1 + span * ypad;}}if(independentTicks){axis.independentTicks = independentTicks;var opts=this.optionsViewForAxis_('y' + (i?'2':''));var ticker=opts('ticker');axis.ticks = ticker(axis.computedValueRange[0],axis.computedValueRange[1],this.plotter_.area.h,opts,this); // Define the first independent axis as primary axis.
if(!p_axis)p_axis = axis;}}if(p_axis === undefined){throw "Configuration Error: At least one axis has to have the \\"independentTicks\\" option activated.";} // Add ticks. By default, all axes inherit the tick positions of the
// primary axis. However, if an axis is specifically marked as having
// independent ticks, then that is permissible as well.
for(var i=0;i < numAxes;i++) {var axis=this.axes_[i];if(!axis.independentTicks){var opts=this.optionsViewForAxis_('y' + (i?'2':''));var ticker=opts('ticker');var p_ticks=p_axis.ticks;var p_scale=p_axis.computedValueRange[1] - p_axis.computedValueRange[0];var scale=axis.computedValueRange[1] - axis.computedValueRange[0];var tick_values=[];for(var k=0;k < p_ticks.length;k++) {var y_frac=(p_ticks[k].v - p_axis.computedValueRange[0]) / p_scale;var y_val=axis.computedValueRange[0] + y_frac * scale;tick_values.push(y_val);}axis.ticks = ticker(axis.computedValueRange[0],axis.computedValueRange[1],this.plotter_.area.h,opts,this,tick_values);}}}; /**
 * Detects the type of the str (date or numeric) and sets the various
 * formatting attributes in this.attrs_ based on this type.
 * @param {string} str An x value.
 * @private
 */Dygraph.prototype.detectTypeFromString_ = function(str){var isDate=false;var dashPos=str.indexOf('-'); // could be 2006-01-01 _or_ 1.0e-2
if(dashPos > 0 && str[dashPos - 1] != 'e' && str[dashPos - 1] != 'E' || str.indexOf('/') >= 0 || isNaN(parseFloat(str))){isDate = true;}else if(str.length == 8 && str > '19700101' && str < '20371231'){ // TODO(danvk): remove support for this format.
isDate = true;}this.setXAxisOptions_(isDate);};Dygraph.prototype.setXAxisOptions_ = function(isDate){if(isDate){this.attrs_.xValueParser = utils.dateParser;this.attrs_.axes.x.valueFormatter = utils.dateValueFormatter;this.attrs_.axes.x.ticker = DygraphTickers.dateTicker;this.attrs_.axes.x.axisLabelFormatter = utils.dateAxisLabelFormatter;}else { /** @private (shut up, jsdoc!) */this.attrs_.xValueParser = function(x){return parseFloat(x);}; // TODO(danvk): use Dygraph.numberValueFormatter here?
/** @private (shut up, jsdoc!) */this.attrs_.axes.x.valueFormatter = function(x){return x;};this.attrs_.axes.x.ticker = DygraphTickers.numericTicks;this.attrs_.axes.x.axisLabelFormatter = this.attrs_.axes.x.valueFormatter;}}; /**
 * @private
 * Parses a string in a special csv format.  We expect a csv file where each
 * line is a date point, and the first field in each line is the date string.
 * We also expect that all remaining fields represent series.
 * if the errorBars attribute is set, then interpret the fields as:
 * date, series1, stddev1, series2, stddev2, ...
 * @param {[Object]} data See above.
 *
 * @return [Object] An array with one entry for each row. These entries
 * are an array of cells in that row. The first entry is the parsed x-value for
 * the row. The second, third, etc. are the y-values. These can take on one of
 * three forms, depending on the CSV and constructor parameters:
 * 1. numeric value
 * 2. [ value, stddev ]
 * 3. [ low value, center value, high value ]
 */Dygraph.prototype.parseCSV_ = function(data){var ret=[];var line_delimiter=utils.detectLineDelimiter(data);var lines=data.split(line_delimiter || "\\n");var vals,j; // Use the default delimiter or fall back to a tab if that makes sense.
var delim=this.getStringOption('delimiter');if(lines[0].indexOf(delim) == -1 && lines[0].indexOf('\t') >= 0){delim = '\t';}var start=0;if(!('labels' in this.user_attrs_)){ // User hasn't explicitly set labels, so they're (presumably) in the CSV.
start = 1;this.attrs_.labels = lines[0].split(delim); // NOTE: _not_ user_attrs_.
this.attributes_.reparseSeries();}var line_no=0;var xParser;var defaultParserSet=false; // attempt to auto-detect x value type
var expectedCols=this.attr_("labels").length;var outOfOrder=false;for(var i=start;i < lines.length;i++) {var line=lines[i];line_no = i;if(line.length === 0)continue; // skip blank lines
if(line[0] == '#')continue; // skip comment lines
var inFields=line.split(delim);if(inFields.length < 2)continue;var fields=[];if(!defaultParserSet){this.detectTypeFromString_(inFields[0]);xParser = this.getFunctionOption("xValueParser");defaultParserSet = true;}fields[0] = xParser(inFields[0],this); // If fractions are expected, parse the numbers as "A/B"
if(this.fractions_){for(j = 1;j < inFields.length;j++) { // TODO(danvk): figure out an appropriate way to flag parse errors.
vals = inFields[j].split("/");if(vals.length != 2){console.error('Expected fractional "num/den" values in CSV data ' + "but found a value '" + inFields[j] + "' on line " + (1 + i) + " ('" + line + "') which is not of this form.");fields[j] = [0,0];}else {fields[j] = [utils.parseFloat_(vals[0],i,line),utils.parseFloat_(vals[1],i,line)];}}}else if(this.getBooleanOption("errorBars")){ // If there are error bars, values are (value, stddev) pairs
if(inFields.length % 2 != 1){console.error('Expected alternating (value, stdev.) pairs in CSV data ' + 'but line ' + (1 + i) + ' has an odd number of values (' + (inFields.length - 1) + "): '" + line + "'");}for(j = 1;j < inFields.length;j += 2) {fields[(j + 1) / 2] = [utils.parseFloat_(inFields[j],i,line),utils.parseFloat_(inFields[j + 1],i,line)];}}else if(this.getBooleanOption("customBars")){ // Bars are a low;center;high tuple
for(j = 1;j < inFields.length;j++) {var val=inFields[j];if(/^ *$/.test(val)){fields[j] = [null,null,null];}else {vals = val.split(";");if(vals.length == 3){fields[j] = [utils.parseFloat_(vals[0],i,line),utils.parseFloat_(vals[1],i,line),utils.parseFloat_(vals[2],i,line)];}else {console.warn('When using customBars, values must be either blank ' + 'or "low;center;high" tuples (got "' + val + '" on line ' + (1 + i));}}}}else { // Values are just numbers
for(j = 1;j < inFields.length;j++) {fields[j] = utils.parseFloat_(inFields[j],i,line);}}if(ret.length > 0 && fields[0] < ret[ret.length - 1][0]){outOfOrder = true;}if(fields.length != expectedCols){console.error("Number of columns in line " + i + " (" + fields.length + ") does not agree with number of labels (" + expectedCols + ") " + line);} // If the user specified the 'labels' option and none of the cells of the
// first row parsed correctly, then they probably double-specified the
// labels. We go with the values set in the option, discard this row and
// log a warning to the JS console.
if(i === 0 && this.attr_('labels')){var all_null=true;for(j = 0;all_null && j < fields.length;j++) {if(fields[j])all_null = false;}if(all_null){console.warn("The dygraphs 'labels' option is set, but the first row " + "of CSV data ('" + line + "') appears to also contain " + "labels. Will drop the CSV labels and use the option " + "labels.");continue;}}ret.push(fields);}if(outOfOrder){console.warn("CSV is out of order; order it correctly to speed loading.");ret.sort(function(a,b){return a[0] - b[0];});}return ret;}; // In native format, all values must be dates or numbers.
// This check isn't perfect but will catch most mistaken uses of strings.
function validateNativeFormat(data){var firstRow=data[0];var firstX=firstRow[0];if(typeof firstX !== 'number' && !utils.isDateLike(firstX)){throw new Error('Expected number or date but got ' + typeof firstX + ': ' + firstX + '.');}for(var i=1;i < firstRow.length;i++) {var val=firstRow[i];if(val === null || val === undefined)continue;if(typeof val === 'number')continue;if(utils.isArrayLike(val))continue; // e.g. error bars or custom bars.
throw new Error('Expected number or array but got ' + typeof val + ': ' + val + '.');}} /**
 * The user has provided their data as a pre-packaged JS array. If the x values
 * are numeric, this is the same as dygraphs' internal format. If the x values
 * are dates, we need to convert them from Date objects to ms since epoch.
 * @param {!Array} data
 * @return {Object} data with numeric x values.
 * @private
 */Dygraph.prototype.parseArray_ = function(data){ // Peek at the first x value to see if it's numeric.
if(data.length === 0){console.error("Can't plot empty data set");return null;}if(data[0].length === 0){console.error("Data set cannot contain an empty row");return null;}validateNativeFormat(data);var i;if(this.attr_("labels") === null){console.warn("Using default labels. Set labels explicitly via 'labels' " + "in the options parameter");this.attrs_.labels = ["X"];for(i = 1;i < data[0].length;i++) {this.attrs_.labels.push("Y" + i); // Not user_attrs_.
}this.attributes_.reparseSeries();}else {var num_labels=this.attr_("labels");if(num_labels.length != data[0].length){console.error("Mismatch between number of labels (" + num_labels + ")" + " and number of columns in array (" + data[0].length + ")");return null;}}if(utils.isDateLike(data[0][0])){ // Some intelligent defaults for a date x-axis.
this.attrs_.axes.x.valueFormatter = utils.dateValueFormatter;this.attrs_.axes.x.ticker = DygraphTickers.dateTicker;this.attrs_.axes.x.axisLabelFormatter = utils.dateAxisLabelFormatter; // Assume they're all dates.
var parsedData=utils.clone(data);for(i = 0;i < data.length;i++) {if(parsedData[i].length === 0){console.error("Row " + (1 + i) + " of data is empty");return null;}if(parsedData[i][0] === null || typeof parsedData[i][0].getTime != 'function' || isNaN(parsedData[i][0].getTime())){console.error("x value in row " + (1 + i) + " is not a Date");return null;}parsedData[i][0] = parsedData[i][0].getTime();}return parsedData;}else { // Some intelligent defaults for a numeric x-axis.
/** @private (shut up, jsdoc!) */this.attrs_.axes.x.valueFormatter = function(x){return x;};this.attrs_.axes.x.ticker = DygraphTickers.numericTicks;this.attrs_.axes.x.axisLabelFormatter = utils.numberAxisLabelFormatter;return data;}}; /**
 * Parses a DataTable object from gviz.
 * The data is expected to have a first column that is either a date or a
 * number. All subsequent columns must be numbers. If there is a clear mismatch
 * between this.xValueParser_ and the type of the first column, it will be
 * fixed. Fills out rawData_.
 * @param {!google.visualization.DataTable} data See above.
 * @private
 */Dygraph.prototype.parseDataTable_ = function(data){var shortTextForAnnotationNum=function shortTextForAnnotationNum(num){ // converts [0-9]+ [A-Z][a-z]*
// example: 0=A, 1=B, 25=Z, 26=Aa, 27=Ab
// and continues like.. Ba Bb .. Za .. Zz..Aaa...Zzz Aaaa Zzzz
var shortText=String.fromCharCode(65 /* A */ + num % 26);num = Math.floor(num / 26);while(num > 0) {shortText = String.fromCharCode(65 /* A */ + (num - 1) % 26) + shortText.toLowerCase();num = Math.floor((num - 1) / 26);}return shortText;};var cols=data.getNumberOfColumns();var rows=data.getNumberOfRows();var indepType=data.getColumnType(0);if(indepType == 'date' || indepType == 'datetime'){this.attrs_.xValueParser = utils.dateParser;this.attrs_.axes.x.valueFormatter = utils.dateValueFormatter;this.attrs_.axes.x.ticker = DygraphTickers.dateTicker;this.attrs_.axes.x.axisLabelFormatter = utils.dateAxisLabelFormatter;}else if(indepType == 'number'){this.attrs_.xValueParser = function(x){return parseFloat(x);};this.attrs_.axes.x.valueFormatter = function(x){return x;};this.attrs_.axes.x.ticker = DygraphTickers.numericTicks;this.attrs_.axes.x.axisLabelFormatter = this.attrs_.axes.x.valueFormatter;}else {throw new Error("only 'date', 'datetime' and 'number' types are supported " + "for column 1 of DataTable input (Got '" + indepType + "')");} // Array of the column indices which contain data (and not annotations).
var colIdx=[];var annotationCols={}; // data index -> [annotation cols]
var hasAnnotations=false;var i,j;for(i = 1;i < cols;i++) {var type=data.getColumnType(i);if(type == 'number'){colIdx.push(i);}else if(type == 'string' && this.getBooleanOption('displayAnnotations')){ // This is OK -- it's an annotation column.
var dataIdx=colIdx[colIdx.length - 1];if(!annotationCols.hasOwnProperty(dataIdx)){annotationCols[dataIdx] = [i];}else {annotationCols[dataIdx].push(i);}hasAnnotations = true;}else {throw new Error("Only 'number' is supported as a dependent type with Gviz." + " 'string' is only supported if displayAnnotations is true");}} // Read column labels
// TODO(danvk): add support back for errorBars
var labels=[data.getColumnLabel(0)];for(i = 0;i < colIdx.length;i++) {labels.push(data.getColumnLabel(colIdx[i]));if(this.getBooleanOption("errorBars"))i += 1;}this.attrs_.labels = labels;cols = labels.length;var ret=[];var outOfOrder=false;var annotations=[];for(i = 0;i < rows;i++) {var row=[];if(typeof data.getValue(i,0) === 'undefined' || data.getValue(i,0) === null){console.warn("Ignoring row " + i + " of DataTable because of undefined or null first column.");continue;}if(indepType == 'date' || indepType == 'datetime'){row.push(data.getValue(i,0).getTime());}else {row.push(data.getValue(i,0));}if(!this.getBooleanOption("errorBars")){for(j = 0;j < colIdx.length;j++) {var col=colIdx[j];row.push(data.getValue(i,col));if(hasAnnotations && annotationCols.hasOwnProperty(col) && data.getValue(i,annotationCols[col][0]) !== null){var ann={};ann.series = data.getColumnLabel(col);ann.xval = row[0];ann.shortText = shortTextForAnnotationNum(annotations.length);ann.text = '';for(var k=0;k < annotationCols[col].length;k++) {if(k)ann.text += "\\n";ann.text += data.getValue(i,annotationCols[col][k]);}annotations.push(ann);}} // Strip out infinities, which give dygraphs problems later on.
for(j = 0;j < row.length;j++) {if(!isFinite(row[j]))row[j] = null;}}else {for(j = 0;j < cols - 1;j++) {row.push([data.getValue(i,1 + 2 * j),data.getValue(i,2 + 2 * j)]);}}if(ret.length > 0 && row[0] < ret[ret.length - 1][0]){outOfOrder = true;}ret.push(row);}if(outOfOrder){console.warn("DataTable is out of order; order it correctly to speed loading.");ret.sort(function(a,b){return a[0] - b[0];});}this.rawData_ = ret;if(annotations.length > 0){this.setAnnotations(annotations,true);}this.attributes_.reparseSeries();}; /**
 * Signals to plugins that the chart data has updated.
 * This happens after the data has updated but before the chart has redrawn.
 * @private
 */Dygraph.prototype.cascadeDataDidUpdateEvent_ = function(){ // TODO(danvk): there are some issues checking xAxisRange() and using
// toDomCoords from handlers of this event. The visible range should be set
// when the chart is drawn, not derived from the data.
this.cascadeEvents_('dataDidUpdate',{});}; /**
 * Get the CSV data. If it's in a function, call that function. If it's in a
 * file, do an XMLHttpRequest to get it.
 * @private
 */Dygraph.prototype.start_ = function(){var data=this.file_; // Functions can return references of all other types.
if(typeof data == 'function'){data = data();}if(utils.isArrayLike(data)){this.rawData_ = this.parseArray_(data);this.cascadeDataDidUpdateEvent_();this.predraw_();}else if(typeof data == 'object' && typeof data.getColumnRange == 'function'){ // must be a DataTable from gviz.
this.parseDataTable_(data);this.cascadeDataDidUpdateEvent_();this.predraw_();}else if(typeof data == 'string'){ // Heuristic: a newline means it's CSV data. Otherwise it's an URL.
var line_delimiter=utils.detectLineDelimiter(data);if(line_delimiter){this.loadedEvent_(data);}else { // REMOVE_FOR_IE
var req;if(window.XMLHttpRequest){ // Firefox, Opera, IE7, and other browsers will use the native object
req = new XMLHttpRequest();}else { // IE 5 and 6 will use the ActiveX control
req = new ActiveXObject("Microsoft.XMLHTTP");}var caller=this;req.onreadystatechange = function(){if(req.readyState == 4){if(req.status === 200 ||  // Normal http
req.status === 0){ // Chrome w/ --allow-file-access-from-files
caller.loadedEvent_(req.responseText);}}};req.open("GET",data,true);req.send(null);}}else {console.error("Unknown data format: " + typeof data);}}; /**
 * Changes various properties of the graph. These can include:
 * <ul>
 * <li>file: changes the source data for the graph</li>
 * <li>errorBars: changes whether the data contains stddev</li>
 * </ul>
 *
 * There's a huge variety of options that can be passed to this method. For a
 * full list, see http://dygraphs.com/options.html.
 *
 * @param {Object} input_attrs The new properties and values
 * @param {boolean} block_redraw Usually the chart is redrawn after every
 *     call to updateOptions(). If you know better, you can pass true to
 *     explicitly block the redraw. This can be useful for chaining
 *     updateOptions() calls, avoiding the occasional infinite loop and
 *     preventing redraws when it's not necessary (e.g. when updating a
 *     callback).
 */Dygraph.prototype.updateOptions = function(input_attrs,block_redraw){if(typeof block_redraw == 'undefined')block_redraw = false; // copyUserAttrs_ drops the "file" parameter as a convenience to us.
var file=input_attrs.file;var attrs=Dygraph.copyUserAttrs_(input_attrs); // TODO(danvk): this is a mess. Move these options into attr_.
if('rollPeriod' in attrs){this.rollPeriod_ = attrs.rollPeriod;}if('dateWindow' in attrs){this.dateWindow_ = attrs.dateWindow;} // TODO(danvk): validate per-series options.
// Supported:
// strokeWidth
// pointSize
// drawPoints
// highlightCircleSize
// Check if this set options will require new points.
var requiresNewPoints=utils.isPixelChangingOptionList(this.attr_("labels"),attrs);utils.updateDeep(this.user_attrs_,attrs);this.attributes_.reparseSeries();if(file){ // This event indicates that the data is about to change, but hasn't yet.
// TODO(danvk): support cancellation of the update via this event.
this.cascadeEvents_('dataWillUpdate',{});this.file_ = file;if(!block_redraw)this.start_();}else {if(!block_redraw){if(requiresNewPoints){this.predraw_();}else {this.renderGraph_(false);}}}}; /**
 * Make a copy of input attributes, removing file as a convenience.
 * @private
 */Dygraph.copyUserAttrs_ = function(attrs){var my_attrs={};for(var k in attrs) {if(!attrs.hasOwnProperty(k))continue;if(k == 'file')continue;if(attrs.hasOwnProperty(k))my_attrs[k] = attrs[k];}return my_attrs;}; /**
 * Resizes the dygraph. If no parameters are specified, resizes to fill the
 * containing div (which has presumably changed size since the dygraph was
 * instantiated. If the width/height are specified, the div will be resized.
 *
 * This is far more efficient than destroying and re-instantiating a
 * Dygraph, since it doesn't have to reparse the underlying data.
 *
 * @param {number} width Width (in pixels)
 * @param {number} height Height (in pixels)
 */Dygraph.prototype.resize = function(width,height){if(this.resize_lock){return;}this.resize_lock = true;if(width === null != (height === null)){console.warn("Dygraph.resize() should be called with zero parameters or " + "two non-NULL parameters. Pretending it was zero.");width = height = null;}var old_width=this.width_;var old_height=this.height_;if(width){this.maindiv_.style.width = width + "px";this.maindiv_.style.height = height + "px";this.width_ = width;this.height_ = height;}else {this.width_ = this.maindiv_.clientWidth;this.height_ = this.maindiv_.clientHeight;}if(old_width != this.width_ || old_height != this.height_){ // Resizing a canvas erases it, even when the size doesn't change, so
// any resize needs to be followed by a redraw.
this.resizeElements_();this.predraw_();}this.resize_lock = false;}; /**
 * Adjusts the number of points in the rolling average. Updates the graph to
 * reflect the new averaging period.
 * @param {number} length Number of points over which to average the data.
 */Dygraph.prototype.adjustRoll = function(length){this.rollPeriod_ = length;this.predraw_();}; /**
 * Returns a boolean array of visibility statuses.
 */Dygraph.prototype.visibility = function(){ // Do lazy-initialization, so that this happens after we know the number of
// data series.
if(!this.getOption("visibility")){this.attrs_.visibility = [];} // TODO(danvk): it looks like this could go into an infinite loop w/ user_attrs.
while(this.getOption("visibility").length < this.numColumns() - 1) {this.attrs_.visibility.push(true);}return this.getOption("visibility");}; /**
 * Changes the visibility of one or more series.
 *
 * @param {number|number[]|object} num the series index or an array of series indices
 *                                     or a boolean array of visibility states by index
 *                                     or an object mapping series numbers, as keys, to
 *                                     visibility state (boolean values)
 * @param {boolean} value the visibility state expressed as a boolean
 */Dygraph.prototype.setVisibility = function(num,value){var x=this.visibility();var numIsObject=false;if(!Array.isArray(num)){if(num !== null && typeof num === 'object'){numIsObject = true;}else {num = [num];}}if(numIsObject){for(var i in num) {if(num.hasOwnProperty(i)){if(i < 0 || i >= x.length){console.warn("Invalid series number in setVisibility: " + i);}else {x[i] = num[i];}}}}else {for(var i=0;i < num.length;i++) {if(typeof num[i] === 'boolean'){if(i >= x.length){console.warn("Invalid series number in setVisibility: " + i);}else {x[i] = num[i];}}else {if(num[i] < 0 || num[i] >= x.length){console.warn("Invalid series number in setVisibility: " + num[i]);}else {x[num[i]] = value;}}}}this.predraw_();}; /**
 * How large of an area will the dygraph render itself in?
 * This is used for testing.
 * @return A {width: w, height: h} object.
 * @private
 */Dygraph.prototype.size = function(){return {width:this.width_,height:this.height_};}; /**
 * Update the list of annotations and redraw the chart.
 * See dygraphs.com/annotations.html for more info on how to use annotations.
 * @param ann {Array} An array of annotation objects.
 * @param suppressDraw {Boolean} Set to "true" to block chart redraw (optional).
 */Dygraph.prototype.setAnnotations = function(ann,suppressDraw){ // Only add the annotation CSS rule once we know it will be used.
this.annotations_ = ann;if(!this.layout_){console.warn("Tried to setAnnotations before dygraph was ready. " + "Try setting them in a ready() block. See " + "dygraphs.com/tests/annotation.html");return;}this.layout_.setAnnotations(this.annotations_);if(!suppressDraw){this.predraw_();}}; /**
 * Return the list of annotations.
 */Dygraph.prototype.annotations = function(){return this.annotations_;}; /**
 * Get the list of label names for this graph. The first column is the
 * x-axis, so the data series names start at index 1.
 *
 * Returns null when labels have not yet been defined.
 */Dygraph.prototype.getLabels = function(){var labels=this.attr_("labels");return labels?labels.slice():null;}; /**
 * Get the index of a series (column) given its name. The first column is the
 * x-axis, so the data series start with index 1.
 */Dygraph.prototype.indexFromSetName = function(name){return this.setIndexByName_[name];}; /**
 * Find the row number corresponding to the given x-value.
 * Returns null if there is no such x-value in the data.
 * If there are multiple rows with the same x-value, this will return the
 * first one.
 * @param {number} xVal The x-value to look for (e.g. millis since epoch).
 * @return {?number} The row number, which you can pass to getValue(), or null.
 */Dygraph.prototype.getRowForX = function(xVal){var low=0,high=this.numRows() - 1;while(low <= high) {var idx=high + low >> 1;var x=this.getValue(idx,0);if(x < xVal){low = idx + 1;}else if(x > xVal){high = idx - 1;}else if(low != idx){ // equal, but there may be an earlier match.
high = idx;}else {return idx;}}return null;}; /**
 * Trigger a callback when the dygraph has drawn itself and is ready to be
 * manipulated. This is primarily useful when dygraphs has to do an XHR for the
 * data (i.e. a URL is passed as the data source) and the chart is drawn
 * asynchronously. If the chart has already drawn, the callback will fire
 * immediately.
 *
 * This is a good place to call setAnnotation().
 *
 * @param {function(!Dygraph)} callback The callback to trigger when the chart
 *     is ready.
 */Dygraph.prototype.ready = function(callback){if(this.is_initial_draw_){this.readyFns_.push(callback);}else {callback.call(this,this);}}; /**
 * Add an event handler. This event handler is kept until the graph is
 * destroyed with a call to graph.destroy().
 *
 * @param {!Node} elem The element to add the event to.
 * @param {string} type The type of the event, e.g. 'click' or 'mousemove'.
 * @param {function(Event):(boolean|undefined)} fn The function to call
 *     on the event. The function takes one parameter: the event object.
 * @private
 */Dygraph.prototype.addAndTrackEvent = function(elem,type,fn){utils.addEvent(elem,type,fn);this.registeredEvents_.push({elem:elem,type:type,fn:fn});};Dygraph.prototype.removeTrackedEvents_ = function(){if(this.registeredEvents_){for(var idx=0;idx < this.registeredEvents_.length;idx++) {var reg=this.registeredEvents_[idx];utils.removeEvent(reg.elem,reg.type,reg.fn);}}this.registeredEvents_ = [];}; // Installed plugins, in order of precedence (most-general to most-specific).
Dygraph.PLUGINS = [_pluginsLegend2['default'],_pluginsAxes2['default'],_pluginsRangeSelector2['default'], // Has to be before ChartLabels so that its callbacks are called after ChartLabels' callbacks.
_pluginsChartLabels2['default'],_pluginsAnnotations2['default'],_pluginsGrid2['default']]; // There are many symbols which have historically been available through the
// Dygraph class. These are exported here for backwards compatibility.
Dygraph.GVizChart = _dygraphGviz2['default'];Dygraph.DASHED_LINE = utils.DASHED_LINE;Dygraph.DOT_DASH_LINE = utils.DOT_DASH_LINE;Dygraph.dateAxisLabelFormatter = utils.dateAxisLabelFormatter;Dygraph.toRGB_ = utils.toRGB_;Dygraph.findPos = utils.findPos;Dygraph.pageX = utils.pageX;Dygraph.pageY = utils.pageY;Dygraph.dateString_ = utils.dateString_;Dygraph.defaultInteractionModel = _dygraphInteractionModel2['default'].defaultModel;Dygraph.nonInteractiveModel = Dygraph.nonInteractiveModel_ = _dygraphInteractionModel2['default'].nonInteractiveModel_;Dygraph.Circles = utils.Circles;Dygraph.Plugins = {Legend:_pluginsLegend2['default'],Axes:_pluginsAxes2['default'],Annotations:_pluginsAnnotations2['default'],ChartLabels:_pluginsChartLabels2['default'],Grid:_pluginsGrid2['default'],RangeSelector:_pluginsRangeSelector2['default']};Dygraph.DataHandlers = {DefaultHandler:_datahandlerDefault2['default'],BarsHandler:_datahandlerBars2['default'],CustomBarsHandler:_datahandlerBarsCustom2['default'],DefaultFractionHandler:_datahandlerDefaultFractions2['default'],ErrorBarsHandler:_datahandlerBarsError2['default'],FractionsBarsHandler:_datahandlerBarsFractions2['default']};Dygraph.startPan = _dygraphInteractionModel2['default'].startPan;Dygraph.startZoom = _dygraphInteractionModel2['default'].startZoom;Dygraph.movePan = _dygraphInteractionModel2['default'].movePan;Dygraph.moveZoom = _dygraphInteractionModel2['default'].moveZoom;Dygraph.endPan = _dygraphInteractionModel2['default'].endPan;Dygraph.endZoom = _dygraphInteractionModel2['default'].endZoom;Dygraph.numericLinearTicks = DygraphTickers.numericLinearTicks;Dygraph.numericTicks = DygraphTickers.numericTicks;Dygraph.dateTicker = DygraphTickers.dateTicker;Dygraph.Granularity = DygraphTickers.Granularity;Dygraph.getDateAxis = DygraphTickers.getDateAxis;Dygraph.floatFormat = utils.floatFormat;exports['default'] = Dygraph;module.exports = exports['default'];

}).call(this,require('_process'))

},{"./datahandler/bars":5,"./datahandler/bars-custom":2,"./datahandler/bars-error":3,"./datahandler/bars-fractions":4,"./datahandler/default":8,"./datahandler/default-fractions":7,"./dygraph-canvas":9,"./dygraph-default-attrs":10,"./dygraph-gviz":11,"./dygraph-interaction-model":12,"./dygraph-layout":13,"./dygraph-options":15,"./dygraph-options-reference":14,"./dygraph-tickers":16,"./dygraph-utils":17,"./iframe-tarp":19,"./plugins/annotations":20,"./plugins/axes":21,"./plugins/chart-labels":22,"./plugins/grid":23,"./plugins/legend":24,"./plugins/range-selector":25,"_process":1}],19:[function(require,module,exports){
/**
 * To create a "drag" interaction, you typically register a mousedown event
 * handler on the element where the drag begins. In that handler, you register a
 * mouseup handler on the window to determine when the mouse is released,
 * wherever that release happens. This works well, except when the user releases
 * the mouse over an off-domain iframe. In that case, the mouseup event is
 * handled by the iframe and never bubbles up to the window handler.
 *
 * To deal with this issue, we cover iframes with high z-index divs to make sure
 * they don't capture mouseup.
 *
 * Usage:
 * element.addEventListener('mousedown', function() {
 *   var tarper = new IFrameTarp();
 *   tarper.cover();
 *   var mouseUpHandler = function() {
 *     ...
 *     window.removeEventListener(mouseUpHandler);
 *     tarper.uncover();
 *   };
 *   window.addEventListener('mouseup', mouseUpHandler);
 * };
 *
 * @constructor
 */
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});

function _interopRequireWildcard(obj) { if (obj && obj.__esModule) { return obj; } else { var newObj = {}; if (obj != null) { for (var key in obj) { if (Object.prototype.hasOwnProperty.call(obj, key)) newObj[key] = obj[key]; } } newObj["default"] = obj; return newObj; } }

var _dygraphUtils = require('./dygraph-utils');

var utils = _interopRequireWildcard(_dygraphUtils);

function IFrameTarp() {
  /** @type {Array.<!HTMLDivElement>} */
  this.tarps = [];
};

/**
 * Find all the iframes in the document and cover them with high z-index
 * transparent divs.
 */
IFrameTarp.prototype.cover = function () {
  var iframes = document.getElementsByTagName("iframe");
  for (var i = 0; i < iframes.length; i++) {
    var iframe = iframes[i];
    var pos = utils.findPos(iframe),
        x = pos.x,
        y = pos.y,
        width = iframe.offsetWidth,
        height = iframe.offsetHeight;

    var div = document.createElement("div");
    div.style.position = "absolute";
    div.style.left = x + 'px';
    div.style.top = y + 'px';
    div.style.width = width + 'px';
    div.style.height = height + 'px';
    div.style.zIndex = 999;
    document.body.appendChild(div);
    this.tarps.push(div);
  }
};

/**
 * Remove all the iframe covers. You should call this in a mouseup handler.
 */
IFrameTarp.prototype.uncover = function () {
  for (var i = 0; i < this.tarps.length; i++) {
    this.tarps[i].parentNode.removeChild(this.tarps[i]);
  }
  this.tarps = [];
};

exports["default"] = IFrameTarp;
module.exports = exports["default"];

},{"./dygraph-utils":17}],20:[function(require,module,exports){
/**
 * @license
 * Copyright 2012 Dan Vanderkam (danvdk@gmail.com)
 * MIT-licensed (http://opensource.org/licenses/MIT)
 */

/*global Dygraph:false */

"use strict";

/**
Current bits of jankiness:
- Uses dygraph.layout_ to get the parsed annotations.
- Uses dygraph.plotter_.area

It would be nice if the plugin didn't require so much special support inside
the core dygraphs classes, but annotations involve quite a bit of parsing and
layout.

TODO(danvk): cache DOM elements.
*/

Object.defineProperty(exports, "__esModule", {
  value: true
});
var annotations = function annotations() {
  this.annotations_ = [];
};

annotations.prototype.toString = function () {
  return "Annotations Plugin";
};

annotations.prototype.activate = function (g) {
  return {
    clearChart: this.clearChart,
    didDrawChart: this.didDrawChart
  };
};

annotations.prototype.detachLabels = function () {
  for (var i = 0; i < this.annotations_.length; i++) {
    var a = this.annotations_[i];
    if (a.parentNode) a.parentNode.removeChild(a);
    this.annotations_[i] = null;
  }
  this.annotations_ = [];
};

annotations.prototype.clearChart = function (e) {
  this.detachLabels();
};

annotations.prototype.didDrawChart = function (e) {
  var g = e.dygraph;

  // Early out in the (common) case of zero annotations.
  var points = g.layout_.annotated_points;
  if (!points || points.length === 0) return;

  var containerDiv = e.canvas.parentNode;

  var bindEvt = function bindEvt(eventName, classEventName, pt) {
    return function (annotation_event) {
      var a = pt.annotation;
      if (a.hasOwnProperty(eventName)) {
        a[eventName](a, pt, g, annotation_event);
      } else if (g.getOption(classEventName)) {
        g.getOption(classEventName)(a, pt, g, annotation_event);
      }
    };
  };

  // Add the annotations one-by-one.
  var area = e.dygraph.getArea();

  // x-coord to sum of previous annotation's heights (used for stacking).
  var xToUsedHeight = {};

  for (var i = 0; i < points.length; i++) {
    var p = points[i];
    if (p.canvasx < area.x || p.canvasx > area.x + area.w || p.canvasy < area.y || p.canvasy > area.y + area.h) {
      continue;
    }

    var a = p.annotation;
    var tick_height = 6;
    if (a.hasOwnProperty("tickHeight")) {
      tick_height = a.tickHeight;
    }

    // TODO: deprecate axisLabelFontSize in favor of CSS
    var div = document.createElement("div");
    div.style['fontSize'] = g.getOption('axisLabelFontSize') + "px";
    var className = 'dygraph-annotation';
    if (!a.hasOwnProperty('icon')) {
      // camelCase class names are deprecated.
      className += ' dygraphDefaultAnnotation dygraph-default-annotation';
    }
    if (a.hasOwnProperty('cssClass')) {
      className += " " + a.cssClass;
    }
    div.className = className;

    var width = a.hasOwnProperty('width') ? a.width : 16;
    var height = a.hasOwnProperty('height') ? a.height : 16;
    if (a.hasOwnProperty('icon')) {
      var img = document.createElement("img");
      img.src = a.icon;
      img.width = width;
      img.height = height;
      div.appendChild(img);
    } else if (p.annotation.hasOwnProperty('shortText')) {
      div.appendChild(document.createTextNode(p.annotation.shortText));
    }
    var left = p.canvasx - width / 2;
    div.style.left = left + "px";
    var divTop = 0;
    if (a.attachAtBottom) {
      var y = area.y + area.h - height - tick_height;
      if (xToUsedHeight[left]) {
        y -= xToUsedHeight[left];
      } else {
        xToUsedHeight[left] = 0;
      }
      xToUsedHeight[left] += tick_height + height;
      divTop = y;
    } else {
      divTop = p.canvasy - height - tick_height;
    }
    div.style.top = divTop + "px";
    div.style.width = width + "px";
    div.style.height = height + "px";
    div.title = p.annotation.text;
    div.style.color = g.colorsMap_[p.name];
    div.style.borderColor = g.colorsMap_[p.name];
    a.div = div;

    g.addAndTrackEvent(div, 'click', bindEvt('clickHandler', 'annotationClickHandler', p, this));
    g.addAndTrackEvent(div, 'mouseover', bindEvt('mouseOverHandler', 'annotationMouseOverHandler', p, this));
    g.addAndTrackEvent(div, 'mouseout', bindEvt('mouseOutHandler', 'annotationMouseOutHandler', p, this));
    g.addAndTrackEvent(div, 'dblclick', bindEvt('dblClickHandler', 'annotationDblClickHandler', p, this));

    containerDiv.appendChild(div);
    this.annotations_.push(div);

    var ctx = e.drawingContext;
    ctx.save();
    ctx.strokeStyle = a.hasOwnProperty('tickColor') ? a.tickColor : g.colorsMap_[p.name];
    ctx.lineWidth = a.hasOwnProperty('tickWidth') ? a.tickWidth : g.getOption('strokeWidth');
    ctx.beginPath();
    if (!a.attachAtBottom) {
      ctx.moveTo(p.canvasx, p.canvasy);
      ctx.lineTo(p.canvasx, p.canvasy - 2 - tick_height);
    } else {
      var y = divTop + height;
      ctx.moveTo(p.canvasx, y);
      ctx.lineTo(p.canvasx, y + tick_height);
    }
    ctx.closePath();
    ctx.stroke();
    ctx.restore();
  }
};

annotations.prototype.destroy = function () {
  this.detachLabels();
};

exports["default"] = annotations;
module.exports = exports["default"];

},{}],21:[function(require,module,exports){
/**
 * @license
 * Copyright 2012 Dan Vanderkam (danvdk@gmail.com)
 * MIT-licensed (http://opensource.org/licenses/MIT)
 */

/*global Dygraph:false */

'use strict';

/*
Bits of jankiness:
- Direct layout access
- Direct area access
- Should include calculation of ticks, not just the drawing.

Options left to make axis-friendly.
  ('drawAxesAtZero')
  ('xAxisHeight')
*/

Object.defineProperty(exports, '__esModule', {
  value: true
});

function _interopRequireWildcard(obj) { if (obj && obj.__esModule) { return obj; } else { var newObj = {}; if (obj != null) { for (var key in obj) { if (Object.prototype.hasOwnProperty.call(obj, key)) newObj[key] = obj[key]; } } newObj['default'] = obj; return newObj; } }

var _dygraphUtils = require('../dygraph-utils');

var utils = _interopRequireWildcard(_dygraphUtils);

/**
 * Draws the axes. This includes the labels on the x- and y-axes, as well
 * as the tick marks on the axes.
 * It does _not_ draw the grid lines which span the entire chart.
 */
var axes = function axes() {
  this.xlabels_ = [];
  this.ylabels_ = [];
};

axes.prototype.toString = function () {
  return 'Axes Plugin';
};

axes.prototype.activate = function (g) {
  return {
    layout: this.layout,
    clearChart: this.clearChart,
    willDrawChart: this.willDrawChart
  };
};

axes.prototype.layout = function (e) {
  var g = e.dygraph;

  if (g.getOptionForAxis('drawAxis', 'y')) {
    var w = g.getOptionForAxis('axisLabelWidth', 'y') + 2 * g.getOptionForAxis('axisTickSize', 'y');
    e.reserveSpaceLeft(w);
  }

  if (g.getOptionForAxis('drawAxis', 'x')) {
    var h;
    // NOTE: I think this is probably broken now, since g.getOption() now
    // hits the dictionary. (That is, g.getOption('xAxisHeight') now always
    // has a value.)
    if (g.getOption('xAxisHeight')) {
      h = g.getOption('xAxisHeight');
    } else {
      h = g.getOptionForAxis('axisLabelFontSize', 'x') + 2 * g.getOptionForAxis('axisTickSize', 'x');
    }
    e.reserveSpaceBottom(h);
  }

  if (g.numAxes() == 2) {
    if (g.getOptionForAxis('drawAxis', 'y2')) {
      var w = g.getOptionForAxis('axisLabelWidth', 'y2') + 2 * g.getOptionForAxis('axisTickSize', 'y2');
      e.reserveSpaceRight(w);
    }
  } else if (g.numAxes() > 2) {
    g.error('Only two y-axes are supported at this time. (Trying ' + 'to use ' + g.numAxes() + ')');
  }
};

axes.prototype.detachLabels = function () {
  function removeArray(ary) {
    for (var i = 0; i < ary.length; i++) {
      var el = ary[i];
      if (el.parentNode) el.parentNode.removeChild(el);
    }
  }

  removeArray(this.xlabels_);
  removeArray(this.ylabels_);
  this.xlabels_ = [];
  this.ylabels_ = [];
};

axes.prototype.clearChart = function (e) {
  this.detachLabels();
};

axes.prototype.willDrawChart = function (e) {
  var _this = this;

  var g = e.dygraph;

  if (!g.getOptionForAxis('drawAxis', 'x') && !g.getOptionForAxis('drawAxis', 'y') && !g.getOptionForAxis('drawAxis', 'y2')) {
    return;
  }

  // Round pixels to half-integer boundaries for crisper drawing.
  function halfUp(x) {
    return Math.round(x) + 0.5;
  }
  function halfDown(y) {
    return Math.round(y) - 0.5;
  }

  var context = e.drawingContext;
  var containerDiv = e.canvas.parentNode;
  var canvasWidth = g.width_; // e.canvas.width is affected by pixel ratio.
  var canvasHeight = g.height_;

  var label, x, y, tick, i;

  var makeLabelStyle = function makeLabelStyle(axis) {
    return {
      position: 'absolute',
      fontSize: g.getOptionForAxis('axisLabelFontSize', axis) + 'px',
      width: g.getOptionForAxis('axisLabelWidth', axis) + 'px'
    };
  };

  var labelStyles = {
    x: makeLabelStyle('x'),
    y: makeLabelStyle('y'),
    y2: makeLabelStyle('y2')
  };

  var makeDiv = function makeDiv(txt, axis, prec_axis) {
    /*
     * This seems to be called with the following three sets of axis/prec_axis:
     * x: undefined
     * y: y1
     * y: y2
     */
    var div = document.createElement('div');
    var labelStyle = labelStyles[prec_axis == 'y2' ? 'y2' : axis];
    utils.update(div.style, labelStyle);
    // TODO: combine outer & inner divs
    var inner_div = document.createElement('div');
    inner_div.className = 'dygraph-axis-label' + ' dygraph-axis-label-' + axis + (prec_axis ? ' dygraph-axis-label-' + prec_axis : '');
    inner_div.innerHTML = txt;
    div.appendChild(inner_div);
    return div;
  };

  // axis lines
  context.save();

  var layout = g.layout_;
  var area = e.dygraph.plotter_.area;

  // Helper for repeated axis-option accesses.
  var makeOptionGetter = function makeOptionGetter(axis) {
    return function (option) {
      return g.getOptionForAxis(option, axis);
    };
  };

  if (g.getOptionForAxis('drawAxis', 'y')) {
    if (layout.yticks && layout.yticks.length > 0) {
      var num_axes = g.numAxes();
      var getOptions = [makeOptionGetter('y'), makeOptionGetter('y2')];
      layout.yticks.forEach(function (tick) {
        if (tick.label === undefined) return; // this tick only has a grid line.
        x = area.x;
        var sgn = 1;
        var prec_axis = 'y1';
        var getAxisOption = getOptions[0];
        if (tick.axis == 1) {
          // right-side y-axis
          x = area.x + area.w;
          sgn = -1;
          prec_axis = 'y2';
          getAxisOption = getOptions[1];
        }
        var fontSize = getAxisOption('axisLabelFontSize');
        y = area.y + tick.pos * area.h;

        /* Tick marks are currently clipped, so don't bother drawing them.
        context.beginPath();
        context.moveTo(halfUp(x), halfDown(y));
        context.lineTo(halfUp(x - sgn * this.attr_('axisTickSize')), halfDown(y));
        context.closePath();
        context.stroke();
        */

        label = makeDiv(tick.label, 'y', num_axes == 2 ? prec_axis : null);
        var top = y - fontSize / 2;
        if (top < 0) top = 0;

        if (top + fontSize + 3 > canvasHeight) {
          label.style.bottom = '0';
        } else {
          label.style.top = top + 'px';
        }
        // TODO: replace these with css classes?
        if (tick.axis === 0) {
          label.style.left = area.x - getAxisOption('axisLabelWidth') - getAxisOption('axisTickSize') + 'px';
          label.style.textAlign = 'right';
        } else if (tick.axis == 1) {
          label.style.left = area.x + area.w + getAxisOption('axisTickSize') + 'px';
          label.style.textAlign = 'left';
        }
        label.style.width = getAxisOption('axisLabelWidth') + 'px';
        containerDiv.appendChild(label);
        _this.ylabels_.push(label);
      });

      // The lowest tick on the y-axis often overlaps with the leftmost
      // tick on the x-axis. Shift the bottom tick up a little bit to
      // compensate if necessary.
      var bottomTick = this.ylabels_[0];
      // Interested in the y2 axis also?
      var fontSize = g.getOptionForAxis('axisLabelFontSize', 'y');
      var bottom = parseInt(bottomTick.style.top, 10) + fontSize;
      if (bottom > canvasHeight - fontSize) {
        bottomTick.style.top = parseInt(bottomTick.style.top, 10) - fontSize / 2 + 'px';
      }
    }

    // draw a vertical line on the left to separate the chart from the labels.
    var axisX;
    if (g.getOption('drawAxesAtZero')) {
      var r = g.toPercentXCoord(0);
      if (r > 1 || r < 0 || isNaN(r)) r = 0;
      axisX = halfUp(area.x + r * area.w);
    } else {
      axisX = halfUp(area.x);
    }

    context.strokeStyle = g.getOptionForAxis('axisLineColor', 'y');
    context.lineWidth = g.getOptionForAxis('axisLineWidth', 'y');

    context.beginPath();
    context.moveTo(axisX, halfDown(area.y));
    context.lineTo(axisX, halfDown(area.y + area.h));
    context.closePath();
    context.stroke();

    // if there's a secondary y-axis, draw a vertical line for that, too.
    if (g.numAxes() == 2) {
      context.strokeStyle = g.getOptionForAxis('axisLineColor', 'y2');
      context.lineWidth = g.getOptionForAxis('axisLineWidth', 'y2');
      context.beginPath();
      context.moveTo(halfDown(area.x + area.w), halfDown(area.y));
      context.lineTo(halfDown(area.x + area.w), halfDown(area.y + area.h));
      context.closePath();
      context.stroke();
    }
  }

  if (g.getOptionForAxis('drawAxis', 'x')) {
    if (layout.xticks) {
      var getAxisOption = makeOptionGetter('x');
      layout.xticks.forEach(function (tick) {
        if (tick.label === undefined) return; // this tick only has a grid line.
        x = area.x + tick.pos * area.w;
        y = area.y + area.h;

        /* Tick marks are currently clipped, so don't bother drawing them.
        context.beginPath();
        context.moveTo(halfUp(x), halfDown(y));
        context.lineTo(halfUp(x), halfDown(y + this.attr_('axisTickSize')));
        context.closePath();
        context.stroke();
        */

        label = makeDiv(tick.label, 'x');
        label.style.textAlign = 'center';
        label.style.top = y + getAxisOption('axisTickSize') + 'px';

        var left = x - getAxisOption('axisLabelWidth') / 2;
        if (left + getAxisOption('axisLabelWidth') > canvasWidth) {
          left = canvasWidth - getAxisOption('axisLabelWidth');
          label.style.textAlign = 'right';
        }
        if (left < 0) {
          left = 0;
          label.style.textAlign = 'left';
        }

        label.style.left = left + 'px';
        label.style.width = getAxisOption('axisLabelWidth') + 'px';
        containerDiv.appendChild(label);
        _this.xlabels_.push(label);
      });
    }

    context.strokeStyle = g.getOptionForAxis('axisLineColor', 'x');
    context.lineWidth = g.getOptionForAxis('axisLineWidth', 'x');
    context.beginPath();
    var axisY;
    if (g.getOption('drawAxesAtZero')) {
      var r = g.toPercentYCoord(0, 0);
      if (r > 1 || r < 0) r = 1;
      axisY = halfDown(area.y + r * area.h);
    } else {
      axisY = halfDown(area.y + area.h);
    }
    context.moveTo(halfUp(area.x), axisY);
    context.lineTo(halfUp(area.x + area.w), axisY);
    context.closePath();
    context.stroke();
  }

  context.restore();
};

exports['default'] = axes;
module.exports = exports['default'];

},{"../dygraph-utils":17}],22:[function(require,module,exports){
/**
 * @license
 * Copyright 2012 Dan Vanderkam (danvdk@gmail.com)
 * MIT-licensed (http://opensource.org/licenses/MIT)
 */
/*global Dygraph:false */

"use strict";

// TODO(danvk): move chart label options out of dygraphs and into the plugin.
// TODO(danvk): only tear down & rebuild the DIVs when it's necessary.

Object.defineProperty(exports, "__esModule", {
  value: true
});
var chart_labels = function chart_labels() {
  this.title_div_ = null;
  this.xlabel_div_ = null;
  this.ylabel_div_ = null;
  this.y2label_div_ = null;
};

chart_labels.prototype.toString = function () {
  return "ChartLabels Plugin";
};

chart_labels.prototype.activate = function (g) {
  return {
    layout: this.layout,
    // clearChart: this.clearChart,
    didDrawChart: this.didDrawChart
  };
};

// QUESTION: should there be a plugin-utils.js?
var createDivInRect = function createDivInRect(r) {
  var div = document.createElement('div');
  div.style.position = 'absolute';
  div.style.left = r.x + 'px';
  div.style.top = r.y + 'px';
  div.style.width = r.w + 'px';
  div.style.height = r.h + 'px';
  return div;
};

// Detach and null out any existing nodes.
chart_labels.prototype.detachLabels_ = function () {
  var els = [this.title_div_, this.xlabel_div_, this.ylabel_div_, this.y2label_div_];
  for (var i = 0; i < els.length; i++) {
    var el = els[i];
    if (!el) continue;
    if (el.parentNode) el.parentNode.removeChild(el);
  }

  this.title_div_ = null;
  this.xlabel_div_ = null;
  this.ylabel_div_ = null;
  this.y2label_div_ = null;
};

var createRotatedDiv = function createRotatedDiv(g, box, axis, classes, html) {
  // TODO(danvk): is this outer div actually necessary?
  var div = document.createElement("div");
  div.style.position = 'absolute';
  if (axis == 1) {
    // NOTE: this is cheating. Should be positioned relative to the box.
    div.style.left = '0px';
  } else {
    div.style.left = box.x + 'px';
  }
  div.style.top = box.y + 'px';
  div.style.width = box.w + 'px';
  div.style.height = box.h + 'px';
  div.style.fontSize = g.getOption('yLabelWidth') - 2 + 'px';

  var inner_div = document.createElement("div");
  inner_div.style.position = 'absolute';
  inner_div.style.width = box.h + 'px';
  inner_div.style.height = box.w + 'px';
  inner_div.style.top = box.h / 2 - box.w / 2 + 'px';
  inner_div.style.left = box.w / 2 - box.h / 2 + 'px';
  // TODO: combine inner_div and class_div.
  inner_div.className = 'dygraph-label-rotate-' + (axis == 1 ? 'right' : 'left');

  var class_div = document.createElement("div");
  class_div.className = classes;
  class_div.innerHTML = html;

  inner_div.appendChild(class_div);
  div.appendChild(inner_div);
  return div;
};

chart_labels.prototype.layout = function (e) {
  this.detachLabels_();

  var g = e.dygraph;
  var div = e.chart_div;
  if (g.getOption('title')) {
    // QUESTION: should this return an absolutely-positioned div instead?
    var title_rect = e.reserveSpaceTop(g.getOption('titleHeight'));
    this.title_div_ = createDivInRect(title_rect);
    this.title_div_.style.fontSize = g.getOption('titleHeight') - 8 + 'px';

    var class_div = document.createElement("div");
    class_div.className = 'dygraph-label dygraph-title';
    class_div.innerHTML = g.getOption('title');
    this.title_div_.appendChild(class_div);
    div.appendChild(this.title_div_);
  }

  if (g.getOption('xlabel')) {
    var x_rect = e.reserveSpaceBottom(g.getOption('xLabelHeight'));
    this.xlabel_div_ = createDivInRect(x_rect);
    this.xlabel_div_.style.fontSize = g.getOption('xLabelHeight') - 2 + 'px';

    var class_div = document.createElement("div");
    class_div.className = 'dygraph-label dygraph-xlabel';
    class_div.innerHTML = g.getOption('xlabel');
    this.xlabel_div_.appendChild(class_div);
    div.appendChild(this.xlabel_div_);
  }

  if (g.getOption('ylabel')) {
    // It would make sense to shift the chart here to make room for the y-axis
    // label, but the default yAxisLabelWidth is large enough that this results
    // in overly-padded charts. The y-axis label should fit fine. If it
    // doesn't, the yAxisLabelWidth option can be increased.
    var y_rect = e.reserveSpaceLeft(0);

    this.ylabel_div_ = createRotatedDiv(g, y_rect, 1, // primary (left) y-axis
    'dygraph-label dygraph-ylabel', g.getOption('ylabel'));
    div.appendChild(this.ylabel_div_);
  }

  if (g.getOption('y2label') && g.numAxes() == 2) {
    // same logic applies here as for ylabel.
    var y2_rect = e.reserveSpaceRight(0);
    this.y2label_div_ = createRotatedDiv(g, y2_rect, 2, // secondary (right) y-axis
    'dygraph-label dygraph-y2label', g.getOption('y2label'));
    div.appendChild(this.y2label_div_);
  }
};

chart_labels.prototype.didDrawChart = function (e) {
  var g = e.dygraph;
  if (this.title_div_) {
    this.title_div_.children[0].innerHTML = g.getOption('title');
  }
  if (this.xlabel_div_) {
    this.xlabel_div_.children[0].innerHTML = g.getOption('xlabel');
  }
  if (this.ylabel_div_) {
    this.ylabel_div_.children[0].children[0].innerHTML = g.getOption('ylabel');
  }
  if (this.y2label_div_) {
    this.y2label_div_.children[0].children[0].innerHTML = g.getOption('y2label');
  }
};

chart_labels.prototype.clearChart = function () {};

chart_labels.prototype.destroy = function () {
  this.detachLabels_();
};

exports["default"] = chart_labels;
module.exports = exports["default"];

},{}],23:[function(require,module,exports){
/**
 * @license
 * Copyright 2012 Dan Vanderkam (danvdk@gmail.com)
 * MIT-licensed (http://opensource.org/licenses/MIT)
 */
/*global Dygraph:false */

/*

Current bits of jankiness:
- Direct layout access
- Direct area access

*/

"use strict";

/**
 * Draws the gridlines, i.e. the gray horizontal & vertical lines running the
 * length of the chart.
 *
 * @constructor
 */
Object.defineProperty(exports, "__esModule", {
  value: true
});
var grid = function grid() {};

grid.prototype.toString = function () {
  return "Gridline Plugin";
};

grid.prototype.activate = function (g) {
  return {
    willDrawChart: this.willDrawChart
  };
};

grid.prototype.willDrawChart = function (e) {
  // Draw the new X/Y grid. Lines appear crisper when pixels are rounded to
  // half-integers. This prevents them from drawing in two rows/cols.
  var g = e.dygraph;
  var ctx = e.drawingContext;
  var layout = g.layout_;
  var area = e.dygraph.plotter_.area;

  function halfUp(x) {
    return Math.round(x) + 0.5;
  }
  function halfDown(y) {
    return Math.round(y) - 0.5;
  }

  var x, y, i, ticks;
  if (g.getOptionForAxis('drawGrid', 'y')) {
    var axes = ["y", "y2"];
    var strokeStyles = [],
        lineWidths = [],
        drawGrid = [],
        stroking = [],
        strokePattern = [];
    for (var i = 0; i < axes.length; i++) {
      drawGrid[i] = g.getOptionForAxis('drawGrid', axes[i]);
      if (drawGrid[i]) {
        strokeStyles[i] = g.getOptionForAxis('gridLineColor', axes[i]);
        lineWidths[i] = g.getOptionForAxis('gridLineWidth', axes[i]);
        strokePattern[i] = g.getOptionForAxis('gridLinePattern', axes[i]);
        stroking[i] = strokePattern[i] && strokePattern[i].length >= 2;
      }
    }
    ticks = layout.yticks;
    ctx.save();
    // draw grids for the different y axes
    ticks.forEach(function (tick) {
      if (!tick.has_tick) return;
      var axis = tick.axis;
      if (drawGrid[axis]) {
        ctx.save();
        if (stroking[axis]) {
          if (ctx.setLineDash) ctx.setLineDash(strokePattern[axis]);
        }
        ctx.strokeStyle = strokeStyles[axis];
        ctx.lineWidth = lineWidths[axis];

        x = halfUp(area.x);
        y = halfDown(area.y + tick.pos * area.h);
        ctx.beginPath();
        ctx.moveTo(x, y);
        ctx.lineTo(x + area.w, y);
        ctx.stroke();

        ctx.restore();
      }
    });
    ctx.restore();
  }

  // draw grid for x axis
  if (g.getOptionForAxis('drawGrid', 'x')) {
    ticks = layout.xticks;
    ctx.save();
    var strokePattern = g.getOptionForAxis('gridLinePattern', 'x');
    var stroking = strokePattern && strokePattern.length >= 2;
    if (stroking) {
      if (ctx.setLineDash) ctx.setLineDash(strokePattern);
    }
    ctx.strokeStyle = g.getOptionForAxis('gridLineColor', 'x');
    ctx.lineWidth = g.getOptionForAxis('gridLineWidth', 'x');
    ticks.forEach(function (tick) {
      if (!tick.has_tick) return;
      x = halfUp(area.x + tick.pos * area.w);
      y = halfDown(area.y + area.h);
      ctx.beginPath();
      ctx.moveTo(x, y);
      ctx.lineTo(x, area.y);
      ctx.closePath();
      ctx.stroke();
    });
    if (stroking) {
      if (ctx.setLineDash) ctx.setLineDash([]);
    }
    ctx.restore();
  }
};

grid.prototype.destroy = function () {};

exports["default"] = grid;
module.exports = exports["default"];

},{}],24:[function(require,module,exports){
/**
 * @license
 * Copyright 2012 Dan Vanderkam (danvdk@gmail.com)
 * MIT-licensed (http://opensource.org/licenses/MIT)
 */
/*global Dygraph:false */

/*
Current bits of jankiness:
- Uses two private APIs:
    1. Dygraph.optionsViewForAxis_
    2. dygraph.plotter_.area
- Registers for a "predraw" event, which should be renamed.
- I call calculateEmWidthInDiv more often than needed.
*/

/*global Dygraph:false */
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});

function _interopRequireWildcard(obj) { if (obj && obj.__esModule) { return obj; } else { var newObj = {}; if (obj != null) { for (var key in obj) { if (Object.prototype.hasOwnProperty.call(obj, key)) newObj[key] = obj[key]; } } newObj["default"] = obj; return newObj; } }

var _dygraphUtils = require('../dygraph-utils');

var utils = _interopRequireWildcard(_dygraphUtils);

/**
 * Creates the legend, which appears when the user hovers over the chart.
 * The legend can be either a user-specified or generated div.
 *
 * @constructor
 */
var Legend = function Legend() {
  this.legend_div_ = null;
  this.is_generated_div_ = false; // do we own this div, or was it user-specified?
};

Legend.prototype.toString = function () {
  return "Legend Plugin";
};

/**
 * This is called during the dygraph constructor, after options have been set
 * but before the data is available.
 *
 * Proper tasks to do here include:
 * - Reading your own options
 * - DOM manipulation
 * - Registering event listeners
 *
 * @param {Dygraph} g Graph instance.
 * @return {object.<string, function(ev)>} Mapping of event names to callbacks.
 */
Legend.prototype.activate = function (g) {
  var div;

  var userLabelsDiv = g.getOption('labelsDiv');
  if (userLabelsDiv && null !== userLabelsDiv) {
    if (typeof userLabelsDiv == "string" || userLabelsDiv instanceof String) {
      div = document.getElementById(userLabelsDiv);
    } else {
      div = userLabelsDiv;
    }
  } else {
    div = document.createElement("div");
    div.className = "dygraph-legend";
    // TODO(danvk): come up with a cleaner way to expose this.
    g.graphDiv.appendChild(div);
    this.is_generated_div_ = true;
  }

  this.legend_div_ = div;
  this.one_em_width_ = 10; // just a guess, will be updated.

  return {
    select: this.select,
    deselect: this.deselect,
    // TODO(danvk): rethink the name "predraw" before we commit to it in any API.
    predraw: this.predraw,
    didDrawChart: this.didDrawChart
  };
};

// Needed for dashed lines.
var calculateEmWidthInDiv = function calculateEmWidthInDiv(div) {
  var sizeSpan = document.createElement('span');
  sizeSpan.setAttribute('style', 'margin: 0; padding: 0 0 0 1em; border: 0;');
  div.appendChild(sizeSpan);
  var oneEmWidth = sizeSpan.offsetWidth;
  div.removeChild(sizeSpan);
  return oneEmWidth;
};

var escapeHTML = function escapeHTML(str) {
  return str.replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
};

Legend.prototype.select = function (e) {
  var xValue = e.selectedX;
  var points = e.selectedPoints;
  var row = e.selectedRow;

  var legendMode = e.dygraph.getOption('legend');
  if (legendMode === 'never') {
    this.legend_div_.style.display = 'none';
    return;
  }

  if (legendMode === 'follow') {
    // create floating legend div
    var area = e.dygraph.plotter_.area;
    var labelsDivWidth = this.legend_div_.offsetWidth;
    var yAxisLabelWidth = e.dygraph.getOptionForAxis('axisLabelWidth', 'y');
    // determine floating [left, top] coordinates of the legend div
    // within the plotter_ area
    // offset 50 px to the right and down from the first selection point
    // 50 px is guess based on mouse cursor size
    var leftLegend = points[0].x * area.w + 50;
    var topLegend = points[0].y * area.h - 50;

    // if legend floats to end of the chart area, it flips to the other
    // side of the selection point
    if (leftLegend + labelsDivWidth + 1 > area.w) {
      leftLegend = leftLegend - 2 * 50 - labelsDivWidth - (yAxisLabelWidth - area.x);
    }

    e.dygraph.graphDiv.appendChild(this.legend_div_);
    this.legend_div_.style.left = yAxisLabelWidth + leftLegend + "px";
    this.legend_div_.style.top = topLegend + "px";
  }

  var html = Legend.generateLegendHTML(e.dygraph, xValue, points, this.one_em_width_, row);
  this.legend_div_.innerHTML = html;
  this.legend_div_.style.display = '';
};

Legend.prototype.deselect = function (e) {
  var legendMode = e.dygraph.getOption('legend');
  if (legendMode !== 'always') {
    this.legend_div_.style.display = "none";
  }

  // Have to do this every time, since styles might have changed.
  var oneEmWidth = calculateEmWidthInDiv(this.legend_div_);
  this.one_em_width_ = oneEmWidth;

  var html = Legend.generateLegendHTML(e.dygraph, undefined, undefined, oneEmWidth, null);
  this.legend_div_.innerHTML = html;
};

Legend.prototype.didDrawChart = function (e) {
  this.deselect(e);
};

// Right edge should be flush with the right edge of the charting area (which
// may not be the same as the right edge of the div, if we have two y-axes.
// TODO(danvk): is any of this really necessary? Could just set "right" in "activate".
/**
 * Position the labels div so that:
 * - its right edge is flush with the right edge of the charting area
 * - its top edge is flush with the top edge of the charting area
 * @private
 */
Legend.prototype.predraw = function (e) {
  // Don't touch a user-specified labelsDiv.
  if (!this.is_generated_div_) return;

  // TODO(danvk): only use real APIs for this.
  e.dygraph.graphDiv.appendChild(this.legend_div_);
  var area = e.dygraph.getArea();
  var labelsDivWidth = this.legend_div_.offsetWidth;
  this.legend_div_.style.left = area.x + area.w - labelsDivWidth - 1 + "px";
  this.legend_div_.style.top = area.y + "px";
};

/**
 * Called when dygraph.destroy() is called.
 * You should null out any references and detach any DOM elements.
 */
Legend.prototype.destroy = function () {
  this.legend_div_ = null;
};

/**
 * Generates HTML for the legend which is displayed when hovering over the
 * chart. If no selected points are specified, a default legend is returned
 * (this may just be the empty string).
 * @param {number} x The x-value of the selected points.
 * @param {Object} sel_points List of selected points for the given
 *   x-value. Should have properties like 'name', 'yval' and 'canvasy'.
 * @param {number} oneEmWidth The pixel width for 1em in the legend. Only
 *   relevant when displaying a legend with no selection (i.e. {legend:
 *   'always'}) and with dashed lines.
 * @param {number} row The selected row index.
 * @private
 */
Legend.generateLegendHTML = function (g, x, sel_points, oneEmWidth, row) {
  // Data about the selection to pass to legendFormatter
  var data = {
    dygraph: g,
    x: x,
    series: []
  };

  var labelToSeries = {};
  var labels = g.getLabels();
  if (labels) {
    for (var i = 1; i < labels.length; i++) {
      var series = g.getPropertiesForSeries(labels[i]);
      var strokePattern = g.getOption('strokePattern', labels[i]);
      var seriesData = {
        dashHTML: generateLegendDashHTML(strokePattern, series.color, oneEmWidth),
        label: labels[i],
        labelHTML: escapeHTML(labels[i]),
        isVisible: series.visible,
        color: series.color
      };

      data.series.push(seriesData);
      labelToSeries[labels[i]] = seriesData;
    }
  }

  if (typeof x !== 'undefined') {
    var xOptView = g.optionsViewForAxis_('x');
    var xvf = xOptView('valueFormatter');
    data.xHTML = xvf.call(g, x, xOptView, labels[0], g, row, 0);

    var yOptViews = [];
    var num_axes = g.numAxes();
    for (var i = 0; i < num_axes; i++) {
      // TODO(danvk): remove this use of a private API
      yOptViews[i] = g.optionsViewForAxis_('y' + (i ? 1 + i : ''));
    }

    var showZeros = g.getOption('labelsShowZeroValues');
    var highlightSeries = g.getHighlightSeries();
    for (i = 0; i < sel_points.length; i++) {
      var pt = sel_points[i];
      var seriesData = labelToSeries[pt.name];
      seriesData.y = pt.yval;

      if (pt.yval === 0 && !showZeros || isNaN(pt.canvasy)) {
        seriesData.isVisible = false;
        continue;
      }

      var series = g.getPropertiesForSeries(pt.name);
      var yOptView = yOptViews[series.axis - 1];
      var fmtFunc = yOptView('valueFormatter');
      var yHTML = fmtFunc.call(g, pt.yval, yOptView, pt.name, g, row, labels.indexOf(pt.name));

      utils.update(seriesData, { yHTML: yHTML });

      if (pt.name == highlightSeries) {
        seriesData.isHighlighted = true;
      }
    }
  }

  var formatter = g.getOption('legendFormatter') || Legend.defaultFormatter;
  return formatter.call(g, data);
};

Legend.defaultFormatter = function (data) {
  var g = data.dygraph;

  // TODO(danvk): deprecate this option in place of {legend: 'never'}
  // XXX should this logic be in the formatter?
  if (g.getOption('showLabelsOnHighlight') !== true) return '';

  var sepLines = g.getOption('labelsSeparateLines');
  var html;

  if (typeof data.x === 'undefined') {
    // TODO: this check is duplicated in generateLegendHTML. Put it in one place.
    if (g.getOption('legend') != 'always') {
      return '';
    }

    html = '';
    for (var i = 0; i < data.series.length; i++) {
      var series = data.series[i];
      if (!series.isVisible) continue;

      if (html !== '') html += sepLines ? '<br/>' : ' ';
      html += "<span style='font-weight: bold; color: " + series.color + ";'>" + series.dashHTML + " " + series.labelHTML + "</span>";
    }
    return html;
  }

  html = data.xHTML + ':';
  for (var i = 0; i < data.series.length; i++) {
    var series = data.series[i];
    if (!series.isVisible) continue;
    if (sepLines) html += '<br>';
    var cls = series.isHighlighted ? ' class="highlight"' : '';
    html += "<span" + cls + "> <b><span style='color: " + series.color + ";'>" + series.labelHTML + "</span></b>:&#160;" + series.yHTML + "</span>";
  }
  return html;
};

/**
 * Generates html for the "dash" displayed on the legend when using "legend: always".
 * In particular, this works for dashed lines with any stroke pattern. It will
 * try to scale the pattern to fit in 1em width. Or if small enough repeat the
 * pattern for 1em width.
 *
 * @param strokePattern The pattern
 * @param color The color of the series.
 * @param oneEmWidth The width in pixels of 1em in the legend.
 * @private
 */
// TODO(danvk): cache the results of this
function generateLegendDashHTML(strokePattern, color, oneEmWidth) {
  // Easy, common case: a solid line
  if (!strokePattern || strokePattern.length <= 1) {
    return "<div class=\\"dygraph-legend-line\\" style=\\"border-bottom-color: " + color + ";\\"></div>";
  }

  var i, j, paddingLeft, marginRight;
  var strokePixelLength = 0,
      segmentLoop = 0;
  var normalizedPattern = [];
  var loop;

  // Compute the length of the pixels including the first segment twice,
  // since we repeat it.
  for (i = 0; i <= strokePattern.length; i++) {
    strokePixelLength += strokePattern[i % strokePattern.length];
  }

  // See if we can loop the pattern by itself at least twice.
  loop = Math.floor(oneEmWidth / (strokePixelLength - strokePattern[0]));
  if (loop > 1) {
    // This pattern fits at least two times, no scaling just convert to em;
    for (i = 0; i < strokePattern.length; i++) {
      normalizedPattern[i] = strokePattern[i] / oneEmWidth;
    }
    // Since we are repeating the pattern, we don't worry about repeating the
    // first segment in one draw.
    segmentLoop = normalizedPattern.length;
  } else {
    // If the pattern doesn't fit in the legend we scale it to fit.
    loop = 1;
    for (i = 0; i < strokePattern.length; i++) {
      normalizedPattern[i] = strokePattern[i] / strokePixelLength;
    }
    // For the scaled patterns we do redraw the first segment.
    segmentLoop = normalizedPattern.length + 1;
  }

  // Now make the pattern.
  var dash = "";
  for (j = 0; j < loop; j++) {
    for (i = 0; i < segmentLoop; i += 2) {
      // The padding is the drawn segment.
      paddingLeft = normalizedPattern[i % normalizedPattern.length];
      if (i < strokePattern.length) {
        // The margin is the space segment.
        marginRight = normalizedPattern[(i + 1) % normalizedPattern.length];
      } else {
        // The repeated first segment has no right margin.
        marginRight = 0;
      }
      dash += "<div class=\\"dygraph-legend-dash\\" style=\\"margin-right: " + marginRight + "em; padding-left: " + paddingLeft + "em;\\"></div>";
    }
  }
  return dash;
};

exports["default"] = Legend;
module.exports = exports["default"];

},{"../dygraph-utils":17}],25:[function(require,module,exports){
/**
 * @license
 * Copyright 2011 Paul Felix (paul.eric.felix@gmail.com)
 * MIT-licensed (http://opensource.org/licenses/MIT)
 */
/*global Dygraph:false,TouchEvent:false */

/**
 * @fileoverview This file contains the RangeSelector plugin used to provide
 * a timeline range selector widget for dygraphs.
 */

/*global Dygraph:false */
"use strict";

Object.defineProperty(exports, '__esModule', {
  value: true
});

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { 'default': obj }; }

function _interopRequireWildcard(obj) { if (obj && obj.__esModule) { return obj; } else { var newObj = {}; if (obj != null) { for (var key in obj) { if (Object.prototype.hasOwnProperty.call(obj, key)) newObj[key] = obj[key]; } } newObj['default'] = obj; return newObj; } }

var _dygraphUtils = require('../dygraph-utils');

var utils = _interopRequireWildcard(_dygraphUtils);

var _dygraphInteractionModel = require('../dygraph-interaction-model');

var _dygraphInteractionModel2 = _interopRequireDefault(_dygraphInteractionModel);

var _iframeTarp = require('../iframe-tarp');

var _iframeTarp2 = _interopRequireDefault(_iframeTarp);

var rangeSelector = function rangeSelector() {
  this.hasTouchInterface_ = typeof TouchEvent != 'undefined';
  this.isMobileDevice_ = /mobile|android/gi.test(navigator.appVersion);
  this.interfaceCreated_ = false;
};

rangeSelector.prototype.toString = function () {
  return "RangeSelector Plugin";
};

rangeSelector.prototype.activate = function (dygraph) {
  this.dygraph_ = dygraph;
  if (this.getOption_('showRangeSelector')) {
    this.createInterface_();
  }
  return {
    layout: this.reserveSpace_,
    predraw: this.renderStaticLayer_,
    didDrawChart: this.renderInteractiveLayer_
  };
};

rangeSelector.prototype.destroy = function () {
  this.bgcanvas_ = null;
  this.fgcanvas_ = null;
  this.leftZoomHandle_ = null;
  this.rightZoomHandle_ = null;
};

//------------------------------------------------------------------
// Private methods
//------------------------------------------------------------------

rangeSelector.prototype.getOption_ = function (name, opt_series) {
  return this.dygraph_.getOption(name, opt_series);
};

rangeSelector.prototype.setDefaultOption_ = function (name, value) {
  this.dygraph_.attrs_[name] = value;
};

/**
 * @private
 * Creates the range selector elements and adds them to the graph.
 */
rangeSelector.prototype.createInterface_ = function () {
  this.createCanvases_();
  this.createZoomHandles_();
  this.initInteraction_();

  // Range selector and animatedZooms have a bad interaction. See issue 359.
  if (this.getOption_('animatedZooms')) {
    console.warn('Animated zooms and range selector are not compatible; disabling animatedZooms.');
    this.dygraph_.updateOptions({ animatedZooms: false }, true);
  }

  this.interfaceCreated_ = true;
  this.addToGraph_();
};

/**
 * @private
 * Adds the range selector to the graph.
 */
rangeSelector.prototype.addToGraph_ = function () {
  var graphDiv = this.graphDiv_ = this.dygraph_.graphDiv;
  graphDiv.appendChild(this.bgcanvas_);
  graphDiv.appendChild(this.fgcanvas_);
  graphDiv.appendChild(this.leftZoomHandle_);
  graphDiv.appendChild(this.rightZoomHandle_);
};

/**
 * @private
 * Removes the range selector from the graph.
 */
rangeSelector.prototype.removeFromGraph_ = function () {
  var graphDiv = this.graphDiv_;
  graphDiv.removeChild(this.bgcanvas_);
  graphDiv.removeChild(this.fgcanvas_);
  graphDiv.removeChild(this.leftZoomHandle_);
  graphDiv.removeChild(this.rightZoomHandle_);
  this.graphDiv_ = null;
};

/**
 * @private
 * Called by Layout to allow range selector to reserve its space.
 */
rangeSelector.prototype.reserveSpace_ = function (e) {
  if (this.getOption_('showRangeSelector')) {
    e.reserveSpaceBottom(this.getOption_('rangeSelectorHeight') + 4);
  }
};

/**
 * @private
 * Renders the static portion of the range selector at the predraw stage.
 */
rangeSelector.prototype.renderStaticLayer_ = function () {
  if (!this.updateVisibility_()) {
    return;
  }
  this.resize_();
  this.drawStaticLayer_();
};

/**
 * @private
 * Renders the interactive portion of the range selector after the chart has been drawn.
 */
rangeSelector.prototype.renderInteractiveLayer_ = function () {
  if (!this.updateVisibility_() || this.isChangingRange_) {
    return;
  }
  this.placeZoomHandles_();
  this.drawInteractiveLayer_();
};

/**
 * @private
 * Check to see if the range selector is enabled/disabled and update visibility accordingly.
 */
rangeSelector.prototype.updateVisibility_ = function () {
  var enabled = this.getOption_('showRangeSelector');
  if (enabled) {
    if (!this.interfaceCreated_) {
      this.createInterface_();
    } else if (!this.graphDiv_ || !this.graphDiv_.parentNode) {
      this.addToGraph_();
    }
  } else if (this.graphDiv_) {
    this.removeFromGraph_();
    var dygraph = this.dygraph_;
    setTimeout(function () {
      dygraph.width_ = 0;dygraph.resize();
    }, 1);
  }
  return enabled;
};

/**
 * @private
 * Resizes the range selector.
 */
rangeSelector.prototype.resize_ = function () {
  function setElementRect(canvas, context, rect, pixelRatioOption) {
    var canvasScale = pixelRatioOption || utils.getContextPixelRatio(context);

    canvas.style.top = rect.y + 'px';
    canvas.style.left = rect.x + 'px';
    canvas.width = rect.w * canvasScale;
    canvas.height = rect.h * canvasScale;
    canvas.style.width = rect.w + 'px';
    canvas.style.height = rect.h + 'px';

    if (canvasScale != 1) {
      context.scale(canvasScale, canvasScale);
    }
  }

  var plotArea = this.dygraph_.layout_.getPlotArea();

  var xAxisLabelHeight = 0;
  if (this.dygraph_.getOptionForAxis('drawAxis', 'x')) {
    xAxisLabelHeight = this.getOption_('xAxisHeight') || this.getOption_('axisLabelFontSize') + 2 * this.getOption_('axisTickSize');
  }
  this.canvasRect_ = {
    x: plotArea.x,
    y: plotArea.y + plotArea.h + xAxisLabelHeight + 4,
    w: plotArea.w,
    h: this.getOption_('rangeSelectorHeight')
  };

  var pixelRatioOption = this.dygraph_.getNumericOption('pixelRatio');
  setElementRect(this.bgcanvas_, this.bgcanvas_ctx_, this.canvasRect_, pixelRatioOption);
  setElementRect(this.fgcanvas_, this.fgcanvas_ctx_, this.canvasRect_, pixelRatioOption);
};

/**
 * @private
 * Creates the background and foreground canvases.
 */
rangeSelector.prototype.createCanvases_ = function () {
  this.bgcanvas_ = utils.createCanvas();
  this.bgcanvas_.className = 'dygraph-rangesel-bgcanvas';
  this.bgcanvas_.style.position = 'absolute';
  this.bgcanvas_.style.zIndex = 9;
  this.bgcanvas_ctx_ = utils.getContext(this.bgcanvas_);

  this.fgcanvas_ = utils.createCanvas();
  this.fgcanvas_.className = 'dygraph-rangesel-fgcanvas';
  this.fgcanvas_.style.position = 'absolute';
  this.fgcanvas_.style.zIndex = 9;
  this.fgcanvas_.style.cursor = 'default';
  this.fgcanvas_ctx_ = utils.getContext(this.fgcanvas_);
};

/**
 * @private
 * Creates the zoom handle elements.
 */
rangeSelector.prototype.createZoomHandles_ = function () {
  var img = new Image();
  img.className = 'dygraph-rangesel-zoomhandle';
  img.style.position = 'absolute';
  img.style.zIndex = 10;
  img.style.visibility = 'hidden'; // Initially hidden so they don't show up in the wrong place.
  img.style.cursor = 'col-resize';
  // TODO: change image to more options
  img.width = 9;
  img.height = 16;
  img.src = 'data:image/png;base64,' + 'iVBORw0KGgoAAAANSUhEUgAAAAkAAAAQCAYAAADESFVDAAAAAXNSR0IArs4c6QAAAAZiS0dEANAA' + 'zwDP4Z7KegAAAAlwSFlzAAAOxAAADsQBlSsOGwAAAAd0SU1FB9sHGw0cMqdt1UwAAAAZdEVYdENv' + 'bW1lbnQAQ3JlYXRlZCB3aXRoIEdJTVBXgQ4XAAAAaElEQVQoz+3SsRFAQBCF4Z9WJM8KCDVwownl' + '6YXsTmCUsyKGkZzcl7zkz3YLkypgAnreFmDEpHkIwVOMfpdi9CEEN2nGpFdwD03yEqDtOgCaun7s' + 'qSTDH32I1pQA2Pb9sZecAxc5r3IAb21d6878xsAAAAAASUVORK5CYII=';

  if (this.isMobileDevice_) {
    img.width *= 2;
    img.height *= 2;
  }

  this.leftZoomHandle_ = img;
  this.rightZoomHandle_ = img.cloneNode(false);
};

/**
 * @private
 * Sets up the interaction for the range selector.
 */
rangeSelector.prototype.initInteraction_ = function () {
  var self = this;
  var topElem = document;
  var clientXLast = 0;
  var handle = null;
  var isZooming = false;
  var isPanning = false;
  var dynamic = !this.isMobileDevice_;

  // We cover iframes during mouse interactions. See comments in
  // dygraph-utils.js for more info on why this is a good idea.
  var tarp = new _iframeTarp2['default']();

  // functions, defined below.  Defining them this way (rather than with
  // "function foo() {...}" makes JSHint happy.
  var toXDataWindow, onZoomStart, onZoom, onZoomEnd, doZoom, isMouseInPanZone, onPanStart, onPan, onPanEnd, doPan, onCanvasHover;

  // Touch event functions
  var onZoomHandleTouchEvent, onCanvasTouchEvent, addTouchEvents;

  toXDataWindow = function (zoomHandleStatus) {
    var xDataLimits = self.dygraph_.xAxisExtremes();
    var fact = (xDataLimits[1] - xDataLimits[0]) / self.canvasRect_.w;
    var xDataMin = xDataLimits[0] + (zoomHandleStatus.leftHandlePos - self.canvasRect_.x) * fact;
    var xDataMax = xDataLimits[0] + (zoomHandleStatus.rightHandlePos - self.canvasRect_.x) * fact;
    return [xDataMin, xDataMax];
  };

  onZoomStart = function (e) {
    utils.cancelEvent(e);
    isZooming = true;
    clientXLast = e.clientX;
    handle = e.target ? e.target : e.srcElement;
    if (e.type === 'mousedown' || e.type === 'dragstart') {
      // These events are removed manually.
      utils.addEvent(topElem, 'mousemove', onZoom);
      utils.addEvent(topElem, 'mouseup', onZoomEnd);
    }
    self.fgcanvas_.style.cursor = 'col-resize';
    tarp.cover();
    return true;
  };

  onZoom = function (e) {
    if (!isZooming) {
      return false;
    }
    utils.cancelEvent(e);

    var delX = e.clientX - clientXLast;
    if (Math.abs(delX) < 4) {
      return true;
    }
    clientXLast = e.clientX;

    // Move handle.
    var zoomHandleStatus = self.getZoomHandleStatus_();
    var newPos;
    if (handle == self.leftZoomHandle_) {
      newPos = zoomHandleStatus.leftHandlePos + delX;
      newPos = Math.min(newPos, zoomHandleStatus.rightHandlePos - handle.width - 3);
      newPos = Math.max(newPos, self.canvasRect_.x);
    } else {
      newPos = zoomHandleStatus.rightHandlePos + delX;
      newPos = Math.min(newPos, self.canvasRect_.x + self.canvasRect_.w);
      newPos = Math.max(newPos, zoomHandleStatus.leftHandlePos + handle.width + 3);
    }
    var halfHandleWidth = handle.width / 2;
    handle.style.left = newPos - halfHandleWidth + 'px';
    self.drawInteractiveLayer_();

    // Zoom on the fly.
    if (dynamic) {
      doZoom();
    }
    return true;
  };

  onZoomEnd = function (e) {
    if (!isZooming) {
      return false;
    }
    isZooming = false;
    tarp.uncover();
    utils.removeEvent(topElem, 'mousemove', onZoom);
    utils.removeEvent(topElem, 'mouseup', onZoomEnd);
    self.fgcanvas_.style.cursor = 'default';

    // If on a slower device, zoom now.
    if (!dynamic) {
      doZoom();
    }
    return true;
  };

  doZoom = function () {
    try {
      var zoomHandleStatus = self.getZoomHandleStatus_();
      self.isChangingRange_ = true;
      if (!zoomHandleStatus.isZoomed) {
        self.dygraph_.resetZoom();
      } else {
        var xDataWindow = toXDataWindow(zoomHandleStatus);
        self.dygraph_.doZoomXDates_(xDataWindow[0], xDataWindow[1]);
      }
    } finally {
      self.isChangingRange_ = false;
    }
  };

  isMouseInPanZone = function (e) {
    var rect = self.leftZoomHandle_.getBoundingClientRect();
    var leftHandleClientX = rect.left + rect.width / 2;
    rect = self.rightZoomHandle_.getBoundingClientRect();
    var rightHandleClientX = rect.left + rect.width / 2;
    return e.clientX > leftHandleClientX && e.clientX < rightHandleClientX;
  };

  onPanStart = function (e) {
    if (!isPanning && isMouseInPanZone(e) && self.getZoomHandleStatus_().isZoomed) {
      utils.cancelEvent(e);
      isPanning = true;
      clientXLast = e.clientX;
      if (e.type === 'mousedown') {
        // These events are removed manually.
        utils.addEvent(topElem, 'mousemove', onPan);
        utils.addEvent(topElem, 'mouseup', onPanEnd);
      }
      return true;
    }
    return false;
  };

  onPan = function (e) {
    if (!isPanning) {
      return false;
    }
    utils.cancelEvent(e);

    var delX = e.clientX - clientXLast;
    if (Math.abs(delX) < 4) {
      return true;
    }
    clientXLast = e.clientX;

    // Move range view
    var zoomHandleStatus = self.getZoomHandleStatus_();
    var leftHandlePos = zoomHandleStatus.leftHandlePos;
    var rightHandlePos = zoomHandleStatus.rightHandlePos;
    var rangeSize = rightHandlePos - leftHandlePos;
    if (leftHandlePos + delX <= self.canvasRect_.x) {
      leftHandlePos = self.canvasRect_.x;
      rightHandlePos = leftHandlePos + rangeSize;
    } else if (rightHandlePos + delX >= self.canvasRect_.x + self.canvasRect_.w) {
      rightHandlePos = self.canvasRect_.x + self.canvasRect_.w;
      leftHandlePos = rightHandlePos - rangeSize;
    } else {
      leftHandlePos += delX;
      rightHandlePos += delX;
    }
    var halfHandleWidth = self.leftZoomHandle_.width / 2;
    self.leftZoomHandle_.style.left = leftHandlePos - halfHandleWidth + 'px';
    self.rightZoomHandle_.style.left = rightHandlePos - halfHandleWidth + 'px';
    self.drawInteractiveLayer_();

    // Do pan on the fly.
    if (dynamic) {
      doPan();
    }
    return true;
  };

  onPanEnd = function (e) {
    if (!isPanning) {
      return false;
    }
    isPanning = false;
    utils.removeEvent(topElem, 'mousemove', onPan);
    utils.removeEvent(topElem, 'mouseup', onPanEnd);
    // If on a slower device, do pan now.
    if (!dynamic) {
      doPan();
    }
    return true;
  };

  doPan = function () {
    try {
      self.isChangingRange_ = true;
      self.dygraph_.dateWindow_ = toXDataWindow(self.getZoomHandleStatus_());
      self.dygraph_.drawGraph_(false);
    } finally {
      self.isChangingRange_ = false;
    }
  };

  onCanvasHover = function (e) {
    if (isZooming || isPanning) {
      return;
    }
    var cursor = isMouseInPanZone(e) ? 'move' : 'default';
    if (cursor != self.fgcanvas_.style.cursor) {
      self.fgcanvas_.style.cursor = cursor;
    }
  };

  onZoomHandleTouchEvent = function (e) {
    if (e.type == 'touchstart' && e.targetTouches.length == 1) {
      if (onZoomStart(e.targetTouches[0])) {
        utils.cancelEvent(e);
      }
    } else if (e.type == 'touchmove' && e.targetTouches.length == 1) {
      if (onZoom(e.targetTouches[0])) {
        utils.cancelEvent(e);
      }
    } else {
      onZoomEnd(e);
    }
  };

  onCanvasTouchEvent = function (e) {
    if (e.type == 'touchstart' && e.targetTouches.length == 1) {
      if (onPanStart(e.targetTouches[0])) {
        utils.cancelEvent(e);
      }
    } else if (e.type == 'touchmove' && e.targetTouches.length == 1) {
      if (onPan(e.targetTouches[0])) {
        utils.cancelEvent(e);
      }
    } else {
      onPanEnd(e);
    }
  };

  addTouchEvents = function (elem, fn) {
    var types = ['touchstart', 'touchend', 'touchmove', 'touchcancel'];
    for (var i = 0; i < types.length; i++) {
      self.dygraph_.addAndTrackEvent(elem, types[i], fn);
    }
  };

  this.setDefaultOption_('interactionModel', _dygraphInteractionModel2['default'].dragIsPanInteractionModel);
  this.setDefaultOption_('panEdgeFraction', 0.0001);

  var dragStartEvent = window.opera ? 'mousedown' : 'dragstart';
  this.dygraph_.addAndTrackEvent(this.leftZoomHandle_, dragStartEvent, onZoomStart);
  this.dygraph_.addAndTrackEvent(this.rightZoomHandle_, dragStartEvent, onZoomStart);

  this.dygraph_.addAndTrackEvent(this.fgcanvas_, 'mousedown', onPanStart);
  this.dygraph_.addAndTrackEvent(this.fgcanvas_, 'mousemove', onCanvasHover);

  // Touch events
  if (this.hasTouchInterface_) {
    addTouchEvents(this.leftZoomHandle_, onZoomHandleTouchEvent);
    addTouchEvents(this.rightZoomHandle_, onZoomHandleTouchEvent);
    addTouchEvents(this.fgcanvas_, onCanvasTouchEvent);
  }
};

/**
 * @private
 * Draws the static layer in the background canvas.
 */
rangeSelector.prototype.drawStaticLayer_ = function () {
  var ctx = this.bgcanvas_ctx_;
  ctx.clearRect(0, 0, this.canvasRect_.w, this.canvasRect_.h);
  try {
    this.drawMiniPlot_();
  } catch (ex) {
    console.warn(ex);
  }

  var margin = 0.5;
  this.bgcanvas_ctx_.lineWidth = this.getOption_('rangeSelectorBackgroundLineWidth');
  ctx.strokeStyle = this.getOption_('rangeSelectorBackgroundStrokeColor');
  ctx.beginPath();
  ctx.moveTo(margin, margin);
  ctx.lineTo(margin, this.canvasRect_.h - margin);
  ctx.lineTo(this.canvasRect_.w - margin, this.canvasRect_.h - margin);
  ctx.lineTo(this.canvasRect_.w - margin, margin);
  ctx.stroke();
};

/**
 * @private
 * Draws the mini plot in the background canvas.
 */
rangeSelector.prototype.drawMiniPlot_ = function () {
  var fillStyle = this.getOption_('rangeSelectorPlotFillColor');
  var fillGradientStyle = this.getOption_('rangeSelectorPlotFillGradientColor');
  var strokeStyle = this.getOption_('rangeSelectorPlotStrokeColor');
  if (!fillStyle && !strokeStyle) {
    return;
  }

  var stepPlot = this.getOption_('stepPlot');

  var combinedSeriesData = this.computeCombinedSeriesAndLimits_();
  var yRange = combinedSeriesData.yMax - combinedSeriesData.yMin;

  // Draw the mini plot.
  var ctx = this.bgcanvas_ctx_;
  var margin = 0.5;

  var xExtremes = this.dygraph_.xAxisExtremes();
  var xRange = Math.max(xExtremes[1] - xExtremes[0], 1.e-30);
  var xFact = (this.canvasRect_.w - margin) / xRange;
  var yFact = (this.canvasRect_.h - margin) / yRange;
  var canvasWidth = this.canvasRect_.w - margin;
  var canvasHeight = this.canvasRect_.h - margin;

  var prevX = null,
      prevY = null;

  ctx.beginPath();
  ctx.moveTo(margin, canvasHeight);
  for (var i = 0; i < combinedSeriesData.data.length; i++) {
    var dataPoint = combinedSeriesData.data[i];
    var x = dataPoint[0] !== null ? (dataPoint[0] - xExtremes[0]) * xFact : NaN;
    var y = dataPoint[1] !== null ? canvasHeight - (dataPoint[1] - combinedSeriesData.yMin) * yFact : NaN;

    // Skip points that don't change the x-value. Overly fine-grained points
    // can cause major slowdowns with the ctx.fill() call below.
    if (!stepPlot && prevX !== null && Math.round(x) == Math.round(prevX)) {
      continue;
    }

    if (isFinite(x) && isFinite(y)) {
      if (prevX === null) {
        ctx.lineTo(x, canvasHeight);
      } else if (stepPlot) {
        ctx.lineTo(x, prevY);
      }
      ctx.lineTo(x, y);
      prevX = x;
      prevY = y;
    } else {
      if (prevX !== null) {
        if (stepPlot) {
          ctx.lineTo(x, prevY);
          ctx.lineTo(x, canvasHeight);
        } else {
          ctx.lineTo(prevX, canvasHeight);
        }
      }
      prevX = prevY = null;
    }
  }
  ctx.lineTo(canvasWidth, canvasHeight);
  ctx.closePath();

  if (fillStyle) {
    var lingrad = this.bgcanvas_ctx_.createLinearGradient(0, 0, 0, canvasHeight);
    if (fillGradientStyle) {
      lingrad.addColorStop(0, fillGradientStyle);
    }
    lingrad.addColorStop(1, fillStyle);
    this.bgcanvas_ctx_.fillStyle = lingrad;
    ctx.fill();
  }

  if (strokeStyle) {
    this.bgcanvas_ctx_.strokeStyle = strokeStyle;
    this.bgcanvas_ctx_.lineWidth = this.getOption_('rangeSelectorPlotLineWidth');
    ctx.stroke();
  }
};

/**
 * @private
 * Computes and returns the combined series data along with min/max for the mini plot.
 * The combined series consists of averaged values for all series.
 * When series have error bars, the error bars are ignored.
 * @return {Object} An object containing combined series array, ymin, ymax.
 */
rangeSelector.prototype.computeCombinedSeriesAndLimits_ = function () {
  var g = this.dygraph_;
  var logscale = this.getOption_('logscale');
  var i;

  // Select series to combine. By default, all series are combined.
  var numColumns = g.numColumns();
  var labels = g.getLabels();
  var includeSeries = new Array(numColumns);
  var anySet = false;
  var visibility = g.visibility();
  var inclusion = [];

  for (i = 1; i < numColumns; i++) {
    var include = this.getOption_('showInRangeSelector', labels[i]);
    inclusion.push(include);
    if (include !== null) anySet = true; // it's set explicitly for this series
  }

  if (anySet) {
    for (i = 1; i < numColumns; i++) {
      includeSeries[i] = inclusion[i - 1];
    }
  } else {
    for (i = 1; i < numColumns; i++) {
      includeSeries[i] = visibility[i - 1];
    }
  }

  // Create a combined series (average of selected series values).
  // TODO(danvk): short-circuit if there's only one series.
  var rolledSeries = [];
  var dataHandler = g.dataHandler_;
  var options = g.attributes_;
  for (i = 1; i < g.numColumns(); i++) {
    if (!includeSeries[i]) continue;
    var series = dataHandler.extractSeries(g.rawData_, i, options);
    if (g.rollPeriod() > 1) {
      series = dataHandler.rollingAverage(series, g.rollPeriod(), options);
    }

    rolledSeries.push(series);
  }

  var combinedSeries = [];
  for (i = 0; i < rolledSeries[0].length; i++) {
    var sum = 0;
    var count = 0;
    for (var j = 0; j < rolledSeries.length; j++) {
      var y = rolledSeries[j][i][1];
      if (y === null || isNaN(y)) continue;
      count++;
      sum += y;
    }
    combinedSeries.push([rolledSeries[0][i][0], sum / count]);
  }

  // Compute the y range.
  var yMin = Number.MAX_VALUE;
  var yMax = -Number.MAX_VALUE;
  for (i = 0; i < combinedSeries.length; i++) {
    var yVal = combinedSeries[i][1];
    if (yVal !== null && isFinite(yVal) && (!logscale || yVal > 0)) {
      yMin = Math.min(yMin, yVal);
      yMax = Math.max(yMax, yVal);
    }
  }

  // Convert Y data to log scale if needed.
  // Also, expand the Y range to compress the mini plot a little.
  var extraPercent = 0.25;
  if (logscale) {
    yMax = utils.log10(yMax);
    yMax += yMax * extraPercent;
    yMin = utils.log10(yMin);
    for (i = 0; i < combinedSeries.length; i++) {
      combinedSeries[i][1] = utils.log10(combinedSeries[i][1]);
    }
  } else {
    var yExtra;
    var yRange = yMax - yMin;
    if (yRange <= Number.MIN_VALUE) {
      yExtra = yMax * extraPercent;
    } else {
      yExtra = yRange * extraPercent;
    }
    yMax += yExtra;
    yMin -= yExtra;
  }

  return { data: combinedSeries, yMin: yMin, yMax: yMax };
};

/**
 * @private
 * Places the zoom handles in the proper position based on the current X data window.
 */
rangeSelector.prototype.placeZoomHandles_ = function () {
  var xExtremes = this.dygraph_.xAxisExtremes();
  var xWindowLimits = this.dygraph_.xAxisRange();
  var xRange = xExtremes[1] - xExtremes[0];
  var leftPercent = Math.max(0, (xWindowLimits[0] - xExtremes[0]) / xRange);
  var rightPercent = Math.max(0, (xExtremes[1] - xWindowLimits[1]) / xRange);
  var leftCoord = this.canvasRect_.x + this.canvasRect_.w * leftPercent;
  var rightCoord = this.canvasRect_.x + this.canvasRect_.w * (1 - rightPercent);
  var handleTop = Math.max(this.canvasRect_.y, this.canvasRect_.y + (this.canvasRect_.h - this.leftZoomHandle_.height) / 2);
  var halfHandleWidth = this.leftZoomHandle_.width / 2;
  this.leftZoomHandle_.style.left = leftCoord - halfHandleWidth + 'px';
  this.leftZoomHandle_.style.top = handleTop + 'px';
  this.rightZoomHandle_.style.left = rightCoord - halfHandleWidth + 'px';
  this.rightZoomHandle_.style.top = this.leftZoomHandle_.style.top;

  this.leftZoomHandle_.style.visibility = 'visible';
  this.rightZoomHandle_.style.visibility = 'visible';
};

/**
 * @private
 * Draws the interactive layer in the foreground canvas.
 */
rangeSelector.prototype.drawInteractiveLayer_ = function () {
  var ctx = this.fgcanvas_ctx_;
  ctx.clearRect(0, 0, this.canvasRect_.w, this.canvasRect_.h);
  var margin = 1;
  var width = this.canvasRect_.w - margin;
  var height = this.canvasRect_.h - margin;
  var zoomHandleStatus = this.getZoomHandleStatus_();

  ctx.strokeStyle = this.getOption_('rangeSelectorForegroundStrokeColor');
  ctx.lineWidth = this.getOption_('rangeSelectorForegroundLineWidth');
  if (!zoomHandleStatus.isZoomed) {
    ctx.beginPath();
    ctx.moveTo(margin, margin);
    ctx.lineTo(margin, height);
    ctx.lineTo(width, height);
    ctx.lineTo(width, margin);
    ctx.stroke();
  } else {
    var leftHandleCanvasPos = Math.max(margin, zoomHandleStatus.leftHandlePos - this.canvasRect_.x);
    var rightHandleCanvasPos = Math.min(width, zoomHandleStatus.rightHandlePos - this.canvasRect_.x);

    ctx.fillStyle = 'rgba(240, 240, 240, ' + this.getOption_('rangeSelectorAlpha').toString() + ')';
    ctx.fillRect(0, 0, leftHandleCanvasPos, this.canvasRect_.h);
    ctx.fillRect(rightHandleCanvasPos, 0, this.canvasRect_.w - rightHandleCanvasPos, this.canvasRect_.h);

    ctx.beginPath();
    ctx.moveTo(margin, margin);
    ctx.lineTo(leftHandleCanvasPos, margin);
    ctx.lineTo(leftHandleCanvasPos, height);
    ctx.lineTo(rightHandleCanvasPos, height);
    ctx.lineTo(rightHandleCanvasPos, margin);
    ctx.lineTo(width, margin);
    ctx.stroke();
  }
};

/**
 * @private
 * Returns the current zoom handle position information.
 * @return {Object} The zoom handle status.
 */
rangeSelector.prototype.getZoomHandleStatus_ = function () {
  var halfHandleWidth = this.leftZoomHandle_.width / 2;
  var leftHandlePos = parseFloat(this.leftZoomHandle_.style.left) + halfHandleWidth;
  var rightHandlePos = parseFloat(this.rightZoomHandle_.style.left) + halfHandleWidth;
  return {
    leftHandlePos: leftHandlePos,
    rightHandlePos: rightHandlePos,
    isZoomed: leftHandlePos - 1 > this.canvasRect_.x || rightHandlePos + 1 < this.canvasRect_.x + this.canvasRect_.w
  };
};

exports['default'] = rangeSelector;
module.exports = exports['default'];

},{"../dygraph-interaction-model":12,"../dygraph-utils":17,"../iframe-tarp":19}]},{},[18])(18)
});
//# sourceMappingURL=dygraph.js.map




function gpxGraph(divId, url, highlightGpxPoint, clickGpxPoint) {
    function parseGpxFromUrl(url, callback) {
        var req = new window.XMLHttpRequest();
        req.open('GET', url, true);
        try {
            req.overrideMimeType('text/xml'); // unsupported by IE
        } catch(e) {}
        req.onreadystatechange = function() {
            if (req.readyState != 4) return;
            if (req.status == 200) {
                callback(parseGpxFromXml(req.responseXML));
            } else {
                callback(false);
            }
        };
        req.send(null);
    }

    function parseGpxFromXml(gpx) {
        var output = [];
        var points = gpx.getElementsByTagName("trkpt");
        for (var i = 0; i < points.length; i++) {
            var point = points[i];
            var out = {};
            out.lat = point.getAttribute("lat");
            out.lon = point.getAttribute("lon");
            var eles = point.getElementsByTagName("ele");
            if (eles.length == 1) {
                out.ele = parseFloat(eles[0].textContent);
            }
            var times = point.getElementsByTagName("time");
            if (times.length == 1) {
                out.time = Date.parse(times[0].textContent);
            }
            output.push(out);
        }
        return output;
    }

    function haversineDistance(point1, point2) {
        var lat1 = point1["lat"];
        var lon1 = point1["lon"];
        var lat2 = point2["lat"];
        var lon2 = point2["lon"];
        // https://www.movable-type.co.uk/scripts/latlong.html

        function toRadians(degrees) { return degrees * Math.PI / 180; };
        
        var R = 6371e3; // radius of earth in metres
        var φ1 = toRadians(lat1);
        var φ2 = toRadians(lat2);
        var Δφ = toRadians(lat2-lat1);
        var Δλ = toRadians(lon2-lon1);

        var a = Math.sin(Δφ/2) * Math.sin(Δφ/2) +
            Math.cos(φ1) * Math.cos(φ2) *
            Math.sin(Δλ/2) * Math.sin(Δλ/2);
        var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));

        var d = R * c;
        return d;
    }

    function gpxPlot(divId, gpx, highlightGpxPoint) {
        var data = [];
        var totalDistance = 0.0
        for (var i = 0; i < gpx.length; i++) {
            var point = gpx[i];

            if (i == 0) {
                data.push([new Date(point.time), point.ele, null, null]);
            } else  {
                var prevPoint = gpx[i - 1];

                var distance = haversineDistance(prevPoint, point); // m
                totalDistance += distance;

                var diff = point.time - prevPoint.time; // ms
                var speed = (distance / 1000) / (diff / 1000 / 60 / 60); // km/h

                data.push([new Date(point.time), point.ele, speed, totalDistance]);
            }
        }

        function highlightCallback(event, x, points, row, seriesName) {
            if (highlightGpxPoint) highlightGpxPoint(gpx[row]);
        }

        function clickCallback(event, x, points) {
            if (clickGpxPoint) clickGpxPoint(gpx[points[0].idx]);
        }
        
        return new Dygraph(document.getElementById(divId), data,
                           {
                               labels: ["Date", "Elevation", "Speed(km/h)", "Distance(m)"],
                               series: { "Distance(m)": { axis: "y2" } },
                               highlightCallback: highlightCallback,
                               clickCallback: clickCallback
                               // y2label: "Distance(m)",
                               // axes: { y2: { axisLabelWidth: 90 } }
                           });
    }

    var plot = false;
    parseGpxFromUrl(url,
                    function(gpx) {
                        plot = gpxPlot(divId, gpx, highlightGpxPoint);
                    });

    return function() { return plot.destroy(); };
}
    </script>
  </head>

  
  <body>
    <div id="mapid"></div>
    <div id="info" style="position:absolute;bottom:0px;z-index:9999;width:100%;background-color:white;display:none">
      <a href="#" onclick="document.getElementById('info').style.display='none';">close</a>
      <div id="infoinfo" style="width:100%;"></div>
    </div>
    <script>
      var mymap = L.map('mapid').setView([51.505, -0.09], 13);

      L.tileLayer('http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}',{
      maxZoom: 20,
      subdomains:['mt0','mt1','mt2','mt3']
      }).addTo(mymap);

      global_prev_clicked_layer = null;
      function gpxclick(evt) {
        var gpx = evt.target;

        var info = document.getElementById("info");
        info.style.display = "block";

        var popup = L.popup();
        popup.setContent("<p>" + "name: " + gpx.get_name() + "<br/>"
                               + "start: " + gpx.get_start_time().toString() + "<br/>"
                               + "end: " + gpx.get_end_time().toString() + "<br/>"
                               + "duration: " + gpx.get_duration_string(gpx.get_total_time()) 
                                   + ", " + gpx.get_total_speed().toFixed(2) + " km/h<br/>"
                               + "moving duration: " + gpx.get_duration_string(gpx.get_moving_time()) 
                                   + ", " + gpx.get_moving_speed().toFixed(2) + " km/h<br/>"
                               + "elevation: +" + gpx.get_elevation_gain().toFixed(0)
                                 + ", -" + gpx.get_elevation_loss().toFixed(0)
                                 + ", =" + (gpx.get_elevation_gain() - gpx.get_elevation_loss()).toFixed(0) + "<br/>"
                               + "number of points: " + gpx._info.number_of_points + "<br/>"
                               + "</p>"
                               + "<div id=gpxplotid></div>"
                         + '<a href="#" onclick="mymap.removeLayer(global_prev_clicked_layer);">hide</a>');
        global_prev_clicked_layer = evt.layer; 
        popup.setLatLng(evt.latlng).openOn(mymap);
        global_gpxgraph_cleaner = null;
        var myIcon = L.icon({
          iconUrl: _DEFAULT_MARKER_OPTS.startIconUrl,
          iconSize: [33, 50],
          iconAnchor: [16, 45],
        });
        global_gpxgraph_marker = new L.Marker([0.0, 0.0], {icon: myIcon});
        global_gpxgraph_marker.addTo(mymap);
        if (global_gpxgraph_cleaner != null) global_gpxgraph_cleaner();
        global_gpxgraph_cleaner = gpxGraph("infoinfo", gpx._gpx,
              function(point) {
                global_gpxgraph_marker.setLatLng([point.lat, point.lon]);
              },
              function(point) {
                mymap.panTo([point.lat, point.lon], {animate:true});
              });
      }

      {{{GPXS}}}

      var photos = [
      {{{PHOTOS}}}
      ];

      var photoLayer = L.photo.cluster().on('click', function(evt) {
      var photo = evt.layer.photo;
      var template = "<a href='{url}'><img src='{url}' style='max-width:500px; max-height:500px; width:auto; height:auto' /></a><p>{name}</p>";
      evt.layer.bindPopup(L.Util.template(template, photo), { maxWidth:600}).openPopup();
      });
      photoLayer.add(photos).addTo(mymap);
      mymap.fitBounds(photoLayer.getBounds());
    </script>
  </body>
</html>

"""

def dms2dd(degrees, minutes, seconds, direction):
    dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60)
    if direction == 'S' or direction == 'W':
        dd *= -1
    return dd

def exif_data(file):
    img = PIL.Image.open(file)
    tags = img._getexif()

    if not tags or not 34853 in tags or len(tags[34853]) < 5:
        return None
    
    gpstag = tags[34853]

    gpstag_latitude_ref = gpstag[1]
    gpstag_latitude = gpstag[2]
    gpstag_latitude_degrees = gpstag_latitude[0][0] / gpstag_latitude[0][1];
    gpstag_latitude_minutes = gpstag_latitude[1][0] / gpstag_latitude[1][1];
    gpstag_latitude_seconds = gpstag_latitude[2][0] / gpstag_latitude[2][1];
    latitude = dms2dd(gpstag_latitude_degrees, gpstag_latitude_minutes,
                      gpstag_latitude_seconds, gpstag_latitude_ref);
    
    gpstag_longtitude = gpstag[4]
    gpstag_longtitude_ref = gpstag[3]
    gpstag_longtitude_degrees = gpstag_longtitude[0][0] / gpstag_longtitude[0][1];
    gpstag_longtitude_minutes = gpstag_longtitude[1][0] / gpstag_longtitude[1][1];
    gpstag_longtitude_seconds = gpstag_longtitude[2][0] / gpstag_longtitude[2][1];
    longtitude = dms2dd(gpstag_longtitude_degrees, gpstag_longtitude_minutes,
                        gpstag_longtitude_seconds, gpstag_longtitude_ref);

    output = {"lat":latitude, "lng":longtitude}

    if 5 in gpstag and 6 in gpstag:
        altitude = gpstag[6][0] / gpstag[6][1]
        above_sea_level = gpstag[5]
        if above_sea_level == 1:
            altitude *= -1
        output["altitude"] = altitude

    if 36867 in tags:
        output["date"] = str(tags[36867])

    if 271 in tags or 272 in tags:
        output["camera"] = ""
        if 271 in tags:
            output["camera"] += tags[271] + " "
        if 272 in tags:
            output["camera"] += tags[272]
        
    return output

def make_map_with_photos(files, outputname):
    photos_added = 0
    gpxtracks_added = 0
    skipped = 0
    photos_string = ""
    gpxs_string = ""
    for file in files:
        if file.lower().endswith(".gpx"):
            gpxs_string += "new L.GPX('"+file+"', {async: true}).on('click', gpxclick).addTo(mymap);"
            gpxtracks_added += 1
        else:
            exif = exif_data(file);
            if exif:
                latitude = exif["lat"]
                longtitude = exif["lng"]
                photos_string += "{\"lat\":"+str(latitude)+", \"lng\":"+str(longtitude)
                photos_string += ", \"thumbnail\":\""+file+"\", \"url\":\""+file+"\""
                photos_string += ", \"name\":\""+file
                if "date" in exif:
                    photos_string += "<br/>"+exif["date"]
                if "altitude" in exif:
                    photos_string += "<br/>Altitude: "+str(exif["altitude"])+"m"
                if "camera" in exif:
                    photos_string += "<br/>Camera: " + str(exif["camera"]);
                photos_string += "\"},\n"
                photos_added += 1
            else:
                skipped += 1
            
    html = template.replace("{{{PHOTOS}}}", photos_string).replace("{{{GPXS}}}", gpxs_string);
    open(outputname, "w").write(html)
    return {"photos_added": photos_added, "gpxtracks_added": gpxtracks_added, "skipped": skipped}

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        print(make_map_with_photos(sys.argv[1:], "map.html"))
    else:
        print("Usage: " + sys.argv[0] + " file1.jpg file2.jpg file3.gpx ...")
