import React from 'react'; 
import { WishlistForm, ItemForm } from './Form';
import axios from 'axios';

function isEmpty(obj) {
    return obj && Object.keys(obj).length === 0 && obj.constructor === Object;
}

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
    this.sendRequest = this.sendRequest.bind(this);
    this.getWishlists = this.getWishlists.bind(this);
    this.getWishlists();
  }

  getWishlists() {
      const options = {
          url: window.location.protocol + '//' + window.document.location.host + '/api/wishlists',
          method: 'GET'
      }
      axios(options).then((resp) => {
          this.setState({ wishlists: resp.data.sort((a, b) => a.id > b.id ? 1 : -1) });
      });
  }
  sendRequest(path, method, data = undefined, callback) {
      const options = {
          url: window.location.protocol + '//' + window.document.location.host + path,
          method
      }
      if ( !isEmpty(data) ) {
          options.data = data;
          options.headers = {
              'Content-Type': 'application/json'
          };
      }
      console.log(options);
      axios(options).then((resp) => {
          console.log('xhr success');
          callback(resp);
      }).catch((err) => {
          console.log('xhr error');
          callback(err.response);
      });
  }

  render() {
    console.log('rendering App', this.state);
    return <div className="formColumns">
      <div className="column wishlists">
        <WishlistForm wishlists={this.state.wishlists} app={this} />
      </div>
      <div className="column middle"></div>
      <div className="column items">
        <ItemForm wishlists={this.state.wishlists} app={this} />
      </div>
    </div>;
  }
}

export default App;
