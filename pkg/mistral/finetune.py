from mistralai import Mistral
from io import BufferedReader


class Finetune():
    def __init__(self, client: Mistral):
        self. client = client
    
    def upload_file(self,name: str, data: BufferedReader):
        return self.client.files.upload(
            file={
                "file_name": name,
                "content": data,
            }
        )
    
    def create_job(self, 
                   file_id: str, 
                   model: str, 
                   weight: int,
                   step: int, 
                   learning_rate: float):
        return self.client.fine_tuning.jobs.create(
            model= model, 
            training_files=[{"file_id": file_id, "weight": weight}],
            # validation_files=[file_validation_id], 
            hyperparameters={
                "training_steps": step,
                "learning_rate": learning_rate
            },
            auto_start=True
        )
    
    def list_job(self, limit: int, page: int):
        return self.client.fine_tuning.jobs.list(
            page=page,
            page_size=limit
        )
    
    def get_job(self, job_id):
        return self.client.fine_tuning.jobs.get(
            job_id=job_id
        )
    
    