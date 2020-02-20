import React from 'react';
import { Container, Button } from 'react-bootstrap';
import { FormattedMessage, injectIntl } from 'react-intl';
import ApiClient from '../utils/ApiClient';
import ActivityChart from './ActivityChart';

class NetworkHostDetails extends React.Component {
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
    const label = prompt(this.props.intl.formatMessage({id: 'new_label:'}), this.state.label);
    if (label !== null) {
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
      identity_rows = this.state.fingerprints.map(fp => <tr key={fp.id}>
        <td>{fp.type}</td>
        <td>{fp.value}</td>
      </tr>);
    }

    let vulnerabilities_table;
    if (this.state.vulnerabilities.length > 0) {
      vulnerabilities_table = (
        <table className="table host-vulnerabilities-table">
          <thead>
            <th><FormattedMessage id="type" /></th>
            <th><FormattedMessage id="description" /></th>
          </thead>
          <tbody>
            {this.state.vulnerabilities.map(vuln => <tr key={vuln.id}>
              <td><span role="img" aria-label="Warning">⚠️</span> {vuln.type}</td>
              <td>{vuln.description}</td>
            </tr>)}
          </tbody>
        </table>
      );
    } else {
      vulnerabilities_table = (
        <div><FormattedMessage id="no_vulnerabilities_found" /></div>
      );
    }

    let services_table;
    if (this.state.services.length > 0) {
      services_table = (
        <table className="table host-services-table">
          <thead>
            <th><FormattedMessage id="type" /></th>
            <th><FormattedMessage id="address" /></th>
          </thead>
          <tbody>
            {this.state.services.map(svc => <tr key={svc.id}>
              <td>{svc.type}</td>
              <td>{svc.address}</td>
            </tr>)}
          </tbody>
        </table>
      );
    } else {
      services_table = (
        <div><FormattedMessage id="no_services_found" /></div>
      );
    }

    return (
      <Container className="host-details">
        <h2>
          {this.state.label || this.state.hostname}
          <Button variant="link" onClick={() => this.editDevice()}><FormattedMessage id="rename" /></Button>
        </h2>
        <h4>Details</h4>
        <table className="table host-details-table">
          <tbody>
            <tr>
              <td><FormattedMessage id="last_active" /></td>
              <td>{this.state.last_heartbeat}</td>
            </tr>
            <tr>
              <td><FormattedMessage id="ip_address" /></td>
              <td>{this.state.ip_address}</td>
            </tr>
            <tr>
              <td><FormattedMessage id="mac_address" /></td>
              <td>{this.state.mac_address}</td>
            </tr>
            <tr>
              <td><FormattedMessage id="manufacturer" /></td>
              <td>{this.state.mac_vendor}</td>
            </tr>
            <tr>
              <td><FormattedMessage id="hostname" /></td>
              <td>{this.state.hostname && this.state.hostname !== this.state.ip_address ? this.state.hostname : <FormattedMessage id="(none)" />}</td>
            </tr>
            {identity_rows}
          </tbody>
        </table>
        <br />
        <h4><FormattedMessage id="vulnerabilities" /></h4>
        {vulnerabilities_table}
        <br />
        <h4><FormattedMessage id="services" /></h4>
        {services_table}
        <br />
        <h4><FormattedMessage id="activity" /></h4>
        <h5><FormattedMessage id="by_hours" /></h5>
        <ActivityChart data={this.state.activity.hours} unit="hour" />
        <h5><FormattedMessage id="by_weekdays" /></h5>
        <ActivityChart data={this.state.activity.weekdays} unit="weekday" />
      </Container> 
    );
  }
}

export default injectIntl(NetworkHostDetails);
