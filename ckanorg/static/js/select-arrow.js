document.addEventListener('DOMContentLoaded', function() {
    const select = document.querySelector('select[name="sort"]');
    const wrapper = select.closest('.select-wrapper');
    let isOpen = false;

    // When select is clicked to open or close
    select.addEventListener('mousedown', function(e) {
        if (isOpen) {
            // If it was open, close it
            isOpen = false;
            wrapper.classList.remove('active');
        } else {
            // If it wasn't open, open it
            isOpen = true;
            wrapper.classList.add('active');
        }
    });

    // When select loses focus
    select.addEventListener('blur', function(e) {
        // Don't remove active immediately, wait to see if it's a click on an option
        setTimeout(() => {
            if (!select.matches(':focus')) {
                isOpen = false;
                wrapper.classList.remove('active');
            }
        }, 100);
    });

    // When an option is selected
    select.addEventListener('change', function(e) {
        isOpen = false;
        wrapper.classList.remove('active');
        this.form.submit();
    });

    // Listen for clicks on the document
    document.addEventListener('click', function(e) {
        // If select was open and click is outside the select
        if (isOpen && !select.contains(e.target)) {
            isOpen = false;
            wrapper.classList.remove('active');
        }
    });

    // Handle form submission
    select.closest('form').addEventListener('submit', function() {
        isOpen = false;
        wrapper.classList.remove('active');
    });
});
