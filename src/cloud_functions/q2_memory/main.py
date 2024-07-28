from google.cloud import pubsub_v1
from utils import read_file_from_gcs
import os
import gc

# Retrieve the Google Cloud project ID from environment variables
__project_id__ = os.getenv("GCP_PROJECT_ID")

def q2_memory(request):
    request_json = request.get_json(silent=True)
    bucket_name = request_json['bucket_name']
    file_path = request_json['file_path']
    topic_name = f"projects/{__project_id__}/topics/tweets-topic"

    # Leer archivo desde Cloud Storage
    file_content = read_file_from_gcs(bucket_name, file_path)

    # Procesar archivo por lotes
    batch_size = 100
    lines = file_content.split('\n')
    
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(__project_id__, topic_name)
    
    for i in range(0, len(lines), batch_size):
        batch = lines[i:i + batch_size]
        for line in batch:
            publisher.publish(topic_path, line.encode("utf-8"))
        
        del batch
        gc.collect()
    
    return {"status": "Processing started"}