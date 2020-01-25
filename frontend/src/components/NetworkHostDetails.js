import React from 'react';
import {Container, Button} from 'react-bootstrap';
import ApiClient from '../utils/ApiClient';
import ActivityChart from './ActivityChart';

export default class NetworkHostDetails extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            services: [],
            fingerprints: [],
            vulnerabilities: [],
            activity: {
                hours: [],
                weekdays: []
            }
        };
    }

    editDevice() {
        const {params} = this.props.match;
        const deviceId = parseInt(params.deviceId);
        const label = prompt("Neue Bezeichnung?", this.state.label)
        if (label) {
            this.api.updateDevice(deviceId, {label})
                .catch(alert);
            this.setState({label});
        }
    }

    componentDidMount() {
        const {params} = this.props.match;
        const deviceId = parseInt(params.deviceId);

        this.api = new ApiClient();
        this.api.getDevice(deviceId)
            .then(data => {
                this.setState({...data});
            })
            .catch(alert);
    }

    render() {
        let identity_rows;
        if (this.state.fingerprints.length > 0) {
            identity_rows = this.state.fingerprints.map(fp => <tr>
                <td>{fp.type}</td>
                <td>{fp.value}</td>
            </tr>);
        }

        let vulnerabilities_table;
        if (this.state.vulnerabilities.length > 0) {
            vulnerabilities_table = (
                <table className="table host-vulnerabilities-table">
                    <thead>
                        <th>Typ</th>
                        <th>Beschreibung</th>
                    </thead>
                    <tbody>
                        {this.state.vulnerabilities.map(vuln => <tr>
                            <td><span role="img" aria-label="Warning">⚠️</span> {vuln.type}</td>
                            <td>{vuln.description}</td>
                        </tr>)}
                    </tbody>
                </table>
            );
        } else {
            vulnerabilities_table = (
                <div>Keine Schwachstellen gefunden</div>
            );
        }

        let services_table;
        if (this.state.services.length > 0) {
            services_table = (
                <table className="table host-services-table">
                    <thead>
                        <th>Typ</th>
                        <th>Adresse</th>
                    </thead>
                    <tbody>
                        {this.state.services.map(service => <tr>
                            <td>{service.type}</td>
                            <td>{service.address}</td>
                        </tr>)}
                    </tbody>
                </table>
            );
        } else {
            services_table = (
                <div>Keine Dienste gefunden</div>
            );
        }

        return (
            <Container className="host-details">
                <h2>
                    {this.state.label || this.state.hostname}
                    <Button variant="link" onClick={() => this.editDevice()}>Umbenennen</Button>
                </h2>
                <h4>Details</h4>
                <table className="table host-details-table">
                    <tbody>
                        <tr>
                            <td>Letzte Aktivität</td>
                            <td>{this.state.last_heartbeat}</td>
                        </tr>
                        <tr>
                            <td>IP-Adresse</td>
                            <td>{this.state.ip_address}</td>
                        </tr>
                        <tr>
                            <td>MAC-Adresse</td>
                            <td>{this.state.mac_address}</td>
                        </tr>
                        <tr>
                            <td>Hersteller</td>
                            <td>{this.state.mac_vendor}</td>
                        </tr>
                        <tr>
                            <td>Hostname</td>
                            <td>{this.state.hostname && this.state.hostname !== this.state.ip_address ? this.state.hostname : '(keiner)'}</td>
                        </tr>
                        {identity_rows}
                    </tbody>
                </table>
                <br />
                <h4>Schwachstellen</h4>
                {vulnerabilities_table}
                <br />
                <h4>Angebotene Dienste</h4>
                {services_table}
                <br />
                <h4>Aktivität</h4>
                <h5>Nach Stunden</h5>
                <ActivityChart data={this.state.activity.hours} unit="hour" />
                <h5>Nach Wochentag</h5>
                <ActivityChart data={this.state.activity.weekdays} unit="weekday" />
            </Container> 
        );
    }
}
