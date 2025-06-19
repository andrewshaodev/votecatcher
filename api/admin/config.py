from piccolo_admin.endpoints import create_admin
from api.votecatcher.tables import APIKey

ADMIN = create_admin(
    site_name="VoteCatcher Admin",
    tables=[APIKey],
)
