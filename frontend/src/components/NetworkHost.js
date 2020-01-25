import React from 'react';
import {Link} from "react-router-dom";
import ApiClient from '../utils/ApiClient';
import './NetworkHost.css';

export default class NetworkHost extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            vulnerabilities: []
        };
    }

    getOperatingSystem() {
        if (!this.state.fingerprints) {
            return null;
        }

        const fp = this.state.fingerprints.find(fp => fp.type === "operating_system");
        return fp && fp.value;
    }

    componentDidMount() {
        const deviceId = this.props.device.id;

        this.api = new ApiClient();
        this.api.getDevice(deviceId)
            .then(data => {
                this.setState({...data});
            });
    }

    render() {
        return (
            <Link to={`/devices/${this.props.device.id}`}>
                <div className="network-host">
                    <div className="network-host-label">{this.props.device.label || this.props.device.hostname || this.props.device.mac_address}</div>
                    {this.getOperatingSystem() && <div className="network-host-os">{this.getOperatingSystem()}</div>}
                    {this.state.mac_vendor && <div className="network-host-vendor">{this.state.mac_vendor}</div>}
                    {this.state.vulnerabilities.length > 0 && <span className="network-host-warning" role="img" aria-label="Warning">⚠️ Aufmerksamkeit erforderlich</span>}
                </div>
            </Link>
        );
    }
}
