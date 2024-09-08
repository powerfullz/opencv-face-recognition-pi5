document.addEventListener('DOMContentLoaded', function () {
    // Upload button
    document.getElementById('uploadFaces').addEventListener('click', function () {
        // Prompt user for the name associated with the image
        const nameInput = document.getElementById('name');
        const name = nameInput.value.trim();
        if (name === null || name.trim() === "") {
            alert("Name is required to upload the image.");
            return; // Exit if the user didn't enter a name
        }

        // Trigger file upload dialog
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = 'image/*'; // Accept only images
        input.onchange = function (event) {
            const file = event.target.files[0];
            if (file) {
                // Handle file upload here
                const formData = new FormData();
                formData.append('file', file);
                formData.append('name', name); // Append the name to the form data

                fetch('/upload_faces', {
                    method: 'POST',
                    body: formData
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            alert("Face uploaded and processed successfully. Page will be refreshed after clicking OK");
                            location.reload();
                        } else {
                            alert("Error: " + data.error);
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        alert("An error occurred while uploading the face.");
                    });
            }
        };
        input.click();
    });

    // Reload faces button
    document.getElementById('reloadFaces').addEventListener('click', function () {
        fetch('/reload_faces', {
            method: 'POST'
        }).then(response => response.json())
            .then(data => {
                console.log(data);
                alert('Faces reloaded successfully.');
                location.reload();
            }).catch(error => {
                console.error(error);
                alert('Failed to reload faces.');
            });
    });

    document.getElementById('takePhoto').addEventListener('click', function () {
        // Prompt user for the name associated with the image
        const nameInput = document.getElementById('name');
        const name = nameInput.value.trim();
        if (name === null || name.trim() === "") {
            alert("Name is required to take a photo.");
            return; // Exit if the user didn't enter a name
        }

        const formData = new FormData();
        formData.append('name', name);

        fetch("/take_photo", {
            method: "POST",
            body: formData
        }).then(response => response.json())
            .then(data => {
                console.log(data);
                alert('Photo taken successfully.');
                location.reload();
            }).catch(error => {
                console.error(error);
                alert('Failed to take photo.');
            })
    });

    document.getElementById('manageData').addEventListener('click', function () {
        fetch("/manage_data").then(response => response.json())
            .then(files => {
                // Create a modal to display the files
                const modal = document.createElement('div');
                modal.id = 'manageDataModal';

                const title = document.createElement('h2');
                title.textContent = 'Select files to delete';
                modal.appendChild(title);
                
                // Add file list with checkboxes
                const fileList = document.createElement('ul');
                files.forEach(file => {
                    const listItem = document.createElement('li');
                    const checkbox = document.createElement('input');
                    checkbox.type = 'checkbox';
                    checkbox.value = file;
                    listItem.appendChild(checkbox);
                    listItem.appendChild(document.createTextNode(file));
                    fileList.appendChild(listItem);
                });
                modal.appendChild(fileList);

                // Add confirm and cancel buttons
                const buttonGroup = document.createElement('div');
                buttonGroup.className = 'button-group';

                const confirmButton = document.createElement('button');
                confirmButton.textContent = 'Confirm';
                confirmButton.addEventListener('click', function () {
                    const checkedFiles = Array.from(fileList.querySelectorAll('input:checked')).map(checkbox => checkbox.value);
                    if (checkedFiles.length > 0) {
                        if (confirm('Are you sure you want to delete the selected files?')) {
                            fetch("/delete_files", {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json'
                                },
                                body: JSON.stringify({ files: checkedFiles })
                            }).then(response => response.json())
                                .then(result => {
                                    alert(result.message);
                                    document.body.removeChild(modal);
                                    location.reload();
                                });
                        }
                    } else {
                        alert('No files selected.');
                    }
                });
                buttonGroup.appendChild(confirmButton);

                const cancelButton = document.createElement('button');
                cancelButton.textContent = 'Cancel';
                cancelButton.addEventListener('click', function () {
                    document.body.removeChild(modal);
                });
                buttonGroup.appendChild(cancelButton);

                modal.appendChild(buttonGroup);

                document.body.appendChild(modal);
            });
    });
});
