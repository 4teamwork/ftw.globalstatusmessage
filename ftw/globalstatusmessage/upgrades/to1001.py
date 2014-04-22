from ftw.upgrade import UpgradeStep


class UpgradePermission(UpgradeStep):

    def __call__(self):
        self.setup_install_profile(
            'profile-ftw.globalstatusmessage.upgrades:1001')
