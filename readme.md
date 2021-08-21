# Comandos do git
- Criando um repositório
    - git init
- Adicionando os arquivos ao pacote
    - git add .
- Fazendo o primeiro commit
    - git commit -m 'First commit'
- Acertando a branch
    - git branch -M main
- Definindo o remote. O primeiro é na primeira vez, as demais são a segunda linha
    - git remote add origin https://arvieira:<API_KEY>@github.com/arvieira/Avaliacao_Credito.git
    - git remote set-url origin https://arvieira:<API_KEY>@github.com/arvieira/Avaliacao_Credito.git
- Enviando os arquivos em um push
    - git push -u origin main


# Virtual Environment do Python
- python3 -m venv venv
- source venv/bin/activate
- Adicionar arquivos requirements.txt e executar
    - pip3 install -r requirements.txt


# Streamlit
- Primeira execução de um hello world
    - streamlit hello
- Executando sua primeira aplicação
    - Cria um script em python que importe o streamlit imprima markdown com o st.write do streamlit
    - streamlit run <nome do script>
- Posso criar uma pasta chamada .streamlit com o arquivo config.toml dentro com configurações de 
exibição para o css final.