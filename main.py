from getpass import getpass
from analyzer import ananlyze_password
from pattern_detector import isWeakPassword, loadCommonPasswords
from entropy import calculate_entropy
from breach_checker import check_breach_flag
password =  getpass("Enter your password: ")

if not password:
    print("Please Enter a valid Password!!")
    
commonPassword = loadCommonPasswords()

if password:
    
    ananlyze_password(password)
    isWeakPassword(password,commonPassword)
    calculate_entropy(password)
    check_breach_flag(password)