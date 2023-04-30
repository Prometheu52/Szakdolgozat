import re
import getpass
from enum import Enum
from log import *


class PW_strength(Enum):
  AVG = 0
  STRICT = 1
  ZERO = 2


def create_passwd(strength: PW_strength, prompt="Account password: ") -> str:
    while True:
      first = getpass.getpass(prompt)
      validation_result = True
      if strength != PW_strength.ZERO:
        validation_result = password_validation(first) if strength == PW_strength.AVG else password_validation_strong(first)

      if validation_result:
        second = getpass.getpass("Confirm password: ")
        if first == second:
          return first
        
        log(Log.WARN, "Passwords does not macth! Try again!")
      else:
        l = "6" if strength == PW_strength.AVG else "8"
        sp = "Optional" if strength == PW_strength.AVG else "Requiered"
        log(Log.WARN, 
        f"The password has to be at least {l} characters long and needs at least one Uppercase and lowecase letter and a number.\nSpecial charaters are {sp}")

def ask() -> PW_strength:
    strength = PW_strength.ZERO

    log(Log.INFO, "Do you want to setup password strength validatior?")
    log(Log.INFO, "    For MODERATE setting type: \'1\'")
    log(Log.INFO, "      For STRICT setting type: \'2\'")
    log(Log.INFO, "    Othervise leave the input empty.")
    match input("Strength: ").strip().lower():
        case "1":
            strength = PW_strength.AVG
            log(Log.INFO, "This setting requieres at least 6 characters with both, upper and lowecase english letters with at least one number")
        case "2":
            strength = PW_strength.STRICT
            log(Log.INFO, "This setting requieres at least 8 characters with both, upper and lowecase english letters with at least one number and one special character")
    
    return strength

# At least 8 chars with special char
def password_validation_strong(passwd: str) -> bool:
  password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
  return re.match(password_pattern, passwd) is not None


# At least 6 chars without special char
def password_validation(passwd: str) -> bool:
  password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{6,}$"
  return re.match(password_pattern, passwd) is not None

