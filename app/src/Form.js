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
    this.handleWishlistNameChange = this.handleWishlistNameChange.bind(this);
    this.handleCustomerIdChange = this.handleCustomerIdChange.bind(this);
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
      this.setState({createResult: 'There was an error creating your wishlist'});
    }
  }
  render() {
    const wishlistExists = this.props.wishlists && this.props.wishlists.length;
    const modifyInstructions = wishlistExists ?
          "Update or delete an existing wishlist below." :
          "Add a wishlist before running update and delete operations.";
  
    let modifyTable;
    if ( wishlistExists ) { 
      modifyTable = "table";
    }
    return <>
        <div className="form-container">
          <h2>Wishlists</h2>
          <div className="instructions">Create a new wishlist below.</div>
          <div className="form">
            <div className="inputContainer">
              <label for="wishlist_name">Name:</label>
              <input type="text" name="wishlist_name" id="wishlist_name" value={this.state.wishlist_name} onChange={this.handleWishlistNameChange} />
            </div>
            <div className="inputContainer">
              <label for="customer_id">Customer ID:</label>
              <input type="text" name="customer_id" id="customer_id" value={this.state.customer_id} onChange={this.handleCustomerIdChange} />
            </div>
            <div className="button"><button onClick={this.create}>Create</button></div>
            <div className="result" id="createResult">{this.state.createResult}</div>
          </div>
        </div>
        <div className="instructions">{modifyInstructions}</div>
        {modifyTable}
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
    console.log(e.target.value);
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
