import json

from flask import Blueprint, request, jsonify, abort
from .redis_client import redis_store


bp = Blueprint("api", __name__)


def common_req_data_loop(ending):
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

    def gf_ending(exists, rj, vnc):
        if not exists:
            abort(404, description="invalid var_name or category")
        factor = float(redis_store.get(vnc))
        rj["factor"] = factor

    req_data = common_req_data_loop(gf_ending)
    return jsonify({"results": req_data})
