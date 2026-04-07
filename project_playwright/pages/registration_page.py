from playwright.async_api import Page
from locators.registration.registration_locator import RegistrationLocator

class RegistrationPage:
    def __init__(self,page:Page):
        self.page = page
        self.locators = RegistrationLocator()

    async def navigate(self , url:str):
        await self.page.goto(url)

    async def navigate_to_signup_login(self):
        element = self.page.get_by_role(self.locators.SIGNUP_BUTTON_ROLE,name = self.locators.SIGNUP_BUTTON_NAME)
        await element.wait_for(state = 'visible')
        await element.click()

    async def new_user_signup(self,username:str , useremail:str ):
        await self.page.locator(self.locators.REGISTER_NAME_TEXTBOX).fill(username)
        await self.page.locator(self.locators.REGISTER_EMAIL_TEXTBOX).fill(useremail)
        await self.page.get_by_role(self.locators.SIGNUP_BUTTON_ROLE , name = self.locators.SIGNUP_BUTTON_NAME).click()
        # wait for page to load after button click 
        await self.page.wait_for_load_state("domcontentloaded")
    
    async def information_page_visible(self) -> bool:
        information_page_element = self.page.get_by_text(self.locators.ENTER_ACCOUNT_INFORMATION_TEXT)
        return await information_page_element.is_visible()
    
    async def enter_account_information(self,password:str , day:str , month:str , year:str):
        await self.page.locator(self.locators.PASSWORD_TEXTBOX).fill(password)
        await self.page.locator(self.locators.DAYS_DROPDOWN_ID).select_option(day)
        await self.page.locator(self.locators.MONTHS_DROPDOWN_ID).select_option(month)
        await self.page.locato(self.locators.YEARS_DROPDOWN_ID).select_option(year)
        await self.page.locator(self.locators.NEWSLETTER_CHECKBOX_ID).check()
        await self.page.locator(self.locators.SPECIAL_OFFER_CHECKBOX_ID).check()

    async def enter_address_information(self,first_name:str , last_name:str , company:str , address:str , address_2:str, country:str, city:str ,state:str , zipcode:int , mobile_number:int):
        await self.page.locator(self.locators.FIRST_NAME_TEXTBOX).fill(first_name)
        await self.page.locator(self.locators.LAST_NAME_TEXTBOX).fill(last_name)
        await self.page.locator(self.locators.COMPANY_TEXTBOX).fill(company)
        await self.page.locator(self.locators.ADDRESS_TEXTBOX).fill(address)
        await self.page.locator(self.locators.ADDRESS_2_TEXTBOX).fill(address_2)
        await self.page.locator(self.locators.COUNTRY_DROPDOWN_ID).select_option(country)
        await self.page.locator(self.locators.STATE_TEXTBOX).fill(state)
        await self.page.locator(self.locators.CITY_TEXTBOX).fill(city)
        await self.page.locator(self.locators.STATE_TEXTBOX).fill(state)
        await self.page.locator(self.locators.ZIPCODE_TEXTBOX).fill(str(zipcode))
        await self.page.locator(self.locators.MOBILE_NUMBER_TEXTBOX).fill(str(mobile_number))
        await self.page.get_by_role(self.locators.CREATE_ACCOUNT_BUTTOM_ROLE , name = self.locators.CREATE_ACCOUNT_BUTTOM_NAME).click()

    async def account_created_text_visible(self) -> bool:
        account_created_text = self.page.get_by_text(self.locators.ACCOUNT_CREATED_MESSAGE)
        return await account_created_text.is_visible()
        
    async def click_on_continue_button(self):
        await self.page.get_by_role(self.locators.CONTINUE_BUTTON_ROLE, name=self.locators.CONTINUE_ACCOUNT_BUTTON_NAME).click()
        
    async def is_logged_in(self) -> bool:
        logged_in_element = self.page.get_by_text(self.locators.LOG_IN_TEXT)
        return await logged_in_element.is_visible()
    
    async def delete_account_process(self):
        await self.page.get_by_role(self.locators.DELETE_ACCOUNT_ROLE , name = self.locators.DELETE_ACCOUNT_NAME).click()
        await self.page.locator(self.locators.ACCOUNT_DELETED_MESSAGE).is_visible()
        await self.page.get_by_role(self.locators.DELETE_ACCOUNT_CONTINUE_BUTTON_ROLE , name = self.locators.DELETE_ACCOUNT_CONTINUE_BUTTON_NAME).click()
        




