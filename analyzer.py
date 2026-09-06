import re

def ananlyze_password(password):
    
    length= len(password)
    
    hasUppper = bool(re.search(r"[A-Z]", password))
    hasLower = bool(re.search(r"[a-z]", password))
    hasDigit = bool(re.search(r"[0-9]", password))
    hasSpecial = bool(re.search(r"[^A-Za-z0-9]", password))
    
    points=0
    
    if len>=12:
        points+=3
    elif len>=8:
        points+=2
    elif len>=8:
        points+=1
    
    if hasUppper:
        points+=1
    if hasLower:
        points+=1    
    if hasDigit:
        points+=1
    if hasSpecial:
        points+=1
    
    if points>=7:
        very_strong=True
    elif points>=6:
        strong=True
    elif points>=4:
        moderate=True
    else:
        weak=True
