from ftw.builder import builder_registry
from ftw.builder.content import ArchetypesBuilder
from ftw.builder.content import ATImageBuilder


class ContactBuilder(ATImageBuilder):
    portal_type = 'Contact'

    def with_photo(self):
        self.with_dummy_content()
        self.arguments['image'] = self.arguments['file']
        return self

builder_registry.register('contact', ContactBuilder)


class MemberBuilder(ArchetypesBuilder):
    portal_type = 'Member'

builder_registry.register('member', MemberBuilder)
