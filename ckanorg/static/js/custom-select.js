document.addEventListener('DOMContentLoaded', function () {
    function initCustomSelect() {
        const select = document.querySelector('select[name="sort"]');
        if (!select) return;

        const wrapper = select.closest('.select-wrapper');
        if (!wrapper) return;

        // Visually hide native select but keep it accessible
        select.style.position = 'absolute';
        select.style.left = '-9999px';
        select.setAttribute('aria-hidden', 'true');

        // Prevent duplicating the control
        if (wrapper.querySelector('.custom-select-control')) return;

        wrapper.classList.add('has-custom-select');

        // Create control
        const control = document.createElement('div');
        control.className = 'custom-select-control';
        control.tabIndex = 0;
        control.setAttribute('role', 'button');
        control.setAttribute('aria-haspopup', 'listbox');
        control.setAttribute('aria-expanded', 'false');

        const valueDiv = document.createElement('div');
        valueDiv.className = 'custom-select-value';
        valueDiv.textContent = select.options[select.selectedIndex].textContent.trim();
        control.appendChild(valueDiv);

        const arrow = document.createElement('div');
        arrow.className = 'custom-select-arrow';
        control.appendChild(arrow);

        // Insert control before hidden select
        wrapper.insertBefore(control, select);

        // Build list
        const list = document.createElement('ul');
        list.className = 'custom-select-list';
        list.setAttribute('role', 'listbox');
        list.tabIndex = -1;

        Array.from(select.options).forEach(function (opt) {
            const li = document.createElement('li');
            li.className = 'custom-select-option';
            li.setAttribute('data-value', opt.value);
            li.setAttribute('role', 'option');
            li.tabIndex = -1;
            li.textContent = opt.textContent.trim();
            if (opt.selected) li.classList.add('selected');
            list.appendChild(li);
        });

        wrapper.appendChild(list);

        let open = false;
        let focusedIndex = -1;

        function openDropdown() {
            list.classList.add('open');
            control.classList.add('open');
            control.setAttribute('aria-expanded', 'true');
            open = true;
        }

        function closeDropdown() {
            list.classList.remove('open');
            control.classList.remove('open');
            control.setAttribute('aria-expanded', 'false');
            open = false;
            focusedIndex = -1;
        }

        control.addEventListener('click', function (e) {
            e.stopPropagation();
            if (open) closeDropdown(); else openDropdown();
        });

        document.addEventListener('click', function (e) {
            if (!wrapper.contains(e.target)) closeDropdown();
        });

        // Option click
        list.addEventListener('click', function (e) {
            const li = e.target.closest('.custom-select-option');
            if (!li) return;
            selectOption(li);
        });

        function selectOption(li) {
            const value = li.getAttribute('data-value');
            // update native select
            select.value = value;
            // update visuals
            list.querySelectorAll('.custom-select-option').forEach(function (x) { x.classList.remove('selected'); });
            li.classList.add('selected');
            valueDiv.textContent = li.textContent;

            // dispatch change event
            const ev = new Event('change', { bubbles: true });
            select.dispatchEvent(ev);

            // submit the form if present
            const form = select.closest('form');
            if (form) form.submit();
            closeDropdown();
        }

        // Keyboard support
        control.addEventListener('keydown', function (e) {
        const items = Array.from(list.querySelectorAll('.custom-select-option'));
        if (e.key === 'ArrowDown') {
            e.preventDefault();
            if (!open) openDropdown();
            focusedIndex = Math.min(focusedIndex + 1, items.length - 1);
            items[focusedIndex].focus();
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            if (!open) openDropdown();
            focusedIndex = Math.max(focusedIndex - 1, 0);
            items[focusedIndex].focus();
        } else if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            if (!open) { openDropdown(); } else {
            const focused = document.activeElement.closest && document.activeElement.closest('li.custom-select-option');
            if (focused) selectOption(focused);
            }
        } else if (e.key === 'Escape') {
            if (open) { closeDropdown(); }
        }
        });

        // Allow navigation when list has focus
        list.addEventListener('keydown', function (e) {
        const items = Array.from(list.querySelectorAll('.custom-select-option'));
        if (e.key === 'ArrowDown') {
            e.preventDefault();
            focusedIndex = Math.min(focusedIndex + 1, items.length - 1);
            items[focusedIndex].focus();
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            focusedIndex = Math.max(focusedIndex - 1, 0);
            items[focusedIndex].focus();
        } else if (e.key === 'Enter') {
            e.preventDefault();
            const focused = document.activeElement.closest && document.activeElement.closest('li.custom-select-option');
            if (focused) selectOption(focused);
        } else if (e.key === 'Escape') {
            closeDropdown();
            control.focus();
        }
        });

        // sync when native select changes programmatically
        select.addEventListener('change', function () {
        const opt = select.options[select.selectedIndex];
        valueDiv.textContent = opt.textContent.trim();
        list.querySelectorAll('.custom-select-option').forEach(function (x) { x.classList.toggle('selected', x.getAttribute('data-value') === opt.value); });
        });
    }

    initCustomSelect();
});
