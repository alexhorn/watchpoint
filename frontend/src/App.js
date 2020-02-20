import React from 'react';
import {
  Route,
  BrowserRouter as Router,
  Switch
} from 'react-router-dom';
import { IntlProvider } from 'react-intl';
import NetworkOverview from './components/NetworkOverview';
import NetworkHostDetails from './components/NetworkHostDetails';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import messages_en from './messages/en.json';
import messages_de from './messages/de.json';

const DEFAULT_LANGUAGE = 'en';
const messages = {en: messages_en, de: messages_de};
const language = navigator.language.split(/[-_]/)[0];

function App() {
  return (
    <Router>
      <IntlProvider locale={language} messages={messages[language] || messages[DEFAULT_LANGUAGE]}>
        <div className="App">
          <Switch>
            <Route path="/devices/:deviceId" component={NetworkHostDetails} />
            <Route path="/" component={NetworkOverview} />
          </Switch>
        </div>
      </IntlProvider>
    </Router>
  );
}

export default App;
