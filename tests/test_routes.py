"""Pytests to test the functionality, robustness, and error handling for the API."""


def test_validate_success(client, src_data_wo_factors):
    """
    Test the /validate endpoint with valid input data.

    Parameters:
    - client: The test client used to make HTTP requests.
    - src_data_wo_factors: Source data without factors to be validated.

    Asserts that the response status is 200, the validation results are as expected,
    and the results list matches the input data.
    """
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
    """
    Test the /validate endpoint with invalid data (wrong variable name and category).

    Parameters:
    - client: The test client used to make HTTP requests.
    - src_data_wo_factors: Source data without factors to be validated.

    Asserts that the response status is 200, the validation indicates failure,
    and the specific invalid entry is identified in the results.
    """
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


def test_validate_success_false_01(client, src_data_wo_factors):
    """
    Test the /validate endpoint with a mismatched category for an existing variable.

    Parameters:
    - client: The test client used to make HTTP requests.
    - src_data_wo_factors: Source data without factors to be validated.

    Asserts that the response status is 200, the validation indicates failure,
    and the specific mismatched entry is identified in the results.
    """
    rj_data = src_data_wo_factors["data"]
    r1 = rj_data[1]
    assert r1["var_name"] == "country"
    assert r1["category"] == "Australia"
    r1["category"] = "18-30"
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
        if rjd["var_name"] == "country" and rjd["category"] == "18-30":
            assert res["valid"] is False
        else:
            assert res["valid"] is True


def test_validate_bad_json_00(client):
    """
    Test the /validate endpoint with empty JSON input.

    Parameters:
    - client: The test client used to make HTTP requests.

    Asserts that the response status is 400 and the error message indicates malformed request data.
    """
    response = client.post("/validate", json=[])
    assert response.status_code == 400
    assert "malformed request data" in str(response.data)


def test_validate_bad_json_01(client):
    """
    Test the /validate endpoint with incorrect JSON key.

    Parameters:
    - client: The test client used to make HTTP requests.

    Asserts that the response status is 400 and the error message indicates malformed request data.
    """
    response = client.post("/validate", json={"wrong-key": "some-value"})
    assert response.status_code == 400
    assert "malformed request data" in str(response.data)


def test_validate_bad_json_02(client):
    """
    Test the /validate endpoint with incorrect data type for the 'data' key.

    Parameters:
    - client: The test client used to make HTTP requests.

    Asserts that the response status is 400 and the error message indicates malformed request data.
    """
    response = client.post("/validate", json={"data": "some-value"})
    assert response.status_code == 400
    assert "malformed request data" in str(response.data)


def test_validate_bad_json_03(client, src_data_wo_factors):
    """
    Test the /validate endpoint with incorrect item type in the data list.

    Parameters:
    - client: The test client used to make HTTP requests.
    - src_data_wo_factors: Source data without factors to be validated.

    Asserts that the response status is 404 and the error message indicates malformed request data.
    """
    src_data_wo_factors["data"].append("some-value")
    response = client.post("/validate", json=src_data_wo_factors)
    assert response.status_code == 404
    assert "malformed request data" in str(response.data)


def test_validate_bad_json_04(client, src_data_wo_factors):
    """
    Test the /validate endpoint with a missing 'var_name' key in one of the items.

    Parameters:
    - client: The test client used to make HTTP requests.
    - src_data_wo_factors: Source data without factors to be validated.

    Asserts that the response status is 404 and the error message indicates a missing var_name.
    """
    src_data_wo_factors["data"][3].pop("var_name")
    response = client.post("/validate", json=src_data_wo_factors)
    assert response.status_code == 404
    assert "missing var_name" in str(response.data)


def test_validate_bad_json_05(client, src_data_wo_factors):
    """
    Test the /validate endpoint with a missing 'category' key in one of the items.

    Parameters:
    - client: The test client used to make HTTP requests.
    - src_data_wo_factors: Source data without factors to be validated.

    Asserts that the response status is 404 and the error message indicates a missing category.
    """
    src_data_wo_factors["data"][3].pop("category")
    response = client.post("/validate", json=src_data_wo_factors)
    assert response.status_code == 404
    assert "missing category" in str(response.data)


def test_get_factor_success(client, src_data, src_data_wo_factors):
    """
    Test the /get_factors endpoint with valid input data.

    Parameters:
    - client: The test client used to make HTTP requests.
    - src_data: Source data with factors to be retrieved.
    - src_data_wo_factors: Source data without factors.

    Asserts that the response status is 200, the results are as expected, 
    and each entry in the results matches the corresponding input data.
    """
    sdd = src_data["data"]
    rj_data = src_data_wo_factors["data"]
    response = client.post(
        "/get_factors",
        json=src_data_wo_factors,
    )
    assert response.status_code == 200
    resp_json = response.get_json()
    assert "results" in resp_json
    results = resp_json["results"]
    assert isinstance(results, list)
    assert len(sdd) == len(rj_data) == len(results)
    for sdi, rjd, res in zip(sdd, rj_data, results):
        assert rjd["var_name"] == res["var_name"]
        assert rjd["category"] == res["category"]
        factor = res["factor"]
        assert isinstance(factor, float)
        assert factor == sdi["factor"]


def test_get_factors_bad_json_00(client):
    """
    Test the /get_factors endpoint with empty JSON input.

    Parameters:
    - client: The test client used to make HTTP requests.

    Asserts that the response status is 400 and the error message indicates malformed request data.
    """
    response = client.post("/get_factors", json=[])
    assert response.status_code == 400
    assert "malformed request data" in str(response.data)


def test_get_factors_bad_json_01(client):
    """
    Test the /get_factors endpoint with incorrect JSON key.

    Parameters:
    - client: The test client used to make HTTP requests.

    Asserts that the response status is 400 and the error message indicates malformed request data.
    """
    response = client.post("/get_factors", json={"wrong-key": "some-value"})
    assert response.status_code == 400
    assert "malformed request data" in str(response.data)


def test_get_factors_bad_json_02(client):
    """
    Test the /get_factors endpoint with incorrect data type for the 'data' key.

    Parameters:
    - client: The test client used to make HTTP requests.

    Asserts that the response status is 400 and the error message indicates malformed request data.
    """
    response = client.post("/get_factors", json={"data": "some-value"})
    assert response.status_code == 400
    assert "malformed request data" in str(response.data)


def test_get_factors_bad_json_03(client, src_data_wo_factors):
    """
    Test the /get_factors endpoint with incorrect item type in the data list.

    Parameters:
    - client: The test client used to make HTTP requests.
    - src_data_wo_factors: Source data without factors.

    Asserts that the response status is 404 and the error message indicates malformed request data.
    """
    src_data_wo_factors["data"].append("some-value")
    response = client.post("/get_factors", json=src_data_wo_factors)
    assert response.status_code == 404
    assert "malformed request data" in str(response.data)


def test_get_factors_bad_json_04(client, src_data_wo_factors):
    """
    Test the /get_factors endpoint with a missing 'var_name' key in one of the items.

    Parameters:
    - client: The test client used to make HTTP requests.
    - src_data_wo_factors: Source data without factors.

    Asserts that the response status is 404 and the error message indicates a missing var_name.
    """
    src_data_wo_factors["data"][3].pop("var_name")
    response = client.post("/get_factors", json=src_data_wo_factors)
    assert response.status_code == 404
    assert "missing var_name" in str(response.data)


def test_get_factors_bad_json_05(client, src_data_wo_factors):
    """
    Test the /get_factors endpoint with a missing 'category' key in one of the items.

    Parameters:
    - client: The test client used to make HTTP requests.
    - src_data_wo_factors: Source data without factors.

    Asserts that the response status is 404 and the error message indicates a missing category.
    """
    src_data_wo_factors["data"][3].pop("category")
    response = client.post("/get_factors", json=src_data_wo_factors)
    assert response.status_code == 404
    assert "missing category" in str(response.data)


def test_get_factors_invalid_00(client, src_data_wo_factors):
    """
    Test the /get_factors endpoint with invalid data (wrong variable name and category).

    Parameters:
    - client: The test client used to make HTTP requests.
    - src_data_wo_factors: Source data without factors.

    Asserts that the response status is 404 and the error message indicates invalid var_name or
    category.
    """
    rj_data = src_data_wo_factors["data"]
    rj_data.append({"var_name": "wrong", "category": "UK"})
    response = client.post(
        "/get_factors",
        json=src_data_wo_factors,
    )
    assert response.status_code == 404
    assert "invalid var_name or category" in str(response.data)


def test_get_factors_invalid_01(client, src_data_wo_factors):
    """
    Test the /get_factors endpoint with a mismatched category for an existing variable.

    Parameters:
    - client: The test client used to make HTTP requests.
    - src_data_wo_factors: Source data without factors.

    Asserts that the response status is 404 and the error message indicates invalid var_name or
    category.
    """
    rj_data = src_data_wo_factors["data"]
    r1 = rj_data[1]
    assert r1["var_name"] == "country"
    assert r1["category"] == "Australia"
    r1["category"] = "18-30"
    response = client.post(
        "/get_factors",
        json=src_data_wo_factors,
    )
    assert response.status_code == 404
    assert "invalid var_name or category" in str(response.data)
