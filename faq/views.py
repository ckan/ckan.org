from wagtail.log_actions import log
from wagtail.snippets.views.snippets import CreateView

from .models import FaqPage


class FaqCreateView(CreateView):
    def save_instance(self):
        """
        Called after the form is successfully validated - saves the object to the db
        and returns the new object.
        """
        parent = FaqPage.objects.first()

        if self.draftstate_enabled:
            instance = self.form.save(commit=False)

            if not instance.owner:
                instance.owner = self.request.user

            # If DraftStateMixin is applied, only save to the database in CreateView,
            # and make sure the live field is set to False.
            if self.view_name == "create":
                instance.live = False
                parent.add_child(instance=instance)
                self.form.save_m2m()
        else:
            instance = self.form.save()

        self.has_content_changes = self.view_name == "create" or self.form.has_changed()

        # Save revision if the model inherits from RevisionMixin
        self.new_revision = None
        if self.revision_enabled:
            self.new_revision = instance.save_revision(user=self.request.user)

        log(
            instance=instance,
            action="wagtail.create" if self.view_name == "create" else "wagtail.edit",
            revision=self.new_revision,
            content_changed=self.has_content_changes,
        )

        return instance
