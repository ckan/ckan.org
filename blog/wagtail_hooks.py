from wagtail import hooks


@hooks.register("after_edit_page")
def before_blog_edit(request, page):
    if (
        request.method == "POST"
        and "author" in request.POST
        and not request.POST["author"]
    ):
        if hasattr(page, "author"):
            page.author = request.user.username
            page.save_revision()
