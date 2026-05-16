import asyncio
import httpx
import time

BASE_URL = "http://127.0.0.1:8000"

async def test_endpoint(client, endpoint):
    try:
        start = time.time()
        response = await client.get(f"{BASE_URL}{endpoint}")
        duration = time.time() - start
        return response.status_code, duration
    except Exception as e:
        return str(e), 0

async def run_stress_test(concurrency, total_requests):
    print(f"🚀 Iniciando teste de estresse: {total_requests} requisições com concorrência {concurrency}")
    async with httpx.AsyncClient() as client:
        tasks = []
        for _ in range(total_requests):
            tasks.append(test_endpoint(client, "/"))
        
        start_time = time.time()
        results = await asyncio.gather(*tasks)
        total_duration = time.time() - start_time
        
        successes = [r for r in results if r[0] == 200]
        failures = [r for r in results if r[0] != 200]
        avg_time = sum(r[1] for r in results) / len(results) if results else 0
        
        print(f"\n📊 Resultados do Teste de Estresse:")
        print(f"✅ Sucessos: {len(successes)}")
        print(f"❌ Falhas: {len(failures)}")
        print(f"⏱️ Tempo Total: {total_duration:.2f}s")
        print(f"⚡ Média de Resposta: {avg_time:.4f}s")
        print(f"📈 Requisições/seg: {len(results)/total_duration:.2f}")

if __name__ == "__main__":
    # Aguarda o servidor subir
    time.sleep(5)
    asyncio.run(run_stress_test(concurrency=50, total_requests=500))
