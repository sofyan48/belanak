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
    
    def cancel_job(self, job_id: str):
        return self.client.fine_tuning.jobs.cancel(
            job_id=job_id
        )
    
    def start_job(self, job_id: str):
        return self.client.fine_tuning.jobs.start(
            job_id=job_id
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
            hyperparameters={
                "training_steps": step,
                "learning_rate": learning_rate
            },
            auto_start=False
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
    
    