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
    Should Contain    ${response.text}    Midweek Holidays

API Test - Post Valid Year English
    [Tags]    api    english    finland
    Create Session    flask_session    ${BASE_URL}
    ${data}=    Create Dictionary    year=2025    lang=en    country=fi
    ${response}=    POST On Session    flask_session    /    data=${data}
    Should Be Equal As Numbers    ${response.status_code}    200
    Should Contain    ${response.text}    In 2025, there are
    Should Contain    ${response.text}    Good Friday

API Test - Post Valid Year Finnish
    [Tags]    api    finnish    finland
    Create Session    flask_session    ${BASE_URL}
    ${data}=    Create Dictionary    year=2025    lang=fi    country=fi
    ${response}=    POST On Session    flask_session    /    data=${data}
    Should Be Equal As Numbers    ${response.status_code}    200
    Should Contain    ${response.text}    Vuonna 2025 on
    Should Contain    ${response.text}    Pitkäperjantai

API Test - Swedish Holidays in Swedish
    [Tags]    api    swedish    sweden
    Create Session    flask_session    ${BASE_URL}
    ${data}=    Create Dictionary    year=2025    lang=sv    country=se
    ${response}=    POST On Session    flask_session    /    data=${data}
    Should Be Equal As Numbers    ${response.status_code}    200
    Should Contain    ${response.text}    År 2025 finns det
    Should Contain    ${response.text}    Långfredag

API Test - Swedish Holidays in English
    [Tags]    api    english    sweden
    Create Session    flask_session    ${BASE_URL}
    ${data}=    Create Dictionary    year=2025    lang=en    country=se
    ${response}=    POST On Session    flask_session    /    data=${data}
    Should Be Equal As Numbers    ${response.status_code}    200
    Should Contain    ${response.text}    In 2025, there are
    Should Contain    ${response.text}    Swedish National Day

API Test - Norwegian Holidays in Norwegian
    [Tags]    api    norwegian    norway
    Create Session    flask_session    ${BASE_URL}
    ${data}=    Create Dictionary    year=2027    lang=no    country=no
    ${response}=    POST On Session    flask_session    /    data=${data}
    Should Be Equal As Numbers    ${response.status_code}    200
    Should Contain    ${response.text}    I 2027 er det
    Should Contain    ${response.text}    Langfredag

API Test - Norwegian Holidays in English
    [Tags]    api    english    norway
    Create Session    flask_session    ${BASE_URL}
    ${data}=    Create Dictionary    year=2027    lang=en    country=no
    ${response}=    POST On Session    flask_session    /    data=${data}
    Should Be Equal As Numbers    ${response.status_code}    200
    Should Contain    ${response.text}    In 2027, there are
    Should Contain    ${response.text}    Constitution Day

API Test - Estonian Holidays in Estonian
    [Tags]    api    estonian    estonia
    Create Session    flask_session    ${BASE_URL}
    ${data}=    Create Dictionary    year=2025    lang=et    country=ee
    ${response}=    POST On Session    flask_session    /    data=${data}
    Should Be Equal As Numbers    ${response.status_code}    200
    Should Contain    ${response.text}    Aastal 2025 on
    Should Contain    ${response.text}    Suur reede

API Test - Estonian Holidays in English
    [Tags]    api    english    estonia
    Create Session    flask_session    ${BASE_URL}
    ${data}=    Create Dictionary    year=2025    lang=en    country=ee
    ${response}=    POST On Session    flask_session    /    data=${data}
    Should Be Equal As Numbers    ${response.status_code}    200
    Should Contain    ${response.text}    In 2025, there are
    Should Contain    ${response.text}    Independence Day

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