const express = require("express");
const multer = require("multer");
const fs = require("fs");
const path = require("path");
const cors = require("cors");

const app = express();
app.use(cors());

// Määritetään tallennuspolku
const uploadPath = "C:/Talobot/data";

// Varmistetaan, että hakemisto on olemassa
if (!fs.existsSync(uploadPath)) {
    fs.mkdirSync(uploadPath, { recursive: true });
}

// Tiedoston tallennusasetukset
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, uploadPath);
    },
    filename: (req, file, cb) => {
        cb(null, "1.pdf"); // Tallenna aina nimellä "1.pdf"
    }
});

const upload = multer({ storage });

// Reitti tiedoston lataamiseen
app.post("/upload", upload.single("file"), (req, res) => {
    res.send({ message: "Tiedosto tallennettu onnistuneesti C:/Talobot/data/1.pdf" });
});

// Käynnistä palvelin
app.listen(5000, () => console.log("Palvelin käynnissä portissa 5000"));
