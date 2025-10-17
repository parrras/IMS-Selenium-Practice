import time
from AccountingPOM.DebitNote import DebitNotePage

def main():
    login = DebitNotePage()
    login.open()
    login.enter_username("Paras")
    login.enter_password("Ims@1234")
    login.click_signin()
    time.sleep(3)

    login.handle_duplicate_logout()
    login.open_accounting_module()
    login.open_debit_note()
    login.edit_debit_note()
    login.view_debit_note()

if __name__ == "__main__":
    main()
