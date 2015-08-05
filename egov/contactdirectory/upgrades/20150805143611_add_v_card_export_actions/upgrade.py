from ftw.upgrade import UpgradeStep


class AddVCardExportActions(UpgradeStep):
    """Add v card export actions.
    """

    def __call__(self):
        self.install_upgrade_profile()
