import React, { useState } from "react";

const FileUploader = () => {
    const [selectedFile, setSelectedFile] = useState(null);

    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
    };

    const handleUpload = async () => {
        if (!selectedFile) {
            alert("Valitse tiedosto ensin!");
            return;
        }

        const formData = new FormData();
        formData.append("file", selectedFile);

        const response = await fetch("http://localhost:5000/upload", {
            method: "POST",
            body: formData,
        });

        const data = await response.json();
        alert(data.message);
    };

    return (
        <div>
            <h2>Lataa PDF-tiedosto</h2>
            <input type="file" accept="application/pdf" onChange={handleFileChange} />
            <button onClick={handleUpload}>Lähetä</button>
        </div>
    );
};

export default FileUploader;
