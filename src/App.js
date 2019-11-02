import React, { Component } from 'react';
import { BrowserRouter as Router, Route } from "react-router-dom";
import { geoMercator, geoPath, geoEqualEarth, geoProjection, geoAlbers } from "d3-geo";
import { feature } from "topojson-client";

/*
import Header from './components/header';
import Home from './components/home';
import Address from './components/address';
*/

const wards = require('./data/topo_wards.json');
const lads = require('./data/topo_lad.json');
const wards_features = feature(wards, wards.objects.wards).features;
const lads_features = feature(lads, lads.objects.lad).features;
console.log(wards_features);

let wards_to_lads = {};
wards_features.map((w, i) => {
	let ward = w.properties.WD13NM;
	let wcdo = w.properties.WD13CDO;
	lads_features.map((l, ind) => {
		let lcdo = l.properties.LAD13CDO;
		if (wcdo.substring(0, 4).includes(lcdo)) {
			wards_to_lads[ward] = l.properties.LAD13NM;
		}
	});
});

class App extends Component {
	constructor() {
		super()
		this.state = {
            wardsData: feature(wards, wards.objects.wards).features,
		}
	}
	projection() {
		return geoAlbers()
        .center([0, 55.4])
           .rotate([4.4, 0])
           .parallels([50, 60])
			.scale(4000)
			.translate([800/2, 450/2])
		/*geoAlbers()
			.center([0,42.954])
  			.parallels([41,44])
  			.translate([800/2,450/2])
  			.scale(100)
			.scale(100)
			.translate([800/2, 450/2]);
		*/
	}

	render() {
		this.state.wardsData.map((d,i) => {
			if(i == 10) {
				console.log(d);
			}
		})
		console.log(this.projection())
		return (
		    <svg width="800" height="450" viewBox="0 0 800 450">
		        <g className="wards" transform="scale()">
		          {this.state.wardsData.map((d,i) => (
		              <path
		                key={ `path-${ i }` }
		                d={ geoPath().projection(this.projection())(d) }
		                className="ward"
						data-ward-name={ d.properties.WD13NM }
		                fill={ `rgba(38,50,56,${1 / this.state.wardsData.length * i})` }
		                stroke="#FFFFFF"
		                strokeWidth={ 0.5 }
		              />
		            ))
		          }
		        </g>
		      </svg>
		    )
	}
}

export default App;
