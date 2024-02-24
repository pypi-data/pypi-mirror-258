_B='pg-postgres_fdw'
_A='pg-plv8'
import os,shutil
from typing import List
from localstack import config
from localstack.packages import InstallTarget,Package,PackageInstaller
from localstack.packages.core import ArchiveDownloadAndExtractInstaller
from localstack.utils.files import cp_r,file_exists_not_empty
from localstack.utils.http import download
from localstack.utils.platform import get_arch
PG_PLV8_URL='https://localstack-assets.s3.amazonaws.com/postgres-<pg_version>-plv8-<arch>.zip'
PG_POSTGRES_FDW_URL='https://localstack-assets.s3.amazonaws.com/postgres-<pg_version>-postgres_fdw-<arch>.zip'
POSTGRES_VERSION='15'
class CachingArchiveDownloadAndExtractInstaller(ArchiveDownloadAndExtractInstaller):
	def _install(D,target):
		B=D._get_download_url();C=os.path.basename(B);A=os.path.join(config.dirs.cache,C);E=os.path.join(config.dirs.tmp,C)
		if not file_exists_not_empty(A):download(B,A)
		shutil.copy(A,E);super()._install(target=target)
class PostgresExtensionInstaller(CachingArchiveDownloadAndExtractInstaller):
	url_pattern:0;extension_name:0
	def _get_download_url(B):A=B.url_pattern.replace('<pg_version>',POSTGRES_VERSION);A=A.replace('<arch>',get_arch());return A
	def _post_process(A,target):B=A._get_install_dir(target);cp_r(os.path.join(B,'usr'),'/usr')
	def _get_install_marker_path(A,install_dir):return f"/usr/share/postgresql/{POSTGRES_VERSION}/extension/{A.extension_name}.control"
class PostgresPlv8Package(Package):
	def __init__(A):super().__init__(_A,POSTGRES_VERSION)
	def get_versions(A):return[POSTGRES_VERSION]
	def _get_installer(A,version):return PostgresPlv8Installer(version)
class PostgresPlv8Installer(PostgresExtensionInstaller):
	def __init__(A,version):super().__init__(_A,version);A.url_pattern=PG_PLV8_URL;A.extension_name='plv8'
class PostgresFdwPackage(Package):
	def __init__(A):super().__init__(_B,POSTGRES_VERSION)
	def get_versions(A):return[POSTGRES_VERSION]
	def _get_installer(A,version):return PostgresFdwInstaller(version)
class PostgresFdwInstaller(PostgresExtensionInstaller):
	def __init__(A,version):super().__init__(_B,version);A.url_pattern=PG_POSTGRES_FDW_URL;A.extension_name='postgres_fdw'
postgres_plv8_package=PostgresPlv8Package()
postgres_fdw_package=PostgresFdwPackage()