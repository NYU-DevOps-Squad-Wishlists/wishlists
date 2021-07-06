# Wishlists

## Dependencies
Before you start the app, you'll need to install the following dependencies (follow the installation instructions on their websites for info):
* Docker: https://docs.docker.com/get-docker/
* Vagrant: https://www.vagrantup.com/docs/installation

## Starting the app
After installing the base dependencies, you should be able to start the app locally:
* First, clone this repository: `git clone https://github.com/NYU-DevOps-Squad-Wishlists/wishlists.git`
* Next, run `vagrant up`.  This will build the VM and provision all the requirements.
* Go to (https://localhost:5000) to see the app landing page

If you can see the app landing page, you're ready to start using its REST endpoints.

## REST Endpoints

### `POST /wishlists`

#### Description
Creates a new wishlist.

#### Paramaters
None

#### Body
Expects the following JSON:
```
{
   "name": "wishlistName",
   "customerId": "customerId"
}
```

#### Returns
| HTTP code | Body | Description | 
| --------- | ---- | ----------- |
| `201`     |  -   | The wishlist was created successfully |
| `400`     | Error JSON object | User error (invalid JSON) |
| `500`     | Error JSON object | Server error |

### `GET /wishlists`

#### Description
Gets all wishlists.

#### Parameters
None

#### Body
None

#### Returns
| HTTP code | Body | Description | 
| --------- | ---- | ----------- |
| `200`     | Wishlists JSON object | All the existing wishlists in the database |
| `500`     | Error JSON object | Server error |

### `GET /wishlists/:WishlistId`

#### Description
Gets all the items on a specific wishlist.

#### Parameters
None

#### Body
None

#### Returns
| HTTP code | Body | Description | 
| --------- | ---- | ----------- |
| `200`     | Wishlist items | All the existing items on the wishlist |
| `400`     | Error JSON object | `:WishlistId` is missing |
| `404`     | Error JSON object | `:WishlistId` does not exist |
| `500`     | Error JSON object | Server error |

### `PUT /wishlists/:WishlistId`

#### Description
Updates a specific wishlist.

#### Parameters
None

#### Body
None

#### Returns
| HTTP code | Body | Description | 
| --------- | ---- | ----------- |
| `200`     | Wishlists JSON object | The wishlist name has been updated successfully |
| `400`     | Error JSON object | `:WishlistId` is missing |
| `404`     | Error JSON object | `:WishlistId` is does not exist |
| `500`     | Error JSON object | Server error |

### `DELETE /wishlists/:WishlistId`

#### Description
Deletes a wishlist.

#### Parameters
None

#### Body
None

#### Returns
| HTTP code | Body | Description | 
| --------- | ---- | ----------- |
| `200`     | Wishlists JSON object | The JSON object of the wishlist deleted |
| `400`     | Error JSON object | `:WishlistId` is missing |
| `404`     | Error JSON object | `:WishlistId` is does not exist |
| `500`     | Error JSON object | Server error |

### `POST /wishlists/:WishlistId/items/:ItemId`

#### Description
Adds an item to a wishlist

#### Parameters
None

#### Body
None

#### Returns
| HTTP code | Body | Description | 
| --------- | ---- | ----------- |
| `201`     | Wishlist item JSON object | The JSON object of the wishlist item added |
| `400`     | Error JSON object | `:WishlistId` or `:ItemId` is missing |
| `404`     | Error JSON object | `:WishlistId` or `:ItemId` not found |
| `500`     | Error JSON object | Server error |

### `GET /wishlists/:WishlistId/items/:ItemId`

#### Description
Retrieves an item on a wishlist

#### Parameters
None

#### Body
None

#### Returns
| HTTP code | Body | Description | 
| --------- | ---- | ----------- |
| `200`     | Wishlist item JSON object | The JSON object of the wishlist item requests |
| `400`     | Error JSON object | `:WishlistId` or `:ItemId` is missing |
| `404`     | Error JSON object | `:WishlistId` or `:ItemId` not found |
| `500`     | Error JSON object | Server error |

### `PUT /wishlists/:WishlistId/items/:ItemId`

#### Description
Updates information about an existing item on a wishlist

#### Parameters
None

#### Body
JSON key-value store of new information for the item.  Example:
```
{
   ...
}
```

#### Returns
| HTTP code | Body | Description | 
| --------- | ---- | ----------- |
| `200`     | Wishlist item JSON object | The JSON object of the wishlist item with updated data |
| `400`     | Error JSON object | `:WishlistId` or `:ItemId` is missing |
| `404`     | Error JSON object | `:WishlistId` or `:ItemId` not found |
| `500`     | Error JSON object | Server error |

### `DELETE /wishlists/:WishlistId/items/:ItemId`

#### Description
Deletes an item from a wishlist.

#### Parameters
None

#### Body
None

#### Returns
| HTTP code | Body | Description | 
| --------- | ---- | ----------- |
| `200`     | Wishlist item JSON object | The JSON object of the wishlist item deleted |
| `400`     | Error JSON object | `:WishlistId` or `:ItemId` is missing |
| `404`     | Error JSON object | `:WishlistId` or `:ItemId` not found |
| `500`     | Error JSON object | Server error |
