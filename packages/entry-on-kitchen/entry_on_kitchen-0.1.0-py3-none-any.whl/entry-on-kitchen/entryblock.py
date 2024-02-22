import requests
import json
import time

class EntryBlock:
    def __init__(self, pipelineId, entryBlockId, entryPoint="", entryAuthCode):
        if not pipelineId or not entryBlockId:
            raise ValueError('pipelineId and entryBlockId are required')

        self.pipelineId = pipelineId
        self.entryBlockId = entryBlockId
        self.entryPoint = entryPoint
        self.entryAuthCode = entryAuthCode

    def runSync(self, body):
        result = None
        resolved = False

        headers = {
            'Content-Type': 'application/json',
            'X-Entry-Auth-Code': self.entryAuthCode,
        }

        entryPoint = self.entryPoint + "." if self.entryPoint else ""

        stringifiedBody = body if isinstance(body, str) else json.dumps(body)

        response = requests.post(
            f"https://{entryPoint}entry.on.kitchen/{self.pipelineId}/{self.entryBlockId}/sync",
            data=stringifiedBody,
            headers=headers
        )

        result = response.json() if response.ok else response.json()

        return result

    def pollStatus(self, runId):
        status = None
        resolved = False

        headers = {
            'Content-Type': 'application/json',
            'X-Entry-Auth-Code': self.entryAuthCode,
        }

        entryPoint = self.entryPoint + "." if self.entryPoint else ""

        response = requests.get(
            f"https://{entryPoint}entry.on.kitchen/{self.pipelineId}/pollstatus/{runId}",
            headers=headers
        )

        status = response.json() if response.ok else response.json()

        return status

    def pollStatusAsync(self, runId):
        headers = {
            'Content-Type': 'application/json',
            'X-Entry-Auth-Code': self.entryAuthCode,
        }

        entryPoint = self.entryPoint + "." if self.entryPoint else ""

        response = requests.get(
            f"https://{entryPoint}entry.on.kitchen/{self.pipelineId}/pollstatus/{runId}",
            headers=headers
        )

        return response.json()

    def runAsync(self, body):
        headers = {
            'Content-Type': 'application/json',
            'X-Entry-Auth-Code': self.entryAuthCode,
        }

        entryPoint = self.entryPoint + "." if self.entryPoint else ""

        stringifiedBody = body if isinstance(body, str) else json.dumps(body)

        response = requests.post(
            f"https://{entryPoint}entry.on.kitchen/{self.pipelineId}/{self.entryBlockId}/async",
            data=stringifiedBody,
            headers=headers
        )

        if response.ok:
            runId = response.json()['runId']
            while True:
                status = self.pollStatusAsync(runId)
                if status['status'] == "finished":
                    return status
                elif status['status'] == "running":
                    time.sleep(1)
                else:
                    return status
        else:
            print('Unable to runAsync:', response.json())

