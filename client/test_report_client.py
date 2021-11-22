import urllib3
import json

http = urllib3.PoolManager()
url = "https://heroku-test-report-api.herokuapp.com/api/v1"
token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlZrYXJ4RUY5bm1NakpJTElQTURfZiJ9.eyJpc3MiOiJodHRwczovL2Rldi0zcmltdnQ4NC51cy5hdXRoMC5jb20vIiwic3ViIjoid2czNWZycnUyOEd5OUxGRnhOdmVIa3dTSVRkSG1OcnRAY2xpZW50cyIsImF1ZCI6InRlc3QtcmVwb3J0LWF1dGgiLCJpYXQiOjE2Mzc1MzgxNDEsImV4cCI6MTYzNzYyNDU0MSwiYXpwIjoid2czNWZycnUyOEd5OUxGRnhOdmVIa3dTSVRkSG1OcnQiLCJzY29wZSI6ImFwaSIsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyJ9.JZTV1AeWXLQiRpPvj-Ng-uT85rhM8Crsgro3eR-FdMAnicofRemMzxdNTjarR0oyE7SpserYg8d5Ia8L7Yc3TfVIRdIDqazzjSoGXpus8EX6bfLdh9SLwqyBwxIpWEVWrmSj34cqpnKb3_TaTxTpvhOsqjK5GNKVT5tkK5t1Sc8Lgmg-K-CbRosSfjmiVvYBoAB315jd7j0XtUTiKC9bT8mT5GFgkPOORnfMKeUMsf0j0uVYahvs3Shdd3dnSxcjDIIjQOu9P6BlkBFYRsyhqh-Em-dkTOU3xZRfVjp8BkH8GdsDb2cinphl0VLw2AVWqe4N24EospBO4hTN-ZMgBQ"

header = {'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + token}

def get_projects():
    response = http.request(
        method='GET',
        url=url + '/projects',
        headers=header
    )
    return json.loads(response.data.decode('utf-8'))

def get_test_runs(project_id):
    response = http.request(
        method='GET',
        url=url + '/results/' + project_id,
        headers=header
    )
    return json.loads(response.data.decode('utf-8'))

def set_test_stability():
    stability_data_list = []
    stability_response_list = []
    test_projects = get_projects()
    for project in test_projects:
        test_runs = get_test_runs(project["id"])

        sum_total_case = 0
        sum_passed_case = 0
        sum_duration = 0

        for test_run in test_runs:
            sum_total_case += test_run["testTotal"]
            sum_passed_case += test_run["testPassed"]
            sum_duration += test_run["duration"]

        data = {
            "id": project["id"],
            "name": project["name"],
            "platform": "Desktop",
            "successRate": sum_passed_case/sum_total_case,
            "totalRuns": len(test_runs),
            "totalDuration": sum_duration
        }
        stability_data_list.append(data)

    for data in stability_data_list:
        encoded_data = json.dumps(data).encode('utf-8')
        response = http.request(
            method='POST',
            url=url + '/stability',
            body=encoded_data,
            headers=header
        )
        stability_response_list.append(json.loads(response.data.decode('utf-8')))

    return stability_response_list