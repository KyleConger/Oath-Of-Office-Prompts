from dotenv import load_dotenv
import os
load_dotenv()

import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate(os.getenv('FIREBASE_CRED'))
app = firebase_admin.initialize_app(cred, {
    'projectId': os.getenv('FIREBASE_PROJECT_ID'),
})
db = firestore.client()

class Prompts:
    def __init__(self, job_name, job_info):
        self.IssueTitle = job_info[0] if len(job_info) > 0 else None
        self.IssueScenario = job_info[1] if len(job_info) > 1 else []
        self.GlobalVariables = job_info[2] if len(job_info) > 2 else []
        self.Options = job_info[3] if len(job_info) > 3 else {}
        self.Variables = job_info[4] if len(job_info) > 4 else []
    
    @staticmethod
    def from_dict(source):
        return Prompts(
            job_name=source.get('job_name'),
            job_info=[
                source.get('IssueTitle'),
                source.get('IssueScenario'),
                source.get('GlobalVariables'),
                source.get('Options'),
                source.get('Variables')
            ]
        )

    def to_dict(self):
        return {
            'IssueTitle': self.IssueTitle,
            'IssueScenario': self.IssueScenario,
            'GlobalVariables': self.GlobalVariables,
            'Options': self.Options,
            'Variables': self.Variables
        }

    def __repr__(self):
        return f"Prompts(IssueTitle={self.IssueTitle}, IssueScenario={self.IssueScenario}, GlobalVariables={self.GlobalVariables}, Options={self.Options}, Variables={self.Variables})"

class Firestore_Use:
    @staticmethod
    def firestore_save(name, info, storagegrouping):
        # Replace slashes in the name to avoid invalid document IDs
        sanitized_name = name.replace('/', '_')
        
        if storagegrouping == "Prompts":
            instance = Prompts(sanitized_name, info)
        else:
            raise ValueError("Invalid storage grouping")

        # Create a nested dictionary structure
        data = {
            'IssueTitle': instance.Code,
            'IssueScenario': instance.Tasks,
            'GlobalVariables': instance.Knowledge,
            'Options': {
                'Option1': {
                    'OptionTitle': instance.Abilities,
                    'OptionResult': {
                        'Middle Class': instance.Skills,
                        'Technology Industry': instance.Skills,
                        'The Economy': instance.Skills
                    }
                },
                'Option2': {
                    'OptionTitle': instance.Abilities,
                    'OptionResult': {
                        'Middle Class': instance.Skills,
                        'Technology Industry': instance.Skills,
                        'The Economy': instance.Skills
                    }
                }
            },
            'Variables': instance.Skills
        }

        doc_ref = db.collection(storagegrouping).document(sanitized_name)
        doc_ref.set(data)

    @staticmethod
    def firestore_search(name, storagegrouping):
        doc_ref = db.collection(storagegrouping).document(name)
        doc = doc_ref.get()
        if doc.exists:
            if storagegrouping == "Prompts":
                instance = Prompts.from_dict(doc.to_dict())
            else:
                raise ValueError("Invalid storage grouping")
            return instance
        else:
            return None
