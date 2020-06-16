# Edit M
Demostração de como editar um arquivo do Power BI utilizando Python

Qualquer Dúvida pode me chamar no Linkedin https://www.linkedin.com/in/tadeu-mansi/

# Configuração

Para utilizar esse código basta instanciar a classe EditM e passar seus parâmetros.

```python
pbit_antigo = r"seu_relatorio_atual.pbit"
pbit_novo = r"vai_ser_criado.pbit"
codigo_velho = bytes('codigo m que você quer buscar','utf-8')
codigo_novo = bytes('codigo m que você quer atualizar','utf-8')
m = EditM(pbit_antigo,pbit_novo,codigo_velho,codigo_novo)  
```

# Vídeo Demonstrativo

[![IMAGE ALT TEXT HERE](http://img.youtube.com/vi/c0UZTCEww1E/0.jpg)](https://www.youtube.com/watch?v=c0UZTCEww1E)

