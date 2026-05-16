# 🔑 Credenciais Arc e Circle - Explicado

## ✅ O Que Você JÁ TEM (No .env.example)

### Arc Network (JÁ CONFIGURADO)

```bash
# ✅ VOCÊ JÁ TEM ISSO:
ARC_RPC_URL=https://rpc.testnet.arc.network      # URL pública do Arc testnet
ARC_CHAIN_ID=5042002                              # ID da rede Arc testnet
USDC_ADDRESS=0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913  # Endereço USDC em Arc
```

**O que significa:**
- **RPC_URL**: É como um "telefone" para falar com a rede Arc. Qualquer pessoa pode usar (é pública)
- **CHAIN_ID**: Identificador único da rede (como um número de série)
- **USDC_ADDRESS**: Endereço do contrato USDC já deployado em Arc

✅ **Você NÃO precisa fazer nada aqui - já está pronto!**

---

## ❌ O Que Você PRECISA (Circle Sandbox)

### Circle - 3 Credenciais Necessárias

#### 1️⃣ **CIRCLE_API_KEY** - Sua Chave de Acesso

```
O que é: Token para autenticar suas requisições à API Circle
Onde obter: https://console.circle.com → API Keys → Create New Key
Exemplo: pk_test_51234567890abcdefghijklmnop
Segurança: ⚠️ NUNCA compartilhe ou committe no Git
```

**Como usar:**
```bash
# No código
curl -H "Authorization: Bearer pk_test_..." https://api-sandbox.circle.com/v1/...
```

#### 2️⃣ **CIRCLE_ENTITY_SECRET** - Seu Segredo Privado

```
O que é: Chave secreta para assinar requisições (como uma senha)
Onde obter: https://console.circle.com → Settings → Entity Secret
Exemplo: secret_live_abcdefghijklmnopqrstuvwxyz
Segurança: ⚠️ NUNCA compartilhe ou committe no Git
```

**Como usar:**
```bash
# No código (para assinar requisições)
import hmac
signature = hmac.new(
    CIRCLE_ENTITY_SECRET.encode(),
    message.encode(),
    hashlib.sha256
).hexdigest()
```

#### 3️⃣ **CIRCLE_WALLET_SET_ID** - ID do Seu Conjunto de Wallets

```
O que é: Identificador do grupo de wallets que você criou na Circle
Onde obter: https://console.circle.com → Wallets → Wallet Sets → Copy ID
Exemplo: 550e8400-e29b-41d4-a716-446655440000
Segurança: ✅ Pode ser compartilhado (não é secreto)
```

**Como usar:**
```bash
# No código (para criar wallets para seus usuários)
payload = {
    "walletSetId": "550e8400-e29b-41d4-a716-446655440000",
    "blockchains": ["ARC", "ETHEREUM", "POLYGON"]
}
```

---

## 🎯 Resumo: O Que Você Precisa Fazer

### Passo 1: Ir para Circle Console

```
1. Abra: https://console.circle.com
2. Faça login (ou crie conta)
3. Vá para: Settings → API Keys
```

### Passo 2: Copiar as 3 Credenciais

| Credencial | Onde | Tipo |
|-----------|------|------|
| **API_KEY** | Settings → API Keys → Create | Público (mas seguro) |
| **ENTITY_SECRET** | Settings → Entity Secret | ⚠️ SECRETO |
| **WALLET_SET_ID** | Wallets → Wallet Sets → Copy | Público |

### Passo 3: Editar .env

```bash
# Copiar .env.example para .env
cp .env.example .env

# Editar .env com suas credenciais
CIRCLE_API_KEY=pk_test_...
CIRCLE_ENTITY_SECRET=secret_live_...
CIRCLE_WALLET_SET_ID=550e8400-...
```

### Passo 4: ⚠️ NÃO COMMITTE .env

```bash
# .env está em .gitignore - NÃO será commitado
git status
# Não deve mostrar .env
```

---

## 📊 Tabela Completa: O Que Você Tem vs Precisa

| Variável | Status | Valor | Segurança | Ação |
|----------|--------|-------|-----------|------|
| `ARC_RPC_URL` | ✅ Pronto | `https://rpc.testnet.arc.network` | Público | Nada |
| `ARC_CHAIN_ID` | ✅ Pronto | `5042002` | Público | Nada |
| `USDC_ADDRESS` | ✅ Pronto | `0x833589...` | Público | Nada |
| `CIRCLE_API_KEY` | ❌ Falta | `pk_test_...` | Secreto | Obter em Circle |
| `CIRCLE_ENTITY_SECRET` | ❌ Falta | `secret_live_...` | ⚠️ Muito Secreto | Obter em Circle |
| `CIRCLE_WALLET_SET_ID` | ❌ Falta | `550e8400-...` | Público | Obter em Circle |
| `PRIVATE_KEY` | ✅ Pronto | `0x41975...` | ⚠️ Muito Secreto | Já tem |

---

## 🔐 Segurança: O Que é "Secret"?

### ⚠️ SECRETO (Nunca compartilhe)

```
❌ CIRCLE_ENTITY_SECRET = secret_live_...
❌ PRIVATE_KEY = 0x41975...
❌ DATABASE_PASSWORD = ...
```

**Se vazar:**
- Alguém pode assinar transações em seu nome
- Alguém pode acessar suas wallets
- Alguém pode drenar seus fundos

**O que fazer se vazar:**
1. Regenerar a credencial em Circle Console
2. Atualizar .env
3. Fazer deploy novamente

### ✅ PÚBLICO (Pode compartilhar)

```
✅ ARC_RPC_URL = https://rpc.testnet.arc.network
✅ ARC_CHAIN_ID = 5042002
✅ CIRCLE_API_KEY = pk_test_... (mas ainda é privado para você)
✅ CIRCLE_WALLET_SET_ID = 550e8400-...
✅ USDC_ADDRESS = 0x833589...
```

**Esses podem estar em:**
- Documentação pública
- Código aberto no GitHub
- Compartilhados com equipe

---

## 🚀 Fluxo Completo

### 1. Você cria uma conta em Circle

```
https://console.circle.com → Sign Up
```

### 2. Circle cria para você:

```
✅ API_KEY (para autenticar)
✅ ENTITY_SECRET (para assinar)
✅ WALLET_SET_ID (seu grupo de wallets)
```

### 3. Você coloca no .env

```bash
CIRCLE_API_KEY=pk_test_...
CIRCLE_ENTITY_SECRET=secret_live_...
CIRCLE_WALLET_SET_ID=550e8400-...
```

### 4. Seu código usa para:

```python
# Criar wallets para usuários
wallet = circle_service.create_wallet(user_id)

# Transferir USDC
transfer = circle_service.transfer_usdc(
    from_wallet_id=wallet["id"],
    to_address="0x...",
    amount=100.0
)

# Verificar balance
balance = circle_service.get_wallet_balance(wallet["id"])
```

### 5. Circle faz a mágica

```
Circle API → Valida credenciais → Cria wallet → Transfere USDC → Retorna resultado
```

---

## 💡 Analogia Simples

**Circle é como um banco:**

```
CIRCLE_API_KEY      = Seu número de cliente (público)
CIRCLE_ENTITY_SECRET = Sua senha (SECRETO)
CIRCLE_WALLET_SET_ID = Seu número de conta (público)

Quando você quer transferir dinheiro:
1. Você prova quem é (API_KEY)
2. Você assina com sua senha (ENTITY_SECRET)
3. Você diz qual conta usar (WALLET_SET_ID)
4. O banco faz a transferência
```

---

## 🎯 Checklist: Pronto para Deploy

- [ ] Tenho conta em Circle (https://console.circle.com)
- [ ] Copiei CIRCLE_API_KEY
- [ ] Copiei CIRCLE_ENTITY_SECRET
- [ ] Copiei CIRCLE_WALLET_SET_ID
- [ ] Criei .env com as 3 credenciais
- [ ] Verifiquei que .env NÃO está em Git
- [ ] Testei: `npm run setup`
- [ ] Testei: `npm run deploy:arc`

---

## 🆘 Troubleshooting

### "Circle API retorna 401 Unauthorized"

```
❌ Problema: API_KEY está errado ou expirou
✅ Solução: Regenerar em Circle Console → Settings → API Keys
```

### "Invalid Entity Secret"

```
❌ Problema: ENTITY_SECRET está errado
✅ Solução: Copiar novamente de Circle Console → Settings → Entity Secret
```

### "Wallet Set not found"

```
❌ Problema: WALLET_SET_ID está errado
✅ Solução: Verificar em Circle Console → Wallets → Wallet Sets
```

### "Arquivo .env commitado no Git"

```
❌ Problema: Você commitou .env (com secrets!)
✅ Solução: 
1. git rm --cached .env
2. git commit -m "Remove .env"
3. git push
4. Regenerar todas as credenciais em Circle
```

---

## 📚 Links Úteis

- **Circle Console**: https://console.circle.com
- **Circle Docs**: https://developers.circle.com
- **Arc Network**: https://arc.io
- **ORVION Docs**: ./README_FINAL.md

---

**Resumo Final:**

| Item | Você Tem? | Ação |
|------|----------|------|
| Arc RPC URL | ✅ Sim | Nada |
| Arc Chain ID | ✅ Sim | Nada |
| Circle API Key | ❌ Não | Obter em Circle |
| Circle Entity Secret | ❌ Não | Obter em Circle |
| Circle Wallet Set ID | ❌ Não | Obter em Circle |

**Próximo passo:** Ir para https://console.circle.com e copiar as 3 credenciais! 🚀
