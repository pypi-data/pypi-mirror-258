_A='snowflake.'
import json,logging,traceback
from typing import NamedTuple
from localstack import config
from localstack.utils.analytics import EventLogger,log
from localstack.utils.strings import to_str
from rolo import Response
from rolo.gateway import ExceptionHandler,HandlerChain,RequestContext
from sqlglot import exp,parse_one
from werkzeug import Response as WerkzeugResponse
from snowflake_local import config as sf_config
from snowflake_local import constants
from snowflake_local.server.models import QueryException
from snowflake_local.server.routes import get_request_data
LOG=logging.getLogger(__name__)
class SnowflakeEvent(NamedTuple):method:str;route:str;status_code:int;query:str;version:str;user_agent:str;exc_msg:str
EVENT_NAME='extensions_sf_event'
def obfuscate_query(sql_query):
	C={'column':exp.Column,'table':exp.Table,'literal':exp.Literal};A=parse_one(sql_query)
	for(D,B)in C.items():
		if A.find(B):
			for E in A.find_all(B):E.replace(B(this=f"<{D}>",is_string=True))
	return A.sql()
class SnowflakeAnalyticsHandler:
	def __init__(A,event_logger=None):A.handler=event_logger or log
	def __call__(D,chain,context,response):
		A=context
		if _A not in A.request.url:return
		if config.DISABLE_EVENTS:return
		C=getattr(A,'snowflake_exception',None);E=get_request_data(A.request);B=E.get('sqlText','')
		if B:
			try:B=obfuscate_query(B)
			except Exception as F:B=f"Exception occurred while obfuscating the query: {str(F)}"
		G=SnowflakeEvent(route=A.request.path,method=A.request.method,status_code=response.status_code,query=B,version=constants.VERSION,user_agent=A.request.user_agent.string,exc_msg=C.message if C else'');D.handler.event(EVENT_NAME,G._asdict())
class QueryFailureHandler(ExceptionHandler):
	def __call__(D,chain,exception,context,response):
		B=context;A=exception
		if _A not in B.request.url:return
		if not isinstance(A,QueryException):return
		C=D.build_exception_response(A,B)
		if C:response.update_from(C)
	def build_exception_response(D,exception,context):
		A=exception;B=A.query_data;context.snowflake_exception=A;C=Response.for_json(B.to_dict(),status=200)
		if config.DEBUG:A.message=''.join(traceback.format_exception(type(A),value=A,tb=A.__traceback__))
		return C
class TraceLoggingHandler:
	def __call__(G,chain,context,response):
		E=context;A=response
		if not sf_config.TRACE_LOG:return
		if _A not in E.request.url:return
		D=E.request;B=get_request_data(D)
		if isinstance(B,dict):B=json.dumps(B)
		F=None;C=str(A)
		if isinstance(A,WerkzeugResponse):
			F=A.status_code;C=A.data
			try:C=to_str(C)
			except Exception:pass
		LOG.debug('REQ: %s %s %s -- RES: %s %s',D.method,D.path,B,F,C)