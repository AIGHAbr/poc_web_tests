global prompt_robot
prompt_robot = ("""
Com base nos logs fornecidos, que simula a navegação no site e as ações realizadas, 
crie para mim os script de teste para o Robot Framework.
Retorne somente os scripts de teste, nada mais.
Olhe os eventos e identifique repetições, para que não gere código duplicado.
Preste atenção nos eventos de click e sendkeys, pois eles são os mais importantes.
Preste atenção em teclas especiais, como Enter e Tab.          
Segue abaixo os logs:
""")