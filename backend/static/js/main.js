document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('flightForm');
    
    // Dynamic destination filtering
    const sourceSelect = document.getElementById('source_city');
    const destSelect = document.getElementById('destination_city');
    
    sourceSelect.addEventListener('change', function() {
        const selectedSource = this.value;
        Array.from(destSelect.options).forEach(option => {
            option.style.display = option.value === selectedSource ? 'none' : '';
        });
        destSelect.value = '';
    });

    // Form validation
    form.addEventListener('submit', function(e) {
        let isValid = true;
        
        // Validate all required fields
        document.querySelectorAll('[required]').forEach(field => {
            if (!field.value) {
                field.classList.add('is-invalid');
                isValid = false;
            } else {
                field.classList.remove('is-invalid');
            }
        });

        // Validate days_left
        const daysLeft = document.getElementById('days_left');
        if (daysLeft.value < 1) {
            daysLeft.classList.add('is-invalid');
            isValid = false;
        }

        if (!isValid) {
            e.preventDefault();
            alert('Please fill all required fields correctly');
        }
    });
});