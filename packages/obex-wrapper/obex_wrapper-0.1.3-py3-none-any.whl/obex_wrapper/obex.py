
from __future__ import annotations

import httpx
import json 
from datetime import datetime
import uuid
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

from opentelemetry.sdk.resources import Resource
import logging

from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from presidio_analyzer import AnalyzerEngine
import boto3
from google.cloud import storage
import google.auth
import requests
from google.auth.transport.requests import Request

OTEL_COLLECTOR_ENDPOINT= "https://otelcol.g58o14d6u7j6c.us-east-2.cs.amazonlightsail.com"

class ObexConfig:
	def __init__(self, env, aws_session, gcp_creds):
		if env is None:
			env = "GCP"
		if env == "AWS":
			if aws_session is None:
				aws_session = boto3.Session()  
			self.s3_client = aws_session.resource('s3')
			self.read_config = self.read_config_from_s3
		if env == "GCP":
			if gcp_creds is None:
				gcp_creds, _ = google.auth.default()
			self.gcs_client = storage.Client(project="obex-413700", credentials=gcp_creds)
			self.read_config = self.read_file_from_gcs
			self.get_user_name(gcp_creds)

	def get_user_name(self, gcp_creds):
		headers = {}
		gcp_creds.refresh(Request())
		gcp_creds.apply(headers)

		response = requests.get('https://www.googleapis.com/oauth2/v3/tokeninfo', headers=headers)
		self.user = response.json()['email']

	def read_file_from_gcs(self):
		try:
			bucket = self.gcs_client.get_bucket('obex-config-dev')
			blob = bucket.blob('obex-config.json')
			self.config = json.loads(blob.download_as_text())
		except Exception as e:
			raise Exception("Error reading the Obex config file from GCS: " 
				   + str(e) + ". Please check if you have the right permissions.")


	def read_config_from_s3(self):
		try:
			obj = self.s3_client.Object('obex-config-dev', 'obex-config.json').get()
			data = obj['Body'].read().decode('utf-8')
			self.config = json.loads(data)
		except Exception as e:
			raise Exception("Error reading the Obex config file from S3: " 
				   + str(e) + ". Please check if you have the right permissions.")
	
	def get_dlp_config(self):
		self.read_config()
		return self.config['dlp']

	def get_api_key(self, provider):
		self.read_config()
		return self.config['api_keys'][provider]
	
	def get_user(self):
		return self.user

	def get_org(self):
		return "Acme Inc."

class ObexDLPBlocker:
	def __init__(self, config_provider):
		self.config_provider = config_provider
		self.redact_analyzer = AnalyzerEngine()
		self.block_analyzer = AnalyzerEngine()
		dlp_config = self.config_provider.get_dlp_config()
		self.redact_entities = []
		self.block_entities = []
		for z in dlp_config['preset']:
			if z['status'] == "Redact":
				self.redact_entities.append(z['name'])
			elif z['status'] == "Block":
				self.block_entities.append(z['name'])

	def check(self, text):
		block_results = self.block_analyzer.analyze(text=text,entities=self.block_entities, language='en')
		return block_results

class ObexLogger:
	def __init__(self):
		resource = Resource(attributes={SERVICE_NAME: "obex"})
		
		self._logger = logging.getLogger("obex")
		exporter = OTLPLogExporter(endpoint=OTEL_COLLECTOR_ENDPOINT+"/v1/logs")
		logger_provider = LoggerProvider(resource=resource)
		logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
		handler = LoggingHandler(level=logging.DEBUG, logger_provider=logger_provider)
		self._logger.addHandler(handler)
		self._logger.setLevel(logging.DEBUG)
	
	def log(self, data):
		self._logger.debug(json.dumps(data))


class Obex:
	def __init__(self,*, env=None, aws_session=None, gcp_creds=None):
		self.config = ObexConfig(env, aws_session, gcp_creds)
		self.logger = ObexLogger()
		self.dlp_blocker = ObexDLPBlocker(self.config)
	
	def build_audit_object(self, request, request_body, dlp_check):
		data = {}		
		data["type"] = "obex_ai_call_event"
		data["uid"] = str(uuid.uuid4())
		data["url"] = str(request.url)
		data["timestamp"] = str(datetime.now())
		data["prompt"] = request_body
		data["user"] = self.config.get_user()
		data["org"] = self.config.get_org()
		data["provider"] = "OpenAI"
		data["model"] = "GPT 3.5"
		data["dlp"] = str(dlp_check)
		return data
	
	def set_auth_header(self, request):
		request.headers['authorization'] = "Bearer " + self.config.get_api_key("openai")

	def protect(self, func):

		oldsend = httpx.Client.send

		def new_send(*args, **kwargs):
			request = args[1]
			request_body = request.read().decode("utf-8")

			self.set_auth_header(request)
			dlp_check = self.dlp_blocker.check(request_body)
			audit_data = self.build_audit_object(request, request_body, dlp_check)
			self.logger.log(audit_data)
			if dlp_check:
				responseContent = '{"msg": "Request blocked by Obex for violating DLP rules"}'
				return httpx.Response(status_code=403, request=request, json=responseContent)	
			z = oldsend(*args, **kwargs)
			return z

		def wrapper(*args, **kwargs):
			httpx.Client.send = new_send
			z = func(*args, **kwargs)
			httpx.Client.send = oldsend
			return z

		return wrapper

