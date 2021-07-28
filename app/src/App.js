import React from 'react'; 
import { WishlistForm, ItemForm } from './Form';
import axios from 'axios';

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
      url: `http://127.0.0.1:5000/wishlists`,
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      },
      data: {}
    }
    axios(options).then((resp) => {
      this.setState({ wishlists: resp.data.sort((a, b) => a.id > b.id ? 1 : -1) });
    });
  }
  sendRequest(path, method, data = {}, callback) {
    const options = {
      url: `http://127.0.0.1:5000${path}`,
      method,
      headers: {
        'Content-Type': 'application/json'
      },
      data,
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
