class PermissionsManager:
    def __init__(self):
        self.user_permissions = {}

    def set_permission(self, user_id, permission_level):
        self.user_permissions[user_id] = permission_level

    def get_permission(self, user_id):
        return self.user_permissions.get(user_id, "guest")

    def has_permission(self, user_id, required_level):
        user_level = self.get_permission(user_id)
        levels = ["guest", "user", "admin"]
        return levels.index(user_level) >= levels.index(required_level)
