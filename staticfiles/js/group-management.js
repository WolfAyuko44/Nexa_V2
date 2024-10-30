// group-management.js

document.addEventListener('DOMContentLoaded', function() {
    const addMemberButton = document.querySelector('#add-member');
    const memberList = document.querySelector('#member-list');
    const groupId = document.querySelector('body').dataset.groupId;

    if (addMemberButton) {
        addMemberButton.addEventListener('click', function() {
            const newMember = prompt('Enter the username of the new member:');
            if (newMember) {
                fetch(`/api/groups/${groupId}/members`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken()  // Adjust according to your setup
                    },
                    body: JSON.stringify({ username: newMember })
                })
                .then(response => response.json())
                .then(data => {
                    memberList.innerHTML += `<li>${newMember}</li>`;
                })
                .catch(error => console.error('Error adding member:', error));
            }
        });
    }

    function getCSRFToken() {
        const token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        return token;
    }
});
