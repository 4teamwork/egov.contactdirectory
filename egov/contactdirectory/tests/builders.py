from ftw.builder import builder_registry
from ftw.builder.content import ImageBuilder


class ContactBuilder(ImageBuilder):
    portal_type = 'Contact'

    def with_photo(self):
        self.with_dummy_content()
        self.arguments['image'] = self.arguments['file']
        return self

builder_registry.register('contact', ContactBuilder)
