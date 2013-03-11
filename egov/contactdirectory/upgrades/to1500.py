from ftw.upgrade import UpgradeStep


class MigrateSimplelayoutActions(UpgradeStep):

    def __call__(self):
        self.setup_install_profile(
            'profile-egov.contactdirectory.upgrades:1500')
