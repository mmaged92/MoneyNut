Dropzone.options.myDropzone = {
    maxFilesize: 10,        // MB
    acceptedFiles: ".csv",
    headers: {
        "X-CSRFToken": "{{ csrf_token }}"
    },
    init: function() {
        this.on("success", function(file, response) {
            alert("File uploaded successfully!");
        });
    }
};