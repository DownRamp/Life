require('dotenv').config();

const express = require("express");
const cors = require("cors");
const db_start = require("./config/db.config");
const { logger } = require('./middlewares/logEvents');
const errorHandler = require('./middlewares/errorHandler');
const bodyParser = require('body-parser');

var corsOptions = {
  origin: "http://localhost:8081"
};

const app = express();
app.use(cors(corsOptions));
app.use(logger);
app.use(errorHandler);

// parse requests of content-type - application/json
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
// parse requests of content-type - application/x-www-form-urlencoded
app.use(express.urlencoded({ extended: true }));

db_start()

// routes
require("./routes/auth.routes")(app);
require("./routes/sport.routes")(app);

// simple route
app.get("/", (req, res) => {
  res.json({ message: "WORKING" });
});

// set port, listen for requests
const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}.`);
});
