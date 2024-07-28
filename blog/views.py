from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.views.generic.list import ListView

from wagtail.admin import messages
from wagtail.log_actions import log
from wagtail.snippets.views.snippets import CreateView

from .models import BlogListingPage, BlogPostPage, PostCategoryPage


class UsersBlogPostListView(ListView):
    model = BlogPostPage

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_name = self.kwargs.get("username", "")
        author = User.objects.get(username=user_name)
        context["posts"] = BlogPostPage.objects.filter(owner=author.id)
        context["author"] = author
        return context


class TagsBlogPostListView(ListView):
    model = BlogPostPage

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = self.kwargs.get("tag", "")
        context["posts"] = BlogPostPage.objects.filter(tags__name=tag)
        context["tag"] = tag
        return context


class CategoriesBlogPostListView(ListView):
    model = BlogPostPage

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat_id = self.kwargs.get("cat_id", "")
        if cat_id == 0:
            context["posts"] = BlogPostPage.objects.all()
        else:
            context["posts"] = BlogPostPage.objects.filter(category=cat_id).order_by(
                "-last_published_at"
            )
            context["categories"] = PostCategoryPage.objects.all().order_by(
                "category_title"
            )
            context["cat_selected"] = PostCategoryPage.objects.filter(id=cat_id).first()
        return context


class SearchBlogPostListView(ListView):
    model = BlogPostPage

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            if self.get_paginate_by(self.object_list) is not None and hasattr(
                self.object_list, "exists"
            ):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(
                    _("Empty list and “%(class_name)s.allow_empty” is False.")
                    % {
                        "class_name": self.__class__.__name__,
                    }
                )

        search_query = request.GET.get("query", None)
        if search_query:
            search_results = (
                BlogPostPage.objects.order_by("-last_published_at")
                .live()
                .autocomplete(
                    search_query,
                    fields=["post_title", "post_subtitle"],
                    order_by_relevance=False
                )
            )
        else:
            search_results = BlogPostPage.objects.none()
        context = self.get_context_data()
        context["posts"] = search_results
        context["query"] = search_query
        return self.render_to_response(context)


class ProfileCreateView(CreateView):
    def form_valid(self, form):
        form.instance.user = self.request.user
        instance = form.save()
        messages.success(
            self.request,
            self.get_success_message(instance),
            buttons=self.get_success_message_buttons(instance),
        )
        return redirect(self.get_success_url())


class PostCreateView(CreateView):
    def save_instance(self):
        """
        Called after the form is successfully validated - saves the object to the db
        and returns the new object.
        """
        parent = BlogListingPage.objects.first()

        if self.draftstate_enabled:
            instance = self.form.save(commit=False)

            if not instance.author:
                instance.author = self.request.user

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
