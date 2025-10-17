import time
from contraVoucher import ContraVoucherPage

def main():
    login = ContraVoucherPage()
    login.open()
    login.enter_username("Paras")
    login.enter_password("Ims@1234")
    login.click_signin()
    time.sleep(3)

    login.handle_duplicate_logout()
    login.open_accounting_module()
    login.open_contra_voucher()
    login.edit_contra_voucher()
    login.view_delete_contra_voucher()

if __name__ == "__main__":
    main()
