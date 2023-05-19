import os
from dotenv import load_dotenv
import requests
from datetime import datetime
from typing import Dict, List


class PrometeoAuth:
    def __init__(self, api_key: str, base_url: str) -> None:
        self.api_key = api_key
        self.base_url = base_url
        self.session_key = self.get_session_key()

    def login(self) -> Dict:
        url = f"{self.base_url}/login/"
        data = {"provider": "test", "username": "12345", "password": "gfdsa"}
        headers = {"X-API-Key": self.api_key}
        response = requests.post(url, data=data, headers=headers)
        if response.ok:
            return response.json()

    def get_session_key(self) -> str:
        login_data: Dict = self.login()
        return login_data.get("key")

    def logout(self) -> bool:
        url = f"{self.base_url}/logout/"
        params = {"key": self.session_key}
        headers = {"X-API-Key": self.base_url}
        response = requests.get(url, params=params, headers=headers)
        return response.ok


class PrometeoData:
    def __init__(self, api_key: str, base_url: str, session_key: str) -> None:
        self.api_key = api_key
        self.base_url = base_url
        self.session_key = session_key

    def get_info_user(self) -> Dict:
        url = f"{self.base_url}/info/"
        params = {"key": self.session_key}
        headers = {"X-API-Key": self.api_key}
        response = requests.get(url, params=params, headers=headers)
        if response.ok:
            return response.json().get("info", [])

    def get_accounts(self) -> List[Dict]:
        url = f"{self.base_url}/account/"
        params = {"key": self.session_key}
        headers = {"X-API-Key": self.api_key}
        response = requests.get(url, params=params, headers=headers)
        if response.ok:
            return response.json().get("accounts", [])

    def get_account_movements(
        self,
        account_number: str,
        currency: str,
        date_start: datetime,
        date_end: datetime,
    ) -> List[Dict]:
        url = f"{self.base_url}/account/{account_number}/movement/"
        params = {
            "accountNumber": account_number,
            "currency": currency,
            "date_start": date_start.strftime("%d/%m/%Y"),
            "date_end": date_end.strftime("%d/%m/%Y"),
            "key": self.session_key,
        }
        headers = {"X-API-Key": self.api_key}
        response = requests.get(url, params=params, headers=headers)
        if response.ok:
            return response.json().get("movements", [])
    
    def get_credit_cards(self) -> List[Dict]:
        url = f"{self.base_url}/credit-card/"
        params = {"key": self.session_key}
        headers = {"X-API-Key": self.api_key}
        response = requests.get(url, params=params, headers=headers)
        if response.ok:
            return response.json().get("credit_cards", [])

    def get_credit_card_movements(
        self,
        card_number: str,
        currency: str,
        date_start: datetime,
        date_end: datetime,
    ) -> List[Dict]:
        url = f"{self.base_url}/credit-card/{card_number}/movements"
        params = {
            "card_number": card_number,
            "currency": currency,
            "date_start": date_start.strftime("%d/%m/%Y"),
            "date_end": date_end.strftime("%d/%m/%Y"),
            "key": self.session_key,
        }
        headers = {"X-API-Key": self.api_key}
        response = requests.get(url, params=params, headers=headers)
        if response.ok:
            return response.json().get("movements", [])


def main():
    load_dotenv()
    api_key = os.getenv("API_KEY")
    base_url = "https://banking.sandbox.prometeoapi.com"
    prometeo_auth = PrometeoAuth(api_key=api_key, base_url=base_url)
    prometeo_data = PrometeoData(
        api_key=api_key, base_url=base_url, session_key=prometeo_auth.session_key
    )
    start_date = datetime.now().replace(day=1, month=5)
    end_date = datetime.now()
    
    info_user: Dict = prometeo_data.get_info_user()
    print("info_user:", info_user)
    
    accounts: List[Dict] = prometeo_data.get_accounts()
    print("accounts:", accounts)

    credit_cards: List[Dict] = prometeo_data.get_credit_cards()
    print("credit_cards:", credit_cards)

    movements_data = {}
    for account in accounts:
        account_number = account.get("number")
        movements_data[account_number] = prometeo_data.get_account_movements(
            account_number,
            account.get("currency", "USD"),
            start_date,
            end_date
        )
    for credit_card in credit_cards:
        card_number = credit_card.get("number")
        movements_data[card_number] = prometeo_data.get_credit_card_movements(
            card_number,
            credit_card.get("currency", "USD"),
            start_date,
            end_date
        )

    accounts_expenses = {}
    accounts_credits = {}
    for account_number, movements in movements_data.items():
        for movement in movements:
            if debit := movement.get("debit"):
                accounts_expenses[account_number] = (
                    accounts_expenses.get(account_number, 0) + debit
                )
            if credit := movement.get("credit"):
                accounts_credits[account_number] = (
                    accounts_credits.get(account_number, 0) + credit
                )
    print("accounts_expenses", accounts_expenses)
    print("accounts_credits", accounts_credits)
    prometeo_auth.logout()

if __name__ == "__main__":
    main()
