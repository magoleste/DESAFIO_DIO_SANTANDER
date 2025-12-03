# Instale os pacotes necessários
# pip install pandas requests openai

import pandas as pd
import requests
import openai

# Configurações
sdw2023_api_url = 'https://sdw-2023-prd.up.railway.app'
openai.api_key = 'DEVE PREENCHER A KEY DA OPENAI'

# ---------------------------------------------
# ETAPA 1: Ler a lista de usuários do CSV
# ---------------------------------------------
df = pd.read_csv('SDW2023.csv')  
user_ids = df['UserID'].tolist()
users = []  

# Para cada ID, buscamos os dados do usuário na API
for user_id in user_ids:
    response = requests.get(f'{sdw2023_api_url}/users/{user_id}')
    if response.status_code == 200:
        user = response.json()  # Converte a resposta em dicionário
        users.append(user)  # Adiciona o usuário a lista
    else:
        print(f"Erro ao obter usuário {user_id}")

# ---------------------------------------------
# ETAPA 2: Criar uma mensagem personalizada
# ---------------------------------------------
# Para cada usuário, vamos gerar uma mensagem de marketing
for user in users:
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Você é especialista em marketing."},
            {"role": "user", "content": f"Crie uma mensagem curta para {user['name']} sobre investimentos."}
        ]
    )
    message = completion.choices[0].message.content.strip()  # Pega o texto gerado

    # Adiciona a mensagem ao campo 'news' do usuário
    user['news'].append({
        "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
        "description": message
    })

# ---------------------------------------------
# ETAPA 3: Atualizar os usuários na API
# ---------------------------------------------
for user in users:
    response = requests.put(f"{sdw2023_api_url}/users/{user['id']}", json=user)
    if response.status_code == 200:
        print(f"Usuário {user['name']} atualizado com sucesso!")
    else:
        print(f"Erro ao atualizar usuário {user['name']}")
