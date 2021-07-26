const Wishlist = {
  wishlist_id: {
    type: 'auto',
    title: 'Wishlist ID'
  },
  name: {
    type: 'string',
    title: 'Name'
  },
  customer_id: {
    type: 'int',
    title: 'Customer ID'
  }
};

const Item = {
  wishlist_id: {
    type: 'select',
    title: 'Wishlist ID',
    options: []
  },
  item_id: {
    type: 'auto',
    title: 'Item ID',
  },
  name: {
    type: 'string',
    title: 'Name',
  }
};
  
export { Wishlist, Item };
