from google.cloud import pubsub_v1
from utils import read_file_from_gcs
import os

# Retrieve the Google Cloud project ID from environment variables
__project_id__ = os.getenv("GCP_PROJECT_ID")

def q2_memory(request):
    request_json = request.get_json(silent=True)
    bucket_name = request_json['bucket_name']
    file_path = request_json['file_path']
    topic_name = f"projects/{__project_id__}/topics/tweets-topic"

    # Leer archivo desde Cloud Storage
    file_content = read_file_from_gcs(bucket_name, file_path)
    lines = file_content.split('\n')
    
    # Publicar mensajes en Pub/Sub
    publisher = pubsub_v1.PublisherClient()
    
    for line in lines:
        publisher.publish(topic_name, line.encode("utf-8"))
    
    return {"status": "Processing started"}
