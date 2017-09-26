from virga.providers import AbstractProvider


class MockProvider(AbstractProvider):
    def lookup(self, section, identifier, resource_id):
        pass

    def action(self):
        pass
