document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('uploadFaces').addEventListener('click', function () {
        // Prompt user for the name associated with the image
        let name = prompt("Please enter the name associated with the image:");
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
                }).then(response => response.json())
                    .then(data => {
                        console.log(data);
                        alert('Faces uploaded successfully!');
                    }).catch(error => {
                        console.error(error);
                        alert('Failed to upload faces.');
                    });
            }
        };
        input.click();
    });

    document.getElementById('reloadFaces').addEventListener('click', function () {
        fetch('/reload_faces', {
            method: 'POST'
        }).then(response => response.json())
            .then(data => {
                console.log(data);
                alert('Faces reloaded successfully!');
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
