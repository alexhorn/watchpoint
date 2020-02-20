import React from 'react';
import { Container } from 'react-bootstrap';
import { FormattedMessage } from 'react-intl';
import ApiClient from '../utils/ApiClient';
import NetworkHost from './NetworkHost';

export default class NetworkOverview extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      devices: []
    };
  }

  componentDidMount() {
    this.api = new ApiClient();
    this.api.getDevices()
      .then(({devices}) => {
        this.setState({devices});
      })
      .catch(alert);
  }

  render() {
    return (
      <Container>
        <h2>
          <FormattedMessage id="network_overview" />
        </h2>
        {this.state.devices.map(device => <NetworkHost key={device.mac_address} device={device}/>)}
      </Container>
    );
  }
}
