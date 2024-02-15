app_documentation = """
Estou elaborando uma documentação de uso do nosso sistema. 
Peço que você observe os logs de navegação, reflita sobre essas ações, e me ajude a escrever uma documentação de uso. 

Siga as seguintes diretivas: 

* Toda a documentação dever ser em inglês.
* Preste atenção nos eventos 'qa', eles descrevem observações importante do time de qualidade.
* Utilize todos os eventos registrados nos logs para compreender as ações realizadas.
* Baseie-se nos eventos auxiliares, como 'change' e 'info', para entender comportamento esperado da aplicação.
* Descubra o fluxo principal e os cenários de sucesso.
* Entenda os erros mais comuns e como evita-los. 
* Note que dados mal-formatados, normalmente nos 'sendkeys' seguidos por 'change', podem ser fornecidos e que podem provocam aletarções nos CSS e em outros atributos. Utilize esses casos para detectar essas situações inadequadas.
* Preste atenção na digitação de teclas especiais, como 'ENTER' e 'TAB'.

Seguem os logs:
"""