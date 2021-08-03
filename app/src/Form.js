import React from 'react'; 
import { Wishlist, Item } from './Model';

class WishlistForm extends React.Component {
  constructor(props) {
    super(props);
    this.app = props.app;
    this.state = {};
    this.model = Wishlist;

    this.clearResult = this.clearResult.bind(this);
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
    this.clearResult();
  }
  clearResult(e) {
    this.setState({
        wishlistResult: '',
        wishlistResultClassName: '',
        wishlistResultStatus: 'Awaiting next action',
        wishlistResponseCode: ''
    });
  }
  handleWishlistNameChange(e) {
    this.setState({wishlist_name: e.target.value});
  }
  handleCustomerIdChange(e) {
    this.setState({customer_id: e.target.value});
  }
  create(e) {
    e.preventDefault();
    this.setState({wishlistResultStatus: 'Sending request'});
    this.app.sendRequest(`/wishlists`, 'POST', {
      name: this.state.wishlist_name,
      customer_id: parseInt(this.state.customer_id)
    }, this.createCallback);
    return false;
  }
  createCallback(resp) {
    let message, className;
    if ( resp.status === 201 ) {
        message = 'Wishlist created successfully!';
        className = 'success';
        this.app.getWishlists();
    } else {
        message = resp.data.message;
        className = 'error';
    }
    this.setState({
        wishlistResult: message,
        wishlistResultClassName: className,
        wishlistResultStatus: 'Transaction complete',
        wishlistResponseCode: resp.status
    });
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
    this.setState({
        wishlistResult: "Wishlist updated successfully",
        wishlistResultClassName: 'success',
        wishlistResultStatus: 'Transaction complete',
        wishlistResponseCode: resp.status
    });
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
    this.setState({
        wishlistResult: "Wishlist deleted successfully",
        wishlistResultClassName: 'success',
        wishlistResultStatus: 'Transaction complete',
        wishlistResponseCode: resp.status
    });
  }
  read(e) {
      e.preventDefault();
      console.log('sending read request');
      this.app.sendRequest(`/wishlists`, 'GET', {
      }, this.readCallback);
      return false;
  }
  readCallback(resp) {
    let res = '';
    let table = '';
    if (resp.data && resp.data.length) {
        table = <table className="wishlistTable"><tr><th>ID</th><th>Name</th><th>Customer ID</th></tr>
            {resp.data.sort((a, b) => a.id - b.id).map((wishlist, index) => {
                return <tr className="dataRow" key={'wishlist ' + wishlist.id}><td className="cellId">{wishlist.id}</td><td className="cellName">{wishlist.name}</td><td className="cellCustomerId">{wishlist.customer_id}</td></tr>;
            })}
            </table>;
        res = "Wishlists printed below";
    } else {
        res = "No wishlists exist";
    }
    this.setState({
        readTable: table,
        wishlistResult: res,
        wishlistResultClassName: 'success',
        wishlistResultStatus: 'Transaction complete',
        wishlistResponseCode: resp.status
    });
  }
  search(e) {
    e.preventDefault();
    this.app.sendRequest(`/wishlists?customer_id=${document.getElementById('search_customer_id').value}`, 'GET', {
    }, this.searchCallback);
    return false;
  }
  searchCallback(resp) {
    let res = '';
    let table = '';
    if (resp.data && resp.data.length) {
        table = <table className="wishlistTable"><tr><th>ID</th><th>Name</th><th>Customer ID</th></tr>
            {resp.data.sort((a, b) => a.id - b.id).map((wishlist, index) => {
                return <tr className="dataRow" key="wishlist{wishlist.id}"><td className="cellId">{wishlist.id}</td><td className="cellName">{wishlist.name}</td><td className="cellCustomerId">{wishlist.customer_id}</td></tr>;
            })}
        </table>;
        res = 'Search results below';
    } else {
        res = "No wishlists exist with that Customer ID";
    }
    this.setState({
        searchTable: table,
        wishlistResult: res,
        wishlistResultClassName: 'success',
        wishlistResultStatus: 'Transaction complete',
        wishlistResponseCode: resp.status
    });
  }

  render() {
    const wishlistExists = this.props.wishlists && this.props.wishlists.length;
    const modifyInstructions = wishlistExists ?
          "Update or delete an existing wishlist below." :
          "Add a wishlist to run update and delete operations.";
  
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
          return <tr className="dataRow" key={'wishlist_' + wishlist.id}>
            <td className="cellId"><input type="hidden" id={'wishlist_id_'+index} value={wishlist.id} />{wishlist.id}</td>
            <td className="cellName"><input type="text" id={'wishlist_name_'+index} defaultValue={wishlist.name} /></td>
            <td className="cellCustomerId"><input type="text" id={'wishlist_customer_id_'+index} defaultValue={wishlist.customer_id} /></td>
            <td className="cellAction"><button id={'wishlist_update_'+index} onClick={(e) => this.update(e, index)}>Update Wishlist</button> <button id={'wishlist_delete_'+index} onClick={(e) => this.delete(e, index)}>Delete Wishlist</button></td>
          </tr>;
        })}
      </table></div>
    }
    return <>
        <div className="form-container">
          <h2>Wishlists</h2>
          <div className="resultInstructions">The box below will display the result of the transaction (success or errors).</div>
          <div className="resultBox">
            <div className="resultStatus" id="wishlist_result_status">Status: {this.state.wishlistResultStatus}</div>
            <div className="responseCode" id="wishlist_response_code">Response code: {this.state.wishlistResponseCode}</div>
            <div className={"result " + this.state.wishlistResultClassName} id="wishlist_result">{this.state.wishlistResult}</div>
            <button id="wishlist_result_clear" onClick={this.clearResult}>Clear Result</button>
          </div>
          <div className="instructions">Create a new wishlist below.</div>
          <div className="form">
            <div className="inputContainer">
              <label for="wishlist_name">Name:</label>
              <div className="item">
                <input type="text" name="wishlist_name" id="wishlist_name" onChange={this.handleWishlistNameChange} />
              </div>
            </div>
            <div className="inputContainer">
              <label for="customer_id">Customer ID:</label>
              <div className="item">
                <input type="text" name="customer_id" id="customer_id" onChange={this.handleCustomerIdChange} />
              </div>
            </div>
            <div className="submitResult">
              <div className="button"><button id="wishlist_create" onClick={this.create}>Create Wishlist</button></div>
            </div>
          </div>
        </div>
        <div className="form-container">
          <div className="instructions">Click the button below to read all Wishlists.</div>
          <button id="wishlist_read" onClick={this.read}>Read Wishlists</button>
          <div className="readTable" id="wishlist_read_table">{this.state.readTable}</div>
        </div>
        <div className="form-container">
          <div className="instructions">Search for wishlists by Customer ID.</div>
          <div className="form">
            <div className="inputContainer">
              <label for="wishlist_name">Customer ID:</label>
              <div className="item">
                <input type="text" name="search_customer_id" id="search_customer_id" />
              </div>
            </div>
            <div className="submitResult">
              <div className="button"><button id="wishlist_search" onClick={this.search}>Search Wishlists</button></div>
            </div>
          </div>
          <div className="searchTable" id="wishlist_search_table">{this.state.searchTable}</div>
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
    this.app = props.app;

    this.clearResult = this.clearResult.bind(this);
    this.wishlistChange = this.wishlistChange.bind(this);
    this.getCurrentItems = this.getCurrentItems.bind(this);
    this.create = this.create.bind(this);
    this.createCallback = this.createCallback.bind(this);
    this.read = this.read.bind(this);
    this.readCallback = this.readCallback.bind(this);
    this.update = this.update.bind(this);
    this.updateCallback = this.updateCallback.bind(this);
    this.odelete = this.delete.bind(this);
    this.deleteCallback = this.deleteCallback.bind(this);
    this.purchase = this.purchase.bind(this);
    this.purchaseCallback = this.purchaseCallback.bind(this);
  }

  componentDidMount() {
      this.clearResult();
  }
  clearResult(e) {
    this.setState({
        itemResult: '',
        itemResultClassName: '',
        itemResultStatus: 'Awaiting next action',
        itemResponseCode: ''
    });
  }
  wishlistChange(e) {
    this.setState({
      current_items: [],
      current_wishlist: this.props.wishlists.find((wishlist) => wishlist.id === parseInt(e.target.value, 10)),
    });
    this.getCurrentItems(parseInt(e.target.value), 10);
  }
  currentBasePath(wid = null) {
    const wishlist_id = wid || this.state.current_wishlist.id;
    return `/wishlists/${wishlist_id}`;
  }
  getCurrentItems(wid) {
    const wishlist_id = wid || this.state.current_wishlist.id;
    this.app.sendRequest(`${this.currentBasePath(wid)}/items`, 'GET', {
    }, (resp) => {
      if (resp.data.length) {
        const items = resp.data.sort((a, b) => a.id - b.id);
        this.setState({current_items: items});
      } else {
        this.setState({current_items: []});
      }
    });
  }

  create(e) {
    e.preventDefault();
    const item_name = document.getElementById('item_name').value.toString();
    this.app.sendRequest(`${this.currentBasePath()}/items`, 'POST', {
      wishlist_id: this.state.current_wishlist.id,
      name: item_name
    }, this.createCallback);
    return false;
  }
  createCallback(resp) {
    let message, className;
    const current_items = this.state.current_items;
    if ( resp.status === 201 ) {
        current_items.push(resp.data);
        message = 'Item added successfully!';
        className = 'success';
    } else {
        message = resp.data.message;
        className = 'error';
    }
    this.setState({
        itemResult: message,
        itemResultClassName: className,
        itemResultStatus: 'Transaction complete',
        itemResponseCode: resp.status,
        current_items
    });
  }
  read(e) {
    e.preventDefault();
    this.app.sendRequest(`${this.currentBasePath()}/items`, 'GET', {
    }, this.readCallback);
    return false;
  }
  readCallback(resp) {
    let res = '';
    let table = '';
    if (resp.data.length) {
      const items = resp.data.sort((a, b) => a.id - b.id);
      table = <table className="wishlistTable"><tr><th>ID</th><th>Name</th><th>Purchased</th></tr>
          {items.map((item, index) => {
              return <tr className="dataRow" key={'item_' + item.id}><td className="cellId">{item.id}</td><td className="cellName">{item.name}</td><td className="cellPurchased">{item.purchased.toString()}</td></tr>;
          })}
      </table>;
      res = 'Items listed below';
      // this.setState({current_items: items});
    } else {
      res = "No items on this wishlist";
    }
    this.setState({
        itemResult: res,
        itemResultClassName: 'success',
        itemResultStatus: 'Transaction complete',
        itemResponseCode: resp.status,
        readTable: table
    });
  }
  update(e, item_id) {
    e.preventDefault();
    const new_name = document.getElementById(`item_name_${item_id}`).value;
    this.app.sendRequest(`${this.currentBasePath()}/items/${item_id}`, 'PUT', {
        wishlist_id: this.state.current_wishlist.id,
        name: new_name
    }, this.updateCallback);
    return false;
  }
  updateCallback(resp) {
      let message = '', className = '';
      if ( resp.status === 200 ) {
          this.getCurrentItems();
          message = 'Item updated successfully';
          className = 'success';
      } else {
          message = resp.data.message;
          className = 'error';
      }
      this.setState({
          itemResult: message,
          itemResultClassName: className,
          itemResultStatus: 'Transaction complete',
          itemResponseCode: resp.status
      });
  }
  delete(e, item_id) {
    e.preventDefault();
    this.app.sendRequest(`${this.currentBasePath()}/items/${item_id}`, 'DELETE', {
        wishlist_id: this.state.current_wishlist.id
    }, this.deleteCallback);
    return false;
  }
  deleteCallback(resp) {
      let message = '', className = '';
      if ( resp.status === 204 ) {
          this.getCurrentItems();
          message = 'Item deleted successfully';
          className = 'success';
      } else {
          message = resp.data.message;
          className = 'error';
      }
      this.setState({
          itemResult: message,
          itemResultClassName: className,
          itemResultStatus: 'Transaction complete',
          itemResponseCode: resp.status
      });
  }
  purchase(e, item_id) {
    e.preventDefault();
    this.app.sendRequest(`${this.currentBasePath()}/items/${item_id}/purchase`, 'PUT', {
        wishlist_id: this.state.current_wishlist.id
    }, this.purchaseCallback);
    return false;
  }
  purchaseCallback(resp) {
      let message = '', className = '';
      if ( resp.status === 200 ) {
          this.getCurrentItems();
          message = 'Item purchased';
          className = 'success';
      } else {
          message = resp.data.message;
          className = 'error';
      }
      this.setState({
          itemResult: message,
          itemResultClassName: className,
          itemResultStatus: 'Transaction complete',
          itemResponseCode: resp.status
      });
  }


  render() {
    const wishlistExists = this.props.wishlists && this.props.wishlists.length;
    let html;
    let modifyTable;
    let modifyInstructions;
    let wishlistSelector;
    if ( !wishlistExists ) {
      html = "Create a wishlist before running CRUD operations on Items.";
    } else {
      wishlistSelector = <>
        <div className="form-container">
          <div className="instructions">Select a Wishlist to perform Item CRUD operations.</div>
          <div className="form">
            <div className="inputContainer">
              <label for="wishlist_id">Wishlist:</label>
              <div className="input">
                <select onChange={this.wishlistChange} name="wishlist_id" id="wishlist_selector"><option value="">-- select a Wishlist --</option>{this.props.wishlists.map((wishlist) => <option value={wishlist.id}>{wishlist.name}</option>)}</select>
              </div>
            </div>
          </div>
        </div>
      </>;

      if ( this.state.current_wishlist ) {
        html = <><div className="form-container">
          <div className="instructions">Add an item to the <strong>{this.state.current_wishlist.name}</strong> wishlist below.</div>
          <div className="form">
            <div className="inputContainer">
              <label for="item_name">Item Name:</label>
              <div className="item">
                <input type="text" name="item_name" id="item_name" onChange={this.handleItemNameChange} />
              </div>
            </div>
            <div className="submitResult">
              <div className="button"><button id="item_create" onClick={this.create}>Add Item</button></div>
            </div>
          </div>
        </div>
        <div className="form-container">
          <div className="instructions">Read items on the <strong>{this.state.current_wishlist.name}</strong> wishlist below.</div>
          <button id="item_read" onClick={this.read}>Read Items</button>
          <div className="readTable" id="item_read_table">{this.state.readTable}</div>
        </div>
        </>;

        if ( this.state.current_items && this.state.current_items.length ) {
          modifyInstructions = 'Update, delete or purchase an item on this wishlist below.';
          modifyTable = <>
          <div className="form-container"><table className="wishlistTable">
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Purchased</th>
              <th>Action</th>
            </tr>
            {this.state.current_items.map((item, index) => {
              return <tr className="dataRow" key={'item ' + item.id}>
                <td className="cellId"><input type="hidden" id={'item_id_'+item.id} value={item.id} />{item.id}</td>
                <td className="cellName"><input type="text" id={'item_name_'+item.id} defaultValue={item.name} /></td>
                <td className="cellPurchased">{item.purchased.toString()}</td>
                <td className="cellAction"><button id={'item_update_'+item.id} onClick={(e) => this.update(e, item.id)}>Update Item</button> <button id={'item_delete_'+item.id} onClick={(e) => this.delete(e, item.id)}>Delete Item</button> <button id={'item_purchase_'+item.id} onClick={(e) => this.purchase(e, item.id)}>Purchase Item</button></td>
              </tr>;
            })}
          </table></div></>;
        } else {
            modifyInstructions = "Add an item to this wishlist before running update, delete or purchase operations on items.";
        }
      }
    }
    return <>
          <h2>Items</h2>
          <div className="resultInstructions">The box below will display the result of the transaction (success or errors).</div>
          <div className="resultBox">
            <div className="resultStatus" id="item_result_status">Status: {this.state.itemResultStatus}</div>
            <div className="responseCode" id="item_response_code">Response code: {this.state.itemResponseCode}</div>
            <div className={"result " + this.state.itemResultClassName} id="item_result">{this.state.itemResult}</div>
            <button id="item_result_clear" onClick={this.clearResult}>Clear Result</button>
          </div>
          {wishlistSelector}
          {html}
          <div className="instructions">{modifyInstructions}</div>
          {modifyTable}
          <div className={'udpResult ' + this.state.udpClassName} id="udpResult_item">{this.state.udpResult}</div>
    </>;
  }
}

export { WishlistForm, ItemForm };
