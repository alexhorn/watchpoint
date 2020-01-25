import React from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route
} from "react-router-dom";
import NetworkOverview from './components/NetworkOverview';
import NetworkHostDetails from './components/NetworkHostDetails';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Switch>
          <Route path="/devices/:deviceId" component={NetworkHostDetails} />
          <Route path="/" component={NetworkOverview} />
        </Switch>
      </div>
    </Router>
  );
}

export default App;
