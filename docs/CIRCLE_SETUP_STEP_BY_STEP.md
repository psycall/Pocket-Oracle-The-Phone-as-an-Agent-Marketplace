# 🔑 Circle Setup - Passo a Passo

## Você Tem:
```
TEST_API_KEY: e6946e7c1722ec9e3e08a251e532c79a:d83f0a6964b28b30c09f73e4a8b7a00d
```

## Você Precisa Gerar:
```
❌ CIRCLE_ENTITY_SECRET (vazio)
❌ CIRCLE_WALLET_SET_ID (vazio)
```

---

## 🎯 Passo 1: Colocar API Key no .env

```bash
# Editar .env
CIRCLE_API_KEY=e6946e7c1722ec9e3e08a251e532c79a:d83f0a6964b28b30c09f73e4a8b7a00d
```

**Pronto! Essa você já tem.**

---

## 🎯 Passo 2: Gerar CIRCLE_ENTITY_SECRET

### Onde encontrar:

1. **Abra Circle Console**:
   ```
   https://console.circle.com
   ```

2. **Clique em "Settings"** (canto superior direito)
   ```
   Profile icon → Settings
   ```

3. **Procure por "Entity Secret"** ou "API Secret"
   ```
   Você vai ver um campo com um botão "Generate" ou "Regenerate"
   ```

4. **Clique em "Generate"** (se estiver vazio)
   ```
   Vai gerar algo como: secret_live_abcdefghijklmnopqrstuvwxyz
   ```

5. **Copie e cole no .env**:
   ```bash
   CIRCLE_ENTITY_SECRET=secret_live_abcdefghijklmnopqrstuvwxyz
   ```

**Se não conseguir encontrar:**
- Procure por "API Secret" ou "Signing Secret"
- Ou vá em: Settings → API → Secrets

---

## 🎯 Passo 3: Gerar CIRCLE_WALLET_SET_ID

### Onde encontrar:

1. **No Circle Console**, procure por "Wallets"
   ```
   Menu esquerdo → Wallets
   ```

2. **Procure por "Wallet Sets"**
   ```
   Você vai ver uma lista de wallet sets
   ```

3. **Se não tiver nenhum, crie um novo**:
   ```
   Botão "+ Create Wallet Set"
   ```

4. **Copie o ID**:
   ```
   Você vai ver um ID como: 550e8400-e29b-41d4-a716-446655440000
   Clique no ícone de copiar ao lado
   ```

5. **Cole no .env**:
   ```bash
   CIRCLE_WALLET_SET_ID=550e8400-e29b-41d4-a716-446655440000
   ```

**Se não conseguir encontrar:**
- Procure por "Wallet Management"
- Ou vá em: Wallets → Wallet Sets → Copy ID

---

## 📝 Seu .env Deve Ficar Assim:

```bash
# Circle Services
CIRCLE_API_KEY=e6946e7c1722ec9e3e08a251e532c79a:d83f0a6964b28b30c09f73e4a8b7a00d
CIRCLE_ENTITY_SECRET=secret_live_abcdefghijklmnopqrstuvwxyz
CIRCLE_WALLET_SET_ID=550e8400-e29b-41d4-a716-446655440000

# Arc Network (já pronto)
ARC_RPC_URL=https://rpc.testnet.arc.network
ARC_CHAIN_ID=5042002

# Smart Contract
PRIVATE_KEY=0x41975126c6465e2d42bd75154867d75604fd67a2da40a91d2ab3489cac9186c8
```

---

## 🔍 Verificar se Está Correto

### Teste 1: Verificar .env

```bash
# Ver se as 3 credenciais estão lá
cat .env | grep CIRCLE

# Deve mostrar:
# CIRCLE_API_KEY=e6946e7c...
# CIRCLE_ENTITY_SECRET=secret_live_...
# CIRCLE_WALLET_SET_ID=550e8400-...
```

### Teste 2: Verificar se .env não está em Git

```bash
# Verificar que .env está em .gitignore
grep "^\.env$" .gitignore

# Deve mostrar: .env
```

### Teste 3: Testar conexão com Circle

```bash
# Python test
python -c "
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('CIRCLE_API_KEY')
entity_secret = os.getenv('CIRCLE_ENTITY_SECRET')
wallet_set_id = os.getenv('CIRCLE_WALLET_SET_ID')

print('✅ API Key:', api_key[:20] + '...' if api_key else '❌ Vazio')
print('✅ Entity Secret:', entity_secret[:20] + '...' if entity_secret else '❌ Vazio')
print('✅ Wallet Set ID:', wallet_set_id if wallet_set_id else '❌ Vazio')
"
```

---

## 🚀 Próximos Passos

Depois que tiver as 3 credenciais no .env:

```bash
# 1. Setup
npm run setup

# 2. Deploy
npm run deploy:arc

# 3. Backend
python main.py

# 4. Frontend
cd frontend && npm start
```

---

## ⚠️ Troubleshooting

### "Não consigo encontrar Entity Secret"

**Solução:**
1. Vá para: https://console.circle.com/settings
2. Procure por "API" ou "Secrets"
3. Se não tiver, clique em "Generate New Secret"
4. Copie o valor

### "Não consigo encontrar Wallet Set ID"

**Solução:**
1. Vá para: https://console.circle.com/wallets
2. Procure por "Wallet Sets"
3. Se não tiver nenhum, clique em "+ Create"
4. Copie o ID

### "API Key não funciona"

**Solução:**
1. Verifique se copiou corretamente
2. Verifique se não tem espaços extras
3. Tente regenerar a chave em Circle Console

### ".env commitado no Git"

**Solução:**
```bash
# Se você acidentalmente commitou .env:
git rm --cached .env
git commit -m "Remove .env"
git push

# Regenerar TODAS as credenciais em Circle
# Porque agora estão expostas!
```

---

## 📊 Checklist Final

- [ ] Copiei CIRCLE_API_KEY para .env
- [ ] Gerei CIRCLE_ENTITY_SECRET e copiei para .env
- [ ] Gerei CIRCLE_WALLET_SET_ID e copiei para .env
- [ ] Verifiquei que .env NÃO está em Git
- [ ] Testei: `python -c "import os; print(os.getenv('CIRCLE_API_KEY'))"`
- [ ] Pronto para deploy!

---

## 🎯 Resumo

| Credencial | Você Tem? | Ação |
|-----------|----------|------|
| `CIRCLE_API_KEY` | ✅ Sim | Cole em .env |
| `CIRCLE_ENTITY_SECRET` | ❌ Não | Gere em Circle Console → Settings |
| `CIRCLE_WALLET_SET_ID` | ❌ Não | Gere em Circle Console → Wallets |

**Depois que tiver os 3, você está pronto para deploy!** 🚀
