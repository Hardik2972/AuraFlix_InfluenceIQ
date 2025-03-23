const express = require('express');
const app = express();
require('dotenv').config();

// Middleware
app.use(express.json());


// Start Server
app.listen(process.env.PORT, () => {
  console.log(`Server is running on http://localhost:${process.env.PORT}`);
});
