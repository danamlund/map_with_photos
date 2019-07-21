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
				html: '<div style="background-image: url(' + photo.thumbnail + ');"></div>â€‹',
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
					html: '<div style="background-image: url(' + cluster.getAllChildMarkers()[0].photo.thumbnail + ');"></div>â€‹<b>' + cluster.getChildCount() + '</b>'
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
    </script>
  </head>

  
  <body>
    <div id="mapid"></div>
    <script>
      var mymap = L.map('mapid').setView([51.505, -0.09], 13);

      L.tileLayer('http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}',{
      maxZoom: 20,
      subdomains:['mt0','mt1','mt2','mt3']
      }).addTo(mymap);

      global_prev_clicked_layer = null;
      function gpxclick(evt) {
        var gpx = evt.target;
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
                         + '<a href="#" onclick="mymap.removeLayer(global_prev_clicked_layer);">hide</a>');
        global_prev_clicked_layer = evt.layer; 
        popup.setLatLng(evt.latlng).openOn(mymap);
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
