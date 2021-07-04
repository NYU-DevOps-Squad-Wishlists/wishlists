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

#### Returns
| HTTP code | Body | Description | 
| --------- | ---- | ----------- |
| `200`     | Wishlists JSON object | All the existing wishlists in the database |
| `500`     | Error JSON object | Server error |

### `PUT /wishlists/:WishlistId`

#### Description
