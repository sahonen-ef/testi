*** Settings ***
Library    RequestsLibrary
Library    Collections

*** Variables ***
${BASE_URL}    http://flask_app:5000

*** Test Cases ***
API Test - Get Main Page
    [Tags]    api    smoke
    Create Session    flask_session    ${BASE_URL}
    ${response}=    GET On Session    flask_session    /
    Should Be Equal As Numbers    ${response.status_code}    200
    Should Contain    ${response.text}    Finnish Midweek Holidays

API Test - Post Valid Year English
    [Tags]    api    english
    Create Session    flask_session    ${BASE_URL}
    ${data}=    Create Dictionary    year=2025    lang=en
    ${response}=    POST On Session    flask_session    /    data=${data}
    Should Be Equal As Numbers    ${response.status_code}    200
    Should Contain    ${response.text}    In 2025, there are
    Should Contain    ${response.text}    Good Friday

API Test - Post Valid Year Finnish
    [Tags]    api    finnish
    Create Session    flask_session    ${BASE_URL}
    ${data}=    Create Dictionary    year=2025    lang=fi
    ${response}=    POST On Session    flask_session    /    data=${data}
    Should Be Equal As Numbers    ${response.status_code}    200
    Should Contain    ${response.text}    Vuonna 2025 on
    Should Contain    ${response.text}    Pitkäperjantai

API Test - Post Invalid Year
    [Tags]    api    validation
    Create Session    flask_session    ${BASE_URL}
    ${data}=    Create Dictionary    year=abc    lang=en
    ${response}=    POST On Session    flask_session    /    data=${data}
    Should Be Equal As Numbers    ${response.status_code}    200
    Should Contain    ${response.text}    Please enter a valid integer year

API Test - Post Out Of Range Year
    [Tags]    api    validation
    Create Session    flask_session    ${BASE_URL}
    ${data}=    Create Dictionary    year=1800    lang=en
    ${response}=    POST On Session    flask_session    /    data=${data}
    Should Be Equal As Numbers    ${response.status_code}    200
    Should Contain    ${response.text}    Please enter a valid year between 1900 and 2100

*** Keywords ***
Setup Test Session
    Create Session    flask_session    ${BASE_URL}

Teardown Test Session
    Delete All Sessions