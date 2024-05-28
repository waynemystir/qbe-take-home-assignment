import json


def test_validate_success(client, src_data_wo_factors):
    rj_data = src_data_wo_factors["data"]
    response = client.post(
        "/validate",
        json=src_data_wo_factors,
    )
    assert response.status_code == 200
    resp_json = response.get_json()
    assert "is_valid" in resp_json
    is_valid = resp_json["is_valid"]
    assert is_valid is True
    assert "results" in resp_json
    results = resp_json["results"]
    assert isinstance(results, list)
    assert len(rj_data) == len(results)
    for rjd, res in zip(rj_data, results):
        assert rjd["var_name"] == res["var_name"]
        assert rjd["category"] == res["category"]
        assert res["valid"] is True


def test_validate_success_false_00(client, src_data_wo_factors):
    rj_data = src_data_wo_factors["data"]
    rj_data.append({"var_name": "wrong", "category": "UK"})
    response = client.post(
        "/validate",
        json=src_data_wo_factors,
    )
    assert response.status_code == 200
    resp_json = response.get_json()
    assert "is_valid" in resp_json
    is_valid = resp_json["is_valid"]
    assert is_valid is False
    assert "results" in resp_json
    results = resp_json["results"]
    assert isinstance(results, list)
    assert len(rj_data) == len(results)
    for rjd, res in zip(rj_data, results):
        assert rjd["var_name"] == res["var_name"]
        assert rjd["category"] == res["category"]
        if rjd["var_name"] == "wrong":
            assert res["valid"] is False
        else:
            assert res["valid"] is True
