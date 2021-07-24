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
      this.setState({ wishlists: resp.data });
    });
  }
  sendRequest(path, method, data = {}) {
    const options = {
      url: `http://127.0.0.1:5000${path}`,
      method,
      headers: {
        'Content-Type': 'application/json'
      },
      data,
    }
    axios(options).then((resp) => {
      console.log(resp);
    });
  }

  render() {
    console.log('rendering App', this.state);
    return <>
      <WishlistForm wishlists={this.state.wishlists} app={this} />
      <ItemForm wishlists={this.state.wishlists} app={this} />
    </>;
  }
}

export default App;
