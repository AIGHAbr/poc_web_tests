dev_robot = """
Estou elaborando casos de teste usando o Robot Framework, uma framework de automação para desenvolvimento de testes de aceitação 
e ATDD (Desenvolvimento Guiado por Testes de Aceitação). Peço que você crie scripts no Robot Framework que reflitam essas interações. 
Siga as seguintes diretivas: 

* Escrita em Inglês: Todos os scripts devem ser escritos em inglês.
* Análise de Eventos: Utilize todos os eventos registrados nos logs para compreender as ações realizadas.
* Assertivas: Baseie-se nos eventos auxiliares, como 'change' e 'info', para criar verificações e assertivas que confirmem o comportamento esperado da aplicação.
* Caminho Feliz: Desenvolva scripts que cubram o fluxo principal de uso validando os cenários de sucesso.
* Tratamento de Erros: Elabore testes que verifiquem como a aplicação lida com erros. 
* Dados Inválidos: Note que dados mal-formatados, normalmente nos 'sendkeys' seguidos por 'change', podem ser fornecidos e que podem provocam aletarções nos CSS e em outros atributos. Utilize esses casos para criar verificações que possam detectar essas situações inadequadas.
* Armazene em váriaveis com nomes sugestivos os valores digitados pelo usuário.
* Preste atenção na digitação de teclas especiais, como 'ENTER' e 'TAB'.
* Separe o script em dois pedaços, keyword.resouce e testsuit.robot, e coloque um separador com 3 caracteres '=' entre eles.


Use esses exemplos para entender como devem ser os script:

<inicio keyword.resouce>
*** Settings ***
Documentation     A resource file with keywords for testing the Wellzesta Life staging environment.
Library           SeleniumLibrary

*** Variables ***
${EMAIL_INPUT}    xpath://input[@id="email"]
${PIN_INPUT}      xpath://input[@id="pin"]
${AUTH_BUTTON}    xpath://button[contains(text(), "Login")]

*** Keywords ***
Open Browser To Login Page
    [Arguments]    ${LOGIN_URL}    ${BROWSER}
    Open Browser    ${LOGIN_URL}    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Email

Go To Login Page
    [Arguments]    ${LOGIN_URL}
    Go To    ${LOGIN_URL}
    Wait Until Page Contains    Email    10s

Enter Email
    [Arguments]    ${email}
    Wait Until Element Is Visible    ${EMAIL_INPUT}    10s
    Input Text    ${EMAIL_INPUT}    ${email}
    Press Keys    ${EMAIL_INPUT}    ENTER

Enter PIN
    [Arguments]    ${pin}
    Wait Until Element Is Visible    ${PIN_INPUT}    10s
    Input Text    ${PIN_INPUT}    ${pin}
    Press Keys    ${PIN_INPUT}    ENTER

Verify Successful Login
    [Arguments]    ${success_message}
    Wait Until Page Contains    ${success_message}    15s

Verify Login Error
    [Arguments]    ${error_message}
    Wait Until Element Contains    ${AUTH_BUTTON}    ${error_message}    15s

<fim keyword.resouce>


<inicio testsuit.robot>
*** Settings ***
Documentation     Test Suite for validating the login functionality on the Wellzesta Life staging environment.
Resource          keywords.resource

Suite Setup       Open Browser To Login Page    ${LOGIN_URL}    ${BROWSER}
Suite Teardown    Close Browser
Test Setup        Go To Login Page    ${LOGIN_URL}
Test Teardown     Capture Page Screenshot

*** Variables ***
${BROWSER}        Chrome
${LOGIN_URL}      https://life.stg.wellzesta.com/login
${EMAIL}          sandro@gmail.com
${PIN}            1234
${SUCCESS_MESSAGE}    Cacau Caregivers United
${ERROR_MESSAGE}      Login    # Assumindo que o botão volta para "Login" em caso de erro

*** Test Cases ***
Valid Login
    [Documentation]    Test Case to verify if a user can log in with valid credentials.
    Enter Email    ${EMAIL}
    Enter PIN    ${PIN}
    Verify Successful Login    ${SUCCESS_MESSAGE}

Invalid Login
    [Documentation]    Test Case to verify the system behavior with invalid PIN.
    Enter Email    ${EMAIL}
    Enter PIN    0000    # Assuming 0000 is an invalid PIN
    Verify Login Error    ${ERROR_MESSAGE}

<fim testsuit.robot>

Aguarde até que eu envie os logs para você criar os scripts.
"""