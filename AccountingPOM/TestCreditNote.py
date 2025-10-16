import time
from AccountingPOM.CreditNote import CreditNotePage

def main():
    login = CreditNotePage()
    login.open()
    login.enter_username("Paras")
    login.enter_password("Ims@1234")
    login.click_signin()
    time.sleep(3)

    login.handle_duplicate_logout()
    login.open_accounting_module()
    login.open_credit_note()

if __name__ == "__main__":
    main()
