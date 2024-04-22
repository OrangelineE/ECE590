document.addEventListener('DOMContentLoaded', () => {
    // Attach event listeners to each "Save Reminder" button
    document.querySelectorAll('[id^="saveReminderButton-"]').forEach(button => {
        button.addEventListener('click', function() {
            const slotId = this.id.split('-')[1];
            saveReminder(slotId);
        });
    });
});

function saveReminder(slotId) {
    const quantityInput = document.getElementById(`quantity-${slotId}`);
    const frequencySelect = document.getElementById(`frequency-${slotId}`);
    const timeInput = document.getElementById(`time-${slotId}`);

    const reminderData = {
        slot_id: slotId,
        alarm_time: `${new Date().toISOString().split('T')[0]}T${timeInput.value}:00`,
        frequency: frequencySelect.value,
        quantity: parseInt(quantityInput.value, 10)
    };

    fetch('/add_reminder', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify(reminderData),
        credentials: 'same-origin'
    })
    .then(response => {
        console.log(response); // Log the raw response
        if (!response.ok) {
            return response.text().then(text => { throw new Error(text) });
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);

        let modalElement = document.getElementById(`reminderModal-${slotId}`);
        let modalInstance = bootstrap.Modal.getInstance(modalElement);
        modalInstance.hide();
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
