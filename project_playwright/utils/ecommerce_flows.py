from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.registration_page import RegistrationPage
from utils.test_data_factory import build_unique_email


async def register_new_user(page, env, record):
    home_page = HomePage(page)
    registration_page = RegistrationPage(page)

    email = build_unique_email(record["email_template"])
    await home_page.navigate(env["base_url"])
    await home_page.go_to_signup_login()
    await registration_page.new_user_signup(record["name"], email)
    await registration_page.enter_account_information(
        password=record["password"],
        day=record["day"],
        month=record["month"],
        year=record["year"],
    )
    await registration_page.enter_address_information(
        first_name=record["first_name"],
        last_name=record["last_name"],
        company=record["company"],
        address=record["address"],
        address_2=record["address_2"],
        country=record["country"],
        city=record["city"],
        state=record["state"],
        zipcode=record["zipcode"],
        mobile_number=record["mobile_number"],
    )
    return email


async def login_existing_user(page, env):
    home_page = HomePage(page)
    login_page = LoginPage(page)

    await home_page.navigate(env["base_url"])
    await home_page.go_to_signup_login()
    await login_page.login(env["username"], env["password"])


async def add_first_product_to_cart(page, env):
    home_page = HomePage(page)
    products_page = ProductsPage(page)

    await home_page.navigate(env["base_url"])
    await home_page.go_to_products()
    await products_page.add_product_to_cart(0)
    await products_page.view_cart_from_modal()


async def add_two_products_to_cart(page, env):
    home_page = HomePage(page)
    products_page = ProductsPage(page)

    await home_page.navigate(env["base_url"])
    await home_page.go_to_products()
    await products_page.add_product_to_cart(0)
    await products_page.continue_shopping()
    await products_page.add_product_to_cart(2)
    await products_page.view_cart_from_modal()
