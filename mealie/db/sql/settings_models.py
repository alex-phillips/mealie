import sqlalchemy as sa
import sqlalchemy.orm as orm
from db.sql.model_base import BaseMixins, SqlAlchemyBase


class SiteSettingsModel(SqlAlchemyBase):
    __tablename__ = "site_settings"
    name = sa.Column(sa.String, primary_key=True)
    webhooks = orm.relationship("WebHookModel", uselist=False, cascade="all, delete")

    def __init__(self, name: str = None, webhooks: dict = None) -> None:
        self.name = name
        self.webhooks = WebHookModel(**webhooks)

    def update(self, session, name, webhooks: dict) -> dict:
        self.name = name
        self.webhooks.update(session=session, **webhooks)
        return

    def dict(self):
        data = {"name": self.name, "webhooks": self.webhooks.dict()}
        return data


class WebHookModel(SqlAlchemyBase, BaseMixins):
    __tablename__ = "webhook_settings"
    id = sa.Column(sa.Integer, primary_key=True)
    parent_id = sa.Column(sa.String, sa.ForeignKey("site_settings.name"))
    webhookURLs = orm.relationship(
        "WebhookURLModel", uselist=True, cascade="all, delete"
    )
    webhookTime = sa.Column(sa.String, default="00:00")
    enabled = sa.Column(sa.Boolean, default=False)

    def __init__(
        self, webhookURLs: list, webhookTime: str, enabled: bool = False
    ) -> None:

        self.webhookURLs = [WebhookURLModel(url=x) for x in webhookURLs]
        self.webhookTime = webhookTime
        self.enabled = enabled

    def update(
        self, session, webhookURLs: list, webhookTime: str, enabled: bool
    ) -> None:

        self._sql_remove_list(session, [WebhookURLModel], self.id)

        self.__init__(webhookURLs, webhookTime, enabled)

    def dict(self):
        data = {
            "webhookURLs": [url.to_str() for url in self.webhookURLs],
            "webhookTime": self.webhookTime,
            "enabled": self.enabled,
        }
        return data


class WebhookURLModel(SqlAlchemyBase):
    __tablename__ = "webhook_urls"
    id = sa.Column(sa.Integer, primary_key=True)
    url = sa.Column(sa.String)
    parent_id = sa.Column(sa.Integer, sa.ForeignKey("webhook_settings.id"))

    def to_str(self):
        return self.url
