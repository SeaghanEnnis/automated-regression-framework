import requests
import json
     
def not_found_validation(site_id):
    with open('environment.json', 'r') as file:
        data = json.load(file)
        data_url = (data['host']).replace("env", data['env']) + data["dataPath"]
        
    url = data_url + site_id
    data_headers = {'Content-Type': 'application/json','Authorization': 'Bearer Bad-token'}
    response = requests.get(url, headers=data_headers)
    
   
    assert response.status_code == 401, "Response is Not Auth"
    assert response.text != "", "Body is returned"

    
def test_run_data_bad_token():
    not_found_validation("HOHOU00122A")

def test_run_data_bad_token_fake_site():
    not_found_validation("ABCDE")


    
