document.addEventListener('DOMContentLoaded', function() {
    const filterSelect = document.getElementById('categorie');
    
    if (filterSelect) {
        filterSelect.addEventListener('change', function() {
            this.form.submit();
        });
    }
});
