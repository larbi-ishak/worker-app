import redis
import time
import os
import random
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('infrastructure-worker')

REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

def main():
    logger.info(f"Establishing connection pool to Redis at {REDIS_HOST}:{REDIS_PORT}")
    pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    r = redis.Redis(connection_pool=pool)
    
    components = [
        'gaussdb-cluster-01', 
        'nova-faas-gateway', 
        'kata-runtime-node-alpha', 
        'argocd-sync-controller',
        'terraform-state-lock'
    ]
    states = ['Healthy', 'Healthy', 'Healthy', 'Degraded', 'Scaling', 'Reconciling']

    while True:
        try:
            component = random.choice(components)
            state = random.choice(states)
            timestamp = datetime.utcnow().isoformat() + "Z"
            
            payload = f"{state}|{timestamp}"
            r.hset('global_infra_status', component, payload)
            
            logger.info(f"Telemetry updated: {component} -> {state}")
        except redis.ConnectionError as e:
            logger.error(f"Redis connection failed: {e}")
            
        time.sleep(2)

if __name__ == "__main__":
    main()
