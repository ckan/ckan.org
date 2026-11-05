"""Sync "Get notified of new stories" sign-ups to Mailchimp.

Subscribers go to their own audience (MailChimpSettings.stories_audience_id),
never the newsletter audience: the sign-up form promises "stories updates only,
no newsletters".

New addresses are added as ``pending``, so Mailchimp sends its own
confirmation e-mail (double opt-in) - anyone can type any address into the
form. Existing members keep their current status, so someone who unsubscribed
is never silently re-subscribed. The call is an idempotent upsert and is safe
to repeat.
"""

import hashlib
import logging

import mailchimp_marketing as MailchimpMarketing
import requests
from mailchimp_marketing.api_client import ApiClientError

logger = logging.getLogger("error_logger")


def sync_story_subscriber(mailchimp_settings, email: str) -> bool:
    """Upsert ``email`` into the stories audience.

    Returns ``True`` when Mailchimp accepted the request. Failures are logged
    and never raised: the address is already stored locally and can be
    re-synced with ``manage.py sync_story_subscribers``.
    """
    api_key = mailchimp_settings.api_key
    audience_id = mailchimp_settings.stories_audience_id
    if not (api_key and audience_id):
        logger.warning("Mailchimp stories audience is not configured; story subscriber not synced")
        return False

    client = MailchimpMarketing.Client()
    client.set_config({"api_key": api_key, "server": api_key.split("-")[-1]})
    subscriber_hash = hashlib.md5(email.lower().encode("utf-8")).hexdigest()
    try:
        client.lists.set_list_member(
            audience_id,
            subscriber_hash,
            {"email_address": email, "status_if_new": "pending"},
        )
    except ApiClientError as error:
        logger.error("Mailchimp rejected story subscriber %s: %s", subscriber_hash, error.text)
        return False
    except requests.RequestException:
        logger.exception("Could not reach Mailchimp for story subscriber %s", subscriber_hash)
        return False
    return True
