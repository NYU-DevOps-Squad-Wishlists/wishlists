import React from 'react'; 
import { Wishlist, Item } from './Model';

function generateInput(input) {
  if ( input[1].type === 'select' ) {
  }
  return <input type="text" name="{input[0]}" />;
}

class WishlistForm extends React.Component {
  constructor(props) {
    super(props);
    this.app = props.app;
    this.state = {};
    this.model = Wishlist;

    this.create = this.create.bind(this);
    this.createCallback = this.createCallback.bind(this);
    this.update = this.update.bind(this);
    this.updateCallback = this.updateCallback.bind(this);
    this.delete = this.delete.bind(this);
    this.deleteCallback = this.deleteCallback.bind(this);
    this.read = this.read.bind(this);
    this.readCallback = this.readCallback.bind(this);
    this.search = this.search.bind(this);
    this.searchCallback = this.searchCallback.bind(this);
    this.handleWishlistNameChange = this.handleWishlistNameChange.bind(this);
    this.handleCustomerIdChange = this.handleCustomerIdChange.bind(this);
  }
  componentDidMount() {
    this.setState({udResult: ''});
  }
  handleWishlistNameChange(e) {
    this.setState({wishlist_name: e.target.value});
  }
  handleCustomerIdChange(e) {
    this.setState({customer_id: e.target.value});
  }
  create(e) {
    e.preventDefault();
    this.app.sendRequest(`/wishlists`, 'POST', {
      name: this.state.wishlist_name,
      customer_id: parseInt(this.state.customer_id)
    }, this.createCallback);
    return false;
  }
  createCallback(resp) {
    if ( resp.status === 201 ) {
      this.setState({createResult: 'Wishlist created successfully!'});
      this.app.getWishlists();
    } else {
      this.setState({createResult: `${resp.data.status} ${resp.data.error}: ${resp.data.message}`});
    }
  }
  update(e, index) {
    e.preventDefault();
    // extract the wishlist_id
    const wishlist_id = document.getElementById(`wishlist_id_${index}`).value;
    if ( wishlist_id ) {
      this.setState({lastUdIndex: index});
      this.app.sendRequest(`/wishlists/${wishlist_id}`, 'PUT', {
        customer_id: document.getElementById(`wishlist_customer_id_${index}`).value,
        name: document.getElementById(`wishlist_name_${index}`).value
      }, this.updateCallback);
    }
    return false;
  }
  updateCallback(resp) {
    this.app.getWishlists();
    this.setState({udResult: "Wishlist updated successfully"});
  }
  delete(e, index) {
    e.preventDefault();
    // extract the wishlist_id
    const wishlist_id = document.getElementById(`wishlist_id_${index}`).value;
    if ( wishlist_id ) {
      this.app.sendRequest(`/wishlists/${wishlist_id}`, 'DELETE', {
      }, this.deleteCallback);
    }
    return false;
  }
  deleteCallback(resp) {
    this.app.getWishlists();
    this.setState({udResult: "Wishlist deleted successfully"});
  }
  read(e) {
    e.preventDefault();
    this.app.sendRequest(`/wishlists`, 'GET', {
    }, this.readCallback);
    return false;
  }
  readCallback(resp) {
    let res = '';
    if (resp.data.length) {
      res = <table className="wishlistTable"><tr><th>ID</th><th>Name</th><th>Customer ID</th></tr>
          {this.props.wishlists.map((wishlist, index) => {
              return <tr key="wishlist{wishlist.id}"><td className="cellId">{wishlist.id}</td><td className="cellName">{wishlist.name}</td><td className="cellCustomerId">{wishlist.customer_id}</td></tr>;
          })}
      </table>;
    } else {
        res = "No wishlists exist";
    }
    this.setState({readResult: res});
  }
  search(e) {
    e.preventDefault();
    this.app.sendRequest(`/wishlists`, 'GET', {
        customer_id: document.getElementById('customer_id')
    }, this.searchCallback);
    return false;
  }
  searchCallback(resp) {
    let res = '';
    if (resp.data.length) {
      res = <table className="wishlistTable"><tr><th>ID</th><th>Name</th><th>Customer ID</th></tr>
          {this.props.wishlists.map((wishlist, index) => {
              return <tr key="wishlist{wishlist.id}"><td className="cellId">{wishlist.id}</td><td className="cellName">{wishlist.name}</td><td className="cellCustomerId">{wishlist.customer_id}</td></tr>;
          })}
      </table>;
    } else {
        res = "No wishlists exist with that Customer ID";
    }
    this.setState({searchResult: res});
  }

  render() {
    const wishlistExists = this.props.wishlists && this.props.wishlists.length;
    const modifyInstructions = wishlistExists ?
          "Update or delete an existing wishlist below." :
          "Add a wishlist before running update and delete operations.";
  
    let modifyTable;
    if ( wishlistExists ) { 
      modifyTable = <div className="form-container"><table className="wishlistTable">
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Customer ID</th>
            <th>Action</th>
        </tr>
        {this.props.wishlists.map((wishlist, index) => {
          return <tr key="wishlist{wishlist.id}">
            <td className="cellId"><input type="hidden" id={'wishlist_id_'+index} value={wishlist.id} />{wishlist.id}</td>
            <td className="cellName"><input type="text" id={'wishlist_name_'+index} defaultValue={wishlist.name} /></td>
            <td className="cellCustomerId"><input type="text" id={'wishlist_customer_id_'+index} defaultValue={wishlist.customer_id} /></td>
            <td className="cellAction"><button onClick={(e) => this.update(e, index)}>Update</button> <button onClick={(e) => this.delete(e, index)}>Delete</button></td>
          </tr>;
        })}
      </table>
      <div className="udResult">{this.state.udResult}</div></div>;
    }
    return <>
        <div className="form-container">
          <h2>Wishlists</h2>
          <div className="instructions">Create a new wishlist below.</div>
          <div className="form">
            <div className="inputContainer">
              <label for="wishlist_name">Name:</label>
              <div className="item">
                <input type="text" name="wishlist_name" id="wishlist_name" value={this.state.wishlist_name} onChange={this.handleWishlistNameChange} />
              </div>
            </div>
            <div className="inputContainer">
              <label for="customer_id">Customer ID:</label>
              <div className="item">
                <input type="text" name="customer_id" id="customer_id" value={this.state.customer_id} onChange={this.handleCustomerIdChange} />
              </div>
            </div>
            <div className="submitResult">
              <div className="button"><button onClick={this.create}>Create</button></div>
              <div className="result" id="createResult">{this.state.createResult}</div>
            </div>
          </div>
        </div>
        <div className="instructions">{modifyInstructions}</div>
        {modifyTable}
        <div className="form-container">
          <div className="instructions">Click the button below to read all Wishlists.</div>
          <button onClick={this.read}>Read</button>
          <div className="readResult">{this.state.readResult}</div>
        </div>
        <div className="form-container">
          <div className="instructions">Search for wishlists by Customer ID.</div>
          <div className="form">
            <div className="inputContainer">
              <label for="wishlist_name">Customer ID:</label>
              <div className="item">
                <input type="text" name="customer_id" id="customer_id" />
              </div>
            </div>
            <div className="submitResult">
              <div className="button"><button onClick={this.search}>Search</button></div>
            </div>
          </div>
          <div className="searchResult">{this.state.searchResult}</div>
        </div>
    </>
  }
}

class ItemForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
    this.model = Item;
    this.wishlistChange = this.wishlistChange.bind(this);
  }

  wishlistChange(e) {
    this.setState({
      current_wishlist: parseInt(e.target.value)
    });
  }

  render() {
    const wishlistExists = this.props.wishlists && this.props.wishlists.length;
  
    let html;
    let wishlistSelector;
    if ( !wishlistExists ) {
      html = "Create a wishlist above before running CRUD operations on Items.";
    } else {
      wishlistSelector = <>
        <div className="form-container">
          <div className="instructions">Select a Wishlist to perform Item CRUD operations.</div>
          <div className="form">
            <label for="wishlist_id">Wishlist:</label>
            <select onChange={this.wishlistChange} name="wishlist_id"><option value="">-- select a Wishlist --</option>{this.props.wishlists.map((wishlist) => <option value={wishlist.id}>{wishlist.name}</option>)}</select>
          </div>
        </div>
      </>;

      if ( this.state.current_wishlist ) {
        html = <>
          <div className="form-container">
            <div className="instructions">{this.props.createInstructions}</div>
            <form className="form">
            {this.model && Object.entries(this.model).map((modelProps) => {
              if ( modelProps[1].type !== 'auto' ) {
                return <>
                  <label key={modelProps[0]} for={modelProps[0]}>{modelProps[1].title}</label>
                  {generateInput(modelProps)}
                </>;
              }
            })}
            </form>
          </div>
          <div className="instructions">{this.props.modifyInstructions}</div>
        </>;
      }
    }
    return <><h2>Items</h2>{wishlistSelector}{html}</>;
  }
}

export { WishlistForm, ItemForm };
