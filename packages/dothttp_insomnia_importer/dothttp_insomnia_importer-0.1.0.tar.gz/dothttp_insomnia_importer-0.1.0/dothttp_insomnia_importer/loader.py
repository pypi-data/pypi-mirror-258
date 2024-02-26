import json
import os
import sys
import uuid

from .utils import add_url_params

rootId = "d1097c3b-2011-47a4-8f95-87b8f4b54d6d"  # unique guid for root


def transform_url(insomnia_url):
    """
    Transforms the given Insomnia URL.

    Args:
        insomnia_url (str): The Insomnia URL to be transformed.

    Returns:
        str: The transformed URL.
    """
    return insomnia_url

def transform_headers(insomnia_headers):
    """
    Transforms the headers from the Insomnia format to a list of dictionaries.

    Args:
        insomnia_headers (list): List of headers in the Insomnia format.

    Returns:
        list: List of dictionaries representing the transformed headers.
    """
    output_headers = []
    for element in insomnia_headers:
        header = {}
        header['key'] = element['name']
        header['value'] = element['value']
        output_headers.append(header)
    return output_headers

def transform_body(insomnia_body):
    """
    Transforms the body of an Insomnia request to a format compatible with Postman.

    Args:
        insomnia_body (dict): The body of the Insomnia request.

    Returns:
        dict: The transformed body in a format compatible with Postman.
    """
    body = {}
    if insomnia_body['mimeType'] in ["", "application/json", "application/xml"]:
        body['mode'] = "raw"
        body['raw'] = insomnia_body['text']
    elif insomnia_body['mimeType'] == "multipart/form-data":
        body['mode'] = "formdata"
        body['formdata'] = [{'key': param['name'], 'value': param['value']} for param in insomnia_body['params']]
    elif insomnia_body['mimeType'] == "application/x-www-form-urlencoded":
        body['mode'] = "urlencoded"
        body['urlencoded'] = [{'key': param['name'], 'value': param['value']} for param in insomnia_body['params']]
    elif insomnia_body['mimeType'] == "application/octet-stream":
        body['mode'] = "file"
        body['file'] = {}
        body['file']['src'] = "/C:/PleaseSelectAFile"
        print("Warning: A file is supposed to be a part of the request!!! Would need to be manually selected in Postman.")
    elif insomnia_body['mimeType'] == "application/graphql":
        graphql_body = json.loads(insomnia_body['text'])
        body['mode'] = "graphql"
        body['graphql'] = {}
        body['graphql']['query'] = graphql_body['query']
        body['graphql']['variables'] = json.dumps(graphql_body['variables'])
    else:
        print("Warning: Body type unsupported; skipped!!! ... " + insomnia_body['mimeType'])
        body['mode'] = "raw"
        body['raw'] = "github.com/Vyoam/InsomniaToPostmanFormat: Unsupported body type "+insomnia_body['mimeType']
    return body

def transform_item(insomnia_item):
    """
    Transforms an Insomnia item into a Postman item.

    Args:
        insomnia_item (dict): The Insomnia item to be transformed.

    Returns:
        dict: The transformed Postman item.
    """
    postman_item = {}
    postman_item['name'] = insomnia_item['name']
    request = {}
    request['description'] = insomnia_item['description']
    request['method'] = insomnia_item['method']
    request['header'] = transform_headers(insomnia_item['headers'])
    if insomnia_item['body']:
        request['body'] = transform_body(insomnia_item['body'])
    query = []
    request['url'] = transform_url(insomnia_item['url'])
    if 'parameters' in insomnia_item and insomnia_item['parameters']:
        if 'raw' in request['url'] and "?" in request['url']['raw']:
            print("Warning: Query params detected in both the raw query and the 'parameters' object of Insomnia request!!! Exported Postman collection may need manual editing for erroneous '?' in url.")
        query =[(param['name'], param['value']) for param in insomnia_item['parameters']]
    request['url'] = add_url_params(request['url'], query)
    
    request['auth'] = {} # todo
    if insomnia_item['authentication']:
        print("Warning: Auth param export not yet supported!!!")
    postman_item['request'] = request
    postman_item['response'] = []
    return postman_item


def generate_maps(insomnia_parent_child_list):
    """
    Generate parent-children map and flat map from the given Insomnia parent-child list.

    Args:
        insomnia_parent_child_list (list): List of Insomnia parent-child elements.

    Returns:
        tuple: A tuple containing two dictionaries:
            - parent_children_map: A dictionary mapping parent IDs to their corresponding children.
            - flat_map: A dictionary mapping element IDs to their corresponding elements.
    """
    parent_children_map = {}
    flat_map = {}
    for element in insomnia_parent_child_list:
        flat_map[element['_id']] = element
        if element['_type'] == "workspace":
            parent_children_map[rootId] = [element]
        elif element['_type'] in ["request", "request_group"]:
            if element['parentId'] not in parent_children_map:
                parent_children_map[element['parentId']] = []
            parent_children_map[element['parentId']].append(element)
        else:
            print(f"Warning: Item type unsupported; skipped!!! ... {element['_type']}")
    return parent_children_map, flat_map

def generate_tree_recursively(element, parent_children_map):
    """
    Recursively generates a tree structure from an Insomnia element.

    Args:
        element (dict): The Insomnia element to generate the tree from.
        parent_children_map (dict): A mapping of parent element IDs to their child elements.

    Returns:
        dict: The generated tree structure in the form of a dictionary.
    """
    postman_item = {}
    if element['_type'] == "request_group":
        postman_item['name'] = element['name']
        postman_item['item'] = [generate_tree_recursively(child, parent_children_map) for child in parent_children_map.get(element['_id'], [])]
    elif element['_type'] == "request":
        postman_item = transform_item(element)
    else:
        print(f"Warning: Item type unsupported; skipped!!! ... {element['_type']}")
    return postman_item

def get_sub_item_trees(parent_children_map):
    """
    Generate sub-item trees recursively based on the parent-children map.

    Args:
        parent_children_map (dict): A dictionary representing the parent-children relationship.

    Returns:
        list: A list of sub-item trees generated recursively.

    """
    sub_item_trees = []
    roots = parent_children_map.get(rootId, [])
    for element in parent_children_map.get(roots[0]['_id'], []):
        sub_item_trees.append(generate_tree_recursively(element, parent_children_map))
    return sub_item_trees

def transform_data(input_data_string, filename):
    """
    Transforms the input data from Insomnia format to Postman format.

    Args:
        input_data_string (str): The input data string in Insomnia format.
        filename (str): The name of the file.

    Returns:
        dict: The transformed data in Postman format.
    """
    input_data = json.loads(input_data_string)
    if input_data['__export_format'] != 4:
        print(f"Error: Version (__export_format {input_data['__export_format']}) not supported. Only version 4 is supported.")
        sys.exit(2)
    output_data = {
        "info": {
            "_postman_id": "",
            "name": "",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "item": []
    }
    output_data['info']['_postman_id'] = str(uuid.uuid4())
    parent_children_map, flat_map = generate_maps(input_data['resources'])
    sub_items = get_sub_item_trees(parent_children_map)
    output_data['item'].extend(sub_items)
    output_data['info']['name'] = os.path.splitext(filename)[0]
    return output_data

