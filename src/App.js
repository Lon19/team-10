import React, { Component } from 'react';
import { BrowserRouter as Router, Route } from "react-router-dom";
import { geoMercator, geoPath, geoEqualEarth, geoProjection, geoAlbers } from "d3-geo";
import styles from "./css/index.css";
import { feature } from "topojson-client";
import Customisation from "./Customisation"

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

let wards_and_lads_values = {};
//[w, l] -> value
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
    usesLads = false;
	constructor() {
		super()
		this.state = {
            wardsData: feature(wards, wards.objects.wards).features,
            ladsData: feature(lads, lads.objects.lad).features,
		}
        this.change_region_preference = this.change_region_preference.bind(this);
	}
	projection() {
		return geoAlbers()
        .center([0, 55.4])
           .rotate([4.4, 0])
           .parallels([50, 60])
			.scale(3000)
			.translate([800/2, 450/2])
		/*geoAlbers()
			.center([0,42.954])
  			.parallels([41,44])
  			.translate([800/2,450/2])
c  			.scale(100)
			.scale(100)
			.translate([800/2, 450/2]);
		*/
	}

    async get_all_data() {
        const response = await fetch("http://127.0.0.1:5005/fetchData");
        let data = JSON.parse(response);
        let districts = data['districts'];
        districts.map((d, ws) => {
            ws.map((w) => {
                let wl = [];
                wl.append(w['ward_name']);
                wl.append(d['districtName']);
                let total = 0;
                total += w['age-group'][0]['value'];
                total += w['age-group'][1]['value'];
                wards_and_lads_values[wl] = total;
            })
        })
    }



    async compute_colour(wd13nm) {
        //const response = await axios.get("http://localhost:5005/fetchData?ward="+wd13nm+"&lad=" + wards_to_lads[wd13nm]);
        // const response = fetch("http://127.0.0.1:5005/fetchData?ward="+wd13nm+"&lad="+wards_to_lads[wd13nm]);
        // fetch("http://127.0.0.1:5005/fetchData?ward="+wd13nm+"&lad="+wards_to_lads[wd13nm]).then(

        // for (int i = 0; i < data['age-group'].size())
        let count = wards_and_lads_values[[wd13nm, wards_to_lads[wd13nm]]];
        // let colour = (38, 50, 56, 0);
        let colour = "#666666";
        if (count <= 20) {
            colour = "#00ff00";
        } else if (count <= 50) {
            colour = "#006600";
        } else if (count <= 105) {
            colour = "ffff00";
        } else if (count <= 145) {
            colour = "#ff8106";
        } else if (count <= 260) {
            colour = "#990000";
        } else {
            colour = "#ff0000";
        }
        return colour;
    }

    change_region_preference(value) {
        if (value.includes("lads")) {
            this.setState({
                usesLads: true
            })
        } else {
            this.setState({
                usesLads: false
            })
        }
    }

    componentDidUpdate() {
        this.render();
    }

	render() {
        this.get_all_data();
		this.state.wardsData.map((d,i) => {
			if(i == 10) {
				console.log(d);
			}
		})
		console.log(this.projection())
        if (!this.state.usesLads) {
    		return (
                <div>
    		    <svg className={styles.left} viewBox="0 0 800 450">
    		        <g className="wards" transform="scale()">
    		          {this.state.wardsData.map((d,i) => (
    		              <path
    		                key={ `path-${ i }` }
    		                d={ geoPath().projection(this.projection())(d) }
    		                className="ward"
    						data-ward-name={ d.properties.WD13NM }
    		                fill={  this.compute_colour(d.properties.WD13NM) }
    		                stroke="#FFFFFF"
    		                strokeWidth={ 0.5 }
    		              />
                      ))
    		          }
    		        </g>
    		      </svg>
                  <div>
                    <Customisation cb={this.change_region_preference}>
                    </Customisation>
                  </div>
                  </div>
    		    )
        } else {
            return (
                <div id="wrapper">
                    <svg className={styles.left} viewBox="0 0 800 450">
        		        <g className="wards" transform="scale()">
        		          {this.state.ladsData.map((d,i) => (
        		              <path
        		                key={ `path-${ i }` }
        		                d={ geoPath().projection(this.projection())(d) }
        		                className="ward"
        						data-ward-name={ d.properties.LAD13NM }
        		                fill={  this.compute_colour(d.properties.LAD13NM) }
        		                stroke="#FFFFFF"
        		                strokeWidth={ 0.5 }
        		              />
                          ))
        		          }
        		        </g>
        		      </svg>
                      <div>
                        <Customisation cb={this.change_region_preference}>
                        </Customisation>
                      </div>
                  </div>
    		    )
        }
	}
}

export default App;
