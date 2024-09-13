import typing
from pathlib import Path
from alembic import command
from alembic.config import Config
from salestrack_utils.core.settings import CoreSettings
from salestrack_utils.addon.databases.alembic import constants
from salestrack_utils.core.utils import resolve_component_module_location


def get_alembic_config() -> Config:
    """return alembic config object"""
    alembic_path = Path(constants.__file__).parent
    # import pdb; pdb.set_trace()
    alembic_ini_file = alembic_path.joinpath("alembic.ini")
    config = Config(str(alembic_ini_file))
    config.set_main_option("script_location", str(alembic_path))
    return config


class AlembicCommand:
    """alembic migrate commands"""
    
    def __init__(self, settings: CoreSettings) -> None:
        self.alembic_cfg = get_alembic_config()
        # import pdb; pdb.set_trace()
        self.alembic_cfg.set_main_option("sqlalchemy.url", f"{settings.pg_dsn}")
        self.alembic_cfg.set_main_option("database_schema", "public")

        migration_paths = []
        for component in settings.components:
            migration_paths.append(
                resolve_component_module_location(
                    component, "alembic_versions"
                )
            )
        self.alembic_cfg.set_main_option(
            "version_locations",
            " ".join([str(path) for path in migration_paths])
        )
    
    def current(self) -> None:
        """show current revision"""
        command.current(self.alembic_cfg)

    def heads(self, verbose: bool = False) -> None:
        """Show available heads"""
        command.heads(self.alembic_cfg, verbose=verbose)

    def history(self) -> None:
        """Show revision history"""
        command.history(self.alembic_cfg)

    def initrevision(
        self,
        message: str,
        branch_label: str,
        version_path: str,
        head: str = "base",
    ) -> None:
        """initialize a branch"""
        command.revision(
            self.alembic_cfg,
            message=message,
            autogenerate=False,
            head=head,
            branch_label=branch_label,
            version_path=version_path
        )
    
    def makemigrations(
        self,
        message: str,
        branch_label: typing.Optional[str] = None,
        depends: typing.Optional[str] = None,
        auto: bool = False
    ) -> None:
        """create migration script"""
        _head = f"{branch_label}@head"
        command.revision(
            self.alembic_cfg,
            autogenerate=auto,
            message=message,
            head=_head,
            depends_on=depends
        )
    
    def migrate(self, revision: str = "head", sql: bool = False) -> None:
        """upgrade a revision"""
        command.upgrade(self.alembic_cfg, revision=revision, sql=sql, tag=None)

    def rollback(self, revision: str) -> None:
        """downgrade revision"""
        command.downgrade(self.alembic_cfg, revision=revision)

    def branches(self, verbose: bool = False) -> None:
        """list all branches"""
        command.branches(self.alembic_cfg, verbose=verbose)

    def show(self, rev: str) -> None:
        """show revision info"""
        command.show(self.alembic_cfg, rev=rev)