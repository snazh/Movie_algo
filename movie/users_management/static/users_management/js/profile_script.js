document.addEventListener('DOMContentLoaded', function () {
    const profileForm = document.querySelector('form');
    const inputFields = profileForm.querySelectorAll('input[type="text"], input[type="email"], textarea');
    const initialFieldValues = Array.from(inputFields).map(field => field.value);

    profileForm.addEventListener('submit', function (event) {
        event.preventDefault();

        if (validateFields(inputFields)) {
            inputFields.forEach(function (inputField, index) {
                inputField.disabled = !inputField.disabled;

                if (inputField.disabled) {
                    inputField.style.border = 'none';
                    inputField.value = initialFieldValues[index];
                } else {
                    inputField.style.border = '1px solid white';
                }
            });

            const submitButton = profileForm.querySelector('input[type="submit"]');
            if (inputFields[0].disabled) {
                submitButton.value = 'Edit profile';
                alert('Changes saved!');
            } else {
                submitButton.value = 'Save changes';
            }
        }
    });

    function validateFields(fields) {
        let isValid = true;

        fields.forEach(function (field) {
            if (field.hasAttribute('required') && field.value.trim() === '') {
                alert('Please fill in all required fields.');
                isValid = false;
            }
        });

        return isValid;
    }
});
