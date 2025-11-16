# 🚀 Wagtail Deployment Checklist (6.2 → 7.2)

## 1. Environment Compatibility

✅ Python version: Ensure compatibility with Python 3.11–3.14 (Wagtail 7.2 supports 3.14).

✅ Django version: Upgrade to Django 5.0/5.1/5.2.x depending on project needs.

✅ PostgreSQL version: Use 12+ (preferably 15 or 16) for long-term support.

✅ Document chosen versions in deployment notes for reproducibility.

## 2. UI & Accessibility Changes

🖼 ImageBlock alt text (6.3)

Test migrations for new ImageBlock usage.

Verify alt text entry in editorial workflows.

🌗 Dark Mode refinements (6.4, 7.0)

Check readability and contrast in admin UI.

Ensure custom branding/themes don’t break in dark mode.

📑 Sidebar overhaul (7.0)

Validate expand/collapse behavior.

Confirm no JS errors in navigation.

Test responsiveness on mobile/tablet.

♿ Accessibility improvements (6.3–7.2)

Verify ARIA labels, keyboard navigation, and screen reader support.

Ensure alt text is enforced in editorial guidelines.

## 3. Editorial Workflow Enhancements

🔄 Preview workflow (7.0)

Test preview states (draft, scheduled, published).

Ensure editors can switch seamlessly between modes.

📦 StreamField UI updates (7.0)

Validate block insertion, drag/drop, and ordering.

Check custom StreamField blocks for compatibility.

⚠️ Error feedback (7.1)

Confirm validation messages are clear and localized.

Test form submissions with invalid data.

## 4. Performance & Reliability

🌲 Page tree performance (7.1)

Benchmark loading times for large hierarchies.

Monitor DB queries during navigation.

⚡ General admin polish (7.2)

Check spacing, iconography, and consistency.

Validate custom admin extensions against new UI.

## 5. Deployment Hygiene

📋 Static assets

Rebuild and collect static files after upgrade.

Verify caching/CDN invalidation.

🧩 JS/CSS modules

Confirm no conflicts with sidebar/navigation scripts.

Test bundling/minification in CI/CD pipeline.

🔒 Security

Apply latest Django/Wagtail security patches.

Confirm database migrations run cleanly.

🧪 Regression testing

Run automated tests for editorial workflows.

Perform manual smoke tests in staging before production rollout.

## 6. Documentation & Training

📖 Update internal docs with:

New ImageBlock usage and alt text guidelines.

Sidebar navigation changes.

Dark mode support.

🎓 Train editors on:

Preview workflow improvements.

Accessibility best practices (alt text, keyboard navigation).

# ✅ Outcome: This checklist ensures smooth upgrades, reliable deployments, and a consistent editorial experience across Wagtail 6.2.4 → 7.2.