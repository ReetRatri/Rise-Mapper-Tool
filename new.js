document.getElementById('fileInput').addEventListener('change', function(event) {
    const fileInput = event.target;
    const file = fileInput.files[0];
 
    if (file) {
        // Get the file name
        const fileName = file.name;
        // Get the file path (only the name, not the full path for security reasons)
        document.getElementById('filePath').textContent = `Selected file: ${fileName}`;
 
        // If you need to read the file content
        const reader = new FileReader();
        reader.onload = function(e) {
            const fileContent = e.target.result;
            console.log('File content:', fileContent);
        };
        reader.readAsText(file);  // You can use readAsArrayBuffer or readAsDataURL depending on the file type
    } else {
        document.getElementById('filePath').textContent = 'No file selected';
    }
});