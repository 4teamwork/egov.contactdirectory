from ftw.upgrade import UpgradeStep


class AddSupportForLDAPSync(UpgradeStep):
    """Add support for ldap sync.
    """

    def __call__(self):
        self.install_upgrade_profile()
