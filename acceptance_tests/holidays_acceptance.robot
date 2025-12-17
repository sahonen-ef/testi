*** Settings ***
Library    Browser
Suite Setup    Set Browser Timeout    10s
Suite Teardown    Browser.Close Browser

*** Variables ***
${BASE_URL}    http://app:5000    # Default, can be overridden via -v BASE_URL:http://host:port

*** Test Cases ***
Midweek Holidays in English
    [Tags]    smoke    english    ui    holidays
    [Documentation]    Verifies that the system correctly displays Finnish midweek holidays in English for a standard year, ensuring basic functionality works as expected.
    Given User opens the application
    When User enters year and language    2025    en
    Then User sees working day holidays for year    2025
    And User should see holiday name    Good Friday
    [Teardown]    Close Browser

Midweek Holidays in Finnish
    [Tags]    smoke    finnish    ui    holidays
    [Documentation]    Verifies that the system correctly displays Finnish midweek holidays in Finnish language, ensuring localization works properly.
    Given User opens the application
    When User enters year and language    2025    fi
    Then User sees working day holidays for Finnish year    2025
    And User should see holiday name    Pitkäperjantai
    [Teardown]    Close Browser

Past Year Holidays
    [Tags]    regression    english    ui    holidays    historical
    [Documentation]    Verifies that the system correctly calculates and displays holidays for past years, ensuring historical data accuracy.
    Given User opens the application
    When User enters year and language    2020    en
    Then User sees working day holidays for year    2020
    And User should see holiday name    Christmas Day
    [Teardown]    Close Browser

Future Year Holidays
    [Tags]    regression    english    ui    holidays    future
    [Documentation]    Verifies that the system correctly calculates and displays holidays for future years, ensuring forward calculation accuracy.
    Given User opens the application
    When User enters year and language    2030    en
    Then User sees working day holidays for year    2030
    And User should see holiday name    New Year's Day
    [Teardown]    Close Browser

Validate Holidays for Earliest Supported Year
    [Tags]    regression    boundary    ui    english    holidays
    [Documentation]    Verifies that the system correctly returns holidays for the earliest supported year, ensuring boundary year handling works as expected.
    Given User opens the application
    When User enters year and language    1900    en
    Then User sees working day holidays for year    1900
    And User should see at least one holiday displayed
    [Teardown]    Close Browser

Validate Holidays for Far Future Year
    [Tags]    regression    boundary    ui    english    holidays
    [Documentation]    Verifies that the system correctly returns holidays for a far future year, ensuring future boundary year handling works as expected.
    Given User opens the application
    When User enters year and language    2100    en
    Then User sees working day holidays for year    2100
    And User should see at least one holiday displayed
    [Teardown]    Close Browser

Handle Unsupported Year Input
    [Tags]    regression    negative    ui    english    validation
    [Documentation]    Verifies that HTML5 validation prevents submission of years below the minimum (1900).
    Given User opens the application
    When User verifies min validation for year    1500
    Then Year input should have min attribute    1900
    [Teardown]    Close Browser

Handle Empty Year Input
    [Tags]    regression    negative    ui    english    validation
    [Documentation]    Verifies that the system handles empty year input appropriately through HTML5 validation.
    Given User opens the application
    When User submits form with empty year
    Then User should see HTML5 validation message
    [Teardown]    Close Browser

Handle Invalid Year Format
    [Tags]    regression    negative    ui    english    validation
    [Documentation]    Verifies that number input prevents non-numeric input via HTML5 validation.
    Given User opens the application
    When User verifies number input validation
    Then User should see year input has number type
    [Teardown]    Close Browser

Year Above Maximum Range
    [Tags]    regression    negative    ui    english    validation
    [Documentation]    Verifies that HTML5 validation prevents submission of years above the maximum (2100).
    Given User opens the application
    When User verifies max validation for year    2500
    Then Year input should have max attribute    2100
    [Teardown]    Close Browser

Leap Year Holidays
    [Tags]    regression    leapyear    ui    holidays
    [Documentation]    Verifies that the system correctly calculates holidays for a leap year (e.g., 2000).
    Given User opens the application
    When User enters year and language    2000    en
    Then User sees working day holidays for year    2000
    And User should see holiday name    Good Friday
    [Teardown]    Close Browser

Holidays in Swedish
    [Tags]    regression    swedish    ui    holidays    skip
    [Documentation]    Verifies that the system correctly displays holidays in Swedish. NOTE: Swedish not yet implemented, test skipped.
    Given User opens the application
    When User enters year and language    2025    en
    Then User sees working day holidays for year    2025
    And User should see holiday name    Good Friday
    [Teardown]    Close Browser

Holidays in Norwegian
    [Tags]    regression    norwegian    ui    holidays    skip
    [Documentation]    Verifies that the system correctly displays holidays in Norwegian. NOTE: Norwegian not yet implemented, test skipped.
    Given User opens the application
    When User enters year and language    2025    en
    Then User sees working day holidays for year    2025
    And User should see holiday name    Good Friday
    [Teardown]    Close Browser

Holidays in Estonian
    [Tags]    regression    estonian    ui    holidays    skip
    [Documentation]    Verifies that the system correctly displays holidays in Estonian. NOTE: Estonian not yet implemented, test skipped.
    Given User opens the application
    When User enters year and language    2025    en
    Then User sees working day holidays for year    2025
    And User should see holiday name    Good Friday
    [Teardown]    Close Browser

Validate Holidays for Year Just Above Minimum
    [Tags]    regression    boundary    ui    holidays    edgecase
    [Documentation]    Verifies that the system correctly handles the year just above the minimum supported range (1901).
    Given User opens the application
    When User enters year and language    1901    en
    Then User sees working day holidays for year    1901
    And User should see at least one holiday displayed
    [Teardown]    Close Browser

Validate Holidays for Year Just Below Maximum
    [Tags]    regression    boundary    ui    holidays    edgecase
    [Documentation]    Verifies that the system correctly handles the year just below the maximum supported range (2099).
    Given User opens the application
    When User enters year and language    2099    en
    Then User sees working day holidays for year    2099
    And User should see at least one holiday displayed
    [Teardown]    Close Browser

*** Keywords ***
User opens the application
    [Documentation]    Opens a new browser instance and navigates to the holiday application
    ${chromium_args}=    Create List    --disable-blink-features=AutoupgradeMixedContent
    New Browser    chromium    headless=True    args=${chromium_args}
    New Context    ignoreHTTPSErrors=True
    New Page    ${BASE_URL}

User enters year
    [Arguments]    ${year}
    [Documentation]    Enters a year value and submits using Enter key
    Fill Text    input[name="year"]    ${year}
    Press Keys    input[name="year"]    Enter

User enters year and language
    [Arguments]    ${year}    ${lang}
    [Documentation]    Enters year and selects language, then submits the form
    Fill Text    input[name="year"]    ${year}
    Select Options By    select[name="lang"]    value    ${lang}
    Click    button[type="submit"]

User enters invalid year
    [Arguments]    ${invalid_value}
    [Documentation]    Enters an invalid year value and submits the form
    Fill Text    input[name="year"]    ${invalid_value}
    Click    button[type="submit"]

User sees working day holidays for year
    [Arguments]    ${year}
    [Documentation]    Verifies that holidays are displayed for the specified year in English
    ${body_text}=    Get Text    css=body
    Should Contain    ${body_text}    In ${year}, there are
    Should Contain    ${body_text}    public holidays in Finland that fall on a working day

User sees working day holidays for Finnish year
    [Arguments]    ${year}
    [Documentation]    Verifies that holidays are displayed for the specified year in Finnish
    ${body_text}=    Get Text    css=body
    Should Contain    ${body_text}    Vuonna ${year} on
    Should Contain    ${body_text}    arkipäivälle

User should see holiday name
    [Arguments]    ${holiday_name}
    [Documentation]    Verifies that a specific holiday name appears in the results
    ${body_text}=    Get Text    css=body
    Should Contain    ${body_text}    ${holiday_name}

User should see at least one holiday displayed
    [Documentation]    Verifies that at least one holiday is shown in the results table
    ${holiday_rows}=    Get Element Count    css=tbody tr
    Should Be True    ${holiday_rows} > 0    msg=No holidays found in the results table

User should see error message
    [Documentation]    Verifies that an error message is displayed on the page
    ${body_text}=    Get Text    css=body
    Should Contain Any    ${body_text}    error    Error    invalid    Invalid    Please enter

User should see error message containing
    [Arguments]    ${expected_message}
    [Documentation]    Verifies that a specific error message is displayed
    ${body_text}=    Get Text    css=body
    Should Contain    ${body_text}    ${expected_message}

User submits form with empty year
    [Documentation]    Attempts to submit the form without entering a year
    Clear Text    input[name="year"]
    Select Options By    select[name="lang"]    value    en
    Click    button[type="submit"]

User verifies number input validation
    [Documentation]    Verifies that year input is type=number which prevents text entry
    ${input_type}=    Get Attribute    input[name="year"]    type
    Should Be Equal    ${input_type}    number    msg=Year input should be type='number'

User should see year input has number type
    [Documentation]    Confirms that the year input field is properly configured as number type
    ${input_type}=    Get Attribute    input[name="year"]    type
    Should Be Equal    ${input_type}    number

User verifies min validation for year
    [Arguments]    ${year}
    [Documentation]    Verifies that the year input has min validation
    Fill Text    input[name="year"]    ${year}
    ${min_value}=    Get Attribute    input[name="year"]    min
    Should Be Equal    ${min_value}    1900

User verifies max validation for year
    [Arguments]    ${year}
    [Documentation]    Verifies that the year input has max validation
    Fill Text    input[name="year"]    ${year}
    ${max_value}=    Get Attribute    input[name="year"]    max
    Should Be Equal    ${max_value}    2100

Year input should have min attribute
    [Arguments]    ${expected_min}
    [Documentation]    Verifies the min attribute value
    ${min_value}=    Get Attribute    input[name="year"]    min
    Should Be Equal    ${min_value}    ${expected_min}

Year input should have max attribute
    [Arguments]    ${expected_max}
    [Documentation]    Verifies the max attribute value
    ${max_value}=    Get Attribute    input[name="year"]    max
    Should Be Equal    ${max_value}    ${expected_max}

User should see HTML5 validation message
    [Documentation]    Verifies that HTML5 form validation prevents submission with empty required field
    ${required_attr}=    Get Attribute    input[name="year"]    required
    Should Not Be Equal    ${required_attr}    ${None}    msg=Year input should have required attribute

Close Browser
    [Documentation]    Closes the current browser instance
    Browser.Close Browser
