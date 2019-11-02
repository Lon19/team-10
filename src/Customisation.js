import React, { Component } from 'react';
import { BrowserRouter as Router, Route } from "react-router-dom";
import styles from "./css/index.css";

class Customisation extends Component {
    constructor(cb) {
        super(cb);
        this.state = {value: "ward"};

        this.handleChange = this.handleChange.bind(this);
    }

    handleChange(event) {
        this.setState({value: event.target.value});
        this.props.cb(this.state.value);
    }
    render() {
        return (
            <div className={styles.right}>
            <select onChange={this.handleChange}>
                <option selected="selected" value="ward">Ward</option>
                <option value="district">District</option>
            </select>
            </div>
        )
    }
}

export default Customisation
