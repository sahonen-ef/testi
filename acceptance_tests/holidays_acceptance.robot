*** Settings ***
Library    Browser

*** Test Cases ***
Midweek Holidays in English
    [Tags]    smoke    english
    Given User opens the application
    When User enters year and language    2025    en
    Then User sees working day holidays for year    2025
    And User should see holiday name    Good Friday
    [Teardown]    Close Browser

Midweek Holidays in Finnish
    [Tags]    smoke    finnish
    Given User opens the application
    When User enters year and language    2025    fi
    Then User sees working day holidays for Finnish year    2025
    And User should see holiday name    Pitkäperjantai
    [Teardown]    Close Browser

Past Year Holidays
    [Tags]    regression    english
    Given User opens the application
    When User enters year and language    2020    en
    Then User sees working day holidays for year    2020
    And User should see holiday name    Christmas Day
    [Teardown]    Close Browser

Future Year Holidays
    [Tags]    regression    english
    Given User opens the application
    When User enters year and language    2030    en
    Then User sees working day holidays for year    2030
    And User should see holiday name    New Year's Day
    [Teardown]    Close Browser

*** Keywords ***
User opens the application
    New Browser    chromium
    New Page    http://flask_app:5000

User enters year
    [Arguments]    ${year}
    Fill Text    input[name="year"]    ${year}
    Press Keys    input[name="year"]    Enter

User enters year and language
    [Arguments]    ${year}    ${lang}
    Fill Text    input[name="year"]    ${year}
    Select Options By    select[name="lang"]    value    ${lang}
    Click    button[type="submit"]

User enters invalid year
    [Arguments]    ${invalid_value}
    Fill Text    input[name="year"]    ${invalid_value}
    Click    button[type="submit"]
    


User sees working day holidays for year
    [Arguments]    ${year}
    ${body_text}=    Get Text    css=body
    Should Contain    ${body_text}    In ${year}, there are

User sees working day holidays for Finnish year
    [Arguments]    ${year}
    ${body_text}=    Get Text    css=body
    Should Contain    ${body_text}    Vuonna ${year} on

User should see holiday name
    [Arguments]    ${holiday_name}
    ${body_text}=    Get Text    css=body
    Should Contain    ${body_text}    ${holiday_name}

User should see error message
    ${body_text}=    Get Text    css=body
    Should Contain Any    ${body_text}    error    Error    invalid    Invalid    Please enter

Close Browser
    Browser.Close Browser
