import requests
from .customresponse import CustomResponse
from datetime import datetime, timezone
from .commonfunctions import rfplogger
import time

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

######################### GRAPHQL FUNCTIONS

def Shopify_get_metaobject_gid(shop="", access_token="", api_version="2024-01", metaobject_type="", handle=""):

    # print(f"Access token: {access_token}")

    url = f"https://{shop}.myshopify.com/admin/api/{api_version}/graphql.json"
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': access_token
    }

    # print(f"headers: {headers}")

    query = """
    query GetMetaobjectByHandle($type: String!, $handle: String!) {
      metaobjectByHandle(handle: {
            type: $type,
            handle: $handle
        }) {
            id
            type
            handle
        }
    }
    """
    
    variables = {
        "type": metaobject_type,
        "handle": handle
    }
    
    payload = {
        'query': query,
        'variables': variables
    }

    # print(f"payload: {payload}")
    
    response = requests.post(url, json=payload, headers=headers)
    # response = requests.post(url, json={'query': query}, headers=headers)
    
    if response.status_code == 200:
        response_json = response.json()
        result_id = response_json['data']['metaobjectByHandle']['id']
        return result_id
    else:
        print(f"Error: {response.status_code}")
        return None

def Shopify_update_metaobject(shop="", access_token="", api_version="2024-01", metaobject_gid="", banner_url="", mobile_banner_url="", product_url="", metaobject_banner_number=1):
    # Push to shopify banner object for vinzo
    url = f"https://{shop}.myshopify.com/admin/api/{api_version}/graphql.json"
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': access_token
    }

    # Generate field names based on metaobject_banner_number
    field_names = [f"product_link_{metaobject_banner_number}",
                   f"banner_url_{metaobject_banner_number}",
                   f"mobile_banner_url_{metaobject_banner_number}"
    ]

    print(field_names)

    mutation = """
    mutation UpdateMetaobject($id: ID!, $metaobject: MetaobjectUpdateInput!) {
    metaobjectUpdate(id: $id, metaobject: $metaobject) {
        metaobject {
        handle
        """
    
    # Add dynamic field names to the mutation
    for field_name in field_names:
        mutation += f"{field_name}: field(key: \"{field_name}\") {{ value }}\n"

    mutation += """
        }
        userErrors {
        field
        message
        code
        }
    }
    }
    """

    variables = { 
        "id": metaobject_gid,
        "metaobject": {
            "fields": [
                {"key": field_name, "value": value}
                for field_name, value in zip(field_names, [product_url, banner_url, mobile_banner_url])
            ]
        } 
    }

    response = requests.post(url, json={'query': mutation, 'variables': variables}, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error loading to shopify: {response.status_code}")
        return (f"Error loading to shopify: {response.status_code}")

def Shopify_get_products(shop="", access_token="", api_version="2024-01"):

    '''Uses Admin API'''

    url = f"https://{shop}.myshopify.com/admin/api/{api_version}/products.json"
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': access_token
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve products: {response.status_code}")
        return None
    
def Shopify_get_collections(shop="", access_token="", api_version="2024-01"):

    url_custom = f"https://{shop}.myshopify.com/admin/api/{api_version}/custom_collections.json"
    url_smart = f"https://{shop}.myshopify.com/admin/api/{api_version}/smart_collections.json"
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': access_token
    }

    response = requests.get(url_smart, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve smart collections: {response.status_code}")
        print(f"response {response.text}")
        return CustomResponse(data=response.text, status_code=response.status_code)
    smart_collections = response.json()['smart_collections']
    
    response = requests.get(url_custom, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve custom collections: {response.status_code}")
        print(f"response {response.text}")
        return CustomResponse(data=response.text, status_code=response.status_code)
    custom_collections = response.json()['custom_collections']
    
    all_collections = smart_collections + custom_collections

    return CustomResponse(data=all_collections, status_code=200)

def Shopify_get_collection_metadata(shop="", access_token="", api_version="2024-01", collection_id=""):
    '''Returns metafields and metadata'''
    metadata_url = f"https://{shop}.myshopify.com/admin/api/{api_version}/collections/{collection_id}.json"
    
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': access_token
    }

    response = requests.get(metadata_url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to retrieve metadata for collection ID {collection_id}. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return CustomResponse(data=response.text, status_code=400)
    
    collection_metadata = response.json()['collection']
    
    # Retrieve metafields for the collection
    metafields_url = f"https://{shop}.myshopify.com/admin/api/{api_version}/collections/{collection_id}/metafields.json"
    response = requests.get(metafields_url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to retrieve metafields for collection ID {collection_id}. Status code: {response.status_code}")
        print(f"Metafields response: {response.text}")
        return CustomResponse(data=response.text, status_code=400)
    metafields_data = response.json()['metafields']

    # Join metadata and metafield 
    collection_metadata['metafields'] = metafields_data

    # print(f"collection_metadata: {collection_metadata}")

    return CustomResponse(data=collection_metadata, status_code=200)

def Shopify_get_collection_url(shop="", access_token="", api_version="2024-01", collection_id=""):    
    collection_url = f"https://{shop}.myshopify.com/admin/api/{api_version}/collections/{collection_id}"
    response = requests.get(collection_url)    
    if response.status_code == 200:
        return CustomResponse(data=collection_url, status_code=200)
    else:
        # Handle the case where the URL does not exist
        return CustomResponse(data="Collection URL does not exist", status_code=404)

def Shopify_get_products_in_collection(shop="", access_token="", api_version="2024-01", collection_id=""):

    url = f"https://{shop}.myshopify.com/admin/api/{api_version}/collections/{collection_id}/products.json"
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': access_token
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        products=response.json()['products']
        return CustomResponse(data=products, status_code=200)

    else:
        print(f"Failed to retrieve products in collection {collection_id}: {response.status_code}")
        return CustomResponse(data=response.text, status_code=400)
    
def Shopify_get_product_variants(shop="", access_token="", api_version="2024-01", product_id=""):
    url = f"https://{shop}.myshopify.com/admin/api/{api_version}/products/{product_id}/variants.json"
    
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': access_token
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        variants=response.json()['variants']
        return CustomResponse(data=variants, status_code=200)
    else:
        print(f"Failed to retrieve product variants for product {product_id}: {response.status_code}")
        return CustomResponse(data=response.text, status_code=400)

def Shopify_get_customers(shop="", access_token="", api_version="2024-01"):
    # Endpoint URL for fetching customers
    url = f"https://{shop}.myshopify.com/admin/api/{api_version}/customers.json"
    
    # Headers for the request, including the required access token for authentication
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': access_token
    }

    # Making the GET request to the API
    response = requests.get(url, headers=headers)
    
    # Check the response status code
    if response.status_code != 200:
        # If the request was not successful, print an error message and return a custom response
        print(f"Failed to retrieve customers: {response.status_code}")
        print(f"response: {response.text}")
        return CustomResponse(data=response.text, status_code=response.status_code)
    
    # If the request was successful, parse the JSON response to get the customers
    customers = response.json()['customers']
    
    # Return a custom response containing the customers and a successful status code
    return CustomResponse(data=customers, status_code=200)

def Shopify_get_products_with_metafields(shop="", access_token="", api_version="2024-01", metafield_key="custom.unpublish_after", filterdate="23/02/2024"):
    url = f"https://{shop}.myshopify.com/admin/api/{api_version}/graphql.json"
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': access_token
    }

    # Initialize variables for pagination
    cursor = None
    filtered_products = []
    
    i = 0
    while True:
        print(f"Getting products... {i}", end='\r', flush=True)
        i += 1
        # Construct GraphQL query with pagination
        query = '''
        query ($cursor: String) {
            products(first: 250, after: $cursor) {
                edges {
                    node {
                        id
                        title
                        metafield(key: "%s") {
                            value
                        }
                    }
                    cursor
                }
                pageInfo {
                    hasNextPage
                    endCursor
                }
            }
        }
        ''' % (metafield_key)

        # Send request to Shopify GraphQL API
        response = requests.post(url, json={'query': query, 'variables': {'cursor': cursor}}, headers=headers)
        
        if response.status_code != 200:
            error_message = f"Failed to retrieve products with metafields: {response.status_code}"
            print(error_message)
            return CustomResponse(data=error_message, status_code=400)
        
        products = response.json()['data']['products']['edges']
        page_info = response.json()['data']['products']['pageInfo']
        cursor = page_info['endCursor'] if page_info['hasNextPage'] else None
              
        for product in products:
            # Attempt to retrieve the 'metafield' if it exists, otherwise use an empty dictionary
            metafield = product['node'].get('metafield') or {}
            metafield_value = metafield.get('value', '')
            
            if metafield_value:
                try:
                    # Convert the metafield value string to a datetime object
                    metafield_date = datetime.strptime(metafield_value, '%Y-%m-%dT%H:%M:%S%z')
                    # Convert the filter string to a datetime object
                    filter_date = datetime.strptime(filterdate, '%d/%m/%Y').replace(tzinfo=timezone.utc)
                    
                    if metafield_date < filter_date:
                        filtered_products.append({
                            'id': product['node']['id'],
                            'title': product['node']['title'],
                            'unpublish_metafield': metafield_value
                        })
            
                except ValueError as e:
                    print(f"Error parsing date for product {product['node']['id']}: {e}")

        if not page_info['hasNextPage']:
            break

    return CustomResponse(data=filtered_products, status_code=200)

def Shopify_get_products_and_inventoryid_with_metafields(shop="", access_token="", api_version="2024-01", metafield_key="custom.unpublish_after", filterdate="23/02/2024"):
    url = f"https://{shop}.myshopify.com/admin/api/{api_version}/graphql.json"
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': access_token
    }

    # Initialize variables for pagination
    cursor = None
    filtered_products = []
    
    i = 0
    while True:
        print(f"Getting products and inventory id... {i}", end='\r', flush=True)
        i += 1
        # Construct GraphQL query with pagination and include variant inventory_item_id
        query = '''
        query ($cursor: String) {
            products(first: 250, after: $cursor) {
                edges {
                    node {
                        id
                        title
                        metafield(key: "%s") {
                            value
                        }
                        variants(first: 250) {
                            edges {
                                node {
                                    id
                                    inventoryItem {
                                        id
                                    }
                                }
                            }
                        }
                    }
                    cursor
                }
                pageInfo {
                    hasNextPage
                    endCursor
                }
            }
        }
        ''' % (metafield_key)

        # Send request to Shopify GraphQL API
        response = requests.post(url, json={'query': query, 'variables': {'cursor': cursor}}, headers=headers)
        
        if response.status_code != 200:
            error_message = f"Failed to retrieve products with metafields: {response.status_code}"
            print(error_message)
            return CustomResponse(data=error_message, status_code=400)
        
        #rfplogger(i)
        #rfplogger(response.json())
        
        products = response.json()['data']['products']['edges']
        page_info = response.json()['data']['products']['pageInfo']
        cursor = page_info['endCursor'] if page_info['hasNextPage'] else None

        for product in products:
            # Attempt to retrieve the 'metafield' if it exists, otherwise use an empty dictionary
            metafield = product['node'].get('metafield') or {}
            metafield_value = metafield.get('value', '')
            
            variant_inventory_ids = [variant['node']['inventoryItem']['id'] for variant in product['node']['variants']['edges']]
            
            if metafield_value:
                try:
                    # Convert the metafield value string to a datetime object
                    metafield_date = datetime.strptime(metafield_value, '%Y-%m-%dT%H:%M:%S%z')
                    # Convert the filter string to a datetime object
                    filter_date = datetime.strptime(filterdate, '%d/%m/%Y').replace(tzinfo=timezone.utc)
                    
                    if metafield_date < filter_date:
                        filtered_products.append({
                            'id': product['node']['id'],
                            'title': product['node']['title'],
                            'unpublish_metafield': metafield_value,
                            'variant_inventory_item_ids': variant_inventory_ids
                        })
            
                except ValueError as e:
                    print(f"Error parsing date for product {product['node']['id']}: {e}")

        if not page_info['hasNextPage']:
            break
        
        #print("Wait 3 seconds...")
        time.sleep(3) # Query takes 288 tokens, wait 3 seconds so never deplete

    return CustomResponse(data=filtered_products, status_code=200)

def Shopify_unpublish_products_channel(shop="", access_token="", api_version="2024-01", products=[], channel_id=""):
    
    '''
    Upublishes products for a channel id by removing from channel id
    '''

    url = f"https://{shop}.myshopify.com/admin/api/{api_version}/graphql.json"
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': access_token
    }

    # Prepare the GraphQL mutation for unpublishing products
    mutation = '''
    mutation publishableUnpublish($id: ID!, $input: [PublicationInput!]!) {
      publishableUnpublish(id: $id, input: $input) {
        userErrors {
          field
          message
        }
      }
    }
    '''
    allpublished = True
    for product in products:
        variables = {
            # "id": f"gid://shopify/Product/{product['id']}",
            "id": product['admin_graphql_api_id'],
            "input": [{
                "publicationId": channel_id
            }]
        }
        response = requests.post(url, json={'query': mutation, 'variables': variables}, headers=headers)
        if response.status_code == 200:
            errors = response.json().get('errors', [])  
            if errors:
                allpublished=False
                continue

            # data = response.json().get('data', {})
            # print(f"Product {product['id']} unpublished successfully.")
        else:
            allpublished=False
            print(f"Failed to unpublish product {product['id']}: {response.status_code}")

    message = "All products were unpublished correctly"
    if allpublished != True:
        message = "Not all products were unpublished correctly"

    return CustomResponse(data=message, status_code=200)

def Shopify_get_online_store_channel_id(shop="", access_token="", api_version="2024-01"):
    url = f"https://{shop}.myshopify.com/admin/api/{api_version}/graphql.json"

    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': access_token,
    }
    query = '''
    {
      publications(first: 250) {
        edges {
          node {
            id
            name
          }
        }
      }
    }
    '''
    response = requests.post(url, json={'query': query}, headers=headers)
    if response.status_code == 200:
        data = response.json()
        publications = data['data']['publications']['edges']
        for publication in publications:
            if publication['node']['name'] == 'Online Store':
                return publication['node']['id']
    return None

def BORRAR_Shopify_bulk_set_inventory_to_zero(shop="", access_token="", api_version="2024-01", inventory_item_ids="", location_id=""):
    url = f"https://{shop}.myshopify.com/admin/api/{api_version}/graphql.json"
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': access_token
    }

    # GraphQL mutation to set inventory quantities to zero
    mutation = '''
    mutation inventoryBulkAdjustQuantityAtLocation($inventoryItemAdjustments: [InventoryAdjustItemInput!]!, $locationId: ID!) {
      inventoryBulkAdjustQuantityAtLocation(inventoryItemAdjustments: $inventoryItemAdjustments, locationId: $locationId) {
        inventoryLevels {
          id
          available
        }
        userErrors {
          field
          message
        }
      }
    }
    '''

    # Preparing the adjustments input for the GraphQL mutation
    adjustments = [{"inventoryItemId": item_id, "availableDelta": -9999} for item_id in inventory_item_ids]

    variables = {
        "inventoryItemAdjustments": adjustments,
        "locationId": location_id
    }

    response = requests.post(url, json={'query': mutation, 'variables': variables}, headers=headers)
    if response.status_code == 200:
        print("Inventory set to zero successfully.")
    else:
        print(f"Failed to set inventory to zero: {response.status_code}")

def Shopify_reduce_inventory_by_9999(shop="", access_token="", api_version="2024-01", inventory_item_ids="", location_id=""):
    # inventory_item_ids = ["inventory-item-id-1", "inventory-item-id-2"]  # List of inventory item IDs

    url = f"https://{shop}.myshopify.com/admin/api/{api_version}/graphql.json"
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': access_token
    }

    # GraphQL mutation to set inventory quantities to zero
    mutation = '''
    mutation inventoryBulkAdjustQuantityAtLocation($inventoryItemAdjustments: [InventoryAdjustItemInput!]!, $locationId: ID!) {
      inventoryBulkAdjustQuantityAtLocation(inventoryItemAdjustments: $inventoryItemAdjustments, locationId: $locationId) {
        inventoryLevels {
          id
          available
        }
        userErrors {
          field
          message
        }
      }
    }
    '''
    # Preparing the adjustments input for the GraphQL mutation
    adjustments = [{"inventoryItemId": item_id, "availableDelta": -9999} for item_id in inventory_item_ids]
    print(adjustments)
    variables = {
        "inventoryItemAdjustments": adjustments,
        "locationId": location_id
        
    }

    response = requests.post(url, json={'query': mutation, 'variables': variables}, headers=headers)
    rfplogger(response.json())
    if response.status_code == 200:
        message="Inventory set to zero successfully."
        print(message)
        return CustomResponse(data=message, status_code=200)
        
    else:
        message=f"Failed to set inventory to zero: {response.status_code}"
        print(message)
        return CustomResponse(data=message, status_code=400)

def Shopify_set_inventory_to_zero(shop="", access_token="", api_version="2024-01", inventory_item_ids="", location_id="", reason="correction", reference_document_uri=""):
    
    # Loop through each chunk and make the API call
    for chunk in chunker(inventory_item_ids, 250):

        url = f"https://{shop}.myshopify.com/admin/api/{api_version}/graphql.json"
        headers = {
            'Content-Type': 'application/json',
            'X-Shopify-Access-Token': access_token
        }

        # GraphQL mutation to set inventory quantities to zero
        mutation = '''
        mutation inventorySetOnHandQuantities($input: InventorySetOnHandQuantitiesInput!) {
        inventorySetOnHandQuantities(input: $input) {
            inventoryAdjustmentGroup {
            id
            }
            userErrors {
            field
            message
            }
        }
        }
        '''
        # Build the setQuantities input dynamically
        #set_quantities = [{"inventoryItemId": item_id, "locationId": location_id, "quantity": 0} for item_id in inventory_item_ids]
        set_quantities = [{"inventoryItemId": item_id, "locationId": location_id, "quantity": 0} for item_id in chunk]

        variables = {
            "input": {
                "reason": reason,
                #"referenceDocumentUri": reference_document_uri,
                "setQuantities": set_quantities
            }
        }

        response = requests.post(url, json={'query': mutation, 'variables': variables}, headers=headers)
        
        if response.status_code != 200:
            message = f"Failed to set inventory to zero for chunk: {response.status_code}"
            print(message)
            return CustomResponse(data=message, status_code=400)

        print("Waiting...")
        rfplogger(response.json())
        time.sleep(2)

    message="Inventory set to zero successfully for all items."
    print(message)
    rfplogger(response.json())
    return CustomResponse(data=message, status_code=200)
    
def Shopify_get_locations(shop="", access_token="", api_version="2024-01"):
    url = f"https://{shop}.myshopify.com/admin/api/{api_version}/locations.json"
    headers = {"X-Shopify-Access-Token": access_token}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return CustomResponse(data=response.json()['locations'], status_code=200)  # Returns a list of locations
    else:
        print(f"Failed to retrieve locations: {response.status_code}")
        return CustomResponse(data="", status_code=400)
    
###################### SPECIFIC FUNCTIONS
    
def Shopify_get_marketing_customer_list(shop="", access_token="", api_version="2024-01"):
    ''' Returns a dictionary with 2 lists, customer who are subscribe to email marketing and cutomers subscribed to SMS marketing'''
    # Assume Shopify_get_customers is defined elsewhere and correctly returns customer data
    response = Shopify_get_customers(shop, access_token, api_version)
    
    # Initialize dictionaries to hold subscribers
    marketing_lists = {
        'newsletter_subscribers': [],
        'sms_marketing_subscribers': []
    }
    
    # Proceed only if the response was successful
    if response.status_code != 200:
        print("Failed to retrieve customers. Status Code:", response.status_code)
        return response

    # Iterate through the customer data
    for customer in response.data:
        email_marketing_consent = customer.get('email_marketing_consent')
        if email_marketing_consent and email_marketing_consent.get('state') == 'subscribed':
            marketing_lists['newsletter_subscribers'].append({
                'first_name': customer.get('first_name', ''),
                'last_name': customer.get('last_name', ''),
                'email': customer.get('email', '')
            })
        
        sms_marketing_consent = customer.get('sms_marketing_consent')
        # Adjusted to check if sms_marketing_consent is not None and then proceed
        if sms_marketing_consent and sms_marketing_consent.get('state') == 'subscribed':
            marketing_lists['sms_marketing_subscribers'].append({
                'first_name': customer.get('first_name', ''),
                'last_name': customer.get('last_name', ''),
                'email': customer.get('email', '')  # Assuming you want the email for SMS subscribers
            })
    
    return CustomResponse(data=marketing_lists, status_code=200)
    
def Shopify_set_stock_zero_metafield_unpublish(shop="", access_token="", api_version="2024-01", metafield_key="custom.unpublish_after", filter_date="", reason="correction", reference_document_uri=""):
    '''
    Set stock to zero for all products with custom.unpublish_after 
    less than the in the filter_date
    '''
    # GET PRODUCTS AND RELATED INVENTORY ID WITH METAFIELD VALUE. 
    # Has to get all products in store in batches of 250, takes 3 seconds per batch
    custom_response = Shopify_get_products_and_inventoryid_with_metafields(shop=shop, access_token=access_token, api_version="2024-01", metafield_key=metafield_key, filterdate=filter_date)
    if custom_response.status_code != 200:
        error_message = "Error getting product with metafield value"
        print(error_message)
        return CustomResponse(data=error_message, status_code=400)

    filtered_products = custom_response.data
    
    # GET INVENTORY ITEMS FOR ALL VARIANTS
    inventory_item_ids = [item_id for product in filtered_products for item_id in product['variant_inventory_item_ids']]
    # GET INVENTORY LOCATION
    custom_response = Shopify_get_locations(shop=shop, access_token=access_token, api_version="2024-01")
    if custom_response.status_code!=200:
        error_message = "Error getting locations"
        print(error_message)
        return CustomResponse(data=error_message, status_code=400)
    locations = custom_response.data
    if locations:
        # Take the first location from the list
        first_location = locations[0]  # Access the first item in the list
        location_id = first_location['id']
        location_id = f"gid://shopify/Location/{location_id}"
    else:
        error_message = "Error No locations found."
        print(error_message)
        return CustomResponse(data=error_message, status_code=400)
    
    # SET STOCK TO ZERO. VERY FAST, JUST 1 MUTATION WITH ALL INVENTORY ITEMS
    reference_document_uri = ""
    custom_response=Shopify_set_inventory_to_zero(shop=shop, access_token=access_token, api_version="2024-01", inventory_item_ids=inventory_item_ids, location_id=location_id, reason=reason, reference_document_uri=reference_document_uri)
    if custom_response.status_code != 200:
        error_message = "Error setting inventory to zero"
        print(error_message)
        return CustomResponse(data=error_message, status_code=400)
    
    return CustomResponse(data="All OK", status_code=200)

    # GET PRODUCTS WITH METAFIELD VALUE. Has to get all products in store in batches of 250
    #custom_response = Shopify_get_products_with_metafields(shop=shop, access_token=access_token, api_version="2024-01", metafield_key=metafield_key, filterdate=filter_date)
    #if custom_response.status_code != 200:
    #    error_message = "Error getting product with metafield value"
    #    print(error_message)
    #    return CustomResponse(data=error_message, status_code=400)

    # Extracting just the numerical ID part from each product's 'id' field
    product_ids = [product['id'].split('/')[-1] for product in filtered_products]

    # GET INVENTORY ITEMS FOR EACH PRODUCT id. Loops for each product, takes a long time!
    inventory_item_ids = []
    for product_id in product_ids:
        custom_response = Shopify_get_product_variants(shop=shop, access_token=access_token, api_version="2024-01", product_id=product_id)
        
        # Check if variants were retrieved successfully
        if custom_response.status_code !=200:
                error_message = "Error getting variants"
                print(error_message)
                return CustomResponse(data=error_message, status_code=400)
        
        variants=custom_response.data

        for variant in variants:
            inventory_gid = f"gid://shopify/InventoryItem/{variant['inventory_item_id']}"
            inventory_item_ids.append(inventory_gid)
 
    # GET INVENTORY LOCATION
    custom_response = Shopify_get_locations(shop=shop, access_token=access_token, api_version="2024-01")
    if custom_response.status_code!=200:
        error_message = "Error getting locations"
        print(error_message)
        return CustomResponse(data=error_message, status_code=400)
    locations = custom_response.data
    if locations:
        # Take the first location from the list
        first_location = locations[0]  # Access the first item in the list
        location_id = first_location['id']
        location_id = f"gid://shopify/Location/{location_id}"
    else:
        error_message = "Error No locations found."
        print(error_message)
        return CustomResponse(data=error_message, status_code=400)
    
    # SET STOCK TO ZERO. VERY FAST, JUST 1 MUTATION WITH ALL INVENTORY ITEMS
    reference_document_uri = ""
    custom_response=Shopify_set_inventory_to_zero(shop=shop, access_token=access_token, api_version="2024-01", inventory_item_ids=inventory_item_ids, location_id=location_id, reason=reason, reference_document_uri=reference_document_uri)
    if custom_response.status_code != 200:
        error_message = "Error setting inventory to zero"
        print(error_message)
        return CustomResponse(data=error_message, status_code=400)
    
    return CustomResponse(data="All OK", status_code=200)

def Shopify_collection_unpublish(shop="", access_token="", api_version="2024-01", collection_id=""):
    
    # GET PRODUCTS IN COLLECTION    
    custom_response = Shopify_get_products_in_collection(shop=shop, access_token=access_token, collection_id=collection_id)
    if custom_response.status_code!= 200:
        error_message="Couldn't get products from collection"
        print(error_message)
        return CustomResponse(data=error_message, status_code=400)
    products = custom_response.data
    
    # Filter products already unpublished to speed up
    products = [product for product in products if product['published_at'] is not None]

    # UNPUBLISH PRODUCTS FROM COLLECTION BY CHANNEL ID
    channel_id = Shopify_get_online_store_channel_id(shop=shop, access_token=access_token, api_version=api_version)  
    custom_response = Shopify_unpublish_products_channel(shop=shop, access_token=access_token, api_version=api_version, products=products, channel_id=channel_id)
    if custom_response.status_code != 200:
        error_message="Couldn't unpublish products"
        print(error_message)
        return CustomResponse(data=error_message, status_code=400)
    
    message=f"Collection {collection_id}: {len(products)} products unpublished successfully."
    return CustomResponse(data=message, status_code=200)