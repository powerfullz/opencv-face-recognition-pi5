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
        let input = document.createElement('input');
        input.type = 'file';
        input.accept = 'image/*'; // Accept only images
        input.onchange = function (event) {
            let file = event.target.files[0];
            if (file) {
                // Handle file upload here
                let formData = new FormData();
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
                alert('Faces reloaded successfully!');
                location.reload();
            }).catch(error => {
                console.error(error);
                alert('Failed to reload faces.');
            });
    });

    document.getElementById('takePhoto').addEventListener('click', function () {
        alert('This feature is under development.');
    });

    document.getElementById('manageData').addEventListener('click', function () {
        alert('This feature is under development.');
    });
});
