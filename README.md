# open_banking_prometeo

## [Prometeo API](https://docs.prometeoapi.com/reference/login)

```bash
sudo pip3 install virtualenv

virtualenv pyvenv

source aws/pyvenv/bin/activate

pip freeze > requirements.txt
pip install requirements.txt

pip freeze
pip list

python3 main.py

deactivate
```




Create API
- Calls Prometeo's API and writes to a propetary db
- A Frontend app will make calls to retrieve data from propetary db (not prometeo)
- user should only be able to
  -  change the category of the transaction
  -  change frequency of the transaction -> recurrent (one-time, daily, weekly, monthly, every 3 months, yearly, etc)
  -  change note
- user shouldn't be able to add a transaction
- Frontend -> Streamlit
  - https://retool.com/integrations/rest-api
  - React ?
- Transactional DB
  - account
    - id_account
    - number
    - name
    - type (savings, checking, credit card, investment, loan, property, asset)
    - is_connected (T/F) -> automatic with an open banking solution like prometeo
    - currency
    - balance
    - due_date (credit card, loan)
    - raw (json)
  - transaction
    - id_transaction
    - id_account
    - date
    - amount (expense -> negative | income -> positive)
    - reference
    - detail
    - extra_data
    - notes
    - tag
    - subcategory_id
  - category
    - category_id
    - name
    - type (needs, wants, savings)
  - subcategory
    - subcategory_id
    - category_id
    - name
    - type (needs, wants, savings)