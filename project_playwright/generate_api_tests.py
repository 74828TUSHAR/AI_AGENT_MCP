from pathlib import Path

HEADER = """import logging

import allure
import pytest

from constants.api_routes import *
from utils.api_assertions import assert_api_field_equal, assert_api_truthy
from utils.api_flows import create_user, delete_user, get_user_by_email, update_user
from utils.api_test_runner import log_api_header, run_api_scenario

TEST_DATA_FILE = "api/api_regression.json"

logger = logging.getLogger(__name__)


"""


def wrap_test(case_no, title, story, func_name, scenarios, body):
    scenario_dict = "{\n" + ",\n".join(
        f'        "{key}": "{value}"' for key, value in scenarios.items()
    ) + "\n    }"
    return f"""@pytest.mark.asyncio
@pytest.mark.regression
@pytest.mark.test_data(index=0)
@allure.feature("API")
@allure.story("{story}")
@allure.title("API Case {case_no:02d} - {title}")
async def {func_name}(api_client, test_record):
    scenarios = {scenario_dict}
    log_api_header(logger, "{func_name}", scenarios)

{body}
"""


def block(scenario_no, description, step_title, inner):
    return f"""    # ============================================================
    # SCENARIO {scenario_no}: {description}
    # ============================================================
    with allure.step("Scenario {scenario_no}: {step_title}"):
        async def scenario():
{indent(inner, 3)}

        await run_api_scenario(logger, test_name, "scenario_{scenario_no}", scenario)

"""


def indent(text, level):
    pad = "    " * level
    return "\n".join(f"{pad}{line}" if line else "" for line in text.splitlines())


def simple_body(assertions):
    return assertions


def main():
    base = Path("tests") / "UI" / "nightly" / "regression"
    base.mkdir(parents=True, exist_ok=True)
    for pkg in [Path("tests") / "UI", Path("tests") / "UI" / "nightly", base]:
        (pkg / "__init__.py").write_text("", encoding="utf-8")

    filenames = {
        1: "test_api_case_01_get_all_products_list.py",
        2: "test_api_case_02_post_all_products_list_not_supported.py",
        3: "test_api_case_03_get_all_brands_list.py",
        4: "test_api_case_04_put_brands_list_not_supported.py",
        5: "test_api_case_05_search_product.py",
        6: "test_api_case_06_search_product_without_parameter.py",
        7: "test_api_case_07_verify_login_valid.py",
        8: "test_api_case_08_verify_login_missing_email.py",
        9: "test_api_case_09_verify_login_delete_not_supported.py",
        10: "test_api_case_10_verify_login_invalid.py",
        11: "test_api_case_11_create_account.py",
        12: "test_api_case_12_delete_account.py",
        13: "test_api_case_13_update_account.py",
        14: "test_api_case_14_get_user_detail_by_email.py",
        15: "test_api_case_15_get_user_detail_missing_email.py",
        16: "test_api_case_16_validate_products_payload_structure.py",
        17: "test_api_case_17_validate_product_item_fields.py",
        18: "test_api_case_18_validate_brands_payload_structure.py",
        19: "test_api_case_19_validate_brand_item_fields.py",
        20: "test_api_case_20_validate_search_results_payload_structure.py",
        21: "test_api_case_21_validate_search_results_non_empty.py",
        22: "test_api_case_22_create_account_response_contract.py",
        23: "test_api_case_23_created_user_can_verify_login.py",
        24: "test_api_case_24_updated_user_detail_persists.py",
        25: "test_api_case_25_deleted_user_cannot_verify_login.py",
        26: "test_api_case_26_search_product_secondary_term.py",
    }

    cases = {}

    cases[1] = wrap_test(
        1,
        "Get all products list",
        "Products API",
        "test_api_case_01_get_all_products_list",
        {"scenario_1": "Send GET request to products list API and verify successful response"},
        """    test_name = "test_api_case_01_get_all_products_list"\n\n"""
        + block(1, "Send GET request to products list API and verify successful response", "GET products list",
                """response = await api_client.get(PRODUCTS_LIST)\nassert_api_field_equal(logger, field_name="response_code", actual=response.response_code, expected=200, response=response)\nassert_api_truthy(logger, field_name="products_list", actual=response.body_json.get("products"), response=response)""")
    )

    cases[2] = wrap_test(
        2, "POST to all products list is not supported", "Products API",
        "test_api_case_02_post_all_products_list_not_supported",
        {"scenario_1": "Send POST request to products list API and verify method not supported response"},
        """    test_name = "test_api_case_02_post_all_products_list_not_supported"\n\n"""
        + block(1, "Send POST request to products list API and verify method not supported response", "POST products list",
                """response = await api_client.post(PRODUCTS_LIST)\nassert_api_field_equal(logger, field_name="response_code", actual=response.response_code, expected=405, response=response)\nassert_api_field_equal(logger, field_name="message", actual=response.message, expected="This request method is not supported.", response=response)""")
    )

    cases[3] = wrap_test(
        3, "Get all brands list", "Brands API",
        "test_api_case_03_get_all_brands_list",
        {"scenario_1": "Send GET request to brands list API and verify successful response"},
        """    test_name = "test_api_case_03_get_all_brands_list"\n\n"""
        + block(1, "Send GET request to brands list API and verify successful response", "GET brands list",
                """response = await api_client.get(BRANDS_LIST)\nassert_api_field_equal(logger, field_name="response_code", actual=response.response_code, expected=200, response=response)\nassert_api_truthy(logger, field_name="brands_list", actual=response.body_json.get("brands"), response=response)""")
    )

    cases[4] = wrap_test(
        4, "PUT to all brands list is not supported", "Brands API",
        "test_api_case_04_put_brands_list_not_supported",
        {"scenario_1": "Send PUT request to brands list API and verify method not supported response"},
        """    test_name = "test_api_case_04_put_brands_list_not_supported"\n\n"""
        + block(1, "Send PUT request to brands list API and verify method not supported response", "PUT brands list",
                """response = await api_client.put(BRANDS_LIST)\nassert_api_field_equal(logger, field_name="response_code", actual=response.response_code, expected=405, response=response)\nassert_api_field_equal(logger, field_name="message", actual=response.message, expected="This request method is not supported.", response=response)""")
    )

    cases[5] = wrap_test(
        5, "Search product with valid parameter", "Search Product API",
        "test_api_case_05_search_product",
        {"scenario_1": "Send POST request to search product API and verify successful response"},
        """    test_name = "test_api_case_05_search_product"\n\n"""
        + block(1, "Send POST request to search product API and verify successful response", "Search product",
                """response = await api_client.post(SEARCH_PRODUCT, form={"search_product": test_record["search_product"]})\nassert_api_field_equal(logger, field_name="response_code", actual=response.response_code, expected=200, response=response)\nassert_api_truthy(logger, field_name="search_results", actual=response.body_json.get("products"), response=response)""")
    )

    cases[6] = wrap_test(
        6, "Search product without parameter", "Search Product API",
        "test_api_case_06_search_product_without_parameter",
        {"scenario_1": "Send POST request to search product API without parameter and verify bad request response"},
        """    test_name = "test_api_case_06_search_product_without_parameter"\n\n"""
        + block(1, "Send POST request to search product API without parameter and verify bad request response", "Search product without parameter",
                """response = await api_client.post(SEARCH_PRODUCT)\nassert_api_field_equal(logger, field_name="response_code", actual=response.response_code, expected=400, response=response)\nassert_api_field_equal(logger, field_name="message", actual=response.message, expected="Bad request, search_product parameter is missing in POST request.", response=response)""")
    )

    cases[7] = wrap_test(
        7, "Verify login with valid details", "Verify Login API",
        "test_api_case_07_verify_login_valid",
        {"scenario_1": "Send POST request to verify login API with valid email and password"},
        """    test_name = "test_api_case_07_verify_login_valid"\n\n"""
        + block(1, "Send POST request to verify login API with valid email and password", "Verify valid login",
                """response = await api_client.post(VERIFY_LOGIN, form={"email": test_record["valid_login_email"], "password": test_record["valid_login_password"]})\nassert_api_field_equal(logger, field_name="response_code", actual=response.response_code, expected=200, response=response)\nassert_api_field_equal(logger, field_name="message", actual=response.message, expected="User exists!", response=response)""")
    )

    cases[8] = wrap_test(
        8, "Verify login without email", "Verify Login API",
        "test_api_case_08_verify_login_missing_email",
        {"scenario_1": "Send POST request to verify login API without email and verify bad request response"},
        """    test_name = "test_api_case_08_verify_login_missing_email"\n\n"""
        + block(1, "Send POST request to verify login API without email and verify bad request response", "Verify login without email",
                """response = await api_client.post(VERIFY_LOGIN, form={"password": test_record["valid_login_password"]})\nassert_api_field_equal(logger, field_name="response_code", actual=response.response_code, expected=400, response=response)\nassert_api_field_equal(logger, field_name="message", actual=response.message, expected="Bad request, email or password parameter is missing in POST request.", response=response)""")
    )

    cases[9] = wrap_test(
        9, "DELETE to verify login is not supported", "Verify Login API",
        "test_api_case_09_verify_login_delete_not_supported",
        {"scenario_1": "Send DELETE request to verify login API and verify method not supported response"},
        """    test_name = "test_api_case_09_verify_login_delete_not_supported"\n\n"""
        + block(1, "Send DELETE request to verify login API and verify method not supported response", "DELETE verify login",
                """response = await api_client.delete(VERIFY_LOGIN)\nassert_api_field_equal(logger, field_name="response_code", actual=response.response_code, expected=405, response=response)\nassert_api_field_equal(logger, field_name="message", actual=response.message, expected="This request method is not supported.", response=response)""")
    )

    cases[10] = wrap_test(
        10, "Verify login with invalid details", "Verify Login API",
        "test_api_case_10_verify_login_invalid",
        {"scenario_1": "Send POST request to verify login API with invalid email and password"},
        """    test_name = "test_api_case_10_verify_login_invalid"\n\n"""
        + block(1, "Send POST request to verify login API with invalid email and password", "Verify invalid login",
                """response = await api_client.post(VERIFY_LOGIN, form={"email": test_record["invalid_login_email"], "password": test_record["invalid_login_password"]})\nassert_api_field_equal(logger, field_name="response_code", actual=response.response_code, expected=404, response=response)\nassert_api_field_equal(logger, field_name="message", actual=response.message, expected="User not found!", response=response)""")
    )

    cases[11] = wrap_test(
        11, "Create account", "Account API",
        "test_api_case_11_create_account",
        {"scenario_1": "Create a new account and verify successful account creation response", "scenario_2": "Delete created account as cleanup"},
        """    test_name = "test_api_case_11_create_account"\n    created_payload = {}\n\n"""
        + block(1, "Create a new account and verify successful account creation response", "Create account",
                """nonlocal created_payload\ncreated_payload, response = await create_user(api_client, test_record["user_template"])\nassert_api_field_equal(logger, field_name="response_code", actual=response.response_code, expected=201, response=response)\nassert_api_field_equal(logger, field_name="message", actual=response.message, expected="User created!", response=response)""")
        + block(2, "Delete created account as cleanup", "Cleanup created account",
                """response = await delete_user(api_client, created_payload["email"], created_payload["password"])\nassert_api_field_equal(logger, field_name="cleanup_response_code", actual=response.response_code, expected=200, response=response)""")
    )

    cases[12] = wrap_test(
        12, "Delete account", "Account API",
        "test_api_case_12_delete_account",
        {"scenario_1": "Create a new account for delete validation", "scenario_2": "Delete created account and verify successful response"},
        """    test_name = "test_api_case_12_delete_account"\n    created_payload = {}\n\n"""
        + block(1, "Create a new account for delete validation", "Create account for deletion",
                """nonlocal created_payload\ncreated_payload, response = await create_user(api_client, test_record["user_template"])\nassert_api_field_equal(logger, field_name="create_response_code", actual=response.response_code, expected=201, response=response)""")
        + block(2, "Delete created account and verify successful response", "Delete account",
                """response = await delete_user(api_client, created_payload["email"], created_payload["password"])\nassert_api_field_equal(logger, field_name="response_code", actual=response.response_code, expected=200, response=response)\nassert_api_field_equal(logger, field_name="message", actual=response.message, expected="Account deleted!", response=response)""")
    )

    cases[13] = wrap_test(
        13, "Update account", "Account API",
        "test_api_case_13_update_account",
        {"scenario_1": "Create a new account for update validation", "scenario_2": "Update account and verify successful response", "scenario_3": "Delete updated account as cleanup"},
        """    test_name = "test_api_case_13_update_account"\n    created_payload = {}\n    updated_payload = {}\n\n"""
        + block(1, "Create a new account for update validation", "Create account for update",
                """nonlocal created_payload\ncreated_payload, response = await create_user(api_client, test_record["user_template"])\nassert_api_field_equal(logger, field_name="create_response_code", actual=response.response_code, expected=201, response=response)""")
        + block(2, "Update account and verify successful response", "Update account",
                """nonlocal updated_payload\nupdated_payload, response = await update_user(api_client, created_payload, test_record["updated_user_template"])\nassert_api_field_equal(logger, field_name="response_code", actual=response.response_code, expected=200, response=response)\nassert_api_field_equal(logger, field_name="message", actual=response.message, expected="User updated!", response=response)""")
        + block(3, "Delete updated account as cleanup", "Cleanup updated account",
                """response = await delete_user(api_client, updated_payload["email"], updated_payload["password"])\nassert_api_field_equal(logger, field_name="cleanup_response_code", actual=response.response_code, expected=200, response=response)""")
    )

    cases[14] = wrap_test(
        14, "Get user detail by email", "Account API",
        "test_api_case_14_get_user_detail_by_email",
        {"scenario_1": "Create a new account for detail validation", "scenario_2": "Get user detail by email and verify returned user data", "scenario_3": "Delete created account as cleanup"},
        """    test_name = "test_api_case_14_get_user_detail_by_email"\n    created_payload = {}\n\n"""
        + block(1, "Create a new account for detail validation", "Create account for detail lookup",
                """nonlocal created_payload\ncreated_payload, response = await create_user(api_client, test_record["user_template"])\nassert_api_field_equal(logger, field_name="create_response_code", actual=response.response_code, expected=201, response=response)""")
        + block(2, "Get user detail by email and verify returned user data", "Get user detail by email",
                """response = await get_user_by_email(api_client, created_payload["email"])\nuser = response.body_json.get("user", {})\nassert_api_field_equal(logger, field_name="response_code", actual=response.response_code, expected=200, response=response)\nassert_api_field_equal(logger, field_name="user_email", actual=user.get("email"), expected=created_payload["email"], response=response)""")
        + block(3, "Delete created account as cleanup", "Cleanup created account",
                """response = await delete_user(api_client, created_payload["email"], created_payload["password"])\nassert_api_field_equal(logger, field_name="cleanup_response_code", actual=response.response_code, expected=200, response=response)""")
    )

    cases[15] = wrap_test(
        15, "Get user detail without email", "Account API",
        "test_api_case_15_get_user_detail_missing_email",
        {"scenario_1": "Send GET request to user detail API without email and verify bad request response"},
        """    test_name = "test_api_case_15_get_user_detail_missing_email"\n\n"""
        + block(1, "Send GET request to user detail API without email and verify bad request response", "Get user detail without email",
                """response = await api_client.get(GET_USER_DETAIL_BY_EMAIL)\nassert_api_field_equal(logger, field_name="response_code", actual=response.response_code, expected=400, response=response)\nassert_api_field_equal(logger, field_name="message", actual=response.message, expected="Bad request, email parameter is missing in GET request.", response=response)""")
    )

    cases[16] = wrap_test(
        16, "Validate products payload structure", "Products Contract",
        "test_api_case_16_validate_products_payload_structure",
        {"scenario_1": "Verify products list response contains top-level contract keys"},
        """    test_name = "test_api_case_16_validate_products_payload_structure"\n\n"""
        + block(1, "Verify products list response contains top-level contract keys", "Validate products payload structure",
                """response = await api_client.get(PRODUCTS_LIST)\nbody = response.body_json\nassert_api_field_equal(logger, field_name="response_code", actual=body.get("responseCode"), expected=200, response=response)\nassert_api_truthy(logger, field_name="has_products_key", actual="products" in body, response=response)\nassert_api_truthy(logger, field_name="products_is_list", actual=isinstance(body.get("products"), list), response=response)""")
    )

    cases[17] = wrap_test(
        17, "Validate first product item fields", "Products Contract",
        "test_api_case_17_validate_product_item_fields",
        {"scenario_1": "Verify first product item contains required product fields"},
        """    test_name = "test_api_case_17_validate_product_item_fields"\n\n"""
        + block(1, "Verify first product item contains required product fields", "Validate first product item",
                """response = await api_client.get(PRODUCTS_LIST)\nproduct = response.body_json.get("products", [])[0]\nfor field_name in ["id", "name", "price", "brand", "category"]:\n    assert_api_truthy(logger, field_name=f"first_product_{field_name}", actual=field_name in product, response=response)""")
    )

    cases[18] = wrap_test(
        18, "Validate brands payload structure", "Brands Contract",
        "test_api_case_18_validate_brands_payload_structure",
        {"scenario_1": "Verify brands list response contains required top-level contract keys"},
        """    test_name = "test_api_case_18_validate_brands_payload_structure"\n\n"""
        + block(1, "Verify brands list response contains required top-level contract keys", "Validate brands payload structure",
                """response = await api_client.get(BRANDS_LIST)\nbody = response.body_json\nassert_api_field_equal(logger, field_name="response_code", actual=body.get("responseCode"), expected=200, response=response)\nassert_api_truthy(logger, field_name="has_brands_key", actual="brands" in body, response=response)\nassert_api_truthy(logger, field_name="brands_is_list", actual=isinstance(body.get("brands"), list), response=response)""")
    )

    cases[19] = wrap_test(
        19, "Validate first brand item fields", "Brands Contract",
        "test_api_case_19_validate_brand_item_fields",
        {"scenario_1": "Verify first brand item contains required fields"},
        """    test_name = "test_api_case_19_validate_brand_item_fields"\n\n"""
        + block(1, "Verify first brand item contains required fields", "Validate first brand item",
                """response = await api_client.get(BRANDS_LIST)\nbrand = response.body_json.get("brands", [])[0]\nfor field_name in ["id", "brand"]:\n    assert_api_truthy(logger, field_name=f"first_brand_{field_name}", actual=field_name in brand, response=response)""")
    )

    cases[20] = wrap_test(
        20, "Validate search results payload structure", "Search Product Contract",
        "test_api_case_20_validate_search_results_payload_structure",
        {"scenario_1": "Verify search product response contains required top-level keys"},
        """    test_name = "test_api_case_20_validate_search_results_payload_structure"\n\n"""
        + block(1, "Verify search product response contains required top-level keys", "Validate search payload structure",
                """response = await api_client.post(SEARCH_PRODUCT, form={"search_product": test_record["search_product"]})\nbody = response.body_json\nassert_api_field_equal(logger, field_name="response_code", actual=body.get("responseCode"), expected=200, response=response)\nassert_api_truthy(logger, field_name="has_products_key", actual="products" in body, response=response)\nassert_api_truthy(logger, field_name="products_is_list", actual=isinstance(body.get("products"), list), response=response)""")
    )

    cases[21] = wrap_test(
        21, "Validate search results are non-empty", "Search Product Contract",
        "test_api_case_21_validate_search_results_non_empty",
        {"scenario_1": "Verify valid search term returns at least one product"},
        """    test_name = "test_api_case_21_validate_search_results_non_empty"\n\n"""
        + block(1, "Verify valid search term returns at least one product", "Validate search results are non-empty",
                """response = await api_client.post(SEARCH_PRODUCT, form={"search_product": test_record["search_product_secondary"]})\nproducts = response.body_json.get("products", [])\nassert_api_truthy(logger, field_name="non_empty_search_results", actual=len(products) > 0, response=response)""")
    )

    cases[22] = wrap_test(
        22, "Validate create account response contract", "Account Contract",
        "test_api_case_22_create_account_response_contract",
        {"scenario_1": "Create a new account and validate create account response contract", "scenario_2": "Delete created account as cleanup"},
        """    test_name = "test_api_case_22_create_account_response_contract"\n    created_payload = {}\n\n"""
        + block(1, "Create a new account and validate create account response contract", "Validate create account contract",
                """nonlocal created_payload\ncreated_payload, response = await create_user(api_client, test_record["user_template"])\nassert_api_field_equal(logger, field_name="response_code", actual=response.response_code, expected=201, response=response)\nassert_api_field_equal(logger, field_name="message", actual=response.message, expected="User created!", response=response)""")
        + block(2, "Delete created account as cleanup", "Cleanup created account",
                """response = await delete_user(api_client, created_payload["email"], created_payload["password"])\nassert_api_field_equal(logger, field_name="cleanup_response_code", actual=response.response_code, expected=200, response=response)""")
    )

    cases[23] = wrap_test(
        23, "Created user can verify login", "Account Lifecycle",
        "test_api_case_23_created_user_can_verify_login",
        {"scenario_1": "Create a new account", "scenario_2": "Verify created user login through verify login API", "scenario_3": "Delete created account as cleanup"},
        """    test_name = "test_api_case_23_created_user_can_verify_login"\n    created_payload = {}\n\n"""
        + block(1, "Create a new account", "Create account",
                """nonlocal created_payload\ncreated_payload, response = await create_user(api_client, test_record["user_template"])\nassert_api_field_equal(logger, field_name="create_response_code", actual=response.response_code, expected=201, response=response)""")
        + block(2, "Verify created user login through verify login API", "Verify created user login",
                """response = await api_client.post(VERIFY_LOGIN, form={"email": created_payload["email"], "password": created_payload["password"]})\nassert_api_field_equal(logger, field_name="response_code", actual=response.response_code, expected=200, response=response)\nassert_api_field_equal(logger, field_name="message", actual=response.message, expected="User exists!", response=response)""")
        + block(3, "Delete created account as cleanup", "Cleanup created account",
                """response = await delete_user(api_client, created_payload["email"], created_payload["password"])\nassert_api_field_equal(logger, field_name="cleanup_response_code", actual=response.response_code, expected=200, response=response)""")
    )

    cases[24] = wrap_test(
        24, "Updated user details persist", "Account Lifecycle",
        "test_api_case_24_updated_user_detail_persists",
        {"scenario_1": "Create a new account", "scenario_2": "Update created account", "scenario_3": "Get user details and verify updated fields", "scenario_4": "Delete updated account as cleanup"},
        """    test_name = "test_api_case_24_updated_user_detail_persists"\n    created_payload = {}\n    updated_payload = {}\n\n"""
        + block(1, "Create a new account", "Create account",
                """nonlocal created_payload\ncreated_payload, response = await create_user(api_client, test_record["user_template"])\nassert_api_field_equal(logger, field_name="create_response_code", actual=response.response_code, expected=201, response=response)""")
        + block(2, "Update created account", "Update account",
                """nonlocal updated_payload\nupdated_payload, response = await update_user(api_client, created_payload, test_record["updated_user_template"])\nassert_api_field_equal(logger, field_name="update_response_code", actual=response.response_code, expected=200, response=response)""")
        + block(3, "Get user details and verify updated fields", "Verify updated fields",
                """response = await get_user_by_email(api_client, updated_payload["email"])\nuser = response.body_json.get("user", {})\nassert_api_field_equal(logger, field_name="updated_name", actual=user.get("name"), expected=updated_payload["name"], response=response)\nassert_api_field_equal(logger, field_name="updated_city", actual=user.get("city"), expected=updated_payload["city"], response=response)""")
        + block(4, "Delete updated account as cleanup", "Cleanup updated account",
                """response = await delete_user(api_client, updated_payload["email"], updated_payload["password"])\nassert_api_field_equal(logger, field_name="cleanup_response_code", actual=response.response_code, expected=200, response=response)""")
    )

    cases[25] = wrap_test(
        25, "Deleted user cannot verify login", "Account Lifecycle",
        "test_api_case_25_deleted_user_cannot_verify_login",
        {"scenario_1": "Create a new account", "scenario_2": "Delete created account", "scenario_3": "Verify deleted user no longer exists for login"},
        """    test_name = "test_api_case_25_deleted_user_cannot_verify_login"\n    created_payload = {}\n\n"""
        + block(1, "Create a new account", "Create account",
                """nonlocal created_payload\ncreated_payload, response = await create_user(api_client, test_record["user_template"])\nassert_api_field_equal(logger, field_name="create_response_code", actual=response.response_code, expected=201, response=response)""")
        + block(2, "Delete created account", "Delete account",
                """response = await delete_user(api_client, created_payload["email"], created_payload["password"])\nassert_api_field_equal(logger, field_name="delete_response_code", actual=response.response_code, expected=200, response=response)""")
        + block(3, "Verify deleted user no longer exists for login", "Verify deleted user login fails",
                """response = await api_client.post(VERIFY_LOGIN, form={"email": created_payload["email"], "password": created_payload["password"]})\nassert_api_field_equal(logger, field_name="response_code", actual=response.response_code, expected=404, response=response)\nassert_api_field_equal(logger, field_name="message", actual=response.message, expected="User not found!", response=response)""")
    )

    cases[26] = wrap_test(
        26, "Search product with secondary term", "Search Product API",
        "test_api_case_26_search_product_secondary_term",
        {"scenario_1": "Send POST request to search product API using secondary search term and verify successful response"},
        """    test_name = "test_api_case_26_search_product_secondary_term"\n\n"""
        + block(1, "Send POST request to search product API using secondary search term and verify successful response", "Search product with secondary term",
                """response = await api_client.post(SEARCH_PRODUCT, form={"search_product": test_record["search_product_secondary"]})\nassert_api_field_equal(logger, field_name="response_code", actual=response.response_code, expected=200, response=response)\nassert_api_truthy(logger, field_name="secondary_search_results", actual=response.body_json.get("products"), response=response)""")
    )

    for case_no, content in cases.items():
        (base / filenames[case_no]).write_text(HEADER + content, encoding="utf-8")

    print(f"Created {len(cases)} files in {base}")


if __name__ == "__main__":
    main()
