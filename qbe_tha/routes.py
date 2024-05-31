"""
Define and implement the API routes
"""

from flask import Blueprint, request, jsonify, abort
from .redis_client import redis_store

bp = Blueprint("api", __name__)


def common_req_data_loop(ending):
    """
    Process the common request data for both validate and get_factors endpoints.

    Parameters:
    - ending: A function to execute at the end of processing each item in the request data.

    Retrieves JSON data from the request, validates its structure, and processes each item
    using the provided ending function. Aborts the request with a 400 or 404 status code if 
    the request data is malformed or missing required fields.

    Returns:
    - req_data: The list of request data items.
    """
    req_json = request.get_json()
    if not isinstance(req_json, dict):
        abort(400, description="malformed request data")
    req_data = req_json.get("data", None)
    if not isinstance(req_data, list):
        abort(400, description="malformed request data")

    for rj in req_data:
        if not isinstance(rj, dict):
            abort(404, description="malformed request data")
        var_name = rj.get("var_name", None)
        category = rj.get("category", None)
        if not isinstance(var_name, str):
            abort(404, description="missing var_name")
        if not isinstance(category, str):
            abort(404, description="missing category")
        vnc = var_name + category
        exists = redis_store.exists(vnc)
        ending(exists, rj, vnc)

    return req_data


@bp.route("/validate", methods=["POST"])
def validate():
    """
    API endpoint to validate the existence of variable names and categories.

    Processes the request data to check if each variable name and category exists in the Redis store.
    Returns a JSON response indicating whether all entries are valid and includes the validation 
    results for each item.

    Returns:
    - JSON response with keys "is_valid" (boolean) and "results" (list of request data with validation status).
    """
    is_valid = True

    def val_ending(exists, rj, vnc):
        nonlocal is_valid
        # if exists, then it must be that var_name is in {"country", "age_group"} and
        # category matches var_name
        if exists:
            rj["valid"] = True
            return
        # if not exists, then either var_name is not in {"country", "age_group"} or
        # category doesn't match var_name
        is_valid = False
        rj["valid"] = False

    req_data = common_req_data_loop(val_ending)
    return jsonify({"is_valid": is_valid, "results": req_data})


@bp.route("/get_factors", methods=["POST"])
def get_factors():
    """
    API endpoint to retrieve factors for valid variable names and categories.

    Processes the request data to retrieve factors from the Redis store for each variable name and
    category. Aborts the request with a 404 status code if an entry is invalid. Returns a JSON
    response with the factors for each valid entry.

    Returns:
    - JSON response with key "results" (list of request data with factors included).
    """

    def gf_ending(exists, rj, vnc):
        if not exists:
            abort(404, description="invalid var_name or category")
        factor = float(redis_store.get(vnc))
        rj["factor"] = factor

    req_data = common_req_data_loop(gf_ending)
    return jsonify({"results": req_data})
