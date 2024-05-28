import json

from flask import Blueprint, request, jsonify, abort
from .redis_client import redis_store


bp = Blueprint("api", __name__)


@bp.route("/validate", methods=["POST"])
def validate():
    req_json = request.get_json()
    print(f"EEE:{req_json=}")
    if not isinstance(req_json, dict):
        return abort(400, description="malformed request data")
    req_data = req_json.get("data", None)
    if not isinstance(req_data, list):
        return abort(400, description="malformed request data")

    is_valid = True
    for rj in req_data:
        if not isinstance(rj, dict):
            return abort(404, description="malformed request data")
        var_name = rj.get("var_name", None)
        category = rj.get("category", None)
        if not isinstance(var_name, str):
            return abort(404, description="missing var_name")
        if not isinstance(category, str):
            return abort(404, description="missing category")
        vnc = var_name + category
        exists = redis_store.exists(vnc)
        # if exists, then it must be that var_name is in {"country", "age_group"} and
        # category matches var_name
        if exists:
            rj["valid"] = True
            continue
        # if not exists, then either var_name is not in {"country", "age_group"} or
        # category doesn't match var_name
        is_valid = False
        rj["valid"] = False

    return jsonify({"is_valid": is_valid, "results": req_data})


@bp.route("/get_factors", methods=["POST"])
def get_factors():
    req_json = request.get_json()
    print(f"QQQ:{req_json=}")
    if not isinstance(req_json, dict):
        return abort(400, description="malformed request data")
    req_data = req_json.get("data", None)
    if not isinstance(req_data, list):
        return abort(400, description="malformed request data")

    for rj in req_data:
        if not isinstance(rj, dict):
            return abort(404, description="malformed request data")
        var_name = rj.get("var_name", None)
        category = rj.get("category", None)
        if not isinstance(var_name, str):
            return abort(404, description="missing var_name")
        if not isinstance(category, str):
            return abort(404, description="missing category")
        vnc = var_name + category
        exists = redis_store.exists(vnc)
        if not exists:
            return abort(404, description="invalid var_name or category")
        factor = float(redis_store.get(vnc))
        rj["factor"] = factor

    return jsonify({"results": req_data})
