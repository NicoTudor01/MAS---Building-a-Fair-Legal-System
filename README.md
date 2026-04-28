# Building a Fair Legal System Through A Multi-Agent System

## How to use:

### 1. Activate virtual envirnment if not active:
  On controller:
   ```
   source ~/.venv/bin/activate
   ```
### 2. Run the main script from controller with 4 options:
__Fraud:__  
   One round:
   ```
   python main.py --case fraud --voting plurality
   ```
   Communication (plurality):
   ```
   python main.py --case fraud --voting plurality --communicate
   ```
   Communication (social welfare):
   ```
   python main.py --case fraud --voting social_welfare --communicate
   ```
   Communication (tournament):
   ```
   python main.py --case fraud --voting tournament --communicate
   ```
   Communication (slater):
   ```
   python main.py --case fraud --voting slater --communicate
   ```
__Tax Evasion:__  
   One round:
   ```
   python main.py --case tax_evasion --voting plurality
   ```
   Communication (plurality):
   ```
   python main.py --case tax_evasion --voting plurality --communicate
   ```
   Communication (social welfare):
   ```
   python main.py --case tax_evasion --voting social_welfare --communicate
   ```
   Communication (tournament):
   ```
   python main.py --case tax_evasion --voting tournament --communicate
   ```
   Communication (slater):
   ```
   python main.py --case tax_evasion --voting slater --communicate
   ```
__Defamation:__  
   One round:
   ```
   python main.py --case defamation --voting plurality
   ```
   Communication (plurality):
   ```
   python main.py --case defamation --voting plurality --communicate
   ```
   Communication (social welfare):
   ```
   python main.py --case defamation --voting social_welfare --communicate
   ```
   Communication (tournament):
   ```
   python main.py --case defamation --voting tournament --communicate
   ```
   Communication (slater):
   ```
   python main.py --case defamation --voting slater --communicate
   ```
__Larceny:__  
   One round:
   ```
   python main.py --case larceny --voting plurality
   ```
   Communication (plurality):
   ```
   python main.py --case larceny --voting plurality --communicate
   ```
   Communication (social welfare):
   ```
   python main.py --case larceny --voting social_welfare --communicate
   ```
   Communication (tournament):
   ```
   python main.py --case larceny --voting tournament --communicate
   ```
   Communication (slater):
   ```
   python main.py --case larceny --voting slater --communicate
   ```
__Perjury:__  
   One round:
   ```
   python main.py --case perjury --voting plurality
   ```
