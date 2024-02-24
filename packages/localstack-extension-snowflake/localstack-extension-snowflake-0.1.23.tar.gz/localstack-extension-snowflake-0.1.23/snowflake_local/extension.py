import logging
from localstack.extensions.api import Extension
from rolo.gateway import CompositeExceptionHandler,CompositeResponseHandler
from rolo.router import Router,RuleAdapter,WithHost
LOG=logging.getLogger(__name__)
SQLGLOT_VERSION='21.2.0'
class SnowflakeExtension(Extension):
	name='snowflake'
	def on_platform_start(C):
		from localstack import config as A;from localstack.utils.run import run
		if A.is_in_docker:
			try:run(['pip','install',f"sqlglot=={SQLGLOT_VERSION}"])
			except Exception as B:LOG.debug('Unable to install sqlglot version: %s',B)
	def update_gateway_routes(C,router):from snowflake_local.server.routes import HOST_URL_PATTERN as A,RequestHandler as B;router.add(WithHost(A,[RuleAdapter(B())]))
	def update_response_handlers(D,handlers):A=handlers;from snowflake_local.analytics.handler import SnowflakeAnalyticsHandler as B,TraceLoggingHandler as C;A.append(B());A.append(C())
	def update_exception_handlers(B,handlers):from snowflake_local.analytics.handler import QueryFailureHandler as A;handlers.append(A())